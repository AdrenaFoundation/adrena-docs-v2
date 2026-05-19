---
title: "Staking"
---

# Staking 🔒

ADX and ALP tokens can both be staked to earn protocol fee distributions in USDC plus ADX emissions. The SDK supports liquid staking (no lock-up) and locked staking (fixed duration with boosted rewards).

See [Staking Implementation Details](../technical-documentation/staking-implementation-details.md) for protocol-level mechanics.

---

## Staking Types

All staking functions accept a `stakingType` parameter:

| Value | Token |
|-------|-------|
| `1`   | ADX   |
| `2`   | ALP   |

---

## Liquid Staking

Liquid stakes have no lock-up period. You can unstake at any time.

### Add Liquid Stake

```typescript
import { addLiquidStake } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';

const { wallet, rpc } = await createKitClient();

// Stake 100 ADX (6 decimals)
await addLiquidStake({
  wallet,
  rpc,
  stakingType: 1,               // 1 = ADX, 2 = ALP
  amount: BigInt(100_000_000),  // 100 ADX in native units
});
```

### Remove Liquid Stake

```typescript
import { removeLiquidStake } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';

const { wallet, rpc } = await createKitClient();

await removeLiquidStake({
  wallet,
  rpc,
  stakingType: 1,
  amount: BigInt(100_000_000),
});
```

---

## Locked Staking

Lock a stake for a fixed duration to earn boosted rewards. Longer durations provide a higher multiplier.

### Add Locked Stake

```typescript
import { addLockedStake } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';

const { wallet, rpc } = await createKitClient();

// Lock 500 ADX for 90 days
await addLockedStake({
  wallet,
  rpc,
  stakingType: 1,
  amount: BigInt(500_000_000), // 500 ADX in native units
  lockedDays: 90,
});
```

### Supported lock durations

`7` · `30` · `60` · `90` · `180` · `360` · `540` · `720` days

---

## Remove Locked Stake

After the lock period expires, withdraw by providing the index of the lock in the `UserStaking` account (zero-based).

```typescript
import { removeLockedStake } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';

const { wallet, rpc } = await createKitClient();

await removeLockedStake({
  wallet,
  rpc,
  stakingType: 1,
  lockedStakeIndex: 0, // 0-based index in the UserStaking account
});
```

---

## Claim Staking Rewards

Claims all pending USDC fee rewards and ADX emissions for the given staking type.

```typescript
import { claimStakes } from 'adrena-sdk/core';
import { createKitClient } from 'adrena-sdk/clients';

const { wallet, rpc } = await createKitClient();

// Claim ADX staking rewards
await claimStakes({ wallet, rpc, stakingType: 1 });

// Claim ALP staking rewards
await claimStakes({ wallet, rpc, stakingType: 2 });
```
