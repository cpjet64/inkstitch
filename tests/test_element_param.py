import pytest

from lib.elements.element import EmbroideryElement, Param


def test_param_default_lists_are_not_shared_between_instances():
    first = Param("a", "desc")
    second = Param("b", "desc")

    first.values.append("x")
    first.options.append("opt")

    assert second.values == [""]
    assert second.options == []


def test_param_copies_caller_lists():
    values = ["v1", "v2"]
    options = ["o1"]

    param = Param("a", "desc", values=values, options=options)

    values.append("v3")
    options.append("o2")

    assert param.values == ["v1", "v2"]
    assert param.options == ["o1"]


def test_shape_not_implemented_message_is_formatted():
    element = object.__new__(EmbroideryElement)

    with pytest.raises(NotImplementedError, match="EmbroideryElement must implement shape\\(\\)"):
        EmbroideryElement.shape.fget(element)


def test_first_stitch_not_implemented_message_is_formatted():
    element = object.__new__(EmbroideryElement)

    with pytest.raises(NotImplementedError, match="EmbroideryElement must implement first_stitch\\(\\)"):
        EmbroideryElement.first_stitch.fget(element)
