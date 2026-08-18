import pytest

from app.agents.requirement_intelligence.normalization import (
    normalize_area_to_m2,
    normalize_duration_to_hours,
    normalize_energy_to_kwh,
    normalize_input_text,
    normalize_lkr_amount,
    normalize_payback_to_years,
    normalize_power_to_kw,
)


def test_input_text_is_cleaned_without_changing_meaning() -> None:
    text = "  I\u200b live \n in   Galle.  "

    assert normalize_input_text(text) == "I live in Galle."


def test_square_feet_are_converted_to_square_metres() -> None:
    result = normalize_area_to_m2(1500, "sq ft")

    assert result == pytest.approx(139.35456)


def test_mwh_is_converted_to_kwh() -> None:
    result = normalize_energy_to_kwh(1.2, "MWh")

    assert result == pytest.approx(1200)


def test_watts_are_converted_to_kw() -> None:
    result = normalize_power_to_kw(5000, "W")

    assert result == pytest.approx(5)


def test_lkr_millions_are_normalized() -> None:
    result = normalize_lkr_amount(2.5, "million")

    assert result == pytest.approx(2_500_000)


def test_minutes_are_converted_to_hours() -> None:
    result = normalize_duration_to_hours(90, "minutes")

    assert result == pytest.approx(1.5)


def test_months_are_converted_to_years() -> None:
    result = normalize_payback_to_years(36, "months")

    assert result == pytest.approx(3)


def test_unknown_unit_is_rejected() -> None:
    with pytest.raises(ValueError):
        normalize_area_to_m2(100, "acres")


def test_negative_measurement_is_rejected() -> None:
    with pytest.raises(ValueError):
        normalize_energy_to_kwh(-500, "kWh")