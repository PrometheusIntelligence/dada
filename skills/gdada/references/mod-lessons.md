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

### L23 (2026-11-16, Olympia, Khemet)
**Evidence:** "Excellent improvement, polish a bit finer edges, then do the same for the earlier models." A `figure` kit (biped builder with a
jaw, two-box torso, shoulder caps, three-part limbs; tapering sway chains) plus a texture bevel pass took ten creatures from zombie skins to
24 to 105 part models in one session, where the first two models had taken four rounds each. Three things went wrong on the way: a
snake chain drawn with negative `grow` and mismatched lengths came apart into floating cubes (segments must overlap their pivots, taper by
size, not by shrinking); water and lava placed on a temple floor poured out over the grass (set liquids into the floor, ringed by solid
blocks, never on top); and templates placed at the wrong height for the world (a shallow flat world has ground at y -58, a deep one at
-20) hung in the air and made a half-hour of photographs useless.
**Rule:** after the second hand-built model, write the kit; judge every model from six angles; give a liquid a basin; and print the world's
ground height beside every `place` command. When a dead Xvfb leaves a lock, the next client silently fails to start: the tool now clears it.

### L24 (2026-11-16, Asgard)
**Evidence:** "Give Asgard's Draugr, Troll and Raven the same model treatment, and a big wolf for sure." Seven creatures (three rebuilt, four new)
went from spec to photographed in one session because the tool already had the kit. Three things needed new tool features, not new hand work:
a four-legged beast (a `Rig.quadruped` builder that solves the hip height from the leg angles; the first wolf stood on stilts with its head
in the air until leg length and neck angle were tuned from a side photograph), a creature whose class is hand-written (a flying, tameable
Parrot: an `external` spec that generates only its model, texture, egg, loot and language), and a behaviour that had lived in a hand-written
class (the troll's daylight stone, now `stone_by_day`). A walking wolf is still a zombie underneath; the model and `size` make it a wolf.
Weapons held "pointing down" twice: a held item's rotation is added to the arm's, so the part must be rotated to oppose the arm's pose.
**Rule:** when a creature needs something the generator lacks, add it to the generator and the doc, then use it; do not leave one mob as a
hand-written exception unless it needs real AI the data cannot say. Model a four-legged beast from a side photograph first (legs, neck,
tail), the face second. Photograph a flier on the ground or with its AI off in its folded pose, and say that the wing beat was not seen.

### L25 (2026-11-16, Asgard)
**Evidence:** `mobtest troll` reported "does not move" and read like a bug; the troll is stone at noon by design, and the harness sets the time
to noon. A repeat at midnight showed it hunting (reach 6 s, hit 6). Two other single runs reported empty reach times that a repeat did not.
**Rule:** a creature with a time or weather rule is measured under both conditions (`mobtest --time 6000` and `--time 18000`), and a measured
null is repeated once before it goes in a table or a status line. Write both numbers; a rule that stops a mob is a result, not a failure.

### L26 (2026-11-16, Asgard, Khemet)
**Evidence:** "polish all those into a 2.0, cleaning up little things being rough like faces looking off; mostly A minus; the raven's beak is a B."
Face close-ups of fifteen creatures found six causes, none visible from the six-angle sheet: a brow box in the face's own plane that hid the
frost giant's eyes, nose and mouth; a helm cap over the draugr's eye rows; wrap bands across the mummies' eyes; tusks that read as a smile; wolf
eyes on the wrong rows; a one-pixel jackal eye at the edge of its head; and a straight duck-bill for the raven. Three of the close-ups were
themselves wrong (the camera saw a belly, the sky, the inside of a head) because the face camera assumed a biped's head position.
**Rule:** polish starts with the face close-up, with the camera told where the head is. A shared `face()` helper (brow, socket row, glowing
row, pupil, nose, nostrils, cheeks, mouth, teeth) lays a face out in one call, and `shadw-mod mob lint` prints polish notices. New creatures
join the same pass (a Cobra, a Crocodile and the Sun Pharaoh went in during it), and the version bump is the owner's call.

### L27 (2026-11-16, Olympia, Asgard, Khemet)
**Evidence:** "A Pegasus based off the horse model, some other mounts, and Khemet needs a craftable chariot." A Pegasus (flies when saddled and ridden) and Sleipnir (eight legs) are `AbstractHorse` subclasses, the chariot a `Mob` with the riding hooks plus an item and a recipe; all three take only their model from the mob tool (`external` specs). Findings: a wing animation that adds its folded pose per frame gave a T-pose however the angles were signed, and only a pose baked into the model's own rotations (with the animation adding an `air` offset to undo it) behaved, so a resting pose belongs in the model, not in a per-frame `rest`; a fold about the vertical axis puts the forearm's feathers sideways (a bird's Z-fold needs the forearm to come back), so a raised, curled pose is the safe resting pose for big wings; `merge()` takes (dx, dz, dy) and passing the depth as the third value lifted the ponies onto the carriage; the chariot's visual team overhangs its hitbox, by design.
**Rule:** mounts are hand-written on the vanilla riding classes with generated models; read the vanilla riding hooks with `javap` before writing one; verify what can be verified without a keyboard (the entity summons, the recipe unlocks, `ride` seats the player, the item is given) and say that flight, steering and taming were not driven. Resting poses go in the model's rotations; animations only undo or add to them.

### L28 (2026-11-16, Olympia, Asgard, Khemet)
**Evidence:** "pictures on the sites need to be better framed." The creature pictures were crops of the six-angle sheet cut with hand-set boxes; every creature sat off-centre and small (a quarter of the frame), the three-quarter camera was aimed 10 degrees off (yaw 145 where 135 looks at the mob), boss bars cut into the top, and a wolf's head was cut at the edge. Replacing the boxes with the camera fixed all of it: portrait cameras are AIMED at the creature (yaw 135 from 45 degrees, side view yaw 90), set at a per-creature fraction of the full-view distance, raised and pitched 12 degrees down so the creature sits mid-frame with the ground showing, and only boss frames are trimmed (top 40 px, back to 16:9). The site pictures are then the photographs themselves, two per creature, with no crop boxes to maintain, and a group picture of full frames.
**Rule:** frame in the camera, not in the crop: aim, set the distance by the creature's size (a low, long creature needs a closer camera than a tall one), raise and pitch the camera, and keep boss bars out of the crop. Look at the group picture, not only the single cards: it shows the one creature that is half the size of its neighbours.

### L29 (2026-11-23, Terraria Khemet)
**Evidence:** "Add Terraria modding to our stack; begin with a Terraria version of Khemet: a grand pyramid, Egypt bosses." The SHADW stack gained a second game: the `terraria-tmodloader` adapter, content as data (`content/*.json`) generating C#, sprites, localization and a world-generation blueprint, then Khemet for Terraria (a 121-by-94 stepped pyramid with eleven rooms, three pharaoh bosses on one parameterised boss template, three enemies, 22 items, 4 blocks). Facts that shaped it: the machine had .NET 8 (apt) but no route to tModLoader's releases, so the code was compiled only against a stub of the API (a check that catches syntax and names, not API truth); a structure drawn as characters can be flood-filled for connectivity and rendered, which proved every room reachable and caught a throne room with no floor; a tModLoader tile needs the 288-by-270 sheet, an enemy one frame per animation step, a boss a `_Head_Boss` icon, and armour needs equip sheets on the player template, so armour was left out rather than guessed.
**Rule:** for a new game, copy the Minecraft recipe (content as data, generate, lint, preview) and put the verification you can do on this machine first: a blueprint's connectivity, a stub compile, sprite previews you look at. Label everything not proved in the real engine (here: never loaded in tModLoader), keep the registry status `experimental` until a real build passes, and give the repo a CI job that does the real build. Do not hand-write what you cannot check (armour sheets, worm AI) in the first version.

### L30 (2026-11-24, Terraria Olympia)
**Evidence:** "Render everything in sprites unless you can install the mod loader and Terraria; continue with the Greek Terraria version; keep expanding the tool." steamcmd could not run (a 32-bit binary, and Steam's own protocol is not HTTPS through the proxy), so tModLoader stayed unavailable and everything was shown as generated sprites and blueprint pictures. Olympia for Terraria reused the Khemet pipeline and forced the tool to grow in the directions the Greek content needed: ground bosses (walk, jump, charge, slam), a rain attack, potions with buffs, bows, general spawn rules by zone and by structure area, and two new structure kinds (a surface temple whose columns are background walls so a 2D side view can be walked through, and an underground perfect maze whose floor holes carry platforms so it can be climbed). Findings: a side-view colonnade of solid columns blocks the flood-fill, so columns must be walls; a maze generated by depth-first search is connected by construction but the platforms in its floor holes are what make it climbable; unknown vanilla IDs are the main risk when the real API is out of reach, so the check lists any name not on a confirmed list.
**Rule:** grow the tool from the next mod's needs, and prove what the machine can prove (connectivity, previews you look at, a stub compile). Each new feature gets a content key, a generator, a lint rule and a preview, never a hand-edited generated file. The second mod on an adapter finds the adapter's gaps; the first mod's output must regenerate unchanged (or intentionally) when the tool grows.

### L31 (2026-11-24, Terraria sprites)
**Evidence:** "First think we need to use gdada to redo those sprites a lot about c maybe grade now generous c possible a D." The first Terraria sprites were flat painters (a base colour, a bevel, a few details); bosses read as a bust over a tapering stripe, and the 16-pixel tiles and 30-pixel items had no shading logic. The redraw added `tlib/art.py` (five-tone ramps from one base colour with a hue shift, hard bands instead of dither, one light from the upper left, lit ellipses/polygons/lines, a selective outline, a specular pixel) and gave every piece a silhouette plan: one shape that breaks the outline (a long blade, a tall crown, a bolt held over the head) and one thing only it carries (the scales of Maat, the was-staff, a burst of snakes). Findings: dither looked like noise at 1x and lit from the wrong corner on the first try, so bands must be hard and the light direction checked on a ball; bosses drawn near the canvas edge clip their best silhouette (bolt, axe, crown), so budget a margin before drawing; a painter that is handed a single tone where a ramp is expected fails far from the cause.
**Rule:** for generated pixel art, build a shading toolkit first, plan the silhouette per piece, and render three checks every run: silhouette only, actual size (1x) and a numbered grading sheet (G1, G2, ...) so the owner can grade by number. Never claim a grade above what the sheet earns; the person grades, and a piece below A stays in the queue.

### L32 (2026-11-24, Terraria Wilds)
**Evidence:** "Use gdada and shadw modding to read plan and build this new terraria mod in master prompt under design." The plan was a 30 KB master prompt for a huge expansion (guild, kingdoms, wildlife, bosses, museum, events, 20 NPCs). Its own section 20 named a first milestone of eleven checkable items, and the build did that and only that: VISION.md first (the eleven items as must-haves), then the tool grew to fit (Town NPCs, a guild/contract/journal system, passive critters, two structure kinds), then content, then the checks. Findings: a plan this large is built by finding its own milestone, not by sampling every section; each must-have is mapped to what exists and what state it is in (the README table), and the ones only partly met (a wanderer that is a Town NPC, multiplayer, furniture) are named; lint can prove game-logic properties without the game (every contract can be offered in some order, a last rank can be earned, every discovery has a source); a file in the repo had a trailing space in its name, so read the directory listing before assuming a path.
**Rule:** for a big plan, build the plan's own first milestone, quote it as the checklist, and prove with lint what the machine can prove (references, reachability, playability order). Write each limit into the README table row it affects, not a list at the bottom.

### L33 (2026-11-24, Calamity art study, Terraria)
**Evidence:** "Look at Calamity mod and others to know the art more to improve ours." Measured over about 1,100 Calamity sprites (read as a reference; none copied, their licence forbids redistribution): a median of 11 to 14 colours per sprite, **no semi-transparent pixels**, weapons about 56 by 58 pixels (ours were about 44), a full dark tinted outline, mottled surfaces, one accent hue glowing against a muted body (a red eye, neon lines), ragged asymmetric silhouettes. Ours had 17 colours on items and **45 on NPCs**. Added to the shared toolkit: a texture pass (clusters, small steps), chipped edges, a rim light and median-cut palette quantisation; the median fell to 15 to 16. First try at texture was uniform speckle and made big sprites look dirty: texture must be low-amplitude, in 3-pixel clusters, and only on large areas.
**Rule:** study a reference by measuring first (size, palette, transparency), then by looking; add what is measurable as a pass over every sprite. Filters do not fix drawing: our bosses are still blocky (straight limbs, flat polygons), and that needs redrawn forms (tapered limbs, asymmetry, an accent glow), not more passes. Reference mods are for technique and numbers only; never copy their art or bundle them.
