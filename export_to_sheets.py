"""
Export data.json to a CSV file ready to paste into (or import to) Google Sheets.

Usage:
    python export_to_sheets.py

Outputs:
    policies_for_sheets.csv  — open in Excel/Sheets or File > Import in Google Sheets

Column order matches what sync_from_sheets.py expects:
    ID, Country, ISO3, Region, IRENA pillar, Measure name,
    Measure Description, Technology focus, Measure type,
    Crisis response typology, Impact assessment,
    Quantifiable Targets / Capital, Date,
    Observed / Expected Impact, Link

NOTE: This script migrates old-schema data.json fields to the new ECTT schema.
      New fields (pillar, crisis_response_typology, impact_assessment, etc.) are
      populated with placeholder values — fill them in Google Sheets before syncing.
"""

import csv
import json

DATA_FILE = "data.json"
OUTPUT_FILE = "policies_for_sheets.csv"

COLUMNS = [
    "ID", "Country", "ISO3", "Region",
    "IRENA pillar", "Measure name", "Measure Description",
    "Technology focus", "Measure type", "Crisis response typology",
    "Impact assessment", "Quantifiable Targets / Capital", "Date",
    "Observed / Expected Impact", "Link"
]

# Best-effort mapping from old sector values to new Pillar values.
# These are approximate — review and correct in Google Sheets.
SECTOR_TO_PILLAR = {
    "Power":        "Renewable Energy",
    "Transport":    "Electrification",
    "Buildings":    "Electrification",
    "Industry":     "Infrastructure",
    "Cross-cutting":"Renewable Energy",
}


def migrate(p):
    """Map a data.json policy record to the Google Sheet column names."""
    return {
        "ID":                             p.get("id", ""),
        "Country":                        p.get("country", ""),
        "ISO3":                           p.get("iso3", ""),
        "Region":                         p.get("region", ""),
        "IRENA pillar":                   p.get("pillar") or SECTOR_TO_PILLAR.get(p.get("sector", ""), ""),
        "Measure name":                   p.get("measure_name") or p.get("policy_name", ""),
        "Measure Description":            p.get("measure_description") or p.get("description", ""),
        "Technology focus":               p.get("technology_focus", ""),
        "Measure type":                   p.get("measure_type") or p.get("policy_type", ""),
        "Crisis response typology":       p.get("crisis_response_typology", ""),
        "Impact assessment":              p.get("impact_assessment", ""),
        "Quantifiable Targets / Capital":  p.get("quantifiable_targets") or p.get("quantitative_details", ""),
        "Date":                           p.get("date", ""),
        "Observed / Expected Impact":     p.get("observed_expected_impact") or p.get("impacts", ""),
        "Link":                           p.get("source_url", ""),
    }


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    policies = data.get("policies", [])
    rows = [migrate(p) for p in policies]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        # utf-8-sig adds BOM so Excel opens it correctly without garbling special chars
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    empty_pillar = sum(1 for r in rows if not r["IRENA pillar"])
    empty_typology = sum(1 for r in rows if not r["Crisis response typology"])

    print(f"Exported {len(rows)} rows to {OUTPUT_FILE}")
    print()
    if empty_pillar:
        print(f"  WARNING: {empty_pillar} rows have no Pillar value -- fill in Google Sheets")
    if empty_typology:
        print(f"  WARNING: {empty_typology} rows need a Crisis Response Typology (Accelerated Pivot / Pre-Existing Buffer)")
    print()
    print("Next steps:")
    print("  1. Go to your Google Sheet")
    print("  2. File > Import > Upload > select policies_for_sheets.csv")
    print("  3. Choose 'Replace current sheet' and 'No' to convert numbers")
    print("  4. Fill in 'crisis_response_typology' and review 'pillar' for each row")
    print("  5. Publish: File > Share > Publish to web > Sheet1 > CSV > Publish")
    print("  6. Copy the published CSV URL and set it as the SHEETS_CSV_URL repo variable")


if __name__ == "__main__":
    main()
