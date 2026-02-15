from typing import Any, cast
from unittest.mock import PropertyMock, patch

from shapely.geometry import MultiPolygon, Polygon

from lib.elements.fill_stitch import (
    BorderCrossWarning,
    FillStitch,
    InvalidShapeError,
    MissingGuideLineWarning,
    SmallShapeWarning,
    StrokeAndFillWarning,
)
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


class DummyNodeWithStroke(DummyNode):
    def style(self, key, default=None):
        if key == "stroke":
            return "#000000"
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
        fill = cast(Any, object.__new__(FillStitch))
        fill.node = DummyNode()
        fill.shrink_or_grow_shape = lambda shape, amount, validate=False: shape
        fill.get_param = lambda name, default=None: default
        fill.get_float_param = lambda name, default=None: default if default is not None else 0

        warnings = list(FillStitch.validation_warnings(fill))
    small_shape_warnings = [warning for warning in warnings if isinstance(warning, SmallShapeWarning)]

    assert len(small_shape_warnings) == 1


def test_validation_warnings_guided_fill_continues_after_missing_guide_line():
    with patch.object(
        FillStitch,
        "original_shape",
        new_callable=PropertyMock,
        return_value=Polygon([(0, 0), (10, 0), (10, 10), (0, 10)]),
    ), patch.object(
        FillStitch,
        "shape",
        new_callable=PropertyMock,
        return_value=MultiPolygon([Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])]),
    ), patch.object(FillStitch, "fill_method", new_callable=PropertyMock, return_value="guided_fill"), patch.object(
        FillStitch,
        "fill_underlay_inset",
        new_callable=PropertyMock,
        return_value=0,
    ), patch.object(FillStitch, "expand", new_callable=PropertyMock, return_value=0), patch.object(
        FillStitch,
        "_get_guide_lines",
        return_value=[],
    ):
        fill = cast(Any, object.__new__(FillStitch))
        fill.node = DummyNodeWithStroke()
        fill.shrink_or_grow_shape = lambda shape, amount, validate=False: shape
        fill.get_param = lambda name, default=None: default
        fill.get_float_param = lambda name, default=None: default if default is not None else 0

        warnings = list(FillStitch.validation_warnings(fill))

    warning_types = {type(warning) for warning in warnings}
    assert MissingGuideLineWarning in warning_types
    assert StrokeAndFillWarning in warning_types


def test_validation_errors_handles_unexpected_validity_message_format():
    invalid_shape = Polygon([(0, 0), (2, 2), (2, 0), (0, 2)])

    with patch.object(
        FillStitch,
        "shape",
        new_callable=PropertyMock,
        return_value=invalid_shape,
    ), patch("lib.elements.fill_stitch.explain_validity", return_value="unexpected format"):
        fill = cast(Any, object.__new__(FillStitch))
        errors = list(FillStitch.validation_errors(fill))

    assert len(errors) == 1
    assert isinstance(errors[0], InvalidShapeError)


def test_validation_warnings_handles_unexpected_validity_message_format():
    invalid_shape = Polygon([(0, 0), (2, 2), (2, 0), (0, 2)])
    valid_shape = MultiPolygon([Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])])

    with patch.object(
        FillStitch,
        "original_shape",
        new_callable=PropertyMock,
        return_value=invalid_shape,
    ), patch.object(
        FillStitch,
        "shape",
        new_callable=PropertyMock,
        return_value=valid_shape,
    ), patch.object(FillStitch, "fill_method", new_callable=PropertyMock, return_value="auto_fill"), patch.object(
        FillStitch,
        "fill_underlay_inset",
        new_callable=PropertyMock,
        return_value=0,
    ), patch.object(FillStitch, "expand", new_callable=PropertyMock, return_value=0), patch(
        "lib.elements.fill_stitch.explain_validity",
        return_value="unexpected format",
    ):
        fill = cast(Any, object.__new__(FillStitch))
        fill.node = DummyNode()
        fill.shrink_or_grow_shape = lambda shape, amount, validate=False: shape
        fill.get_param = lambda name, default=None: default
        fill.get_float_param = lambda name, default=None: default if default is not None else 0
        warnings = list(FillStitch.validation_warnings(fill))

    warning_types = {type(warning) for warning in warnings}
    assert BorderCrossWarning in warning_types
