from lib.tartan.palette import Palette


def _stripe(width=5.0, color="#000000", render=1):
    return {"render": render, "color": color, "width": width}


def test_palette_default_stripes_are_not_shared_between_instances():
    first = Palette()
    second = Palette()

    first.palette_stripes[0].append(_stripe())

    assert first.palette_stripes[0] != second.palette_stripes[0]
    assert second.palette_stripes == [[], []]


def test_update_code_asymmetric_uses_serialized_code_string():
    palette = Palette(
        palette_stripes=[[_stripe(width=4.0, color="#112233")], []],
        symmetry=False,
        equal_warp_weft=True,
    )

    palette.update_code()

    assert palette.palette_code == "...(#112233)4.0..."
    assert "[" not in palette.palette_code
