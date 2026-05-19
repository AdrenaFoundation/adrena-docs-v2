---
title: "TypeScript SDK"
---

# TypeScript SDK 🛠️

The Adrena TypeScript SDK provides a high-level interface for interacting with the Adrena Protocol on Solana - opening and closing perpetual positions, managing liquidity, staking tokens, and querying off-chain analytics.

Built on [@solana/kit](https://github.com/anza-xyz/kit) (Web3.js v2). All transactions are submitted via [Jito bundles](https://www.jito.network/) for MEV protection.

---

## Installation

```bash
# npm
npm install adrena-sdk-ts@beta

# yarn
yarn add adrena-sdk-ts@beta
```

---

## Configuration

All SDK functions require a `wallet` (transaction signer) and an `rpc` client. Use `createKitClient` to create both.

### Option 1 - `.env` file (recommended)

Create a `.env` file in your project root:

```env
PRIVATE_KEY_STR=<your-base58-private-key>
RPC_URL=https://your-rpc-url.com
WS_URL=wss://your-ws-url.com
```

> Never commit private keys. Add `.env` to your `.gitignore`.

Then in code:

```typescript
import { createKitClient } from 'adrena-sdk-ts/clients';

const { wallet, rpc } = await createKitClient();
```

### Option 2 - Pass credentials directly

```typescript
import { createKitClient } from 'adrena-sdk-ts/clients';

const { wallet, rpc } = await createKitClient({
  privateKey: 'your-base58-private-key',
  rpcUrl: 'https://your-rpc-url.com',
});
```

---

## Supported Assets

Adrena runs two separate on-chain pools. The SDK exposes both.

### Main Pool - Crypto Assets

| Symbol  | Role                     | Decimals |
|---------|--------------------------|----------|
| JITOSOL | Principal / Collateral   | 9        |
| WBTC    | Principal / Collateral   | 8        |
| BONK    | Principal / Collateral   | 5        |
| USDC    | Collateral / Liquidity   | 6        |

**`PrincipalToken`** - the asset being traded: `"JITOSOL" | "WBTC" | "BONK"`

**`CollateralToken`** - the asset deposited as margin: `"USDC" | "JITOSOL" | "WBTC" | "BONK"`

> For **longs**, the collateral token must match the principal token (e.g. a JITOSOL long requires JITOSOL collateral).
> For **shorts**, the collateral token must always be `"USDC"`.

### Commodities Pool - Synthetic Assets

| Symbol | Name      | Decimals |
|--------|-----------|----------|
| XAU    | Gold      | 6        |
| XAG    | Silver    | 6        |
| WTI    | Crude Oil | 6        |

**`CommodityToken`** - `"XAU" | "XAG" | "WTI"`

Commodity positions are collateralised in USDC for both longs and shorts. There is no token swap - you deposit USDC and trade a price-feed-backed synthetic custody settled in USDC on close.

---

## Module Overview

The SDK is split into focused sub-packages. Import only what you need.

| Import path                | Purpose                                              |
|----------------------------|------------------------------------------------------|
| `adrena-sdk-ts/clients`    | Create the RPC + wallet client (`createKitClient`)   |
| `adrena-sdk-ts/core`       | High-level trading, liquidity, and staking functions |
| `adrena-sdk-ts/instructions` | Low-level instruction builders for custom transactions |
| `adrena-sdk-ts/helpers`    | PDAs, math, token accounts, transaction utilities    |
| `adrena-sdk-ts/adrena-api` | REST API client for off-chain data and analytics     |

---

## Sections

- [Trading](trading.md)
- [Commodities](commodities.md)
- [Liquidity & Swap](liquidity-and-swap.md)
- [Staking](staking.md)
- [Data API](data-api.md)
