# GDADA map design rules (Place run, layout pass)

These are the layout rules the person has given for maps. They are checkable, so each has a rule id the host lint prints. A map
that breaks one is not finished. The lint for The Holy Temple is `tools/map_rules.mjs` (run `node tools/map_rules.mjs`, add
`--quiet` for the count). The rules grow: every time the person corrects a map, add the rule here, the check there, and a
lesson in `world-lessons.md`. Read this file before drawing any map; run the lint before showing any map.

## The rules

| id | rule | why (the person's words) |
|---|---|---|
| `surface` | Small things (screens, clipboards, tablets, phones, radios, fax) stand on a table or counter, never alone on the floor. A screen with a table beside it is a desk. | "cables should be on tables not the floor" |
| `accent` | Accent pieces (sphinx, obelisk, statue, brazier) go on either side of the room as a pair, mirrored about the middle. Only the centre column (x 9 to 10) may hold a single one. | "accents like the sphinx should be on either side of room" |
| `lamps` | Light posts are in one line (one row) at even spacing, give or take one cell. Never scattered. | "light posts should be in semi normal line not random" |
| `backwall` | Bookcases, clocks, wardrobes stand against a wall (the row under a wall cell), not out in the room. | a tall object's upper half overlays the wall |
| `chair` | A chair belongs at a table or in a row of chairs at one. | chairs are for sitting at something |
| `tallabove` | A tall object's upper half is drawn on the cell above: that cell must be wall or empty floor, never another object. | the upper half would hide it |

## Process (a layout pass, every time)

1. Run the lint on the map or region. Fix every break; do not argue with a rule unless the person has said it is wrong.
2. Fixing means moving or pairing, not deleting: a lone obelisk gets a partner; a CRT gets a table beside it.
3. Re-run the whole-world check (reachability) after fixing: a table must not wall off a door, a person or a thing you can examine.
4. Show the map to the person. Their words become the next rule or the next lesson.

## What a good room looks like (not yet rules; promote to a rule when the person confirms)

- One focal thing the player sees on entering (the clock, the throne, the sphinx), the rest in service of it.
- Furniture in groups with walking lanes between, along walls more than in the middle.
- Symmetry for sacred and official places; irregularity for houses and dreams.
- A room tells you who uses it: a coffee cup on the desk, a coat on the chair.

## The tile plan and the scale pass (added 2026-11-10)

The person: "plan needs way more tiles, factor in size of things better; make a tool in gdada". Two measured passes, both with scripts:

- **Tile plan** (`scripts/tile_variety.mjs <world-dir>`): counts the ground kinds each map shows and the share of the commonest. A map is bare
  when it has under 3 kinds or one kind covers over 70% of its floor. Fix by giving the map a **ground layer**: a second grid of
  decorative ground tiles under the objects (paths between doors, runners, flagstones, moss, cracks, other grass, wet sand at the water,
  runway markings). The Holy Temple's `tools/dress_ground.py` generates one by theme, deterministically, and aims for about 45% of the
  floor in other tiles. Hand-place a ground layer where the room has a story (a worn path to the one door that matters).
- **Scale pass** (`scripts/scale_check.mjs <art.hc> <scale-table.json>`): every object has a target height in person-heights in the game's
  scale table; the script measures the opaque height of each object (a tall object's two cells together, a block's cells together) and
  fails any outside the tolerance (height, and `width_persons` for wide things such as a jet, checked across a block's cells). Targets come from what the thing is, not from the current drawing (lesson L38). A jet is bigger than a person (three cells wide, two tall), a dome is four wide, a chair is lower
  than a person. Write the table entry before drawing; draw to it.

Both are run before a map or an object is shown to the person.
