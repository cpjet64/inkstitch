from pathlib import Path


def test_png_simple_init_passes_args_to_base_constructor():
    source = Path("lib/extensions/png_simple.py").read_text(encoding="utf-8")

    assert "InkstitchExtension.__init__(self, *args, **kwargs)" in source
