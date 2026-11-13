# GDADA Place run: maps and world

The **Place** run type fills in or expands a game's world: maps, the people in them, the texts and questions they carry. It is built for scale:
a world authored as text files that a host tool builds and checks, so many places can be written in parallel and trusted without a runtime.
It reads [world-lessons.md](world-lessons.md) first and always appends to it.

## Use it when

The game needs many more places than one author can hand-write in the engine's language, or when a place is being redesigned. Mode and run
type are stated as usual; run type is **Place**.

## Inputs

- The design documents that name the places and who is in them, and the theme the game must keep (for The Holy Temple, `design/gdada-unknowns.md`: every place raises a question; an answer asks another).
- The **world format** and **checker**: for The Holy Temple, `world/README.md`, `tools/make_world.py` (format and rules) and `tools/check_world.mjs` (reachability, dialogue width, questions).
- A **viewer**: `cpp-sprites` (`hcviz`), to look at every map.
- Shared limits the format imposes (ids, door count, generated-text slots, save bits). Read them before assigning work.

## Step 0 (Place)

1. Read `world-lessons.md` in full.
2. Print the baseline from the checker: maps, doors, people, questions, generated texts against their caps. Zero printed with its denominator.
3. Premortem R0: how will two authors collide (ids, caps, doors into each other's rooms), and how will a place become unreachable or empty?
4. Wire **one entry stub per region** into the existing game before authors start, so each region is reachable and checkable alone.

## The loop

- **One region per author, in isolation.** Each author edits only their region's files, runs the region check (a private build of the original maps plus their region) and looks at their maps in the viewer.
- **Merge only on report.** Run the whole-world build and check after the authors finish, never during. The merge is where shared limits and cross-region collisions show up.
- **Every place earns its place:** it raises a question, or has a person with a routine and a complaint, or it is cut.
- **A second look is a deliverable.** Authors must revise at least once after viewing; report the change.

## Measurements (print them in the Panel Report)

| Check | How | Pass |
|---|---|---|
| Reachability | flood the whole world from a new game with everything granted | every map and every person reached (N of N) |
| Limits | maps, doors, people, questions, generated texts against their caps | all under, with the number printed |
| Questions | every question can be asked; every answer has something that files it | 0 of N unfiled |
| Dialogue | page lines and column width | none over |
| Density | objects per map | few or no bare maps (print how many of N are under the threshold) |
| Seen by the person | a sample of the maps was shown, and what they said is logged | yes |

## Panel seats (exact labels from the graph)

- `Environmental storytelling (Jenkins, Game Design as Narrative Architecture)`
- `Teach by play: introduce, develop, twist, conclude (Nintendo level design; Kishotenketsu)`
- `Procedural generation with a solver behind it (Shaker, Togelius and Nelson, Procedural Content Generation in Games)` (for generated places)
- `Scope: cut to the loop, then the juice (Brooks, The Mythical Man-Month; Shape Up)`

## Stop test (Place)

- **P1** whole-world reachability passes; every limit has headroom.
- **P2** every question can be asked and every answer is filed.
- **P3** a sample has been looked at by the run and by the person, and a second layout pass happened.
- **P4** generated places (if any) have a solver, and the generator reproduces its committed output byte for byte.
- **P5** `world-lessons.md` was read first and has at least one new entry.
- **P6** the shared diagram of the world was regenerated.

Round cap 3.
