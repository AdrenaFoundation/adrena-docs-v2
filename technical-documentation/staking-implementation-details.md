---
title: "Staking Implementation Details"
source: "https://docs.adrena.trade/technical-documentation/staking-implementation-details"
---

# Staking Details 🏦

Adrena and its 100% revenue sharing is all about redistributing revenues as the core feature of the platform. A big chunk of that is done through ALP (pool's share) appreciation, as most of the fee revenues go back to the pool directly.

The exact distribution is as follow:

75% for ALP (liquid), shared with ALP Locked Stakers

30% for RW-ALP (liquid), shared with RW-ALP Locked Stakers

5% for ADX, shared with ADX Stakers (liquid and locked)

---
Adrena offers the possibility to Lock Stake, aligning with the protocol long term strategy. By doing so, users get amplified revenue share (at the detriment of non Locked Stakers on USDC yield, not for ADX bonuses).

Let's take the case of ALP for an example:

Starting conditions:

1000 ALP token circulating

800 un-Staked

100 Staked 180 days

100 Staked 360 days


100$ of revenue is to be distributed this round to ALP.

800 ALP un-Staked <=> 800

100 ALP Staked 180 days <=> 100 * 1.75 (175)

100 ALP Staked 360 days <=> 100  * 2.50 (250)


Total weight is 800 + 175 + 250 (1225)


And so final distribution is

1000/1225 * 100$ -> to the LP pool (all ALP appreciating)

75/1225 * 100$ going as bonus USDC yield to ALP 180 days Stakers

150/1225 * 100$ going as bonus USDC yield to ALP 360 days Stakers

---

Rewards accrue as time passes, and actions are carried on the platform. But the actual rewards are accumulated and distributed in rounds in order to batch operations together.
