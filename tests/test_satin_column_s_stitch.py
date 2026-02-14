from lib.elements.satin_column import SatinColumn
from lib.utils.geometry import Point


class DummySatinColumn:
    color = None
    zigzag_spacing = 10
    max_stitch_length_px = 2
    pull_compensation_px = 0
    pull_compensation_percent = 0
    random_split_jitter = 0
    random_split_phase = False
    min_random_split_length_px = None
    random_seed = 0

    def __init__(self):
        self._pairs = [
            (Point(0, 0), Point(10, 0)),
            (Point(0, 5), Point(10, 5)),
        ]

    def plot_points_on_rails(self, *args, **kwargs):
        return list(self._pairs)

    def inset_short_stitches_sawtooth(self, pairs):
        return list(pairs)

    def get_split_points(self, *args, **kwargs):
        if len(args) == 5:
            # This branch is used for inter-row subdivision stitches.
            return [Point(99, 99)], None
        return [], None

    def _center_walk_is_odd(self):
        return False


def test_do_s_stitch_includes_inter_row_subdivision_points():
    satin = DummySatinColumn()

    stitch_group = SatinColumn.do_s_stitch(satin)

    stitch_coords = [(stitch.x, stitch.y) for stitch in stitch_group.stitches]
    assert (99, 99) in stitch_coords
