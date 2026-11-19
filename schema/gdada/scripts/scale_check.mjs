#!/usr/bin/env node
// scale_check: do the things in the art library have a believable size next to a person?
//   node scale_check.mjs <art.hc> <scale-table.json> [--json]
// art.hc       the game's generated art data: lines "//NAME" followed by 16-character quoted rows (HolyC string arrays).
// scale table  { "person_px": 24, "tolerance": 0.25, "objects": { "O_PALM": { "persons": 1.33, "why": "..." }, "O_PLANE1": { "persons": 2, "width_persons": 4.6 } } }
//              persons = the height the thing should have, in person-heights (a person is person_px tall).
// A tall object is two cells, NAME (lower) and NAMEU (upper); a wide one is NAME1, NAME2 ...; they are measured together.
// Exit 1 if any listed object is outside the tolerance, or if an object has no entry in the table (--allow-missing to skip).
import { readFileSync } from "node:fs";

export function parseArt(text) {
  const out = new Map(); let name = null, rows = [];
  for (const line of text.split("\n")) {
    const m = line.match(/^\/\/([A-Z][A-Z0-9_]+)\s*$/);
    if (m) { if (name && rows.length) out.set(name, rows); name = m[1]; rows = []; continue; }
    const r = line.match(/^"([0-9a-fA-F.]{16})",?\s*$/);
    if (r && name) rows.push(r[1]);
    else if (name && rows.length && !r) { out.set(name, rows); name = null; rows = []; }
  }
  if (name && rows.length) out.set(name, rows);
  return out;
}

// opaque extent of one 16x16 cell: first and last row with any non-transparent pixel (and columns)
const extent = (rows) => {
  let y0 = -1, y1 = -1, x0 = 99, x1 = -1;
  rows.forEach((r, y) => [...r].forEach((c, x) => { if (c !== ".") { if (y0 < 0) y0 = y; y1 = y; x0 = Math.min(x0, x); x1 = Math.max(x1, x); } }));
  return y0 < 0 ? null : { y0, y1, x0, x1 };
};

export function measure(art) {
  const res = new Map();
  for (const [name, rows] of art) {
    if (!name.startsWith("O_") || rows.length !== 16) continue;
    if (/U{1,2}$/.test(name) && art.has(name.replace(/U{1,2}$/, ""))) continue;     // upper cells: counted with the base
    const e = extent(rows); if (!e) continue;
    let h = e.y1 - e.y0 + 1, w = e.x1 - e.x0 + 1;
    const up = art.get(name + "U"), up2 = art.get(name + "UU");
    const top = up2 || up;                                                          // the topmost cell above the base
    if (top) { const u = extent(top); if (u) h = (16 - u.y0) + (up2 ? 16 : 0) + (e.y1 + 1); }   // rows of the top cell, the middle cell, the base
    let cols = 1;
    for (let k = 1; art.has(name.replace(/\d*$/, "") + k) && k < 8; k++) cols = k;       // NAME1..NAMEk side by side
    res.set(name, { h, w, tall: !!up });
  }
  // a block is NAME1..NAMEn side by side (the base NAME1 exists): its cells are one object, as tall as its tallest cell
  for (const [name, v] of res) {
    const m = name.match(/^(O_[A-Z]+?)(\d+)$/);
    if (!m || !res.has(m[1] + "1")) continue;
    let h = 0, cols = 0; for (const [n2, v2] of res) if (n2.startsWith(m[1]) && /^\d+$/.test(n2.slice(m[1].length))) { h = Math.max(h, v2.h); cols++; }
    v.h = h; v.w = cols * 16; v.cols = cols;                                       // a block is as wide as its cells
  }
  return res;
}

export function check(art, table) {
  const P = table.person_px || 24, tol = table.tolerance ?? 0.25, m = measure(art), bad = [], ok = [], missing = [];
  for (const [name, v] of m) {
    const want = table.objects?.[name];
    if (!want) { missing.push(name); continue; }
    const target = want.persons * P, lo = target * (1 - tol), hi = target * (1 + tol);
    const rec = { name, px: v.h, persons: +(v.h / P).toFixed(2), want: want.persons, why: want.why || "" };
    let off = v.h < lo || v.h > hi;
    if (want.width_persons) {                                                      // a width target: for blocks, the whole row of cells
      const wt = want.width_persons * P, wpx = v.w; rec.width_px = wpx; rec.width_persons = +(wpx / P).toFixed(2); rec.want_width = want.width_persons;
      if (wpx < wt * (1 - tol) || wpx > wt * (1 + tol)) off = true;
    }
    (off ? bad : ok).push(rec);
  }
  return { bad, ok, missing };
}

if (process.argv[1] && process.argv[1].endsWith("scale_check.mjs")) {
  const [artPath, tablePath] = process.argv.slice(2).filter((a) => !a.startsWith("--"));
  if (!artPath || !tablePath) { console.error("usage: scale_check.mjs <art.hc> <scale-table.json>"); process.exit(2); }
  const r = check(parseArt(readFileSync(artPath, "utf8")), JSON.parse(readFileSync(tablePath, "utf8")));
  if (process.argv.includes("--json")) console.log(JSON.stringify(r, null, 1));
  else {
    for (const b of r.bad) console.log(`TOO ${b.persons > b.want ? "BIG  " : "SMALL"} ${b.name.padEnd(14)} ${String(b.px).padStart(3)} px = ${b.persons} persons, wanted ${b.want}` + (b.want_width ? `; width ${b.width_persons} persons, wanted ${b.want_width}` : "") + (b.why ? `  (${b.why})` : ""));
    if (r.missing.length) console.log(`no entry in the scale table (${r.missing.length}): ${r.missing.join(" ")}`);
    console.log(`scale: ${r.ok.length} right, ${r.bad.length} off, ${r.missing.length} unlisted`);
  }
  process.exit(r.bad.length || (r.missing.length && !process.argv.includes("--allow-missing")) ? 1 : 0);
}
