from unittest.mock import Mock, call, patch

from lib.threads.catalog import _ThreadCatalog


class DummyColor:
    def __init__(self, name, number, manufacturer, description, chart=None):
        self.name = name
        self.number = number
        self.manufacturer = manufacturer
        self.description = description
        self.chart = chart


class DummyColorBlock:
    def __init__(self, color):
        self.color = color


def test_load_palettes_parses_each_valid_palette_once():
    catalog = object.__new__(_ThreadCatalog)
    catalog.palettes = []
    valid_palette = Mock(is_gimp_palette=True)

    with patch("lib.threads.catalog.glob", return_value=["/tmp/InkStitch-test.gpl"]), patch(
        "lib.threads.catalog.ThreadPalette",
        return_value=valid_palette,
    ) as thread_palette:
        catalog.load_palettes(["/tmp"])

    assert catalog.palettes == [valid_palette]
    assert thread_palette.call_count == 1


def test_load_palettes_skips_non_gimp_palettes():
    catalog = object.__new__(_ThreadCatalog)
    catalog.palettes = []
    invalid_palette = Mock(is_gimp_palette=False)

    with patch("lib.threads.catalog.glob", return_value=["/tmp/InkStitch-bad.gpl"]), patch(
        "lib.threads.catalog.ThreadPalette",
        return_value=invalid_palette,
    ):
        catalog.load_palettes(["/tmp"])

    assert catalog.palettes == []


def test_apply_palette_returns_early_for_none_palette():
    color = DummyColor(
        name="normal name",
        number="N1",
        manufacturer="normal manufacturer",
        description="normal description",
    )
    stitch_plan = [DummyColorBlock(color)]

    catalog = object.__new__(_ThreadCatalog)
    catalog.apply_palette(stitch_plan, None)

    assert color.name == "normal name"
    assert color.number == "N1"
    assert color.manufacturer == "normal manufacturer"
    assert color.description == "normal description"


def test_apply_palette_does_not_overwrite_cutwork_colors():
    cutwork_color = DummyColor(
        name="cutwork name",
        number="CW1",
        manufacturer="cutwork manufacturer",
        description="cutwork description",
        chart="cutwork chart",
    )
    normal_color = DummyColor(
        name="normal name",
        number="N1",
        manufacturer="normal manufacturer",
        description="normal description",
    )
    stitch_plan = [DummyColorBlock(cutwork_color), DummyColorBlock(normal_color)]

    nearest = DummyColor(
        name="palette name",
        number="P1",
        manufacturer="palette manufacturer",
        description="palette description",
    )
    palette = Mock()
    palette.nearest_color.return_value = nearest

    catalog = object.__new__(_ThreadCatalog)
    catalog.apply_palette(stitch_plan, palette)

    assert cutwork_color.name == "cutwork name"
    assert cutwork_color.number == "CW1"
    assert cutwork_color.manufacturer == "cutwork manufacturer"
    assert cutwork_color.description == "cutwork description"

    assert normal_color.name == "palette name"
    assert normal_color.number == "P1"
    assert normal_color.manufacturer == "palette manufacturer"
    assert normal_color.description == "palette description"

    assert palette.nearest_color.call_args_list == [call(normal_color)]


def test_apply_palette_overwrites_non_cutwork_colors():
    first = DummyColor(
        name="first",
        number="1",
        manufacturer="m1",
        description="d1",
    )
    second = DummyColor(
        name="second",
        number="2",
        manufacturer="m2",
        description="d2",
    )
    stitch_plan = [DummyColorBlock(first), DummyColorBlock(second)]

    nearest = DummyColor(
        name="palette name",
        number="P1",
        manufacturer="palette manufacturer",
        description="palette description",
    )
    palette = Mock()
    palette.nearest_color.return_value = nearest

    catalog = object.__new__(_ThreadCatalog)
    catalog.apply_palette(stitch_plan, palette)

    assert first.name == "palette name"
    assert first.number == "P1"
    assert first.manufacturer == "palette manufacturer"
    assert first.description == "palette description"

    assert second.name == "palette name"
    assert second.number == "P1"
    assert second.manufacturer == "palette manufacturer"
    assert second.description == "palette description"

    assert palette.nearest_color.call_args_list == [call(first), call(second)]
