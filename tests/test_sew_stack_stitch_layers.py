import importlib


def test_stitch_layers_module_uses_dunder_all_for_exports():
    module = importlib.import_module("lib.sew_stack.stitch_layers")

    assert hasattr(module, "__all__")
    assert module.__all__ == ["RunningStitchLayer"]
    exported_layer = getattr(module, module.__all__[0])
    assert module.by_id[exported_layer.layer_id] is exported_layer
