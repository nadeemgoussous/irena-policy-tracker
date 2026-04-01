# IRENA Renewable Energy Policy Tracker

## What this project is
Interactive policy tracker for IRENA — a world map + filterable table showing renewable energy policy and market responses to the 2026 Iran war energy crisis. Built as a static HTML demo hosted on GitHub Pages, with future integration into IRENA's Sitecore CMS (likely via iframe).

**Live site:** https://nadeemgoussous.github.io/irena-policy-tracker/
**GitHub repo:** https://github.com/nadeemgoussous/irena-policy-tracker

## Key files

| File | Role |
|------|------|
| `index.html` | The tracker — **this is the GitHub Pages entry point and the only file to edit** |
| `data.json` | Policy database — **do not edit manually; managed via Google Sheets sync** |
| `sync_from_sheets.py` | Fetches the published Google Sheet CSV and overwrites `data.json` — run by GitHub Actions |
| `export_to_sheets.py` | One-time script to export `data.json` → `policies_for_sheets.csv` for seeding the Google Sheet |
| `policies.md` | Source document for current dataset (2026 Iran crisis responses) |
| `world-110m.json` | TopoJSON world map geometry (Natural Earth 110m, do not edit) |

## Running locally

```bash
cd policy_tracker
python -m http.server 8080
# open http://localhost:8080/index.html
```

Requires a server (not `file://`) because `data.json` and `world-110m.json` are fetched via `fetch()`.

## Deploying changes

```bash
# After editing index.html:
git add index.html
git commit -m "your message"
git push
# GitHub Pages auto-deploys from main branch root (~1 min)
```

## Google Sheets data sync

`data.json` is managed via a Google Sheet. A GitHub Actions workflow (`.github/workflows/sync-sheets.yml`) runs every hour, fetches the sheet as CSV, and commits an updated `data.json` if anything changed.

**Source of truth: the Google Sheet. Do not edit `data.json` directly.**

### How the sync works

1. The sheet is published as CSV via **File → Share → Publish to web**
2. The published CSV URL is stored as a GitHub repo variable (`SHEETS_CSV_URL`)
3. `sync_from_sheets.py` fetches the CSV, converts it to the `data.json` schema, and writes the file
4. The Actions bot commits and pushes if data changed; no commit if nothing changed
5. GitHub Pages picks up the new `data.json` within ~1 min

### Sheet column order (row 1 = headers, exact names required)

```
id | country | iso3 | region | policy_name | sector | policy_type | date | quantitative_details | context | impacts
```

### Adding / editing / deleting entries

Just edit the Google Sheet. The tracker updates within the hour. To trigger immediately: GitHub repo → Actions tab → "Sync data from Google Sheets" → Run workflow.

### Deleting a row

Deleting a row from the sheet removes that entry from the tracker on the next sync. The `id` column should always be filled in manually — gaps are fine, but blanks cause auto-numbering which may produce duplicates.

### Re-seeding the sheet from data.json

```bash
python export_to_sheets.py
# outputs policies_for_sheets.csv — import into Google Sheets
```

### Changing the sync frequency

Edit the cron in `.github/workflows/sync-sheets.yml`:
- Every hour: `"0 * * * *"`
- Every 6 hours: `"0 */6 * * *"`

## Current data schema

Each entry in `data.json`:
```json
{
  "id": 1,
  "country": "Spain",
  "iso3": "ESP",
  "region": "Europe",
  "policy_name": "RE Grid as Energy Security Shield",
  "sector": "Cross-cutting",
  "policy_type": "Existing Capacity",
  "date": "Ongoing March 2026",
  "quantitative_details": "60%+ electricity from renewables; wholesale prices €37–57/MWh",
  "context": "Decades of RE investment now paying off as energy security shield",
  "impacts": "Wholesale electricity prices 3–4× lower than gas-dependent neighbours"
}
```

Valid `region` values: `Africa` / `Americas` / `Asia-Pacific` / `Europe` / `International` / `Middle East`

Valid `sector` values: `Buildings` / `Cross-cutting` / `Industry` / `Power` / `Transport`

Valid `policy_type` values: `Analysis` / `Emergency Measure` / `Existing Capacity` / `Financing / Strategy` / `Incentive` / `Infrastructure` / `Mandate / Regulation` / `Market Response` / `Target / Strategy`

For multilateral organizations (IEA, IRENA, ASEAN, G7 etc.) use `iso3: "INT"` and `region: "International"`.

## UI features (current)

**Table columns:** Country / Org · Region · Policy / Measure (with expandable context) · Sector · Type (colour badge) · Date · Key Details

**Filter dropdowns:** Region · Sector · Policy Type · Search (full-text: searches country, policy name, sector, type, key details, context, date)

**Map:** D3 choropleth — click a country to filter the table; choropleth shading reflects current filtered counts

**Org panel:** Clickable chip strip below the map for multilateral/regional orgs (`iso3: "INT"` or `"EUU"`) that have no map geometry — IEA, IRENA, EU, ASEAN, G7, UNFCCC, Ember, IEEFA

**Context toggle:** Each table row has a `▸ context` button that expands an inline quote/context block

## Tech stack

- **D3.js v7** — choropleth SVG world map (CDN)
- **TopoJSON** — world map geometry parsing
- **Vanilla JS** — filters, table, pagination, map↔table sync
- **IRENA design system** — palette `#003F73` / `#00A3E0`, Graphik font, `l-grid` layout, max-width 1316px

## Sitecore integration path (future)

Embed via iframe when needed:
```html
<iframe src="https://nadeemgoussous.github.io/irena-policy-tracker/" width="100%" height="900px" style="border:none;"></iframe>
```
