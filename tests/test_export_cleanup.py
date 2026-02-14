from types import SimpleNamespace
from unittest.mock import Mock, call, patch

import pytest

from lib.extensions.batch_lettering import BatchLettering
from lib.extensions.output import Output
from lib.extensions.zip import Zip


class DummyTempFile:
    """Simple temp-file stub used to drive exporter cleanup paths."""

    def __init__(self, name):
        self.name = name

    def close(self):
        pass


class RaisingZipFile:
    """ZipFile stand-in that fails on enter to simulate archive errors."""

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        raise RuntimeError("zip failure")

    def __exit__(self, exc_type, exc, tb):
        return False


def test_output_effect_cleans_temp_file_when_export_raises():
    extension = object.__new__(Output)
    extension.file_extension = "dst"
    extension.settings = {}
    extension.elements = []
    extension.document = SimpleNamespace(getroot=lambda: object())
    extension.get_elements = lambda: True
    extension.get_inkstitch_metadata = lambda: {
        "collapse_len_mm": 3,
        "min_stitch_len_mm": 0.1,
        "thread-palette": "Ink/Stitch",
        "rotate_on_export": 0,
    }
    extension.elements_to_stitch_groups = lambda elements: []

    with patch("lib.extensions.output.stitch_groups_to_stitch_plan", return_value=object()), \
            patch("lib.extensions.output.ThreadCatalog", return_value=Mock(match_and_apply_palette=Mock())), \
            patch("lib.extensions.output.tempfile.NamedTemporaryFile", return_value=DummyTempFile("/tmp/out.dst")), \
            patch("lib.extensions.output.write_embroidery_file", side_effect=SystemExit(1)), \
            patch("lib.extensions.output.os.remove") as remove_file:
        with pytest.raises(SystemExit) as context:
            extension.effect()

    assert context.value.code == 1
    remove_file.assert_called_once_with("/tmp/out.dst")


def test_zip_effect_cleans_generated_files_when_zipping_fails():
    extension = object.__new__(Zip)
    extension.options = SimpleNamespace(x_repeats=1, y_repeats=1, custom_file_name="")
    extension.elements = []
    extension.get_elements = lambda: True
    extension.get_inkstitch_metadata = lambda: {
        "collapse_len_mm": 3,
        "min_stitch_len_mm": 0.1,
        "thread-palette": "Ink/Stitch",
    }
    extension.elements_to_stitch_groups = lambda elements: []
    extension._get_file_name = lambda: "design"
    extension.generate_output_files = lambda stitch_plan, path, base_file_name: [
        f"{path}/design.dst",
        f"{path}/design.pes",
    ]

    with patch("lib.extensions.zip.stitch_groups_to_stitch_plan", return_value=object()), \
            patch("lib.extensions.zip.ThreadCatalog", return_value=Mock(match_and_apply_palette=Mock())), \
            patch("lib.extensions.zip.tempfile.mkdtemp", return_value="/tmp/zip-workdir"), \
            patch("lib.extensions.zip.tempfile.NamedTemporaryFile", return_value=DummyTempFile("/tmp/export.zip")), \
            patch("lib.extensions.zip.ZipFile", RaisingZipFile), \
            patch("lib.extensions.zip.os.remove") as remove_file, \
            patch("lib.extensions.zip.os.rmdir") as remove_dir:
        with pytest.raises(RuntimeError):
            extension.effect()

    assert remove_file.call_args_list == [
        call("/tmp/export.zip"),
        call("/tmp/zip-workdir/design.dst"),
        call("/tmp/zip-workdir/design.pes"),
    ]
    remove_dir.assert_called_once_with("/tmp/zip-workdir")


def test_batch_lettering_cleans_generated_files_when_zipping_fails():
    extension = object.__new__(BatchLettering)
    extension.svg = SimpleNamespace(findone=lambda selector: None)
    extension.get_inkstitch_metadata = lambda: {
        "collapse_len_mm": 3,
        "min_stitch_len_mm": 0.1,
    }
    extension.generate_stitch_plan = lambda text, text_positioning_path: (object(), object())
    extension.generate_output_file = lambda file_format, path, text, stitch_plan, i: f"{path}/{i:03d}.{file_format}"
    extension.reset_document = lambda lettering_group, text_positioning_path: None

    with patch("lib.extensions.batch_lettering.tempfile.mkdtemp", return_value="/tmp/batch-workdir"), \
            patch("lib.extensions.batch_lettering.tempfile.NamedTemporaryFile", return_value=DummyTempFile("/tmp/batch.zip")), \
            patch("lib.extensions.batch_lettering.ZipFile", RaisingZipFile), \
            patch("lib.extensions.batch_lettering.os.remove") as remove_file, \
            patch("lib.extensions.batch_lettering.os.rmdir") as remove_dir:
        with pytest.raises(RuntimeError):
            extension.generate_output_files(["alpha", "beta"], ["dst"])

    assert remove_file.call_args_list == [
        call("/tmp/batch.zip"),
        call("/tmp/batch-workdir/000.dst"),
        call("/tmp/batch-workdir/001.dst"),
    ]
    remove_dir.assert_called_once_with("/tmp/batch-workdir")
