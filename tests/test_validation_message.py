from lib.elements.validation import ValidationMessage


class DummyValidationMessage(ValidationMessage):
    steps_to_solve = ["one", "two"]


def test_validation_message_steps_to_solve_are_instance_local():
    first = DummyValidationMessage()
    second = DummyValidationMessage()

    first.steps_to_solve.append("three")

    assert second.steps_to_solve == ["one", "two"]
