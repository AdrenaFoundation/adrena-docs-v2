---
title: "LP Tokens"
source: "https://docs.adrena.trade/tokenomics/alp"
---

# ALP & RW-ALP 💎

ALP & RW-ALP are the platform collateral liquidity provider tokens - for the GMX-style Pool and for the Autonom Pool respectively. ALP & RW-ALP holders act as the counterparty to traders on Adrena.

By holding ALP & RW-ALP, you:

Provide liquidity for traders to open leveraged positions
Earn a share of all trading fees (open, close, borrow)
Are exposed to trader PnL (partially, depending on trade direction)
For a deeper explanation of how the pool interacts with trader positions, 
see [Peer-to-Pool Perp Model](../../about-adrena/what-is-adrena/peer-to-pool-perp-model.md).

---

## LP Sandwich Attack Mitigation

To prevent atomic mint-then-redeem attacks (where a bad actor adds liquidity and immediately removes it to extract value), Adrena enforces a time-based guard: **liquidity cannot be removed in the same slot that it was added**. The pool records the timestamp of the last deposit and rejects removal requests that arrive before it.
