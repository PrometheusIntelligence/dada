# Reuse the part that was good, not the part that was easy

Written 2026-11-18 from two runs graded by the owner: LearnAPI (A-) and LearnSQL (B: "looks like the old design for the Docker one, kind of; the design JS is OK but the colors suck").

## What happened
LearnSQL was built by copying LearnAPI's machinery (build script, check script, floor probe, panel brief) and, with it, LearnAPI's *look*: a dark slab hero, a flat prose column below, the same header, the same card and table styling, a night-coloured ground. Every measurement passed. The panel found real defects in claims, scale and accessibility. Nobody asked the one question the owner asked at a glance: **does this look like the last site?** It did, and the owner had already seen that look on LearnDocker.

The palette had the same shape of failure. The rule says to derive the palette from the topic's own colour system. The run did: Solarized (the colours SQL editors use), retuned until every pair measured dE >= 30 and every hue passed contrast. It was sourced, measured, and ugly: olive, mustard and teal-black. The rule produces a *defensible* palette, not a *good* one. LearnAPI's palette, derived the same way from Swagger's method colours, was graded A-. Same method, different result, so the method is not the guarantee; looking is.

## Traps
1. **Copying the skeleton copies the look.** Layout, ground colour, hero composition and type pairing travel together with the build scripts. A new subject then arrives dressed as the previous one.
2. **Measured is not good.** dE >= 30 and 4.5:1 prove a palette is distinguishable and legible. They say nothing about whether it is pleasant, or distinct from the sibling sites.
3. **The panel judges the run it is shown.** Six seats argued over claims and craft and none was briefed to compare against earlier work, so the sameness was invisible to them.
4. **One reused good idea is not a reused good design.** The Row Flow, the step player and the runner were fine (the owner kept "the design JS"). The colour and the page frame were not.

## What to reuse, and what not to
| Reuse (it was good) | Do not reuse (it was easy) |
|---|---|
| The measuring harness, check script, tamper probes, floor probe | The hero composition (slab + figure + tiles) |
| Deploy files, `fluid.json`, `.vercelignore`, root redirect | The ground colour and the zone scheme |
| Interaction code that earned praise (step player, runner, menu) | The palette family, or the palette method run mechanically |
| Content rules: every figure recomputed, every quotation verified | Type pairing, nav pattern, card and table skin |
| Panel seats and their briefing | The first-screen form: a second sibling site should not open with the same kind of figure |

## Rules for a run
- **Sibling test (R0).** Before the first move, list the sibling sites (same author, same run family) and put their first-screen screenshots beside the new site's first spike. If the ground colour family, the hero composition and the palette family all match, the run fails R0 and the first move is to change them. Record the result in the Traversal Plan.
- **Name what you reuse.** The Traversal Plan lists which parts are carried over from a sibling and why each earned it. Everything not listed is designed fresh.
- **Pick a palette by looking.** Derive two or three candidate palettes from the topic (different sources, or different grounds), render the same hero in each, and choose by eye against the best-graded palettes on record (Internet Structure's TIA-598 on cable-jacket night; LearnAPI's tuned Swagger hues). Then measure the winner. Measuring picks nothing; it only vets.
- **Vary the ground between siblings.** If the last site was dark, the next opens light, or the reverse.
- **Brief one seat to compare.** Seat a critic whose duty is "does this repeat the previous site?" with the sibling's screenshot in the evidence file.
- **Reuse is a decision record**, not a default: one line per carried-over part, with the grade it came from.

## Lesson from Done by 6 (2026-11): the first pass was "very basic, boilerplate"
- A clean, correct, accessible SaaS look is not a design. The first redo passed the Mobile Floor and still read as a template. Passing the floor is a gate, not a direction: pick a single idea that only this product could have (here, the day as a 12-hour clock with 6 at the bottom, the page background as the sky at the rep's time) and let it drive colour, header, dial and copy.
- Make the idea live on the data: the dial uses the real day, excludes example data, and has its own copy for weekend, before-start, during and after-hours.
- Re-check every state the idea creates. A time-of-day sky means text on bare sky flips colour at night; any text that sits outside a panel must use the sky's text colour, and fixed-colour links or help text must sit on a panel. This was found only by repeating the contrast measurement across time states, because it failed on some runs and passed on others.
- Keep the one thing the owner liked (the proposal's little clock) and rebuild everything around it.
