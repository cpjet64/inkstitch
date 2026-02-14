from unittest.mock import patch

from lib.gui.element_info import ElementInfoFrame


class DummyClipboard:
    def __init__(self, open_result=True):
        self.open_result = open_result
        self.open_calls = 0
        self.set_data_calls = 0
        self.close_calls = 0

    def Open(self):
        self.open_calls += 1
        return self.open_result

    def SetData(self, data):
        self.set_data_calls += 1

    def Close(self):
        self.close_calls += 1


def test_on_copy_closes_clipboard_after_copy():
    frame = ElementInfoFrame.__new__(ElementInfoFrame)
    frame.export_txt = "copied text"
    clipboard = DummyClipboard(open_result=True)

    with patch("lib.gui.element_info.wx.TheClipboard", clipboard), patch(
        "lib.gui.element_info.wx.TextDataObject",
        side_effect=lambda text: text,
    ):
        ElementInfoFrame.on_copy(frame, None)

    assert clipboard.open_calls == 1
    assert clipboard.set_data_calls == 1
    assert clipboard.close_calls == 1
