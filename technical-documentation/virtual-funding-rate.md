---
title: "Virtual Funding Rate"
---

# Virtual Funding Rate

## Background

In a peer-to-pool perpetual model, open interest (OI) between longs and shorts is rarely balanced. When longs significantly outweigh shorts (or vice versa), the liquidity pool bears disproportionate directional risk. The **Virtual Funding Rate (VFR)** is a periodic payment mechanism that redistributes this imbalance cost directly between the two sides, keeping the pool's net exposure manageable over time.

This is analogous to the funding rate on centralized exchanges, but applied within Adrena's on-chain peer-to-pool architecture.

---

## How VFR Works

Funding flows from the heavier side to the lighter side every hour:

- If **longs > shorts**: long positions pay short positions
- If **shorts > longs**: short positions pay long positions

The rate scales with the imbalance — the more skewed OI is, the higher the funding obligation. Funding is **accrued continuously** and **settled at position close**, meaning it accumulates in the position's tracked state and is applied when the position is closed.

---

## Rate Calculation

The hourly funding rate is determined by OI imbalance and a configurable sensitivity:

1. **OI Imbalance** =  |long OI − short OI| / total OI, expressed in BPS
2. **Scaled Imbalance** = imbalance × imbalance_sensitivity_bps / 10,000
3. **Funding Rate** = max_hourly_funding_rate × scaled_imbalance / 10,000
4. Rate is capped at `max_hourly_funding_rate`

The `min_total_oi_usd` threshold must be exceeded for VFR to activate — this prevents the rate from firing on negligible open interest.

### Parameters (per custody)

| Parameter | Description |
|-----------|-------------|
| `max_hourly_funding_rate` | Hard cap on the hourly funding rate |
| `min_total_oi_usd` | Minimum total OI required to activate funding |
| `imbalance_sensitivity_bps` | Multiplier controlling how aggressively the rate responds to imbalance |

These are configured per-custody and can be adjusted by governance.

---

## Impact on Positions

Funding is tracked cumulatively at both the **custody level** (global index) and the **position level** (entry index). At position close:

- The difference between the current global index and the position's entry index is applied
- Net funding is either deducted from or added to the position's realized PnL
- Traders on the heavier side pay; traders on the lighter side receive

This means:
- **Paying side**: effective cost increases over time for holding a position on the crowded side
- **Receiving side**: positions on the minority side earn a passive income component on top of any trading PnL

---

## Comparison to Traditional Funding Rates

| Aspect | CEX Funding Rate | Adrena VFR |
|--------|-----------------|------------|
| Settlement frequency | Every 8 hours (typically) | Continuous accrual, settled at close |
| Counterparty | Other traders | LP pool acts as intermediary distributor |
| Transparency | Published oracle | On-chain, per-custody state |
| Rate mechanism | Index–mark price divergence | OI imbalance sensitivity |

---

## Relationship to Borrow Fees

VFR operates independently from the borrow fee. Both accrue while a position is open:

- **Borrow fee**: paid by all positions to compensate liquidity providers for locking pool assets (see [Fees](../about-adrena/fees.md))
- **VFR**: net transfer between longs and shorts based on OI imbalance — can partially offset borrow costs for positions on the minority side

See [Position Parameters](position-parameters.md) for how both fees interact with a position's overall cost.
