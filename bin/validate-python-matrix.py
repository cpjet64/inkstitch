#!/usr/bin/env python3

"""Run install + lint + type-check + tests across local versioned venvs."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

SUPPORTED_VERSIONS = ["39", "310", "311", "312", "313"]
EXPERIMENTAL_VERSIONS = ["314"]

RUFF_TARGETS = ["lib", "tests"]


def venv_python(version: str) -> Path:
    venv_dir = Path(f".venv{version}")
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def run_cmd(cmd: list[str], label: str) -> int:
    print(f"[matrix] {label}: {' '.join(cmd)}")
    completed = subprocess.run(cmd)
    return completed.returncode


def validate_version(version: str, skip_install: bool, strict_mypy: bool, run_ruff: bool) -> int:
    python_path = venv_python(version)
    if not python_path.exists():
        print(f"[matrix] .venv{version}: missing interpreter at {python_path}")
        return 1

    print(f"[matrix] ===== Python {version} =====")

    if not skip_install:
        if run_cmd([str(python_path), "-m", "pip", "install", "--upgrade", "pip", "wheel"], f".venv{version} install bootstrap") != 0:
            return 1
        if run_cmd([str(python_path), "-m", "pip", "install", "-r", "requirements.txt"], f".venv{version} install requirements") != 0:
            return 1

    blocking_checks = [
        ([str(python_path), "-m", "pytest", "-q"], f".venv{version} pytest"),
    ]

    if run_ruff:
        blocking_checks.append(([str(python_path), "-m", "ruff", "check", *RUFF_TARGETS], f".venv{version} ruff"))

    for cmd, label in blocking_checks:
        if run_cmd(cmd, label) != 0:
            return 1

    mypy_cmd = [str(python_path), "-m", "mypy"]
    mypy_label = f".venv{version} mypy"
    mypy_rc = run_cmd(mypy_cmd, mypy_label)
    if mypy_rc != 0:
        if strict_mypy:
            return 1
        print(f"[matrix] {mypy_label}: non-blocking failure (matches CI behavior)")

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--versions",
        default=",".join(SUPPORTED_VERSIONS),
        help="Comma-separated venv suffixes, e.g. 39,310,311,312,313",
    )
    parser.add_argument(
        "--include-experimental",
        action="store_true",
        help="Also include experimental versions (currently: 314).",
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip pip install steps and only run checks.",
    )
    parser.add_argument(
        "--strict-mypy",
        action="store_true",
        help="Treat mypy failures as blocking. By default, mypy is non-blocking to match CI.",
    )
    parser.add_argument(
        "--ruff-once",
        action="store_true",
        help="Run ruff only once on the first version (default runs ruff for every version).",
    )
    parser.add_argument(
        "--flake8-once",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    versions = [v.strip() for v in args.versions.split(",") if v.strip()]
    if args.include_experimental:
        versions.extend(EXPERIMENTAL_VERSIONS)

    failures = []
    for index, version in enumerate(versions):
        run_ruff = (not (args.ruff_once or args.flake8_once)) or index == 0
        if validate_version(version, args.skip_install, args.strict_mypy, run_ruff) != 0:
            failures.append(version)

    if failures:
        print(f"[matrix] FAILED versions: {', '.join(failures)}")
        return 1

    print("[matrix] All versions passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
