from unittest.mock import Mock, patch

import pytest

from lib.extensions.print_pdf import open_url


class DummyFile:
    def __init__(self):
        self.closed = False

    def fileno(self):
        return 99

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


class DummyStdout:
    def fileno(self):
        return 1


def test_open_url_restores_descriptors_and_closes_devnull_on_error():
    dummy_file = DummyFile()
    dup2 = Mock()
    close = Mock()

    with patch("lib.extensions.print_pdf.open", return_value=dummy_file), patch(
        "lib.extensions.print_pdf.os.dup",
        return_value=200,
    ), patch("lib.extensions.print_pdf.os.dup2", dup2), patch(
        "lib.extensions.print_pdf.os.close",
        close,
    ), patch(
        "lib.extensions.print_pdf.webbrowser.open",
        side_effect=RuntimeError("browser failed"),
    ), patch(
        "lib.extensions.print_pdf.sys.stdout",
        DummyStdout(),
    ):
        with pytest.raises(RuntimeError):
            open_url("https://example.test")

    assert dup2.call_count == 2
    assert dup2.call_args_list[0].args == (99, 1)
    assert dup2.call_args_list[1].args == (200, 1)
    close.assert_called_once_with(200)
    assert dummy_file.closed is True
