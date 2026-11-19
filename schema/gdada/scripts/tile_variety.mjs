#!/usr/bin/env node
// tile_variety: which maps are a bare plan (one flat floor) and need more tiles?
//   node tile_variety.mjs <world-dir> [--min-types 3] [--max-share 70] [--json]
// Reads world/**/*.map: the main grid, and an optional "ground" block (a second 20x14 grid of decorative ground tiles, '.' = the
// map's own floor). For each map it counts the floor cells and how many distinct ground kinds they show, and the share of the
// commonest one. A map fails when it has fewer than --min-types kinds or one kind covers more than --max-share percent.
// Ground kinds: the map's floor, each distinct non-'.' ground-block character, and the main-grid characters that stand for
// their own ground (--ground-chars, default ",=:X~": grass road walk checker water).
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

export function analyse(text, groundChars = ",=:X~") {
  const L = text.split("\n"), name = (L.find((l) => l.startsWith("map ")) || "map ?").slice(4).trim();
  const gi = L.indexOf("grid"); if (gi < 0) return null;
  const grid = L.slice(gi + 1, gi + 15);
  const gj = L.indexOf("ground");
  const ground = gj >= 0 ? L.slice(gj + 1, gj + 15) : [];
  const WALLISH = new Set(["#", "W", "o", "a", "n", "h", "b", "s", "l", "u", "6", "8", "Z", "E", "D"]);
  const count = new Map(); let floor = 0;
  for (let y = 0; y < 14; y++) for (let x = 0; x < 20; x++) {
    const c = grid[y]?.[x]; if (!c || WALLISH.has(c)) continue;
    floor++;
    const g = ground[y]?.[x];
    const kind = g && g !== "." ? "g:" + g : groundChars.includes(c) ? "c:" + c : "floor";
    count.set(kind, (count.get(kind) || 0) + 1);
  }
  const top = Math.max(0, ...count.values());
  return { name, floor, types: count.size, share: floor ? Math.round((100 * top) / floor) : 0, kinds: Object.fromEntries(count) };
}

export function walk(dir) {
  const out = [];
  for (const e of readdirSync(dir)) { const p = join(dir, e); if (statSync(p).isDirectory()) out.push(...walk(p)); else if (e.endsWith(".map")) out.push(p); }
  return out;
}

if (process.argv[1] && process.argv[1].endsWith("tile_variety.mjs")) {
  const args = process.argv.slice(2), dir = args.find((a) => !a.startsWith("--") && isNaN(+a));
  const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? +args[i + 1] : d; };
  const minTypes = opt("--min-types", 3), maxShare = opt("--max-share", 70);
  const gc = args.includes("--ground-chars") ? args[args.indexOf("--ground-chars") + 1] : ",=:X~";
  if (!dir) { console.error("usage: tile_variety.mjs <world-dir> [--min-types 3] [--max-share 70]"); process.exit(2); }
  const rows = walk(dir).map((p) => analyse(readFileSync(p, "utf8"), gc)).filter(Boolean);
  const bad = rows.filter((r) => r.floor && (r.types < minTypes || r.share > maxShare)).sort((a, b) => b.share - a.share);
  if (args.includes("--json")) console.log(JSON.stringify({ rows, bad }, null, 1));
  else {
    for (const r of bad.slice(0, 40)) console.log(`${r.name.padEnd(22)} ${String(r.floor).padStart(3)} floor cells, ${r.types} kind(s), commonest ${r.share}%`);
    if (bad.length > 40) console.log(`... and ${bad.length - 40} more`);
    const avg = (rows.reduce((s, r) => s + r.types, 0) / Math.max(1, rows.length)).toFixed(2);
    console.log(`tiles: ${rows.length} maps, mean ${avg} ground kinds per map, ${bad.length} bare (fewer than ${minTypes} kinds or one kind over ${maxShare}%)`);
  }
  process.exit(bad.length ? 1 : 0);
}
