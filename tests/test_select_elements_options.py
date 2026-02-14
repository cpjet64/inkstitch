from types import SimpleNamespace

from lib.extensions.select_elements import SelectElements


class DummyNode:
    def get_id(self):
        return ""

    def get(self, key):
        return None


def test_running_condition_invalid_option_returns_false():
    extension = object.__new__(SelectElements)
    extension.options = SimpleNamespace(running_stitch_condition="invalid-condition")

    element = SimpleNamespace(node=DummyNode())

    assert extension._running_condition(element) is False


def test_fill_underlay_invalid_option_returns_false():
    extension = object.__new__(SelectElements)
    extension.options = SimpleNamespace(fill_underlay="invalid-underlay")

    element = SimpleNamespace(fill_underlay=True)

    assert extension._select_fill_underlay(element) is False


def test_satin_filters_invalid_option_returns_false():
    extension = object.__new__(SelectElements)
    extension.options = SimpleNamespace(satin_underlay="invalid-underlay", rung_count="invalid-count")

    element = SimpleNamespace(
        center_walk_underlay=True,
        contour_underlay=False,
        zigzag_underlay=False,
        paths=[1, 2],
    )

    assert extension._select_satin_underlay(element) is False
    assert extension._select_rung_count(element) is False
