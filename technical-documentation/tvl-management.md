# TVL Management

## Why TVL is Managed

LP returns are mechanically a function of fees divided by capital deployed. When TVL grows faster than trading volume, every LP earns a smaller share of the same fee stream - the pool dilutes its own yield.

ALP operates with a **soft cap on TVL that grows in step with realized fees**. The protocol commits to a target LP yield band, and the cap is adjusted upward - only on rule, only when justified - such that yield stays inside that band.

This is not a yield guarantee. Fees can fall and APY can dip. What the framework guarantees is that the protocol won't make things worse by allowing fresh capital to dilute already-stressed yields, and won't squander high-fee periods by leaving capacity frozen.

## Reference APY

Every TVL decision anchors to a single, publicly computable metric.

```
                   (F_W × 365/W × 0.75) - TraderPnL_W - ULP_W
Reference APY  =  ────────────────────────────────────────────
                                  TVL_W avg
```

- **F\_W** - total fees over the trailing window (W = 30 or 15 days)
- **0.75** - LP share of protocol revenue
- **TraderPnL\_W** - net trader P&L impact on the pool (positive = pool drag)
- **ULP\_W** - Assets Unlocked Performance, the impact of price moves on assets not currently locked in trader positions
- **TVL\_W avg** - time-weighted average TVL over the window

The formula captures realized LP return, not headline fee yield. A pool can generate strong fees while losing capital to trader PnL or market drift on unutilized assets - Reference APY accounts for both.

The metric is computable from on-chain data, so any LP can verify the protocol's reported number.

## Operating Bands

| Band | APY | Action |
|---|---|---|
| 🟦 Critical | < 5% | Pause new minting |
| 🟨 Below-Target | 5% - 25% | No protocol action |
| 🟢 Green | 25% - 35% | Normal operation; lifts considered above 30% |
| 🟥 Blue | > 35% | Lift cap per formula |

Green is the design target. There is no mechanism for protocol-driven TVL reduction - at 20% APY the pool is still productive, and forcing capacity contraction would signal unwarranted distress. The mint pause trigger sits at <5%, the level at which the pool is genuinely unviable.

## Cap Lift Formula

```
                                                    F_run-rate
New Cap  =  min (  Current Cap × 1.30  ,  ─────────────────────  )
                                                    APY_target
```

Where **F\_run-rate** : annualized fee run rate net of trader PnL and ULP drag, after the 75% LP share (USD per year); computed as (F\_30 × 365/30 × 0.75) - TraderPnL\_30 - ULP\_30, **APY\_target = 27%** (Green band midpoint, buffered against downside drift).

Two triggers:

- **Standard** - first Monday of each month. Trailing 30-day Reference APY above 30% across two consecutive reviews.
- **Expedited** - 15-day trailing Reference APY above 35%. Upward only.

The expedited path exists because fee growth can outpace a monthly window, especially at relaunch.

## Why +30% Per Lift

The step-size cap is the most important parameter for LP experience.

| Pre-lift APY | Post-lift APY (constant fees, +30% TVL) |
|---|---|
| 30% | 23.1% |
| 35% | 26.9% |
| 40% | 30.8% |

A lift from 35% lands at 27% - the middle of Green. A larger step (e.g., +50%) would land that same pre-lift reading at 23%, a meaningful negative LP experience. +30% is the constraint that prevents this.

## Notice and Transparency

- Cap adjustments announced at least 7 days before taking effect
- Current TVL, cap, trailing Reference APY, and band are displayed on the ALP page
- A historical log of every cap adjustment is maintained
- Parameter changes require a governance proposal with at least 14 days' notice

## Parameter Summary

| Parameter | Value |
|---|---|
| LP fee share | 75% |
| Target band | 25% - 35% APY |
| Lift trigger (standard) | > 30% for 2 consecutive reviews |
| Lift trigger (expedited) | 15-day > 35% |
| Max lift per adjustment | +30% |
| Post-lift APY target | 27% |
| Reference window | 30 days (standard), 15 days (expedited) |
| Review cadence | Monthly, first Monday |
| Mint pause trigger | < 5% |
| Notice period | 7 days |
