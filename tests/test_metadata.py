from lib.metadata import InkStitchMetadata


class DummyChild:
    def __init__(self, tag, prefix):
        self.tag = tag
        self.prefix = prefix


def test_len_returns_zero_for_empty_metadata():
    metadata = object.__new__(InkStitchMetadata)
    metadata.metadata = []

    assert len(metadata) == 0


def test_len_counts_only_inkstitch_metadata_items():
    metadata = object.__new__(InkStitchMetadata)
    metadata.metadata = [
        DummyChild("{inkstitch}thread-palette", "inkstitch"),
        DummyChild("{inkstitch}collapse_len_mm", "inkstitch"),
        DummyChild("{http://www.w3.org/2000/svg}title", "svg"),
    ]

    assert len(metadata) == 2
