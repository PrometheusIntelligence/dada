# Art style guides (a list that grows)

Every game picks **one style** in its `VISION.md` before art starts, and writes the pick in the log with the owner's words. A style is a set of rules a critic can check, not a mood. Add a guide here when a game commits to a new style; do not edit a guide to excuse a piece that breaks it. Each guide names: **the rules**, **what to measure**, **what to reject**, and **where it was used**.

Entries are in the order they were adopted. The newest is at the bottom.

## 1. Pixel (hard-edged, low palette)
**Rules:** a fixed small palette (8 to 16 colours), no anti-aliasing, features built from rectangles and lines on the pixel grid; silhouette first; light from one direction; selective outline only where a shape meets a same-value ground; dither is allowed and is a deliberate texture.
**Measure:** distinct colours used; the silhouette test (flat one colour); pair distance between sprites; the 1x read.
**Reject:** soft gradients, mixed pixel sizes, a sprite that needs colour to read.
**Used:** the earlier gdada games; Tidewatch; the first two runs of Last Frequency.

## 2. Cel-shaded (flat colour, hard shade, ink line)
**Adopted:** 2026-11-27 for *Last Frequency* (owner: "I like cell shaded look, lets go with that for this game").
**Rules:**
1. **Flat fills only.** No halftone, no dither, no gradients. A glow is a stack of hard-edged flat shapes, never a dotted fade.
2. **Two tones per surface**: a lit tone and one shadow tone, with a hard terminator between them. A third tone is a rim or a highlight, and only a thin one. Every surface has the same light direction (upper left for outdoors; the nearest lamp indoors).
3. **An ink line** around every object (1 px for small things at 1x, 2 px for large ones), darker than any fill it touches, unbroken at silhouettes, thinner inside (panel lines are 1 px, the outer line is 2 px).
4. **Cast shadows are shapes**: one flat dark parallelogram per object on the ground, the same length and direction for everything lit by the same lamp.
5. **Details are graphic marks, not texture**: a row of windows, a band, a rivet line; no noise.
6. Palette ramps are shared: each hue has `light / base / shade` slots, chosen once; add a new hue only with a shade.
**Measure:** (a) count distinct colours per object (<= 3 plus ink); (b) count dithered or noisy pixels (target 0); (c) outline continuity on the silhouette (every boundary pixel against the ground is the ink colour); (d) a shadow shape exists under every grounded object; (e) the silhouette-only render still matches the metrics of the pixel run.
**Reject:** fuzzy glows, stippled smoke, gradients, a shade that is a darker copy of the fill with no terminator, an outline that changes weight at random.
**Used:** *Last Frequency* from run 4 (ships, first-person interior, UI paper).

## 3. Painterly (reserved)
Soft edges, brush-like fills, colour temperature carrying light. Not adopted by any game yet. Write the rules the first time a game asks for it.

## 4. Line and tone (reserved)
Engraving or woodcut: hatching carries shade, a single ink colour on paper. Not adopted by any game yet.

## How to add a style
1. Write the rules and the measures above in the same shape.
2. Show the owner one object in the style and the same object in the nearest existing style, side by side.
3. Log the owner's pick with their words, in the game's VISION.md and in the log.
