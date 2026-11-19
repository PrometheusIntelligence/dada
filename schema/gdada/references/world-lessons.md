# World lessons (a ledger; read first, append last)

Same format as the sprite lessons: `### L<n> (date, game)`, **Evidence:**, **Rule:**. Checked by `scripts/check_sprite_lessons.mjs <this file>`.

### L1 (2026-11-08, The Holy Temple)
**Evidence:** moving the world from hand-written HolyC arrays to text files (`world/`, built by `tools/make_world.py`) took the game from 15 to 178 maps (188 people, 197 questions, 918 generated examine texts, 175 spoken lines) in one fan-out of six parallel authors, with the whole-world check passing (178 of 178 maps reachable).
**Rule:** when a world must be large, make the world data, not code. A text format with a host validator is what lets many authors work at once and be trusted without a runtime.

### L2 (2026-11-08, The Holy Temple)
**Evidence:** the full merge found what no isolated region check could: 415 doors against a cap of 256, 918 examine texts against a cap of 512, and 7 questions whose answers nothing filed.
**Rule:** shared limits are a merge-time failure. Print every cap with its headroom at Step 0, set caps for the target size rather than the current size, and run the whole-world build after the authors finish.

### L3 (2026-11-08, The Holy Temple)
**Evidence:** a designer noticed the notebook check's pattern ignored question names containing an underscore, so about 150 questions (every one in the town, undercity and other new regions) were not being verified as askable or answerable until it was fixed.
**Rule:** test a checker against names in the style new authors will actually use. A checker that silently skips the new style is worse than none.

### L4 (2026-11-08, The Holy Temple)
**Evidence:** one entry stub per region, wired into the original game before the authors began, plus an isolated per-region check that builds a private copy, let six authors work at once with no collisions: 6 of 6 regions passed their own checks, and the merged world passed reachability on the first full build.
**Rule:** give every author a wired entry, a private build and a one-command check. Doors into regions that are not loaded are walled up in the private build so one region can be checked alone.

### L5 (2026-11-08, The Holy Temple)
**Evidence:** all six authors reported one layout pass, not two, though asked for two. The density measure was nonetheless healthy: median 33 objects per map, 1 of 178 maps under 4 objects (`an_impossible`).
**Rule:** a second look is a deliverable, not a hope. Measure density and report the count of bare maps with its denominator; the metric caught the one bare map where the authors' own reports did not.

### L6 (2026-11-08, The Holy Temple)
**Evidence:** authors working in a shared tree meant the repository hook kept finding uncommitted, half-written files; the shared build failed (24 to 72 problems) for most of the fan-out while every region's isolated check passed.
**Rule:** judge an author by their isolated check, commit work in progress knowing the shared build is red, and trust only the final whole-world build.

### L7 (2026-11-09, The Holy Temple)
**Evidence:** the person looked at placed scenes and corrected layout: "cables should be on tables not the floor", "accents like the sphinx should be on either side of room", "light posts should be in semi normal line not random". A first lint found 292 breaks in 181 maps, 255 of them small things (screens, clipboards, radios) on bare floor, written long before.
**Rule:** layout rules the person states become checkable rules in `map-design-rules.md` and a lint in the game repo, then the whole world is fixed against them, not only the map that was shown. A correction about one map is a rule about all of them.

### L8 (2026-11-09, The Holy Temple): places that allude to the real
**Evidence:** the person asked for "a white blue ... place alluding to" a real, notorious private island and its striped temple, "about the limits of what humans know".
**Rule:** allude by structure, never by name or claim. Take the public shape (an island that needs a boat, blue-and-white stripes, a guest book, a flight log, a sealed list) and make it serve the game's theme: the heaviest records are the ones nobody may read; names are struck through and written back in pencil; every landing is logged and no departure. Name no real person, accuse no real person, put nothing sexual or exploitative on screen; the player finds absences and questions, never answers. Check the wording against the rule "evidence, not explanation".
**Later (L25, L27, archive-craft.md):** this is the default when the owner has not decided; The Holy Temple's owner later welcomed direct
references and one parody of a public figure (VISION 57-59).

### L9 (2026-11-10, The Holy Temple): a bare plan and a wrong size
**Evidence:** island maps graded B+ and the airstrip C: "plan needs way more tiles, factor in size of things better". Every map had one floor tile under everything; the plane was one cell, smaller than a person; the dome a single cell. A first measure: 113 of 190 maps had a single ground tile covering over 70% of the floor.
**Rule:** variety and scale are measured, not hoped for. Add a ground layer (tile plan) so no one tile covers more than 70% of a room, and give every object a scale-table entry in person-heights before drawing it. Big things are drawn big: multi-cell blocks (3x2 plane, 4x2 dome) through per-map legends, not scaled-down icons.

### L10 (2026-11-10, The Holy Temple): detail is quiet, and a ground layer runs under objects
**Evidence:** airstrip A-, but "the ground under the plane is broken": the ground layer was written only under floor cells, so under a plane (a legend object) the runway stopped and bare gravel showed. "Rooms are all better but need more attention to detail." A first, random ground (planks and red runners in patches over carpet) read as noise.
**Rule:** (1) a ground layer covers every cell that shows the floor, objects included (engine: the floor under an object is the map floor, so the ground must follow); derive "shows the floor" from the engine's own tables, not from the character '.'. (2) Detail is quiet: props that say who uses the room (a cup, papers, a lamp on a table, a bell on a counter), worn and faded variants of the floor itself, one runner from the door to whoever is there; not patches of unlike tiles. (3) Every variant of a tile must be seamless with its base. (4) After any map or art change run the lint, the tile plan, the scale pass and `art_guard`.

### L11 (2026-11-09, The Holy Temple): density is built, not sprinkled
**Evidence:** the eldritch maps (symmetrical, themed, mostly empty floor) and objects were graded C: "great ideas but need refinement ... do a densely packed library". Two causes: the first batch of single-cell objects skipped the edge and depth passes (L33, L36), and rooms were laid out as a few big pieces on a wide empty floor.
**Rule:** a room is dense when its walls and aisles are filled. Fill every free cell of the wall rows with wall-hung pieces of the theme (scroll racks, eye jars, skull shelves, sigils); build library rooms as bands of tall shelves one cell apart (each band's base row carries the shelf and the row above it is solid wall, so the shelf's upper half overlaps it and the aisles stay one cell wide and open); put book piles, ladders and cabinets in the *band* cells, never in a one-wide aisle (the bot found a pile that cut a room in two). Generate such rooms by loops in the room generator (`tools/gen_eldritch.py`) so the density is repeatable, then re-run the lint, the reachability check and the tile plan.

### L12 (2026-11-10, The Holy Temple): forms as gameplay, areas with names, doors that read the notebook
**Evidence:** the person asked for a Papers-Please-style forms interface ("higher quality for zoomed in") set in an endless office you can get lost in, joined to a municipal corruption satire; pop-up area names designed per theme; and a place that unlocks "under certain conditions" (the notebook).
**Rule:** make the interface a **zoomed view** (32x32 portraits at 4x, large seal and stamps) with the correct answer to every case *derived from the rules on the host* (never typed by hand), so a case set can be proved solvable like a map; every rule must decide at least one case; envelopes are offered, never scored, and remembered. Make "get lost" a graph property (four doors in every room, wrap-around, no geometry that agrees with itself) with one locked way out earned at the desk (a flag). Make conditions data: `needs=answered:N`, `hours=`, `flag=`; the bot treats them as granted. A conditional place is reached from a place that hints at the condition.

### L13 (2026-11-09, The Holy Temple): encounters are standoffs, and the interface decides the grade
**Evidence:** the forms desk interface was graded A+; the area names B ("very good names"; "make sure to theme them"). The person asked for different things "around" the paperwork interface and for the encounter frame.
**Rule:** a rich interface earns its grade from three things: a zoomed-in view with real pixel art (32x32 portraits at 4x), a data-driven rule set whose solution is derived and proved on the host, and one choice the game never scores (the envelope). Vary an interface by theme data (surface colour, header bar, memo voice, own jurisdiction) and by new rule sets, not by new code. An encounter is a courteous standoff: the foe's *composure* is shown as pillars that crack and a foe that shakes; yours is five stones and the edges of the screen closing; each move can be used once; moves are gated by the notebook (answers, questions asked) and by what you have done (flags); a blocking, courteous move always exists; you may always bow and leave; losing costs nothing. Prove on the host that a winning line exists that keeps the player above zero.

### L14 (2026-11-09, The Holy Temple): a paperwork family is one idea in many interfaces
**Evidence:** the forms desk was A+; the person asked to "expand more paperwork mini games around the idea" and to "change up interfaces" because the earlier change-ups were good.
**Rule:** keep the idea (a clerk applies posted rules to a stream of items; the answer is derived from the rules on the host and proved solvable) but give each game a different *verb and surface*: stamp (desk), plug a cord (switchboard), black out a line (redaction), flag a row (ledger audit). Each has a short, visible rules panel that grows by shift, passes at <=1 mistake, and is placed in a themed room from data (`mini X Y = ID`). Never reuse a layout; check the rules panel does not clip at four rules. Candidates next: card sorting, telegram decode, document comparison, parcel routing.

### L15 (2026-11-09, The Holy Temple): dry dialogue works on a confession, not on a gag
**Evidence:** (graded line by line) A: the councillor who abstained "in the gallery, so no one would see", the safety officer whose accidents were "reclassified as events", the mail sorter who sorts "by feeling... seventy percent apology". B+/B: the information clerk (can say where everything is, not where you are), the secretary (minutes of meetings not yet held), Maurice and the bird as beneficiary. C+: lines that were only wordplay with no person in them ("the loop is a lot of loop", "five of us, very close"). C: plain bureaucratic lines with no turn (the reply clerk, payroll). Dream people should be more non-sequitur, which suits them.
**Rule:** the voice is deadpan literal logic carried one step too far, delivered by someone who has quietly accepted it, and ends on a small human admission or a specific object (a hat, a bird, a cold coffee). Test: could this line only be said by this person? Cross-references (Rosen, Pritchard, Wren, Maurice) land well when each speaker only knows one fact about the other. Dream voices: sentences that agree with each other grammatically and with nothing else. A "burnt out" character is made of tiny unrelated confessions in a bright, apologetic voice, not of complaints.

### L16 (2026-11-09, The Holy Temple): a recurring presence is made uncomfortable by data, not by script
**Evidence:** the person asked for "someone in this game to make every different person uncomfortable".
**Rule:** one figure (the Visitor) with a schedule that crosses every region, plus ONE compiled reaction per person keyed to that figure (`in_company_of:<id>`), each written from the person's own fear, secret, keeps and species, never a template. The dread is in the courtesy: the figure never says anything wrong, it stands one step too near and says kind true things in an order that makes them worse. A set piece for a mood is a screen the player acts in (a fitting, a dance whose last step is stillness), not a paragraph. Check: every person has the reaction, no two are alike, and the figure is on a legal schedule (home at least part of the day).

### L17 (2026-11-09, The Holy Temple): puzzles without lame puzzles are a clue web of standoffs
**Evidence:** the person: "I like the idea of the non linear different encounters puzzle game without lame puzzles", and "scenes need something to break them up".
**Rule:** an encounter is a courteous standoff placed mid-region (it breaks a scene); its strong moves are keyed to SPECIFIC knowledge or objects found in OTHER regions (`knows:Q_X`, `heard:Q_X`, `item:IT_X`), each locked card shows an oblique hint of where the key lives, and winning gives an item or flag that is a key somewhere else. The host check proves no single clue is required (every keyed move can be missing and a win still exists), so there is never one right order and never a riddle to guess. `tools/clue_web.py` writes the web (trigger, clue regions, gift, what the gift unlocks) so dead-end gifts are visible.

### L18 (2026-11-09, The Holy Temple): stats decide the standoff; gear and growth are Munchkin; every thing has several roads
**Evidence:** the person: "health should be based off different stats -- a physical fight is strength, an argument is intelligence; stats go up rarely from bonuses but also from items, kinda in the style of Munchkin; NPCs can be looted but of course they remember; this gives multiple ways to the same paths, such as looting the key vs charming the guy."
**Rule:**
- Four stats (BRAWN, WIT, CHARM, NERVE); each encounter declares `test=` and your stones are 3 + that stat's total, so the same foe is easy for one build and hard for another. Moves may lean on a stat (`stat=`), adding damage only above the base so host checks made at base stay honest.
- Growth is rare and earned (`raise=` on a few wins); most power is carried: every item adds bonuses, positive and negative (Munchkin rules, deadpan descriptions that state the bonus as a joke and as a fact).
- Looting (`world/loot.txt`): look first (what you notice, what it needs, what you have), take second. Success costs a little mind and the person remembers: they turn their back and say a `remember` line now and then. Caught is remembered too, and can start a scuffle (a BRAWN standoff) that, won, gives the thing anyway.
- Every thing that can be stolen must be gettable another way -- a `gift` (talk once you qualify by stat or by a flag earned elsewhere), an encounter's `give=`, or a map `give` -- host-checked; `tools/clue_web.py` prints every road to every thing. Stealing is a path, never the only path, and never free.

### L19 (2026-11-09, The Holy Temple): foes have stats too; the craft is choosing the contest
**Evidence:** the person: "a minotaur level ... minotaur is super strong so it's bad to fight him in brawn, try to get him into an intelligence encounter; apply this throughout the game: match-ups, the enemy's health goes with the stat of the encounter."
**Rule:** every foe carries four stats (`stats=B,W,C,N`); its composure is 2 + its stat in the current frame, yours 3 + yours. A standoff starts in the foe's chosen frame (the Minotaur charges: BRAWN 10) and some moves `shift=` it to another (QUERY HIS ARITHMETIC: WIT 2), keeping what each side has lost. The card shows the new matchup ("TURNS IT TO WIT: IT HAS 2"). Host check: some frame reachable by free moves is winnable at base stats; the obvious frame may be a trap (thirty heroes took him by the horns). Teach the trap in the level: a survivor who says "nobody asked him anything", a name to find, an audit to read.

### L20 (2026-11-09, The Holy Temple): encounters come from the state of the world, not from a script
**Evidence:** the person: "add new unique dynamic encounters possible everywhere ... encounters should be possible anywhere based on parameters, where people don't want you, etc."; "items need unique ways to obtain them".
**Rule:** a director (`world/director.txt`) checks rules on arrival and after waiting: place (region), hour, who is present and what you did to them (robbed, caught, pestered), what you carry (anything stolen), hidden mind, and notebook progress (the first hour stays safe). The foe is whoever is present; their stats come from species presets nudged by traits; templates (`foe=ANY`, `@` = their name) open all four contests so the host check can prove every person is beatable by picking their weakest. Rules rest (`cool=`) and roll dice (`chance=`). Things now come seven ways: found, given, won, taken, traded, dropped by a beaten foe, or earned by a stat; `clue_web.py` lists every road to every thing.

### L21 (2026-11-10, The Holy Temple): the size of a map is a feeling; rooms one screen, outdoors and mazes scroll
**Evidence:** the person: "we should have some scrolling maps, not limit all to one screen; that should be mostly indoors, or maybe it's better for claustrophobia."
**Rule:** a map declares its size (`size W H`); the engine keeps a camera centred on the player and clamped to the map, draws only the cells and people in view (one spare row and column while it slides), and every tool reads each map's own size (compiler, reachability bot, map linter, renderer). One screen is a deliberate choice for rooms (closeness, claustrophobia); scrolling is for outside, for mazes and for walks that should take time. A maze needs floor and wall of different value (the first scrolling maze was stone on stone and unreadable). `widen_map.py` grows an old one-screen map without breaking its doors.

### L22 (2026-11-10, The Holy Temple): what made two rooms A- and their neighbours B
**Evidence:** of nine detailed rooms the person graded the dream kitchen and the unborn throne room A-, the library OK, and the rest "need detail refinement".
**Rule:** (measured on the A- rooms) (1) the room fills the screen (frame use 90%+; no small cell floating in a slab of wall: wall mass under 5%); (2) furniture in functional groups against the walls (a counter run along the top wall, a table ringed by chairs, a bed with a nightstand) with clear walking lanes between; (3) one focal object, framed by mirrored pairs in a formal room; (4) one calm base floor with soft variant patches and ONE deliberate rug or runner, never a confetti of textures or black holes; (5) 3-5 things on the top wall (clock, window, shelf, poster). `tools/map_audit.py` now measures frame use, wall mass and wall objects.

### L23 (2026-11-10, The Holy Temple): the L22 rule works; dark formal rooms still fail
**Evidence:** after refining 16 rooms by L22, the person graded one sheet A- and the other A/A except two C: the eldritch gallery and the third stair, both dark, busy, formal rooms of grey stone with statues.
**Rule:** L22 lifts most rooms to A-/A. Where it does not, the room is dark-on-dark: grey statues on grey stone with a patterned border lose their shapes. Give a dark room a light floor field (or a light runner wide enough to hold the focal), fewer kinds of statue, and one warm light source per group; check the render at 1x for silhouettes before adding more.

### L24 (2026-11-10, The Holy Temple): districts, not screens and not one map
**Evidence:** asked how the town should scroll, the person chose "a few scrolling districts" over one giant town or single screens.
**Rule:** merge edge-connected outdoor screens into districts of 2-3 screens (a street and its plaza, a park and its cemetery), keep buildings as one-screen rooms, keep the hard-coded original maps whole and put the merged base at (0,0) so their doors stay valid. A merge tool must translate everything that names a coordinate (doors both ways, people, schedules, minis, patches), rename clashing legend characters so each examine text stays with its object, and be re-runnable from a fixed source revision; then polish the seams by hand so the district reads as one place (continuous kerbs, lamps on one row at even spacing, a single fence line).

### L25 (2026-11-10, The Holy Temple): flag real-world allusions, then let the owner decide (REVISED the same day)
**Evidence:** while extending the island into the Estate, the building agent found that an earlier island map matched a real private island in identifying detail (a "temple" with blue-and-white stripes and a gold dome, an area banner about "the right blue"). The brief and VISION both forbid alluding to a real person by place or detail.
**Rule:** horror about wealth, secrecy and complicity stays general: invented colours, buildings and names; no single detail that a reader could match to a real place or case. REVISED by the owner: "NO, make the pavilion blue and white, we can reference that." The recolour was reverted. The rule is now: agents FLAG a recognisable real-world allusion (as this one did) and the lead ASKS before changing graded or authored work; the owner decides. Referencing a real place's look is allowed when the owner says so; naming or portraying real people is still out. Never "fix" an owner's deliberate reference on a lead's own judgment.

### L26 (2026-11-10, The Holy Temple): a world is a playground when every zone has more than one road in
**Evidence:** asked to "survey and audit how the player passes between all zones ... multiple ways to get to new zones, playground style", a
door-graph audit (`tools/zone_audit.py`) found 5 of 20 zones with a single entrance (dream, labyrinth, sand, Vatican, Watchers) and one zone
5 crossings deep.
**Rule:** every zone gets 2+ entrances from 2+ different regions; if all are gated, the gates differ in kind (time, knowledge, item, flag), so a
player who cannot or will not do one thing has another road; each road has a reason in the fiction (an examine line on both sides); no zone
deeper than about 4 crossings by its easiest road. Audit the door graph after every new region; it is cheap and it finds what playtesting
finds an hour in.

### L27 (2026-11-10, The Holy Temple): a region drawn from a real archive takes its rule, not its people
**Evidence:** the owner asked for a region "with material from" their archive of allegations about real people. What made THE INDEX work was the archive's own provenance rule ("an index, not a finding": solid = a record asserts it, dashed = on the same list, dotted = hedged, a denial makes no line, a path is not proof), turned into a wall of string, a card-sorting paperwork game whose answers are derived on the host, and a standoff won by refusing to conclude. Every source SHAPE (a mind-research program, planted stories, stay-behind caches, a lakeside play, an offshore leak, a review queue of unmerged names) became an invented analogue strung between the game's OWN institutions.
**Rule:** when a brief draws on a real-world archive, import its method and its shapes, never its names, cases or allegations; skip outright any folder about abuse; put the strings between the game's existing invented people so the region links the world instead of the news; leave every dossier entry unresolved; and list the shapes a reader could still recognise (a famous ritual, a famous number) for the owner to OK (L25). (The Holy Temple's owner, 2026-11-11: direct references to real places, programs and records are welcome -- "the game is
about what humans know and don't know"; real people and abuse cases stay out. Ask each owner once; record the answer in VISION. Later the same day the owner allowed one named PARODY of a public figure from the public record only -- ROBERT HANDSOME, after the Cold War mole, and FOXBONE PARK -- never his private life or family: a parody is allowed only when the owner asks for it by name, and it is recorded in VISION as its own rule.)

### L28 (2026-11-10, The Holy Temple): an open road into a new zone can bypass an old zone's gate
**Evidence:** the Index's open lane from County Road 9 plus ungated return doors into the Department's Records and the Papal Archive let the reachability bot walk into Records before the Department had looked the player up; check_world failed two progression tests ("expected unreachable") that no zone audit could see.
**Rule:** a return door from a new zone into an old one carries the old zone's gate (here FL_UNLISTED and FL_ENC_PREFECT), not just the new zone's. Run the whole-world progression checks after linking, not only the playground audit; more roads in must never mean a way round.

### L29 (2026-11-11, The Holy Temple): a record's mechanism becomes a verb only when it changes what a key does
**Evidence:** four more archive records (a non-attribution rule, a hotel suite, a refused takeover, a modelling institute) were built for the Index as invented places. What made each one play, not just read, was attaching the mechanism to an existing system: lines heard under the rule enter the notebook as SOMEONE SAID and work as keys in two standoffs, while the move that NAMES the speaker lands on nothing and costs a stone; the suite's register is a list, so the Index table files it LISTED; the officer's claim carries a denial, so it files NO LINE (a teaching card for the rule order); the institute's standoff marks the most likely move PREDICTED and makes it fail.
**Rule:** for each borrowed mechanism, name the existing system it bends (a key, a card rule, a standoff move) and make one choice cost or fail because of it; then cross-link every piece's key into at least one other region's standoff, door or dossier, and give the hub (here the Index wall) one card per thread. A shape with no verb is set dressing.

### L30 (2026-11-11, The Holy Temple): widen a save by appending, and test the old size in the real runtime
**Evidence:** the 64..255 flag range was full. Appending `flags_hi2[4]` after the last field (not growing `flags_hi[3]` in the middle) kept every older field at its offset, so the reader accepts `size == offset(CState.flags_hi2)` for version 14 exactly as 13 -> 14 did; a TempleOS test writes a v14-sized file with a v15 flag set past its end and checks it loads with that flag clear. A host check (`check_world.mjs`) also hard-coded the old flag ceiling and had to move with it.
**Rule:** grow saved state only at the end; let the reader recognise every older size by an `offset()` of the first new field; grep the host tools for the old ceiling; and prove the widening with a fixture written at the old size in the real runtime, not by reasoning.

### L31 (2026-11-11, The Holy Temple): doors connect a world; threads tie it -- count both
**Evidence:** every zone passed the playground audit (2+ ways in), yet the first atlas (`tools/world_graph.py`) showed regions nothing else
cared about: nothing earned anywhere mattered in the Department or the Sand City, and the Index gave nothing back. A player could walk in
and out of them without carrying anything across. (The first count also missed every standoff: the tool read `encounter E_` where the
data says `enc E_` -- 67 threads reported, 126 real. Check a new audit against one hand-traced example before trusting its zeroes.)
**Rule:** after a region lands, run `python3 tools/world_graph.py` and read threads OUT and IN per region, not just doors. Every region
needs at least one of each: something earned there that changes a door, a standoff or a person elsewhere, and something from elsewhere
that changes it. The cheapest honest thread is a person who noticed (`behavior.reacts` with `flag:` / `answered:` / `asked:`), in the
voice of where they stand; key only on questions that can actually be asked or answered (some are open on purpose).
