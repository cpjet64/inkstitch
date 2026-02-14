from lib.stitch_plan import Stitch


def test_stitch_from_base_allows_explicit_falsy_overrides():
    base = Stitch(
        1,
        2,
        color="red",
        jump=True,
        stop=True,
        trim=True,
        color_change=True,
        min_stitch_length=1.5,
    )

    derived = Stitch(
        base,
        color="",
        jump=False,
        stop=False,
        trim=False,
        color_change=False,
        min_stitch_length=0,
    )

    assert derived.color == ""
    assert derived.jump is False
    assert derived.stop is False
    assert derived.trim is False
    assert derived.color_change is False
    assert derived.min_stitch_length == 0


def test_stitch_from_base_preserves_values_when_override_is_none():
    base = Stitch(
        1,
        2,
        color="blue",
        jump=True,
        min_stitch_length=2.0,
    )

    derived = Stitch(base, color=None, jump=None, min_stitch_length=None)

    assert derived.color == "blue"
    assert derived.jump is True
    assert derived.min_stitch_length == 2.0
