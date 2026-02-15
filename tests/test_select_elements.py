from typing import Any, cast
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from lib.extensions import select_elements as select_elements_module
from lib.extensions.select_elements import SelectElements


def _extension_with_python_path(python_path=""):
    extension = cast(Any, object.__new__(SelectElements))
    extension.options = SimpleNamespace(python_path=python_path)
    return extension


def test_get_paths_frozen_linux_uses_python_from_path():
    extension = _extension_with_python_path()

    with patch("lib.extensions.select_elements.get_bundled_dir", return_value="/bundled/dbus"), \
            patch.object(select_elements_module.sys, "platform", "linux"), \
            patch.object(select_elements_module.sys, "frozen", True, create=True), \
            patch.object(select_elements_module.sys, "_MEIPASS", "/tmp", create=True), \
            patch("lib.extensions.select_elements.shutil.which", return_value="/usr/bin/python3"), \
            patch("lib.extensions.select_elements.os.path.isfile", side_effect=lambda path: path == "/usr/bin/python3"):
        py_path, file_path = extension._get_paths()

    assert py_path == "/usr/bin/python3"
    assert file_path == "/bundled/dbus"


def test_get_paths_frozen_darwin_preserves_detected_inkscape_python():
    extension = _extension_with_python_path()
    inkscape_python = "/Applications/Inkscape.app/Contents/Resources/bin/python3"

    with patch("lib.extensions.select_elements.get_bundled_dir", return_value="/bundled/dbus"), \
            patch.object(select_elements_module.sys, "platform", "darwin"), \
            patch.object(select_elements_module.sys, "frozen", True, create=True), \
            patch.object(select_elements_module.sys, "_MEIPASS", "/tmp", create=True), \
            patch("lib.extensions.select_elements.os.path.isfile", side_effect=lambda path: path == inkscape_python):
        py_path, _ = extension._get_paths()

    assert py_path == inkscape_python


def test_get_paths_allows_custom_python_command_from_path():
    extension = _extension_with_python_path("python3")

    with patch("lib.extensions.select_elements.get_bundled_dir", return_value="/bundled/dbus"), \
            patch.object(select_elements_module.sys, "platform", "linux"), \
            patch.object(select_elements_module.sys, "frozen", False, create=True), \
            patch("lib.extensions.select_elements.os.path.isfile", return_value=False), \
            patch("lib.extensions.select_elements.shutil.which", return_value="/usr/bin/python3"):
        py_path, _ = extension._get_paths()

    assert py_path == "python3"


def test_get_paths_exits_when_python_path_is_unresolvable():
    extension = _extension_with_python_path()

    with patch("lib.extensions.select_elements.get_bundled_dir", return_value="/bundled/dbus"), \
            patch.object(select_elements_module.sys, "platform", "linux"), \
            patch.object(select_elements_module.sys, "frozen", True, create=True), \
            patch.object(select_elements_module.sys, "_MEIPASS", "/tmp", create=True), \
            patch("lib.extensions.select_elements.os.path.isfile", return_value=False), \
            patch("lib.extensions.select_elements.shutil.which", return_value=None), \
            patch("lib.extensions.select_elements.errormsg") as error_message:
        with pytest.raises(SystemExit) as context:
            extension._get_paths()

    assert context.value.code == 0
    error_message.assert_called_once()
