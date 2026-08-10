# $1M ARR Plan by Dashboard

Geth-powered trading platform — revenue plan mapped to the 10 monetizable dashboards.

---

## Revenue model at a glance

| Revenue line | Price | Target count | ARR |
|---|---|---|---|
| **Pro subscriptions** (individuals) | $59/mo | 600 users | $425k |
| **Desk plans** (teams 2–10 seats) | $599/mo | 45 teams | $323k |
| **Enterprise** (white-label, SLA, custom) | $35k/yr avg | 5 clients | $175k |
| **API add-on** (usage overage) | $99–999/mo | ~60 accounts | $115k |
| **Total** | | | **~$1.04M** |

Slack built in: if Enterprise lands at 3 instead of 5, ~150 more Pro users cover the gap.

---

## The 10 dashboards — build order and plan mapping

### Wave 1 — the wedge

1. **Live Swap Tape** — Free (delayed, top 10 tokens) → Pro (real-time, all tokens).
   The demo that sells everything else; acquisition → Pro trigger.
2. **Token Trader Cockpit** — Pro. Buy/sell ratio, velocity, holders, liquidity,
   sellability warnings. Highest daily session count; retention driver.
3. **Liquidity Events Feed** — Pro (view) → Desk (alerts). LP add/remove,
   owner-LP concentration, liquidity-pulled flags. Rug/opportunity detection.
4. **Alerts Center** — Pro (5 rules, email) → Desk (50 rules, webhooks) →
   Enterprise (unlimited, SLA). The retention lock and the upsell mechanism.

**Milestone:** launchable paid product; 150 Pro = ~$106k ARR run rate.

### Wave 2 — the moat

5. **Portfolio + PnL** — Free (1 wallet) → Pro (10) → Desk (unlimited + shared).
   Daily-open habit product; drives Pro base 150 → 400.
6. **Whale / Large Flow Tape** — Pro (view) → Desk (filters + alerts + export).
   Shareable signal product; organic marketing loop.
7. **Execution Quality Desk** — Pro. User's own swaps: slippage vs expected,
   gas vs block benchmark, failed/replaced txs. Unique wedge nobody else does well.
   Sales line: "You lost $340 to slippage and gas overpay this month."

**Milestone:** 400–600 Pro + 10–15 Desk = ~$450–530k ARR run rate.

### Wave 3 — the B2B expansion

8. **CEX Flow Board** — Desk + Enterprise. Sourced/published exchange addresses
   only; netflow trends. Justifies $599/mo vs $59/mo.
9. **Stablecoin Flow Board** — Desk + Enterprise. USDC/USDT/DAI flows, DEX/CEX
   rotation, risk-on/off. Pairs with #8 as the "flow suite."
10. **API Analytics Access** — add-on at every tier. `/tape`, `/token`, `/flows`,
    `/portfolio`, `/alerts` with keys + rate tiers. Highest revenue ceiling,
    lowest churn.

**Milestone:** 45 Desk + 3–5 Enterprise + API = cross $1M ARR run rate.

---

## Pricing sheet

| Tier | Price | Dashboards | Alert quota | API |
|---|---|---|---|---|
| **Free** | $0 | Tape (delayed), 1-wallet portfolio, network health | 1 rule | — |
| **Pro** | $59/mo ($590/yr) | Trader dashboards 1–7 | 5 rules, email | $99/mo add-on |
| **Desk** | $599/mo (5 seats) | Everything + flow boards 8–9, exports, shared watchlists | 50 rules, webhooks | Soft cap incl., overage billed |
| **Enterprise** | $25k–$60k/yr | White-label, custom indexes, SLA, private deploy | Unlimited | Contract |

Annual at ~2 months free; target 40% of Pro on annual by year end.

---

## Acquisition funnel math

| Funnel stage | Number | Assumption |
|---|---|---|
| Free signups | ~20,000 | 3% free→Pro conversion |
| → Pro users | 600 | typical for trading tools with strong free tier |
| Pro → Desk | 45 teams | ~1 team per 13 Pro users |
| Desk/inbound → Enterprise | 5 | white-label + flow-suite deals from client presentations |
| Dev signups → API paid | 60 | free-key funnel from docs + "get this via API" buttons |

Channels in priority order:

1. Screenshot loop — watermarked share images on whale tape + execution cards
2. Public data-freshness badge — trader trust
3. Telegram/Discord alert bots — branded free distribution
4. Client-deck presentations — every prototype demo is an Enterprise lead

---

## Quarterly targets

| Quarter | Focus | ARR run rate |
|---|---|---|
| Q1 | Wave 1 live, 150 Pro | ~$106k |
| Q2 | Wave 2 live, 400 Pro, 10 Desk | ~$355k |
| Q3 | Wave 3 live, 550 Pro, 30 Desk, 2 Ent, API beta | ~$700k |
| Q4 | 600 Pro, 45 Desk, 5 Ent, 60 API accounts | **~$1.04M** |

---

## Three rules that protect the plan

1. **Alerts before breadth.** A user with 3 alert rules set is worth more than
   5 new dashboards. Ship Alerts Center in wave 1 no matter what slips.
2. **No dashboard #11 until the 10 are monetized.** Every extra dashboard delays
   the Desk tier — a third of the revenue.
3. **Sourced labels only on flow boards.** One fabricated exchange attribution
   destroys the trust that Desk/Enterprise pricing depends on.
