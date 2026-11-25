#!/usr/bin/env node
/**
 * Measure a mobile app (rendered as its web build) at phone sizes, the way the DADA Mobile run needs.
 *
 *   node tools/mobile-measure.mjs --base http://localhost:8099 --routes /,/explore,/docs --out /tmp/shots
 *   node tools/mobile-measure.mjs --selftest        # the probe must FAIL a page built to fail it
 *
 * Needs Playwright (`require('playwright')` must resolve; set PLAYWRIGHT=/path/to/playwright if it lives elsewhere).
 * For each route and each device it saves a screenshot (deviceScaleFactor 2, laid out at the device's CSS width) and runs:
 *   overflow   horizontal page overflow, and any element whose content is wider than its box (clipped text)
 *   targets    interactive elements smaller than 44 x 44 CSS px (Apple HIG) or 48 dp (Material) on either axis
 *   text       visible text smaller than 12 px
 *   contrast   WCAG contrast of visible text against its nearest opaque background (4.5:1, 3:1 for 24px+ or 18.66px+ bold)
 *   chrome     fixed/sticky bars (tab bar, header) overlapping the last piece of content once scrolled to the end
 *   fold       bottom edge of the first content block against the device height (is the first screen complete?)
 * `--fail` rows are printed; the exit code is the number of failing probes (capped at 99), so 0 is clean.
 * A web render is NOT a native emulator: it shows layout, size and colour, not Face ID, the keystore, system fonts or safe areas.
 */
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');

const DEVICES = {
  'iphone-15-pro': { viewport: { width: 393, height: 852 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148' },
  'iphone-se': { viewport: { width: 375, height: 667 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148' },
  'pixel-7': { viewport: { width: 412, height: 915 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36' },
};

const args = Object.fromEntries(process.argv.slice(2).map((a, i, all) => a.startsWith('--') ? [a.slice(2), all[i + 1] && !all[i + 1].startsWith('--') ? all[i + 1] : true] : []).filter((x) => x.length));

// Runs in the page. Returns rows of {probe, el, value, fail}.
const PROBES = ({ width: W, height: H }) => {
  const rows = [];
  const vis = (e) => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0; };
  const label = (e) => (e.getAttribute('aria-label') || e.innerText || e.tagName).trim().replace(/\s+/g, ' ').slice(0, 40);
  const sw = document.documentElement.scrollWidth;
  rows.push({ probe: 'overflow', el: 'page', value: `scrollWidth ${sw} vs ${W}`, fail: sw > W + 1 });
  for (const e of document.querySelectorAll('body *')) {
    if (!vis(e)) continue;
    const s = getComputedStyle(e);
    if (['hidden', 'clip'].includes(s.overflowX) && e.scrollWidth > e.clientWidth + 2 && e.children.length === 0 && e.innerText) rows.push({ probe: 'overflow', el: label(e), value: `content ${e.scrollWidth} > box ${e.clientWidth}`, fail: true });
  }
  const interactive = [...document.querySelectorAll('a[href],button,input,textarea,select,[role=button],[role=link],[role=tab],[tabindex]:not([tabindex="-1"])')].filter(vis);
  for (const e of interactive) {
    const r = e.getBoundingClientRect();
    if (r.height > 5000) continue;
    rows.push({ probe: 'targets', el: label(e), value: `${Math.round(r.width)}x${Math.round(r.height)}`, fail: r.width < 44 || r.height < 44 });
  }
  const lum = ([r, g, b]) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,/]+/).map(Number); return { rgb: p.slice(0, 3), a: p.length > 3 ? p[3] : 1 }; };
  const bgOf = (e) => { let n = e; while (n) { const c = parse(getComputedStyle(n).backgroundColor); if (c && c.a > 0.95) return c.rgb; n = n.parentElement; } return [255, 255, 255]; };
  const seen = new Set();
  for (const e of document.querySelectorAll('body *')) {
    if (!vis(e) || ![...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) continue;
    const s = getComputedStyle(e), fs = parseFloat(s.fontSize), key = `${s.color}|${fs}|${bgOf(e)}|${e.innerText.slice(0, 12)}`;
    if (seen.has(key)) continue; seen.add(key);
    rows.push({ probe: 'text', el: label(e), value: `${fs}px`, fail: fs < 12 });
    const fg = parse(s.color); if (!fg) continue;
    const bg = bgOf(e), a = fg.a, mix = fg.rgb.map((v, i) => v * a + bg[i] * (1 - a));
    const L1 = lum(mix) + 0.05, L2 = lum(bg) + 0.05, ratio = Math.max(L1, L2) / Math.min(L1, L2);
    const large = fs >= 24 || (fs >= 18.66 && +s.fontWeight >= 700);
    rows.push({ probe: 'contrast', el: label(e), value: ratio.toFixed(2) + ':1', fail: ratio < (large ? 3 : 4.5) });
  }
  const fixed = [...document.querySelectorAll('body *')].filter((e) => vis(e) && ['fixed', 'sticky'].includes(getComputedStyle(e).position));
  const scrollers = [...document.querySelectorAll('*')].filter((e) => e.scrollHeight > e.clientHeight + 4 && ['auto', 'scroll'].includes(getComputedStyle(e).overflowY) && vis(e));
  for (const sc of scrollers) sc.scrollTop = sc.scrollHeight;
  window.scrollTo(0, document.body.scrollHeight);
  const content = [...document.querySelectorAll('body *')].filter((e) => vis(e) && e.children.length === 0 && e.innerText && !fixed.some((f) => f.contains(e)));
  const lastBottom = Math.max(0, ...content.map((e) => e.getBoundingClientRect().bottom));
  const bars = fixed.filter((f) => f.getBoundingClientRect().top > H * 0.6 && f.getBoundingClientRect().height < 140);
  for (const b of bars) rows.push({ probe: 'chrome', el: 'bottom bar', value: `last content ends ${Math.round(lastBottom)}, bar starts ${Math.round(b.getBoundingClientRect().top)}`, fail: lastBottom > b.getBoundingClientRect().top + 1 });
  for (const sc of scrollers) sc.scrollTop = 0; window.scrollTo(0, 0);
  const first = content.filter((e) => e.getBoundingClientRect().top < H).map((e) => e.getBoundingClientRect().bottom);
  rows.push({ probe: 'fold', el: 'first screen', value: `content to ${Math.round(Math.max(0, ...first))} of ${H}`, fail: Math.max(0, ...first) > H });
  return rows;
};

async function run(base, routes, devices, out) {
  mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const all = [];
  for (const d of devices) {
    const ctx = await browser.newContext(DEVICES[d]);
    const page = await ctx.newPage();
    for (const route of routes) {
      await page.goto(base + route, { waitUntil: 'networkidle' }).catch(() => {});
      await page.waitForTimeout(800);
      const name = `${d}${route.replace(/[^a-z0-9]+/gi, '-').replace(/-$/, '') || '-home'}`;
      await page.screenshot({ path: `${out}/${name}.png` });
      for (const r of await page.evaluate(PROBES, DEVICES[d].viewport)) all.push({ device: d, route, ...r });
    }
    await ctx.close();
  }
  await browser.close();
  return all;
}

function report(rows) {
  const fails = rows.filter((r) => r.fail);
  const by = {};
  for (const r of rows) { const k = r.probe; by[k] ??= { n: 0, fail: 0 }; by[k].n++; if (r.fail) by[k].fail++; }
  console.log('probe      failing / measured');
  for (const [k, v] of Object.entries(by)) console.log(`${k.padEnd(10)} ${String(v.fail).padStart(4)} / ${v.n}`);
  for (const f of fails.slice(0, 60)) console.log(`FAIL ${f.device} ${f.route} ${f.probe}: "${f.el}" ${f.value}`);
  if (fails.length > 60) console.log(`... ${fails.length - 60} more`);
  return fails.length;
}

if (args.selftest) {
  // A page built to fail every probe. If any probe reports clean, the instrument is broken (lesson: an inverted filter reported 0).
  const { createServer } = await import('node:http');
  const page = (body) => `<!doctype html><meta name=viewport content="width=device-width"><body style="margin:0;background:#fff">${body}`;
  const pages = {
    '/a': page(`<button style="width:20px;height:20px;position:absolute;top:10px">x</button><p style="color:#bbb;font-size:9px;margin:40px 0 0">low contrast tiny text</p><div style="width:900px;height:10px;background:red"></div><div style="overflow:hidden;width:50px"><span style="white-space:nowrap">clipped clipped clipped clipped</span></div>`),
    '/b': page(`<div style="height:1500px"></div><p>end</p><nav style="position:fixed;bottom:0;left:0;right:0;height:80px;background:#222;color:#fff">bar</nav>`),
  };
  const srv = createServer((_, r) => { r.setHeader('content-type', 'text/html'); r.end(pages[_.url] ?? ''); }).listen(0);
  const rows = await run(`http://localhost:${srv.address().port}`, ['/a', '/b'], ['iphone-15-pro'], process.env.TMPDIR || '/tmp');
  srv.close();
  const need = ['overflow', 'targets', 'text', 'contrast', 'chrome'];
  if (process.env.DEBUG) console.log(rows.filter((r) => ['overflow','chrome','fold'].includes(r.probe)));
  const missed = need.filter((p) => !rows.some((r) => r.probe === p && r.fail));
  console.log(missed.length ? `SELFTEST FAILED: probes that did not fail the bad page: ${missed.join(', ')}` : 'selftest ok: every probe fails the page built to fail it');
  process.exit(missed.length ? 1 : 0);
}

const base = args.base, routes = String(args.routes || '/').split(','), out = args.out || './mobile-shots';
const devices = String(args.devices || 'iphone-15-pro,pixel-7').split(',');
if (!base) { console.error('usage: --base URL [--routes /,/a] [--devices iphone-15-pro,iphone-se,pixel-7] [--out dir] | --selftest'); process.exit(2); }
const rows = await run(base, routes, devices, out);
writeFileSync(`${out}/measure.json`, JSON.stringify(rows, null, 1));
process.exit(Math.min(99, report(rows)));
