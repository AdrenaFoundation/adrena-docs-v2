# Asset Mix and Weights

## Why This Matters

Every ALP token is backed by a basket of underlying assets in defined proportions. Two questions determine the LP experience: **what's in the basket** and **in what proportions**. Both are decisions the protocol makes on behalf of LPs, and both should be made by discipline rather than discretion.

This page documents the methodology that produces the target weights, the bands within which the pool operates, and the mechanism that keeps weights in line with target.

## The Four Principles

The target weights derive from four principles applied jointly.

**1. Volatility-weighted allocation.** Among the volatile assets, weight is inversely proportional to volatility relative to the lowest-volatility asset (BTC). More volatile assets receive smaller weights so that no single asset's price swings dominate the LP token's NAV.

- SOL is 1.5–1.7x BTC volatility → strict weighting puts SOL at ~60–70% of BTC weight
- BONK is 1.7–2.8x BTC volatility → strict weighting puts BONK at ~35–60% of BTC weight

**2. SOL-dominance compromise.** Pure volatility weighting would produce a BTC-dominant pool, but ALP is positioned as a Solana-ecosystem product. The deliberate compromise is to overweight SOL relative to its volatility-implied weight, accepting moderate additional NAV volatility for product coherence.

**3. USDC anchor at 30%.** USDC presence in the pool serves three purposes: it enables short positions, it reduces overall pool volatility through diversification, and it provides the redemption-friendly asset for LP exits. 30% is the lower bound that keeps the pool feeling balanced without diluting fee-generating capacity from volatile assets.

**4. Correlation as secondary filter.** When evaluating new additions or rebalances, correlation to existing assets is a tiebreaker, not a gate. In crypto, baseline correlations are high in absolute terms; the framework looks for relative differences.

## Target Weights and Bands

| Asset | Target | Min | Max |
|---|---|---|---|
| USDC | 30% | 25% | 40% |
| SOL | 35% | 28% | 42% |
| BTC | 25% | 20% | 30% |
| BONK | 10% | 7% | 15% |

The Min/Max bands define the operating perimeter. Within the band the protocol does not intervene — mint and redeem fees naturally incentivize arbitrage back toward target. Sustained breaches (>14 days outside band) trigger a governance review of whether the target itself should adjust.

Band widths are asymmetric per asset:

- **USDC** has a wider upper band because in stress events traders close positions and the pool naturally accumulates USDC; defending a tight cap there would be counterproductive.
- **BONK** has the widest relative band because its volatility makes weight maintenance costly; tighter bands would generate excessive rebalancing trades.

## Volatility Window

All volatility computations — both initial weight derivation and future rebalancing decisions — use a **90-day rolling window**. Shorter windows are too sensitive to single events; longer windows lag market regime changes and produce stale weights.

## Dynamic Mint and Redeem Fees

The pool migrates toward target weights through a fee mechanism rather than protocol-side swaps.

- When an asset is **below** target, its mint fee is **lower** (incentive to deposit) and its redeem fee is **higher** (disincentive to withdraw)
- When an asset is **above** target, its mint fee is **higher** and its redeem fee is **lower**

The primary tool during the relaunch period is **zero mint fee on under-weighted assets**, channeling new deposits toward whichever assets the pool needs. The team monitors weights against bands and adjusts fee parameters via governance as conditions evolve.

If natural flow does not converge the pool toward target within a reasonable window, a manual rebalance via Jupiter Swap can be executed as a fallback.

## Review Cadence

- Target weights reviewed **quarterly** via governance proposal
- Bands reviewed **annually** unless breached
- Volatility data refreshed at every quarterly review

## Parameter Summary

| Parameter | Value |
|---|---|
| Volatility window | 90 days rolling |
| Band breach review trigger | >14 days outside band |
| Target review cadence | Quarterly |
| Band review cadence | Annual (unless breached) |
| Primary rebalancing mechanism | Dynamic mint/redeem fees |
| Fallback rebalancing mechanism | Manual swap via governance |
