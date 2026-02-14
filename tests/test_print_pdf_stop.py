from unittest.mock import Mock

from lib.extensions.print_pdf import PrintPreviewServer


def test_stop_handles_uninitialized_server_fields():
    server = object.__new__(PrintPreviewServer)
    server.flask_server = None
    server.server_thread = None

    PrintPreviewServer.stop(server)


def test_stop_shuts_down_server_and_joins_thread():
    server = object.__new__(PrintPreviewServer)
    server.flask_server = Mock()
    server.server_thread = Mock()

    PrintPreviewServer.stop(server)

    server.flask_server.shutdown.assert_called_once()
    server.server_thread.join.assert_called_once()
