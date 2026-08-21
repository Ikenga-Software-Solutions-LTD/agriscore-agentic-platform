from __future__ import annotations

from datetime import date

from app.domain.models import AssessmentRequest
from app.scoring.engine import calculate_assessment, load_policy


def _factor(value: float, quality: float = 0.9) -> dict:
    return {
        "value": value,
        "evidence": {
            "source": "test-fixture",
            "observed_on": date.today().isoformat(),
            "quality": quality,
        },
    }


def _request(quality: float = 0.9) -> AssessmentRequest:
    return AssessmentRequest.model_validate(
        {
            "assessment_reference": "TEST-PLOT-1",
            "crop": "test crop",
            "country_code": "JAM",
            "planting_date": date.today().isoformat(),
            "agronomic": {
                "crop_compatibility": _factor(80, quality),
                "soil_ph_fit": _factor(60, quality),
                "nutrient_adequacy": _factor(70, quality),
                "drainage": _factor(90, quality),
            },
            "climate": {
                "precipitation_fit": _factor(50, quality),
                "drought_resilience": _factor(40, quality),
                "storm_exposure": _factor(60, quality),
                "planting_window": _factor(80, quality),
            },
            "market": {
                "demand_signal": _factor(75, quality),
                "price_trend": _factor(65, quality),
                "import_substitution_priority": _factor(55, quality),
            },
        }
    )


def test_component_and_composite_score_are_replayable() -> None:
    result = calculate_assessment(_request(), assessment_date=date.today())

    components = {component.name: component.score for component in result.components}
    assert components["agronomic"] == 73.5
    assert components["climate"] == 54.5
    assert components["market"] == 67.5
    assert result.feasibility_score == 65.7
    assert result.band == "CONDITIONAL_FEASIBILITY"
    assert result.status == "DECISION_SUPPORT"
    assert result.evidence_quality == 0.9


def test_low_evidence_quality_requires_review_without_changing_score() -> None:
    high_quality = calculate_assessment(_request(quality=0.9), assessment_date=date.today())
    low_quality = calculate_assessment(_request(quality=0.3), assessment_date=date.today())

    assert low_quality.feasibility_score == high_quality.feasibility_score
    assert low_quality.status == "REVIEW_REQUIRED"
    assert low_quality.review_reasons


def test_policy_is_valid_and_has_reproducibility_hash() -> None:
    policy = load_policy()

    assert policy.policy_id == "agriscore-pilot-feasibility-v0.1"
    assert len(policy.policy_hash) == 64
    assert sum(policy.weights.values()) == 1.0


def test_guyana_maize_requires_profile_approval_without_changing_score() -> None:
    generic_request = _request()
    guyana_request = generic_request.model_copy(update={"country_code": "GUY", "crop": "maize"})

    generic_result = calculate_assessment(generic_request, assessment_date=date.today())
    guyana_result = calculate_assessment(guyana_request, assessment_date=date.today())

    assert guyana_result.feasibility_score == generic_result.feasibility_score
    assert guyana_result.status == "REVIEW_REQUIRED"
    assert any("PENDING_AGRONOMIC_REVIEW" in reason for reason in guyana_result.review_reasons)


def test_guyana_ginger_requires_profile_approval() -> None:
    ginger_request = _request().model_copy(update={"country_code": "GUY", "crop": "ginger"})

    result = calculate_assessment(ginger_request, assessment_date=date.today())

    assert result.status == "REVIEW_REQUIRED"
    assert any("guyana-ginger" in reason for reason in result.review_reasons)
