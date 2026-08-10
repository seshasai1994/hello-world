# $1M Roadmap — 36 Months, Gated

Complete execution roadmap for the Geth-powered trading + compliance analytics
platform. Commitment model: hard quarterly gates, not projections. Hit the
gate, proceed. Miss by <50%, one quarter to recover. Miss by >50% twice,
pivot or stop.

---

## Operating rules

1. Every quarter has a revenue gate with a decision attached.
2. Founder-led sales from month 1 — 50 conversations per quarter, non-negotiable.
3. Nothing gets built that isn't attached to a revenue line validated by 3+ buyer conversations.
4. Runway never drops below 9 months without a bridge decision.

## Resources required

| Resource | Spec | When |
|---|---|---|
| Founder, 50% of week on sales | From month 1 | Day 0 |
| 2 senior backend/data engineers | Indexers, PG/CH, APIs | Month 0–1 |
| 1 frontend engineer (contract OK) | Dashboards | Month 2 |
| Capital | $1.2–1.5M total, >= 18 months runway | Day 0 |
| Infra | ~$500/mo growing to ~$3k/mo by year 2 | As needed |
| Legal (entity, ToS, contract template) | ~$10k | Month 1 |

---

## Phase 1 — Foundation + first cash (Months 0–6)

**Build**
- M0–1: Geth full + Lighthouse; managed RPC backup; Postgres schema + checkpointed indexer framework
- M1–3: transfers, swaps, LP, approvals indexers; Redis + WS fan-out; trace indexer started
- M3–5: 4 dashboards (Live Tape, Token Cockpit, Liquidity Events, Alerts Center); Paddle billing; Pro tier live
- M5–6: trace indexer production-ready — "every wei including internal transfers" claim goes live

**Sell**
- 150 outreach → 40 conversations → 2 paid pilots ($5–15k) + 1 monitoring retainer ($2–4k/mo)
- Weekly public data screenshot thread (freshness = marketing)

**Gate 1 (end M6): $25k+ booked + 50 Pro subscribers + tape uptime >99% for 60 days.**
Miss badly → problem is positioning/market, not code. Stop building, fix sales.

## Phase 2 — Compliance suite + recurring base (Months 6–12)

**Build**
- M6–8: Exposure Screening (published lists + hop traversal), Treasury Board, Approval Monitor
- M8–10: Whale Tape with internal transfers, Execution Quality Desk, Portfolio/PnL
- M10–12: API tier v1 (address activity, token, tape; keys + rate limits)

**Sell**
- Convert pilots to annuals ($15–40k each)
- 2–4 compliance pilots ($5–10k each)
- 1 managed-stack / white-label anchor deal in pipeline ($30–100k)
- Pro base 150 → 350

**Gate 2 (end M12): $35–50k MRR equivalent OR one anchor deal >= $50k signed.**
Make-or-break gate. Missing both = services shop, not platform — decide deliberately.

## Phase 3 — Scale what converted (Months 12–24)

**Build (only what Phase 2 revenue validated)**
- Archive node (path-based Geth or Erigon for trace_filter) → attestations, snapshots, historical PnL
- ClickHouse analytics tier; Desk plan features (shared watchlists, exports, webhooks)
- Enterprise hardening only when a contract requires it (SSO, audit logs, SLA)

**Sell**
- Sales hire month 12–15 (after founder has closed 10+ deals)
- 3–5 enterprise/white-label deals ($30–100k)
- Desk 20–40 teams; Pro 350 → 600; API 30–60 accounts

**Gate 3 (end M18): $60k MRR. Gate 4 (end M24): $83k MRR = $1M ARR.**
Cumulative collections cross $1M in months 20–26 on this curve.

## Phase 4 — Durability (Months 24–36)

Multi-chain expansion (same pipeline, new markets), data licensing / warehouse
feeds, iOS as retention feature. Makes the $1M defensible instead of peak.

---

## Revenue bridge

| Quarter | MRR exit | Cumulative collected | Driver |
|---|---|---|---|
| Q1 | ~$3k | ~$15k | Pilots booked |
| Q2 | ~$10k | ~$50k | Pilots + retainers + Pro launch |
| Q3 | ~$20k | ~$110k | Compliance pilots, Pro growth |
| Q4 | ~$40k | ~$230k | Anchor deal + annuals |
| Q5 | ~$50k | ~$390k | Desk tier + API |
| Q6 | ~$62k | ~$580k | Enterprise #2–3 |
| Q7 | ~$72k | ~$800k | Scale + archive products |
| Q8 | ~$85k | ~$1.05M | $1M ARR + $1M collected |

Honest odds: roughly 1 in 5. The crypto market cycle is the largest
un-priceable external risk.

## Kill risks, ranked

1. Founder selling <50% of time (kills silently by month 8)
2. Building Phase 3 features in Phase 1 (Neo4j, iOS, dashboard #11)
3. Under-capitalization (<18 months runway at start)
4. Bear market in months 6–18 (halve consumer numbers; lean on compliance — those budgets survive bears)
5. One fabricated data incident (stale tape sold as live, unsourced label) — trust products die from one lie
