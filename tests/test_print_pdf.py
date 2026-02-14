from unittest.mock import Mock, patch

import flask.cli  # noqa: F401

from lib.extensions import print_pdf


def _make_print_server(metadata=None):
    metadata = metadata or {}
    with patch("lib.extensions.print_pdf.Thread.start", return_value=None):
        return print_pdf.PrintPreviewServer(
            html="",
            metadata=metadata,
            stitch_plan=[],
            realistic_overview_svg="<svg/>",
            realistic_color_block_svgs=[],
        )


def test_get_settings_field_route_works_with_field_name():
    metadata = {"paper-size": "A4"}
    print_server = _make_print_server(metadata)

    response = print_server.app.test_client().get("/settings/paper-size")

    assert response.status_code == 200
    assert response.get_json() == "A4"


def test_set_palette_clears_all_color_and_thread_overrides():
    metadata = {
        "color-ff0000": "red",
        "thread-ff0000": "Thread Red",
        "color-00ff00": "green",
        "thread-00ff00": "Thread Green",
        "thread-palette": "old",
        "footer-info": "keep me",
    }
    print_server = _make_print_server(metadata)
    catalog = Mock()
    catalog.get_palette_by_name.return_value = object()

    with patch("lib.extensions.print_pdf.ThreadCatalog", return_value=catalog):
        response = print_server.app.test_client().post("/palette", json={"name": "new-palette"})

    assert response.status_code == 200
    assert "color-ff0000" not in metadata
    assert "thread-ff0000" not in metadata
    assert "color-00ff00" not in metadata
    assert "thread-00ff00" not in metadata
    assert metadata["thread-palette"] == "new-palette"


def test_set_palette_preserves_non_thread_metadata():
    metadata = {
        "color-ff0000": "red",
        "thread-ff0000": "Thread Red",
        "paper-size": "a4",
        "footer-info": "persistent",
    }
    print_server = _make_print_server(metadata)
    catalog = Mock()
    palette = object()
    catalog.get_palette_by_name.return_value = palette

    with patch("lib.extensions.print_pdf.ThreadCatalog", return_value=catalog):
        response = print_server.app.test_client().post("/palette", json={"name": "palette-x"})

    assert response.status_code == 200
    assert metadata["paper-size"] == "a4"
    assert metadata["footer-info"] == "persistent"
    assert metadata["thread-palette"] == "palette-x"
    catalog.get_palette_by_name.assert_called_once_with("palette-x")
    catalog.apply_palette.assert_called_once_with([], palette)
