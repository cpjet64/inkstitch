from typing import Any, cast
from types import SimpleNamespace
from unittest.mock import patch

from lib.extensions.batch_lettering import BatchLettering


def test_generate_output_files_returns_early_when_no_text_outputs():
    extension = cast(Any, object.__new__(BatchLettering))
    extension.svg = SimpleNamespace(findone=lambda query: None)
    extension.get_inkstitch_metadata = lambda: {
        "collapse_len_mm": 0,
        "min_stitch_len_mm": 0,
    }

    with patch("lib.extensions.batch_lettering.tempfile.NamedTemporaryFile") as named_temp_file, patch(
        "lib.extensions.batch_lettering.errormsg"
    ) as errormsg:
        BatchLettering.generate_output_files(extension, ["", ""], ["svg"])

    errormsg.assert_called_once()
    named_temp_file.assert_not_called()
