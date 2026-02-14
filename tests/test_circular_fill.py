from lib.stitches.circular_fill import _apply_bean_stitch_and_repeats


def test_apply_bean_stitch_and_repeats_uses_linear_growth():
    stitches = [1, 2]

    result = _apply_bean_stitch_and_repeats(stitches, repeats=3, bean_stitch_repeats=[0])

    assert result == [1, 2, 2, 1, 1, 2]
