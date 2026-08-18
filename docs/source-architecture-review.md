# AgriScore Architecture Notes

Source: `/home/ubuntu/upload/AgriScoreSystemArchitecture&TechnicalSpecificationV2.pdf`

## Core purpose

AgriScore is described as an autonomous multi-agent AI ecosystem that computes a dynamic crop viability score from 0 to 100 for smallholder farmers. The stated objective is to bridge producers, input suppliers, micro-lenders, and corporate off-takers.

## Proposed 3-layer architecture

### Layer 1: Autonomous Multi-Agent Reasoning Engine

The document proposes a reasoning layer that ingests weather, satellite/IoT, web-scraped market data, and database records.

The named agents are:

| Agent | Role |
|---|---|
| A_P Production & Agronomic Agent | Evaluates soil pH, NPK deficits, sub-soil drainage, and local micro-climate weather risks |
| A_E Economic & Market Agent | Computes buyer deficits, wholesale price trends, and CARICOM import priority metrics |
| A_S Scoring & Supervisory Orchestrator | Combines outputs into a composite score using 35/30/35 weighting |

### Layer 2: Interactive Chatbot Gateway

This layer is positioned as the farmer-facing conversational interface. The document lists these capabilities:

| Capability | Description |
|---|---|
| Order for input | One-step ordering of fertilizer, lime, and seeds |
| Post-production images | Farmer uploads of farm and crop-health photos |
| Recall conversation context | Long-term memory of past interactions, land acreage, and crop cycles |
| Notifications | Production alerts and market-price alerts |
| Consultation scheduling | Automated booking with agricultural experts |

### Layer 3: Enterprise Web Portal & System Dashboard

The management layer includes farmer registration, crop selection, admin dashboard, company dashboard, and agent tracking/evaluation.

## Scoring methodology in the document

The composite score uses three weighted dimensions:

| Component | Weight | Example inputs |
|---|---:|---|
| Agronomic suitability | 35% | Soil pH, NPK deficits, drainage index, crop compatibility |
| Climate & environmental risk | 30% | Rain forecast, drought index, storm risk, maturation timing |
| Market & economic demand | 35% | Wholesale price trends, import substitution priority, off-taker demand |

## Financial risk tiering proposed in the document

| Score range | Tier | Lending / insurance / off-taker implication |
|---|---|---|
| 85-100 | Tier 1 Prime AAA | Up to 5,000 USD at 4.2% APR, 1.8% insurance, automatic B2B matching |
| 72-84 | Tier 2 Preferred AA | Up to 3,000 USD at 5.8% APR, 2.5% insurance, priority listing |
| 60-71 | Tier 3 Standard A | Up to 1,500 USD at 7.5% APR, 3.5% insurance, manual buyer request match |
| <60 | Tier 4 High Risk | Ineligible, remediation required |

## Proposed codebase blueprint in the document

```text
agriscore-system/
├── agents/
│   ├── production_agent.py
│   ├── economic_agent.py
│   └── scoring_orchestrator.py
├── services/
│   ├── chatbot_gateway.py
│   └── notification_engine.py
├── frontend/
│   ├── portal/
│   └── static/
├── data/
│   ├── crop_guidelines.json
│   └── market_demand.json
├── server.py
└── README.md
```

## Explicit next steps listed in the document

1. Refine production and economic agents with real API integrations for telemetry and market feeds.
2. Add persistent chatbot context storage using a vector database such as ChromaDB or Pinecone.
3. Connect Layer 3 tracking and evaluation modules to Layer 1 telemetry for observability.

## Initial implementation observations

The document provides a useful high-level concept, but the current architecture is still product-centric rather than production-grade. It does not yet specify:

| Missing area | Why it matters |
|---|---|
| Model selection and prompting strategy | Needed for the LLM-driven reasoning brain the user requested |
| Deterministic scoring vs. LLM judgment boundary | Needed for auditability, credit governance, and reproducibility |
| Data contracts and schemas | Needed for integration stability across agents |
| Evidence traces and explanation outputs | Needed for lender trust and farmer transparency |
| Risk controls and human review gates | Needed to avoid unsafe automated financial decisions |
| Evaluation framework | Needed to measure agronomic accuracy and credit-worthiness performance |
| Deployment target and service boundaries | Needed before selecting project scaffolding |

These observations should drive the refined architecture and the first implementation slice.
