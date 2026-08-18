import pytest
from pydantic import ValidationError

from app.schemas.energy_profile import (
    EnergyGoal,
    EnergyProfile,
    PropertyType,
    TechnologyPreference,
    ValueSource,
)


def test_empty_energy_profile_is_valid() -> None:
    profile = EnergyProfile()

    assert profile.location.country is None
    assert profile.energy.monthly_energy_kwh is None
    assert profile.goals == []
    assert profile.preferred_technologies == []


def test_energy_profile_accepts_valid_user_data() -> None:
    profile = EnergyProfile(
        location={
            "country": "Sri Lanka",
            "city": "Galle",
        },
        property={
            "property_type": PropertyType.HOTEL,
            "roof_area_m2": 450,
        },
        energy={
            "monthly_electricity_bill_lkr": 250000,
        },
        financial={
            "budget_lkr": 5000000,
        },
        goals=[
            EnergyGoal.REDUCE_ELECTRICITY_COST,
            EnergyGoal.BACKUP_POWER,
        ],
        preferred_technologies=[
            TechnologyPreference.SOLAR_PV,
            TechnologyPreference.BATTERY_STORAGE,
        ],
        field_sources={
            "location.city": ValueSource.USER_PROVIDED,
            "energy.monthly_electricity_bill_lkr":
                ValueSource.USER_PROVIDED,
        },
    )

    assert profile.location.city == "Galle"
    assert profile.property.property_type == PropertyType.HOTEL
    assert profile.energy.monthly_electricity_bill_lkr == 250000
    assert profile.financial.budget_lkr == 5000000


def test_unknown_information_remains_none() -> None:
    profile = EnergyProfile(
        location={
            "city": "Colombo",
        }
    )

    assert profile.energy.monthly_energy_kwh is None
    assert profile.property.roof_area_m2 is None
    assert profile.financial.budget_lkr is None


def test_negative_energy_usage_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EnergyProfile(
            energy={
                "monthly_energy_kwh": -100,
            }
        )


def test_negative_roof_area_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EnergyProfile(
            property={
                "roof_area_m2": -25,
            }
        )


def test_unknown_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        EnergyProfile(
            location={
                "city": "Colombo",
                "invented_field": "invalid",
            }
        )