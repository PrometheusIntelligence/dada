---
name: dada-app
description: "DADA for apps and data viewports: use with the dada skill when the artifact is an application, dashboard, map or other data viewport read in a browser and on a phone, not a marketing site. Adds the app-specific run: a phone-first first-screen probe, marks sized in screen pixels, honest data marks (area proportional to count, legend equals what is drawn, references kept out of totals), floors held by tests, a claims check after every doc edit, and the panel seats an app needs (measurement, usability, claims, data-graphic, inclusion, phone interaction). Triggers: polish or review an app, dashboard, map, operator console, data viewport; make it clear and beautiful on a phone; run the panel on an app."
---

# DADA-App: the DADA run for applications and data viewports

DADA's traversal (living Frontier, WHOLE rounds, stop conditions S1 to S5, one agent per literary reference, no move
quota) is unchanged: read the `dada` skill first and follow it. This skill only adds what an
**application** needs that a website does not. It was written from the OperatorOS world-picture polish run (three
panels, five seats, 36 browser checks); the measured facts behind each rule are in
[references/app-lessons.md](references/app-lessons.md).

## When to use it
Use it when the artifact is read in a browser and **acts on data**: a dashboard, an operator console, a map with
layers, a timeline, a table of records. Use plain `dada` for a site with pages and a landing; use both when an app
also has public pages (the landing rule belongs to the site, the rules below to the app).

## What an app run adds (in the order a run meets them)

### R0: measure before the panel sits
1. **Serve the built app** (`npm run build && npm run preview`) and keep it running; seats read the same build.
2. **Run the first-screen probe** at 390x844 and 375x812 (phone, touch) and at 1280x800 and 1440x900:
   `NODE_PATH=$(npm root -g) node skills/dada-app/scripts/floor_probe.cjs --url http://127.0.0.1:4190/ --ready '<selector of the first mark>' --map '<selector of the map or main viewport>' --marks '<every kind of mark, comma-separated>' --out R0/floor.json`
   List **every** kind of mark in `--marks` (for OperatorOS: `.event-marker, .cluster-marker, .world-war-marker, .mesh-marker, .drone-marker`): marks are held to 24px, everything else to 44px, so a mark kind left out is miscounted as a failing control (58 false failures at 390x844 until all five kinds were listed).
   It reports the Mobile Floor rows M1, M3, M4, M5, M7, M8, whether the **viewport starts above the fold and marks are
   visible without scrolling**, the bytes transferred before the viewport is usable (and the largest request), and
   tap targets of the marks themselves. It carries a fixture that must fail (an 8px label, a 20px button, a 10px
   input); if the fixture is not reported, the probe is broken and no number from it counts.
3. **Write the evidence file** from [references/evidence-template.md](references/evidence-template.md): what the
   artifact claims about itself (its docs and labels), the screenshots (opened and checked, not tiled), the numbers,
   the tests, and what has not been run. A seat is briefed with that file and nothing the conductor believes.
4. **Seat the panel** with [references/app-panel.md](references/app-panel.md). Required for an app: Cairo (measures,
   runs the probe and the tests, audits claims), Krug (five-second test and a traced mark on the first screens),
   Debord (claims check), Tufte (instrumentation, for any data graphic), Mace (inclusion), plus a phone-interaction
   seat for anything read on a phone. Launch three at a time, each filing `panel-R<n>/<seat>.md`.

### The moves an app run reaches for (each came from a finding that recurred)
- **Size marks in screen pixels.** Divide by the drawn scale (`u = px / (svgWidth / viewBoxWidth)`); use
  `vector-effect: non-scaling-stroke`. A 6-unit glyph is 2px on a phone.
- **Phone first screen is the design.** Controls that are not the data fold behind one labelled button (Filters);
  the sidebar becomes one labelled scrolling row; the viewport takes the data's own proportions; the key and a
  one-line hint sit with the viewport. Measure the result; a layout push that moves the viewport *down* is reverted.
- **Honest marks.** Area proportional to the number it encodes (state the minimum and the cap), a mixed group shows
  its shares, no non-data ink (halos, pulses), the legend lists everything drawn and **equals what is drawn**, one
  count source for legend, layer list and footer, and anything that is a *reference* rather than an *observation* is
  drawn differently, counted on its own line and never inside a group.
- **Floors are held by tests.** A stylesheet test (`no font-size under 12px`, `no bare 100vh`, floors sheet imported
  last) plus the rendered probe as an npm script; the docs say which command runs which floor.
- **Access.** Skip links first in the page; a visible focus ring on every kind of mark; names on every control; 44px
  controls on coarse pointers, 24px marks.

### After every edit to a doc or a label, not only the last
**Re-run Step 2g.** In the OperatorOS run three of four claims-seat findings in the last round were numbers that had
moved after the edit that wrote them. A figure in prose is re-measured by the command that produced it, right after the
edit that could change it. See [references/claims-check.md](references/claims-check.md).

### Close
Write the five DADA artifacts in `DESIGN-LOG.md`, the facts about the medium in `CARRY-FORWARD.md`, and state what
the run did **not** cover (no screen reader, no real phone, harnesses not run). A run that ends at the round cap with
S2 or S3 unmet says so and names the resume point.

## Not covered by this skill
Backends, data pipelines and performance beyond the first-screen bytes; those are findings to log as DEFERRED (out of
run type) and offer as a Full run.
