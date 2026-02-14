from types import SimpleNamespace
from unittest.mock import patch

from lib.extensions.print_pdf import PrintPreviewServer


def test_set_metadata_field_requires_value_key():
    server = object.__new__(PrintPreviewServer)
    server.metadata = {}

    assert server.set_metadata_field("field", None) is False
    assert server.set_metadata_field("field", {}) is False
    assert server.set_metadata_field("field", {"value": 123}) is True
    assert server.metadata["field"] == 123


def test_set_defaults_requires_value_key():
    server = object.__new__(PrintPreviewServer)
    server.metadata = {}
    server.stitch_plan = [SimpleNamespace()]

    with patch("lib.extensions.print_pdf.save_defaults") as save_defaults:
        assert server.set_defaults(None) is False
        assert server.set_defaults({}) is False
        assert server.set_defaults({"value": {"a": 1}}) is True

    save_defaults.assert_called_once_with({"a": 1})
