"""
Export data.json to a CSV file ready to paste into (or import to) Google Sheets.

Usage:
    python export_to_sheets.py

Outputs:
    policies_for_sheets.csv  — open in Excel/Sheets or File > Import in Google Sheets

Column order matches what sync_from_sheets.py expects:
    id, country, iso3, region, policy_name, sector, policy_type,
    date, quantitative_details, impacts, description, source_url
"""

import csv
import json

DATA_FILE = "data.json"
OUTPUT_FILE = "policies_for_sheets.csv"

COLUMNS = [
    "id", "country", "iso3", "region", "policy_name",
    "sector", "policy_type", "date", "quantitative_details", "impacts",
    "description", "source_url"
]


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    policies = data.get("policies", [])

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        # utf-8-sig adds BOM so Excel opens it correctly without garbling special chars
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(policies)

    print(f"Exported {len(policies)} rows to {OUTPUT_FILE}")
    print()
    print("Next steps:")
    print("  1. Go to your Google Sheet")
    print("  2. File > Import > Upload > select policies_for_sheets.csv")
    print("  3. Choose 'Replace current sheet' and 'No' to convert numbers")
    print("  4. Publish: File > Share > Publish to web > Sheet1 > CSV > Publish")
    print("  5. Copy the published CSV URL")
    print("  6. Add it as a repo variable: GitHub repo > Settings > Secrets and variables")
    print("     > Variables > New repository variable > Name: SHEETS_CSV_URL")


if __name__ == "__main__":
    main()
