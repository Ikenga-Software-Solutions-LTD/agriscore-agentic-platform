# Frontend MVP Brief — Guyana Officer-Led Pilot Portal

**Status:** Design and implementation brief; no frontend code has been built yet.  
**Primary release goal:** Enable trained officers and agronomists to operate the Guyana maize-and-ginger feasibility pilot safely using the existing backend foundation.

## 1. Product decision

The first interface should be an **authenticated web portal for officers and agronomists**, not a fully self-service farmer app. This reduces data-quality risk during the pilot and makes the evidence workflow easier to observe, support, and refine. Farmers participate through guided officer interactions and receive a plain-language report or discussion; farmer self-service, chat, voice, and multilingual interfaces are later releases.

## 2. Information architecture

| Area | Officer | Agronomist reviewer | Administrator |
|---|---|---|---|
| Home | My work, draft assessments, evidence tasks, review feedback | Review queue, pending profile issues, evidence requests | Pilot health, user roles, data-quality and incident summary |
| Assessments | Create/edit draft, submit, view report, follow up | Open submitted record, inspect trace, record disposition | View across cohort, no silent assessment editing |
| Farmers and plots | Create pseudonymous farmer/plot records and consent references | Read context necessary to review | Manage retention/access policy configuration only |
| Evidence | Record/upload controlled evidence; resolve gaps | Verify evidence and request clarification | Monitor completeness, source quality, and connector failures |
| Crop profiles | Read active version and known requirements | Review/approve version under a controlled workflow | See approval status and change history |
| Reports | Discuss/export farmer-friendly report | Export review-ready report | Export de-identified pilot readout |

## 3. P0 screen set

| Screen | Primary action | Essential elements | Current backend support | New backend capability required |
|---|---|---|---|---|
| Sign-in / role landing | Enter secure pilot workspace | User identity, assigned role, clear disclaimer | None | Authentication and role-based access control |
| Officer dashboard | See work requiring action | Drafts, submitted assessments, evidence gaps, review feedback, follow-ups | `GET /health`, pilot scope endpoint | Assessment list/query service and persistent records |
| Enrolment and consent | Start a crop–plot assessment | Pseudonymous reference, consent reference, plot basics, intended crop, planting window | Typed assessment input exists | Farmer/plot/consent persistence model |
| Crop evidence checklist | Collect guided evidence | Maize/ginger-specific sections, raw units, sources, dates, verification state | Guyana pilot scope names required domains | Raw evidence ledger and controlled vocabulary APIs |
| Assessment result | Understand result and next action | Feasibility score, component trace, review status, evidence gaps, safe narrative, disclaimer | `POST /v1/assessments` | Stored assessment retrieval and evidence-task links |
| Agronomist review queue | Review / request clarification | Priority/status, crop, time window, evidence quality, factor trace, source links | Score/review reasons available in response | Queue, reviewer disposition, immutable review record |
| Farmer report | Explain result in plain language | Summary, evidence status, actions, reviewer comments, no financial claims | Narrative object exists | Printable/report export endpoint |
| Admin pilot dashboard | Maintain safe operation | Profile status, completion rate, gap patterns, review turnaround, fallback/provider failures | Pilot scope endpoint | Aggregated pilot telemetry and role management |

## 4. Officer assessment flow

1. **Select or create farmer/plot.** The officer records only the minimum consented information and generates a pseudonymous assessment reference.
2. **Choose crop and planting window.** Only maize and ginger appear. The portal immediately shows the crop’s current approval state and evidence checklist.
3. **Collect evidence by section.** Soil, field/drainage, climate, market, and—only for ginger—planting-material records are captured in raw form with source/date/unit/method.
4. **Save draft and resolve gaps.** The officer can leave a draft but the dashboard shows missing or invalid items clearly.
5. **Generate assessment.** The backend calculates the transparent score and quality state. A pending crop profile or incomplete evidence leads to `REVIEW_REQUIRED`, not a green success state.
6. **Submit for agronomic review.** The officer cannot erase the assessment trace. They can add a note or attach new evidence by reference.
7. **Discuss report with farmer.** The officer uses a plain-language view to explain drivers, uncertainty, and next information/actions to consider.
8. **Record follow-up.** The officer logs evidence received, review response, planting decision, or later outcome observation according to consent.

## 5. Interface-state requirements

| State | Visual treatment | Required action |
|---|---|---|
| Draft | Neutral status; visible completeness meter | Officer may continue editing; no score shown as final |
| Evidence gap | Prominent amber indicator with exact missing/invalid item | Add, verify, or explain the evidence; cannot hide the gap |
| Review required | Amber review state; never visually equivalent to approval | Submit to reviewer or gather requested evidence |
| Agronomic discussion required | Distinct reviewer status with comment/action panel | Officer schedules/discusses next steps; no automatic recommendation |
| Pilot feasibility noted | Blue/neutral informational state, not green “approved” | Officer explains evidence-supported result and limitations |
| Profile pending | Prominent system-level banner for maize/ginger | Blocks decision-support readiness until approved profile exists |
| LLM fallback | Small transparency note indicating a deterministic explanation was used | No user action required; operations dashboard records event |
| Connector unavailable | Error state with retained draft and retry/manual-entry option | Officer can use approved manual evidence route or return later |

## 6. UX and safety requirements

The portal must use plain language, mobile-responsive layouts, low-bandwidth-friendly forms, autosave or explicit draft saving, and readable reports. It must not make the score appear more precise or authoritative than the evidence supports. It must never label a crop as “approved,” “creditworthy,” “insured,” “funded,” or “matched.”

Users need visible source/date/quality information beside every evidence-derived factor. A narrative explanation must be visually secondary to the deterministic factor trace, so an LLM summary cannot obscure the actual calculation. The interface must preserve the original assessment whenever evidence, policy, or a reviewer disposition changes.

## 7. Required backend additions before portal implementation

| Capability | Minimum API/domain addition | Why it is required |
|---|---|---|
| Identity and roles | User, organisation, role, and session model | Separates officer, reviewer, administrator, and technical access |
| Persistent assessment store | Assessment, farmer reference, plot, planting-window, and audit tables | Current assessment API is stateless and cannot support drafts or review history |
| Evidence ledger | Raw evidence item, attachment metadata, verification state, controlled metric vocabulary | Prevents hard-coding scores from untraceable form inputs |
| Crop profile registry | Draft/approved/retired profile state, version, owner, reviewer, effective date | Allows NAREI-informed profiles to become active safely |
| Review workflow | Assignment, disposition, rationale, evidence request, timestamp | Creates accountability and an operational review queue |
| Report service | Assessment read model and printable export | Supports officer/farmer discussion without raw-system complexity |
| Audit/observability store | Policy/profile/model/event tracking and pilot metrics | Supports data quality, safety review, and post-pilot evaluation |

## 8. Frontend build sequence

| Release slice | Scope | Demonstrable outcome |
|---|---|---|
| Portal foundation | Authentication, roles, shared layout, API client, audit-friendly navigation | Each user sees only permitted pilot areas |
| Officer workflow | Enrolment, plot/crop plan, raw evidence checklist, drafts | Officer can prepare a record without engineering assistance |
| Assessment/review workflow | Submit result, factor trace, review queue, disposition, report view | Agronomist can review and return a traceable response |
| Operations workflow | Data-quality dashboard, profile status, partner/source health | Pilot team can manage readiness and identify gaps |
| Field refinement | Follow-up capture, report export, accessibility/low-bandwidth improvements | Controlled cohort can complete an end-to-end planting-cycle workflow |

## 9. Design acceptance criteria

The portal design is ready for implementation when a prototype walkthrough demonstrates that an officer can find an assessment task, complete the maize or ginger checklist, understand why an item is incomplete, submit a result, send it to review, receive a decision/supporting comment, and explain a farmer-facing report without encountering financial or commercial calls to action. An agronomist must be able to view the precise evidence and factor trace that produced the result, while an administrator can determine whether unapproved profiles or weak evidence are preventing reliable operation.
