# THE JOURNEY

> **A living record of the AgriScore project**  
> **Author:** Chinedu Jamike, Libertas Alpha Technologies  
> **Project:** AgriScore Agentic Platform  
> **Last updated:** 22 August 2026  
> **Status:** Foundation built; Guyana maize-and-ginger pilot definition in progress

## Why this document exists

This is the story of how AgriScore is being built: what we are trying to achieve, the choices we have made, the work completed, the lessons learned, and the milestones still ahead. It is intended to be read by the people building, supporting, governing, funding, and eventually using the platform.

AgriScore is being created to help farmers and agricultural professionals make better-informed decisions before planting. It will bring together evidence about a crop, a plot, soil, climate, water risk, and the market, then explain the strengths, uncertainties, and next questions in clear language. The initial pilot is deliberately focused on **Guyana**, **maize**, and **ginger**.

The ambition is substantial, but the approach is disciplined. We are not building a machine that promises harvests or makes automatic financial decisions. We are building a trusted evidence and decision-support service: one that helps people see what is known, what is uncertain, and what should be checked before significant farming decisions are made.

## Our guiding principles

| Principle | What it means in practice |
|---|---|
| **Evidence before confidence** | A favourable score cannot hide missing, stale, low-quality, or unverified evidence. |
| **Local expertise first** | Guyana-specific crop profiles and thresholds must be approved by qualified local agricultural experts. |
| **People remain accountable** | Officers and agronomists review evidence and decisions; the software supports their work rather than replacing it. |
| **Explainability is essential** | Every assessment must show the factors, sources, dates, quality state, and reasons behind its result. |
| **Safety is designed in** | The platform does not approve credit, quote insurance, set prices, execute contracts, place orders, or make payments. |
| **Start narrow; learn properly** | We begin with two crops in one country and expand only after controlled evidence and field learning. |

## The story so far

The project began with a practical question: how can farmers, agricultural officers, and eventually responsible partners make better decisions before planting, without relying on disconnected records, informal assumptions, or opaque technology?

The first work was to turn that question into a technical foundation. A proposed architecture was reviewed and refined into an evidence-driven design. The system was intentionally separated into two parts. First, a **deterministic scoring engine** calculates transparent agronomic, climate, and market components from structured evidence. Second, a constrained **AI explanation layer** translates the result into plain language, priorities, and follow-up questions. The AI cannot change the score or make a financial decision.

The next decision was to avoid building for every crop and every country at once. Guyana was selected as the first pilot country, with maize and ginger as the first two crops. This created a real operating context: local agricultural knowledge, soil testing, weather/climate evidence, market records, extension support, and agronomic review now matter more than generic software features.

The work then shifted from a technical engine to a usable pilot concept. A detailed pilot charter, evidence protocol, control configuration, implementation backlog, user journey, and visual process map were created. This gives the project a clear route from today’s backend foundation to an officer-led field pilot and, after validation, a market-ready product.

## Progress timeline

| Date | Milestone | What changed | Evidence / reference |
|---|---|---|---|
| **18 August 2026** | Evidence-driven feasibility baseline established | The first runnable backend was committed. It introduced the Python/FastAPI service, typed assessment contracts, transparent feasibility engine, versioned policy, LLM explanation layer with deterministic fallback, provider-neutral integration contracts, fixtures, tests, and technical documentation. | [Commit `a0e54a0`](https://github.com/Ikenga-Software-Solutions-LTD/agriscore-agentic-platform/commit/a0e54a043f495093fe90cebe8c14c2ce241e6b6e) |
| **18 August 2026** | Baseline handover documented | The implementation status, validation status, technical limitations, safeguards, and recommended next engineering decisions were recorded. | [Commit `876ba0b`](https://github.com/Ikenga-Software-Solutions-LTD/agriscore-agentic-platform/commit/876ba0b55f880bfbc898523c0df56025f3e276b6) |
| **21 August 2026** | Guyana pilot scope defined | Guyana was configured as the controlled pilot country, with maize and ginger as the only pilot crops. Both crops were made `PENDING_AGRONOMIC_REVIEW`, preventing them from appearing decision-ready until local crop profiles are approved. The pilot charter, evidence protocol, data-source hierarchy, and Increment 1 backlog were added. | [Commit `2a9cd18`](https://github.com/Ikenga-Software-Solutions-LTD/agriscore-agentic-platform/commit/2a9cd18dc661db54545b2513d15e7ebed5b8e0b4) |
| **22 August 2026** | User journey and frontend blueprint completed | The full officer-led journey was documented for the farmer, field officer, agronomist/NAREI reviewer, administrator, and technical operator. A visual journey map and a first frontend MVP brief were added to clarify what must be built next. | [Commit `9f35038`](https://github.com/Ikenga-Software-Solutions-LTD/agriscore-agentic-platform/commit/9f350380d1d4f6e7c3d13efe6c40b88ffd827002) |
| **22 August 2026** | Living project narrative established | This document was created as the central, author-attributed record of the project journey and the rule for documenting material progress was established. | This entry will be linked to the commit that introduces this document. |

## What has been built

The project is no longer only an idea or a presentation. It has a real, tested backend foundation.

| Capability | Current position |
|---|---|
| Feasibility scoring | Built. Agronomic, climate, and market inputs are assessed using transparent weighted components. |
| Evidence quality controls | Built. Source, date, quality, and staleness are carried into the assessment and can trigger `REVIEW_REQUIRED`. |
| AI explanation | Built and validated. The AI explains the deterministic result but cannot change it. A non-AI fallback is available. |
| Audit information | Built. Policy version, policy hash, request fingerprint, factor trace, timestamp, and model mode are retained in the response. |
| Guyana pilot guard | Built. The system recognises Guyana, maize, and ginger and requires local crop-profile approval before decision-support readiness. |
| Data integrations | Designed, not connected. Contracts exist for climate, soil, and market evidence providers. |
| Frontend portal | Designed, not built. The first interface will be for officers and agronomists, not a self-service farmer app. |
| Real field data | Not yet connected. The next stage is governed data collection with local partners. |
| Financial services | Not built and intentionally excluded from the pilot. |

## Where we are now

We are at the transition from **technical foundation** to **controlled pilot readiness**.

The important next task is not to add more artificial intelligence. It is to work with the right Guyana partners to make the system locally credible. We need named agronomic reviewers, selected pilot locations, a soil-testing route, an approved climate-data arrangement, clear market-observation definitions, and a consent/data-sharing process before real farmer or plot records are introduced.

Once these foundations are agreed, the next engineering work will build the officer portal, crop-profile registry, raw evidence ledger, review workflow, and secure storage needed to operate a small pilot safely.

## The road to a market-ready solution

| Stage | Purpose | Evidence of readiness |
|---|---|---|
| **Controlled design** | Define the Guyana pilot, users, crops, rules, roles, and evidence requirements | Approved pilot charter, operating roles, evidence protocol, and crop-profile ownership |
| **Officer-led MVP** | Allow trained officers to create, assess, review, and report on pilot cases | Working portal, secure roles, evidence ledger, review queue, and traceable reports |
| **Field validation** | Compare assessments with expert judgment and observed field outcomes | Expert evaluation, data-quality results, outcome records, and documented limitations |
| **Calibration and refinement** | Improve profiles, workflow, explanations, and support from real pilot learning | Versioned changes approved through governance and tested before release |
| **Controlled market launch** | Expand to more users and partners only when the system is proven useful, safe, and operable | Stable operations, partner agreements, support process, security controls, and measurable pilot value |

A market-ready AgriScore solution will not be defined merely by attractive screens or a large AI model. It will be defined by trust: reliable local evidence, clear explanations, competent human review, useful field outcomes, and responsible governance.

## Next chapter

The next chapter begins with collaboration. NAREI and other relevant Guyana partners will be approached to help validate agronomic crop profiles, soil and plant-health evidence, field workflow, and evaluation methods. At the same time, the project will translate the user journey into the first officer-facing portal and governed evidence-management workflow.

The work ahead is to prove that the platform is useful in the real decisions farmers and officers face before planting. If it earns that trust with maize and ginger in Guyana, the platform will have a credible foundation for carefully expanding to other crops, locations, and partner services.

## Living-record convention

This file is a controlled living record. It will be updated whenever the project achieves a **material milestone**, including a completed feature, a verified test/deployment, an approved policy or crop profile, a confirmed partner or pilot operating decision, a validated data connection, a user-research outcome, a pilot finding, or a formal go/no-go decision.

Each new entry must state the date, what changed, why it matters, its status, and a reference to the relevant commit, document, or approved record. Minor formatting changes and routine maintenance do not require a narrative entry. Historical dates will not be invented: where a date cannot be verified, the entry will state that it is unconfirmed.

| Entry template | Required content |
|---|---|
| **Date** | Calendar date in `DD Month YYYY` format |
| **Milestone** | Short, specific title |
| **What changed** | Plain-language account of completed work or decision |
| **Why it matters** | Effect on pilot readiness, safety, usability, evidence quality, or market path |
| **Status** | Completed, validated, approved, blocked, deferred, or superseded |
| **Reference** | Git commit, document path, partner record, or decision log |

---

*This document is authored by Chinedu Jamike of Libertas Alpha Technologies and maintained as the living project record for AgriScore.*
