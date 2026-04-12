#!/usr/bin/env python3
"""
Adrena Docs - Missing Page Fetcher
===================================
Run this script on your LOCAL machine (not in a restricted sandbox)
to fetch and fill in all placeholder pages.

Usage:
    pip install requests beautifulsoup4 html2text
    python scripts/fetch-missing-pages.py

It will only overwrite pages that contain the ⚠️ placeholder marker.
"""

import os
import re
import time
import requests
import html2text
from bs4 import BeautifulSoup

DOCS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://docs.adrena.trade"

h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = False
h.body_width = 0

def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    return r.text

def extract_content(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove nav/sidebar/chrome
    for tag in soup.select("nav, header, footer, [class*='sidebar'], [class*='toc'], [class*='breadcrumb'], button, [class*='feedback'], [class*='search']"):
        tag.decompose()

    # GitBook renders in main article
    content = None
    for selector in ["main article", "main [class*='page-body']", "article", "main"]:
        content = soup.select_one(selector)
        if content:
            break

    if not content:
        content = soup.body

    title_tag = soup.find("h1") or soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""
    title = re.sub(r"\s*\|\s*Adrena$", "", title)

    md = h.handle(str(content))
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return title, md

def needs_update(filepath):
    if not os.path.exists(filepath):
        return True
    with open(filepath, "r") as f:
        return "⚠️" in f.read()

def update_page(filepath, source_url, title, content):
    frontmatter = f'---\ntitle: "{title}"\nsource: "{source_url}"\n---\n\n'
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)
    print(f"  ✅ Updated: {os.path.relpath(filepath, DOCS_ROOT)}")

# Map of (md file path relative to docs root) -> source URL
PAGE_MAP = {
    "README.md": "/",
    "about-adrena/README.md": "/about-adrena/what-is-adrena",
    "about-adrena/what-is-adrena/trading-competitions.md": "/about-adrena/what-is-adrena/trading-competitions",
    "about-adrena/what-is-adrena/rpc-and-trade-execution.md": "/about-adrena/what-is-adrena/rpc-and-trade-execution",
    "about-adrena/fees.md": "/about-adrena/fees",
    "about-adrena/trader-profile.md": "/about-adrena/trader-profile",
    "about-adrena/achievements.md": "/about-adrena/achievements",
    "about-adrena/referral-system.md": "/about-adrena/referral-system",
    "about-adrena/governance.md": "/about-adrena/governance-need",
    "tokenomics/tokenomics-overview.md": "/tokenomics/tokenomics-overview",
    "tokenomics/adx.md": "/tokenomics/adx",
    "tokenomics/alp/README.md": "/tokenomics/alp",
    "technical-documentation/governance-shadow-token.md": "/technical-documentation/governance-shadow-token",
    "technical-documentation/mrsablier-and-mrsablierstaking.md": "/technical-documentation/mrsablier-and-mrsablierstaking-open-source-keepers",
    "technical-documentation/oracles-and-price-feeds.md": "/technical-documentation/oracles-and-price-feeds",
    "technical-documentation/position-parameters.md": "/technical-documentation/position-parameters",
    "technical-documentation/staking-implementation-details.md": "/technical-documentation/staking-implementation-details",
    "terms-and-conditions/README.md": "/terms-and-conditions",
    "terms-and-conditions/token-terms-and-conditions.md": "/terms-and-conditions/token-terms-and-conditions",
    "guides/how-to-change-to-devnet-in-phantom-wallet.md": "/guides/how-to-change-to-devnet-in-phantom-wallet",
    "guides/how-to-get-devnet-sol.md": "/guides/how-to-get-devnet-sol",
    "guides/how-to-get-tokens-to-trade.md": "/guides/how-to-get-tokens-to-trade",
    "guides/how-to-open-and-close-a-trade.md": "/guides/how-to-open-and-close-a-trade",
    "reports/2024-11-21-increase-position-price-miscalculations.md": "/reports/21-11-2024-be-increase-position-position.price-miscalculations",
    "reports/2024-10-22-staking-accounting-issue.md": "/reports/22-10-2024-upgrade-staking-accounting-issue-causing-extra-reward-distribution",
}

def main():
    print(f"🔍 Checking for placeholder pages in: {DOCS_ROOT}\n")
    updated = 0
    skipped = 0
    failed = []

    for rel_path, url_path in PAGE_MAP.items():
        filepath = os.path.join(DOCS_ROOT, rel_path)
        if not needs_update(filepath):
            skipped += 1
            continue

        url = BASE_URL + url_path
        print(f"  Fetching: {url}")
        try:
            html = fetch_page(url)
            title, content = extract_content(html)
            update_page(filepath, url, title, content)
            updated += 1
            time.sleep(1)
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            failed.append(rel_path)

    print(f"\n{'='*50}")
    print(f"✅ Updated: {updated} | Skipped (already full): {skipped} | Failed: {len(failed)}")
    if failed:
        print("Failed pages:")
        for p in failed:
            print(f"  - {p}")

if __name__ == "__main__":
    main()
