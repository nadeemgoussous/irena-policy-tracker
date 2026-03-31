# IRENA Renewable Energy Policy Tracker

Interactive policy tracker with a choropleth world map and filterable table. Built as a static HTML demo for GitHub Pages.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Main tracker page (all logic inline) |
| `data.json` | Policy database — **edit this to update the tracker** |
| `world-110m.json` | World map geometry (Natural Earth 110m, do not edit) |

## Updating the data

Open `data.json` in GitHub's web editor (click the file → pencil icon) and add/edit entries in the `policies` array. Each policy entry looks like:

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
  "description": "Sets targets for renewable energy share in Nigeria's electricity mix.",
  "source_url": "https://www.irena.org/..."
}
```

### Field reference

| Field | Values |
|-------|--------|
| `iso3` | ISO 3166-1 alpha-3 country code (e.g. `NGA`, `DEU`, `BRA`) |
| `region` | `Africa` / `Asia-Pacific` / `Europe` / `Latin America` / `Middle East` / `North America` |
| `policy_type` | `Auction` / `Feed-in Tariff` / `Mandate` / `Net Metering` / `Target` / `Tax Incentive` / `Other` |
| `status` | `Active` / `Planned` / `Expired` / `Under Review` |
| `year` | 4-digit year the policy was introduced |

Also update `"last_updated"` at the top of the file when you make changes.

## Running locally

```bash
python -m http.server 8080
# then open http://localhost:8080
```

(Required because the page fetches `data.json` and `world-110m.json` via `fetch()`, which needs a server — not `file://`.)

## GitHub Pages deployment

1. Push this folder to a GitHub repo
2. Go to **Settings → Pages → Source: Deploy from branch → main / root**
3. Your tracker will be live at `https://<username>.github.io/<repo-name>/`

## Sitecore iframe embed

Once deployed on GitHub Pages, embed in any Sitecore page with:

```html
<iframe
  src="https://<username>.github.io/<repo-name>/"
  width="100%"
  height="900px"
  style="border:none;"
  title="IRENA Renewable Energy Policy Tracker">
</iframe>
```
