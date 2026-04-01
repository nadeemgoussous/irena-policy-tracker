# IRENA Energy Crisis Transition Tracker (ECTT)

Interactive world map + filterable table tracking national and multilateral responses to the 2026 Iran war energy crisis — renewable energy pivots, electrification accelerations, infrastructure investments, and strategic buffers. Built as a static HTML demo on GitHub Pages.

**Live site:** https://nadeemgoussous.github.io/irena-policy-tracker/

---

## Updating the data

Data is managed via **Google Sheets** — the tracker syncs automatically every hour.

1. Open the Google Sheet
2. Add, edit, or delete rows directly
3. The tracker updates within the hour

To trigger an immediate sync: go to the [Actions tab](https://github.com/nadeemgoussous/irena-policy-tracker/actions) → "Sync data from Google Sheets" → **Run workflow**.

### Sheet column reference

| Column | Description | Example |
|--------|-------------|---------|
| `id` | Unique integer — fill in manually, gaps are fine | `42` |
| `country` | Country or org name as displayed | `South Korea` |
| `iso3` | ISO 3166-1 alpha-3 code; use `INT` for multilateral orgs | `KOR` |
| `region` | One of the valid regions below | `Asia-Pacific` |
| `measure_name` | Short title of the policy or measure | `100 GW RE Target Acceleration` |
| `pillar` | One of the valid pillars below | `Renewable Energy` |
| `technology_focus` | Specific technology area | `Solar PV` |
| `measure_type` | One of the valid measure types below | `Target / Strategy` |
| `crisis_response_typology` | `Accelerated Pivot` or `Pre-Existing Buffer` | `Accelerated Pivot` |
| `date` | Free-text date string | `March 2026` |
| `quantifiable_targets` | Key numbers, targets, capital figures | `100 GW RE by 2030` |
| `impact_assessment` | Categorical impact label | `Fossil Import Displacement` |
| `measure_description` | Objective mechanics of the policy | `Upward revision of national RE targets…` |
| `observed_expected_impact` | Macroeconomic result and geopolitical context | `Establishes a revised target of 20%…` |
| `source_url` | Link to source report or announcement | `https://…` |

**Valid `region` values:** `Africa` / `Americas` / `Asia-Pacific` / `Europe` / `International` / `Middle East`

**Valid `pillar` values:** `Renewable Energy` / `Electrification` / `Infrastructure` / `Finance & Investment` / `Analysis`

**Valid `crisis_response_typology` values:** `Accelerated Pivot` / `Pre-Existing Buffer`

**Valid `measure_type` values:** `Analysis` / `Emergency Measure` / `Existing Capacity` / `Financing / Strategy` / `Incentive` / `Infrastructure` / `Mandate / Regulation` / `Market Response` / `Target / Strategy`

For multilateral organizations (IEA, IRENA, ASEAN, G7 etc.) use `iso3: INT` and `region: International`.

---

## Key files

| File | Role |
|------|------|
| `index.html` | Main tracker — GitHub Pages entry point |
| `data.json` | Policy database — auto-updated by sync workflow, do not edit manually |
| `sync_from_sheets.py` | Fetches the Google Sheet CSV and writes `data.json` |
| `export_to_sheets.py` | Exports `data.json` → CSV for seeding or migrating the Sheet |
| `.github/workflows/sync-sheets.yml` | GitHub Actions workflow — runs sync every hour |
| `world-110m.json` | TopoJSON world map geometry (do not edit) |

---

## Running locally

```bash
python -m http.server 8080
# open http://localhost:8080/index.html
```

Requires a server (not `file://`) because `data.json` and `world-110m.json` are fetched via `fetch()`.

---

## Sitecore iframe embed

```html
<iframe
  src="https://nadeemgoussous.github.io/irena-policy-tracker/"
  width="100%"
  height="900px"
  style="border:none;"
  title="IRENA Energy Crisis Transition Tracker">
</iframe>
```

---

## Google Sheets sync — setup (one-time)

1. Export current data to CSV: `python export_to_sheets.py`
2. Import `policies_for_sheets.csv` into Google Sheets (File → Import → Replace sheet)
3. Fill in `crisis_response_typology` for each row and review auto-mapped `pillar` values
4. Publish as CSV: File → Share → Publish to web → Sheet1 → CSV → Publish → copy URL
5. Add as a repo variable: GitHub repo → Settings → Secrets and variables → Variables → New → `SHEETS_CSV_URL`
