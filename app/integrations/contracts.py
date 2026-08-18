"""Provider-neutral external data contracts.

Adapters normalize data before it reaches the scoring service. They must never inject
free-form provider output directly into prompts or mutate a completed assessment.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Protocol

from app.domain.models import FactorInput


@dataclass(frozen=True)
class GeoPoint:
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not -90 <= self.latitude <= 90:
            raise ValueError("latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("longitude must be between -180 and 180")


@dataclass(frozen=True)
class ProviderProvenance:
    provider: str
    retrieved_at: datetime
    source_time_start: date
    source_time_end: date
    source_reference: str | None
    quality_notes: str | None = None


@dataclass(frozen=True)
class ClimateEvidenceBundle:
    precipitation_fit: FactorInput
    drought_resilience: FactorInput
    storm_exposure: FactorInput
    planting_window: FactorInput
    provenance: ProviderProvenance


@dataclass(frozen=True)
class SoilEvidenceBundle:
    crop_compatibility: FactorInput
    soil_ph_fit: FactorInput
    nutrient_adequacy: FactorInput
    drainage: FactorInput
    provenance: ProviderProvenance


@dataclass(frozen=True)
class MarketEvidenceBundle:
    demand_signal: FactorInput
    price_trend: FactorInput
    import_substitution_priority: FactorInput
    provenance: ProviderProvenance


class ClimateProvider(Protocol):
    async def get_climate_evidence(
        self,
        point: GeoPoint,
        crop: str,
        planting_date: date,
    ) -> ClimateEvidenceBundle: ...


class SoilProvider(Protocol):
    async def get_soil_evidence(self, point: GeoPoint, crop: str) -> SoilEvidenceBundle: ...


class MarketProvider(Protocol):
    async def get_market_evidence(
        self,
        country_code: str,
        crop: str,
    ) -> MarketEvidenceBundle: ...
