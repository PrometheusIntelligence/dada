---
name: gdada-3d
description: "GDADA method for 3D games, first-person interiors first: choose a renderer the target can afford (a software painter's-algorithm renderer with near-plane clipping, or a GPU one), build rooms and props from boxes, prisms and trim, find click targets by projecting the same geometry that is drawn, cel-shade in 3D (flat fills, two tones, ink edges, flat cast shadows), and measure detail by an edge budget, projection tests and frame time. Use when a game needs a walkable 3D space, when a 3D scene is 'too few edges', or when a 3D look must match concept art. From Last Frequency runs 3 to 6 (TempleOS, HolyC)."
---

# GDADA 3D games

Read [references/lessons.md](references/lessons.md) first and append to it at the end of every 3D run. Also read [references/space-logic.md](references/space-logic.md) (proportions, openings, circulation, the space lint), [references/render-recipes.md](references/render-recipes.md) (how each piece is drawn) and give [references/critic-3d.md](references/critic-3d.md) to the critic. The art style is chosen first (`gdada/references/art-styles.md`); this skill assumes **cel-shaded** unless the owner picked another.

## The loop

1. **Contract.** Write the 3D must-haves in VISION.md with the owner's words (first person or not, walkable or fixed stops, what is clickable, the style, the frame budget).
2. **Pick the renderer by what the target can afford** and write why in a decision record:
   - *Software painter's algorithm* (TempleOS, any CPU-only target): convex polygons, sorted far to near, **clipped at the near plane** (Sutherland-Hodgman on z), back faces culled by normal. Boxes, eight-sided prisms and floor discs cover most interiors.
   - *GPU*: standard; the rest of this skill (edges, targets, tests, critic) still applies.
3. **Space (logic first).** Use the proportions table; make openings recesses; make every stair arrive at a hole; then run the space lint (`templates/space-lint.HC.txt`) before looking at a single render. Details in `references/space-logic.md`.
3b. **Shape.** Build rooms from a few primitives that read at once: a round drum of facets, a floor, a ceiling, furniture as boxes on a ring. One light per room, in a known place. Eye height 1.6 m; remember that near floor objects are below the bottom of the view unless the player looks down: put anything clickable above knee height or give it uprights.
4. **Targets by projection.** The clickable box list is found by projecting the same boxes the picture is drawn from (all eight corners, clamped at the near plane, merged per target id, added far to near so the nearest wins). Never keep a second hand-made hit list.
5. **Cel in 3D.** Flat fills; each surface has a lit tone and a shade tone with a hard edge; an **ink edge on every polygon** (2 px for objects, 1 px for inner marks); one flat cast shadow under every grounded object, same direction and length; lamp light as flat concentric discs and floor pools, never a dotted fade. Shade is chosen per face by orientation; walls by angle to the lamp.
6. **Edges are detail.** In a 16-colour, low-resolution 3D view, detail is the number of distinct edges, not texture. Add architecture (pilasters with base and capital, a ring beam with corbels, cornice, skirting, dado rail, panel mouldings, blind arches, irregular stone courses with a bevel line, ceiling boards and rafters, a rosette), furniture structure (legs, aprons, drawers, slats, battens, posts, shelf boards), and frames (window jambs, lintels, sills; door frames with thresholds). Prefer lines and small boxes to big polygons: lines are cheap.
7. **Measure.** (a) an **edge budget**: count polygons plus lines drawn per view over a sweep of positions and yaws; set a floor from the first measurement and raise it with each pass (Last Frequency: 734 to 1,432 per view in one pass); (b) projection tests: every floor exposes at least N clickable things from the centre, the first view has the focal object mid-screen; (c) **time per view** at the slowest target; (d) the keyboard path still reaches every target after the change.
8. **Show it.** Render from the real target at several positions and yaws (a corner, a wall, a doorway, a stair), not one hero shot. Look for dark-on-dark, floating panels, near-plane wedges, props the same colour as the wall behind them.
9. **Critic round.** At least one independent critic reads the stills (and the concept art if there is some) against the style guide; their objections are applied or named as not applied. State plainly that it was read, not played.
10. **Stop test.** The owner has seen the renders and graded them; edge budget and tests pass; every skipped item is named.

## Water (and other repeating textures)

Water is the thing most likely to read as wallpaper. Design it in `scripts/water_lab.py` first: it renders styles (flat, scallop, layered, hokusai) on the game's palette and prints measures (tones, edges per row, share of unique rows, tile repeat, depth gradient); `--check hokusai` exits 1 under the floors, `--recipe` prints per-band counts to port. Judge by the sheet and the numbers, then draw it in the game with its own primitives. The recipe: six depth bands with a haze, swell lines, jittered scallop rows that grow toward the viewer, foam lace, glitter and lamp reflection animated by tick, a far island, a wake, one big claw-foam crest. Run 12 of Last Frequency: edges per row 0.2 (flat) to 50 (hokusai).

## Traps (each cost a run)

- **Stale layout in tests:** a TAB loop can return at once on a layout from before the camera was set. Tick once after placing the camera.
- **Painter's order:** flat floor items (rugs, puddles) must be drawn before upright items, or a big rug whose centre is nearer overdraws furniture standing behind it.
- **Palette collisions:** if a prop's front tone equals the wall behind it, it melts into the wall whatever the outline. Separate props from walls by hue (warm wood on brick red, cool shade on violet), not by value alone.
- **Staircases:** do not simulate walking up a helix; draw the stair (treads, risers, rail) and teleport with a fade.
- **Pointer at the window edge turns the head**; keep that off any target.
- **A lit disc is an occluder** in a flat renderer: draw halos before objects and keep them small.
- **"Too polygonal":** coarse n-gons read as faceted. Use many narrow quads for curved walls, smooth columns (`V3Cyl`) for round things, depth bands and contact shadows for depth.
- **Ground clutter blocks the walker:** give flat objects (h under 3 cm) no collision.

## Reusable code

The Last Frequency first-person engine lives in the TempleOS fork as `Backend/Lib/View3.HC` and `Gfx.HC` (camera, near-clipped polygon, line, box, prism, wall quad, cast shadow, edge counters). Use it, or port its structure to another target.
