from types import SimpleNamespace

from lib.threads.catalog import _ThreadCatalog


class DummyColor:
    def __init__(self, chart=None):
        self.chart = chart
        self.name = "old-name"
        self.number = "old-number"
        self.manufacturer = "old-manufacturer"
        self.description = "old-description"


def test_apply_palette_returns_early_for_none_palette():
    catalog = object.__new__(_ThreadCatalog)
    color = DummyColor(chart=None)
    stitch_plan = [SimpleNamespace(color=color)]

    catalog.apply_palette(stitch_plan, None)

    assert color.name == "old-name"
    assert color.number == "old-number"
    assert color.manufacturer == "old-manufacturer"
    assert color.description == "old-description"


def test_apply_palette_skips_cutwork_colors():
    catalog = object.__new__(_ThreadCatalog)
    color = DummyColor(chart="cutwork")
    stitch_plan = [SimpleNamespace(color=color)]
    palette = SimpleNamespace(
        nearest_color=lambda selected_color: (_ for _ in ()).throw(AssertionError("nearest_color should not be called"))
    )

    catalog.apply_palette(stitch_plan, palette)

    assert color.name == "old-name"
    assert color.number == "old-number"
    assert color.manufacturer == "old-manufacturer"
    assert color.description == "old-description"
