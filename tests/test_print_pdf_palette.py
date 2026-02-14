from types import SimpleNamespace
from unittest.mock import Mock, patch

from lib.extensions.print_pdf import PrintPreviewServer


def _make_server(metadata):
    server = object.__new__(PrintPreviewServer)
    server.metadata = metadata
    server.stitch_plan = [SimpleNamespace(color=SimpleNamespace(chart=None))]
    return server


def test_apply_palette_returns_false_for_unknown_palette_and_preserves_metadata():
    metadata = {"thread-palette": "old", "color-0": "red", "thread-0": "name"}
    server = _make_server(metadata)

    with patch("lib.extensions.print_pdf.ThreadCatalog") as thread_catalog:
        catalog = thread_catalog.return_value
        catalog.get_palette_by_name.return_value = None

        result = PrintPreviewServer.apply_palette(server, "missing")

    assert result is False
    assert metadata["thread-palette"] == "old"
    assert "color-0" in metadata
    assert "thread-0" in metadata
    catalog.apply_palette.assert_not_called()


def test_apply_palette_updates_metadata_for_known_palette():
    metadata = {"thread-palette": "old", "color-0": "red", "thread-0": "name", "other": "keep"}
    server = _make_server(metadata)
    fake_palette = object()

    with patch("lib.extensions.print_pdf.ThreadCatalog") as thread_catalog:
        catalog = thread_catalog.return_value
        catalog.get_palette_by_name.return_value = fake_palette
        catalog.apply_palette = Mock()

        result = PrintPreviewServer.apply_palette(server, "new-palette")

    assert result is True
    assert metadata["thread-palette"] == "new-palette"
    assert "color-0" not in metadata
    assert "thread-0" not in metadata
    assert metadata["other"] == "keep"
    catalog.apply_palette.assert_called_once_with(server.stitch_plan, fake_palette)
