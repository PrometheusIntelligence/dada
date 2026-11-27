// Mobile Floor and first-screen probe for an application or data viewport (DADA mobile-standard rows M1, M3, M4, M5, M7, M8, plus the first-screen rule).
//   NODE_PATH=$(npm root -g) node floor_probe.cjs --url http://127.0.0.1:4190/ --ready '.mark' --map '.viewport' [--marks '.mark'] [--out floor.json]
// --ready: a selector that exists once the data is drawn. --map: the data viewport (its top and bottom are compared with the fold).
// --marks: the selector of the data marks (default: --ready). Marks are held to 24px hit targets, other controls to 44px on phones.
// The probe has a fixture that must fail (an 8px label, a 20px button, a 10px input); if it is not reported, no number counts. Exit 1 when a row fails.
const { chromium } = require('playwright');
const fs = require('fs');
const arg = (name, fallback) => { const i = process.argv.indexOf('--' + name); return i > -1 ? process.argv[i + 1] : fallback; };
const URL = arg('url', 'http://127.0.0.1:4173/'), READY = arg('ready'), MAP = arg('map'), MARKS = arg('marks', READY), OUT = arg('out');
if (!READY || !MAP) { console.error('usage: floor_probe.cjs --url URL --ready SELECTOR --map SELECTOR [--marks SELECTOR] [--out FILE]'); process.exit(2); }

const probe = ({ map, marks }) => {
  const vis = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el); return r.width > 0 && r.height > 0 && r.right > 0 && r.bottom > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05; };
  const name = el => `${el.tagName.toLowerCase()}${el.tagName === 'A' || el.tagName === 'BUTTON' ? '(' + el.textContent.trim().slice(0, 18) + ')' : ''}${el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/)[0] : ''}${el.getAttribute('aria-label') ? `[${el.getAttribute('aria-label').slice(0, 28)}]` : ''}`;
  const out = { overflow: Math.max(0, document.documentElement.scrollWidth - innerWidth), targets: [], tiny: [], inputZoom: [], hoverUngated: 0, vh100: 0, bars: 0, markTargets: { n: 0, under24: 0 } };
  const markSet = new Set(marks ? document.querySelectorAll(marks) : []);
  const hit = el => { const r = el.getBoundingClientRect(); let w = r.width, h = r.height; if (el.tagName === 'INPUT' && el.closest('label')) { const l = el.closest('label').getBoundingClientRect(); w = Math.max(w, l.width); h = Math.max(h, l.height); } return [w, h]; };
  document.querySelectorAll('button, a[href], input:not([type=hidden]), select, textarea, summary, [role=button], [role=tab]').forEach(el => {
    if (!vis(el)) return;
    if (markSet.has(el) || el.closest(marks || '#__none__')) { const [w, h] = hit(el.closest(marks) || el); out.markTargets.n++; if (Math.min(w, h) < 24) out.markTargets.under24++; return; }
    if (el.tagName === 'A' && getComputedStyle(el).display === 'inline' && el.parentElement && /^(P|LI|DD|DIV|SPAN)$/.test(el.parentElement.tagName) && el.parentElement.textContent.trim().length > el.textContent.trim().length + 12) return;
    const [w, h] = hit(el); if (w < 44 || h < 44) out.targets.push(`${name(el)} ${Math.round(w)}x${Math.round(h)}`);
  });
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), seen = new Set();
  while (walker.nextNode()) { const t = walker.currentNode, el = t.parentElement; if (!el || !t.textContent.trim() || seen.has(el)) continue; seen.add(el); if (!vis(el) || el.closest('[aria-hidden="true"], script, style, svg')) continue; const px = parseFloat(getComputedStyle(el).fontSize); if (px < 12) out.tiny.push(`${name(el)} ${px}px "${t.textContent.trim().slice(0, 24)}"`); }
  document.querySelectorAll('input, select, textarea').forEach(el => { if (vis(el) && el.type !== 'checkbox' && el.type !== 'radio' && parseFloat(getComputedStyle(el).fontSize) < 16) out.inputZoom.push(name(el)); });
  for (const sheet of document.styleSheets) { let rules; try { rules = sheet.cssRules; } catch { continue; } const walk = (list, gated) => { for (const r of list) { if (r.cssRules && r.media) walk(r.cssRules, gated || /hover:\s*hover/.test(r.media.mediaText)); else if (r.cssRules) walk(r.cssRules, gated); else if (r.selectorText && /:hover/.test(r.selectorText) && !gated) out.hoverUngated++; if (r.style && /\b100vh\b/.test(r.style.cssText) && /height/.test(r.cssText)) out.vh100++; } }; walk(rules, false); }
  let barPx = 0; document.querySelectorAll('body *').forEach(el => { const s = getComputedStyle(el); if ((s.position === 'fixed' || s.position === 'sticky') && vis(el)) { const r = el.getBoundingClientRect(); if (r.width > innerWidth * .6 && r.height < innerHeight * .5) barPx += r.height; } });
  out.bars = Math.round(barPx / innerHeight * 100);
  const m = map && document.querySelector(map); if (m) { const r = m.getBoundingClientRect(); out.firstScreen = { top: Math.round(r.top), bottom: Math.round(r.bottom), fold: innerHeight, scrollsSideways: m.scrollWidth > m.clientWidth + 1 }; }
  out.marksOnScreen = marks ? [...document.querySelectorAll(marks)].filter(el => { const r = el.getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight && r.left >= 0 && r.right <= innerWidth; }).length : 0;
  return out;
};

(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const report = { url: URL, widths: {}, failures: [] };
  for (const [w, h, label] of [[390, 844, 'phone 390x844'], [375, 812, 'phone 375x812'], [1280, 800, 'desktop 1280x800'], [1440, 900, 'desktop 1440x900']]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, hasTouch: w < 800, isMobile: w < 800, deviceScaleFactor: 1 });
    const page = await ctx.newPage(); const bytes = { total: 0, largest: { url: '', bytes: 0 } };
    page.on('response', async r => { try { const b = (await r.body()).length; bytes.total += b; if (b > bytes.largest.bytes) bytes.largest = { url: r.url().replace(/^https?:\/\/[^/]+/, ''), bytes: b }; } catch { /* redirects have no body */ } });
    await page.goto(URL); await page.waitForSelector(READY, { timeout: 30000 }); await page.waitForTimeout(700);
    const r = await page.evaluate(probe, { map: MAP, marks: MARKS }); r.bytesBeforeViewportUsable = bytes.total; r.largestRequest = bytes.largest;
    const rows = [];
    if (w < 800) { rows.push(['M1 no sideways scroll', r.overflow === 0, r.overflow], ['M3 controls >= 44px', r.targets.length === 0, r.targets.length], ['M4 no text under 12px', r.tiny.length === 0, r.tiny.length], ['M5 inputs >= 16px', r.inputZoom.length === 0, r.inputZoom.length], ['M6 hover gated', r.hoverUngated === 0, r.hoverUngated], ['M7 no bare 100vh', r.vh100 === 0, r.vh100], ['M8 bars <= 15% of height', r.bars <= 15, r.bars], ['marks >= 24px hit targets', r.markTargets.under24 === 0, `${r.markTargets.under24} of ${r.markTargets.n}`]); }
    else rows.push(['no sideways scroll', r.overflow === 0, r.overflow]);
    rows.push(['first screen: viewport starts above the fold', !!r.firstScreen && r.firstScreen.top < h, r.firstScreen && r.firstScreen.top], ['first screen: marks visible without scrolling', r.marksOnScreen > 0, r.marksOnScreen]);
    r.rows = rows.map(([row, pass, value]) => ({ row, pass, value })); r.fails = r.rows.filter(x => !x.pass).map(x => x.row);
    report.widths[label] = r; for (const f of r.fails) report.failures.push(`${label}: ${f}`);
    await ctx.close();
  }
  await browser.close();
  const b2 = await chromium.launch(); const p2 = await (await b2.newContext({ viewport: { width: 390, height: 800 } })).newPage();
  await p2.setContent('<button style="width:20px;height:20px">x</button><p style="font-size:8px">tiny</p><input style="font-size:10px">');
  const fx = await p2.evaluate(probe, { map: null, marks: null }); await b2.close();
  report.selfTest = { pass: fx.targets.length >= 1 && fx.tiny.length === 1 && fx.inputZoom.length === 1, detail: { targets: fx.targets.length, tiny: fx.tiny.length, inputZoom: fx.inputZoom.length } };
  if (!report.selfTest.pass) report.failures.push('probe self-test failed: the fixture was not reported');
  const text = JSON.stringify(report, null, 1); if (OUT) fs.writeFileSync(OUT, text); console.log(text);
  process.exit(report.failures.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
