import re
import unicodedata


_SQUARE_FEET_TO_SQUARE_METRES = 0.09290304

_AREA_UNIT_FACTORS = {
    "m2": 1.0,
    "sqm": 1.0,
    "sq m": 1.0,
    "square meter": 1.0,
    "square meters": 1.0,
    "square metre": 1.0,
    "square metres": 1.0,
    "ft2": _SQUARE_FEET_TO_SQUARE_METRES,
    "sq ft": _SQUARE_FEET_TO_SQUARE_METRES,
    "square foot": _SQUARE_FEET_TO_SQUARE_METRES,
    "square feet": _SQUARE_FEET_TO_SQUARE_METRES,
}

_ENERGY_UNIT_FACTORS = {
    "wh": 0.001,
    "kwh": 1.0,
    "mwh": 1000.0,
}

_POWER_UNIT_FACTORS = {
    "w": 0.001,
    "kw": 1.0,
    "mw": 1000.0,
}

_DURATION_UNIT_FACTORS = {
    "minute": 1 / 60,
    "minutes": 1 / 60,
    "min": 1 / 60,
    "hour": 1.0,
    "hours": 1.0,
    "hr": 1.0,
    "hrs": 1.0,
    "day": 24.0,
    "days": 24.0,
}

_PAYBACK_UNIT_FACTORS = {
    "month": 1 / 12,
    "months": 1 / 12,
    "year": 1.0,
    "years": 1.0,
}

_MAGNITUDE_FACTORS = {
    "thousand": 1_000.0,
    "k": 1_000.0,
    "million": 1_000_000.0,
    "mn": 1_000_000.0,
    "m": 1_000_000.0,
    "billion": 1_000_000_000.0,
    "bn": 1_000_000_000.0,
    "b": 1_000_000_000.0,
}


def normalize_input_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)

    normalized = "".join(
        character
        for character in normalized
        if not unicodedata.category(character).startswith("C")
        or character in "\n\t"
    )

    return re.sub(r"\s+", " ", normalized).strip()


def normalize_area_to_m2(value: float, unit: str) -> float:
    return _convert_measurement(
        value=value,
        unit=unit,
        factors=_AREA_UNIT_FACTORS,
    )


def normalize_energy_to_kwh(value: float, unit: str) -> float:
    return _convert_measurement(
        value=value,
        unit=unit,
        factors=_ENERGY_UNIT_FACTORS,
    )


def normalize_power_to_kw(value: float, unit: str) -> float:
    return _convert_measurement(
        value=value,
        unit=unit,
        factors=_POWER_UNIT_FACTORS,
    )


def normalize_duration_to_hours(value: float, unit: str) -> float:
    return _convert_measurement(
        value=value,
        unit=unit,
        factors=_DURATION_UNIT_FACTORS,
    )


def normalize_payback_to_years(value: float, unit: str) -> float:
    return _convert_measurement(
        value=value,
        unit=unit,
        factors=_PAYBACK_UNIT_FACTORS,
    )


def normalize_lkr_amount(
    value: float,
    magnitude: str | None = None,
) -> float:
    _validate_non_negative(value)

    if magnitude is None:
        return float(value)

    normalized_magnitude = _normalize_unit(magnitude)

    try:
        factor = _MAGNITUDE_FACTORS[normalized_magnitude]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported monetary magnitude: {magnitude}"
        ) from exc

    return float(value) * factor


def _convert_measurement(
    value: float,
    unit: str,
    factors: dict[str, float],
) -> float:
    _validate_non_negative(value)

    normalized_unit = _normalize_unit(unit)

    try:
        factor = factors[normalized_unit]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported unit: {unit}"
        ) from exc

    return float(value) * factor


def _normalize_unit(unit: str) -> str:
    normalized = unicodedata.normalize("NFKC", unit)
    normalized = normalized.lower().strip().replace(".", "")
    return re.sub(r"\s+", " ", normalized)


def _validate_non_negative(value: float) -> None:
    if value < 0:
        raise ValueError("Measurement values cannot be negative")