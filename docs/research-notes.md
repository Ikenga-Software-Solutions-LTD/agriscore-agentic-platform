# AgriScore Research and Design Evidence

## Verified language-model availability

The live sandbox LLM catalog retrieved on 2026-08-18 contains these model families: GPT-5 (`gpt-5-nano`, `gpt-5-mini`, `gpt-5`, `gpt-5.5`), Claude (`claude-haiku-4-5`, `claude-sonnet-4-6`, `claude-opus-4-6`, `claude-opus-4-7`), and Gemini (`gemini-3-flash-preview`, `gemini-3.1-pro-preview`). Each advertises a thinking parameter in the live catalog. The project should use an OpenAI-compatible provider abstraction and choose a model by environment variable; no API key should be committed.

## Data-source findings

| Source | Verified capability or limitation | Architectural decision |
|---|---|---|
| NASA POWER APIs | The official API documentation states that the REST APIs support analysis-ready data distribution and return user-specific data products. It also documents normal 200 success, 422 validation, and 429 rate-limit responses. | Implement a resilient read-only climate connector with timeout, retry/backoff, caching, and provenance capture. Do not treat it as the only weather/forecast source. |
| ISRIC SoilGrids | The ISRIC page currently states that its REST API is paused, beta, has no uptime guarantee, and is not appropriate as the sole production dependency. | Do not bind the application directly to the SoilGrids API. Store soil observations through a provider-neutral contract; allow later ingest of bulk/raster datasets or a reliable partner provider. Prefer laboratory soil-test evidence where available. |
| FAOSTAT | Search results identify FAOSTAT as FAO's agricultural and food-related data resource with a developer/API portal. The direct web extraction target was stale. | Treat FAOSTAT as an optional historical benchmark source. Implement the local-market data contract and fixtures first; use validated local off-taker/wholesale data for operational market scores. |

## Governance findings

| Source | Relevant finding | Architectural control |
|---|---|---|
| NIST AI RMF | NIST describes the AI RMF as voluntary guidance to incorporate trustworthiness into the design, development, use, and evaluation of AI systems, and provides a GenAI profile for generative-AI-specific risks. | Implement traceability, reliability checks, documented limitations, model/prompt versioning, access control hooks, and evaluation artifacts. |
| Federal Reserve model-risk guidance | The guidance describes model risk as the potential for adverse financial consequences from decisions based on model output. It stresses validation, outcome analysis, ongoing monitoring, clear limits, documentation, and effective challenge. The current page says agentic and generative AI are not directly in scope but governance principles should inform their controls. | Keep deterministic scoring separate from LLM narrative reasoning; require policy-configured thresholds, score reliability checks, and a human review queue before any credit decision. Preserve reproducible inputs and decision traces. |
| CFPB AI credit guidance | The CFPB says lenders must provide specific and accurate reasons for adverse actions, even when using complex or AI models. | The baseline must produce structured factor-level explanations and not output an opaque approval/denial. Jurisdiction-specific compliance remains a lender responsibility. |

## Selected development position

The first usable vertical slice should be a backend decision-support API, not a complete lender or marketplace platform. It should:

1. Ingest a typed farm-and-crop assessment request.
2. Calculate agronomic, climate, and market components deterministically from transparent rules and versioned profiles.
3. Assess evidence completeness and confidence; incomplete inputs must route to review rather than be artificially scored as creditworthy.
4. Ask a tool-using LLM to synthesize an explanation, remediation actions, and questions; it must receive the deterministic component outputs and cannot alter the composite score or tier.
5. Return a provenance-rich assessment containing a score, risk tier, readiness/review state, component evidence, and LLM explanation.
6. Keep credit amount, APR, insurance rate, approval/denial, and external ordering/matching outside the automated baseline until the lender has supplied approved policy, outcome data, jurisdictional review, and a validation plan.

## Source URLs

1. https://power.larc.nasa.gov/docs/services/api/
2. https://isric.org/explore/soilgrids
3. https://www.nist.gov/itl/ai-risk-management-framework
4. https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm
5. https://www.consumerfinance.gov/archive/newsroom/cfpb-issues-guidance-on-credit-denials-by-lenders-using-artificial-intelligence/
6. https://www.fao.org/faostat/en/
