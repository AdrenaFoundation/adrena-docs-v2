# Custody Addition Framework

## Why a Framework

ALP's custody slots are a finite resource. The pool can hold up to 8 custodies; 4 are currently used (USDC, SOL, BTC, BONK). Adding a new tradable asset is a real product lever - more custodies means more trader pairs and more potential volume - but each addition also dilutes existing weights, changes the LP token's volatility profile, and consumes a slot that's hard to free up.

This page sets out the rules for when an addition is justified, what weight a new asset should receive, and how the pool migrates to accommodate it.

## Addition Justification Test

A custody addition is considered when both of the following are met.

**Volume test.** The candidate has demonstrated trader demand on comparable platforms, measured as the candidate's trading volume as a percentage of the most-traded asset on that platform. A reading of **15-25% or more** of the leader's volume is a meaningful signal that the asset commands real trader interest in relative terms. Below 15%, the addition risks being a vanity slot - present but undertraded.

**Reserve sufficiency test.** The pool's current TVL must produce a custody reserve large enough to support typical trade sizes for that specific asset on comparable platforms. The check is asset-specific: a long-tail asset with smaller typical trade sizes needs a meaningfully smaller reserve than a major asset where trades routinely run into hundreds of thousands.

There is no fixed minimum TVL gate. As an indicative reference, a custody reserve of around $100k can support meaningful trading for less liquid assets; major assets typically require several hundred thousand or more. The protocol verifies sufficiency on a case-by-case basis by comparing the implied reserve (current TVL × proposed weight) against typical and high-percentile trade sizes observed on comparable platforms.

**Correlation as tiebreaker.** When multiple candidates pass the volume and reserve tests, preference goes to assets that bring lower correlation to the existing basket. In crypto, baseline correlations are high in absolute terms - the framework uses correlation as a relative preference among qualifying candidates, not as a hard gate.

## Weight Determination

A new asset's target weight is determined by:

1. Compute the asset's volatility relative to BTC over the 90-day window
2. Apply the volatility-weighting principle (see [Asset Mix and Weights](asset-mix-and-weights.md))
3. Cap the new weight at **12.5%** initially, regardless of what volatility-weighting suggests, to limit risk during the asset's first integration period
4. After 90 days of operation, the cap is removed and the asset can rebalance to its volatility-implied weight if justified

## Rebalancing Path

Adding an asset means reducing existing weights. The protocol does not dump existing assets to fund the new custody.

1. The new asset's initial target weight is determined per the rules above
2. Existing volatile assets reduce pro-rata to make room - USDC anchor remains at 30%, the volatile basket goes from 70% to (70% − new\_weight)%
3. Market mint/redeem flow migrates the pool composition over a 30-day window, with mint and redeem fees adjusted to incentivize correct flow (same dynamic fee mechanism as standard rebalancing)
4. Protocol-driven swaps are reserved as a fallback if the 30-day market-driven path fails to converge

## Worked Example

A hypothetical addition of a 5% custody at a point when ALP TVL is $2M. This sizing reflects an asset where typical trades are smaller than for the existing basket - the 5% allocation produces a $100k reserve, sufficient for that asset's trade-size profile.

| Asset | Pre-Addition Weight | Post-Addition Weight | Pre-Addition $ | Post-Addition $ |
|---|---|---|---|---|
| USDC | 30% | 30% | $0.60M | $0.60M |
| SOL | 35% | 32.5% | $0.70M | $0.65M |
| BTC | 25% | 23.2% | $0.50M | $0.46M |
| BONK | 10% | 9.3% | $0.20M | $0.19M |
| New asset | - | 5% | - | $0.10M |

Existing volatile assets reduce pro-rata at ~7% relative reduction each. The actual weight for any candidate would be computed against current 90-day volatility data and reserve sufficiency at the time of evaluation, capped at the 12.5% initial-period limit.

## Parameter Summary

| Parameter | Value |
|---|---|
| Maximum custodies | 8 |
| Current custodies | 4 (USDC, SOL, BTC, BONK) |
| Volume test threshold | 15-25% of platform leader's volume |
| Reserve sufficiency | Case-by-case; sized to typical trade sizes on comparable platforms |
| Initial weight cap | 12.5% |
| Initial period (cap applies) | 90 days |
| Rebalancing window | 30 days market-driven, swap fallback |
