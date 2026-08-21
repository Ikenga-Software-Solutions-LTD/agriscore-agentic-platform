"""FastAPI entry point for the AgriScore baseline decision-support service."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.agents.assessment_brain import AssessmentBrain
from app.domain.models import AssessmentAudit, AssessmentRequest, AssessmentResponse
from app.scoring.engine import calculate_assessment, load_policy
from app.scoring.pilot_scope import load_guyana_pilot_scope


APP_VERSION = "0.1.0"
DISCLAIMER = (
    "AgriScore is a crop-feasibility decision-support prototype. It does not approve, deny, "
    "price, or guarantee credit or insurance; it does not execute contracts, match buyers, "
    "or place orders. Human review and locally validated policy are required before any "
    "financial or commercial action."
)


def _fingerprint(request: AssessmentRequest) -> str:
    canonical = json.dumps(
        request.model_dump(mode="json"), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def create_app() -> FastAPI:
    app = FastAPI(
        title="AgriScore Decision Support API",
        version=APP_VERSION,
        description="Evidence-driven crop-feasibility scoring with constrained LLM explanations.",
    )

    @app.get("/health", tags=["service"])
    async def health() -> dict[str, str]:
        policy = load_policy()
        return {
            "status": "ok",
            "version": APP_VERSION,
            "policy_id": policy.policy_id,
            "policy_hash": policy.policy_hash,
        }

    @app.get("/v1/policies/current", tags=["policy"])
    async def current_policy() -> JSONResponse:
        policy = load_policy()
        return JSONResponse(
            {
                "policy_id": policy.policy_id,
                "policy_hash": policy.policy_hash,
                "weights": dict(policy.weights),
                "minimum_evidence_quality_for_decision_support": policy.minimum_evidence_quality,
                "review_required_factor_floor": policy.review_required_factor_floor,
                "max_evidence_age_days": policy.max_evidence_age_days,
                "notice": "This is a crop-feasibility policy, not a credit or insurance policy.",
            }
        )

    @app.get("/v1/pilots/guyana", tags=["pilot"])
    async def guyana_pilot_scope() -> JSONResponse:
        scope = load_guyana_pilot_scope()
        return JSONResponse(
            {
                "pilot_id": scope.pilot_id,
                "country_code": scope.country_code,
                "status": scope.status,
                "financial_actions_permitted": False,
                "commercial_actions_permitted": False,
                "crops": [
                    {
                        "key": crop.key,
                        "display_name": crop.display_name,
                        "crop_profile_id": crop.profile_id,
                        "active_profile_version": crop.active_profile_version,
                        "profile_approval_status": crop.profile_approval_status,
                        "required_evidence_domains": list(crop.required_evidence_domains),
                        "required_additional_evidence": list(crop.required_additional_evidence),
                    }
                    for crop in scope.crops.values()
                ],
            }
        )

    @app.post(
        "/v1/assessments",
        response_model=AssessmentResponse,
        status_code=200,
        tags=["assessment"],
    )
    async def create_assessment(request: AssessmentRequest) -> AssessmentResponse:
        assessment = calculate_assessment(request)
        brain_result = await AssessmentBrain().narrate(request, assessment)
        assessed_at = datetime.now(timezone.utc)
        audit = AssessmentAudit(
            assessment_id=f"asm_{uuid4().hex}",
            assessed_at=assessed_at,
            request_fingerprint=_fingerprint(request),
            policy_id=assessment.policy_id,
            policy_hash=assessment.policy_hash,
            agent_provider=brain_result.provider,
            agent_model=brain_result.model,
            agent_mode=brain_result.narrative.generated_by,
        )
        return AssessmentResponse(
            assessment=assessment,
            narrative=brain_result.narrative,
            audit=audit,
            disclaimer=DISCLAIMER,
        )

    return app


app = create_app()
