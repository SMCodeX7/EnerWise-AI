from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class PropertyType(StrEnum):
    RESIDENTIAL = "residential"
    SMALL_BUSINESS = "small_business"
    HOTEL = "hotel"
    OFFICE = "office"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    OTHER = "other"


class OwnershipStatus(StrEnum):
    OWNED = "owned"
    RENTED = "rented"
    UNKNOWN = "unknown"


class EnergyGoal(StrEnum):
    REDUCE_ELECTRICITY_COST = "reduce_electricity_cost"
    BACKUP_POWER = "backup_power"
    REDUCE_EMISSIONS = "reduce_emissions"
    ENERGY_INDEPENDENCE = "energy_independence"
    OTHER = "other"


class TechnologyPreference(StrEnum):
    SOLAR_PV = "solar_pv"
    BATTERY_STORAGE = "battery_storage"
    SMALL_WIND = "small_wind"


class ShadingLevel(StrEnum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    UNKNOWN = "unknown"


class ValueSource(StrEnum):
    USER_PROVIDED = "user_provided"
    INFERRED = "inferred"
    DERIVED = "derived"
    SYSTEM_DEFAULT = "system_default"


class LocationProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    country: str | None = None
    province: str | None = None
    district: str | None = None
    city: str | None = None


class PropertyProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    property_type: PropertyType | None = None
    ownership_status: OwnershipStatus = OwnershipStatus.UNKNOWN
    roof_area_m2: float | None = Field(default=None, gt=0)
    available_ground_area_m2: float | None = Field(default=None, ge=0)
    shading_level: ShadingLevel = ShadingLevel.UNKNOWN


class EnergyUsageProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    monthly_energy_kwh: float | None = Field(default=None, gt=0)
    monthly_electricity_bill_lkr: float | None = Field(default=None, ge=0)
    peak_demand_kw: float | None = Field(default=None, gt=0)
    backup_hours_required: float | None = Field(default=None, gt=0)


class FinancialProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    budget_lkr: float | None = Field(default=None, ge=0)
    target_payback_years: float | None = Field(default=None, gt=0)


class EnergyProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    location: LocationProfile = Field(default_factory=LocationProfile)
    property: PropertyProfile = Field(default_factory=PropertyProfile)
    energy: EnergyUsageProfile = Field(default_factory=EnergyUsageProfile)
    financial: FinancialProfile = Field(default_factory=FinancialProfile)

    goals: list[EnergyGoal] = Field(default_factory=list)
    preferred_technologies: list[TechnologyPreference] = Field(
        default_factory=list
    )

    constraints: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)

    field_sources: dict[str, ValueSource] = Field(default_factory=dict)