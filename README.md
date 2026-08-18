# AgriScore Agentic Platform

AgriScore is an **evidence-driven crop-feasibility decision-support API**. It combines transparent agronomic, climate, and market component scores with a constrained LLM explanation layer.

> **Current scope:** This repository is a pilot foundation. It does **not** approve, deny, price, or guarantee credit or insurance. It does not execute purchases, contracts, buyer matching, or market transactions.

The supplied concept proposed an agentic ecosystem spanning farmer interaction, scoring, and enterprise operations. This baseline begins with the smallest defensible vertical slice: a reproducible assessment API with a strict separation between deterministic score calculation and LLM-generated explanation.

| Capability | Baseline behavior |
|---|---|
| Deterministic scoring | Uses a versioned 35% agronomic, 30% climate, 35% market policy with factor-level traces. |
| Evidence gate | Marks an assessment `REVIEW_REQUIRED` when evidence quality is inadequate or stale. |
| LLM assessment brain | Explains immutable results, risks, remediation priorities, and missing-data questions through a strict JSON schema. |
| Safe fallback | Returns a deterministic narrative whenever model configuration, a provider response, or schema validation fails. |
| Audit metadata | Returns a policy hash, request fingerprint, model/mode, and timestamp. It does not persist raw requests in v0.1. |
| External data | Defines climate, soil, and market provider contracts; no production data feed is silently assumed. |

## Architectural principles

The LLM is the **reasoning and communication layer**, not the decision engine. It receives a finalized evidence packet and is prevented by contract and prompt from changing scores, pricing credit, making lending decisions, quoting insurance, or executing commercial activity. The feasibility score remains a transparent function of versioned factors and weights.

| Layer | Responsibility |
|---|---|
| Evidence | Validate normalized input values and capture source, observed date, and quality. |
| Scoring | Produce component scores, composite feasibility score, score band, evidence gate, and factor trace. |
| Assessment brain | Generate a grounded, non-authoritative narrative in strict JSON or use a deterministic fallback. |
| Governance | Track policy hash, request fingerprint, LLM model/mode, and review status. |
| Integrations | Use provider-neutral contracts for future soil, climate, and market adapters. |

See [the implementation architecture](docs/architecture.md) for the target design, guardrails, roadmap, and evidence sources. See [the source-architecture review](docs/source-architecture-review.md) for the supplied specification distilled into implementation needs.

## Quick start

The baseline supports Python 3.11 or later.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.api.main:app --reload
```

Then browse the local OpenAPI UI at `http://127.0.0.1:8000/docs` or check service health:

```bash
curl http://127.0.0.1:8000/health
```

Run the automated tests with:

```bash
pytest
```

## Optional LLM configuration

The service is usable without an LLM. Without all three settings below, it automatically produces a deterministic explanation. To enable the LLM assessment brain, copy `.env.example` to `.env`, set values through your runtime environment or secret manager, and never commit the secret file.

| Variable | Purpose |
|---|---|
| `AGRI_LLM_API_KEY` | Credential for an OpenAI-compatible endpoint. |
| `AGRI_LLM_BASE_URL` | Endpoint root, excluding `/chat/completions`. |
| `AGRI_LLM_MODEL` | Model selector; the baseline default is `gpt-5`. |
| `AGRI_LLM_TIMEOUT_SECONDS` | Time budget before deterministic fallback, default 20 seconds. |

The adapter requests strict JSON output. A failed request, invalid payload, or unavailable endpoint must not change the deterministic score; it switches to fallback narration instead.

## Example assessment request

The input values are already normalized factor scores. A later integration layer will derive them from validated soil, climate, crop, and market data sources. This avoids treating raw third-party data as score-ready without data quality checks.

```bash
curl -X POST http://127.0.0.1:8000/v1/assessments \
  -H 'Content-Type: application/json' \
  -d @examples/assessment_request.json
```

A response includes:

| Field | Meaning |
|---|---|
| `assessment.feasibility_score` | Replayable 0–100 feasibility score. Not a credit score. |
| `assessment.band` | Feasibility band from the versioned pilot policy. |
| `assessment.status` | `DECISION_SUPPORT` only when pilot evidence gates pass; otherwise `REVIEW_REQUIRED`. |
| `assessment.components` | All factor inputs, weights, contributions, sources, observation dates, and quality flags. |
| `narrative` | LLM or deterministic explanation. It cannot modify `assessment`. |
| `audit` | Non-persistent trace metadata for policy/model/version review. |

## Data and governance boundaries

External data is treated as evidence, not fact. Each upstream adapter must attach provider provenance, retrieval timing, time coverage, quality notes, and normalized units before scoring. The architecture intentionally does not depend solely on SoilGrids because ISRIC reports its REST API is paused and lacks a production uptime guarantee.[1]

Before any lender uses an extension of this system for a credit-related decision, qualified local stakeholders must establish legal and policy requirements, permissible inputs, fair-lending/consumer-protection controls, validation against local outcome data, model monitoring, human review, and incident handling. Sound model-risk practice calls for validation, outcome analysis, ongoing monitoring, documentation, and effective challenge.[2] The baseline has no automated financial decision functionality.

## Repository layout

```text
app/
  agents/          constrained LLM assessment brain and fallback
  api/             FastAPI endpoints
  domain/          strict input/output contracts
  integrations/    provider-neutral climate, soil, and market contracts
  scoring/         transparent policy loading and calculation
config/            versioned pilot policy
docs/              architecture, source review, and research notes
tests/             scoring, API, and failure-mode validation
```

## Development sequence

| Stage | Purpose | Required evidence before progression |
|---|---|---|
| Baseline | Establish explainable assessment workflow and API | Unit/API tests, policy review, security review of secret handling |
| Data readiness | Curate regional crop profiles and supplier adapters | Agricultural expert sign-off, provenance standards, data-quality thresholds |
| Field pilot | Capture evidence and decisions with farmer/officer workflow | Consent/privacy design, pilot protocol, monitoring dashboard |
| Finance readiness | Consider separate financial-policy service | Local legal/compliance review, historical outcomes, independent validation, adverse-reason process |

## License and contribution note

This repository is initially marked **Proprietary** pending the project sponsor's licensing decision. Contributors should not add private farmer data, credentials, unverified crop thresholds, or real lending-policy terms to the repository.

## References

[1]: https://isric.org/explore/soilgrids "ISRIC SoilGrids status"
[2]: https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm "Federal Reserve model-risk guidance"
