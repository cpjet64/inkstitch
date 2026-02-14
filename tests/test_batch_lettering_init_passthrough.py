from pathlib import Path


def test_batch_lettering_init_passes_args_to_base_constructor():
    source = Path("lib/extensions/batch_lettering.py").read_text(encoding="utf-8")

    assert "InkstitchExtension.__init__(self, *args, **kwargs)" in source
