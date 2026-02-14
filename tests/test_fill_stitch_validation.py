from unittest.mock import PropertyMock, patch

from shapely.geometry import MultiPolygon, Polygon

from lib.elements.fill_stitch import FillStitch, SmallShapeWarning
from lib.svg.tags import INKSCAPE_LABEL


class DummyNode:
    def get(self, key, default=None):
        if key == INKSCAPE_LABEL:
            return "label"
        if key == "id":
            return "shape-id"
        return default

    def style(self, key, default=None):
        return default


def test_validation_warnings_uses_individual_shape_area_for_small_shape_warning():
    with patch.object(
        FillStitch,
        "original_shape",
        new_callable=PropertyMock,
        return_value=Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
    ), patch.object(
        FillStitch,
        "shape",
        new_callable=PropertyMock,
        return_value=MultiPolygon(
            [
                Polygon([(0, 0), (3, 0), (3, 3), (0, 3)]),  # area 9 -> warning
                Polygon([(0, 0), (7, 0), (7, 7), (0, 7)]),  # area 49 -> no warning
            ]
        ),
    ), patch.object(FillStitch, "fill_method", new_callable=PropertyMock, return_value="auto_fill"), patch.object(
        FillStitch,
        "fill_underlay_inset",
        new_callable=PropertyMock,
        return_value=0,
    ), patch.object(FillStitch, "expand", new_callable=PropertyMock, return_value=0):
        fill = object.__new__(FillStitch)
        fill.node = DummyNode()
        fill.shrink_or_grow_shape = lambda shape, amount, validate=False: shape
        fill.get_param = lambda name, default=None: default
        fill.get_float_param = lambda name, default=None: default if default is not None else 0

        warnings = list(FillStitch.validation_warnings(fill))
    small_shape_warnings = [warning for warning in warnings if isinstance(warning, SmallShapeWarning)]

    assert len(small_shape_warnings) == 1
