"""
CTRI Clinical Trials Scraper (via WHO ICTRP)
=============================================
Searches the WHO ICTRP portal for Clinical Trials Registry - India (CTRI)
trials matching a keyword, and saves results to a CSV file.

Run locally:   python scraper.py --keyword "diabetes"
GitHub Actions: keyword comes from the workflow input
"""

import argparse
import csv
import os
import time
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ── Constants ─────────────────────────────────────────────────────────────────
BASE_URL    = "https://trialsearch.who.int/"
SEARCH_URL  = "https://trialsearch.who.int/AdvSearch.aspx"
HEADERS     = {
    "User-Agent": "Mozilla/5.0 (compatible; research-scraper/1.0)"
}

# ── Scraper ───────────────────────────────────────────────────────────────────

def get_viewstate(session: requests.Session) -> dict:
    """Fetch the ICTRP advanced search page and extract ASP.NET hidden fields."""
    print("  → Fetching search page...")
    resp = session.get(SEARCH_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    fields = {}
    for hidden in soup.find_all("input", type="hidden"):
        name = hidden.get("name", "")
        if name:
            fields[name] = hidden.get("value", "")
    return fields


def run_search(session: requests.Session, keyword: str) -> requests.Response:
    """Submit the ICTRP advanced search form for the given keyword, filtered to CTRI."""
    print(f"  → Submitting search for: '{keyword}' ...")

    hidden = get_viewstate(session)

    # Build the POST payload — mirrors the ICTRP Advanced Search form
    payload = {
        **hidden,
        "ctl00$ContentPlaceHolder1$txtTitle":       keyword,   # 'Title' field
        "ctl00$ContentPlaceHolder1$txtCondition":   "",
        "ctl00$ContentPlaceHolder1$txtIntervention":"",
        "ctl00$ContentPlaceHolder1$txtPrimarySpons":"",
        "ctl00$ContentPlaceHolder1$txtPI":          "",
        "ctl00$ContentPlaceHolder1$ddlRecruitStatus":"",       # all statuses
        "ctl00$ContentPlaceHolder1$ddlCountry":     "",
        "ctl00$ContentPlaceHolder1$ddlPhase":       "",
        # Filter to CTRI only
        "ctl00$ContentPlaceHolder1$ddlRegistry":    "CTRI",
        "ctl00$ContentPlaceHolder1$BtnSearch":      "Search",
        "__EVENTTARGET":   "",
        "__EVENTARGUMENT": "",
    }

    resp = session.post(SEARCH_URL, data=payload, headers={
        **HEADERS,
        "Referer": SEARCH_URL,
        "Content-Type": "application/x-www-form-urlencoded",
    }, timeout=60)
    resp.raise_for_status()
    return resp


def parse_results(html: str, keyword: str) -> list[dict]:
    """Parse the search results page and extract trial information."""
    soup = BeautifulSoup(html, "html.parser")
    trials = []

    # ICTRP results are in a table with class 'ResultsTable' or similar
    # Try multiple possible table selectors
    results_table = (
        soup.find("table", {"id": lambda x: x and "Grid" in x}) or
        soup.find("table", {"class": lambda x: x and "result" in str(x).lower()}) or
        soup.find("table", {"summary": lambda x: x and "trial" in str(x).lower()}) or
        soup.find("table", {"id": "ctl00_ContentPlaceHolder1_gvRecords"})
    )

    if not results_table:
        # Fallback: look for any data table with multiple rows
        all_tables = soup.find_all("table")
        for t in all_tables:
            rows = t.find_all("tr")
            if len(rows) > 2:
                results_table = t
                break

    if not results_table:
        print("  ⚠  Could not find results table in page.")
        # Save raw HTML for debugging
        Path("debug_output.html").write_text(html, encoding="utf-8")
        print("     Raw HTML saved to debug_output.html for inspection.")
        return []

    rows = results_table.find_all("tr")
    headers = []

    for i, row in enumerate(rows):
        cells = row.find_all(["th", "td"])
        text  = [c.get_text(strip=True) for c in cells]

        if i == 0:  # Header row
            headers = text
            continue

        if not any(text):   # Skip empty rows
            continue

        # Build a dict from headers + values
        if headers and len(text) == len(headers):
            trial = dict(zip(headers, text))
        else:
            # Fallback: use positional keys
            trial = {f"col_{j}": v for j, v in enumerate(text)}

        # Add metadata
        trial["search_keyword"]  = keyword
        trial["scraped_at"]      = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        trial["source_registry"] = "CTRI (via WHO ICTRP)"
        trials.append(trial)

    return trials


def save_to_csv(trials: list[dict], keyword: str, output_dir: str = "results") -> str:
    """Save the list of trial dicts to a CSV file."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    safe_keyword = keyword.replace(" ", "_").replace("/", "-")[:50]
    timestamp    = datetime.utcnow().strftime("%Y%m%d_%H%M")
    filename     = f"{output_dir}/ctri_{safe_keyword}_{timestamp}.csv"

    if not trials:
        print("  ⚠  No trials to save.")
        return ""

    all_keys = list(trials[0].keys())

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(trials)

    return filename


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Scrape CTRI trials from WHO ICTRP")
    parser.add_argument(
        "--keyword", "-k",
        required=True,
        help='Search keyword, e.g. "diabetes" or "hypertension"'
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="results",
        help="Folder to save CSV results (default: results/)"
    )
    args = parser.parse_args()

    keyword = args.keyword.strip()
    print(f"\n🔍  CTRI Scraper — keyword: '{keyword}'")
    print("=" * 50)

    session = requests.Session()

    try:
        response = run_search(session, keyword)
    except requests.RequestException as e:
        print(f"\n❌  Network error: {e}")
        sys.exit(1)

    print("  → Parsing results...")
    trials = parse_results(response.text, keyword)

    if trials:
        print(f"  ✅  Found {len(trials)} trial(s).")
        csv_path = save_to_csv(trials, keyword, args.output_dir)
        if csv_path:
            print(f"  💾  Saved → {csv_path}")
    else:
        print("  ⚠  No results found. Try a different keyword.")

    print("\nDone.\n")
    return len(trials)


if __name__ == "__main__":
    main()
