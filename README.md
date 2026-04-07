# IRENA Energy Crisis Transition Tracker (ECTT)

Interactive world map + filterable table tracking national and multilateral responses to the 2026 Iran war energy crisis — renewable energy pivots, electrification accelerations, infrastructure investments, and strategic buffers. Built as a static HTML demo on GitHub Pages, with future integration into IRENA's Sitecore CMS (likely via iframe).

**Live site:** https://nadeemgoussous.github.io/irena-policy-tracker/

---

## Updating the data

Data is managed via **Google Sheets** — the tracker syncs automatically every hour.

1. Open the Google Sheet
2. Add, edit, or delete rows directly
3. The tracker updates within the hour

To trigger an immediate sync: go to the [Actions tab](https://github.com/nadeemgoussous/irena-policy-tracker/actions) → "Sync data from Google Sheets" → **Run workflow**.

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

### Sheet column reference

| Column | Description | Example |
|--------|-------------|---------|
| `ID` | Unique integer — fill in manually, gaps are fine | `42` |
| `Country` | Country or org name as displayed | `S. Korea` |
| `ISO3` | ISO 3166-1 alpha-3 code; use `INT` for multilateral orgs | `KOR` |
| `Region` | One of the valid regions below | `Asia-Pac` |
| `Measure name` | Short title of the policy or measure | `RE acceleration and 100 GW target` |
| `IRENA pillar` | One of the valid pillars below | `Renewable energy` |
| `Technology focus` | Specific technology area | `Solar PV` |
| `Measure type` | One of the valid measure types below | `Target / strategy` |
| `Crisis response typology` | One of the valid typologies below | `Accelerated pivot` |
| `Date` | Free-text date string | `March 2026` |
| `Quantifiable Targets / Capital` | Key numbers, targets, capital figures | `100 GW RE by 2030` |
| `Impact assessment` | Categorical impact label | `Fossil import displacement` |
| `Measure Description` | Objective mechanics of the policy | `Revision of long-term targets…` |
| `Observed / Expected Impact` | Macroeconomic result and geopolitical context | `20% RE in generation by 2030…` |
| `Link` | Link to source report or announcement | `https://…` |

**Valid `Region` values:** `Africa` / `Americas` / `Asia-Pac` / `Europe` / `Intl.` / `MENA`

**Valid `IRENA pillar` values:** `Renewable energy` / `Electrification` / `Energy efficiency` / `Grid & system` / `Analytics`

**Valid `Crisis response typology` values:** `Accelerated pivot` / `Pre-existing buffer` / `Emergency measure`

**Valid `Measure type` values:** `Analytical assessment` / `Emergency measure` / `Fiscal incentive` / `Infrastructure / asset` / `Infrastructure inv.` / `Market response` / `Regulatory mandate` / `Target / strategy`

For multilateral organizations (IEA, IRENA, ASEAN, G7 etc.) use `ISO3: INT` and `Region: Intl.`.

### Deleting a row

Deleting a row from the sheet removes that entry from the tracker on the next sync. The `ID` column should always be filled in manually — gaps are fine, but blanks cause auto-numbering which may produce duplicates.

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

---

## Key files

| File | Role |
|------|------|
| `index.html` | Main tracker — **GitHub Pages entry point and the only file to edit** |
| `data.json` | Policy database — auto-updated by sync workflow, do not edit manually |
| `sync_from_sheets.py` | Fetches the Google Sheet CSV and writes `data.json` |
| `export_to_sheets.py` | Exports `data.json` → CSV for seeding or migrating the Sheet |
| `policies.md` | Source document for current dataset (2026 Iran crisis responses) |
| `world-110m.json` | TopoJSON world map geometry (Natural Earth 110m, do not edit) |
| `.github/workflows/sync-sheets.yml` | GitHub Actions workflow — runs sync every hour |
| `tests/tracker.spec.js` | Playwright test suite |
| `playwright.config.js` | Playwright config — 3 profiles: Desktop Chrome, iPhone 13, Pixel 5 |

---

## Running locally

```bash
python -m http.server 8080
# open http://localhost:8080/index.html
```

Requires a server (not `file://`) because `data.json` and `world-110m.json` are fetched via `fetch()`.

---

## Running tests

```bash
npx playwright test                              # all 3 profiles
npx playwright test --project="Desktop Chrome"   # desktop only
npx playwright test --project="Mobile Chrome (Pixel 5)"
npx playwright show-report                       # open HTML report
```

Tests spin up the Python server automatically (`reuseExistingServer: true`). Requires Playwright browsers: `npx playwright install chromium webkit`.

---

## Deploying changes

```bash
# After editing index.html:
git add index.html
git commit -m "your message"
git push
# GitHub Pages auto-deploys from main branch root (~1 min)
```

---

## UI features

**Table columns:** Country · IRENA Pillar (badge) · Measure Name · Measure Description · Response Typology (badge) · Impact Assessment · Quantifiable Targets / Capital · [ + View Details ]

**Filter dropdowns:** Region · Pillar · Response Typology · Search (full-text: searches country, measure name, pillar, measure type, impact assessment, description, date)

**Map:** D3 choropleth — click a country to filter the table; choropleth shading reflects current filtered counts. IRENA geographic disclaimer shown below map.

**Org panel:** Clickable chip strip below the map for multilateral/regional orgs (`iso3: "INT"` or `"EUU"`) — IEA, IRENA, EU, ASEAN, G7, UNFCCC, Ember, IEEFA

**Row modal:** Structured policy brief — metadata tags (pillar, technology focus, measure type, date), region in subtitle, analytical classification (typology + impact assessment), quantitative call-out box, measure description, observed/expected impact, source link. Region, technology focus, measure type and date are shown only in the modal (not in the table).

---

## Tech stack

- **D3.js v7** — choropleth SVG world map (CDN)
- **TopoJSON** — world map geometry parsing
- **Vanilla JS** — filters, table, pagination, map↔table sync
- **IRENA design system** — palette `#0073AE` / `#00A3E0`, max-width 1316px

---

## Sitecore iframe embed (future)

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
3. Fill in `Crisis response typology` for each row and review auto-mapped `IRENA pillar` values
4. Publish as CSV: File → Share → Publish to web → Sheet1 → CSV → Publish → copy URL
5. Add as a repo variable: GitHub repo → Settings → Secrets and variables → Variables → New → `SHEETS_CSV_URL`
