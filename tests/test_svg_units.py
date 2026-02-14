from lib.svg.units import get_doc_size, get_viewbox, get_viewbox_transform


class DummySvg:
    def __init__(self, attrib):
        self.attrib = attrib

    def get(self, key, default=None):
        return self.attrib.get(key, default)


def test_get_viewbox_pads_short_value_to_four_entries():
    svg = DummySvg({"viewBox": "1 2"})

    assert get_viewbox(svg) == ["1", "2", "0", "0"]


def test_get_doc_size_handles_short_viewbox_without_index_error():
    svg = DummySvg({"viewBox": "1 2"})

    width, height = get_doc_size(svg)

    assert width == 0
    assert height == 0


def test_get_viewbox_transform_handles_short_viewbox_without_index_error():
    svg = DummySvg({"width": "10px", "height": "10px", "viewBox": "1 2"})

    transform = get_viewbox_transform(svg)

    assert transform is not None
