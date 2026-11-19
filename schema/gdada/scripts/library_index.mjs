#!/usr/bin/env node
// library_index: the sprite library as a catalogue: every sprite, object, tile and colossus the game has, when it was added, and its grade.
//   node library_index.mjs --art Src/ArtTile.HC Src/ArtSpr.HC Src/ArtBig.HC --grades art-grades.json --ledger library-ledger.json \
//        --batch "eldritch-1" [--out-json design/sprite-library.json] [--out-md design/SPRITE-LIBRARY.md]
// The ledger { "ID": { "added": "2026-11-10", "batch": "eldritch-1" } } remembers when each piece first appeared; this run adds new ones under --batch.
// The grades come from art-grades.json (the person's, never ours). The markdown groups by kind and shows counts, so the library can be seen to grow.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { parseAll } from "./art_guard.mjs";

export function kindOf(id) {
  if (id.startsWith("S_")) return "sprite"; if (id.startsWith("B_")) return "colossus"; if (id.startsWith("T_")) return "tile";
  if (id.startsWith("O_")) return "object"; return "other";
}
export function build(art, grades, ledger, batch, today) {
  const by = Object.fromEntries((grades?.items || []).map((i) => [i.id, i]));
  const rows = [];
  for (const [id, rows16] of art) {
    if (/^O_.*U{1,2}$/.test(id) && art.has(id.replace(/U{1,2}$/, ""))) continue;          // upper cells are part of their object
    if (!ledger[id]) ledger[id] = { added: today, batch };
    const g = by[id] || by[id.replace(/\d+$/, "1")];
    rows.push({ id, kind: kindOf(id), size: `${rows16[0].length}x${rows16.length}`, added: ledger[id].added, batch: ledger[id].batch, grade: g?.grade || "", status: g?.status || "" });
  }
  rows.sort((a, b) => a.kind.localeCompare(b.kind) || a.added.localeCompare(b.added) || a.id.localeCompare(b.id));
  return rows;
}
export function markdown(rows, today) {
  const kinds = [...new Set(rows.map((r) => r.kind))];
  let md = `# Sprite library\n\nGenerated ${today} by gdada \`library_index.mjs\`. Grades are the person's; blank means not yet graded.\n\n`;
  md += "| kind | pieces | graded | A or A- | |\n|---|---|---|---|---|\n";
  for (const k of kinds) { const r = rows.filter((x) => x.kind === k); md += `| ${k} | ${r.length} | ${r.filter((x) => x.grade).length} | ${r.filter((x) => /^A/.test(x.grade)).length} | |\n`; }
  md += `| **total** | ${rows.length} | ${rows.filter((x) => x.grade).length} | ${rows.filter((x) => /^A/.test(x.grade)).length} | |\n`;
  for (const k of kinds) {
    md += `\n## ${k === "colossus" ? "colossi" : k + "s"}\n\n| id | size | added | batch | grade |\n|---|---|---|---|---|\n`;
    for (const r of rows.filter((x) => x.kind === k)) md += `| ${r.id} | ${r.size} | ${r.added} | ${r.batch} | ${r.grade} |\n`;
  }
  return md;
}

if (process.argv[1] && process.argv[1].endsWith("library_index.mjs")) {
  const a = process.argv.slice(2), opt = (k) => (a.includes(k) ? a[a.indexOf(k) + 1] : null);
  const ai = a.indexOf("--art"); const files = []; for (let i = ai + 1; i < a.length && !a[i].startsWith("--"); i++) files.push(a[i]);
  const art = new Map(); for (const f of files) for (const [k, v] of parseAll(readFileSync(f, "utf8"))) art.set(k, v);
  const grades = opt("--grades") && existsSync(opt("--grades")) ? JSON.parse(readFileSync(opt("--grades"), "utf8")) : { items: [] };
  const lf = opt("--ledger"), ledger = lf && existsSync(lf) ? JSON.parse(readFileSync(lf, "utf8")) : {};
  const today = new Date().toISOString().slice(0, 10), batch = opt("--batch") || "unlabelled";
  const rows = build(art, grades, ledger, batch, today);
  if (lf) writeFileSync(lf, JSON.stringify(ledger, null, 1) + "\n");
  if (opt("--out-json")) writeFileSync(opt("--out-json"), JSON.stringify(rows, null, 1) + "\n");
  if (opt("--out-md")) writeFileSync(opt("--out-md"), markdown(rows, today));
  console.log(`library: ${rows.length} pieces (${[...new Set(rows.map((r) => r.kind))].map((k) => rows.filter((r) => r.kind === k).length + " " + k).join(", ")})`);
}
