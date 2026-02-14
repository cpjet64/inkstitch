from shapely.geometry import Point as ShapelyPoint

from lib.elements.validation import ValidationMessage


def test_validation_message_accepts_none_position():
    message = ValidationMessage(position=None, label="test")

    assert message.position is None
    assert message.label == "test"


def test_validation_message_converts_tuple_position():
    message = ValidationMessage(position=(1.25, 2.5))

    assert message.position is not None
    assert message.position.x == 1.25
    assert message.position.y == 2.5


def test_validation_message_converts_shapely_point_position():
    message = ValidationMessage(position=ShapelyPoint(3, 4))

    assert message.position is not None
    assert message.position.x == 3
    assert message.position.y == 4
