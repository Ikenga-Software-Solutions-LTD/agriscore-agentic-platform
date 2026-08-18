"""Typed contracts for AgriScore's evidence-driven assessment workflow.

This module deliberately excludes personal-credit attributes and downstream lending
terms. The request captures only the agronomic, climate, market, and evidence-quality
inputs needed by the v0.1 feasibility policy.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AssessmentStatus(StrEnum):
    DECISION_SUPPORT = "DECISION_SUPPORT"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class ScoreBand(StrEnum):
    HIGH_FEASIBILITY = "HIGH_FEASIBILITY"
    FAVORABLE_FEASIBILITY = "FAVORABLE_FEASIBILITY"
    CONDITIONAL_FEASIBILITY = "CONDITIONAL_FEASIBILITY"
    LOW_FEASIBILITY = "LOW_FEASIBILITY"


class EvidenceItem(BaseModel):
    """A normalized evidence item supporting a factor score.

    `quality` is an upstream quality assessment in [0, 1], not a model confidence.
    `observed_on` is intentionally required to prevent timeless evidence from silently
    influencing the assessment.
    """

    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=2, max_length=120)
    observed_on: date
    quality: float = Field(ge=0.0, le=1.0)
    note: str | None = Field(default=None, max_length=500)


class FactorInput(BaseModel):
    """One normalized 0-100 factor supplied by a validated upstream process."""

    model_config = ConfigDict(extra="forbid")

    value: float = Field(ge=0.0, le=100.0)
    evidence: EvidenceItem


class AgronomicInputs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    crop_compatibility: FactorInput
    soil_ph_fit: FactorInput
    nutrient_adequacy: FactorInput
    drainage: FactorInput


class ClimateInputs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    precipitation_fit: FactorInput
    drought_resilience: FactorInput
    storm_exposure: FactorInput
    planting_window: FactorInput


class MarketInputs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    demand_signal: FactorInput
    price_trend: FactorInput
    import_substitution_priority: FactorInput


class AssessmentRequest(BaseModel):
    """A de-identified crop feasibility request.

    The API does not persist this object. `assessment_reference` is caller-managed and
    may be a pseudonymous plot identifier, never a national ID or loan application ID.
    """

    model_config = ConfigDict(extra="forbid")

    assessment_reference: str = Field(min_length=3, max_length=80, pattern=r"^[A-Za-z0-9_.-]+$")
    crop: str = Field(min_length=2, max_length=80)
    country_code: str = Field(min_length=2, max_length=3, pattern=r"^[A-Z]{2,3}$")
    planting_date: date
    agronomic: AgronomicInputs
    climate: ClimateInputs
    market: MarketInputs


class FactorTrace(BaseModel):
    model_config = ConfigDict(extra="forbid")

    factor: str
    value: float = Field(ge=0.0, le=100.0)
    weight_within_component: float = Field(gt=0.0, le=1.0)
    weighted_contribution: float = Field(ge=0.0, le=100.0)
    evidence_source: str
    observed_on: date
    evidence_quality: float = Field(ge=0.0, le=1.0)
    is_stale: bool


class ComponentResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Literal["agronomic", "climate", "market"]
    weight: float = Field(gt=0.0, le=1.0)
    score: float = Field(ge=0.0, le=100.0)
    factor_traces: list[FactorTrace]


class DeterministicAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_id: str
    policy_hash: str
    feasibility_score: float = Field(ge=0.0, le=100.0)
    band: ScoreBand
    status: AssessmentStatus
    evidence_quality: float = Field(ge=0.0, le=1.0)
    review_reasons: list[str]
    components: list[ComponentResult]


class AgentNarrative(BaseModel):
    """Constrained, non-authoritative LLM output.

    Each driver must map to a supplied score factor. This model intentionally has no
    fields for loan terms, approval decisions, prices, contracts, or predictions.
    """

    model_config = ConfigDict(extra="forbid")

    executive_summary: str = Field(min_length=1, max_length=1_200)
    positive_drivers: list[str] = Field(max_length=5)
    risk_drivers: list[str] = Field(max_length=5)
    remediation_actions: list[str] = Field(max_length=5)
    clarifying_questions: list[str] = Field(max_length=5)
    confidence_statement: str = Field(min_length=1, max_length=500)
    generated_by: Literal["llm", "deterministic_fallback"]


class AssessmentAudit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    assessment_id: str
    assessed_at: datetime
    request_fingerprint: str
    policy_id: str
    policy_hash: str
    agent_provider: str
    agent_model: str | None
    agent_mode: Literal["llm", "deterministic_fallback"]

    @field_validator("assessed_at", mode="before")
    @classmethod
    def ensure_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


class AssessmentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    assessment: DeterministicAssessment
    narrative: AgentNarrative
    audit: AssessmentAudit
    disclaimer: str
