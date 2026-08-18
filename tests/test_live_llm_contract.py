"""Opt-in integration test for a configured OpenAI-compatible model.

Run only when intentionally requested:
AGRI_RUN_LIVE_LLM_TEST=1 AGRI_LLM_MODEL=gpt-5-mini pytest tests/test_live_llm_contract.py
"""

from __future__ import annotations

import asyncio
import os
from datetime import date

import pytest

from app.agents.assessment_brain import AssessmentBrain
from app.domain.models import AssessmentRequest
from app.scoring.engine import calculate_assessment


pytestmark = pytest.mark.skipif(
    os.getenv("AGRI_RUN_LIVE_LLM_TEST") != "1",
    reason="Live LLM integration tests run only when explicitly enabled.",
)


def _factor(value: float) -> dict:
    return {
        "value": value,
        "evidence": {
            "source": "live-contract-fixture",
            "observed_on": date.today().isoformat(),
            "quality": 0.85,
        },
    }


def test_live_llm_returns_constrained_narrative() -> None:
    request = AssessmentRequest.model_validate(
        {
            "assessment_reference": "LIVE-CHECK-001",
            "crop": "test crop",
            "country_code": "JAM",
            "planting_date": date.today().isoformat(),
            "agronomic": {
                "crop_compatibility": _factor(80),
                "soil_ph_fit": _factor(72),
                "nutrient_adequacy": _factor(60),
                "drainage": _factor(84),
            },
            "climate": {
                "precipitation_fit": _factor(68),
                "drought_resilience": _factor(55),
                "storm_exposure": _factor(52),
                "planting_window": _factor(78),
            },
            "market": {
                "demand_signal": _factor(76),
                "price_trend": _factor(66),
                "import_substitution_priority": _factor(80),
            },
        }
    )
    assessment = calculate_assessment(request, assessment_date=date.today())
    result = asyncio.run(AssessmentBrain().narrate(request, assessment))

    assert result.narrative.generated_by == "llm"
    assert result.model
    assert 1 <= len(result.narrative.executive_summary) <= 1200
    assert "loan" not in result.narrative.model_dump_json().lower()
    assert "apr" not in result.narrative.model_dump_json().lower()
