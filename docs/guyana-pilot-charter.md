# AgriScore Guyana Pilot Charter

**Status:** Draft for stakeholder validation  
**Geography:** Cooperative Republic of Guyana  
**Pilot crops:** Maize and ginger  
**Product scope:** Pre-plant crop-feasibility decision support  
**Financial scope:** Explicitly excluded from the pilot

## 1. Pilot purpose

The Guyana pilot will test whether AgriScore can help a farmer, extension officer, or agricultural programme officer assemble evidence and understand the feasibility of planting **maize** or **ginger** on a specific plot. The system will generate an explainable assessment across agronomic suitability, climate/environmental exposure, and market evidence. It will identify evidence gaps and propose readiness actions for human review.

> **This pilot does not make or recommend lending, insurance, pricing, procurement, off-taker matching, input-ordering, or contractual decisions.** Its output is an explainable feasibility assessment and a review-ready evidence record.

The pilot is intentionally narrow. It is designed to establish trusted data contracts, validate the assessment workflow with local experts, and capture the evidence needed for later model calibration. It is not intended to prove creditworthiness, yield prediction, or profitability.

## 2. Proposed pilot boundary

| Dimension | Proposed boundary | Rationale |
|---|---|---|
| Country | Guyana | User-selected initial market and operating context. |
| Crop portfolio | Maize and ginger only | Provides two distinct crop-evidence pathways while keeping profile governance manageable. |
| Decision point | Pre-planting feasibility assessment | Enables intervention before inputs and planting decisions are committed. |
| Primary users | Participating farmers and trained agricultural/extension officers | Keeps the first workflow human-supported and interpretable. |
| Assessment unit | One crop–plot–planting-window combination | Prevents a score from being reused across different land, crops, or seasons. |
| Initial capacity | Up to 40 assessments, balanced where feasible across crops | Sufficient to test operational workflow and data completeness; not a statistically validated outcome model. |
| Geographic focus | Partner-selected locations within Guyana, documented at plot level | Avoids assuming that one ecological profile represents the entire country. |
| Duration | One documented planting cycle per crop, with subsequent outcome-capture plan | Aligns the pilot with observed agronomic and operational evidence rather than one-time scoring. |
| External action | Human review only | Prevents automated financial or commercial action before validation. |

## 3. Pilot questions

The pilot will answer the following practical questions.

| Question | Success signal | Evidence to collect |
|---|---|---|
| Can users complete a reliable assessment workflow? | A trained officer can create and submit a plot assessment without engineering intervention. | Completion rate, elapsed time, missing-field rate, support issues. |
| Can the system distinguish usable from insufficient evidence? | Low-quality, stale, or incomplete evidence is consistently marked `REVIEW_REQUIRED`. | Quality-gate events, source completeness, reviewer disposition. |
| Are score drivers intelligible and locally credible? | Agronomists can trace each component to known evidence and explain whether it is reasonable. | Structured expert review and disagreement reasons. |
| Do remediation actions improve assessment readiness? | Users can resolve flagged evidence gaps or document why they cannot. | Action completion, evidence refresh, follow-up review. |
| Is the LLM explanation safe and useful? | Narrative stays grounded in immutable factors and avoids financial/commercial claims. | LLM QA checklist, fallback rate, unsafe-output count. |
| Is there a viable evidence pipeline for each crop? | Climate, soil, crop-profile, and market inputs have named owners and provenance. | Data inventory, data-quality logs, provider/SOP approval. |

## 4. Minimum assessment record

A pilot assessment cannot be decision-support ready unless it records the following categories. The precise crop-specific measurements and thresholds will be defined only after research and local agronomic validation.

| Evidence domain | Minimum record | Current owner to designate |
|---|---|---|
| Farmer/plot | Pseudonymous farmer reference, plot reference, approximate location, area, planned planting date, crop | Pilot operations lead |
| Crop profile | Crop version, intended cultivar/production system where known, local agronomic reference | Agronomic lead |
| Soil | Test/sample date, laboratory or collection source, pH, relevant nutrients, drainage/field-condition evidence, units | Soil/laboratory partner |
| Climate | Location/time window, provider, retrieved date, precipitation and relevant risk indicators, quality flags | Data engineering lead |
| Market | Commodity definition, local demand/price/off-taker observation, date, location/market, collection method | Market/off-taker lead |
| Review | Assessment status, factor trace, reviewer identity/role, comments, final pilot disposition | Review lead |

## 5. Proposed pilot roles

| Role | Accountability | Independence boundary |
|---|---|---|
| Pilot sponsor | Approves scope, partners, resourcing, and go/no-go decisions | Does not unilaterally alter completed assessments. |
| Agronomic lead | Owns maize and ginger profile review, soil/field evidence interpretation, and remediation guidance | Reviews scoring assumptions independently from implementation. |
| Data engineering lead | Owns provider connectors, provenance, quality checks, caching, and failure states | Does not set agricultural thresholds without approval. |
| Field/extension lead | Trains users, coordinates evidence collection, and manages consent/participant operations | Does not suppress `REVIEW_REQUIRED` flags. |
| Reviewer | Reviews assessment evidence and explains exceptions or overrides | Cannot rewrite policy weights from the assessment screen. |
| Product/AI lead | Maintains prompts, fallback behaviour, policy versions, and evaluation logs | Cannot authorize financial/commercial activity. |

## 6. Explicit exclusions and safeguards

The following are **out of scope** for the Guyana pilot: credit approval or decline, loan sizing, APR calculation, insurance pricing, off-taker selection, contract execution, automated input ordering, autonomous notifications, and prescriptive pesticide/fertiliser instructions. These exclusions are enforced both in product design and in the LLM assessment prompt.

The pilot will collect only the minimum personal and plot information needed to assess a crop–plot–planting-window combination. Each record must be pseudonymised for engineering and model evaluation wherever practical. Assessment narratives must state uncertainty where evidence is incomplete, stale, or low quality.

## 7. Stage gates

| Gate | Decision | Required artefacts |
|---|---|---|
| G0 — Scope confirmation | Begin Increment 1 | Approved charter, named leads, selected partner locations, participant/consent approach. |
| G1 — Data readiness | Begin controlled workflow testing | Expert-reviewed crop-profile schema; data dictionary; climate/soil/market data protocol; quality thresholds. |
| G2 — Workflow readiness | Begin field pilot enrolment | Officer workflow, authenticated roles, review queue, test evidence records, support plan. |
| G3 — Pilot operation | Continue, adjust, or pause | Data-quality dashboard, safety review, reviewer feedback, incident log, change-control record. |
| G4 — Pilot readout | Consider the next product increment | Outcome data, expert validation, limitations report, calibration recommendations, sponsor decision. |

## 8. Immediate decisions needed from pilot stakeholders

The first implementation increment can begin with this country and crop scope. Before field enrolment, the sponsor should identify the pilot partner(s), candidate locations, agronomic lead, soil-testing route, extension/field operator, market-data owner, participant-consent process, and the planned planting windows. These operational choices will be recorded as controlled pilot configuration, rather than hard-coded assumptions in the scoring engine.
