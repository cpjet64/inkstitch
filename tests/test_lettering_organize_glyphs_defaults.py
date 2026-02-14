import ast
from pathlib import Path


def test_create_and_fill_group_uses_non_mutable_default_lists():
    source = Path("lib/extensions/lettering_organize_glyphs.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    target_function = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "LetteringOrganizeGlyphs":
            for class_item in node.body:
                if isinstance(class_item, ast.FunctionDef) and class_item.name == "_create_and_fill_group":
                    target_function = class_item
                    break

    assert target_function is not None

    arg_names = [argument.arg for argument in target_function.args.args]
    defaults_offset = len(arg_names) - len(target_function.args.defaults)

    excepting_default = target_function.args.defaults[arg_names.index("excepting") - defaults_offset]
    adding_default = target_function.args.defaults[arg_names.index("adding") - defaults_offset]

    assert isinstance(excepting_default, ast.Constant)
    assert excepting_default.value is None
    assert isinstance(adding_default, ast.Constant)
    assert adding_default.value is None
