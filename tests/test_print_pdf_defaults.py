from unittest.mock import mock_open, patch

import pytest

from lib.extensions.print_pdf import load_defaults


def test_load_defaults_returns_empty_dict_for_missing_file():
    with patch("lib.extensions.print_pdf.open", side_effect=OSError):
        defaults = load_defaults()

    assert defaults == {}


def test_load_defaults_does_not_swallow_keyboard_interrupt():
    with patch("lib.extensions.print_pdf.open", mock_open(read_data="{}")), patch(
        "lib.extensions.print_pdf.json.load",
        side_effect=KeyboardInterrupt,
    ):
        with pytest.raises(KeyboardInterrupt):
            load_defaults()
