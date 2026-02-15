from typing import Any, cast

from lib.utils.cache import METHOD_CACHE_SIZE, cache


class CachedThing:
    def __init__(self):
        self.calls = 0

    @cache
    def compute(self, value):
        self.calls += 1
        return value * 10


def test_cache_decorator_reuses_cached_method_result():
    thing = CachedThing()

    assert thing.compute(2) == 20
    assert thing.compute(2) == 20

    assert thing.calls == 1
    cached_compute = cast(Any, CachedThing.compute)
    cached_compute.cache_clear()


def test_cache_decorator_uses_bounded_maxsize():
    cached_compute = cast(Any, CachedThing.compute)
    assert cached_compute.cache_info().maxsize == METHOD_CACHE_SIZE
    cached_compute.cache_clear()
