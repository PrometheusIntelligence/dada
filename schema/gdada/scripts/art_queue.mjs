#!/usr/bin/env node
// art_queue: what the next Art or Colossus run should work on, from the person's grades.
//   node art_queue.mjs [art-grades.json] [--json]
// Order: (1) redrawn pieces waiting for a grade, (2) assigned pieces below A, lowest grade first, (3) graded below A,
// (4) praised but never graded, (5) the wishlist (assigned, then open). A piece leaves the queue only when it is graded A.
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ORDER = { F: 0, D: 1, C: 2, B: 3, A: 4 };
// a grade is a letter A to F with an optional + or - (B+ sits between B and A)
export const rank = (g) => ORDER[g[0]] + (g[1] === "+" ? 0.4 : g[1] === "-" ? -0.4 : 0);
const validGrade = (g) => /^[A-F][+-]?$/.test(g);
export function queue(data) {
  const q = [];
  const below = (it) => it.grade && rank(it.grade) < ORDER.A;
  for (const it of data.items) if (it.status === "redrawn_awaiting_grade") q.push({ rank: 1, why: `redrawn, awaiting the person's grade (was ${it.previous || it.grade})`, id: it.id });
  const rest = data.items.filter((it) => it.status !== "redrawn_awaiting_grade" && below(it)).sort((a, z) => rank(a.grade) - rank(z.grade));
  for (const it of rest) q.push({ rank: 2, why: `graded ${it.grade} ("${it.said}")${it.task ? ": " + it.task : ""}`, id: it.id });
  for (const it of data.items) if (it.status === "praised_ungraded") q.push({ rank: 3, why: `praised, never graded: ask for grades (${it.note || ""})`, id: it.id });
  for (const w of data.wishlist || []) if (w.status === "drawn_awaiting_grade") q.push({ rank: 1, why: `drawn, awaiting the person's grade (${w.kind})`, id: w.id });
  for (const w of data.wishlist || []) if (w.status !== "done" && w.status !== "drawn_awaiting_grade") q.push({ rank: 4, why: `${w.status}: wished by ${w.source} (${w.kind})`, id: w.id });
  return q;
}
export function check(data) {
  const errs = [], ids = new Set();
  for (const it of data.items) {
    if (ids.has(it.id)) errs.push(`duplicate id ${it.id}`); ids.add(it.id);
    if (it.grade && !validGrade(it.grade)) errs.push(`${it.id}: grade ${it.grade} is not A to F (with an optional + or -)`);
    if (it.grade && !it.said) errs.push(`${it.id}: a grade must carry the person's words (said)`);
  }
  return errs;
}
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2).filter((a) => a !== "--json");
  const p = args[0] || join(dirname(fileURLToPath(import.meta.url)), "..", "references", "art-grades.json");
  const data = JSON.parse(readFileSync(p, "utf8")), errs = check(data), q = queue(data);
  if (process.argv.includes("--json")) console.log(JSON.stringify({ queue: q, errors: errs }, null, 2));
  else {
    const graded = data.items.filter((i) => i.grade);
    const counts = Object.fromEntries(Object.keys(ORDER).map((g) => [g, graded.filter((i) => i.grade[0] === g).length]));
    console.log(`art grades: ${graded.length} graded (${Object.entries(counts).map(([g, n]) => `${g}:${n}`).join(" ")}), queue ${q.length}`);
    for (const e of errs) console.log("ERROR:", e);
    for (const x of q) console.log(`  [${x.rank}] ${x.id.padEnd(16)} ${x.why}`);
  }
  process.exit(errs.length ? 1 : 0);
}
