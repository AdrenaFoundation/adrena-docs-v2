---
title: "Oracles and Price Feeds"
source: "https://docs.adrena.trade/technical-documentation/oracles-and-price-feeds"
---

# Oracles and Price Feeds 🔮

Adrena uses oracle price feeds to determine trade execution prices. All trades execute at oracle price with zero slippage.

---

## Three-Provider Oracle System

As of Release 39, Adrena sources prices from **three independent oracle providers**. Each provider covers a distinct feed ID range:

| Provider | Feed ID Range | Mechanism |
|----------|--------------|-----------|
| **ChaosLabs** | 0 – 29 | Off-chain signed batch price submissions |
| **Autonom** | 30 – 141 | Off-chain signed batch prices + market session data |
| **Switchboard** | 142 – 255 | On-chain quote account verification |

Switchboard prices are verified entirely on-chain — no off-chain oracle infrastructure dependency. ChaosLabs and Autonom deliver signed price batches that are validated on-chain before use.

---

## Multi-Oracle Consensus

A `MultiOracleConfig` is attached to each pool, controlling how prices from multiple providers are reconciled:

| Parameter | Description |
|-----------|-------------|
| `min_agree` | Minimum number of providers that must agree on a price (1–3) |
| `price_diff_threshold_bps` | Maximum allowed price deviation between providers (100 BPS = 1%) |
| `staleness_seconds` | Maximum age of an accepted price (default: 7 seconds) |

### Default configurations

**Standard (GMX) Pools** — crypto assets:
- Providers order: Switchboard → ChaosLabs → Autonom
- `min_agree`: 2 (two-of-three must agree)
- `price_diff_threshold_bps`: 100

**Autonom Pools** — RWA/synthetic assets:
- Providers order: Autonom → Switchboard → ChaosLabs
- `min_agree`: 1 (single provider sufficient)
- `price_diff_threshold_bps`: 100

---

## Conservative Pricing

To protect the liquidity pool against adverse price selection:

- **Long positions** are priced using the oracle's **lower bound** — the worst case for a long entry/exit
- **Short positions** are priced using the oracle's **upper bound** — the worst case for a short entry/exit

This means traders always transact at the conservative end of the oracle's confidence interval, reducing the pool's exposure to oracle manipulation.

---

## Price Staleness and Timestamp Validation

- Prices older than `staleness_seconds` (7s default) are rejected
- Prices with a timestamp more than **2 seconds in the future** are also rejected (prevents pre-dated manipulation)
- The staleness window is intentionally set to 7 seconds to accommodate legitimate on-chain latency while maintaining a tight replay-attack surface

---

## Switchboard On-Chain Verification

Switchboard prices undergo full on-chain validation:
- Queue matching (feed must be registered to the expected queue)
- Quote account freshness check
- Data format validation

This requires Switchboard quote accounts to be passed as remaining accounts in relevant instructions.

---

## Liquidation Safety Mechanisms

### Asymmetric Liquidation Defense
For pools that temporarily fall back to a single oracle provider, **asymmetric liquidation** is available. When enabled, a liquidation can only proceed if a backup oracle has also provided a recent, confirming price for that asset. This prevents liquidations being triggered by a single stale or manipulated feed.

### Circuit Breaker
When enabled, the circuit breaker **pauses all liquidations** if no backup oracle has delivered a fresh price within the configured window (default: 300 seconds). This is a safety valve for infrastructure outages — protecting traders from being liquidated on stale prices when oracle redundancy is temporarily unavailable.

| Parameter | Description |
|-----------|-------------|
| `asymmetric_liquidation` | Enable/disable asymmetric liquidation defense (0/1) |
| `circuit_breaker_enabled` | Enable/disable the circuit breaker (0/1) |
| `circuit_breaker_seconds` | Freshness window for the backup oracle (seconds) |

Both are enabled by default for GMX pools and disabled for Autonom pools (see [Autonom Pools](autonom-pools.md)).

---

## Oracle Capacity

The oracle account supports up to **50 simultaneous price slots** (expanded from 20 in Release 37). This accommodates the full range of assets across crypto (ChaosLabs/Switchboard) and RWA/synthetic (Autonom) markets.
