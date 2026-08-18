# AgriScore Baseline — Implementation Status and Handover

**Baseline release:** `0.1.0`  
**Local commit:** `a0e54a0`  
**Assessment scope:** Agricultural crop-feasibility decision support, not financial underwriting

## Delivered baseline

The repository implements a complete, runnable service slice from typed evidence input through deterministic scoring and an LLM-assisted narrative. It retains the original architecture's 35% agronomic, 30% climate, and 35% market composition, but makes the calculation inspectable, versioned, and separately testable.

| Area | Delivered capability | Deliberate boundary |
|---|---|---|
| API | FastAPI health, policy, and assessment endpoints | No authentication, persistence, or public deployment in v0.1. |
| Evidence | Strongly typed factors with source, observation date, quality, and staleness flags | Upstream raw data normalization remains a provider responsibility. |
| Scoring | Reproducible component and composite score, score band, and factor trace | Output is a feasibility score, **not a credit score**. |
| Review gate | `REVIEW_REQUIRED` for stale, low-quality, or inadequate evidence | A passing gate is not approval for a financial or commercial action. |
| LLM brain | Strict-JSON explanation, risk/positive drivers, remediation priorities, clarifying questions | The LLM cannot alter score, policy, or tier and cannot quote/promise financial terms. |
| Resilience | Deterministic explanation fallback when a model is absent, fails, times out, or returns invalid schema | The fallback is intentionally conservative rather than simulated intelligence. |
| Data integration | Provider-neutral climate, soil, and market contracts | No unaudited external data source is wired into a decision path. |
| Governance | Policy hash, request fingerprint, model/mode, timestamp, source trace, and immutable output separation | No persistent audit store yet; production retention/privacy policy remains to be designed. |

## Validation completed

The repository's offline regression suite confirms scoring weights, score bands, policy hashing, evidence gates, API response structure, and deterministic fallback. The optional live integration test also passed against a configured `gpt-5-mini` model using strict JSON output. It validated that an LLM narrative is returned under the expected schema without loan or APR fields.

| Validation | Result | Notes |
|---|---|---|
| Scoring unit tests | Passed | Validates component totals, 35/30/35 composition, quality gate, policy hash. |
| API tests | Passed | Validates health endpoint, full request/response workflow, fallback agent mode, financial disclaimer. |
| Live LLM contract test | Passed | Explicit opt-in; model response must satisfy the constrained narrative schema. |
| Full normal test suite | 6 passed, 1 skipped | The live model test is intentionally skipped unless explicitly enabled. |

## Critical constraints before a field or finance pilot

The system should be treated as a **technical prototype**, not as verified agronomic or financial decisioning. The factor values in the sample request are illustrative; they are not crop recommendations, regional thresholds, or production data. Before a field pilot, the project needs a regional crop-profile governance process, validated data suppliers, data-quality monitoring, consent/privacy design, farmer/officer workflow testing, and clear operating procedures for human review.

Before a lender or insurer uses any extension for action, the project requires a separate and approved financial-policy service, local jurisdictional legal/compliance analysis, feature-permissibility review, historical outcome data, model validation, fairness/impact testing, adverse-reason content, independent review, monitoring thresholds, override/appeal handling, and incident response. This aligns with general model-risk principles that emphasize documented purpose, validation, outcome analysis, monitoring, and effective challenge.[1] Generative AI controls should also be designed around trustworthy-AI risk management across the full lifecycle.[2]

## Recommended next development increment

The most valuable next increment is a **data-readiness pilot**, not an immediate dashboard or lending implementation. The team should define a small set of region/crop pairs, recruit subject-matter owners, create a governed crop-profile schema, and build read-only adapters that return provenance-rich climate, soil, and market evidence. NASA POWER is a viable candidate for climate data because it exposes analysis-ready data through REST services, but the adapter must implement timeout, rate-limit, cache, and quality controls.[3] SoilGrids should not be a single production dependency because its official status page notes that the REST API is paused and does not guarantee uptime.[4]

| First data-readiness deliverable | Owner category | Acceptance criterion |
|---|---|---|
| Crop-profile specification | Agronomist / extension partner | Crop requirements, ranges, source references, review date, and regional applicability are explicitly documented. |
| Soil evidence protocol | Soil-lab / agronomy owner | Units, sample method, sample age, location precision, and quality rules are defined. |
| Climate provider adapter | Data engineering owner | Provenance, cache/timeout/retry behavior, failure status, and independent sanity checks are tested. |
| Market evidence protocol | Market/off-taker owner | Commodity specification, market location, observation method, price/volume freshness, and data rights are documented. |
| Review workflow | Product / risk owner | Review triggers, responsible role, approvals, escalation, and record-retention rules are documented. |

## Deployment alternatives

The codebase is API-first and can be deployed without changing domain logic. The two viable initial operating models should be selected based on how frequently data refreshes and whether a stakeholder UI is needed.

| Approach | Tradeoffs | Cost | Setup complexity |
|---|---|---|---|
| Managed API with a simple reviewer portal and scheduled data refreshes | Best for early pilots; provides user management and configuration space; constrained runtime for specialized geospatial/ML tooling | Low to start; operational cost depends on managed services and usage | Moderate |
| Containerized API with a dedicated worker/data pipeline | Supports custom geospatial libraries, larger processing jobs, and a separate queue; carries more operating and security responsibility | Higher infrastructure and operational overhead | High |

The repository does not force either route. The first approach is usually sufficient for an evidence-collection pilot; the second is appropriate only if real satellite/raster processing or larger data workloads create a documented runtime constraint.

## References

[1]: https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm "Federal Reserve: Supervisory Guidance on Model Risk Management"
[2]: https://www.nist.gov/itl/ai-risk-management-framework "NIST AI Risk Management Framework"
[3]: https://power.larc.nasa.gov/docs/services/api/ "NASA POWER API Documentation"
[4]: https://isric.org/explore/soilgrids "ISRIC SoilGrids service status"
