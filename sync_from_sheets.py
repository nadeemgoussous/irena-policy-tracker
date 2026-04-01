"""
Sync data.json from a published Google Sheet (CSV export).

Usage:
    python sync_from_sheets.py --url "https://docs.google.com/spreadsheets/d/e/PUBLISHED_ID/pub?output=csv"

The sheet must have these columns (row 1 = headers, exact names):
    id | country | iso3 | region | measure_name | pillar | crisis_response_typology | date

Optional columns (read if present, ignored if missing):
    technology_focus | measure_type | quantifiable_targets | impact_assessment |
    measure_description | observed_expected_impact | source_url

Rows with an empty 'country' are skipped.
The top-level 'last_updated' field in data.json is set to today's date automatically.
"""

import argparse
import csv
import json
import io
import sys
import urllib.request
from datetime import date

DATA_FILE = "data.json"

REQUIRED_COLUMNS = [
    "country", "iso3", "region", "measure_name",
    "pillar", "crisis_response_typology", "date"
]


def fetch_csv(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_policies(csv_text):
    reader = csv.DictReader(io.StringIO(csv_text))
    policies = []
    missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
    if missing:
        print(f"ERROR: Sheet is missing columns: {missing}", file=sys.stderr)
        sys.exit(1)

    for i, row in enumerate(reader, start=1):
        if not row.get("country", "").strip():
            continue  # skip empty rows
        policy = {
            "id": int(row["id"]) if row.get("id", "").strip().isdigit() else i,
            "country": row["country"].strip(),
            "iso3": row["iso3"].strip(),
            "region": row["region"].strip(),
            "measure_name": row["measure_name"].strip(),
            "pillar": row["pillar"].strip(),
            "technology_focus": row.get("technology_focus", "").strip(),
            "measure_type": row.get("measure_type", "").strip(),
            "crisis_response_typology": row["crisis_response_typology"].strip(),
            "date": row["date"].strip(),
            "quantifiable_targets": row.get("quantifiable_targets", "").strip(),
            "impact_assessment": row.get("impact_assessment", "").strip(),
            "measure_description": row.get("measure_description", "").strip(),
            "observed_expected_impact": row.get("observed_expected_impact", "").strip(),
            "source_url": row.get("source_url", "").strip(),
        }
        policies.append(policy)
    return policies


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Published Google Sheet CSV URL")
    args = parser.parse_args()

    print(f"Fetching sheet from: {args.url}")
    csv_text = fetch_csv(args.url)

    policies = parse_policies(csv_text)
    print(f"Parsed {len(policies)} policies from sheet")

    output = {
        "last_updated": date.today().isoformat(),
        "policies": policies,
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Written {len(policies)} entries to {DATA_FILE}")


if __name__ == "__main__":
    main()
