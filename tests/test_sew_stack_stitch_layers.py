import importlib


def test_stitch_layers_module_uses_dunder_all_for_exports():
    module = importlib.import_module("lib.sew_stack.stitch_layers")

    assert hasattr(module, "__all__")
    assert module.by_id[module.__all__[0].layer_id] is module.__all__[0]
