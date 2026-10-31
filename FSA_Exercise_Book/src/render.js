// Usage: node render.js book.html out.pdf
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const [, , htmlPath, outPath] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 } });
  page.on('pageerror', e => console.error('PAGE ERROR:', e.message));
  page.on('console', m => { if (m.type() === 'error') console.error('CONSOLE:', m.text()); });
  await page.goto('file://' + path.resolve(htmlPath), { waitUntil: 'load' });
  await page.waitForFunction('window.__done === true', null, { timeout: 180000 });
  const n = await page.evaluate('window.__pages');
  const ov = await page.evaluate('window.__overflow');
  if (ov.length) console.log('OVERFLOW pages:', JSON.stringify(ov));
  await page.pdf({
    path: outPath, format: 'A4', printBackground: true, preferCSSPageSize: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }, outline: true, tagged: true,
  });
  await browser.close();
  console.log(`pages=${n} -> ${outPath}`);
})().catch(e => { console.error(e); process.exit(1); });
