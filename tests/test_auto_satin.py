from types import SimpleNamespace
from unittest.mock import patch

import pytest

from lib.extensions.auto_satin import AutoSatin


class DummyElement:
    def __init__(self, command=None):
        self.command = command

    def get_command(self, command_type):
        return self.command


def test_get_point_exits_with_code_1_on_duplicate_commands():
    extension = object.__new__(AutoSatin)
    extension.elements = [
        DummyElement(SimpleNamespace(target_point=(1, 2))),
        DummyElement(SimpleNamespace(target_point=(3, 4))),
    ]

    with patch("lib.extensions.auto_satin.inkex.errormsg") as error_message:
        with pytest.raises(SystemExit) as context:
            extension.get_point("autoroute_start")

    assert context.value.code == 1
    error_message.assert_called_once()


def test_get_point_returns_target_for_single_command():
    extension = object.__new__(AutoSatin)
    extension.elements = [
        DummyElement(None),
        DummyElement(SimpleNamespace(target_point=(3, 4))),
    ]

    result = extension.get_point("autoroute_start")

    assert result == (3, 4)
