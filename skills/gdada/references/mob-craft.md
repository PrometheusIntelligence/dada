# Mob craft (creatures for Minecraft mods)

How a Mod run makes a creature. Read [mod-lessons.md](mod-lessons.md) first (L7, L16, L20, L21).

1. **Write the design line first**, in `VISION.md` terms: what the player does about it (flee, fight, avoid by day, bait it), and the
   one thing it does that no other creature here does. A creature with no decision for the player is cut.
2. **Define it as data**: `shadw-mod mob <mod> new <id>`, then edit `mobs/<id>.json`: attributes, flags, behaviours, spawn, drops, skin,
   egg. Choose behaviours from the list in `adapters/minecraft-fabric/mobs.py`; if the design needs one that does not exist, add it
   to the generator (all mods get it) rather than hand-writing a class.
3. **Generate, lint, build**: `mob gen`, `mob lint`, `shadw-mod lint`, `gradle build`. Look at the skin on a contact sheet.
4. **Measure**: `playtest <mod> mobtest <id>` in a running game; add the row to the mod's creature table. A claim like "hunts you"
   is a reach time from a stated distance, not "it moves".
5. **Photograph it** with the AI off and the player in spectator, close enough to read the face; clear drops from the ground first.
6. **Write the rung** for each claim (rendered, loaded, logic-tested/measured, hand-played). A creature is not done until a person
   has fought it.

Balance heuristics from the measured table: a normal zombie-speed creature reaches a player 12 blocks away in about 5 to 7 s; a charger
in 3 to 4 s; first hits on Easy run about 3 for a 4-damage creature; a boss that takes a player from full health in six seconds is
too hard until a person says otherwise.

## Models (added 2026-11-16)

A creature with a name in a myth needs a silhouette that names it, so give it a `"model"` (see `shadw-modding/docs/MOBS.md`). Build it with the
figure kit (`Rig.biped`, `Rig.quadruped`, `Rig.chain`) in a `tools/gen_models.py` script, then `tools/model_sheet.py` and `shoot` for six angles. Check, in
this order: the silhouette from the side (horns, tail, weapon), the face close-up (eyes, muzzle, tusks), the back, then the edges
(bevelled faces, tapering limbs, no floating segments). Weapons are model parts held in the hand, upright, not pointing at the floor. A
creature that holds an item in its spec's `equipment` and also in its model holds it twice.

Beasts and exceptions (added 2026-11-16, Asgard): a four-legged creature (wolf, hound) is `Rig.quadruped` on the zombie base with a `size`
for the hitbox; judge it from the side first (leg length against body depth, neck angle, tail). A creature the mod needs as its own class
(a flier, a tameable) is an `external` spec: the class stays hand-written, the model comes from the tool, and a mob with its AI off is
photographed in its folded pose. A daylight or weather rule is a behaviour (`stone_by_day`), measured at noon and at midnight.
