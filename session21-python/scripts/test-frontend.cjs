const assert = require('node:assert/strict');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({headless: true, ...(process.env.CHROME_PATH ? {executablePath: process.env.CHROME_PATH} : {})});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    const url = process.env.APP_URL || 'http://localhost:3000';
    await page.goto(url);
    const title = `Capstone browser test ${Date.now()}`;
    await page.getByRole('button', {name: 'New assignment'}).click();
    await page.getByLabel('Assignment title').fill(title);
    await page.getByLabel('Course session').fill('21');
    await page.getByLabel('Due date').fill('2026-10-31');
    await page.getByLabel('Description').fill('Session, due date, persistence and status verified in the browser.');
    const created = page.waitForResponse(r => r.request().method() === 'POST' && r.url().endsWith('/api/tasks'));
    await page.getByRole('button', {name: 'Save assignment'}).click();
    assert.equal((await created).status(), 201);
    const row = page.getByRole('row').filter({hasText: title});
    await row.waitFor();
    assert.match(await row.innerText(), /Session 21/);
    assert.match(await row.innerText(), /Due 2026-10-31/);
    await row.getByTitle('Advance status').click();
    await row.getByText('IN PROGRESS', {exact: true}).waitFor();
    await page.reload();
    await page.getByRole('row').filter({hasText: title}).getByText('IN PROGRESS', {exact: true}).waitFor();
    await page.screenshot({path: 'screenshots/review-frontend.png', fullPage: true});

    // A rejected save must preserve the form and show an error.
    await page.route('**/api/tasks', route => route.request().method() === 'POST' ? route.fulfill({status: 503, body: 'Unavailable'}) : route.continue());
    await page.getByRole('button', {name: 'New assignment'}).click();
    await page.getByLabel('Assignment title').fill('Keep this unsaved assignment');
    await page.getByRole('button', {name: 'Save assignment'}).click();
    await page.getByText('Could not save the assignment. Check the form and try again.', {exact: false}).last().waitFor();
    assert.equal(await page.getByLabel('Assignment title').inputValue(), 'Keep this unsaved assignment');
    await page.screenshot({path: 'screenshots/review-frontend-error.png', fullPage: true});
    await page.locator('button.close').click();
    await page.unroute('**/api/tasks');
    const deleted = page.waitForResponse(r => r.request().method() === 'DELETE');
    await page.getByRole('row').filter({hasText: title}).getByTitle('Delete assignment').click();
    assert.equal((await deleted).status(), 204);
    await page.getByRole('row').filter({hasText: title}).waitFor({state: 'detached'});
    await page.setViewportSize({width: 390, height: 844});
    await page.screenshot({path: 'screenshots/review-frontend-mobile.png', fullPage: true});
    console.log('PASS: creation, session/due date, status, reload persistence, rejected save, deletion and mobile view.');
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error); process.exit(1);});
