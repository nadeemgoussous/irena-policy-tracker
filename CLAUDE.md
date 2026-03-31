# IRENA Renewable Energy Policy Tracker

## What this project is
Interactive policy tracker for IRENA — a world map + filterable table showing renewable energy policies by country. Built as a static HTML demo to be hosted on GitHub Pages, with future integration into IRENA's Sitecore CMS (likely via iframe).

## Key files

| File | Role |
|------|------|
| `index.html` | Standalone tracker (own header/footer, for GitHub Pages / iframe) |
| `irena_policy_tracker.html` | Tracker embedded inside the real IRENA site template |
| `build_tracker.py` | Script that generates `irena_policy_tracker.html` from `webpage_design.html` + the tracker — re-run after changes |
| `data.json` | Policy database — **edit this to add/update policies** |
| `world-110m.json` | TopoJSON world map geometry (Natural Earth 110m, do not edit) |
| `webpage_design.html` | Saved IRENA site page used as the design template/base |

## Running locally

```bash
cd policy_tracker
python -m http.server 8080
# open http://localhost:8080/irena_policy_tracker.html
```

Requires a server (not `file://`) because `data.json` and `world-110m.json` are fetched via `fetch()`.

## Rebuilding the IRENA-embedded version

After making changes to the tracker HTML/CSS/JS logic in `build_tracker.py`, regenerate:

```bash
python build_tracker.py
```

This reads `webpage_design.html`, injects the tracker, and writes `irena_policy_tracker.html`.

## Adding policies

Edit `data.json`. Each entry:
```json
{
  "id": 26,
  "country": "Nigeria",
  "iso3": "NGA",
  "region": "Africa",
  "policy_name": "Renewable Energy Master Plan",
  "policy_type": "Target",
  "status": "Active",
  "year": 2005,
  "description": "...",
  "source_url": "https://..."
}
```

Valid `region` values: `Africa` / `Asia-Pacific` / `Europe` / `Latin America` / `Middle East` / `North America`
Valid `policy_type` values: `Auction` / `Feed-in Tariff` / `Mandate` / `Net Metering` / `Target` / `Tax Incentive` / `Other`
Valid `status` values: `Active` / `Planned` / `Expired` / `Under Review`

## Tech stack

- **D3.js v7** — choropleth SVG world map (CDN for demo; to be bundled for Sitecore)
- **TopoJSON** — world map geometry parsing
- **Vanilla JS** — filters, table, pagination, map↔table sync
- **IRENA design system** — palette `#003F73` / `#00A3E0`, Graphik font, `l-grid` layout, max-width 1316px

## Layout constraints

The tracker sits inside IRENA's `l-grid__m--10` content column (10/12 of 1316px ≈ 1097px wide) alongside the Newsletter sidebar. This matches the width of other IRENA content pages and is intentional — do not break it out to full width.

## Sitecore integration path

1. Host on GitHub Pages (`index.html`)
2. Embed in Sitecore via: `<iframe src="https://..." width="100%" height="900px" style="border:none;">`
3. For native integration: D3 + TopoJSON must be added to `webpage_design_files/` and referenced locally (no CDN)

## Indicators / columns

The user will provide a final list of policy indicators — at that point update:
- `data.json` schema (add new fields)
- Table columns in `build_tracker.py` (the `<thead>` and `<tbody>` row template)
- Filter dropdowns if new categorical fields are added
