# World ties: doors connect a world, threads tie it

From The Holy Temple's playground audit and atlas (2026-11-10..11; world L24, L26, L28, L31). Use after every new region and before any
release. The tools are in this skill (`scripts/zone_audit.py`, `scripts/world_graph.py`, `assets/world-atlas.html`) and work on any game in
the Holy Temple world text format (`world/**/*.map` with `map`, `region`, `door X Y -> MAP X Y face [gates]`; `world/encounters.txt`
with `enc E_..` blocks; `world/loot.txt`; `cast/**/*.json` with `behavior.reacts`).

## Two kinds of tie

- **Doors** (walking): a door whose two sides are in different regions. Each door has a gate kind: **open**, **time** (`hours=`), **know**
  (`needs=answered:N` / `asked:N`), **item** (`lock=IT_..`), **flag** (`flag=FL_..`, or a variant that hides it).
- **Threads** (meaning): something earned in one region that changes a door, a standoff or a person in another: a **flag** set there, a
  **thing** given or dropped there, or a **clue** (a question asked or answered there) read elsewhere as a door gate, a standoff's clue key
  (`needs=knows:` / `heard:` / `item:` / `flag:`), a gift's condition or a person's `when`.

A world can pass every door audit and still feel like islands: the Department and the Sand City had doors in and out but nothing earned
anywhere mattered there (world L31).

## The rules

1. **Playground** (world L26): every zone has 2+ entrances from 2+ different regions; if all of them are gated, the gates differ in kind, so a
   player who cannot or will not do one thing has another road; each road has a reason on both sides; no zone deeper than about 4 crossings
   by its easiest road. `python3 scripts/zone_audit.py <game>` must report 0 failing.
2. **Return doors keep the old gate** (world L28): an open road into a new zone must not become a bypass round an old zone's gate; give the
   door back into the gated zone that zone's own gate, and let the game's progression checks prove it.
3. **Threads both ways** (world L31): every region has at least one thread OUT (earned here, matters elsewhere) and one IN. Read the per-region
   table from `python3 scripts/world_graph.py <game>`, not just the totals.
4. **The cheapest honest thread is a person who noticed**: a `behavior.reacts` line with `flag:` / `answered:` / `asked:` / `holding:`, in the
   voice of where they stand ("We filed it under NO FURTHER ACTION. It is our fullest drawer."). Key only on questions that can actually be
   asked or answered; some are open on purpose (check with grep before keying).
5. **Better threads change play**: a standoff move keyed by a clue from three regions away (the Mole Hunt takes keys from the park, the Index,
   the hotel and the Institute), a door gated by a flag set in another region, a gift only a deed elsewhere unlocks.
6. **Verify an audit against one hand-traced example before trusting its zeroes.** The first atlas read `encounter E_` where the data says
   `enc E_` and reported 67 threads; there were 126.
7. **Generated cast files belong to their generator.** A reaction hand-added to a file a generator writes is wiped on the next run; add it in
   the generator (gen_rooms.py, gen_index.py) or in a hand-owned file.

## The atlas

`world_graph.py` writes `design/WORLD-GRAPH.json` (regions with maps, people and named places; doors with gates; threads with readable names
from flag comments, item names and question text), `.md` (per-region table), `.svg` (graphviz overview). `assets/world-atlas.html` is the
interactive page: regions in columns by the fewest doors from the start (breadth-first), ordered in each column by the mean row of their
neighbours (a few sweeps) so lines cross least, columns over 7 regions in two staggered lanes, pan/zoom/fit, door lines coloured by gate,
threads drawn for the selected region (or all), a side panel listing ways in and out and every thread once with all its places, deep links
(`#region`). A force-directed layout overlapped and was replaced: layered layouts read; force layouts tangle.

Publish: the page reads `WORLD-GRAPH.json` beside it. The Holy Temple publishes it as a claude.ai page and as a site repo
(`SolutionsAsService/holy-temple-map`, `tools/publish_map.sh` wraps the page into a full document and copies the data).

## Numbers (The Holy Temple, 2026-11-11)

23 regions, 365 maps, 85 doors between regions, 144 threads; 0 zones failing the playground test; every region with threads in and out.
