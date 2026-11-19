#!/usr/bin/env node
// npc_check.mjs <cast dir> -- the NPC run's check.  Exit 1 on any failure.  See references/npc-craft.md.
import fs from "node:fs"; import path from "node:path";
const dir = process.argv[2] || "cast"; const files = [];
(function walk(d) { for (const f of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, f.name); if (f.name === "presets") continue; f.isDirectory() ? walk(p) : p.endsWith(".json") && files.push(p); } })(dir);
const cast = files.map(f => ({ f, d: JSON.parse(fs.readFileSync(f, "utf8")) })); const ids = new Set(cast.map(c => c.d.id)); const errs = [], notes = [];
const presetDir = path.join(dir, "presets"); const presets = fs.existsSync(presetDir) ? new Set(fs.readdirSync(presetDir).map(f => f.replace(/\.json$/, ""))) : null;
const need = ["id", "name", "region", "home", "sprite", "species", "role", "look", "mind", "voice", "behavior", "relationships", "lines"];
const strict = cast.filter(c => c.d.lines && c.d.lines.length && c.d.voice);   // people who have been through an NPC run
const FORMS = ["address", "gossip", "notice", "question", "inventory", "fragment", "anecdote", "surroundings", "numbers", "formal", "chatty", "nonsequitur", "stage"];
const WHEN = /^(first_meeting|returning|late_night|morning|afternoon|evening|mind_low|mind_high|many_questions|mask_any|mask:\d+|talked:\d+|random:\d+|holding:\w+|flag:\w+|asked:\w+|answered:\w+|in_company_of:\w+|past_runs:\d+|past_robbed|past_ending|opinion:(trust|respect|fear|curiosity)(>=|<=)-?\d+)$/;
let linesAll = 0, firstAll = 0;
const owner = new Map(), shingles = new Map();
for (const { f, d } of strict) {
  for (const k of need) if (d[k] === undefined || d[k] === null || d[k] === "") errs.push(`${d.id}: missing ${k}`);
  if (!d.look || !d.look.distinct) errs.push(`${d.id}: look.distinct`);
  if (d.mind) { for (const k of ["traits", "want", "fear", "secret", "keeps"]) if (!d.mind[k]) errs.push(`${d.id}: mind.${k}`); if ((d.mind.traits || []).length !== 3) errs.push(`${d.id}: three traits`); }
  if (d.voice) { for (const k of ["register", "diction", "never_says", "sample"]) if (!d.voice[k] || !d.voice[k].length) errs.push(`${d.id}: voice.${k}`); if ((d.voice.diction || []).length < 2) errs.push(`${d.id}: voice.diction needs 2 rules`); }
  if (d.behavior && (!d.behavior.routine || !(d.behavior.reacts || []).length)) errs.push(`${d.id}: behavior.routine and reacts`);
  if (!FORMS.includes((d.voice || {}).form)) errs.push(`${d.id}: voice.form must be one of ${FORMS.join("/")}`);
  const R = (d.behavior || {}).reacts || []; if (R.length < 5) errs.push(`${d.id}: ${R.length} reacts, want 5 or more`);
  for (const r of R) if (!WHEN.test(r.when || "")) errs.push(`${d.id}: bad react when "${r.when}"`);
  if (new Set(R.map(r => (r.when || "").split(":")[0])).size < 3) errs.push(`${d.id}: reacts use fewer than 3 kinds of trigger`);
  const L = d.lines || [];
  { const first = L.filter(l => /(^|[\s"(])I(\b|')/.test(l.text || "")).length; linesAll += L.length; firstAll += first; if (L.length && first / L.length > 0.4) errs.push(`${d.id}: ${first} of ${L.length} lines say I (max 40%)`); } if (L.length < 4 || L.length > 8) errs.push(`${d.id}: ${L.length} lines, want 4-8`);
  for (const l of L) {
    const t = l.text || ""; for (const seg of t.split("|")) if (seg.length > 72) errs.push(`${d.id}: a line segment is ${seg.length} columns`);
    if (owner.has(t) && owner.get(t) !== d.id) errs.push(`${d.id}: line copied from ${owner.get(t)}: "${t.slice(0, 40)}"`); owner.set(t, d.id);
    const w = t.toLowerCase().replace(/[^a-z' ]/g, " ").split(/\s+/).filter(Boolean);
    for (let i = 0; i + 6 <= w.length; i++) { const s = w.slice(i, i + 6).join(" "); if (!shingles.has(s)) shingles.set(s, new Set()); shingles.get(s).add(d.id); }
  }
  if (d.voice && d.voice.sample && L.some(l => l.text === d.voice.sample)) errs.push(`${d.id}: voice.sample must differ from every line`);
  for (const r of d.relationships || []) if (!ids.has(r.with)) errs.push(`${d.id}: relationship to unknown ${r.with}`);
  if ((d.relationships || []).length && !(d.relationships || []).some(r => { const o = cast.find(c => c.d.id === r.with); return o && o.d.region !== d.region; })) notes.push(`${d.id}: no relationship crosses a region`);
  if (presets && d.species && !presets.has(d.species)) errs.push(`${d.id}: species ${d.species} has no preset (cast/presets/${d.species}.json)`);
  if (d.species && d.species !== "human" && !(d.look && /reptil|lizard|jackal|ibis|falcon|cat-headed|ram-headed|crocodile|smooth|featureless|blank|faceless|fox|wolf|bear|rat|goat|hippo|owl|cobra|lion|baboon|vulture|bull|frog|hare|beetle|carapace|horn|whisker|scale|snout|beak|feather|crest|bird|screen|lens|robot|shadow|stone|wing|tail|metal|antenna/i.test(d.look.distinct || ""))) errs.push(`${d.id}: species ${d.species} but look.distinct shows none`);
}
for (const [s, who] of shingles) if (who.size >= 3) errs.push(`template voice: "${s}" in ${[...who].slice(0, 4).join(", ")}`);
const faceKey = c => JSON.stringify([c.d.look && c.d.look.skin, c.d.look && c.d.look.hair_style, c.d.look && c.d.look.hair_color, c.d.look && c.d.look.hat, c.d.look && c.d.look.top, c.d.look && c.d.look.color, c.d.mind && c.d.mind.traits && c.d.mind.traits[0]]);
const seen = new Map(); for (const c of strict) { const k = faceKey(c); if (seen.has(k)) errs.push(`clones: ${seen.get(k)} and ${c.d.id}`); else seen.set(k, c.d.id); }
const tally = k => { const m = {}; for (const c of cast) { const v = c.d.look && c.d.look[k]; m[v] = (m[v] || 0) + 1; } return Object.entries(m).sort((a, b) => b[1] - a[1]).slice(0, 4).map(([a, b]) => `${a}:${b}`).join(" "); };
console.log(`first-person lines: ${firstAll} of ${linesAll} (${Math.round(100 * firstAll / Math.max(1, linesAll))}%, max 35%)`); if (linesAll && firstAll / linesAll > 0.35) errs.push("too many lines say I overall");
console.log(`npc_check: ${cast.length} people, ${strict.length} through an NPC run;`, "hats", tally("hat"), "| hair", tally("hair_style"), "| tops", tally("top"));
for (const n of notes.slice(0, 10)) console.log("note:", n);
if (errs.length) { for (const e of errs.slice(0, 80)) console.log("FAIL:", e); console.log(`npc_check: ${errs.length} problem(s)`); process.exit(1); }
console.log("npc_check: PASS");
