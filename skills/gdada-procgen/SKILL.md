---
name: gdada-procgen
description: "GDADA playbook for procedural maps and cities in a game: terrain from real processes (domain warp, ridged noise, erosion, flow-accumulation rivers, biomes), cities from districts (core, ring, harbour, industry, residential) with roads, bridges, walls and gates, settlements that follow valleys; with preview-first iteration, a stats table, many-seed sweeps, connectivity validation and a contract between generator modules. Use when asked to improve map generation, add map types, make urban or rural layouts, or make maps look natural."
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

## Pitfalls seen

* A sweep that tests only the old geometry breaks when the generator changes: five tests assumed open land and spacing.

* Terrain too steep for blocks gave a city of four buildings: terrace districts first.
* A fixed probe tile made a test fail on a good map: probe several offsets.
* Era-neutral map data, era-specific rendering: cast `style` names per age in the renderer, not in the map.
* Walls with no gate cut the map: leave gaps where roads cross and on each axis.
