# Adrena Docs — Local Clone

A local GitBook-compatible clone of [docs.adrena.trade](https://docs.adrena.trade), structured for editing and syncing back via GitHub → GitBook.

## Structure

```
adrena-docs/
├── .gitbook.yaml               ← GitBook config
├── SUMMARY.md                  ← Table of contents / sidebar
├── README.md                   ← Landing page
├── about-adrena/
│   ├── vision.md
│   ├── README.md               ← What is Adrena?
│   ├── what-is-adrena/
│   │   ├── peer-to-pool-perp-model.md
│   │   ├── no-liquidation-fees.md
│   │   ├── trading-competitions.md
│   │   └── rpc-and-trade-execution.md
│   ├── fees.md
│   ├── trader-profile.md
│   ├── achievements.md
│   ├── mutagen-points-system.md
│   ├── referral-system.md
│   ├── audits.md
│   ├── bug-bounty-program.md
│   ├── useful-links.md
│   └── governance.md
├── tokenomics/
│   ├── tokenomics-overview.md
│   ├── adx.md
│   └── alp/
│       ├── README.md
│       ├── genesis-liquidity.md
│       ├── staked-alp-rewards-emissions-schedule.md
│       └── staking-and-locked-stake-parameters.md
├── technical-documentation/
│   ├── governance-shadow-token.md
│   ├── mrsablier-and-mrsablierstaking.md
│   ├── oracles-and-price-feeds.md
│   ├── toxic-flow-countermeasures.md
│   ├── position-parameters.md
│   ├── sablier-automation-threads.md
│   └── staking-implementation-details.md
├── terms-and-conditions/
│   ├── README.md
│   └── token-terms-and-conditions.md
├── guides/
│   ├── how-to-change-to-devnet-in-phantom-wallet.md
│   ├── how-to-get-devnet-sol.md
│   ├── how-to-get-tokens-to-trade.md
│   └── how-to-open-and-close-a-trade.md
├── reports/
│   ├── 2024-11-21-increase-position-price-miscalculations.md
│   └── 2024-10-22-staking-accounting-issue.md
└── scripts/
    └── fetch-missing-pages.py  ← Run this to fill placeholder pages
```

## Quick Start

### 1. Fill Placeholder Pages

Some pages contain `⚠️` placeholders. Run this script locally to fetch full content:

```bash
pip install requests beautifulsoup4 html2text
python scripts/fetch-missing-pages.py
```

### 2. Edit Locally

Edit any `.md` file with your protocol changes. Pages use standard Markdown with GitBook-flavored extras:

```markdown
{% hint style="info" %}
This is a hint block.
{% endhint %}
```

### 3. Push to GitHub

```bash
git add .
git commit -m "Update: <describe your protocol changes>"
git push origin main
```

### 4. Sync to GitBook

Set up GitHub Sync in your GitBook space:
- Space settings → Configure → GitHub Sync
- Connect to this repository, branch `main`
- Sync direction: **GitHub → GitBook**

Every `git push` will automatically update the live GitBook site.

## Workflow for Protocol Updates

1. Identify which pages are affected by the protocol change
2. Edit the relevant `.md` files
3. Commit with a descriptive message
4. Push → GitBook auto-updates

## GitBook Markdown Tips

| Feature | Syntax |
|---|---|
| Hint/callout | `{% hint style="info" %} ... {% endhint %}` |
| Code block | ` ```language ... ``` ` |
| Embedded link | `{% embed url="https://..." %}` |
| Tabs | `{% tabs %} {% tab title="Name" %} ... {% endtab %} {% endtabs %}` |
