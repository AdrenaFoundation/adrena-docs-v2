---
title: "Commodities"
---

# Commodities ⚗️

The SDK supports synthetic commodity perpetuals through the dedicated commodities pool — trade Gold (XAU), Silver (XAG), and Crude Oil (WTI) against price feeds sourced from Adrena's oracle system.

See [Oracles and Price Feeds](../technical-documentation/oracles-and-price-feeds.md) and [Autonom Pools](../technical-documentation/autonom-pools.md) for the underlying protocol mechanics.

---

## Key Differences from Crypto Trading

- **Collateral is always USDC** — for both longs and shorts, regardless of the commodity
- **`collateralAmount` is in native units** — multiply the human amount by `10^6` (USDC has 6 decimals)
- **Settlement in USDC** — closing a position always returns USDC
- **No token swap** — you deposit USDC and gain synthetic exposure to the price feed; no physical asset is involved

---

## Open a Commodity Long

Go long on a commodity price feed with USDC collateral.

```typescript
import { openCommodityLong } from 'adrena-sdk-ts/core';
import { createKitClient } from 'adrena-sdk-ts/clients';

const { wallet, rpc } = await createKitClient();

// Long Gold with 100 USDC at 5× leverage
const result = await openCommodityLong({
  wallet,
  rpc,
  commodityToken: 'XAU',
  collateralAmount: BigInt(100_000_000), // 100 USDC (6 decimals)
  leverage: 5,
  // price: 2_050,  // optional — override oracle price in USD
});

console.log('tx:', result.txSignature);
console.log('position:', result.positionAddress);
```

The same function handles both opening a new position and increasing an existing one.

---

## Open a Commodity Short

Short a commodity price feed with USDC collateral.

```typescript
import { openCommodityShort } from 'adrena-sdk-ts/core';
import { createKitClient } from 'adrena-sdk-ts/clients';

const { wallet, rpc } = await createKitClient();

// Short Gold with 100 USDC at 5× leverage
const result = await openCommodityShort({
  wallet,
  rpc,
  commodityToken: 'XAU',
  collateralAmount: BigInt(100_000_000), // 100 USDC (6 decimals)
  leverage: 5,
});
```

---

## Close a Commodity Long

Closes the open long position for the given commodity. USDC is returned to the wallet.

```typescript
import { closeCommodityLong } from 'adrena-sdk-ts/core';
import { createKitClient } from 'adrena-sdk-ts/clients';

const { wallet, rpc } = await createKitClient();

const result = await closeCommodityLong({
  wallet,
  rpc,
  commodityToken: 'XAU',
  // price: 2_100,  // optional — override oracle price
});
```

---

## Close a Commodity Short

```typescript
import { closeCommodityShort } from 'adrena-sdk-ts/core';
import { createKitClient } from 'adrena-sdk-ts/clients';

const { wallet, rpc } = await createKitClient();

const result = await closeCommodityShort({
  wallet,
  rpc,
  commodityToken: 'XAU',
});
```

---

## Supported Commodities

| Symbol | Asset     | Oracle feed ID |
|--------|-----------|---------------|
| XAU    | Gold      | 2056          |
| XAG    | Silver    | 2069          |
| WTI    | Crude Oil | 2035          |

All commodity feeds are sourced through the Autonom oracle provider. Prices execute at oracle price with zero slippage, consistent with the broader Adrena protocol.

---

## USDC Decimal Reference

Commodity functions accept `collateralAmount` as a `BigInt` in USDC native units (6 decimals).

| Human amount | Native units (`BigInt`) |
|--------------|------------------------|
| 10 USDC      | `BigInt(10_000_000)`   |
| 100 USDC     | `BigInt(100_000_000)`  |
| 500 USDC     | `BigInt(500_000_000)`  |
| 1,000 USDC   | `BigInt(1_000_000_000)` |
