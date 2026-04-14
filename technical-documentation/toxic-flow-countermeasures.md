---
title: "\"Toxic Flow\" Countermeasures"
source: "https://docs.adrena.trade/technical-documentation/toxic-flow-countermeasures"
---

# "Toxic Flow" Countermeasures ☢️

## Background

GMX-inspired perp venues have liquidity fuelled by passive liquidity providers, and trades execute at 0 slippage based on oracle price. In this context, informed traders can extract value from the platform (see the Avax manipulation incident on GMX Arbitrum). On a traditional order book based venue, this would not be possible, as the cost of liquidity would be impacted.

## How Other Platforms Handle It

- **GMX**: Splits trades into 2 transactions, introducing latency. This acts as a delay-based protection but harms UX significantly.
- **Jupiter Perps**: Uses a keeper model — receives trade intents and funds, then eventually submits trades. Heavy UX during high volatility (comparable to 4 seconds of latency).

## Adrena's Approach

Since inception, Adrena's ethos is to keep it simple and fair, and to provide a user experience on par with what Solana offers in terms of TX settlement speed. **Adrena does not use a keeper.** This allows for:

- Super snappy single-transaction trade execution
- Transparent, straight on-chain experience
- No detours or proxy hops

## Monitoring

Adrena monitors `markout_1m`, `5m`, and `10m` to see the PnL of trades 1/5/10 minutes after opening, allowing the team to identify and respond to toxic flow patterns.

---


See [Position Exit Fees](../about-adrena/what-is-adrena/position-exit-fees.md) for the full breakdown.
