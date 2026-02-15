import re
from pathlib import Path

from lib.sew_stack.stitch_layers.classproperty import classproperty
from lib.sew_stack.stitch_layers.stitch_layer_editor import StitchLayerEditor


class Base:
    @classproperty
    def value(cls: type["Base"]) -> str:
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


def test_stitch_layer_editor_error_message_mentions_classproperty():
    class BrokenEditor(StitchLayerEditor):
        pass

    try:
        BrokenEditor.properties
    except NotImplementedError as error:
        assert "classproperty" in str(error)
    else:
        raise AssertionError("Expected BrokenEditor.properties to raise NotImplementedError")
