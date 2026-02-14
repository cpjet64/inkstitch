import importlib
from types import SimpleNamespace

meander_fill_module = importlib.import_module("lib.stitches.meander_fill")


def test_post_process_uses_linear_repeat_growth(monkeypatch):
    fill = SimpleNamespace(
        smoothness=0,
        zigzag_spacing=0,
        running_stitch_tolerance=0.2,
        running_stitch_length=1.0,
        clip=False,
        bean_stitch_repeats=0,
        repeats=3,
    )

    monkeypatch.setattr(meander_fill_module, "smooth_path", lambda points, smoothness: points)
    monkeypatch.setattr(meander_fill_module, "even_running_stitch", lambda *args, **kwargs: [1, 2])

    result = meander_fill_module.post_process(
        points=[(0, 0), (1, 0)],
        shape=None,
        original_shape=None,
        fill=fill,
    )

    assert result == [1, 2, 2, 1, 1, 2]
