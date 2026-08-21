"""Transparent and replayable feasibility scoring for the AgriScore pilot."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping

from app.domain.models import (
    AssessmentRequest,
    AssessmentStatus,
    ComponentResult,
    DeterministicAssessment,
    FactorInput,
    FactorTrace,
    ScoreBand,
)
from app.scoring.pilot_scope import pilot_review_reasons


POLICY_PATH = Path(__file__).resolve().parents[2] / "config" / "pilot_policy.json"


@dataclass(frozen=True)
class ScoringPolicy:
    policy_id: str
    policy_hash: str
    weights: Mapping[str, float]
    factor_weights: Mapping[str, Mapping[str, float]]
    bands: tuple[tuple[float, ScoreBand], ...]
    minimum_evidence_quality: float
    review_required_factor_floor: float
    max_evidence_age_days: int


class PolicyError(ValueError):
    """Raised when a policy cannot produce deterministic scores."""


def load_policy(path: Path = POLICY_PATH) -> ScoringPolicy:
    raw = path.read_bytes()
    document = json.loads(raw)
    policy_hash = hashlib.sha256(raw).hexdigest()

    weights = document["weights"]
    if round(sum(weights.values()), 10) != 1.0:
        raise PolicyError("Component weights must sum exactly to 1.0")

    factor_weights = document["factor_weights"]
    for component, component_weights in factor_weights.items():
        if round(sum(component_weights.values()), 10) != 1.0:
            raise PolicyError(f"Factor weights for {component} must sum exactly to 1.0")

    bands = tuple(
        (float(item["minimum_score"]), ScoreBand(item["label"]))
        for item in sorted(document["bands"], key=lambda item: item["minimum_score"], reverse=True)
    )
    if not bands or bands[-1][0] != 0:
        raise PolicyError("Bands must include a zero minimum score")

    quality_gates = document["quality_gates"]
    return ScoringPolicy(
        policy_id=document["policy_id"],
        policy_hash=policy_hash,
        weights=weights,
        factor_weights=factor_weights,
        bands=bands,
        minimum_evidence_quality=float(
            quality_gates["minimum_evidence_quality_for_decision_support"]
        ),
        review_required_factor_floor=float(quality_gates["review_required_factor_floor"]),
        max_evidence_age_days=int(quality_gates["max_evidence_age_days"]),
    )


def _factor_trace(
    name: str,
    factor: FactorInput,
    weight: float,
    assessment_date: date,
    max_age_days: int,
) -> FactorTrace:
    age_days = (assessment_date - factor.evidence.observed_on).days
    is_stale = age_days > max_age_days
    return FactorTrace(
        factor=name,
        value=round(factor.value, 2),
        weight_within_component=weight,
        weighted_contribution=round(factor.value * weight, 2),
        evidence_source=factor.evidence.source,
        observed_on=factor.evidence.observed_on,
        evidence_quality=factor.evidence.quality,
        is_stale=is_stale,
    )


def _score_component(
    name: str,
    values: Any,
    component_weight: float,
    factor_weights: Mapping[str, float],
    assessment_date: date,
    max_age_days: int,
) -> ComponentResult:
    traces = [
        _factor_trace(
            factor_name,
            getattr(values, factor_name),
            factor_weight,
            assessment_date,
            max_age_days,
        )
        for factor_name, factor_weight in factor_weights.items()
    ]
    score = sum(trace.weighted_contribution for trace in traces)
    return ComponentResult(
        name=name,  # type: ignore[arg-type]
        weight=component_weight,
        score=round(score, 2),
        factor_traces=traces,
    )


def _band_for(score: float, bands: Iterable[tuple[float, ScoreBand]]) -> ScoreBand:
    for minimum, band in bands:
        if score >= minimum:
            return band
    raise PolicyError("No score band matched")


def _quality_and_reasons(
    components: list[ComponentResult], policy: ScoringPolicy
) -> tuple[float, list[str]]:
    traces = [trace for component in components for trace in component.factor_traces]
    evidence_quality = sum(trace.evidence_quality for trace in traces) / len(traces)
    reasons: list[str] = []

    if evidence_quality < policy.minimum_evidence_quality:
        reasons.append(
            "Average evidence quality is below the pilot threshold for decision-support readiness."
        )

    stale_factors = [trace.factor for trace in traces if trace.is_stale]
    if stale_factors:
        reasons.append(f"Evidence is stale for: {', '.join(stale_factors)}.")

    low_quality_factors = [
        trace.factor
        for trace in traces
        if trace.evidence_quality < policy.review_required_factor_floor
    ]
    if low_quality_factors:
        reasons.append(
            "Evidence quality is critically low for: " + ", ".join(low_quality_factors) + "."
        )

    return round(evidence_quality, 3), reasons


def calculate_assessment(
    request: AssessmentRequest,
    policy: ScoringPolicy | None = None,
    assessment_date: date | None = None,
) -> DeterministicAssessment:
    """Calculate the score without an LLM or external side effects."""

    active_policy = policy or load_policy()
    today = assessment_date or date.today()

    components = [
        _score_component(
            "agronomic",
            request.agronomic,
            active_policy.weights["agronomic"],
            active_policy.factor_weights["agronomic"],
            today,
            active_policy.max_evidence_age_days,
        ),
        _score_component(
            "climate",
            request.climate,
            active_policy.weights["climate"],
            active_policy.factor_weights["climate"],
            today,
            active_policy.max_evidence_age_days,
        ),
        _score_component(
            "market",
            request.market,
            active_policy.weights["market"],
            active_policy.factor_weights["market"],
            today,
            active_policy.max_evidence_age_days,
        ),
    ]
    score = sum(component.score * component.weight for component in components)
    score = round(score, 2)
    evidence_quality, reasons = _quality_and_reasons(components, active_policy)
    reasons.extend(pilot_review_reasons(request))
    status = AssessmentStatus.REVIEW_REQUIRED if reasons else AssessmentStatus.DECISION_SUPPORT

    return DeterministicAssessment(
        policy_id=active_policy.policy_id,
        policy_hash=active_policy.policy_hash,
        feasibility_score=score,
        band=_band_for(score, active_policy.bands),
        status=status,
        evidence_quality=evidence_quality,
        review_reasons=reasons,
        components=components,
    )
