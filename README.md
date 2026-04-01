# IRENA Renewable Energy Policy Tracker

Interactive world map + filterable table tracking renewable energy policy and market responses to the 2026 Iran war energy crisis. Built as a static HTML demo on GitHub Pages.

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
| `country` | Country or org name as displayed | `Spain` |
| `iso3` | ISO 3166-1 alpha-3 code; use `INT` for multilateral orgs | `ESP` |
| `region` | One of the valid regions below | `Europe` |
| `policy_name` | Short title of the policy or measure | `RE Grid as Energy Security Shield` |
| `sector` | One of the valid sectors below | `Solar` |
| `policy_type` | One of the valid policy types below | `Existing Capacity` |
| `date` | Free-text date string | `Ongoing March 2026` |
| `quantitative_details` | Key numbers and figures | `60%+ electricity from renewables` |
| `context` | Background quote or explanatory note | `Decades of RE investment now paying off` |

**Valid `region` values:** `Africa` / `Americas` / `Asia-Pacific` / `Europe` / `International` / `Middle East`

**Valid `sector` values:** `Biofuels` / `Conservation` / `Cross-cutting` / `Energy Efficiency` / `Grid / Storage` / `Hydro` / `Nuclear` / `Solar` / `Transport / EVs` / `Wind`

**Valid `policy_type` values:** `Analysis` / `Emergency Measure` / `Existing Capacity` / `Financing / Strategy` / `Incentive` / `Infrastructure` / `Mandate / Regulation` / `Market Response` / `Target / Strategy`

For multilateral organizations (IEA, IRENA, ASEAN, G7 etc.) use `iso3: INT` and `region: International`.

---

## Key files

| File | Role |
|------|------|
| `index.html` | Main tracker — GitHub Pages entry point |
| `data.json` | Policy database — auto-updated by sync workflow, do not edit manually |
| `sync_from_sheets.py` | Fetches the Google Sheet CSV and writes `data.json` |
| `export_to_sheets.py` | One-time script to export `data.json` → CSV for seeding the Sheet |
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
  title="IRENA Renewable Energy Policy Tracker">
</iframe>
```

---

## Google Sheets sync — setup (one-time)

1. Export current data to CSV: `python export_to_sheets.py`
2. Import `policies_for_sheets.csv` into Google Sheets (File → Import → Replace sheet)
3. Publish as CSV: File → Share → Publish to web → Sheet1 → CSV → Publish → copy URL
4. Add as a repo variable: GitHub repo → Settings → Secrets and variables → Variables → New → `SHEETS_CSV_URL`
