---
title: "Data API"
---

# Data API 📊

The SDK includes a REST client for querying off-chain analytics - position history, pool statistics, leaderboards, oracle prices, and more. This is separate from the on-chain RPC interface.

---

## Setup

Full API reference is available at [datapi.adrena.trade/docs](https://datapi.adrena.trade/docs).

```typescript
import { AdrenaApi } from 'adrena-sdk-ts/adrena-api';

const api = new AdrenaApi(); // defaults to datapi.adrena.trade
```

To point to a custom endpoint:

```typescript
const api = new AdrenaApi('https://your-custom-endpoint.com');
```

---

## Positions

Fetch the position history for a wallet address.

```typescript
const positions = await api.getPositions({
  userWallet: '8xMT...abc',
});
```

---

## Pool Analytics

Query pool-level statistics at various time resolutions.

```typescript
// Latest snapshot
const pool = await api.getPoolInfo();

// Hourly data
const hourly = await api.getHourlyPoolInfo();

// Daily data
const daily = await api.getDailyPoolInfo();
```

---

## Custody Analytics

Per-asset statistics (open interest, utilisation, fees collected).

```typescript
const custody = await api.getCustodyInfo();
const hourlyCustody = await api.getHourlyCustodyInfo();
const dailyCustody = await api.getDailyCustodyInfo();
```

---

## Trader Data

```typescript
// Performance metrics for a single trader
const trader = await api.getTraderInfo('8xMT...abc');

// Trader volume history
const volume = await api.getTraderVolume({ userWallet: '8xMT...abc' });

// Leaderboard
const profiles = await api.getTraderProfiles();
```

---

## Mutagen (Points)

```typescript
// Points for a wallet
const mutagen = await api.getMutagen('8xMT...abc');

// Full leaderboard
const leaderboard = await api.getMutagenLeaderboard();
```

See [Mutagen (Points System)](../about-adrena/mutagen-points-system.md) for details on how points are earned.

---

## Prices

```typescript
// ADX and ALP token prices
const prices = await api.getPrice();

// Latest oracle trading prices for all assets
const tradingPrices = await api.getLastTradingPrices();
```

---

## Available Methods

| Method                    | Description                                      |
|---------------------------|--------------------------------------------------|
| `getPositions(params)`    | Position history for a wallet                    |
| `getPoolInfo(params?)`    | Latest pool statistics                           |
| `getHourlyPoolInfo(params?)` | Hourly pool statistics                        |
| `getDailyPoolInfo(params?)` | Daily pool statistics                          |
| `getCustodyInfo(params?)` | Per-asset custody statistics                     |
| `getHourlyCustodyInfo(params?)` | Hourly custody statistics                  |
| `getDailyCustodyInfo(params?)` | Daily custody statistics                    |
| `getMutagen(userWallet)`  | Mutagen points for a wallet                      |
| `getMutagenLeaderboard(params?)` | Full mutagen leaderboard                  |
| `getTraderInfo(userPubkey)` | Performance metrics for a trader              |
| `getTraderProfiles(params?)` | Trader leaderboard                           |
| `getTraderVolume(params?)` | Volume history for a trader                    |
| `getPrice()`              | Current ADX and ALP token prices                 |
| `getLastTradingPrices()`  | Latest oracle prices for all traded assets       |

---

## Advanced: Building Instructions Manually

Every `core` function is a thin wrapper around an `instructions` builder that then submits via Jito. Use the builders directly when you need to compose custom transactions.

```typescript
import { getOpenLongIxs } from 'adrena-sdk-ts/instructions';
import { sendTransactionWithJito, ADRENA_LOOKUP_TABLE_ADDRESS } from 'adrena-sdk-ts/helpers';
import { createKitClient } from 'adrena-sdk-ts/clients';

const { wallet, rpc } = await createKitClient();

const { ixns, positionAddress } = await getOpenLongIxs(
  wallet,
  'JITOSOL',  // principalToken
  'JITOSOL',  // collateralToken
  10,         // collateralAmount (human-readable)
  3,          // leverage
  rpc,
);

// Prepend/append your own instructions, then send
const txSig = await sendTransactionWithJito(
  ixns,
  wallet,
  rpc,
  false, // simulate only
  true,  // use Jito bundle
  [ADRENA_LOOKUP_TABLE_ADDRESS],
);
```

All liquidity and staking instruction builders follow the same pattern - see `src/instructions/` in the SDK repository for the full set.
