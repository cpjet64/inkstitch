from types import SimpleNamespace
from unittest.mock import patch

import pytest

from lib.extensions.print_pdf import PrintPreviewServer


def _dummy_server():
    return SimpleNamespace(
        shutting_down=False,
        last_request_time=None,
        stop=lambda: None,
    )


def test_watch_logs_and_swallows_runtime_errors():
    server = _dummy_server()

    with patch("lib.extensions.print_pdf.time.sleep", side_effect=RuntimeError("boom")), patch(
        "lib.extensions.print_pdf.debug.log"
    ) as log:
        PrintPreviewServer.watch(server)

    log.assert_called_once()


def test_watch_does_not_swallow_keyboard_interrupt():
    server = _dummy_server()

    with patch("lib.extensions.print_pdf.time.sleep", side_effect=KeyboardInterrupt), patch(
        "lib.extensions.print_pdf.debug.log"
    ):
        with pytest.raises(KeyboardInterrupt):
            PrintPreviewServer.watch(server)
