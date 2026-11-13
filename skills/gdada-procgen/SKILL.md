---
name: gdada-procgen
description: "GDADA playbook for procedural maps and cities in a game: terrain from real processes (domain warp, ridged noise, erosion, flow-accumulation rivers, biomes), cities from districts (core, ring, harbour, industry, residential) with roads, bridges, walls and gates, settlements that follow valleys; with preview-first iteration, a stats table, many-seed sweeps, connectivity validation and a contract between generator modules. Use when asked to improve map generation, make maps age-specific (castles, walled towns, star forts), port a generator, add map types, make urban or rural layouts, or make maps look natural."
---

# GDADA procedural generation

From Tidewatch: nine map types, a city of districts, villages, walls with gates.

## Method

1. **See it first.** Write a preview tool before the generator: shaded height plus tile colours (and structures as shaded boxes) to a PNG, and read it. Judge by eye at small size; numbers lie about pretty.
2. **Processes, not noise alone.** Domain-warped fbm for shape; ridged noise for ranges; thermal and a few hydraulic passes so slopes soften; rivers by flow accumulation from highlands to sea; lakes in basins; coasts with a tidal band; plateaus with cliff rims and a few ramps; biomes from elevation and moisture.
3. **Distinct kinds.** Each map kind needs a one-sentence identity and a measurable fingerprint (height spread, water fraction, forest fraction, longest cliff, land regions). Flat maps are flat on purpose (spread under 8); every other kind has real relief (spread 15+).
4. **Cities are districts.** Pick centres (core first, spacing 24+), terrace the ground under each, give each its own street grid and block size, height by distance from the core, capturable buildings few and spread, the rest scenery. Avenues between districts by A* road; walls with gates where roads cross; harbours on the water; parks and bombed blocks as variety.
5. **Settlements follow terrain.** Level dry ground, a landmark, houses in a ring, farms with fields, a track to the nearest start; castles on hills; towns at river crossings with bridges.
6. **Validate.** Every start position stays connected (the game's cliff rule: step over 18 blocks); sweep 8 seeds per kind and require the largest land region at 85 percent (islands excepted); level patches for villages exist.
7. **Contracts between modules.** Terrain, cities and integration are separate files with function signatures fixed in a CONTRACT.md; the lead wires them with a fallback to the old generator until the new one passes.
8. **Seed search.** Score seeds (structure count, tower count, district balance, connectivity) and pin the best in the registry.

9. **Reach checks must fail, not approximate.** Use a path search that returns nothing when there is no path (a search that returns a partial path reported two islands as connected). Run it on every map kind and every seed in the sweep; islands are the one intended exception.
10. **Spawn order for seas.** Pick spawns after the water is final; starts front the largest sea, roads pay a high cost to cross water, and island maps place starts on separate islands knowingly. Start spread (`pick_spawns`) matters: four spawns put two sides 16 tiles apart and one died by 9:00.
11. **Per-kind validators.** A stats table per kind (height spread, towers within N tiles of the cluster centre, scenery not outposts, ports have tidal flats) in the test, so changing a shared rule shows which map it broke. A change to the tide band moved every shoreline and removed a river.
12. **Hooks, not edits.** Authors work in separate modules against the CONTRACT (signatures, tile glyphs, sea level, cliff step, structure dict, known styles, who calls the reach check); the lead wires them and keeps the old generator as a fallback until the new one passes.
13. **Draw every style in every age.** Neutral style names in the map, a drawing per (style, age) in the renderer; a map structure with no drawing shows as its footprint.
14. **A tool the owner names but you cannot find:** write a stand-in with the same file format, say so, and ask for the real name.

## Era-specific generation (Tidewatch runs 35 and 36)

Evidence for each rule is in dada-lessons `LESSONS.md`, "Games", lessons 125 to 152.

15. **Generate per age; never re-skin at draw time.** The age decides what is built and where (layouts, building mix, defences, fields, roads, woods, ruins): one optional `era` parameter, one pack per age, the plain output unchanged and its hashes still pinned. Renaming one city's styles gives four ages with one plan.
16. **A generator-renderer vocabulary contract.** A list per age of the styles the renderer draws (and a list of styles an age must never contain), asserted by a test; no overlaps, nothing in water, every door on floor. Where the renderer lacks a style, approximate with what exists (moat as water and bridge tiles, vines as a field) and log a renderer request.
17. **Castles, walled towns and star forts are layouts with closed rings and gates.** Test the ring by flood fill, 8-connected: enclosed with the gates walled up, reachable with them open; a two-thick wall from 4-neighbour depth is tight. Concentric castle: curtain with towers every 8 tiles, gatehouse, 2-wide moat with a bridge on the gate axis, inner ward with its own gate, keep taller than every wall (a ward needs 13 wide for a gatehouse between two towers). Revolution walls are ramparts and bastions, never `wall`.
18. **Great places first, scatter last.** Generic outposts laid first blocked every castle site; find sites in tiers (more water, steeper ground), fill ponds inside, lay small capturable buildings after castles and towns. Build over a crossing road and re-route it to the gate.
19. **Dry-run every destructive step** (a town levelled and uprooted roads, then failed its gates), and lay the square and church before the lanes.
20. **Path tests from every spawn**, under the consumer's rule at the worst tide, so a fortress cannot strand a side; then run an AI match on each era map and count keep falls and commands: reachable is not playable (a medieval era map ran 60:00 with no keep falling, cause not found).
21. **Fairness per spawn.** Castles landed at the first two spawns only; place great places per spawn or report win rate per spawn per era map.
22. **Moats with bridges.** A bridge on every gate axis; make narrow water cheap for the road builder (cost 8 against 30 or 600) so bridges exist at all.
23. **Preview first, and a gallery per age.** A footprint preview of every kind and age at a fixed seed before the test; three layout bugs passed every assertion and showed at once in the picture. Draw each building family in a gallery at game zoom before maps show it.
24. **Per-age roads and woods:** straight Roman roads and avenues, winding medieval lanes joined through gates, woods by age.
25. **Generator figures drive render height** (a wall of 3 gives 4 storeys); the renderer must not guess.
26. **Frame-time budget:** draw each structure once to a texture and blit it; record banners, smoke and sails and replay them (176 structures: 37 to 56 ms a frame to 1 to 3 ms). Benchmark in the gallery.
27. **Staged generator ports:** core, relief, cities, eras, each behind a hook seam, gated by the consumer's own map checks on exported copies; grow the schema additively to accept the consumer's real maps; keep a parity export with a `--check`; lock worlds with a recorded `report` tolerance first and drive it to zero deviations; validate connectivity with the consumer's rule on the shipped data; scan every placement family for overlaps; ban engine trig for cross-engine determinism.

## Pitfalls seen

* A sweep that tests only the old geometry breaks when the generator changes: five tests assumed open land and spacing.

* Terrain too steep for blocks gave a city of four buildings: terrace districts first.
* A fixed probe tile made a test fail on a good map: probe several offsets.
* Era-neutral map data with era-specific rendering is enough for building looks (cast `style` names per age in the renderer) but not for layouts: castles, walled towns and fortress plans must be generated per age (rule 15).
* Walls with no gate cut the map: leave gaps where roads cross and on each axis.
