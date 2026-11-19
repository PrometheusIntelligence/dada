---
name: gdada-pixel-style
description: "GDADA method for making terrain, big procedural buildings and sprites look like one game: one pixel scale, stepped lighting with ordered dither on the ground, three-tone shading and dark outlines on procedural volumes, pixel-snapped vertices, surface courses (masonry, roof tiles) for detail, era-appropriate windows, and per-age styling of the same map data. Use when a 2D or isometric game mixes smooth gradients, flat-filled polygons and pixel sprites, or when a new era or building family must match the existing art."
---

# GDADA pixel style unification

From Tidewatch run 24.

1. **Find the odd ones out.** Screenshot terrain, sprite units and procedural buildings together at game zoom. Whatever is smooth, flat-filled or antialiased among pixel sprites is the problem.
2. **One pixel scale.** The ground shader works in world pixels (`floor(world_pos)`), so one art pixel is one world pixel at any zoom.
3. **Ground:** quantise the lighting factor (not the albedo) into 6 or 7 steps and add an ordered 4x4 Bayer dither at world-pixel scale. Hills become banded shading like the sprites' faces.
4. **Procedural volumes:** snap every vertex to integers; shade each face in three steps (top, left, right) never a gradient; outline each face with a dark tone of its own colour; add surface courses (masonry lines every 3 to 4 px alternating tone, roof courses at thirds); windows by kind (rows for offices, a few for stone, none for barns).
5. **Cast by age (looks only).** Layouts are generated per age (see gdada-procgen); for how a building is drawn, keep map data neutral (style names such as tower, midrise, house, landmark, wall) and cast them in the renderer per era (temple, church, domed hall; stone wall, rampart, barrier).
6. **Compare.** Before and after sheet; say what still mismatches (water, palette, scale of tall buildings against 16 px figures).
7. **Outline rule: big buildings are outlined, terrain is not figure-strength.** Outline every face of a big procedural building with a dark tone of its own colour (as units and props are); without it a building reads as ground. Props use the figures' ink and ramps; foliage is modulated slightly down to sit in the ground's palette.
8. **Themed terrain tiles stay quieter than the figures.** One palette per age (warm olive and ochre with dirt roads for ancient, deep green with cobbles for medieval, brighter meadow with gravel and ruts for revolution), small tufts, flowers and pebbles, water with ripples; the ground is not softened toward its mean, but the first attempt was too busy and was toned down by eye. Check figure against ground on a real screenshot (Tidewatch runs 2, 32, 33).
9. **Earthworks are not green slabs.** Draw a rampart as a brick-faced foot, a stepped earth slope and a glacis apron on the ground; walls with coursing, arrow slits, buttresses and merlons running end to end (run 36).
10. **Cache the detail.** Surface courses cost frame time; draw each structure once into a texture (Tidewatch run 36: 37 to 56 ms a frame down to 1 to 3 ms).
