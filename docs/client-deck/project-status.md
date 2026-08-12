# Client Deck — Overall Project Status

Use as one status slide (or two slides: stack vs product). Snapshot date: **2026-08-12**.

---

## Slide title

**Overall Project Status**

Subtitle: *Geth-powered crypto intelligence platform — Stage 9 in progress*

---

## Status legend

| Mark | Meaning |
|---|---|
| ✅ | Complete / operational |
| 🟢 | Active now |
| 🔄 | In progress |
| 🟡 | Available / planned next layer |
| ⏸️ | Paused |
| ⏳ | Not started |

---

## Slide body (copy into PowerPoint / Google Slides)

### INFRASTRUCTURE

| Component | Status | Notes |
|---|---|---|
| **Lighthouse** | ✅ | Consensus client healthy |
| **Geth** | 🔄 | Archive sync / backfill |
| **Custom Indexers** | ⏸️ | Paused pending sync depth |
| **PostgreSQL** | ✅ | Ops / entity store |
| **Neo4j** | ✅ | Relationship graph |
| **ClickHouse** | 🟡 | Available / planned analytics layer |
| **Redis** | ✅ | Cache / sessions / rate limits |

### INTELLIGENCE

| Component | Status | Notes |
|---|---|---|
| **Entity Resolution** | ✅ | Incremental |
| **Risk Indicators** | ✅ | Evidence-first |
| **Event Bus** | ✅ | |
| **Webhook Engine** | ✅ | |
| **Evidence Model** | ✅ | |

### API

| Surface | Status |
|---|---|
| Summary | ✅ |
| Portfolio | ✅ |
| Transactions | ✅ |
| Entity | ✅ |
| Risk | ✅ |
| Relationships | ✅ |
| History | ✅ |

### APPLICATION

| Surface | Status | Notes |
|---|---|---|
| **Wallet Investigator** | ✅ | Stage 8 complete |
| **Evidence Drawer** | ✅ | |
| **Error-state handling** | ✅ | |
| **Interactive graph** | ✅ | |
| **Application Shell** | 🟢 | **Stage 9 — NOW** |
| **Dashboard** | ⏳ | After shell |
| **Global Search** | ⏳ | After shell |
| **Navigation** | ⏳ | After shell |

### COMMERCIAL

| Line | Status |
|---|---|
| Public Explorer | ⏳ |
| Pro SaaS | ⏳ |
| API Plans | ⏳ |
| Monitoring / Alerts | ⏳ |
| Enterprise | ⏳ |
| Multi-chain | ⏳ |

---

## Focus callout (right panel / footer)

**Now:** Stage 9 — Application Shell  
**Done:** Stage 8 Wallet Investigator + evidence UX + full investigation API  
**Next after shell:** Dashboard · Global Search · Navigation  
**Background:** Geth archive sync continues; ClickHouse analytics layer queued; commercial surfaces gated behind product shell

---

## One-line close

**Infra + intelligence + investigation API are live. Stage 9 Application Shell is the product unlock for Dashboard, Search, and Navigation.**

---

## Speaker notes (30–45 seconds)

“Infrastructure is largely standing: Lighthouse, Postgres, Neo4j, and Redis are green. Geth is still archive-syncing, so custom indexers are paused. Intelligence — entity resolution, evidence-first risk, event bus, webhooks — is incremental and working. The investigation API surface is complete. Stage 8 shipped Wallet Investigator with evidence drawer, error states, and interactive graph. Stage 9 is Application Shell: that unlocks dashboard, global search, and navigation. Commercial lines — public explorer, Pro SaaS, API plans, enterprise, multi-chain — stay gated until the shell and those product surfaces land.”

---

## Optional second slide — Stage map

```text
Stage 8 ✅  Wallet Investigator
            Evidence Drawer · Graph · Errors
                    │
                    ▼
Stage 9 🟢  Application Shell   ← NOW
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   Dashboard   Global Search  Navigation
        │
        ▼
Commercial ⏳  Explorer · Pro · API · Alerts · Enterprise · Multi-chain
```
