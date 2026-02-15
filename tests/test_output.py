from unittest.mock import PropertyMock, patch
import os
import tempfile

import pytest
from inkex import Rectangle, SvgDocumentElement
from inkex.tester.svg import svg

from lib import output
from lib.elements import node_to_elements
from lib.stitch_plan.stitch_plan import stitch_groups_to_stitch_plan
from lib.svg.tags import INKSTITCH_ATTRIBS


class TestOutput:
    def _make_stitch_plan(self, svg_doc: SvgDocumentElement):
        # TODO: support SVGs with more than one element
        # (turn InkstitchExtension.elements_to_stitch_groups into a function so we can use it here?)
        assert len(svg_doc) == 1
        [element] = node_to_elements(svg_doc[0])
        stitch_groups = element.embroider(None)
        return stitch_groups_to_stitch_plan(stitch_groups)

    def _build_rect_svg(self) -> SvgDocumentElement:
        root: SvgDocumentElement = svg()
        root.add(
            Rectangle(
                attrib={
                    "width": "10",
                    "height": "10",
                }
            )
        )
        return root

    def _get_output(self, svg: SvgDocumentElement, format: str) -> bytes:
        stitch_plan = self._make_stitch_plan(svg)
        fd, path = tempfile.mkstemp(suffix=f".{format}")
        os.close(fd)
        try:
            output.write_embroidery_file(
                path,
                stitch_plan,
                svg,
                settings={
                    "date": "",  # we need the output to be deterministic for the tests
                },
            )
            with open(path, "rb") as f:
                return f.read()
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_jef_output_does_not_change(self):
        root = self._build_rect_svg()
        output1 = self._get_output(root, "jef")
        output2 = self._get_output(root, "jef")
        assert output1 == output2

    def test_jef_output_includes_trims(self):
        root = self._build_rect_svg()
        rect = root[0]
        output1 = self._get_output(root, "jef")

        rect.attrib[INKSTITCH_ATTRIBS["trim_after"]] = "true"

        output2 = self._get_output(root, "jef")
        assert output1 != output2

    def test_write_embroidery_file_does_not_mutate_settings_argument(self):
        root = self._build_rect_svg()
        stitch_plan = self._make_stitch_plan(root)
        settings = {
            "date": "",
            "custom": "value",
        }
        original_settings = dict(settings)

        with patch("lib.output.pystitch.write") as write_mock:
            output.write_embroidery_file("test.jef", stitch_plan, root, settings=settings)

        assert settings == original_settings
        write_mock.assert_called_once()

    def test_write_embroidery_file_does_not_leak_csv_flags_between_calls(self):
        root = self._build_rect_svg()
        stitch_plan = self._make_stitch_plan(root)
        captured_settings = []

        def capture_settings(pattern, file_path, settings):
            captured_settings.append(dict(settings))

        with patch("lib.output.pystitch.write", side_effect=capture_settings):
            output.write_embroidery_file("first.csv", stitch_plan, root)
            output.write_embroidery_file("second.jef", stitch_plan, root)

        assert "max_stitch" in captured_settings[0]
        assert "max_jump" in captured_settings[0]
        assert "explicit_trim" in captured_settings[0]
        assert "max_stitch" not in captured_settings[1]
        assert "max_jump" not in captured_settings[1]
        assert "explicit_trim" not in captured_settings[1]

    def test_too_many_color_changes_error_extracts_digit_count(self):
        root = self._build_rect_svg()
        stitch_plan = self._make_stitch_plan(root)

        with (
            patch("lib.output.pystitch.write", side_effect=output.TooManyColorChangesError("There are 42 color changes.")),
            patch("lib.output.inkex.errormsg") as errormsg,
        ):
            with pytest.raises(SystemExit) as context:
                output.write_embroidery_file("test.jef", stitch_plan, root)

        assert context.value.code == 1
        errormsg.assert_called_once()
        message = errormsg.call_args[0][0]
        assert "42" in message
        assert "https://inkstitch.org/docs/faq/#too-many-color-changes" in message

    def test_too_many_color_changes_error_handles_missing_digits(self):
        root = self._build_rect_svg()
        stitch_plan = self._make_stitch_plan(root)

        with (
            patch("lib.output.pystitch.write", side_effect=output.TooManyColorChangesError("Too many color changes.")),
            patch("lib.output.inkex.errormsg") as errormsg,
        ):
            with pytest.raises(SystemExit) as context:
                output.write_embroidery_file("test.jef", stitch_plan, root)

        assert context.value.code == 1
        errormsg.assert_called_once()
        message = errormsg.call_args[0][0]
        assert "?" in message

    def test_write_embroidery_file_handles_missing_svg_name(self):
        root = self._build_rect_svg()
        stitch_plan = self._make_stitch_plan(root)

        with patch.object(type(root), "name", new_callable=PropertyMock, return_value=None), patch("lib.output.pystitch.write") as write_mock:
            output.write_embroidery_file("test.jef", stitch_plan, root)

        pattern = write_mock.call_args[0][0]
        assert pattern.extras["name"] == "inkstitch"
