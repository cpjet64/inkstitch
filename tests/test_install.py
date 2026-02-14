from unittest.mock import patch

from lib.extensions.install import Install


def test_install_symbol_libraries_reports_symbol_specific_error():
    extension = object.__new__(Install)
    extension.inkscape_config_path = "/tmp/inkscape"
    extension.install_resources = "/tmp/resources"

    with patch("lib.extensions.install.glob", return_value=["/tmp/resources/symbols/a.svg"]), \
            patch("lib.extensions.install.copy_files", side_effect=IOError("copy failed")), \
            patch.object(extension, "install_error_message") as install_error_message:
        result = extension.install_symbol_libraries()

    assert result is False
    install_error_message.assert_called_once()
    assert install_error_message.call_args[0][0] == "Could not install symbol libraries. Please file an issue on"
