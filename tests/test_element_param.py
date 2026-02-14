from lib.elements.element import Param


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
