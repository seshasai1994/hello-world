# Client Deck — Competitor Slide

Use this as one slide (or a 2-slide split if space is tight).

---

## Slide title

**Competitive Landscape & Our Positioning**

Subtitle: *Geth-powered on-chain trading platform prototype*

---

## Slide body (copy into PowerPoint / Google Slides)

### 5 Competitors

| Competitor | Strength | Gap vs our platform |
|---|---|---|
| **DEX Screener** | Fast live DEX tape, pair discovery, trader UX | Weak wallet/portfolio depth, limited execution-quality analytics, not a self-hosted Geth data plane |
| **Nansen** | Labeled wallets, smart-money dashboards, strong intel brand | Expensive, closed data, less trader execution cockpit, not designed as client-owned infra |
| **Etherscan** | Trusted explorer, tx/token/contract truth | Not a trading terminal; limited live tape, alerts, portfolio PnL, flow board |
| **CryptoQuant / Glassnode** | Macro on-chain flows & market indicators | Not real-time DEX microstructure / swap execution desk for active traders |
| **Chainalysis / TRM** | Enterprise risk & compliance attribution | Compliance-first, not trader workflow; high ACV; not a trading dashboard product |

---

### Market gap

Today’s tools are **fragmented**:

- Explorers → truth, not trading
- DEX tapes → speed, not portfolio/execution depth
- Wallet intel → labels, not self-hosted architecture
- Flow analytics → macro, not desk-level alerts
- Compliance suites → risk verdicts, not trader UX

**No single product** unifies:

`Live Tape + Token Tradability + Liquidity Events + Portfolio + Execution Quality + Alerts`  
on a **Geth-powered, client-ownable architecture**.

---

### Our prototype positioning

**Category:** On-chain Trading Intelligence Platform  
**Positioning line:**

> The unified Geth-powered trading cockpit — live tape, liquidity, portfolio, execution quality, and alerts — built on an architecture you can own and scale.

| Dimension | Our prototype stance |
|---|---|
| **For whom** | Traders, desks, and teams who need on-chain market action + wallet ops in one place |
| **Core wedge** | Trading workflows first (tape, LP events, gas/execution, alerts) |
| **Architecture** | Node → Indexers → Postgres/ClickHouse/Redis → Trading services → Dashboard/API |
| **Trust model** | Evidence-based warnings & sourced labels — not unverified “scam/entity” verdicts |
| **Deployment** | Prototype now on selective live data; production path to self-hosted Geth (~20 TB target) |
| **Differentiator** | Unified product + ownable infra, not another closed SaaS silo |

---

### One-line close (footer)

**DEX Screener speed · Nansen context · Etherscan trust · desk-ready alerts — in one Geth-powered platform.**

---

## Speaker notes (30–45 seconds)

“These five players each own one slice of the stack. DEX Screener owns tape speed. Nansen owns wallet intel. Etherscan owns trusted exploration. CryptoQuant and Glassnode own macro flows. Chainalysis and TRM own enterprise compliance.  

Our prototype sits in the gap between them: a trader-first cockpit that combines live on-chain tape, liquidity events, portfolio, execution quality, and alerts — on an architecture designed to run on self-hosted Geth as we scale storage from this 1 TB prototype toward production.”

---

## Optional second slide — Positioning map

```text
                    High Trading UX
                           │
                           │  ★ OUR PROTOTYPE
                           │     (Tape + Portfolio +
                           │      Execution + Alerts)
         DEX Screener ●    │
                           │
                           │         ● Nansen
                           │
Low Infra Ownability ──────┼──────────────── High Infra Ownability
                           │
              Etherscan ●  │
                           │
     CryptoQuant/Glassnode ●
                           │
                           │              ● Chainalysis/TRM
                           │
                    Low Trading UX
```

---

## Optional objection handlers

| Client question | Answer |
|---|---|
| “Isn’t this just DEX Screener?” | Tape is one module. We add portfolio, execution quality, alerts, and ownable Geth architecture. |
| “Why not just buy Nansen?” | Nansen is closed intel SaaS. We are building a product + infra stack you can deploy, extend, and white-label. |
| “Can you match Etherscan?” | We use explorer-grade truth as a base layer, then productize trading workflows on top. |
| “Do you do Chainalysis-style attribution?” | Not as unverified auto-verdicts. We support sourced labels and evidenced pattern warnings; full attribution needs ground truth. |
| “You only have 1 TB now?” | Correct for prototype. Full architecture is designed; production storage roadmap is ~8 TB MVP → ~20 TB production. |
