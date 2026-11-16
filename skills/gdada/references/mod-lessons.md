# Mod lessons (a ledger; read first, append last)

Every Mod run reads this whole file at Step 0 and appends at least one entry at the end. Source: two Minecraft mods built
with GDADA and the SHADW mod stack (`SolutionsAsService/shadw-modding`): **Asgard** (Norse, 1.21.4 Fabric) and **Khemet**
(Egyptian, same stack), 2026-11-12..15. The stack's own copy of the technical items is `shadw-modding/docs/LESSONS.md`; items
marked **lint** are caught by `shadw-mod lint`, **playtest** are defaults in `shadw-mod playtest`. Entries are never deleted; a
wrong one is superseded by a later entry that names it. Format: `### L<n> (date, game)`, **Evidence**, **Rule**.

### L1 (2026-11-12, Asgard)
**Evidence:** a 1.21.4 item with a model and a texture but no `assets/<ns>/items/<id>.json` rendered purple and black, and nothing
logged. The same missed file hit every new item and every block item, and a spawn egg without two `constant` tints rendered colourless.
**Rule:** resource completeness is a lint, not a memory: every item, block item and spawn egg has its item definition, every block,
item and entity has a language key, and a linter fails the build before anyone opens the game (`shadw-mod lint`).

### L2 (2026-11-14, Khemet)
**Evidence:** two desert plants rendered with solid black backgrounds in a real client. The texture had transparent pixels, the game
did not know to cut them out, and no log line said so. Only a photograph showed it.
**Rule:** anything the game decides at draw time (render layers, tints, light) is invisible to a code check, so look at a render of
every new block family at least once, and lint what can be linted (a transparent texture with no cutout layer is now a rule).

### L3 (2026-11-13, Khemet)
**Evidence:** `/locate` on a mixed-biome world said "not found" for structures that work; a flat world of the target biome answered
in seconds and found all four. A flat world's `structure_overrides` is an allowlist (empty means no structures at all), and a
`forceload` over 256 chunks fails and reads as "not loaded".
**Rule:** prove natural generation in a world made of the target biome, with the mod's own structure sets allowed, and treat a
negative in a mixed world as no evidence. The playtest tool sets these defaults so a person does not rediscover them.

### L4 (2026-11-13, Asgard)
**Evidence:** a summoned zombie vanished with no message: the test server was on Peaceful, which removes hostiles as they spawn. A
cold server was killed by its own watchdog on the first `/locate`. A teleported survival player fell during every camera shot.
**Rule:** a test server is its own configuration: Easy difficulty, watchdog off, spectator cameras, quiet command feedback and
effects cleared before a photograph. Put them in the tool's defaults, not in a checklist.

### L5 (2026-11-14, Khemet)
**Evidence:** the favor system was tested end to end over RCON by an operator command that calls the same function as the altar
block: offering, wrong-item refusal, stage thresholds (Chosen at 28), blessings by stage, favor after death, Slowness in a
sandstorm and none under a roof. No input automation was written. A first check "failed" because the NBT key was `ActiveEffects`
(1.20.5 renamed it `active_effects`); the code was right and the test was wrong.
**Rule:** give every player-facing rule a command that runs the same code path as the click, so it can be tested without a mouse;
and when a check says a thing did not happen, verify the check's key before changing the code.

### L6 (2026-11-14, both)
**Evidence:** Asgard and Khemet were each built on the same bones (data-driven potions, a favor attachment with persistence,
altar blocks, a structure generator, a skin generator, a playtest scene) and the second took a fraction of the first's time once
the first was lifted into the stack (`shadwlib`, the adapter, `lib-sync`).
**Rule:** the second mod is a port: lift the first mod's generators and engine into the stack the moment the second begins, vendor
the library into each mod, and spend the new time on what makes the new mythology different, not on plumbing.

### L7 (2026-11-14, Khemet)
**Evidence:** reusing vanilla models with custom skins (a `Zombie` subclass for the Mummy and Royal Mummy, a `Parrot` subclass for
Raven) produced six creatures with real attributes, drops, spawn rules and a renderer in a few hundred lines. A black head came from
opaque pixels in the zombie hat layer (x 32..63, y 0..15) and was fixed by leaving unpainted pixels transparent.
**Rule:** for the first slice, creatures are a vanilla model, a skin and a behaviour change that the player can feel; bespoke model
code waits until a creature earns it. Say honestly that the model is vanilla.

### L8 (2026-11-15, Khemet)
**Evidence:** a "kept through death" claim on the site was untested until a test killed the player and read the favor back (28
before, 28 after). The Debord seat had objected to it on the page; the measurement removed the objection.
**Rule:** a claim on the site or in the README is either measured in the game, labelled "written, not yet seen in play", or cut.
Every page of the site ends with a Status box listing what was seen and what was not; update it when a claim is actually verified.

### L9 (2026-11-14, Asgard)
**Evidence:** chests, vines and lanterns inside a placed structure template silently vanished because placement runs neighbour
updates. Hanging lights only held when a chain was anchored to a log knot. A dense canopy turned a trunk black at noon until sun
shafts and hanging lights were carved in.
**Rule:** structure templates are tested by placing them and photographing them, and anything that needs support, light or
skylight gets it by construction (a log knot, a carved shaft, an emitter), not by hope. A template places only the blocks you put,
so a carved room needs explicit air.

### L10 (2026-11-14, both)
**Evidence:** every real defect found in two mods (black trunk, black head, buried rune circle, structure placed underwater,
black plants, wrong effect key) was found by looking at a photograph or reading a game log, not by reading code or a generator's
output; and screenshots written to the wrong directory, or taken with effect icons in the corner, nearly went into the site.
**Rule:** generate, then look: a contact sheet for textures, a photograph for every structure and creature, a phone-width render
for every page. Commit a screenshot only after looking at it, and keep capture paths relative to the mod, not the shell.

### L11 (2026-11-15, Khemet)
**Evidence:** a site generator gained a second serif declaration beside the `--serif` variable; the later rule won and the page
showed Georgia while the log claimed one font. A CSS arrow written `"\2192"` in Python rendered as a control character and "92".
A one-line caption added inside the measured landing wall pushed the phone's wall from 752 to 819 against an 812 fold.
**Rule:** assert on computed values, not on source: measure the computed font, the rendered glyph and the wall's bottom edge after
every edit that touches them. (Site-side detail: `dada` field-notes 71.)

### L12 (2026-11-15, Khemet)
**Evidence:** the six category hues for the site were derived from the six canonical colours of Egyptian art and then gated by
CIE76 distance and contrast; the gate rejected carnelian against red ochre (23.8) and a green against turquoise (22.6). Amethyst
passed at 44.9.
**Rule:** a mod's site takes its palette from the mod's own subject, and the build fails on a hue pair under 30 or a contrast under
the floor. A gate that fails is a result, not an obstacle.

### L13 (2026-11-14, both)
**Evidence:** a modpack build bundled two jars of one mod because an old version stayed in `build/libs` after a version bump; a
relative `out` path wrote screenshots into the caller's working directory; the vendored library and a stray copy of `nbt.py`
drifted apart.
**Rule:** the tool, not the person, owns the housekeeping: the pack builder takes only the jar matching the manifest version, paths
resolve against the mod, and a vendored library is refreshed by one command (`shadw-mod lib-sync`).

### L14 (2026-11-15, both)
**Evidence:** four different kinds of claim sat under "it works": it renders in a client, it loads on a server, natural generation
finds it, and its logic runs in the game. Item use, brewing, taming and a click on an altar were never exercised by an automated
test in either mod.
**Rule:** in the log, the README and the site, name each claim's rung (rendered, loaded, generated, logic-tested, hand-played) and
never let a lower rung stand for a higher one. A mod is not "done" until a person has played it.

### L15 (2026-11-16, Olympia brief)
**Evidence:** the Olympia master prompt asks for twelve gods, nine biomes, a custom dimension, ten bosses, sailing, Atlantis and a
prophecy system, and says in its own words that "a functional Minotaur encounter is more valuable than ten unfinished monsters".
**Rule:** a brief that sprawls is a roadmap, not a slice. The first run builds one complete thread through every pillar the brief
names (a place, a god with favor, a relic, a monster that behaves, a site) and writes the rest into the Frontier as DEFERRED with
the phase it belongs to. Do not touch a pillar you cannot test in the same run.

### L16 (2026-11-16, Olympia)
**Evidence:** the first Minotaur wandered its hall for a minute while a player stood 14 blocks away through a wall. Three separate faults
hid behind one symptom, found one at a time by logging and by changing one thing: (1) its target goal passed `mustSee=false` but the
targeting conditions still demanded line of sight (the flag only matters once a target is held; call `ignoreLineOfSight()` on the
conditions); (2) lanterns stood on the floor of one-wide corridors, which pathfinding treats as blocked (set lamps flush in the ceiling);
(3) one-wide corridors stopped a creature of scale 1.5 at every corner (corridors are now three wide). A stalking goal (breadth-first
search over floor tiles, steering a few steps ahead) finishes the job when the stock pathfinder cannot. Result: it reached a player a
162-block walk away in 58 s.
**Rule:** a "hunts you" claim is measured as time-to-reach from a stated distance and path, not as "it moves toward you". Test
creature behaviour in the structure it lives in, poll position and distance every second, and change one thing per test. Size a
structure for the largest creature that must move through it.

### L17 (2026-11-16, Olympia)
**Evidence:** a flat test world with 3 stone layers put the labyrinth's maze below the world floor: `/locate` found the structure and the
maze simply was not there. `shadw-mod playtest up --deep N` now gives N stone layers. A freshly summoned mob's NBT showed only the
attributes it overrides, so `attribute <mob> <name> get` was needed to read the real value.
**Rule:** a structure that goes underground is tested in a world with room under the surface; "found" is not "present". Read live
attributes with the `attribute` command, not NBT.

### L18 (2026-11-16, Olympia)
**Evidence:** Minecraft's tutorial toast ("Move with W, A, S and D") sat in the corner of every first photograph; a boss bar for a Minotaur
placed 300 blocks away appeared in every shot because a boss bar shows to every player tracking the entity; two photo runs started
at once (the first one's child processes survived the kill of its shell) wrote over each other.
**Rule:** the capture tool turns the tutorial off (`tutorialStep:none`); structures with boss entities are placed after every
photograph that must not show a boss bar; a run is stopped by killing its process group and confirming no `playtest.py` remains.

### L19 (2026-11-16, Olympia)
**Evidence:** Mojang-mapped names again differed from memory: `MobEffects.MOVEMENT_SPEED` (not `SPEED`), `Zombie.populateDefaultEquipmentSlots`
(not `populateDefaultEquipment`), `Attributes.SCALE` exists and sizes a mob's hitbox, `ServerBossEvent` needs `startSeenByPlayer` and
`stopSeenByPlayer` overrides. A relic's `use()` can be run over RCON by `/olympia use`, which calls the held item's `use` exactly as a click.
**Rule:** let the compiler name the Mojang symbols; give every mod a test command that runs the held item's `use`, and one that sets a
rule's input (favor) directly, so tests reach every stage without grinding.

### L20 (2026-11-16, Olympia, Khemet, Asgard)
**Evidence:** after three hand-written creature classes (Mummy, Troll, Minotaur) each reused the same pieces, `shadw-mod mob` made a
creature a JSON file and generated its class, skin, egg, lang and loot. Moving Olympia's three hand-written mobs onto specs kept their
behaviour (checked by `mobtest`) and added two more in a few minutes; Khemet gained three. The first generated registry put renderer
classes in the main class and the dedicated server crashed at startup (`Cannot load class ...EntityRenderer in environment type SERVER`):
renderers now live in a separate `GeneratedMobsClient`.
**Rule:** a second and third creature of the same shape is the signal to write a generator, not a fourth class. Keep client-only classes
out of any class the server loads. Migrate hand-written creatures onto the generator one at a time, and prove each with a measurement.

### L21 (2026-11-16, three mods)
**Evidence:** `shadw-mod playtest <mod> mobtest <id>` measured 13 creatures in about a minute each: the Mummy's Weakness (untested since
Khemet slice one) works; the Troll does not move at noon (by design, now visible in a table); a neutral Satyr needs a different test
(provoke, then watch) from a hostile one; and a player left at 200 maximum health but 23 current died during the second creature's
test and every later number was zero, until the harness checked that the player was alive and healed with an amplifier that did not
overflow.
**Rule:** measure every creature with the same harness and publish the table; a harness checks its own preconditions (the player is
alive, at full health) before it measures, and says so when it cannot.

### L22 (2026-11-16, Olympia)
**Evidence:** the first Satyr and Gorgon were zombies with painted skins, and the owner's verdict was "very basic ... really look like
satyr and gorgon". A `model` section in the mob spec (a tree of cuboid parts, auto-packed UVs, paint recipes and procedural animation)
made them real figures in four photograph rounds: goat legs, ram horns and pipes; a twelve-snake mane, wings and a slithering tail.
Photograph problems that cost rounds: the spectator's eye is 1.62 blocks above the position you teleport it to (every "close-up" was
aimed at the wrong height); a mob 5 blocks away fills a tenth of the frame; leftover drops and slimes clutter the shot.
**Rule:** a creature that is a named mythological figure needs a silhouette that names it (horns, hooves, serpent tail), which a
reskinned humanoid cannot give: build a model. Judge it from front, three-quarter, side and back and from a face close-up before
calling it done, with the camera set by eye height, not feet height.
