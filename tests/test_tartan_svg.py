import importlib
from types import SimpleNamespace

from shapely import Point

tartan_svg_module = importlib.import_module("lib.tartan.svg")


class FakePathElement(dict):
    def __init__(self):
        super().__init__()
        self.pop_calls = []

    def set(self, key, value):
        self[key] = value

    def pop(self, key, default=None):
        self.pop_calls.append(key)
        return super().pop(key, default)


class FakeFillStitch:
    def __init__(self, node):
        self.node = node

    def to_stitch_groups(self, _):
        reverse = bool(self.node.get("inkstitch:reverse"))
        flip = bool(self.node.get("inkstitch:flip"))

        if reverse and flip:
            point = (0, 0)
        elif reverse:
            point = (1, 0)
        elif flip:
            point = (2, 0)
        else:
            point = (3, 0)

        return [SimpleNamespace(stitches=[point])]


def test_adapt_legacy_fill_params_clears_reverse_attribute_key(monkeypatch):
    path = FakePathElement()

    monkeypatch.setattr(tartan_svg_module, "FillStitch", FakeFillStitch)
    tartan_svg_module.TartanSvgGroup._adapt_legacy_fill_params(path, Point(0, 0))

    assert "inkstitch:reverse" in path.pop_calls
    assert "inkstitch:revers" not in path.pop_calls
