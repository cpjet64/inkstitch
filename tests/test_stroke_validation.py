from typing import Any, cast
from unittest.mock import patch

from lib.elements.stroke import MultipleGuideLineWarning, Stroke


def test_validation_warnings_reports_multiple_guidelines_for_ripple_stitch():
    stroke = cast(Any, object.__new__(Stroke))
    stroke.node = object()
    stroke.get_boolean_param = lambda name, default=False: False
    stroke.get_param = lambda name, default=None: "ripple_stitch"
    stroke._representative_point = lambda: (0, 0)

    with patch(
        "lib.elements.stroke.get_marker_elements",
        return_value={"stroke": [object(), object()], "satin": []},
    ):
        warnings = list(Stroke.validation_warnings(stroke))

    assert len(warnings) == 1
    assert isinstance(warnings[0], MultipleGuideLineWarning)
