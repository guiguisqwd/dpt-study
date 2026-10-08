// Automated QA for a built daily pack. Usage: node qa.js <pack.html> <out_dir>
// Writes <out_dir>/qa.json and screenshots (page top, every chapter, every figure, mobile top).
// Checks: JS errors, all chapters present, SVG text overlaps / text outside the figure,
// horizontal scroll on a 390 px phone, pronunciation coverage of key terms, say buttons.
const path = require('path');
const fs = require('fs');
function loadPlaywright() {
  for (const p of ['playwright', '/opt/node22/lib/node_modules/playwright', '/opt/npm-tools/node_modules/playwright', '/usr/lib/node_modules/playwright']) {
    try { return require(p); } catch (e) { /* try next */ }
  }
  throw new Error('playwright not found');
}
const { chromium } = loadPlaywright();
const exe = ['/opt/pw-browsers/chromium', process.env.CHROMIUM_PATH].filter(p => p && fs.existsSync(p))[0];

(async () => {
  const file = path.resolve(process.argv[2]);
  const out = path.resolve(process.argv[3]);
  fs.mkdirSync(out, { recursive: true });
  const url = 'file://' + file;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  const report = { file, errors: [], overlaps: [], outside: [], chapters: [], figures: 0, say_buttons: 0,
                   terms_without_pron: [], mobile_scroll_width: null, screenshots: [], figure_shots: [] };
  const page = await browser.newPage({ viewport: { width: 1440, height: 950 } });
  page.on('pageerror', e => report.errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') report.errors.push('console: ' + m.text()); });
  await page.goto(url);
  await page.addStyleTag({ content: 'html{scroll-behavior:auto!important} #read-progress{display:none!important}' });
  await page.waitForTimeout(500);
  const top = path.join(out, 'top.png');
  await page.screenshot({ path: top }); report.screenshots.push(top);
  report.chapters = await page.$$eval('section.chapter', s => s.map(x => x.id));
  for (const id of report.chapters) {
    const p = path.join(out, `chapter-${id}.png`);
    await (await page.$('#' + id)).screenshot({ path: p });
    report.screenshots.push(p);
  }
  const figs = await page.$$('svg[data-figure]');
  report.figures = figs.length;
  for (const f of figs) {
    const n = await f.getAttribute('data-figure');
    const p = path.join(out, `figure-${n}.png`);
    if (!report.figure_shots.includes(p)) { await f.screenshot({ path: p }); report.figure_shots.push(p); }
  }
  const geo = await page.evaluate(() => {
    const ov = [], outside = [];
    document.querySelectorAll('svg[data-figure]').forEach(svg => {
      const n = svg.dataset.figure;
      const ts = [...svg.querySelectorAll('tspan,text')].filter(t => t.tagName === 'tspan' || !t.querySelector('tspan')).filter(t => t.textContent.trim());
      const sr = svg.getBoundingClientRect();
      ts.forEach(t => { const q = t.getBoundingClientRect(); if (q.left < sr.left - 1 || q.right > sr.right + 1 || q.bottom > sr.bottom + 1 || q.top < sr.top - 1) outside.push(n + ': ' + t.textContent.slice(0, 40)); });
      const r = ts.map(t => { const q = t.getBoundingClientRect(); return [q.left, q.top, q.right, q.bottom, t.textContent]; });
      for (let i = 0; i < r.length; i++) for (let j = i + 1; j < r.length; j++) {
        const a = r[i], c = r[j];
        if (Math.min(a[2], c[2]) - Math.max(a[0], c[0]) > 2 && Math.min(a[3], c[3]) - Math.max(a[1], c[1]) > 2) ov.push(n + ': ' + a[4].slice(0, 30) + ' | ' + c[4].slice(0, 30));
      }
    });
    const termsNoPron = [...document.querySelectorAll('.before-terms .term:not(.acu-term)')].filter(t => !t.querySelector('.pron')).map(t => t.querySelector('b').textContent);
    return { ov, outside, termsNoPron, say: document.querySelectorAll('[data-say]').length };
  });
  report.overlaps = geo.ov; report.outside = geo.outside; report.terms_without_pron = geo.termsNoPron; report.say_buttons = geo.say;
  // mobile
  const m = await browser.newPage({ viewport: { width: 390, height: 844 } });
  m.on('pageerror', e => report.errors.push('mobile pageerror: ' + e.message));
  await m.goto(url); await m.waitForTimeout(400);
  report.mobile_scroll_width = await m.evaluate(() => document.documentElement.scrollWidth);
  const mob = path.join(out, 'mobile-top.png');
  await m.screenshot({ path: mob }); report.screenshots.push(mob);
  // flashcards work?
  report.flashcards = await page.evaluate(() => { const d = document.getElementById('deck-data'); return d ? JSON.parse(d.textContent).length : 0; });
  await browser.close();
  fs.writeFileSync(path.join(out, 'qa.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ errors: report.errors.length, overlaps: report.overlaps.length, outside: report.outside.length, chapters: report.chapters.length, figures: report.figures, mobile_scroll_width: report.mobile_scroll_width, terms_without_pron: report.terms_without_pron.length, flashcards: report.flashcards }));
})().catch(e => { console.error(e); process.exit(2); });
