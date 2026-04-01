// @ts-check
const { test, expect } = require('@playwright/test');

// Helper: wait for data to fully load (stats no longer show '—')
async function waitForData(page) {
  await expect(page.locator('#stat-total')).not.toHaveText('—', { timeout: 15000 });
}

// ══════════════════════════════════════════════════════════════════════════════
// 1. PAGE LOAD & STRUCTURE
// ══════════════════════════════════════════════════════════════════════════════
test.describe('Page load & structure', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/index.html');
    await waitForData(page);
  });

  test('title is correct', async ({ page }) => {
    await expect(page).toHaveTitle(/Energy Crisis Transition Tracker/);
  });

  test('header shows IRENA wordmark and tracker title', async ({ page }) => {
    await expect(page.locator('.header-title')).toContainText('Energy Crisis Transition Tracker');
    await expect(page.locator('.header-logo')).toBeVisible();
  });

  test('hero section is visible with description text', async ({ page }) => {
    await expect(page.locator('.hero h1')).toContainText('Energy Crisis Transition Tracker');
    await expect(page.locator('.hero p')).toContainText('national and multilateral responses');
  });

  test('footer renders current year', async ({ page }) => {
    const year = new Date().getFullYear().toString();
    await expect(page.locator('.footer')).toContainText(year);
  });
});

// ══════════════════════════════════════════════════════════════════════════════
// 2. DATA LOADING
// ══════════════════════════════════════════════════════════════════════════════
test.describe('Data loading', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/index.html');
    await waitForData(page);
  });

  test('stats bar shows numeric values', async ({ page }) => {
    const total = await page.locator('#stat-total').textContent();
    const countries = await page.locator('#stat-countries').textContent();
    const emergency = await page.locator('#stat-emergency').textContent();
    const sectors = await page.locator('#stat-sectors').textContent();

    expect(parseInt(total)).toBeGreaterThan(0);
    expect(parseInt(countries)).toBeGreaterThan(0);
    expect(parseInt(emergency)).toBeGreaterThanOrEqual(0);
    expect(parseInt(sectors)).toBeGreaterThan(0);
  });

  test('table has visible rows', async ({ page }) => {
    const rows = page.locator('#table-body tr');
    await expect(rows.first()).toBeVisible();
    const count = await rows.count();
    expect(count).toBeGreaterThan(0);
  });

  test('last updated date is shown in header', async ({ page }) => {
    const text = await page.locator('#header-updated').textContent();
    expect(text).not.toBe('Last updated: —');
  });
});

// ══════════════════════════════════════════════════════════════════════════════
// 3. MAP
// ══════════════════════════════════════════════════════════════════════════════
test.describe('Map', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/index.html');
    await waitForData(page);
  });

  test('SVG map renders country paths', async ({ page }) => {
    const paths = page.locator('#map-svg .country-path');
    const count = await paths.count();
    expect(count).toBeGreaterThan(100); // world-atlas has 177 countries
  });

  test('map legend is visible', async ({ page }) => {
    await expect(page.locator('.map-legend')).toBeVisible();
    await expect(page.locator('.legend-label')).toContainText('Measures');
  });

  test('clicking a country with data filters the table', async ({ page }) => {
    // Try ESP (Spain) — known to be in the dataset
    const spain = page.locator('.country-path[data-iso3="ESP"]');
    const spainExists = await spain.count();

    if (spainExists > 0) {
      await spain.click();
      await expect(page.locator('#active-country-bar')).toBeVisible({ timeout: 5000 });
      await expect(page.locator('#active-country-name')).toContainText('Spain');

      // Table should only show Spain rows
      const rows = page.locator('#table-body tr');
      const firstRowCountry = await rows.first().locator('td').first().textContent();
      expect(firstRowCountry).toContain('Spain');

      // Deselect
      await page.locator('#btn-deselect').click();
      await expect(page.locator('#active-country-bar')).not.toBeVisible();
    }
  });

  test('tooltip appears on country hover', async ({ page }) => {
    const spain = page.locator('.country-path[data-iso3="ESP"]');
    if (await spain.count() > 0) {
      await spain.hover();
      await expect(page.locator('#tooltip')).toBeVisible({ timeout: 3000 });
    }
  });
});

// ══════════════════════════════════════════════════════════════════════════════
// 4. FILTERS
// ══════════════════════════════════════════════════════════════════════════════
test.describe('Filters', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/index.html');
    await waitForData(page);
  });

  test('region filter narrows table results', async ({ page }) => {
    await page.selectOption('#filter-region', 'Europe');
    await page.waitForTimeout(300);

    // All visible rows should be Europe
    const firstRegion = await page.locator('#table-body tr td:nth-child(2)').first().textContent();
    expect(firstRegion?.trim()).toBe('Europe');

    const rows = await page.locator('#table-body tr').count();
    expect(rows).toBeGreaterThan(0);
  });

  test('pillar filter narrows table results', async ({ page }) => {
    await page.selectOption('#filter-pillar', 'Renewable Energy');
    await page.waitForTimeout(300);

    const rows = page.locator('#table-body tr');
    await expect(rows.first()).toBeVisible();

    // All visible rows should have the Renewable Energy pillar badge
    const firstPillarBadge = await rows.first().locator('.pillar-badge').textContent();
    expect(firstPillarBadge?.trim()).toContain('Renewable Energy');
  });

  test('typology filter narrows table results', async ({ page }) => {
    await page.selectOption('#filter-typology', 'Accelerated Pivot');
    await page.waitForTimeout(300);

    const rows = page.locator('#table-body tr');
    const count = await rows.count();
    if (count > 0) {
      const firstBadge = await rows.first().locator('.typology-badge').textContent();
      expect(firstBadge?.trim()).toContain('Accelerated Pivot');
    }
  });

  test('search filter works', async ({ page }) => {
    await page.fill('#filter-search', 'solar');
    await page.waitForTimeout(400);

    const rows = page.locator('#table-body tr');
    const count = await rows.count();

    if (count > 0) {
      const bodyText = await page.locator('#table-body').textContent();
      expect(bodyText?.toLowerCase()).toContain('solar');
    }
  });

  test('clear button resets all filters', async ({ page }) => {
    // Apply some filters
    await page.selectOption('#filter-region', 'Europe');
    await page.fill('#filter-search', 'energy');
    await page.waitForTimeout(300);

    // Clear
    await page.click('#btn-clear');
    await page.waitForTimeout(300);

    // After clear, dropdowns should be reset
    await expect(page.locator('#filter-region')).toHaveValue('');
    await expect(page.locator('#filter-search')).toHaveValue('');
  });

  test('combined filters work', async ({ page }) => {
    await page.selectOption('#filter-region', 'Europe');
    await page.selectOption('#filter-pillar', 'Renewable Energy');
    await page.waitForTimeout(300);

    const rows = page.locator('#table-body tr');
    const count = await rows.count();

    if (count > 0) {
      const regionCell = await rows.first().locator('td:nth-child(2)').textContent();
      expect(regionCell?.trim()).toBe('Europe');
    }
  });
});

// ══════════════════════════════════════════════════════════════════════════════
// 5. TABLE INTERACTIONS
// ══════════════════════════════════════════════════════════════════════════════
test.describe('Table interactions', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/index.html');
    await waitForData(page);
  });

  test('table has correct column headers', async ({ page }) => {
    const headers = page.locator('thead th');
    const texts = await headers.allTextContents();
    const cleaned = texts.map(t => t.replace(/[⇅▲▼]/g, '').trim());
    expect(cleaned).toContain('Country');
    expect(cleaned).toContain('Region');
    expect(cleaned).toContain('Measure Name');
    expect(cleaned).toContain('Pillar');
    expect(cleaned).toContain('Response Typology');
    expect(cleaned).toContain('Impact Assessment');
    expect(cleaned).toContain('Details');
  });

  test('clicking column header sorts the table', async ({ page }) => {
    const countryHeader = page.locator('thead th[data-col="country"]');

    await countryHeader.click(); // sort asc
    await page.waitForTimeout(200);
    const firstAfterAsc = await page.locator('#table-body tr td:first-child').first().textContent();

    await countryHeader.click(); // sort desc
    await page.waitForTimeout(200);
    const firstAfterDesc = await page.locator('#table-body tr td:first-child').first().textContent();

    const rows = await page.locator('#table-body tr').count();
    if (rows > 1) {
      expect(firstAfterAsc).not.toBe(firstAfterDesc);
    }
  });

  test('clicking a row opens the modal', async ({ page }) => {
    const firstRow = page.locator('#table-body tr').first();

    await firstRow.click();

    await expect(page.locator('#modal-overlay')).toHaveClass(/open/, { timeout: 5000 });
    await expect(page.locator('#modal-title')).toBeVisible();
  });

  test('modal close button works', async ({ page }) => {
    await page.locator('#table-body tr').first().click();
    await expect(page.locator('#modal-overlay')).toHaveClass(/open/);

    await page.locator('#modal-close').click();
    await expect(page.locator('#modal-overlay')).not.toHaveClass(/open/);
  });

  test('modal close on overlay click works', async ({ page }) => {
    await page.locator('#table-body tr').first().click();
    await expect(page.locator('#modal-overlay')).toHaveClass(/open/);

    // Click outside modal content (on overlay)
    await page.locator('#modal-overlay').click({ position: { x: 5, y: 5 } });
    await expect(page.locator('#modal-overlay')).not.toHaveClass(/open/);
  });

  test('modal shows policy details', async ({ page }) => {
    await page.locator('#table-body tr').first().click();
    await expect(page.locator('#modal-overlay')).toHaveClass(/open/);

    await expect(page.locator('#modal-title')).not.toBeEmpty();
    await expect(page.locator('#modal-body')).not.toBeEmpty();
  });
});

// ══════════════════════════════════════════════════════════════════════════════
// 6. ORG PANEL
// ══════════════════════════════════════════════════════════════════════════════
test.describe('Org panel', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/index.html');
    await waitForData(page);
  });

  test('org panel renders chips for INT organizations', async ({ page }) => {
    await expect(page.locator('.org-panel')).toBeVisible();
    const chips = page.locator('.org-chip');
    const count = await chips.count();
    expect(count).toBeGreaterThan(0);
  });

  test('clicking an org chip filters the table', async ({ page }) => {
    const firstChip = page.locator('.org-chip').first();

    await firstChip.click();
    await page.waitForTimeout(300);

    await expect(page.locator('#active-org-bar')).toBeVisible({ timeout: 3000 });

    // Deselect
    await page.locator('#btn-deselect-org').click();
    await expect(page.locator('#active-org-bar')).not.toBeVisible();
  });

  test('org chip shows policy count badge', async ({ page }) => {
    const firstChip = page.locator('.org-chip').first();
    await expect(firstChip.locator('.org-count')).toBeVisible();
  });
});

// ══════════════════════════════════════════════════════════════════════════════
// 7. PAGINATION
// ══════════════════════════════════════════════════════════════════════════════
test.describe('Pagination', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/index.html');
    await waitForData(page);
  });

  test('pagination renders when there are multiple pages', async ({ page }) => {
    const total = parseInt(await page.locator('#stat-total').textContent());
    const pageSize = 25;

    if (total > pageSize) {
      await expect(page.locator('.pagination')).toBeVisible();
      const buttons = page.locator('.page-btn');
      const btnCount = await buttons.count();
      expect(btnCount).toBeGreaterThan(1);
    }
  });

  test('clicking next page loads different rows', async ({ page }) => {
    const total = parseInt(await page.locator('#stat-total').textContent());
    if (total <= 25) { test.skip(); return; }

    const firstPageFirstRow = await page.locator('#table-body tr td:first-child').first().textContent();

    // Find page 2 button
    const page2Btn = page.locator('.page-btn').filter({ hasText: '2' });
    if (await page2Btn.count() > 0) {
      // Use JS dispatch to avoid Chrome mobile's overflow hit-test interference
      await page2Btn.evaluate(btn => btn.click());
      await page.waitForTimeout(200);
      const secondPageFirstRow = await page.locator('#table-body tr td:first-child').first().textContent();
      expect(secondPageFirstRow).not.toBe(firstPageFirstRow);
    }
  });
});

// ══════════════════════════════════════════════════════════════════════════════
// 8. MOBILE — LAYOUT & USABILITY
// ══════════════════════════════════════════════════════════════════════════════
test.describe('Mobile layout', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/index.html');
    await waitForData(page);
  });

  test('hero text is readable on mobile', async ({ page, viewport }) => {
    if (!viewport || viewport.width > 767) test.skip();

    const h1 = page.locator('.hero h1');
    await expect(h1).toBeVisible();
    const fontSize = await h1.evaluate(el => getComputedStyle(el).fontSize);
    expect(parseFloat(fontSize)).toBeLessThanOrEqual(22);
  });

  test('stats bar wraps on mobile (cards still visible)', async ({ page, viewport }) => {
    if (!viewport || viewport.width > 767) test.skip();

    await expect(page.locator('.stat-card').first()).toBeVisible();
    await expect(page.locator('.stat-card').last()).toBeVisible();
  });

  test('filter dropdowns are usable on mobile', async ({ page, viewport }) => {
    if (!viewport || viewport.width > 767) test.skip();

    const regionFilter = page.locator('#filter-region');
    await expect(regionFilter).toBeVisible();

    const box = await regionFilter.boundingBox();
    expect(box?.height).toBeGreaterThanOrEqual(32); // tap-target size
  });

  test('table scrolls horizontally on mobile', async ({ page, viewport }) => {
    if (!viewport || viewport.width > 767) test.skip();

    const tableWrap = page.locator('.table-wrap');
    await expect(tableWrap).toBeVisible();

    const overflow = await tableWrap.evaluate(el => getComputedStyle(el).overflowX);
    expect(overflow).toBe('auto');
  });

  test('modal fits within mobile screen', async ({ page, viewport }) => {
    if (!viewport || viewport.width > 767) test.skip();

    await page.locator('#table-body tr').first().click();
    await expect(page.locator('#modal-overlay')).toHaveClass(/open/);

    const modal = page.locator('.modal');
    const box = await modal.boundingBox();
    expect(box?.width).toBeLessThanOrEqual(viewport.width);

    await page.locator('#modal-close').click();
  });

  test('map is visible and does not overflow on mobile', async ({ page, viewport }) => {
    if (!viewport || viewport.width > 767) test.skip();

    const mapContainer = page.locator('#map-container');
    await expect(mapContainer).toBeVisible();

    const containerBox = await mapContainer.boundingBox();
    const svgBox = await page.locator('#map-svg').boundingBox();

    if (containerBox && svgBox) {
      expect(svgBox.width).toBeLessThanOrEqual(containerBox.width + 1);
    }
  });

  test('org chips wrap cleanly on mobile', async ({ page, viewport }) => {
    if (!viewport || viewport.width > 767) test.skip();

    const orgChips = page.locator('.org-chips');
    await expect(orgChips).toBeVisible();

    const overflow = await orgChips.evaluate(el => getComputedStyle(el).flexWrap);
    expect(overflow).toBe('wrap');
  });

  test('pagination buttons are tap-friendly on mobile', async ({ page, viewport }) => {
    if (!viewport || viewport.width > 767) test.skip();

    const total = parseInt(await page.locator('#stat-total').textContent() || '0');
    if (total <= 25) return;

    const firstBtn = page.locator('.page-btn').first();
    const box = await firstBtn.boundingBox();
    expect(box?.height).toBeGreaterThanOrEqual(30);
  });
});

// ══════════════════════════════════════════════════════════════════════════════
// 9. ACCESSIBILITY BASICS
// ══════════════════════════════════════════════════════════════════════════════
test.describe('Accessibility basics', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/index.html');
    await waitForData(page);
  });

  test('filter inputs have associated labels', async ({ page }) => {
    // Labels should have for= attributes matching their input IDs
    const regionLabel = page.locator('label[for="filter-region"]');
    await expect(regionLabel).toBeVisible();

    const searchLabel = page.locator('label[for="filter-search"]');
    await expect(searchLabel).toBeVisible();

    const pillarLabel = page.locator('label[for="filter-pillar"]');
    await expect(pillarLabel).toBeVisible();

    const typologyLabel = page.locator('label[for="filter-typology"]');
    await expect(typologyLabel).toBeVisible();
  });

  test('modal close button is keyboard focusable', async ({ page }) => {
    await page.locator('#table-body tr').first().click();
    await expect(page.locator('#modal-overlay')).toHaveClass(/open/);

    await page.locator('#modal-close').focus();
    await page.keyboard.press('Enter');
    await expect(page.locator('#modal-overlay')).not.toHaveClass(/open/);
  });

  test('page has viewport meta tag for mobile', async ({ page }) => {
    const viewport = await page.locator('meta[name="viewport"]').getAttribute('content');
    expect(viewport).toContain('width=device-width');
  });
});
