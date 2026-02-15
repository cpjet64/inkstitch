from typing import Any, cast
from types import SimpleNamespace
from unittest.mock import Mock, patch

from lib.extensions.zip import Zip


class DummyStitchPlan:
    def make_offsets(self, offsets):
        return self


def test_zip_effect_returns_early_when_no_formats_selected():
    extension = cast(Any, object.__new__(Zip))
    extension.options = SimpleNamespace(x_repeats=1, y_repeats=1, custom_file_name="", dst=False)
    extension.formats = ["dst"]
    extension.elements = [object()]
    extension.get_elements = lambda: extension.elements
    extension.get_inkstitch_metadata = Mock(return_value={
        "collapse_len_mm": 0,
        "min_stitch_len_mm": 0,
        "thread-palette": None,
    })
    extension.elements_to_stitch_groups = lambda elements: []
    extension._get_file_name = lambda: "test"
    extension.document = SimpleNamespace(getroot=lambda: object())
    extension.generate_output_files = Mock()

    with patch("lib.extensions.zip.stitch_groups_to_stitch_plan", return_value=DummyStitchPlan()) as to_stitch_plan, patch(
        "lib.extensions.zip.ThreadCatalog"
    ), patch("lib.extensions.zip.tempfile.NamedTemporaryFile") as named_temp_file, patch(
        "lib.extensions.zip.errormsg"
    ) as errormsg, patch(
        "lib.extensions.zip.sys.exit"
    ) as sys_exit:
        Zip.effect(extension)

    errormsg.assert_called_once()
    named_temp_file.assert_not_called()
    sys_exit.assert_not_called()
    to_stitch_plan.assert_not_called()
    extension.get_inkstitch_metadata.assert_not_called()
    extension.generate_output_files.assert_not_called()
