"""Pilot-specific controls that sit alongside the generic scoring policy.

The generic policy evaluates normalized factors. A pilot-scope control prevents a
numerically high result from being treated as decision-support ready when the local
crop profile or evidence protocol has not been approved.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from app.domain.models import AssessmentRequest


PILOT_SCOPE_PATH = Path(__file__).resolve().parents[2] / "config" / "guyana_pilot_scope.json"


@dataclass(frozen=True)
class PilotCropControl:
    key: str
    display_name: str
    profile_id: str
    active_profile_version: str | None
    profile_approval_status: str
    required_evidence_domains: tuple[str, ...]
    required_additional_evidence: tuple[str, ...]


@dataclass(frozen=True)
class PilotScope:
    pilot_id: str
    country_code: str
    status: str
    crops: dict[str, PilotCropControl]
    unapproved_profile_forces_review: bool


def _crop_key(crop: str) -> str:
    return " ".join(crop.lower().replace("-", " ").split())


def load_guyana_pilot_scope(path: Path = PILOT_SCOPE_PATH) -> PilotScope:
    document = json.loads(path.read_text())
    crops = {
        key: PilotCropControl(
            key=key,
            display_name=value["display_name"],
            profile_id=value["crop_profile_id"],
            active_profile_version=value["active_profile_version"],
            profile_approval_status=value["profile_approval_status"],
            required_evidence_domains=tuple(value["required_evidence_domains"]),
            required_additional_evidence=tuple(value["required_additional_evidence"]),
        )
        for key, value in document["crops"].items()
    }
    return PilotScope(
        pilot_id=document["pilot_id"],
        country_code=document["country_code"],
        status=document["status"],
        crops=crops,
        unapproved_profile_forces_review=document["controls"]["unapproved_profile_forces_review"],
    )


def pilot_review_reasons(request: AssessmentRequest, scope: PilotScope | None = None) -> list[str]:
    """Return non-financial review controls applicable to this pilot request.

    The check is intentionally narrow: it applies only to Guyana and exact pilot-crop
    names. A generic API request remains governed only by the generic policy.
    """

    active_scope = scope or load_guyana_pilot_scope()
    if request.country_code != active_scope.country_code:
        return []

    crop = active_scope.crops.get(_crop_key(request.crop))
    if crop is None:
        return [
            f"Crop '{request.crop}' is outside the controlled Guyana pilot scope; human review is required."
        ]

    reasons: list[str] = []
    if active_scope.unapproved_profile_forces_review and crop.profile_approval_status != "APPROVED":
        reasons.append(
            f"{crop.display_name} crop profile '{crop.profile_id}' has status "
            f"{crop.profile_approval_status}; local agronomic approval is required."
        )
    return reasons
