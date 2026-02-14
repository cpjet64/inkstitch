import ast
import inspect
import textwrap

from lib.gui.test_swatches import GenerateSwatchesFrame


def _count_wx_frame_init_calls(source):
    tree = ast.parse(source)
    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        if (
            isinstance(function, ast.Attribute)
            and function.attr == "__init__"
            and isinstance(function.value, ast.Attribute)
            and function.value.attr == "Frame"
            and isinstance(function.value.value, ast.Name)
            and function.value.value.id == "wx"
        ):
            count += 1
    return count


def test_generate_swatches_frame_initializes_wx_frame_once():
    source = inspect.getsource(GenerateSwatchesFrame.__init__)
    call_count = _count_wx_frame_init_calls(textwrap.dedent(source))

    assert call_count == 1
