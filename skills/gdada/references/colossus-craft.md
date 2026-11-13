# GDADA Colossus run: very large characters and enemies

The **Colossus** run type draws the things that fill a frame: a boss, a god, an enemy shown large in an encounter. It is a sibling of
the **Art** run ([sprite-craft.md](sprite-craft.md)) with its own ledger ([colossus-lessons.md](colossus-lessons.md)). A person-sized
sprite is judged by its silhouette against a cast of similar bodies; a colossus is judged by whether one shape and one empty space
say *enormous* at a glance, and by whether the engine can make it look hurt. A run that does not append a lesson is not complete.

## Use it when

A game has an opponent or a figure that is drawn much larger than the player (a boss, an entity, a monument that moves), typically
64x64 or more, shown in an encounter frame, a cutscene or a title. Mode is chosen as usual; run type is **Colossus**. Ordinary
people and creatures stay in the Art run.

## Inputs

- The **roster**: each colossus with the line in the design that says what it is. Quote the source; never invent what it wants or
  explain it. Where the design says nothing, the colossus stays unexplained and the record says so.
- The **frame**: pixel size (for example 64x64), the on-screen scale, the player sprite's size, how an encounter shows health
  (a gauge, the sprite losing colour, the frame cracking), the palettes and how many colours a figure may use.
- The **viewer and metrics tool**: `cpp-sprites` (`hcviz <game> <out> --metrics --mix 1`) writes `bigs.png` (with a second palette row),
  `bigs_silhouettes.png`, `bigs_1x.png` and appends pairwise near-twin lines to `metrics.txt`.

## Step 0 (Colossus)

1. **Read `colossus-lessons.md` in full** before anything else, and `sprite-lessons.md` for the shared rules. A Frontier item that
   repeats a recorded mistake is a defect of the run.
2. Read the roster quotes. Premortem R0: *how will a player fail to read this as huge, fail to tell two of them apart, or lose the
   figure when the palette changes?*
3. Run the metrics and print the **baseline**: near-twin pairs over all pairs (`0 of 15`, never a bare zero), the closest pair, the
   mean pair distance, and each figure's area and colours.

## The loop (one colossus per pass)

Write the Decision Record **before** drawing:

```
## Move Cn: <colossus>
- Source: the quote that says what it is (or: none, left unexplained)
- Silhouette plan at 64x64 (or the frame size): overall shape family (tower, coil, arch, diagonal, fan, block), bounding box,
  intended fill ratio, where the empty space is
- The one shape that breaks the outline: what sticks out past the mass, and where
- Menace without detail: the negative space (holes, gaps, a cavity that shows the ground) and the scale cue (a repeated
  human-sized unit: a drawer, a chain link, an eye, a step) that makes it enormous
- Tone: bureaucratic / cosmic: what in it is a system (a form, a stamp, a ledger, a stair, a lens) and how it stays unexplained
- Damage states (drawn by the engine, not redrawn): which indices lose colour at stage 1, 2, 3 (for example full colour, then
  the lightest and most saturated indices swapped to gray, then a crack line and a missing chunk), which pixels are crack
  candidates, and what stays readable at stage 3
- Palettes: which indices, and what each becomes under the other palette; which index is the signature colour
- Metric before -> after: nearest neighbour and its distance in px at 64x64; area, bbox fill, enclosed gap pixels, colours
- Result: KEEP | ADAPT | SCRAP
```

Order of levers (cheapest first): **overall shape family, the one outline-breaker, negative space, scale cue, pattern, and only then
colour.** Generate procedurally (ellipses, polygons, thick curves, patterns) so a silhouette can be changed by a number, not
repainted.

## Measurements (print them in the Panel Report)

| Check | How | Pass |
|---|---|---|
| Near twins | `hcviz --metrics`: pixels in one silhouette and not the other, every pair | none closer than 400 px at 64x64 (about 10 percent of the frame; scale the threshold with the area for other sizes) |
| Silhouette-only read | view `bigs_silhouettes.png` | each is named correctly from the flat shape; none is a solid blob (bbox fill under about 85 percent, some enclosed gap) |
| 1x read | view `bigs_1x.png` | the one outline-breaker and the face or focal point are still visible |
| Both palettes | `--mix 1`, view the second row of `bigs.png` | no body merges with the outline; no highlight index turns into a neon outline by accident; the signature colour survives |
| Colour budget | colours per figure, outline excluded | at most 10 |
| Scale | height and width against the player sprite at the same scale | stated (for example 64 rows against 24, 2.7x taller, 4x wider) and a scale cue is present |
| Damage states | the three stages are written in the record and the colour swaps are only palette index swaps | stage 3 still reads as the same creature |
| Frame fit | art touches only rows and columns 1..62, the outline sits on the edge | the host checker (`tools/check_big.mjs`) passes |
| Seen by the person | the renders were shown | their words are logged verbatim as a lesson source |

## Panel seats (exact labels from the graph)

- `Readability: silhouette, contrast, one focal point (Solarski, Drawing Basics and Video Game Art)`
- `Juice it or lose it: feedback in layers (Jonasson and Purho)` (damage states, the sprite losing colour, the frame cracking)
- `Environmental storytelling (Jenkins, Game Design as Narrative Architecture)` (what the creature is made of says what it is)
- `Premortem (Gary Klein, Performing a Project Premortem)` (how the figure fails to read at 1x, in the other palette, or damaged)

## Stop test (Colossus)

- **C1** every pair passes the near-twin threshold, with the count over its denominator, or is a declared twin group.
- **C2** silhouette-only and 1x reads shown for every colossus.
- **C3** both palettes viewed, and any index that behaves badly in the other palette named and fixed or declared.
- **C4** a Decision Record exists for each colossus, including the three damage stages and the colour budget.
- **C5** the person has seen the renders, and what they said is logged.
- **C6** `colossus-lessons.md` was read first and has at least one new entry from this run, each with evidence and a rule; and
  the game still passes its host checks and states art conventions that are still true.

Round cap 3. A gate (no viewer, no metrics, no runtime to see the figure in the encounter frame) is an open item: the run goes on
source-only and says so. Nothing here is judged on a running game unless it was run.
