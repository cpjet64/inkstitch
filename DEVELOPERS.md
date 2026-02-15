# DEVELOPERS.md

Master guide for development workflows in this repository.

## Maintenance Contract

| Field | Value |
| --- | --- |
| Status | Canonical developer-process guide |
| Owners | Ink/Stitch core maintainers |
| Last reviewed | 2026-02-15 |
| Update trigger | Any change to tooling, CI workflows, build/release steps, debug workflow, docs workflow, or contribution policy |
| Required companion updates | `README.md` links, related workflow files under `.github/workflows/`, and any affected templates/scripts |

## 1. Purpose and Audience

This document is for:

1. New contributors who need a reliable path from clone to first PR.
2. Existing contributors who need day-to-day commands and standards.
3. Maintainers who need release, CI/CD, localization, and policy references in one place.

## 2. How To Use This Document

Use one of these paths:

1. New developer path:
   Read sections `3` through `9`, then `11`, `13`, and `17`.
2. Experienced developer path:
   Jump to sections `8`, `9`, `10`, `11`, `13`, and `17` for operational work.
3. Maintainer path:
   Focus on sections `14`, `18`, `19`, `20`, `22`, and `23`.

## 3. Source-of-Truth Hierarchy

When guidance overlaps, use this precedence:

1. `DEVELOPERS.md` (this file): development process and operational workflow.
2. `CODING_STYLE.md`: coding readability/style principles.
3. `CONTRIBUTING.md`: contribution norms and participation entry points.
4. `CODE_OF_CONDUCT.md`: behavior and interaction standards.
5. `README.md`: project overview and user-facing entry point.
6. Workflow files and scripts: `.github/workflows/*`, `Makefile`, `bin/*` are the executable contract.

## 4. Fast Start (15 Minutes)

### 4.1 Windows (PowerShell; Git Bash optional)

```powershell
py -3.13 -m venv .venv/3.13
.venv\3.13\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel
python -m pip install -r requirements.txt
python -m pytest -q
python -m mypy
```

If PowerShell execution policy blocks activation, run commands via the venv interpreter directly:
`.\.venv\3.13\Scripts\python.exe -m <command>`.

Style check options:

```powershell
# Preferred (matches CI script):
bash -x bin/style-check

# Fallback when bash is unavailable:
python -m ruff check .
```

### 4.2 Linux

```bash
python3.13 -m venv .venv/3.13
source .venv/3.13/bin/activate
python -m pip install --upgrade pip wheel
python -m pip install -r requirements.txt
python -m pytest -q
python -m mypy
make style
```

### 4.3 macOS

```bash
python3.13 -m venv .venv/3.13
source .venv/3.13/bin/activate
python -m pip install --upgrade pip wheel
python -m pip install -r requirements.txt
python -m pytest -q
python -m mypy
make style
```

## 5. Python Version Policy and venv Naming

Current repository reality:

1. CI test workflow is matrix-gated for Python `3.9` through `3.13` (`.github/workflows/test.yml`).
2. Build/release workflows currently package with Python `3.11.x` (`.github/workflows/build.yml`).
3. Translation automation currently runs on Python `3.12.x` (`.github/workflows/translations.yml`).

Contributor default:

1. Use Python `3.13` for day-to-day development unless a task explicitly targets another version.

Local venv naming convention:

1. `.venv/3.13` (primary contributor environment)
2. Optional extra interpreters use `.venv/<major.minor>` (example: `.venv/3.11`)

Rule: keep `.venv/<major.minor>` stable so `.gitignore` and automation expectations stay predictable.

## 6. Repo Map (Top-Level)

1. `inkstitch.py`: entrypoint and runtime bootstrapping.
2. `lib/`: core Python code.
3. `lib/extensions/`: Inkscape extension implementations.
4. `lib/stitches/`: stitch-generation algorithms.
5. `lib/elements/`: SVG element abstractions and conversion logic.
6. `lib/stitch_plan/`: stitch plan data structures and generation helpers.
7. `lib/debug/`: debug, logging, and profiling support.
8. `templates/`: INX/XML templates for extension UI integration.
9. `tests/`: automated tests.
10. `bin/`: build/helper scripts.
11. `.github/workflows/`: CI/CD workflow definitions.
12. `print/`: print/export web assets and templates.

## 7. Architecture Overview

High-level flow:

1. Read/parse inputs:
   `lib/svg/*`, `lib/elements/*`, `lib/stitch_plan/read_file.py`.
2. Convert to embroidery structures:
   element classes and stitch-plan generation code.
3. Apply stitch algorithms:
   `lib/stitches/*` and related helpers.
4. Encode/write machine formats:
   `lib/output.py` through `pystitch`.

Where to add new output formats:

1. Writer behavior and format options in `lib/output.py`.
2. Output extension wiring in `lib/extensions/output.py` or related export extension.
3. INX/UI exposure in `templates/*.xml` and `lib/inx/*` generation helpers.
4. Regression coverage in `tests/test_output.py` and extension-level tests.

## 8. Daily Workflow Commands

Core loop:

```bash
python -m pytest -q
python -m mypy
# preferred where bash/make are available
make style
```

Additional useful commands:

```bash
make inx
make locales
make messages.po
make dist
make matrix-check
make matrix-check-fast
bash .githooks/install.sh
```

Notes:

1. `make style` runs `bin/style-check` with project Ruff settings.
2. On Windows without `bash`, run the equivalent `python -m ruff check .` command from section `4.1`.
3. `mypy` uses repository `mypy.ini`.
4. `pytest` scope is controlled by `pytest.ini` (`tests/`).
5. `make matrix-check` runs `nox` across supported versions (`3.9`-`3.13`) for tests + Ruff + mypy.
6. `make matrix-check-fast` runs the quick local nox session (`quick-3.13`) for iterative development.
7. Nox prefers uv-backed virtual environments when `uv` is available and falls back to `virtualenv` otherwise.
8. Ruff excludes local virtualenv folders (`.venv*`) to avoid non-project noise and excessive runtime.
9. Git hook workflow:
   `pre-commit` runs fast staged-file checks (syntax + Ruff + Black check), while `pre-push` runs strict nox validation.
10. Install hooks once per clone with `bash .githooks/install.sh` (or `.\.githooks\install.ps1` on Windows PowerShell).

## 9. Validation Matrix

| Stage | Minimum required locally |
| --- | --- |
| Before commit | Let `pre-commit` run fast staged-file checks; add targeted tests for changed area when behavior changes |
| Before push | Let `pre-push` run strict nox checks (`ci` + `package-3.13` + `audit-3.13`) |
| Before PR | `python -m pytest -q`, `python -m mypy`, style check (`make style` or direct `python -m ruff check .`) |
| Before release/tag | Full test suite, style, mypy, plus packaging sanity (`make dist` on release platform) |

Evidence to include in PR description:

1. Commands run.
2. Pass/fail status.
3. Any intentionally skipped checks with reason.

## 10. Public API Stability Rules

Treat the following as stability-sensitive:

1. Extension names/parameters exposed via INX templates (`templates/*.xml` and generated INX output).
2. User-visible export behavior and output semantics in core format paths.
3. User-facing configuration file keys in debug/logging templates when documented.

Deprecation policy:

1. Prefer additive changes first.
2. Keep backward compatibility for at least one release cycle when practical.
3. Document behavior changes in PR notes and release notes.

Versioning expectation:

1. Breaking behavior needs explicit maintainer sign-off and release-note callout.
2. Silent behavior changes in export/output code are not acceptable without regression tests.

## 11. Coding and Readability Standards

Primary references:

1. `CODING_STYLE.md`
2. `CONTRIBUTING.md`
3. `CODE_OF_CONDUCT.md`

Required coding rules:

1. Optimize for readability over cleverness.
2. Use descriptive names and explicit control flow.
3. Add comments for non-obvious logic, especially embroidery-domain decisions.
4. Prefer small, focused functions over deeply nested blocks.

Type hints:

1. Type annotations are encouraged.
2. Run `python -m mypy` on changed areas.

Comment/docstring policy (team target):

1. Public function docstring coverage in `lib/`: 100%.
2. Public class docstring coverage in `lib/`: 100%.
3. Add "why" comments for complex branch-heavy logic.
4. Any function longer than 60 lines should have section comments for stages.
5. Non-trivial exception handlers should explain failure mode and recovery intent.

Debug/print policy:

1. Prefer structured logging/debug systems over ad-hoc `print(...)`.
2. Direct prints are allowed only for intentional CLI/error surface behavior.

## 12. Debug Harness Guide (Current System + Planned Direction)

Current debug stack:

1. `DEBUG_template.toml` -> copy to `DEBUG.toml`.
2. Optional `LOGGING.toml` (or `LOGGING1.toml`, etc.) via `LOGGING.log_config_file`.
3. Runtime support in `lib/debug/*`.

Key toggles:

1. `DEBUG.debug_enable` and `DEBUG.debug_type` (`vscode`, `pycharm`, `pydev`).
2. `PROFILE.profile_enable` and `PROFILE.profiler_type` (`cprofile`, `profile`, `pyinstrument`, `monkeytype`).
3. Environment overrides:
   `INKSTITCH_DEBUG_ENABLE`, `INKSTITCH_PROFILE_ENABLE`, `INKSTITCH_LOGLEVEL`.

Mode recipes:

1. File logging only:
   use default development logging or `LOGGING_template.toml` with file handlers.
2. Console logging:
   define a stream handler in `LOGGING.toml` and assign it to `inkstitch`/`root`.
3. Console + file:
   configure both handler types in `LOGGING.toml`.

Operational rule:

1. New debug output should be routed through logging/debug infrastructure, not scattered prints.

## 13. Testing Standards

Test layout and naming:

1. Files under `tests/` using `test_*.py`.
2. Name tests as `test_<unit>_<behavior>`.

Change-type expectations:

1. Bug fix:
   include at least one regression test that fails without the fix.
2. Behavior change:
   include positive and negative path coverage.
3. Error handling changes:
   assert user-facing messages and exit behavior.
4. Export pipeline changes:
   add cross-call and mutation safety tests where applicable.

Mocking and fixtures:

1. Patch at module boundaries (`lib.output.pystitch.write` style) rather than deep internals.
2. Keep fixtures explicit and local to behavior under test.
3. Use stable assertions focused on behavior, not incidental implementation details.

Test readability:

1. Use Arrange/Act/Assert comments for non-trivial tests.
2. Prefer clear, scenario-driven setup names.

## 14. Commit and PR Standards

Commit message format:

1. `<area>: <imperative summary>`
2. Example: `output: avoid settings mutation between exports`

Commit quality rules:

1. Keep commits focused and logically atomic.
2. Include tests in the same commit when feasible for behavioral changes.
3. Avoid unrelated formatting churn.

PR checklist:

1. Explain problem and root cause.
2. Describe solution and tradeoffs.
3. Include validation evidence (commands + results).
4. Include test coverage notes.
5. Include docs/localization impact notes.

## 15. CI/CD Contract

Current workflows:

1. `.github/workflows/test.yml`:
   runs on PR/push to `main` with Python `3.9`-`3.13` through nox `ci-*`, plus `packaging+py3.13`.
   Also includes `audit+py3.13` as a blocking check with waiver policy.
2. `.github/workflows/dependency-review.yml`:
   runs on PRs that touch dependency manifests or workflow files and blocks on high-severity supply-chain risk.
3. `.github/dependabot.yml`:
   weekly update automation for pip dependencies and GitHub Actions references.
4. `.github/workflows/build.yml`:
   builds and tests Linux/Windows/macOS artifacts, then creates or updates release artifacts.
5. `.github/workflows/translations.yml`:
   scheduled Crowdin sync and translation update automation.

Required passing checks:

1. Test workflow must pass for merge confidence.
2. Style must pass.
3. Mypy must pass in CI.
4. Audit job must pass; approved exceptions must be listed in `.ci/audit-waivers.json` with owner/reason/expiry.
5. Dependency review must pass on dependency/workflow-changing PRs.

Reproducing CI locally:

1. `python -m pytest -q`
2. `python -m mypy`
3. `make style` (or the direct `python -m ruff check .` fallback on Windows without bash)
4. `python -m nox -s ci` for full local cross-version validation.
5. `python -m nox -s package-3.13` for packaging smoke checks.
6. `python -m nox -s audit-3.13` for blocking audit checks.
7. Install and use git hooks for local guardrails:
   `pre-commit` (fast) and `pre-push` (strict) via `bash .githooks/install.sh` or `.\.githooks\install.ps1`.

## 16. Sphinx Docs Workflow (Current + Target)

Current state:

1. This branch does not currently contain a full in-repo Sphinx scaffold (`docs/` is absent).
2. Documentation contribution context is still tied to the `gh-pages` branch workflows.

Target state for full Sphinx support:

1. Add in-repo docs source tree (`docs/`) with developer/API pages.
2. Add strict docs checks (warnings as errors) and API generation commands.
3. Add CI docs workflow and make it part of merge quality checks.

Planned command contract once scaffold lands:

1. `make docs-api`
2. `make docs-check`

"Everything shows up" verification checklist (once docs scaffold lands):

1. New/changed modules appear in API toctree pages.
2. No autodoc import warnings.
3. No unresolved references under strict mode.
4. Generated docs link correctly from index and section landing pages.

## 17. Docs Contribution Guide

Until full in-repo Sphinx support is merged:

1. Follow current doc contribution process on the `gh-pages` branch.
2. Keep this file as the canonical process source, and keep README guidance concise.

When Sphinx scaffold is merged:

1. Keep one page per major developer workflow.
2. Use consistent autosummary/autodoc conventions for API pages.
3. Require docs updates when behavior, CLI/config keys, or workflows change.
4. Definition of done for docs-impacting PRs:
   updated docs page + successful docs validation + navigable links from index.

## 18. Release Process

Trigger model:

1. Build workflow runs on non-main branch pushes and version tags.
2. Tags matching `v*.*.*` represent release builds.

Release checklist:

1. Ensure test/style/mypy status is acceptable.
2. Ensure translation/localization state is current.
3. Tag release (`vX.Y.Z`) and push tag.
4. Verify workflow artifacts for each platform.
5. Verify release assets are attached and signed where applicable.
6. Smoke-test installed artifacts on at least one target OS.

Post-release verification:

1. Confirm release notes accuracy.
2. Confirm downloadable files are complete and installable.

## 19. Release and Build Notes (Platform Gotchas)

1. Linux builds rely on additional system dependencies for wxPython/PyGObject/numpy/shapely toolchains.
2. Linux32 build uses a specialized container/toolchain path.
3. Windows/macOS builds include signing/notarization integration in CI.
4. Keep build-script changes synchronized with workflow dependency steps.

## 20. Localization Workflow

References:

1. `LOCALIZATION.md`
2. `.github/workflows/translations.yml`

Rules:

1. Add user-facing strings in code with translation wrappers as appropriate.
2. Avoid manual broad edits of translation outputs unless you are doing localization maintenance work.
3. Prefer Crowdin-driven updates for translated strings.
4. Keep localization-related CI automation intact when updating extraction/build scripts.

## 21. Troubleshooting Playbook

Common issues and first checks:

1. Dependency install failures:
   verify Python version and OS system dependencies from workflow files.
2. Style check fails on Windows:
   run `bash -x bin/style-check` from Git Bash/WSL, or run the direct `python -m ruff check .` fallback from section `4.1`.
3. Mypy noise:
   focus first on changed modules; avoid introducing new type errors.
4. Debug output missing:
   verify `DEBUG.toml` exists, toggle flags are enabled, and logging config path is correct.
5. Logging files not created:
   verify write permissions and resolved handler file paths.
6. Extension behavior differs in Inkscape vs local script:
   verify environment variables (`INKSTITCH_OFFLINE_SCRIPT`, `PYTHONPATH`) and debug path ordering behavior.
7. Export regressions:
   run targeted output tests plus full `tests/test_output.py`.

## 22. Glossary

1. INX:
   Inkscape extension definition file generated from templates.
2. Stitch plan:
   intermediate embroidery representation before machine-format encoding.
3. Color block:
   contiguous stitches with the same thread color.
4. Satin stitch:
   dense, column-like stitch fill pattern.
5. Running stitch:
   single-line stitch path, often for outlines/details.
6. Sew stack:
   layered stitch-configuration model in `lib/sew_stack/`.

## 23. Decision Record Index (ADR-Style)

Purpose:

1. Preserve key architectural and process decisions in short, discoverable records.

Recommended location:

1. `docs/adr/` (once docs scaffold exists) or `adr/` in repo root.

Recommended ADR format:

1. ID and title.
2. Date and status.
3. Context.
4. Decision.
5. Consequences.
6. Links to related PRs/issues.

Current index:

1. No formal ADR files are indexed yet.

## 24. Security and Secrets Basics

1. Never commit secrets/tokens/certificates to the repository.
2. Treat CI secrets used for signing, notarization, and Crowdin as restricted.
3. Do not log sensitive data in debug output.
4. If a secret exposure is suspected, rotate credentials and notify maintainers immediately.

---

If you update tooling, workflows, or conventions and this file is not updated in the same change, the change is incomplete.
