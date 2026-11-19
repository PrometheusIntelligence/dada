#!/usr/bin/env node
// art_guard: a change to one sprite, tile or object must not quietly change another.
//   node art_guard.mjs <art.hc> [more.hc ...] --baseline art-baseline.json [--allow ID,ID,...] [--update]
//   node art_guard.mjs <new.hc> --against <old.hc> [--allow ...]       compare two art files directly (e.g. one from `git show REV:path`)
// Reads every "//NAME" followed by quoted rows of equal length, hashes the rows, and reports what changed against the baseline.
// The baseline is a small JSON { "NAME": "hash" }. A run says in advance which pieces it is allowed to change (--allow); any other
// change, addition or removal is reported as a break and the exit status is 1. After a run is accepted, refresh with --update.
// Shared drawing code (pixlib helpers, palette passes) is the usual cause of a piece changing that nobody touched: this finds it.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";

export function parseAll(text) {
  const out = new Map(); let name = null, rows = [];
  const flush = () => { if (name && rows.length && rows.every((r) => r.length === rows[0].length)) out.set(name, rows); name = null; rows = []; };
  for (const line of text.split("\n")) {
    const h = line.match(/^\/\/([A-Z][A-Z0-9_]+)\s*$/);
    if (h) { flush(); name = h[1]; continue; }
    const r = line.match(/^"([0-9a-fA-F.]{8,})",?\s*$/);
    if (r && name) rows.push(r[1]); else if (name && rows.length) flush();
  }
  flush();
  return out;
}
export const hashes = (art) => Object.fromEntries([...art].map(([k, rows]) => [k, createHash("sha1").update(rows.join("\n")).digest("hex").slice(0, 12)]));

export function compare(base, now, allow = []) {
  const ok = new Set(allow), changed = [], added = [], removed = [];
  for (const k of Object.keys(now)) { if (!(k in base)) added.push(k); else if (base[k] !== now[k]) changed.push(k); }
  for (const k of Object.keys(base)) if (!(k in now)) removed.push(k);
  const bad = (a) => a.filter((k) => !ok.has(k));
  return { changed, added, removed, unexpected: { changed: bad(changed), added: bad(added), removed: bad(removed) } };
}

if (process.argv[1] && process.argv[1].endsWith("art_guard.mjs")) {
  const a = process.argv.slice(2), opt = (k) => (a.includes(k) ? a[a.indexOf(k) + 1] : null);
  const skip = new Set(["--baseline", "--allow", "--against"].flatMap((k) => (a.includes(k) ? [a.indexOf(k) + 1] : [])));
  const files = a.filter((x, i) => !x.startsWith("--") && !skip.has(i));
  if (!files.length) { console.error("usage: art_guard.mjs <art.hc ...> --baseline FILE | --against OLD.hc [--allow IDS] [--update]"); process.exit(2); }
  const now = {}; for (const f of files) Object.assign(now, hashes(parseAll(readFileSync(f, "utf8"))));
  const allow = (opt("--allow") || "").split(",").filter(Boolean);
  let base;
  if (opt("--against")) base = hashes(parseAll(readFileSync(opt("--against"), "utf8")));
  else { const bf = opt("--baseline"); if (!bf) { console.error("need --baseline or --against"); process.exit(2); } base = existsSync(bf) ? JSON.parse(readFileSync(bf, "utf8")) : {}; if (a.includes("--update")) { writeFileSync(bf, JSON.stringify(now, null, 0) + "\n"); console.log(`art_guard: baseline written, ${Object.keys(now).length} pieces`); process.exit(0); } }
  const r = compare(base, now, allow), u = r.unexpected;
  for (const k of u.changed) console.log(`CHANGED  ${k}   (not in --allow)`);
  for (const k of u.added) console.log(`ADDED    ${k}   (not in --allow)`);
  for (const k of u.removed) console.log(`REMOVED  ${k}   (not in --allow)`);
  console.log(`art_guard: ${Object.keys(now).length} pieces; ${r.changed.length} changed, ${r.added.length} added, ${r.removed.length} removed; ${u.changed.length + u.added.length + u.removed.length} unexpected`);
  process.exit(u.changed.length + u.removed.length ? 1 : 0);
}
