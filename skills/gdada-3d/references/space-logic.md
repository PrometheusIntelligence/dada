# Space logic: proportions, openings, circulation (read before building any room)

A 3D interior fails in two ways: it looks wrong (proportions, openings) or it behaves wrong (you cannot get anywhere, things overlap). Both are checked by numbers, not by eye.

## Proportions (metres; eye 1.6)
| Thing | Size | Notes |
|---|---|---|
| Room height | 2.6 to 2.8 | ring beam or cornice takes the top 0.15 to 0.3: nothing else may reach into it |
| Door | 0.9 to 1.1 wide, 2.0 to 2.1 high | set into the wall in a frame with a threshold |
| Window | 0.7 to 0.9 wide, sill 0.9 to 1.0, head no higher than 1.9 | round or pointed head fits under the beam; **horizon line of the view outside is at eye height (1.6)** |
| Desk | top 0.72 to 0.78, 1.5 to 1.8 wide, 0.8 deep | kneehole, pedestals, overhanging top |
| Chair | seat 0.42, back to 0.9 | legs, slats |
| Bed | 0.9 to 1.0 wide, 2.0 long, top 0.5 | in a round room, **head to the wall, along the radius** (a bed along a curved wall pokes through it at the corners) |
| Stair | 0.2 rise, 0.28 to 0.7 tread | a flight of 12 rises 2.4 to 2.6 |
| Picture | centre 1.5, 0.5 to 0.7 tall | between the dado (1.0) and the beam (2.0) |
| Shelf | 1.4 to 1.5 | |
| Banner | hangs from the beam, 1.0 long | |

## Openings are recesses, not stickers
A window is a hole in a thick wall: reveal quads on the sill, both jambs and the head (0.4 to 0.5 m deep), the glass at the back, a frame line in ink at the inner edge. A box with a dark rectangle on the front reads as a picture or a hole in a poster. The view through it obeys the horizon: the sea/sky split at eye height, a moon above it, small ships and a beam below it.

## Circulation: stairs and floors
- A flight must **arrive somewhere**: a hole in the ceiling above its top step and a hole in the floor above, in the same plan position, with a rim or rail.
- Alternate the direction of flights (up clockwise, back counter-clockwise): each flight then starts beside where the last one landed, and furniture keeps out of one arc.
- The arrival point is inboard of the hole, looking into the room; the way down is the rail round the hole.
- A **union bounding box** of a spread-out object (a flight of treads) swallows the targets behind it: make each tread its own target.
- Test: the hole on floor f+1 is within 35 degrees of where the flight on floor f ends; the hatch object sits at the hole (within 6 degrees).

## Clearances and overlaps (lint)
Run `templates/space-lint.HC.txt` as a test. It fails on: any object reaching into the beam zone; any object's corner outside the wall circle by more than 12 cm (corner = sqrt((r + d/2)^2 + (w/2)^2)); two big floor pieces overlapping; a flight that ends far from the hole above; a floor with no way down. It found, in one run: a bed poking 13 cm through the wall, a wrong-thing strip 24 cm through the wall, a crate inside a bookcase, a table inside a bed, a clock inside the ring beam.
