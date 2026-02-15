#!/usr/bin/env python3

"""Run pip-audit and enforce a waiver baseline policy."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Waiver:
    package: str
    vuln_id: str
    owner: str
    reason: str
    expires: date


@dataclass(frozen=True)
class Finding:
    package: str
    vuln_id: str
    fix_versions: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--waivers",
        default=".ci/audit-waivers.json",
        help="Path to waiver baseline JSON file.",
    )
    parser.add_argument(
        "--requirements",
        default=None,
        help="Optional requirements file path for pip-audit (-r).",
    )
    return parser.parse_args()


def load_waivers(path: Path) -> tuple[dict[tuple[str, str], Waiver], list[str]]:
    errors: list[str] = []
    if not path.exists():
        return {}, [f"Waiver file not found: {path}"]

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, [f"Invalid JSON in {path}: {exc}"]

    entries = payload.get("waivers", [])
    if not isinstance(entries, list):
        return {}, [f"Invalid format in {path}: 'waivers' must be a list"]

    waivers: dict[tuple[str, str], Waiver] = {}
    required_fields = {"package", "id", "owner", "reason", "expires"}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"Waiver #{index + 1} must be an object")
            continue

        missing = sorted(required_fields - set(entry))
        if missing:
            errors.append(f"Waiver #{index + 1} missing fields: {', '.join(missing)}")
            continue

        package = str(entry["package"]).strip().lower()
        vuln_id = str(entry["id"]).strip().lower()
        owner = str(entry["owner"]).strip()
        reason = str(entry["reason"]).strip()
        expires_raw = str(entry["expires"]).strip()

        if not package or not vuln_id or not owner or not reason or not expires_raw:
            errors.append(f"Waiver #{index + 1} has blank required fields")
            continue

        try:
            expires = date.fromisoformat(expires_raw)
        except ValueError:
            errors.append(f"Waiver #{index + 1} has invalid expires date: {expires_raw}")
            continue

        key = (package, vuln_id)
        if key in waivers:
            errors.append(f"Duplicate waiver entry for package={package}, id={vuln_id}")
            continue

        waivers[key] = Waiver(
            package=package,
            vuln_id=vuln_id,
            owner=owner,
            reason=reason,
            expires=expires,
        )

    return waivers, errors


def run_pip_audit(requirements: str | None) -> tuple[dict[str, Any] | None, str]:
    cmd = [sys.executable, "-m", "pip_audit", "--format", "json", "--progress-spinner", "off"]
    if requirements:
        cmd.extend(["-r", requirements])

    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode not in (0, 1):
        stderr = completed.stderr.strip()
        stdout = completed.stdout.strip()
        details = stderr or stdout or "pip-audit failed without output"
        return None, details

    try:
        payload = json.loads(completed.stdout or "{}")
    except json.JSONDecodeError as exc:
        return None, f"Failed to parse pip-audit JSON output: {exc}"

    return payload, completed.stderr.strip()


def collect_findings(payload: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    dependencies = payload.get("dependencies", [])
    if not isinstance(dependencies, list):
        return findings

    for dependency in dependencies:
        if not isinstance(dependency, dict):
            continue
        package = str(dependency.get("name", "")).strip().lower()
        if not package:
            continue

        vulns = dependency.get("vulns", [])
        if not isinstance(vulns, list):
            continue

        for vuln in vulns:
            if not isinstance(vuln, dict):
                continue
            vuln_id = str(vuln.get("id", "")).strip().lower()
            if not vuln_id:
                continue
            raw_fix_versions = vuln.get("fix_versions", [])
            fix_versions = [str(version).strip() for version in raw_fix_versions if str(version).strip()]
            findings.append(Finding(package=package, vuln_id=vuln_id, fix_versions=fix_versions))

    return findings


def find_waiver(waivers: dict[tuple[str, str], Waiver], finding: Finding) -> Waiver | None:
    return waivers.get((finding.package, finding.vuln_id)) or waivers.get(("*", finding.vuln_id))


def format_fix_versions(fix_versions: list[str]) -> str:
    if not fix_versions:
        return "no fix published"
    return ", ".join(fix_versions)


def main() -> int:
    args = parse_args()
    waivers, waiver_errors = load_waivers(Path(args.waivers))
    if waiver_errors:
        print("[audit] Waiver configuration errors:", file=sys.stderr)
        for error in waiver_errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    payload, audit_error = run_pip_audit(args.requirements)
    if payload is None:
        print(f"[audit] {audit_error}", file=sys.stderr)
        return 1

    findings = collect_findings(payload)
    today = date.today()

    unwaived: list[Finding] = []
    expired: list[tuple[Finding, Waiver]] = []
    active: list[tuple[Finding, Waiver]] = []

    for finding in findings:
        waiver = find_waiver(waivers, finding)
        if waiver is None:
            unwaived.append(finding)
            continue
        if waiver.expires < today:
            expired.append((finding, waiver))
            continue
        active.append((finding, waiver))

    if active:
        print("[audit] Active waivers applied:")
        for finding, waiver in active:
            print(f"  - {finding.package} {finding.vuln_id} " f"(owner: {waiver.owner}, expires: {waiver.expires.isoformat()})")

    if expired:
        print("[audit] Expired waivers must be renewed or removed:", file=sys.stderr)
        for finding, waiver in expired:
            print(
                f"  - {finding.package} {finding.vuln_id} " f"(expired {waiver.expires.isoformat()}, owner: {waiver.owner})",
                file=sys.stderr,
            )

    if unwaived:
        print("[audit] Unwaived vulnerabilities found:", file=sys.stderr)
        for finding in unwaived:
            print(
                f"  - {finding.package} {finding.vuln_id} " f"(fixes: {format_fix_versions(finding.fix_versions)})",
                file=sys.stderr,
            )

    if expired or unwaived:
        return 1

    if findings:
        print(f"[audit] All {len(findings)} vulnerabilities are covered by active waivers.")
    else:
        print("[audit] No vulnerabilities found.")

    if audit_error:
        print(audit_error)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
