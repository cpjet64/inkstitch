"""Nox automation for supported-version quality and dependency checks."""

from __future__ import annotations

import nox

SUPPORTED_PYTHONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]
EXPERIMENTAL_PYTHONS = ["3.14"]

LINUX_WXPYTHON_WHEEL = "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04/" "wxPython-4.2.2-{py_tag}-{py_tag}-linux_x86_64.whl"

nox.options.default_venv_backend = "uv|virtualenv"
nox.options.error_on_missing_interpreters = True
nox.options.sessions = ["ci"]


def install_dev(session: nox.Session) -> None:
    """Install project dependencies for the active interpreter."""
    session.install("--upgrade", "pip", "wheel")
    platform_name = session.run("python", "-c", "import sys; print(sys.platform)", silent=True).strip()

    # Linux uses pinned prebuilt packages in CI because source builds are unreliable.
    if platform_name.startswith("linux"):
        session.install("PyGObject==3.50.0")
        py_tag = session.run(
            "python",
            "-c",
            "import sys; print(f'cp{sys.version_info.major}{sys.version_info.minor}')",
            silent=True,
        ).strip()
        session.install(LINUX_WXPYTHON_WHEEL.format(py_tag=py_tag))

    session.install("-r", "requirements.txt")


def run_lint(session: nox.Session) -> None:
    """Run repository lint checks with Ruff."""
    session.run("ruff", "check", "lib", "tests")


def run_typecheck(session: nox.Session) -> None:
    """Run static type checks."""
    session.run("mypy")


def run_tests(session: nox.Session) -> None:
    """Run unit and integration tests."""
    session.run("pytest", "-q")


@nox.session(python=SUPPORTED_PYTHONS)
def ci(session: nox.Session) -> None:
    """Run tests + lint + type checks for supported Python versions."""
    install_dev(session)
    run_tests(session)
    run_lint(session)
    run_typecheck(session)


@nox.session(python=EXPERIMENTAL_PYTHONS)
def experimental(session: nox.Session) -> None:
    """Run the full quality pipeline for experimental Python versions."""
    install_dev(session)
    run_tests(session)
    run_lint(session)
    run_typecheck(session)


@nox.session(python=["3.13"])
def quick(session: nox.Session) -> None:
    """Fast local iteration on the primary development interpreter."""
    install_dev(session)
    run_tests(session)


@nox.session(python=["3.13"])
def package(session: nox.Session) -> None:
    """Run release-readiness smoke checks."""
    install_dev(session)
    session.run("python", "-m", "compileall", "-q", "lib", "tests")
    session.run("python", "-m", "pip", "check")


@nox.session(python=["3.13"])
def audit(session: nox.Session) -> None:
    """Run dependency vulnerability audit with waiver policy."""
    install_dev(session)
    session.run("python", ".ci/audit_with_waivers.py", "--requirements", "requirements.txt")
