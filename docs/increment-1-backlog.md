# Increment 1 Backlog — Guyana Maize and Ginger Data Readiness

**Increment objective:** Make the AgriScore feasibility workflow ready for controlled evidence collection in Guyana for **maize** and **ginger**. The increment ends with reviewable pilot records and a validated evidence pipeline; it does not launch lending or commercial automation.

## 1. Definition of done

Increment 1 is complete only when a trained pilot officer can create a de-identified maize or ginger assessment record, attach provenance-rich soil, climate, and market evidence, receive a `REVIEW_REQUIRED` result when the crop profile/evidence is not approved, and route the record to an agronomic reviewer. The system must never transform a missing or unapproved profile into an apparently decision-ready score.

| Completion area | Acceptance measure |
|---|---|
| Pilot control | API exposes the Guyana scope; only maize and ginger are supported; both remain profile-gated until formally approved. |
| Crop-profile governance | Each crop has a documented owner, source list, approval state, version, effective date, applicability note, and change-log process. |
| Evidence capture | Every raw item records source, observed date, unit, location reference, method, quality status, collector, and consent basis. |
| Data quality | Missing, stale, ambiguous, unverified, or unapproved evidence produces visible review reasons. |
| Climate pathway | A controlled climate adapter can retrieve and store provenance for a test location/window, with a safe failure state. |
| Soil pathway | Officers can record/import a laboratory or supervised field soil evidence record without exposing the raw report to the LLM. |
| Market pathway | Officers can record a dated, unit-defined local market/buyer observation for the relevant crop form. |
| Review workflow | An agronomic reviewer can inspect factor trace and evidence gaps, then record a non-destructive review disposition. |
| Safety | No lender terms, credit decision, insurance quote, buyer match, order, or contract action is represented in the user interface or API. |

## 2. Sequenced work packages

| ID | Priority | Work package | Key deliverables | Acceptance criteria | Primary owner |
|---|---:|---|---|---|---|
| I1-01 | P0 | Pilot governance setup | Partner map, named pilot roles, consent/data-sharing register, location-selection criteria, issue/escalation path | Sponsor names each accountable role and approves G0 package | Pilot sponsor |
| I1-02 | P0 | Crop-profile schema and approvals | `CropProfile` schema; maize and ginger profile templates; approval/version workflow | Templates cannot become active without agronomic approval metadata | Product + agronomic lead |
| I1-03 | P0 | Raw evidence ledger | Typed evidence record, controlled vocabularies, provenance fields, attachments-by-reference design | A raw record can be validated without relying on free text | Data engineering |
| I1-04 | P0 | Guyana pilot gate | Country/crop scope configuration and policy guard | High numerical maize/ginger result remains `REVIEW_REQUIRED` when profiles are pending | Backend engineering |
| I1-05 | P0 | Soil evidence intake | Laboratory/manual evidence input and validation; report metadata capture | Undated/ambiguous soil evidence is visibly rejected or routed to review | Field + data engineering |
| I1-06 | P0 | Climate evidence adapter | Hydromet engagement protocol; historical/climate fallback adapter; caching/timeouts/provenance | Test retrieval has source/time/location provenance and safe unavailable state | Data engineering |
| I1-07 | P0 | Market evidence protocol and intake | Crop-form taxonomy; local market/buyer observation form; source verification rules | Market score cannot derive from a record without date, unit, location, source, and crop form | Market lead + engineering |
| I1-08 | P1 | Officer review experience | Authentication, role distinction, assessment creation form, evidence-gap view, reviewer disposition | A trained user completes a supervised test assessment without developer support | Product + frontend/backend |
| I1-09 | P1 | Assessment report and exports | Human-readable score/evidence report with policy/profile/version and disclaimer | Reviewer can export a non-financial feasibility report with traceability | Product + engineering |
| I1-10 | P1 | LLM quality evaluation | Expert-labelled explanation test set, groundedness/safety rubric, fallback monitoring | No material contradiction or prohibited financial/commercial language in test set | Product/AI + agronomic lead |
| I1-11 | P1 | Operational observability | Audit persistence design, data-quality metrics, error/fallback metrics, change log | Pilot team can detect evidence gaps, provider failures, and policy/profile changes | Engineering + operations |
| I1-12 | P2 | Pilot dry run | Synthetic workflow rehearsal using explicitly illustrative evidence; staff training; incident exercise | G2 review confirms workflow, roles, and escalation process are workable | All pilot leads |

## 3. First engineering sprint

The first engineering sprint should deliver the structural controls that prevent unsafe acceleration. It should not start with a chatbot, dashboard polish, or external lender integration.

| Sprint item | Repository target | Outcome |
|---|---|---|
| Guyana pilot scope | `config/guyana_pilot_scope.json`, `app/scoring/pilot_scope.py` | Enforces country/crop boundary and profile-review gate. |
| Pilot endpoint | `GET /v1/pilots/guyana` | Exposes pilot crops, approval states, evidence domains, and non-financial restriction. |
| Crop-profile schema | `app/domain/crop_profiles.py` and `config/crop_profiles/` | Establishes versioned but initially inactive maize/ginger profile templates. |
| Evidence ledger schema | `app/domain/evidence.py` | Captures raw provenance before normalized scoring values exist. |
| Review reasons | `app/scoring/engine.py` | Keeps numeric score separate from readiness and adds profile/evidence reasons. |
| Regression tests | `tests/` | Proves no unapproved Guyana pilot crop reaches decision-support status. |

## 4. External dependencies and decision log

| Dependency | Required decision | Blocker level | Mitigation while pending |
|---|---|---:|---|
| Agronomic lead / NAREI engagement | Who approves crop profiles and profile changes? | High | Keep profiles inactive and assessments `REVIEW_REQUIRED`. |
| Partner locations | Which Guyana regions/plot types and planting windows are in the pilot? | High | Do not encode nationwide thresholds; use location-neutral schema. |
| Soil service | Which lab/field protocol and report format will be used? | High | Support manual evidence ledger with clear unverified status. |
| Hydromet access | Which products/stations/forecast/history may be used and under what conditions? | Medium | Use a provenance-rich fallback climate adapter only for controlled development. |
| Market partner | Which markets/buyers will provide dated demand and price observations? | High | Accept only manual verified observations; do not infer market demand. |
| Participant consent | What consent/data-sharing and retention wording is approved? | High | Do not enrol farmers or persist personal data. |
| Hosting/security | Which pilot environment and identity provider is approved? | Medium | Continue local/test environment and do not collect sensitive production data. |

## 5. Out of scope for Increment 1

Increment 1 excludes credit scoring, loan eligibility, APR or insurance rates, underwriting explanations, commercial buyer matching, purchasing, contracts, payments, push notifications, continuous monitoring, and autonomous actions. It also excludes a claim that any crop-specific threshold has been validated for all of Guyana.

## 6. Go/no-go criteria for a controlled field-pilot build

A field-pilot build should not begin until the sponsor can demonstrate that each crop has an approved profile owner and version; data source/quality requirements are defined; a soil/lab pathway is operational; market observations have a named owner; user consent and roles are approved; the `REVIEW_REQUIRED` process has a human owner; and the test suite covers key unsafe and unavailable-data paths.
