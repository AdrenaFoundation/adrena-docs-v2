---
title: "Trading"
---

# Trading 📈

The SDK supports market orders, limit orders, and stop-loss / take-profit management for crypto perpetuals on the main pool. All functions return a `txSignature` and (where applicable) a `positionAddress`.

For synthetic commodity trading (XAU, XAG, WTI) see [Commodities](commodities.md).

---

## Open a Long Position

For longs the `collateralToken` must match the `principalToken` - you deposit the asset you are trading.

```typescript
import { openMarketLong } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';

const { wallet, rpc } = await createKitClient();

const result = await openMarketLong({
  wallet,
  rpc,
  principalToken: 'JITOSOL',   // asset to trade
  collateralToken: 'JITOSOL',  // must match principal for longs
  collateralAmount: 10,         // human-readable units (10 JITOSOL)
  leverage: 3,                  // leverage multiplier
  stopLossPrice: 130,           // optional - trigger price in USD
  takeProfitPrice: 180,         // optional - trigger price in USD
});

console.log('tx:', result.txSignature);
console.log('position:', result.positionAddress);
```

---

## Open a Short Position

For shorts the `collateralToken` must be `"USDC"` regardless of which asset is being shorted.

```typescript
import { openMarketShort } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';

const { wallet, rpc } = await createKitClient();

const result = await openMarketShort({
  wallet,
  rpc,
  principalToken: 'JITOSOL',  // asset to short
  collateralToken: 'USDC',    // must be USDC for shorts
  collateralAmount: 50,        // 50 USDC
  leverage: 5,
  stopLossPrice: 175,          // optional - above entry price for shorts
  takeProfitPrice: 120,        // optional - below entry price for shorts
});
```

---

## Close a Long Position

Closes the existing long position for the given principal token. Defaults to the current oracle price.

```typescript
import { closeLong } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';

const { wallet, rpc } = await createKitClient();

const result = await closeLong({
  wallet,
  rpc,
  principalToken: 'JITOSOL',
  // price: 155.0,  // optional - override close price
});
```

---

## Close a Short Position

```typescript
import { closeShort } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';

const { wallet, rpc } = await createKitClient();

const result = await closeShort({
  wallet,
  rpc,
  principalToken: 'JITOSOL',
  collateralToken: 'USDC',
});
```

---

## Check Position Status

Fetch live P&L, size, liquidation price, and other position metrics.

```typescript
import { getPositionStatus } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';
import {
  fetchPoolUtil,
  loadCustodies,
  getCustodyByMint,
  findPositionAddress,
  PRINCIPAL_ADDRESSES,
} from 'adrena-sdk/helpers';

const { wallet, rpc } = await createKitClient();

const principalToken = 'JITOSOL';
const side = 'long'; // or 'short'

// Derive the on-chain position address
const pool = await fetchPoolUtil('main-pool', undefined, rpc);
const custodies = await loadCustodies(pool.data, rpc);
const principalCustody = getCustodyByMint(
  custodies,
  PRINCIPAL_ADDRESSES[principalToken].address,
);

const positionAddress = (
  await findPositionAddress(pool.address, wallet.address, principalCustody!.address, side)
)[0];

const status = await getPositionStatus({ wallet, rpc, principalToken, positionAddress });

console.log(status);
// { pnl, sizeUsd, entryPrice, pythPrice, exitFee, totalInterest, liquidationPrice, ... }
```

### Returned fields

| Field           | Description                                      |
|-----------------|--------------------------------------------------|
| `entryPrice`    | Price at which the position was opened (USD)     |
| `pythPrice`     | Current oracle price (USD)                       |
| `sizeUsd`       | Notional position size in USD                    |
| `totalInterest` | Accumulated borrow interest owed                 |
| `exitFee`       | Fee charged on close                             |
| `preFeePnl`     | P&L before fees                                  |
| `pnl`           | Net P&L after fees                               |
| `openTime`      | Timestamp when the position was opened           |
| `updateTime`    | Timestamp of the most recent position update     |

---

## Limit Orders

Place a conditional order that fills when the oracle price reaches a target level.

```typescript
import { addLimitOrder } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';

const { wallet, rpc } = await createKitClient();

const result = await addLimitOrder({
  wallet,
  rpc,
  principalToken: 'JITOSOL',
  collateralToken: 'JITOSOL', // matches principal for long; USDC for short
  collateralAmount: 0.5,
  leverage: 10,
  side: 'long',
  triggerPrice: 130,   // order fills when oracle price reaches this level
  limitPrice: null,    // null = market price at fill; set a value to cap fill price
});
```

---

## Cancel Stop Loss / Take Profit

Cancels an existing stop-loss and/or take-profit attached to an open position.

```typescript
import { cancelSLTP } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';

const { wallet, rpc } = await createKitClient();

const result = await cancelSLTP(
  wallet,
  rpc,
  'JITOSOL', // principalToken
  'long',    // side
  true,      // cancelStopLoss
  true,      // cancelTakeProfit
);
```

---

## Confirming Transactions

All core functions submit transactions via Jito bundles. Use `checkTransactionConfirmed` to poll for on-chain confirmation:

```typescript
import { checkTransactionConfirmed } from 'adrena-sdk/helpers';

const result = await openMarketLong({ ... });

const confirmed = await checkTransactionConfirmed(result.txSignature, rpc);
if (confirmed) {
  console.log('Position opened:', result.positionAddress);
} else {
  console.warn('Transaction did not confirm within timeout');
}
```

If the Jito tip endpoint is unreachable the SDK falls back to a standard RPC send automatically.
