---
title: "Position Parameters"
source: "https://docs.adrena.trade/technical-documentation/position-parameters"
---

# Position Parameters 🪖

This page describes the parameters and mechanics that govern how positions are opened, maintained, and closed on Adrena.

---

## Leverage and Position Size

- Maximum leverage and minimum/maximum position size are set per asset
- A **maximum cumulative long position size** cap exists per custody, limiting the total long exposure the pool accepts in a single asset
- These limits protect the pool from excessive directional risk concentration

---

## Opening a Position

Trades execute at oracle price with zero slippage.

For positions in [Autonom Pools](autonom-pools.md) (RWA/synthetic assets), the position can only be opened during the asset's defined market hours.

---

## Ongoing Costs While a Position is Open

### 1. Borrow Fee

The borrow fee accrues continuously (per second) based on pool utilization. Adrena uses a **two-slope model**:

- Below the optimal utilization kink: low, gradually rising rate
- Above the optimal utilization kink: steep rate increase

This ensures cheap borrowing at normal utilization and reflects asset scarcity when the pool is heavily used. The optimal utilization level and rate bounds are set per custody.

### 2. Virtual Funding Rate (VFR)

Positions also accrue a [Virtual Funding Rate](virtual-funding-rate.md) based on the open interest imbalance between longs and shorts. The majority side pays the minority side at an hourly rate proportional to the imbalance. VFR is settled at position close.

---

## Closing a Position

A flat **close fee** (% of position size) applies at close. 

### Collateral Modification Lock

After adding or removing collateral from an existing position, the position is locked for **4 minutes** before it can be closed. This prevents collateral manipulation to game the exit fee tiers.

---

## Liquidation

A position is liquidated when the remaining collateral falls to the liquidation margin threshold. Key properties:

- **Conservative pricing**: Liquidation prices use the oracle's conservative bound (low for longs, high for shorts)
- **Asymmetric liquidation defense** (GMX pools): Requires backup oracle confirmation before liquidating, preventing liquidations on single-oracle staleness
- **Autonom pool liquidations**: Cannot execute outside market hours (no reliable price available)

---

## Market Hours (Autonom Pools Only)

Positions in [Autonom Pools](autonom-pools.md) are subject to the trading hours of the underlying real-world asset. Opening a new position outside market hours returns a `MarketIsClosed` error. 

---

## Fee Summary

| Fee | Timing | Basis |
|-----|--------|-------|
| Borrow fee | Continuous | Per-second, utilization-based |
| Virtual Funding Rate | Continuous | Hourly OI imbalance |
| Close fee | At exit | Flat % of position size|

See [Fees](../about-adrena/fees.md) for distribution details.
