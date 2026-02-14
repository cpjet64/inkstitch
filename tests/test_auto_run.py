from types import SimpleNamespace
from unittest.mock import Mock, patch

from lib.extensions.auto_run import AutoRun


def test_check_selection_returns_early_when_nothing_selected():
    extension = object.__new__(AutoRun)
    extension.svg = SimpleNamespace(selection=[])
    extension.get_elements = Mock()

    with patch("lib.extensions.auto_run.errormsg") as error_message:
        result = extension.check_selection()

    assert result == []
    extension.get_elements.assert_not_called()
    error_message.assert_called_once()


def test_check_selection_returns_empty_when_no_strokes_found():
    extension = object.__new__(AutoRun)
    extension.svg = SimpleNamespace(selection=[object()])
    extension.get_elements = Mock()
    extension.elements = [object(), object()]

    with patch("lib.extensions.auto_run.errormsg") as error_message:
        result = extension.check_selection()

    assert result == []
    error_message.assert_called_once()


def test_check_selection_returns_only_stroke_elements():
    class DummyStroke:
        pass

    extension = object.__new__(AutoRun)
    extension.svg = SimpleNamespace(selection=[object()])
    extension.get_elements = Mock()
    stroke_element = DummyStroke()
    extension.elements = [stroke_element, object()]

    with patch("lib.extensions.auto_run.Stroke", DummyStroke):
        result = extension.check_selection()

    assert result == [stroke_element]
