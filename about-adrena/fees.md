---
title: "Fees"
source: "https://docs.adrena.trade/about-adrena/fees"
---

# Fees 🧀

Adrena charges fees in four categories:

| Fee Type | When Charged | Basis |
|----------|-------------|-------|
| **Open position** | At trade entry | Flat % of position size |
| **Close position** | At trade exit | Flat % of position size (+ exit multiplier if early) |
| **Borrow fee** | Ongoing while position is open | Utilization-based (accrues per second) |
| **Swap / liquidity fee** | Adding or removing ALP liquidity | % of swap value |

---

## Open & Close Fees

Open and close fees are a flat percentage of the **position size** (not collateral). The exact rates are set per asset and visible on the trading UI.

### Position Exit Fee Multipliers

Closing a position within the first 30 minutes incurs a multiplied close fee to deter short-lived exploitation. See [Position Exit Fees](what-is-adrena/position-exit-fees.md) for the full multiplier table.

| Time Since Open | Close Fee Multiplier |
|-----------------|---------------------|
| 0 – 4 min | Cannot close |
| 4 – 7 min | 15× |
| 7 – 15 min | 3× |
| 15 – 30 min | 1.5× |
| 30 min+ | 1× (normal) |

---

## Borrow Fee (Two-Slope Model)

The borrow fee compensates liquidity providers for the pool assets locked against your position. It accrues continuously while the position is open and is settled at close.

Adrena uses a **two-slope borrow rate model** with a utilization kink:

- **Below optimal utilization**: Rate increases gradually from 0 to a midpoint rate — capital is available, so borrowing is cheap
- **Above optimal utilization**: Rate increases steeply from the midpoint to the maximum — scarcity of pool assets is reflected in cost

This makes borrowing cost efficient during normal conditions while strongly incentivizing position reduction when the pool is heavily utilized.

The optimal utilization level and rate bounds are configured per custody and adjustable by governance.

---

## Virtual Funding Rate

In addition to the borrow fee, positions accrue a **Virtual Funding Rate (VFR)** based on open interest imbalance between longs and shorts. The heavier side pays the lighter side hourly. This can partially offset the borrow fee for positions on the minority side.

See [Virtual Funding Rate](../technical-documentation/virtual-funding-rate.md) for details.

---

## Swap / Liquidity Fees

Fees apply when adding or removing liquidity through ALP minting and redemption. Rates vary based on whether the swap moves the pool's asset ratios toward or away from their targets.

---

## Fee Distribution

All protocol fees are split across four recipients:

| Bucket | Recipient |
|--------|-----------|
| **LP fee** | ALP holders (proportional to pool share) |
| **LM fee** | Liquidity mining participants |
| **Protocol fee** | Protocol treasury |
| **Manager fee** | Pool manager / creator |

Referrer fees are sourced from the protocol fee share and distributed to active referrers.

The exact BPS split for each bucket is configurable per pool by governance. This model replaced the single unified fee bucket used prior to Release 39.
