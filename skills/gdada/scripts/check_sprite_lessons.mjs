#!/usr/bin/env node
// check_sprite_lessons: every lesson has a number, a date and a game, Evidence and a Rule; numbers are consecutive.
//   node check_sprite_lessons.mjs [path]   exit 0 ok, 1 malformed
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
export function check(text) {
  const errors = [], blocks = text.split(/^### /m).slice(1);
  if (!blocks.length) errors.push("no lessons");
  blocks.forEach((b, i) => {
    const m = b.match(/^L(\d+) \((\d{4}-\d{2}-\d{2}), ([^)]+)\)/);
    if (!m) { errors.push(`block ${i + 1}: heading must be 'L<n> (<date>, <game>)'`); return; }
    if (+m[1] !== i + 1) errors.push(`L${m[1]}: expected L${i + 1}`);
    if (!/\*\*Evidence:\*\*\s*\S/.test(b)) errors.push(`L${m[1]}: no Evidence`);
    if (!/\*\*Rule:\*\*\s*\S/.test(b)) errors.push(`L${m[1]}: no Rule`);
  });
  return { count: blocks.length, errors };
}
if (import.meta.url === `file://${process.argv[1]}`) {
  const p = process.argv[2] || join(dirname(fileURLToPath(import.meta.url)), "..", "references", "sprite-lessons.md");
  const { count, errors } = check(readFileSync(p, "utf8"));
  for (const e of errors) console.log("ERROR:", e);
  console.log(`sprite lessons: ${count} entries, ${errors.length} problems`);
  process.exit(errors.length ? 1 : 0);
}
