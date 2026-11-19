# Map craft: placement (tile maps, top-down, one-screen rooms and scrolling places)

Distilled from The Holy Temple's map grades, 2026-11-09/10 (world-lessons L21-L25 hold the evidence). Graded A/A-: the dream kitchen, the
unborn throne room, the mask barn, the island court and cottages, the park, the duplicates room, Foundation 2. Graded B-: rooms made
"too same" by one recipe. Estate B+ and the wanderers "getting better on one shots": the rules below are what one-shot maps must follow.

## P1. Use the frame
A room fills the screen (frame use 90%+). Never a small cell inside a slab of solid wall (wall mass under ~5%); if a space must be small,
show what is around it (a corridor, a yard, the other side of glass). Scrolling is for outside, mazes and long walks; rooms stay one screen.

## P2. Furniture is placed by what it is FOR, in groups, against walls
- A counter run along the top wall; a table ringed by its chairs; a bed with its nightstand and lamp; a desk with chair and lamp; benches in
  rows facing what they face; cases and statues in mirrored pairs.
- Groups sit against walls or around one centre; between them run clear walking lanes (2 cells), and every door has a clear landing.
- Small things (papers, phones, lamps, tablets) sit on a surface, never loose on the floor (the map linter's `surface` rule).
- Wall objects (clocks, windows, posters, shelves, inscriptions) only on the top wall row or the side walls; 3-5 on the top wall.

## P3. One focal object, framed
Every room has one thing it is about (a throne, a fountain, a maypole, a counting table, a reliquary), placed on the axis or at the head
of the room. In formal rooms frame it with mirrored pairs (the linter's `accent` rule checks mirror partners). Informal rooms put the focal
off-centre and balance it with a group on the other side.

## P4. Floors are calm; one runner leads
One base floor, soft variant patches of the same family, and ONE deliberate runner or rug that leads from the door to the focal. No
confetti of textures; no black floor showing between patches (it reads as holes).

## P5. Colour carries the region
Each region has its own floor family, wall treatment and main colour pair (a theme sheet); neighbouring rooms never share floor+wall+runner.
A recipe applied everywhere makes every room look the same (graded B-) even when each room is "correct". Vary by room purpose within the
region (reading room, stacks, restricted) and by mood (dark rooms need a light field or a wide light runner, one warm light per group).

## P6. Outdoors and districts
Outdoor places: a continuous road or path, kerbs and fences on one line, lamps in a row at even spacing, trees in rows or groves (never
scattered singles), buildings with real roofs (ridge, slope, eave; flat roofs with parapet and signage band for shops). Merge edge-connected
outdoor screens into districts of 2-3 screens; buildings stay one-screen rooms. Scale matters: a plane is 10 cells, not 4.

## P7. Emptiness is designed
Where emptiness is the point (a last room, a blank archive, a hall too big), keep it but make it legible: one chair, one line on the floor,
one worn path. Say so in the report so a later pass does not "fix" it.

## P8. Generators are the source
Maps written by a generator are edited in the generator (and it must skip maps refined by hand, marked `# ground: hand`). A merge or widen
tool translates every coordinate (doors both ways, people, schedules, patches) and is re-runnable from a fixed revision.

## P9. One-shot checklist (before showing anything)
1. Frame 90%+, wall mass under 5% (the audit measures it). 2. One focal, framed. 3. Groups against walls, 2-cell lanes, door landings clear.
4. One calm floor + one runner; no holes. 5. 3-5 wall objects. 6. The region's colours; differs from its neighbours. 7. Every object
character has an examine text. 8. Render it and LOOK at it at 1x and 2x; fix what reads wrong (a rug that reads as stripes, a tile that
reads as brick, a stall that reads as a booth). 9. Flag anything that echoes a real place or person and ask the owner (L25).

## Lessons from the Estate and wanderers pass (2026-11-10)

### P10. A wall-mass number can lie: measure the caps, not the '#'
The audit's wall mass counts '#', but a generator that turns walls into faces and caps (`faces()`) leaves no '#', so the Estate tunnels
scored "mass 0" while 46% of the map was dark cap rock between small rooms (the grade said "heavy with dark wall"). Count cap legend
characters as mass too. Fix by plan, not by paint: every block of rock one wall thick, the rooms grown to fill the space, and the spare
corners given a purpose (a fuel store, a post room). Evidence: is_tunnels cap mass 46% -> 16%, every door and landing unchanged.

### P11. A floor tile with joints on a 16 px beat reads as a pattern; the fix is fewer lines, not more variety
The Estate parquet (four boards a tile, staggered ends) and the Pales' trellis carpet and mint-cream checker lino all read at 1x as
brick, grid and chessboard, louder than the furniture. Two boards a tile with no ends (and a scattered variant with one end), a carpet
with a two-pixel sprig and no lines, lino with one hairline joint: the floors went quiet and the laid table became the room.

### P12. A bare room is fixed by its groups, and each group needs one new object at most
The wanderers' rooms (audit 28-55) had a focal and nothing round it. What lifted them (to 59-91) was naming the groups first (a sitting
group round a hearth rug; a bed + bedside cupboard + rag rug + wardrobe; a table ringed by its chairs; a desk + chair) and drawing only
the missing piece of each (an armchair, a standard lamp, a coffee table, a dining chair, a bedside cupboard). A mirrored pair at the
focal (two lamps either side of the mantel, a globe and an orrery either side of the telescope rug) did more than any new prop.

### P13. Outdoors: a roof needs two rows, groves need three trees, and the outdoor rules cost nothing in coordinates
Whitlow's houses were one row of shingle over two of siding and read as boxes; the town's existing roof kit (ridge row with a chimney
over an eave row) in the map's top row made them houses without moving a door. Single pines scattered on the observatory hill read as
noise; the same number regrouped into four groves of five to seven, heather at the edges, read as a hillside. Check the schedules and
other maps' door targets first, then do P6 inside the old footprint so no other file changes.

## Lessons from the scale pass (2026-11-10)

### P14. Measure every object against the person, in cells, before judging how it looks
The person said "that bus is wrong". It was three cells long and half a cell high: shorter than the sedan beside it and lower than
the boy waiting for it. A table of real sizes (a person one cell, 1.8 m, so a cell is about 1.2 m; bus 8 x 2, car 3 x 2, bed 1 x 2,
rowboat 3 x 1, plane 10-12) run over every map found 222 outliers on 77 maps (ThirdTemple `tools/scale_audit.py`): 23 two-cell cars,
3 buses, a seven-cell jet next to an eleven-cell crashed plane, 99 one-cell beds, 74 one-cell sarcophagi, one-cell boats and a one-cell
bus shelter. None had been caught by eye in many art reviews, because each object looked fine ALONE; scale only shows beside a person.
Put the table in the tool's header so the owner can tune it, read a bounding box per assembly (not per cell), and keep forest walls of
one-cell trees as an advisory count, not 788 findings. After the pass: 72, all listed with a reason.

### P15. A vehicle is a picture cut into pieces, its height drawn into the row above, and it is parked, not dropped
Draw the whole thing on one canvas (a bus 128 x 48: roof band, windows a person's head high, doors, wheels, a destination sign), outline
it once, then cut it into 16 px pieces placed by legend characters; give repeated window bays one shared name (12 characters for a 16-cell
bus) and draw lettering after mirroring. The roof is picture-only in the row above, so the footprint stays 2 rows. Place it where such a
thing stands: the bus at the kerb with its front door at the stop, cars nose-in inside their painted 3-cell bays (2 x 3 seen from
behind), saloons nose-in to a garage wall, the night car side on by its chauffeur. Evidence: main_street, co_compound (school bus full of
coats, three nose-in cars in the bays), is_garage, west_end car park; all doors, landings, people and schedule spots unchanged.

### P16. A bed that is one cell is a child's bed; grow it from its own art, and never grow a block
Lengthening 60+ beds by hand would never be done; stretching each region's own one-cell bed (head rows, the cover repeated, the foot
rows) into 16 x 32 kept every theme and took one function. Rules that mattered: grow into free floor only (not a door landing, a person,
a schedule spot); never grow a bed that touches another of its kind (four one-cell beds in a 2 x 2 were a double bed: draw it as one
2 x 2 bed instead, or it becomes four long beds in a 2 x 4 slab); never let two grown sarcophagi touch end to end (they read as one
4-cell box). Run it from the generators after they write, so a rerun keeps the beds long. Evidence: br_3_room, dr_mem_bedroom double
beds; an_tombs 15 of 18 sarcophagi 2 cells (the last of each row has no room and stays listed); co_dorms, co_ward, is_ward beds.
