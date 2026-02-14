import ast
from pathlib import Path


def test_prompting_combobox_uses_non_mutable_default_choices():
    source = Path("lib/gui/edit_json/combo_prompt.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    init_function = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "PromptingComboBox":
            for class_item in node.body:
                if isinstance(class_item, ast.FunctionDef) and class_item.name == "__init__":
                    init_function = class_item
                    break

    assert init_function is not None
    arg_names = [argument.arg for argument in init_function.args.args]
    choices_index = arg_names.index("choices")
    defaults_offset = len(arg_names) - len(init_function.args.defaults)
    choices_default = init_function.args.defaults[choices_index - defaults_offset]
    assert isinstance(choices_default, ast.Constant)
    assert choices_default.value is None
