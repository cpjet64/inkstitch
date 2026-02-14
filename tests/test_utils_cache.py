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
    CachedThing.compute.cache_clear()


def test_cache_decorator_uses_bounded_maxsize():
    assert CachedThing.compute.cache_info().maxsize == METHOD_CACHE_SIZE
    CachedThing.compute.cache_clear()
