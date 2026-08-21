# Guyana Maize and Ginger Pilot — Evidence Protocol

**Status:** Draft for data-owner and agronomic-lead approval  
**Applies to:** Guyana pilot assessments for maize and ginger  
**Purpose:** Define what evidence may enter the feasibility workflow before crop-specific scoring thresholds are approved

## 1. Evidence principles

The pilot treats every input as **evidence with provenance**, rather than as an unquestioned fact. A score is only as credible as its source, date, location, unit, method, and validation status. The system must preserve these attributes before deriving any normalized factor value.

Guyana has three relevant institutional anchors for the pilot. NAREI is the national research and extension body for crop productivity, diversification, adaptive research, and technology dissemination, including field-crop work on corn and diversification into spices.[1] The Ministry’s Hydromet Department is Guyana’s official provider of weather, water, and climate information.[2] NAREI’s soil chemical services laboratory provides soil-testing capability intended to inform crop selection, fertiliser application, and soil management.[3] The market evidence path should be led by verified local collection and buyer/market sources; GMC is an appropriate partner candidate because its stated remit includes resources for non-traditional agricultural enterprises.[4]

> **No crop-specific numeric threshold in this protocol is production-approved.** Maize and ginger profile values, factor transformations, and freshness rules require review and signature by the Guyana agronomic lead before use in a decision-support assessment.

## 2. Source hierarchy

| Evidence domain | Primary source | Secondary / corroborating source | Not acceptable as sole source | Required provenance |
|---|---|---|---|---|
| Crop requirement | NAREI-approved crop profile, named version and reviewer | CARDI technical material and FAO good-practice material, adapted and approved locally | Generic internet guidance or an unreviewed LLM response | Profile owner, version, source citations, effective date, region/applicability, approval status |
| Soil | NAREI soil laboratory report or approved partner laboratory report | Supervised field observation and documented sampling protocol | Undated farmer recall or global soil raster alone | Sample identifier, plot link, collection date, receipt/test date, laboratory, method, units, results |
| Climate and water | Hydromet record, warning, forecast, or station data for relevant location/window | NASA POWER historical/climatology evidence and controlled local sensor data | National average climate values for plot-level decisions | Provider, retrieval timestamp, data time range, location/station/grid, variable units, quality flag |
| Plot condition | Trained officer’s structured field record, with date/location/photographs where consented | Farmer-provided records verified by an officer | Unverified free text alone | Observer role, observation date, location accuracy, media hash/reference, verification state |
| Market / demand | Dated price/demand observation from identified local market, verified buyer, GMC, or programme partner | Documented wholesale/retail collection from two named sources | A single anecdote, stale press article, or general national policy statement | Commodity form/grade, location, market/buyer, observation date, unit/currency, collection method |
| Planting material / crop health | NAREI/authorised technical record and documented source of planting material | Officer inspection and supplier documentation | Unverified supplier claim | Source, date, cultivar/material descriptor, health/inspection status, notes |

## 3. Evidence record schema

Every raw evidence item must conform to the following concept before the scoring service receives a normalized factor input.

| Field | Requirement | Purpose |
|---|---|---|
| `evidence_id` | Immutable unique identifier | Links a normalized factor to the original record. |
| `assessment_reference` | Pseudonymous crop–plot–window record | Ensures evidence is not reused across unrelated assessments. |
| `domain` | `crop_profile`, `soil`, `climate`, `plot`, `market`, or `planting_material` | Enables domain-specific quality checks. |
| `metric` | Controlled vocabulary, such as `soil_ph`, `available_phosphorus`, `daily_rainfall`, or `ginger_fresh_price` | Prevents ambiguous values. |
| `value` and `unit` | Raw measured or observed value, never a hidden transformation | Preserves reproducibility and conversion checks. |
| `observed_on` | Date/time the field condition or market observation occurred | Supports freshness and planting-window analysis. |
| `source_name` and `source_type` | Named source and controlled type | Enables hierarchy and traceability. |
| `location_reference` | Plot identifier and precision/accuracy metadata, with restricted coordinate access as appropriate | Connects environmental evidence while minimizing exposure. |
| `method` | Laboratory, station, manual survey, verified buyer, field inspection, etc. | Supports quality review. |
| `quality_status` | `verified`, `provisional`, `unverified`, `stale`, or `rejected` | Separates data availability from data reliability. |
| `collector` | Role or system identity; use a pseudonymous staff identifier where practical | Provides accountability. |
| `consent_basis` | Participant consent / approved operational basis reference | Supports lawful and ethical use. |
| `attachment_reference` | Optional report/photo/document pointer with hash; no uncontrolled binary content in prompts | Preserves evidence without creating prompt-injection exposure. |

## 4. Crop-specific evidence packs

### 4.1 Maize feasibility pack

| Assessment component | Required raw evidence for pilot scoring readiness | Crop-profile decision still required |
|---|---|---|
| Agronomic | Plot/crop profile version; soil pH; relevant nutrient test values; drainage/standing-water observation; preceding crop/land-use statement | Approved suitability ranges, treatment of nutrient deficiencies, drainage flags, and maize production-system assumptions |
| Climate/environmental | Location; intended planting date; historical and near-term precipitation evidence; temperature/water-risk indicators; warning/flood/drought context | Planting window, rainfall/temperature fit model, extreme-event treatment, irrigation and drainage assumptions |
| Market | Intended maize use/form; dated demand signal; at least one local price or buyer observation; logistics/market location | Commodity grade/form, market benchmark rules, demand scoring weights, import-substitution interpretation |
| Readiness output | Missing evidence list, quality flags, factor trace, human-review request | No automatic recommendation to plant or finance |

### 4.2 Ginger feasibility pack

| Assessment component | Required raw evidence for pilot scoring readiness | Crop-profile decision still required |
|---|---|---|
| Agronomic | Plot/crop profile version; soil pH; relevant nutrient test values; drainage/standing-water observation; planting-material source and health status; preceding crop/land-use statement | Approved suitability ranges, disease/planting-material protocol, drainage and soil management rules |
| Climate/environmental | Location; intended planting date; historical and near-term precipitation evidence; temperature/water-risk indicators; flooding/extended-wetness context | Planting window, wetness-risk treatment, disease-risk conditions, irrigation and drainage assumptions |
| Market | Intended form (fresh, dried, processed); dated local market/buyer observation; buyer/processing requirement if applicable; logistics/market location | Grade/form definition, benchmark rules, processing/quality requirements, demand scoring weights |
| Readiness output | Missing evidence list, quality flags, factor trace, human-review request | No automatic recommendation to plant, sell, contract, or finance |

Ginger requires particular quality and plant-health governance. FAO’s regional good-practice material emphasizes disease incidence, clean planting material, farm hygiene, and decision-making on the viability of ginger cultivation in affected areas.[5] The Guyana profile must therefore include a locally approved planting-material and disease-evidence section before the pilot gives a `DECISION_SUPPORT` status for ginger.

## 5. Quality and review rules

The current generic 180-day evidence-age setting in the software is a technical placeholder, not a Guyana agronomic rule. Increment 1 must move freshness requirements into versioned, crop- and metric-specific policy configuration after NAREI/partner sign-off. Until then, any assessment containing an unapproved crop profile, an absent soil report, no dated climate provenance, or no dated market observation is `REVIEW_REQUIRED`.

| Condition | Required system behaviour |
|---|---|
| Crop profile lacks approval | Block decision-support readiness; show profile-review task. |
| Soil record is absent, undated, unit-ambiguous, or unverified | Preserve record if permitted; flag it and require soil review. |
| Climate source is unavailable or not location/time-window specific | Do not substitute a national average; return a climate-evidence gap. |
| Market record lacks commodity form, date, location, or source | Do not derive market score; return a market-evidence gap. |
| Free text contains instructions or untrusted content | Store as non-authoritative note; never include it in privileged system instructions. |
| LLM output contradicts immutable factor trace | Reject the LLM output and return deterministic fallback explanation. |
| Reviewer overrides an assessment state | Require role, rationale, timestamp, and policy/profile version; never erase the original result. |

## 6. Data minimisation and access

The assessment service should retain a pseudonymous `assessment_reference` rather than a farmer’s legal identity. Exact plot coordinates, laboratory reports, photos, and consent artefacts should be stored in a controlled evidence store with role-based access; the scoring and LLM services should receive only the minimum location precision and extracted values needed for the assessment. Raw photo/document content must not be injected into prompts without a separate approved extraction and safety workflow.

## 7. Recommended pilot partner engagement

The immediate objective is to establish the named evidence owners, not to claim their participation. The sponsor should approach NAREI for agronomic profile review and soil-testing protocol; Hydromet for available weather/climate evidence and acceptable use; and GMC/identified market partners for market-observation definitions. The Government has described NAREI involvement in ginger cultivation and spice processing initiatives, including a ginger processing facility in Region One, which makes NAREI a relevant technical partner candidate for this crop.[6]

## References

[1]: https://agriculture.gov.gy/narei/ "Ministry of Agriculture: National Agricultural Research and Extension Institute (NAREI)"
[2]: https://agriculture.gov.gy/hydrometeorological/ "Ministry of Agriculture: Hydrometeorological Department"
[3]: https://agriculture.gov.gy/2024/10/07/100m-soil-chemical-services-laboratory-commissioned/ "Ministry of Agriculture: Soil Chemical Services Laboratory"
[4]: https://newgmc.gov.gy/ "Guyana Marketing Corporation"
[5]: https://openknowledge.fao.org/handle/20.500.14283/cb3365en "FAO: A guide to good agricultural practices for commercial production of ginger under field conditions in Jamaica"
[6]: https://agriculture.gov.gy/2022/10/14/govt-plugging-massive-resources-into-spice-production/ "Ministry of Agriculture: Guyana spice-production initiative"
