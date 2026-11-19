#!/usr/bin/env node
// gdada_next: read a registry, judge every game against gates G0..G5, print the next step.
//   node gdada_next.mjs registry.json [--json]
// Exit: 0 ok, 1 the registry makes an unsupported claim, 2 bad usage.
import { readFileSync } from "node:fs";

export const GATES = ["G0", "G1", "G2", "G3", "G4", "G5"];
// Climbing order: the host check needs no runtime, so it comes before the runtime gate.
export const CLIMB = ["G1", "G0", "G2", "G3", "G4", "G5"];
export const NAMES = { G0: "Runtime", G1: "Host", G2: "Build", G3: "Tests", G4: "Played", G5: "Panel" };
const STEP = {
  G0: (g, b) => b.paused
    ? `runtime search paused (${b.paused}); work source-only: ${g.next_source_only || "plan the next slice"}`
    : `obtain the ${g.backend} runtime (${b.tool || "backend tool"}); every ${g.backend} game is blocked on it`,
  G1: (g) => `make ${g.id} pass the backend host check`,
  G2: (g) => `have the target compiler build ${g.id} and fix what it reports`,
  G3: (g) => `run ${g.id}'s unattended tests in the runtime and fix the failures`,
  G4: (g) => `play ${g.id} in the runtime (person or bot) and record it`,
  G5: (g) => `run a played WHOLE panel round on ${g.id}`,
};

export function judge(reg) {
  const errors = [], rows = [];
  for (const g of reg.games) {
    const b = reg.backends[g.backend];
    if (!b) { errors.push(`${g.id}: backend "${g.backend}" is not registered`); continue; }
    const status = {};
    status.G0 = b.runtime_available
      ? (b.evidence ? "pass" : "invalid")
      : "fail";
    if (status.G0 === "invalid") errors.push(`${g.id}: G0 passes with no evidence on backend ${g.backend}`);
    for (const k of GATES.slice(1)) {
      const e = (g.gates || {})[k] || { status: "unknown", evidence: "" };
      if (e.status === "pass" && !String(e.evidence || "").trim()) {
        errors.push(`${g.id}: ${k} is marked pass with no evidence`);
        status[k] = "invalid";
      } else status[k] = e.status;
    }
    // a pass above a non-pass is unsupported
    let broke = null;
    for (const k of CLIMB) {
      if (status[k] !== "pass" && !broke) broke = k;
      else if (status[k] === "pass" && broke) errors.push(`${g.id}: ${k} passes but ${broke} does not (${status[broke]})`);
    }
    const open = (g.musthaves?.total ?? 0) - (g.musthaves?.verified ?? 0);
    rows.push({ id: g.id, backend: g.backend, status, lowest: broke, open, step: broke ? STEP[broke](g, b) : "done: all gates pass; Extend or Polish next" });
  }
  // order: runtime blockers first, then more open must-haves, then id
  rows.sort((a, z) => (z.lowest === "G0") - (a.lowest === "G0") || z.open - a.open || a.id.localeCompare(z.id));
  return { rows, errors };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const [file, flag] = process.argv.slice(2);
  if (!file) { console.error("usage: gdada_next.mjs registry.json [--json]"); process.exit(2); }
  const reg = JSON.parse(readFileSync(file, "utf8"));
  const { rows, errors } = judge(reg);
  // One game at a time: when the registry names a focus, that game leads and the rest are parked.
  if (reg.focus) rows.sort((a, z) => (z.id === reg.focus) - (a.id === reg.focus));
  if (flag === "--json") console.log(JSON.stringify({ rows, errors }, null, 2));
  else {
    console.log("game".padEnd(18) + GATES.map((k) => k.padEnd(9)).join("") + "open  next step");
    for (const r of rows) console.log(r.id.padEnd(18) + GATES.map((k) => r.status[k].padEnd(9)).join("") + String(r.open).padEnd(6) + r.step);
    for (const e of errors) console.log(`ERROR: ${e}`);
    console.log(reg.focus ? `\nfocus: ${reg.focus} (others parked)` : "");
    console.log(`next: ${rows[0] ? `${rows[0].id}: ${rows[0].step}` : "(no games)"}`);
  }
  process.exit(errors.length ? 1 : 0);
}
