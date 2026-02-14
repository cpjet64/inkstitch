import re
from pathlib import Path

from lib.sew_stack.stitch_layers.classproperty import classproperty


class Base:
    @classproperty
    def value(cls):
        return cls.__name__


def test_classproperty_descriptor_works_for_class_and_instance_access():
    assert Base.value == "Base"
    assert Base().value == "Base"


def test_sew_stack_uses_classproperty_instead_of_classmethod_property_stack():
    files = [
        "lib/sew_stack/stitch_layers/stitch_layer.py",
        "lib/sew_stack/stitch_layers/stitch_layer_editor.py",
        "lib/sew_stack/stitch_layers/running_stitch/running_stitch_layer.py",
    ]

    for file_path in files:
        source = Path(file_path).read_text(encoding="utf-8")
        assert re.search(r"@classmethod\\s*\\n\\s*@property", source) is None
