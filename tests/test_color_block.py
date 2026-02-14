import pytest

from lib.stitch_plan.color_block import ColorBlock


def test_add_stitch_accepts_coordinate_arguments():
    color_block = ColorBlock()

    color_block.add_stitch(3, 4)

    assert len(color_block.stitches) == 1
    assert color_block.stitches[0].x == 3
    assert color_block.stitches[0].y == 4


def test_add_stitch_rejects_command_on_empty_block():
    color_block = ColorBlock()

    with pytest.raises(ValueError):
        color_block.add_stitch(stop=True)
