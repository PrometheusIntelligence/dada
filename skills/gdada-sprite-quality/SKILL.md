---
name: gdada-sprite-quality
description: Use when generated pixel sprites (units, soldiers, tiny figures) look "sloppy" or "C grade" to the owner. A grading rubric, a density budget, and an author-then-critic loop that stops self-congratulation.
---

# Sprite quality loop

Lessons from Tidewatch (3D box models baked to 16 facings):

1. **Look at the owner's actual complaint first at the size players see (1x, game zoom), not the author's 6x preview.** A figure that is fine at 6x can be a blob at 1x; the owner judges at 1x.
2. **Density is a budget.** If the sprite is 14 px tall, no amount of care draws faces, belts or weapon heads. Raise the pixel density first (we upscale small models 2x in the bake step, so 0.5-unit parts become 1 px), then ask authors to spend it on detail. Keep the on-screen size sane.
3. **A rubric beats "make it better".** Write it down (silhouette, anatomy, 3 details per unit, value structure, team colour area on every facing, facing consistency, era truth against concept art, pixel hygiene) and grade A/B/C per unit. Ship only A.
4. **Authors grade themselves too kindly.** After an author stops, a different agent who did not draw it grades every unit from renders (6x and 1x, 8 facings) next to the concept art and returns a defect list per unit; send it back to the author. Two rounds at least.
5. **One file per author, hooked by an `apply(UNITS)` list** so parallel agents never collide; the lead builds the shared bake once and reports honestly what was viewed and what was measured.
6. **Make a contact sheet of the real baked frames (from the final json), not of the intermediate sheet**; crop errors in sheet tools produced misleading previews once.

7. **Scale to the world after the density.** Dense figures grew past the buildings ("units way too large for building scale"). Decide the figure-to-storey ratio when you set the budget (a man is about one storey beside a house) and re-render pixel-aligned, not resampled, to fit.
8. **Thin things vanish.** Weapon shafts 2 px with bright heads; check the canvas edge at facings that point toward or away from the camera.
9. **A global finding is fixed in the shared tool.** A pale team ramp was fixed once in the bake and the renderer, not in three author files.
10. **Say which grades are self-grades.** Authors graded A- to B+ where the critic graded C+; four rounds still ended with self-grades for the best figures and no critic re-grade.
11. **Concept comparison is skipped unless required.** Authors skipped it in rounds 2 to 4; the brief must demand a "what still differs" line per unit.
12. **Battle legibility.** Hairline health bars shown only when hurt or selected, a soft team disc rather than rings, dust and smoke at half opacity, terrain quieter than figures.

Rubric used: see design/SPRITE-RUBRIC.md in the Tidewatch repo.
# Sprite rubric (every unit, every facing)

Graded A/B/C by a critic who has NOT drawn the sprite. A unit ships only at A. Look at facings 0,2,4,6,8,10,12,14 at 6x AND at 1x on green AND beside design/reference concept art.

1. Silhouette: unit kind is identifiable from a black silhouette alone, at 1x, at every facing; weapon/shield/mount extend past the body.
2. Anatomy: head, torso, arms, legs readable as separate shapes (value step between them); hands visible holding the weapon; feet/greaves/boots; no "box with a hat".
3. Equipment detail the era needs: helmet type with face/visor or brim, armour layers (mail/plate/tabard/belt/straps), shield device, weapon head, quiver, canteen, pack, cloak folds. At least 3 distinct details per unit beyond the body.
4. Value structure: at most 3 tones per material + one dark outline, a clear light side (top-left), no 1-pixel speckle, no noisy dithering; large clean colour blocks.
5. Team colour: one big readable area (tabard, shield face, cloak, plume) on EVERY facing, never speckle; faction emblem not required to be legible.
6. Facing consistency: the 16 facings look like the same figure turning (equipment on the same side, no pops, no clipped weapon at canvas edge).
7. Era truth against the concept art: costume/colour palette matches the era sheet; no medieval knight in revolution cut etc.
8. Pixel hygiene: no orphan pixels, no jagged 1px staircases on long weapons where a clean 2px line works, consistent outline.
