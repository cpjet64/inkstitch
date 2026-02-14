from unittest.mock import patch

from lib.extensions.output import Output


def _output_extension():
    return object.__new__(Output)


def test_parse_arguments_uses_current_sys_argv_when_args_none():
    extension = _output_extension()

    with patch("lib.extensions.output.sys.argv", ["inkstitch.py", "--format=dst", "--laser_mode=true"]), \
            patch("lib.extensions.output.InkstitchExtension.parse_arguments") as base_parse_arguments:
        extension.parse_arguments()

    assert extension.file_extension == "dst"
    assert extension.settings["laser_mode"] is True
    base_parse_arguments.assert_called_once_with(extension, [])


def test_parse_arguments_handles_values_with_additional_equals():
    extension = _output_extension()

    with patch("lib.extensions.output.sys.argv", ["inkstitch.py", "--unused"]), \
            patch("lib.extensions.output.InkstitchExtension.parse_arguments") as base_parse_arguments:
        extension.parse_arguments(["--format=pes", "--metadata=a=b=c"])

    assert extension.file_extension == "pes"
    assert extension.settings["metadata"] == "a=b=c"
    base_parse_arguments.assert_called_once_with(extension, [])


def test_parse_arguments_does_not_crash_on_flag_without_equals():
    extension = _output_extension()

    with patch("lib.extensions.output.sys.argv", ["inkstitch.py", "--unused"]), \
            patch("lib.extensions.output.InkstitchExtension.parse_arguments") as base_parse_arguments:
        extension.parse_arguments(["--format=pes", "--flag", "--density=3.5", "--id=node1"])

    assert extension.file_extension == "pes"
    assert extension.settings["density"] == 3.5
    base_parse_arguments.assert_called_once_with(extension, ["--flag", "--id=node1"])
