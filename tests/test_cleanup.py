from unittest.mock import call, patch

from lib.extensions.cleanup import Cleanup


class DummyElement:
    def __init__(self, element_id, label=None):
        self._id = element_id
        self.label = label

    def get_id(self):
        return self._id


def test_cleanup_dry_run_reports_element_and_group_counts():
    extension = object.__new__(Cleanup)
    extension.elements_to_remove = [
        DummyElement("rect1", "Rect 1"),
        DummyElement("rect2"),
    ]
    extension.groups_to_remove = [
        DummyElement("group1", "Layer 1"),
    ]

    with patch("lib.extensions.cleanup.errormsg") as error_message:
        extension._dry_run()

    assert error_message.call_args_list == [
        call("2 elements to remove:"),
        call(" - Rect 1 (id: rect1)"),
        call(" - rect2"),
        call("\n"),
        call("1 groups/layers to remove:"),
        call(" - Layer 1: group1"),
    ]
