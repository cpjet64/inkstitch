from pathlib import Path


def test_build_workflow_uses_posix_python_path_suffix():
    workflow = Path(".github/workflows/build.yml").read_text(encoding="utf-8")

    assert '${{ env.pythonLocation }}\\bin' not in workflow
