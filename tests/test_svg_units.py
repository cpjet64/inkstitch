import pytest

from lib.svg.units import convert_length, parse_length_with_units


def test_parse_length_with_units_accepts_svg_lengths():
    assert parse_length_with_units("10mm") == (10.0, "mm")
    assert parse_length_with_units("25px") == (25.0, "px")


def test_parse_length_with_units_rejects_invalid_units():
    with pytest.raises(ValueError):
        parse_length_with_units("10unknown")


def test_convert_length_converts_mm_to_px():
    result = convert_length("25.4mm")

    assert result == pytest.approx(96.0)
