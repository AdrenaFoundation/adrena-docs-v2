---
title: "Autonom Pools (RWA & Synthetic Assets)"
---

# Autonom Pools (RWA & Synthetic Assets)

## Overview

Autonom Pools are a new pool type in Adrena that enables trading on **real-world assets (RWA)** and **synthetic instruments** — such as equities, commodities, and indices — directly on Solana. Unlike standard GMX-style pools, Autonom pools hold no on-chain token reserves for the traded assets. Instead, positions are entirely USD-denominated and settled against stable collateral.

---

## Differences from Standard (GMX) Pools

| Feature | GMX Pool | Autonom Pool |
|---------|----------|--------------|
| Assets | Native crypto tokens (SOL, BTC, ETH…) | Synthetic: equities, commodities, RWA |
| Custody | Holds actual tokens | No token custody — synthetic PDA only |
| Collateral | Token or stablecoin | Stablecoin only |
| Oracle provider | ChaosLabs / Switchboard consensus | Autonom oracle (primary), others as backup |
| Multi-oracle consensus | Requires 2-of-3 agreement | Requires 1-of-3 agreement |
| Market hours | 24/7 | Subject to underlying market trading hours |
| Position settlement | In underlying token | USD-denominated |

---

## Synthetic Custodies

Each tradable asset in an Autonom Pool is represented by a **synthetic custody** — an on-chain account that records the aggregate open interest and fee state for that asset, but holds no tokens. Key properties:

- Identified by a unique seed (not a token mint), allowing multiple synthetic assets per pool (up to 32)
- Tracks `cumulative_funding_paid_usd` and `cumulative_funding_received_usd` for [Virtual Funding Rate](virtual-funding-rate.md) accounting
- Uses a dedicated `oracle_feed_id` and `trade_oracle_feed_id` for price lookups

---

## Market Hours

Autonom Pool assets correspond to real-world instruments that only trade during certain hours (e.g., US equity market hours, 9:30 AM–4:00 PM ET on weekdays). The protocol enforces this:

- **`market_open_timestamp`** / **`market_close_timestamp`**: Define the active trading window for the pool
- **Opening a position** outside market hours returns a `MarketIsClosed` error
- **Existing positions** remain open through market close — they settle at next open or at the holder's discretion

> **Note:** Closing a position is permitted outside market hours to allow traders to exit risk they cannot actively manage while the market is closed.

---

## Market Special Events

Corporate actions such as **stock splits** and **dividends** can affect the fair value of a synthetic position. When such an event is scheduled:

- Affected feed IDs are recorded in `market_close_affected_feeds`
- The event timestamp is stored in `market_close_event_timestamp`
- Attempts to open new positions in affected assets will return a `MarketStockSpecialEvent` error until the event is processed
- Existing positions in affected assets are handled according to the protocol's event resolution procedure

---

## Oracle Configuration

Autonom Pools use the **Autonom oracle** as the primary price provider. This is an off-chain price feed that delivers signed batch prices (including market session data) on-chain.

Default multi-oracle config for Autonom Pools:

| Parameter | Value |
|-----------|-------|
| Primary provider | Autonom |
| Backup providers | Switchboard, ChaosLabs |
| `min_agree` | 1 (single provider sufficient) |
| `price_diff_threshold_bps` | 100 (1% tolerance) |
| `staleness_seconds` | 7 |
| Asymmetric liquidation | Disabled |
| Circuit breaker | Disabled |

Because Autonom assets may not have broad multi-oracle coverage, a single-oracle consensus threshold is appropriate. The asymmetric liquidation and circuit breaker defenses used in GMX pools are therefore not enabled for Autonom Pools.

See [Oracles and Price Feeds](oracles-and-price-feeds.md) for the full oracle architecture.

---

## Liquidations

Liquidation mechanics for Autonom Pool positions follow the same margin rules as standard positions, with one addition: positions cannot be liquidated outside of market hours (since no reliable price is available). Liquidation resumes at market open.

---

## Collateral

All Autonom Pool positions use stablecoin collateral (USDC or equivalent). There is no token exposure on the collateral side — your profit/loss and collateral are both denominated in USD.
