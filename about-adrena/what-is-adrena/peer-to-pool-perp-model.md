---
title: "Peer-to-Pool Perp Model (and the risks as a Liquidity Provider)"
source: "https://docs.adrena.trade/about-adrena/what-is-adrena/peer-to-pool-perp-model-and-the-risks-as-a-liquidity-provider"
---

# Peer-to-Pool Perp Model

Adrena uses an Asset Backed (or peer-to-pool) Perp Model (similar to what GMX introduced). This system removes a lot of risks usually present in order-book based Perp DEXs. One can think of this model as a PvE model rather than the usual PvP model, enabled by Liquidity Providers (ALP holders) that provide liquidity to traders to leverage their trades.
## How It Works

In a typical order-book based Perp DEX, when a trader opens a position, the counterparty is another trader betting in the opposite direction. In the asset-backed model, traders' counterparty is themselves and the LP pool (depending on the direction of the trade).

### Long Trades

The user borrows long exposure of the asset based on their leverage from the Liquidity Pool (there is no actual borrowing — the trader locks assets in the pool to gain long exposure).

- **Trader is right** → Trader profits. The Liquidity Pool was deprived of the long exposure that goes to the trader instead. The pool does not lose capital, and accrues fees.
- **Trader is wrong** → Trader eventually gets liquidated on their initial collateral. The locked long exposure is released. The pool accrues fees.

### Short Trades

The user borrows stablecoins from the Liquidity Pool based on the platform's maximum profit (100%). Short positions have a limited upside — that's a limitation/security of this model.

- **Trader is right** → Trader profits. The Liquidity Pool pays out stablecoins to the trader but accrues fees.
- **Trader is wrong** → Trader eventually gets liquidated on their initial collateral. The locked short exposure is released. The pool accrues fees.

## Key Characteristics

- LP revenues originate from fees and trader losses — when a trader is liquidated or closes at a loss, their collateral accrues to the pool
- The model may not be as capital efficient as order-book, but oracle-based pricing makes it popular
- Limited by the size of the Liquidity Pool
- Pool Asset Ratios are an important parameter — maximizing volatile assets while controlling overall long exposure

## Risks for Liquidity Providers

As a Liquidity Provider (ALP holder), you are partially exposed to trader PnL depending on trade direction. The pool's goal is to maximize fee revenue through high trading volume.
