import pytest
from unittest.mock import patch

from lib.extensions.output import Output


def test_parse_arguments_reports_missing_format():
    extension = object.__new__(Output)

    with patch("lib.extensions.output.errormsg") as errormsg, patch(
        "lib.extensions.output.InkstitchExtension.parse_arguments"
    ) as parse_arguments:
        with pytest.raises(SystemExit) as error:
            Output.parse_arguments(extension, ["--id=test"])

    assert error.value.code == 1
    errormsg.assert_called_once()
    parse_arguments.assert_not_called()


def test_parse_arguments_extracts_format_and_passes_through_remaining_args():
    extension = object.__new__(Output)

    with patch("lib.extensions.output.InkstitchExtension.parse_arguments") as parse_arguments:
        Output.parse_arguments(extension, ["--format=jef", "--id=test"])

    assert extension.file_extension == "jef"
    assert extension.settings == {}
    parse_arguments.assert_called_once()


def test_parse_arguments_parses_boolean_values_case_insensitively():
    extension = object.__new__(Output)

    with patch("lib.extensions.output.InkstitchExtension.parse_arguments"):
        Output.parse_arguments(extension, ["--format=jef", "--laser_mode=True", "--id=test"])

    assert extension.settings["laser_mode"] is True
