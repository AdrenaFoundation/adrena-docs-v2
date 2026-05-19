---
title: "Liquidity & Swap"
---

# Liquidity & Swap 💧

Liquidity providers deposit collateral into the ALP pool and receive ALP tokens representing their share. The pool earns trading fees distributed to ALP holders. The SDK also supports token swaps directly through the pool.

See [ALP](../tokenomics/alp/README.md) for tokenomics details.

---

## Add Liquidity (ALP)

Deposit a supported collateral token to receive ALP in return. Amounts are expressed in native token units.

```typescript
import { addLiquidity } from 'adrena-sdk-ts/core';
import { createKitClient } from 'adrena-sdk-ts/clients';

const { wallet, rpc } = await createKitClient();

const result = await addLiquidity({
  wallet,
  rpc,
  collateralToken: 'USDC',
  amountIn: BigInt(100_000_000),  // 100 USDC (6 decimals)
  minLpAmountOut: BigInt(0),      // minimum ALP to receive; set >0 for slippage protection
});
```

To deposit into the commodities pool instead of the main pool, pass `poolName: 'commodities-pool'`:

```typescript
await addLiquidity({
  wallet,
  rpc,
  collateralToken: 'USDC',
  amountIn: BigInt(100_000_000),
  minLpAmountOut: BigInt(0),
  poolName: 'commodities-pool',
});
```

---

## Remove Liquidity (ALP)

Burn ALP tokens to withdraw a collateral token from the pool.

```typescript
import { removeLiquidity } from 'adrena-sdk-ts/core';
import { createKitClient } from 'adrena-sdk-ts/clients';

const { wallet, rpc } = await createKitClient();

const result = await removeLiquidity({
  wallet,
  rpc,
  collateralToken: 'USDC',       // token to receive on exit
  lpAmountIn: BigInt(50_000_000), // ALP tokens to burn (6 decimals)
  minAmountOut: BigInt(0),        // minimum collateral to receive
});
```

---

## Swap

Swap between any two supported collateral tokens through the ALP pool.

```typescript
import { swap } from 'adrena-sdk-ts/core';
import { createKitClient } from 'adrena-sdk-ts/clients';

const { wallet, rpc } = await createKitClient();

const result = await swap({
  wallet,
  rpc,
  fromToken: 'USDC',
  toToken: 'JITOSOL',
  amountIn: BigInt(50_000_000),  // 50 USDC (6 decimals)
  minAmountOut: BigInt(0),       // set >0 for slippage protection
});
```

Swaps execute through the pool's internal price oracle - the same zero-slippage mechanism used for trades.

---

## Token Decimal Reference

Native unit amounts are required for liquidity and swap functions. Use the table below to convert human-readable amounts.

| Token   | Decimals | Formula                              |
|---------|----------|--------------------------------------|
| USDC    | 6        | `amount * 10^6` (e.g. `100 * 1e6`)  |
| ALP     | 6        | `amount * 10^6`                      |
| JITOSOL | 9        | `amount * 10^9`                      |
| WBTC    | 8        | `amount * 10^8`                      |
| BONK    | 5        | `amount * 10^5`                      |

---

## Slippage Protection

Set `minLpAmountOut` / `minAmountOut` to a non-zero value to reject the transaction if the pool price moves adversely between submission and execution.

A value of `BigInt(0)` disables the check - acceptable for testing but not recommended in production.
