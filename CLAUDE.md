# IRENA Energy Crisis Transition Tracker (ECTT)

## What this project is
Interactive policy tracker for IRENA — a world map + filterable table tracking national and multilateral responses to the 2026 Iran war energy crisis. Built as a static HTML demo hosted on GitHub Pages, with future integration into IRENA's Sitecore CMS (likely via iframe).

**Live site:** https://nadeemgoussous.github.io/irena-policy-tracker/
**GitHub repo:** https://github.com/nadeemgoussous/irena-policy-tracker

## Key files

| File | Role |
|------|------|
| `index.html` | The tracker — **this is the GitHub Pages entry point and the only file to edit** |
| `data.json` | Policy database — **do not edit manually; managed via Google Sheets sync** |
| `sync_from_sheets.py` | Fetches the published Google Sheet CSV and overwrites `data.json` — run by GitHub Actions |
| `export_to_sheets.py` | Exports `data.json` → `policies_for_sheets.csv` for seeding/migrating the Google Sheet |
| `policies.md` | Source document for current dataset (2026 Iran crisis responses) |
| `world-110m.json` | TopoJSON world map geometry (Natural Earth 110m, do not edit) |
| `tests/tracker.spec.js` | Playwright test suite — 39 tests across 9 suites |
| `playwright.config.js` | Playwright config — 3 profiles: Desktop Chrome, iPhone 13, Pixel 5 |

## Running locally

```bash
cd policy_tracker
python -m http.server 8080
# open http://localhost:8080/index.html
```

Requires a server (not `file://`) because `data.json` and `world-110m.json` are fetched via `fetch()`.

## Running tests

```bash
npx playwright test                        # all 3 profiles
npx playwright test --project="Desktop Chrome"   # desktop only
npx playwright test --project="Mobile Chrome (Pixel 5)"
npx playwright show-report                 # open HTML report
```

Tests spin up the Python server automatically (`reuseExistingServer: true`). Requires Playwright browsers: `npx playwright install chromium webkit`.

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
ID | Country | ISO3 | Region | IRENA pillar | Measure name | Measure Description | Technology focus | Measure type | Crisis response typology | Impact assessment | Quantifiable Targets / Capital | Date | Observed / Expected Impact | Link
```

### Adding / editing / deleting entries

Just edit the Google Sheet. The tracker updates within the hour. To trigger immediately: GitHub repo → Actions tab → "Sync data from Google Sheets" → Run workflow.

### Deleting a row

Deleting a row from the sheet removes that entry from the tracker on the next sync. The `id` column should always be filled in manually — gaps are fine, but blanks cause auto-numbering which may produce duplicates.

### Re-seeding the sheet from data.json

```bash
python export_to_sheets.py
# outputs policies_for_sheets.csv — import into Google Sheets
# script warns on rows missing pillar or crisis_response_typology
```

### Changing the sync frequency

Edit the cron in `.github/workflows/sync-sheets.yml`:
- Every hour: `"0 * * * *"`
- Every 6 hours: `"0 */6 * * *"`

## Current data schema

Each entry in `data.json`:
```json
{
  "id": 24,
  "country": "S. Korea",
  "iso3": "KOR",
  "region": "Asia-Pac",
  "measure_name": "RE acceleration and 100 GW target",
  "pillar": "Renewable energy",
  "technology_focus": "Broad RE",
  "measure_type": "Target / strategy",
  "crisis_response_typology": "Accelerated pivot",
  "date": "",
  "quantifiable_targets": "100 GW RE by 2030",
  "impact_assessment": "Fossil import displacement",
  "measure_description": "Revision of long-term targets and local distance regulations.",
  "observed_expected_impact": "20% RE in generation by 2030; legislative reform removing local distance restrictions on solar; grid innovation plan within 6 months.",
  "source_url": "https://..."
}
```

Valid `region` values: `Africa` / `Americas` / `Asia-Pac` / `Europe` / `Intl.` / `MENA`

Valid `pillar` values: `Renewable energy` / `Electrification` / `Energy efficiency` / `Grid & system` / `Analytics`

Valid `crisis_response_typology` values: `Accelerated pivot` / `Pre-existing buffer` / `Emergency measure`

Valid `measure_type` values: `Analytical assessment` / `Emergency measure` / `Fiscal incentive` / `Infrastructure / asset` / `Infrastructure inv.` / `Market response` / `Regulatory mandate` / `Target / strategy`

For multilateral organizations (IEA, IRENA, ASEAN, G7 etc.) use `iso3: "INT"` and `region: "Intl."`.

## UI features (current)

**Table columns:** Country · IRENA Pillar (badge) · Measure Name · Measure Description · Response Typology (badge) · Impact Assessment · Quantifiable Targets / Capital · [ + View Details ]

**Filter dropdowns:** Region · Pillar · Response Typology · Search (full-text: searches country, measure name, pillar, measure type, impact assessment, description, date)

**Map:** D3 choropleth — click a country to filter the table; choropleth shading reflects current filtered counts. IRENA geographic disclaimer shown below map.

**Org panel:** Clickable chip strip below the map for multilateral/regional orgs (`iso3: "INT"` or `"EUU"`) — IEA, IRENA, EU, ASEAN, G7, UNFCCC, Ember, IEEFA

**Row modal:** Structured policy brief — metadata tags (pillar, technology focus, measure type, date), analytical classification (typology + impact assessment), quantitative call-out box, measure description, observed/expected impact, source link.

## Tech stack

- **D3.js v7** — choropleth SVG world map (CDN)
- **TopoJSON** — world map geometry parsing
- **Vanilla JS** — filters, table, pagination, map↔table sync
- **IRENA design system** — palette `#0073AE` / `#00A3E0`, max-width 1316px

## Sitecore integration path (future)

Embed via iframe when needed:
```html
<iframe src="https://nadeemgoussous.github.io/irena-policy-tracker/" width="100%" height="900px" style="border:none;"></iframe>
```
