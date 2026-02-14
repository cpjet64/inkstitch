from lib.stitch_plan import Stitch, StitchGroup


class DummyLockStitches:
    def stitches(self, stitches, pos):
        return [f"{pos}-lock", len(stitches)]


def test_get_lock_stitches_returns_empty_list_when_lock_missing():
    group = StitchGroup(stitches=[Stitch(0, 0), Stitch(1, 1)], lock_stitches=(None, None))

    assert group.get_lock_stitches("start") == []
    assert group.get_lock_stitches("end") == []


def test_get_lock_stitches_returns_empty_list_when_ties_disabled():
    lock = DummyLockStitches()
    group = StitchGroup(stitches=[Stitch(0, 0), Stitch(1, 1)], lock_stitches=(lock, lock))

    assert group.get_lock_stitches("start", disable_ties=True) == []


def test_get_lock_stitches_returns_generated_lock_stitches():
    start_lock = DummyLockStitches()
    end_lock = DummyLockStitches()
    group = StitchGroup(stitches=[Stitch(0, 0), Stitch(1, 1)], lock_stitches=(start_lock, end_lock))

    assert group.get_lock_stitches("start") == ["start-lock", 2]
    assert group.get_lock_stitches("end") == ["end-lock", 2]
