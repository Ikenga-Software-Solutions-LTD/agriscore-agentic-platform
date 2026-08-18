from __future__ import annotations

import asyncio
from datetime import date

from fastapi.testclient import TestClient

from app.agents.assessment_brain import AssessmentBrain
from app.api.main import create_app
from app.domain.models import AssessmentRequest
from app.scoring.engine import calculate_assessment


def _factor(value: float = 70.0) -> dict:
    return {
        "value": value,
        "evidence": {
            "source": "test-fixture",
            "observed_on": date.today().isoformat(),
            "quality": 0.9,
        },
    }


def _payload() -> dict:
    return {
        "assessment_reference": "TEST-PLOT-2",
        "crop": "test crop",
        "country_code": "JAM",
        "planting_date": date.today().isoformat(),
        "agronomic": {
            "crop_compatibility": _factor(80),
            "soil_ph_fit": _factor(70),
            "nutrient_adequacy": _factor(60),
            "drainage": _factor(90),
        },
        "climate": {
            "precipitation_fit": _factor(70),
            "drought_resilience": _factor(60),
            "storm_exposure": _factor(50),
            "planting_window": _factor(80),
        },
        "market": {
            "demand_signal": _factor(80),
            "price_trend": _factor(70),
            "import_substitution_priority": _factor(60),
        },
    }


def test_health_exposes_policy_version() -> None:
    response = TestClient(create_app()).get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["policy_id"] == "agriscore-pilot-feasibility-v0.1"


def test_assessment_uses_fallback_without_llm_configuration(monkeypatch) -> None:
    monkeypatch.delenv("AGRI_LLM_API_KEY", raising=False)
    monkeypatch.delenv("AGRI_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_BASE", raising=False)

    response = TestClient(create_app()).post("/v1/assessments", json=_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["narrative"]["generated_by"] == "deterministic_fallback"
    assert body["audit"]["agent_mode"] == "deterministic_fallback"
    assert body["assessment"]["status"] == "DECISION_SUPPORT"
    assert "does not approve" in body["disclaimer"]
    assert "loan_amount" not in body["narrative"]


def test_brain_fallback_does_not_change_completed_assessment(monkeypatch) -> None:
    monkeypatch.delenv("AGRI_LLM_API_KEY", raising=False)
    monkeypatch.delenv("AGRI_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_BASE", raising=False)
    request = AssessmentRequest.model_validate(_payload())
    assessment = calculate_assessment(request, assessment_date=date.today())

    result = asyncio.run(AssessmentBrain().narrate(request, assessment))

    assert result.narrative.generated_by == "deterministic_fallback"
    assert str(assessment.feasibility_score) in result.narrative.executive_summary
    assert "credit" in result.narrative.executive_summary.lower()
