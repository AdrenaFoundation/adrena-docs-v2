---
title: "Fees"
source: "https://docs.adrena.trade/about-adrena/fees"
---

# Fees 🧀

Adrena charges fees in four categories:

| Fee Type | When Charged | Basis                                  |
|----------|-------------|----------------------------------------|
| **Close position** | At trade exit | Flat % of position size at open        |
| **Borrow fee** | Ongoing while position is open | Utilization-based (accrues per second) |
| **Virtual Funding Rate (VFR)** | Ongoing while position is open | Hourly, OI-imbalance based |
| **Swap / liquidity fee** | Adding or removing ALP / RWALP liquidity | % of swap value                        |

---

## Close Fees

Close fees are a flat percentage of the **position size** (not collateral). Rates are set per asset on-chain and adjustable by governance.

**Main Pool**

| Asset | Close Fee (BPS) | Close Fee (%) |
|-------|-----------------|---------------|
| SOL   | 10              | 0.10%         |
| BTC   | 10              | 0.10%         |
| BONK  | 18              | 0.18%         |

**Commodities Pool**

| Asset | Close Fee (BPS) | Close Fee (%) |
|-------|-----------------|---------------|
| XAU   | 16              | 0.16%         |
| XAG   | 16              | 0.16%         |
| WTI   | 16              | 0.16%         |

## Borrow Fee (Two-Slope Model)

The borrow fee compensates liquidity providers for the pool assets locked against your position. It accrues continuously while the position is open and is settled at close.

Adrena uses a **two-slope borrow rate model** with a utilization kink:

- **Below optimal utilization**: Rate increases gradually from 0 to a midpoint rate - capital is available, so borrowing is cheap
- **Above optimal utilization**: Rate increases steeply from the midpoint to the maximum - scarcity of pool assets is reflected in cost

This makes borrowing cost efficient during normal conditions while strongly incentivizing position reduction when the pool is heavily utilized.

The optimal utilization level and rate bounds are configured per custody and adjustable by governance.

---

## Virtual Funding Rate

In addition to the borrow fee, positions accrue a **Virtual Funding Rate (VFR)** based on open interest imbalance between longs and shorts. The heavier side pays the lighter side hourly. This can partially offset the borrow fee for positions on the minority side.

See [Virtual Funding Rate](../technical-documentation/virtual-funding-rate.md) for details.

---

## Swap / Liquidity Fees

Fees apply when adding or removing liquidity through ALP / RWALP minting and redemption. Rates vary based on whether the swap moves the pool's asset ratios toward or away from their targets.

---

## Fee Distribution

All protocol fees are split across five buckets. Each bucket has its own BPS share; the split sums to 10,000 BPS (100%) per pool and is configurable per pool by governance.

**ALP**
| Bucket | Recipient | Default BPS |
|--------|-----------|-------------|
| **LP fee** | ALP holders (proportional to pool share) | 7,500 (75%) |
| **Manager fee** | Pool manager / creator (paid to a stable-mint token account) | 1,500 (15%) |
| **Protocol fee** | Protocol treasury | 5000 (5%) |
| **LM fee** | Liquidity mining participants (ADX stakers) | 500 (5%) |
| **Referrer fee** | Active referrers | 100 (see Referral System) |

**RW-ALP**
| Bucket | Recipient | Default BPS |
|--------|-----------|-------------|
| **LP fee** | RW-ALP holders (proportional to pool share) | 5,000 (50%) |
| **Manager fee** | Pool manager / creator (paid to a stable-mint token account) | 4,000 (40%) |
| **Protocol fee** | Protocol treasury | 5000 (5%) |
| **LM fee** | Liquidity mining participants (ADX stakers) | 500 (5%) |
| **Referrer fee** | Active referrers | 100 (see Referral System) |

Each bucket accrues independently on the pool state (`lp_fee_debt_usd`, `manager_fee_debt_usd`, `protocol_fee_debt_usd`, `lm_fee_debt_usd`, `referrers_fee_debt_usd`) and is distributed by the on-chain `distribute_fees` instruction. This five-bucket model replaced the single unified fee bucket used prior to Release 39.
