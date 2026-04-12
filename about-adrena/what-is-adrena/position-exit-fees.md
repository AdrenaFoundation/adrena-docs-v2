---
title: "Position Exit Fees"
---

# Position Exit Fees

## Why Exit Fee Tiers Exist

Adrena's zero-slippage, single-transaction execution model is highly efficient — but it can be exploited by sophisticated actors who open and immediately close positions to extract value during sharp price moves (sandwich attacks) or flash crashes. Position exit fee tiers address this by making very short-lived positions significantly more expensive to close, eliminating the economic incentive for this behavior.

Exit fee tiers were introduced in Release 39 as a proactive complement to Adrena's existing [toxic flow monitoring](../../technical-documentation/toxic-flow-countermeasures.md).

---

## Minimum Open Time

A position **cannot be closed at all** within the first **4 minutes** of opening. This hard minimum prevents the most egregious same-block or near-instant exploitation.

Additionally, after any **collateral modification** (adding or removing collateral from an existing position), a **2-minute lock** applies before the position can be closed. This prevents collateral manipulation being used to game the fee tiers.

---

## Fee Multiplier Table

After the minimum open time has elapsed, the standard close fee is multiplied based on how long the position has been open:

| Time Since Open | Fee Multiplier | Notes |
|-----------------|---------------|-------|
| 0 – 4 min | Cannot close | Hard minimum open time |
| 4 – 7 min | **15×** base close fee | Aggressive deterrent window |
| 7 – 15 min | **3×** base close fee | Elevated fee window |
| 15 – 30 min | **1.5×** base close fee | Moderate fee window |
| 30 min+ | **1×** base close fee | Normal fee applies |

For the base close fee rate, see [Fees](../fees.md).

---

## Example

Suppose the base close fee is 0.06% of position size and a trader opens a $10,000 position:

| Time Held | Effective Close Fee | Cost |
|-----------|--------------------|----|
| 5 min | 15× 0.06% = 0.9% | $90 |
| 10 min | 3× 0.06% = 0.18% | $18 |
| 20 min | 1.5× 0.06% = 0.09% | $9 |
| 45 min | 1× 0.06% = 0.06% | $6 |

The aggressive multipliers in the first 15 minutes make short-term exploitation economically unviable in most scenarios.

---

## What Is Not Affected

- **Liquidations** are not subject to exit fee multipliers — Adrena does not charge extra liquidation fees (see [No Liquidation Fees](no-liquidation-fees.md))
- **Long-held positions** (30 min+) pay exactly the normal close fee with no penalty
- The multipliers apply to the **close fee only** — open fees, borrow fees, and funding rates are unaffected
