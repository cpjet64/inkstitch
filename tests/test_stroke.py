import pytest

from lib.elements.stroke import Stroke
from lib.utils.geometry import Point


def test_apply_max_stitch_length_does_not_duplicate_segment_endpoint():
    dummy_stroke = type("DummyStroke", (), {"max_stitch_length": 2.0})()
    path = [Point(0, 0), Point(5, 0)]

    result = Stroke.apply_max_stitch_length(dummy_stroke, path)
    coords = [(point.x, point.y) for point in result]

    assert len(coords) == 4
    assert coords[0] == (0.0, 0.0)
    assert coords[-1] == (5.0, 0.0)
    assert coords[1][0] == pytest.approx(5.0 / 3.0)
    assert coords[2][0] == pytest.approx(10.0 / 3.0)
    assert coords[1][1] == 0.0
    assert coords[2][1] == 0.0


def test_apply_max_stitch_length_leaves_short_segments_unchanged():
    dummy_stroke = type("DummyStroke", (), {"max_stitch_length": 10.0})()
    path = [Point(0, 0), Point(5, 0)]

    result = Stroke.apply_max_stitch_length(dummy_stroke, path)

    assert [(point.x, point.y) for point in result] == [(0.0, 0.0), (5.0, 0.0)]
