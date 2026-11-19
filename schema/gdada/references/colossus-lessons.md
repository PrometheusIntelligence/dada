# Colossus lessons (a ledger; read first, append last)

Every Colossus run reads this whole file at Step 0 and appends at least one entry at the end. An entry has a number, a date and a
game, **Evidence** (a measurement or the person's own words) and a **Rule**. Entries are never deleted; a wrong one is
superseded by a later entry that names it. `scripts/check_sprite_lessons.mjs` checks the format (the same one as the Art ledger).

### L1 (2026-11-08, The Holy Temple)
**Evidence:** six 64x64 colossi were built from six different shape families (tower with a crown, spiral coil, stacked blocks, arch,
diagonal stair, horizontal almond with a fan). Every one of the 15 pairs differed by 1016 px or more (mean 1535 px, threshold 400,
about 10 percent of the 4096 px frame); none was close to a twin. The lowest pair involved the block-built Filemaw, the only figure
whose first draft was a near-solid square.
**Rule:** decide the shape family first and give every colossus a different one; the near-twin metric then passes by a wide margin.
Choose families that differ in bounding box and in where the empty space is, not in decoration.

### L2 (2026-11-08, The Holy Temple)
**Evidence:** the pair metric passed the first Filemaw (closest pair 935 px) although its flat silhouette was a solid block with no
visible mouth. The mouth had been painted in index 0, the outline colour, which counts as filled in a silhouette. Cutting it as a
transparent hole with teeth around it raised its closest pair to 1016 px and put 92 enclosed gap pixels in the silhouette.
Enclosed gap pixels per figure after the pass: 76 to 391; fill of the 4096 px frame: 52 to 82 percent.
**Rule:** the pair metric does not catch a blob. Also print bbox fill and enclosed gap pixels, and never paint a void (a mouth, a
cavity, a gap between coils) in the outline colour; leave it transparent so the silhouette keeps the negative space.

### L3 (2026-11-08, The Holy Temple)
**Evidence:** menace came from the shape, not the detail. The coil of Apep leaves 153 enclosed gap pixels between its turns and
reads as a serpent in the flat render with no scales at all; the arch of the Babelworm leaves 391 and is the clearest silhouette of
the six; the crowned Bound One owes its read to a crown that breaks the top edge. The 17 small eyes on the Bound One (2x2 px each)
are the smallest unit in the frame, and repeating them across a head 30 px wide is what makes the head vast.
**Rule:** one outline-breaker and one deliberate empty space per colossus, then repeat a human-sized or smaller unit (an eye, a drawer
8 rows tall, a chain link 2 to 3 px, a step) across the mass; the number of repeats, not the detail in one, carries the scale.

### L4 (2026-11-08, The Holy Temple)
**Evidence:** in the temple palette indices 3 and 8 are 65 and 59 from black in RGB distance (1 is 75, 2 is 97, 5 is 172), so a
body in index 3 almost vanishes into its outline; the first Apep, drawn mostly in index 3, read as a dark ribbon. Swapping the base
to index 2 and keeping 3 for the scale lattice fixed it in both palettes. Index a (pale green in town, 284 from black as fluorescent
in the temple) turned the serpent's belly highlight into a bright green outline; kept, because it reads as a deliberate glow.
**Rule:** do not build a mass out of indices 1, 3 or 8 if it must read in the temple palette; use 2, 5, 7 or 6 for mass, dark indices
for pattern. Treat every use of index a, b, e, f as a glow in the temple and place it on purpose.

### L5 (2026-11-08, The Holy Temple)
**Evidence:** chains drawn with links every 3 px read as scattered dots on the chest and floor of the Bound One; at a 2 px step
with alternating 3x2 and 2x3 links they read as chain even in the 1x render (64 px per figure).
**Rule:** a repeated linear motif (chain, tape, ribs) needs a spacing smaller than the unit's own width, so units touch; check it at 1x.
A scale pattern needs a lattice of period 5 (`(x+y)%5`, `(x-y)%5`) laid over a mask, plus a light upper-left and dark lower-right
edge shade, which gave the serpent its scales with two colours.

### L6 (2026-11-08, The Holy Temple)
**Evidence:** the host checker failed the first Bound One because the crown touched row 1 and the outline, index 0, landed on row 0.
The outline needs a free margin of one pixel, so the drawing is clipped to 1..62 and the outline fills 0..63.
**Rule:** draw colossi inside the frame minus one pixel on every side, clear the border, then outline; a checker must allow
index 0 and nothing else on the frame's edge. Measure with a host script (`tools/check_big.mjs`: rows, widths, quadrants, edge).

### L7 (2026-11-08, The Holy Temple)
**Evidence:** colours per figure after outline were 9, 7, 5, 9, 8, 8 (budget 10); the five-colour Filemaw still reads, because
its material (gray metal, gold handles, red stamps) is limited by what it is.
**Rule:** a bureaucratic creature is made of one material plus one accent (gold handle, red stamp, pale page). Spend colours on
that accent and on the eye, not on shading.

### L8 (2026-11-08, The Holy Temple)
**Evidence:** the person's grades after seeing the first six renders, verbatim: "the eye one is an A as well as the computers monster all others are good idea but bit sloppy so c for snake cthulu worm js b needs work". So: B_THEEYE A, B_FILEMAW A, B_BABELWORM B, B_APEP C, B_BOUNDONE C, B_SEVENTHSTAIR not named (taken as "sloppy", C). The metrics had passed all six (0 of 15 near twins), so the metric did not predict the grades.
**Rule:** the near-twin metric measures distinctness, not quality; the person's grade is the quality gate and an Art or Colossus run is not complete until it is asked for. The two A pieces share one strong concept with one focal point (an eye; a mass built from one repeated unit, the drawer). The pieces graded C and B were good ideas drawn with noisy edges and too many competing details. When redrawing, tidy the edges and cut details before adding any.

### L9 (2026-11-08, The Holy Temple)
**Evidence:** redrawing the four pieces graded B or C (Babel Worm, Apep, Bound One, Seventh Stair) with the two A pieces held byte-identical: dense repeated ribs (two per step at 4 px) read as a picket fence, while one 3 px rib per step at 9 px spacing read as a ribcage; a helix coil built from a tube plus an ownership map gave ragged diamonds and broken rims, while stacked drums with a lit front arc gave a clean coil; a uniform 1 px lit rim on the Bound One put lilac lines in every gap, while a highlight on specific forms did not.
**Rule:** keep the gap wider than the unit; build overlapping coils from layered primitives, not from tubes plus ownership maps; highlight chosen forms, never everything.

### L10 (2026-11-08, The Holy Temple)
**Evidence:** colouring the Babel Worm by arc length along its path (bands from `arc % period`) kept every band perpendicular to the body through the bends; overlay approaches gave radial smears. Unframed eyes merged with neighbouring pale shapes, while one framed unit repeated (a 2x2 eye in a 4x4 socket on a hex grid; an 11x5 socketed eye on each stair riser) read at 1x. A transparent hole in the teeth ring kept the maw cut out of the silhouette.
**Rule:** colour banded bodies by arc length; frame every repeated unit in its own socket; cut voids as transparent holes and give teeth dark gaps so they do not merge into a disc. (The agent's self-grades A- or B+ are not the person's grades; the person grades the redraw.)
