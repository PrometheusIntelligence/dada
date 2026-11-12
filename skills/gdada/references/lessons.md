# Lessons

Hard-won, per run. Add one block per run; keep each lesson to the failure, the number, and the rule.

## Tidewatch art revamp (Nov 2026): sprites, buildings, eras

Context: an RTS (Godot, 16 px tiles). Owner brief: "Sprinter need big revamps use gdada for this the sprite tools make
much better 2.0". Round 1 (units only) was graded "a b to c" by the owner. Rounds 2 to 4 below took the art from a
panel average near C+ (B, B-, C+, D+ in R3) toward the fixes listed. Tool: [tools/sprites/](../tools/sprites/).

### 1. Revamp the whole visual system, or the grade is the worst part
The first pass redrew only the units (16x16, shaded, outlined). The owner's grade was B to C, and the panel's R3 note
agreed: buildings and terrain were an older flat style and clashed. Style unity outweighs the polish of any one sprite
(Arnheim: unity of style). **Rule:** inventory every asset class on screen (units, buildings, terrain, UI bars, props,
construction state) before choosing what to redraw; leaving a class out is a decision that needs a Decision Record.

### 2. Draw in shapes and materials, and let the tool shade and outline
Hand-typed pixel grids drift in style and cannot be re-lit. `kit.py` takes rects, ellipses and polygons in named
materials (4-step ramps) and applies top-left shading, an ink outline and a ground shadow. First bake of 16 units: 10
validator failures (clipped outlines, stray pixels, near-identical silhouettes) that a viewer would have shrugged at.
**Rule:** the tool, not the artist, owns shading, outline and shadow; a style change is one edit to the tool.

### 3. Every panel measurement becomes a validator in the same round
Each round's numbers were turned into checks so the defect cannot return: team colour at least 12 px and 12 percent of a
unit (it was 6 px, 6 percent), silhouette difference at least 22 percent between units of an era (was 16), building
team share 4 to 20 percent (was 2.4 to 29.5), a 2:1 luminance ratio between the two sides (was 1.3:1), a walk frame
that differs from the first by at least 8 px. **Rule:** a finding that is not a failing check will be reintroduced.

### 4. Judge the running build; a contact sheet flatters
Every sheet looked fine. In the running game the panel found: olive units quiet against olive grass, the cobble road
the loudest mass on screen, a scaffold identical for every building, a modern tower that read as a water tower, and
sprites clipped by the HUD. **Rule:** a visual panel is shown headless screenshots of the real build at play zoom (here
`xvfb-run godot --rendering-driver opengl3 -- --shot <absolute path> --shot-at <tick> --zoom 3`), base and fight, both
eras, before it is shown any sheet. Use an absolute output path: a relative one landed in the project folder.

### 5. Side identity needs luminance, not only hue
Blue and red teams differed 1.3:1 in luminance; in greyscale they were the same, and under protanopia red matched the
grass (1.1:1). **Rule:** assert a luminance ratio of at least 2:1 between sides in the build, wear team colour on the
largest readable surface (helmet and torso, not a stripe), and give every unit a non-colour cue the game draws (ring
for own units, diamond for the enemy). An overrule of a 3:1 fill-against-grass target is recorded with its price: it
would force near-black or pastel teams and lose hue identity.

### 6. Terrain is sprite art; the ground must be quieter than the figures
A road and wall texture at the same contrast as unit outlines blurred figure and ground. Pulling terrain toward its
tile mean (keep 50 to 70 percent of the texture) fixed the largest complaint without touching a unit. **Rule:** tune
the background last and against the sprites, with the figure/ground check on a real screenshot.

### 7. Show state in the art, not in a bar
Every building under construction used one identical scaffold. A dithered ghost of the finished building behind the
frame ("this will be a stable") tells the player what is coming. Construction, damage and ownership are art problems.

### 8. Seat the left-out player in round 1, not round 3
The accessibility seat (Game Accessibility Guidelines) graded D+ in R3 while Arnheim gave B and Cairo B-; it found the
side-identity problem the others missed. It should have sat in R1. **Rule:** the "player the design leaves out" seat is
in every panel from the first round, and its method (colour-vision simulation, 50 percent downscale, greyscale) is part
of the brief, not a bonus.

### 9. Panels that reach the owner's grade are useful as a leading indicator
Seat grades (B, B-, C+, D+) averaged C+, matching the owner's "b to c". Ask seats for a hard letter grade and what holds
it below the next one; a seat that only lists objections cannot be compared with the person's verdict.

### 10. Look for a named tool across the owner's repositories, and say when it is not there
"Use the gdada sprite tools" matched nothing: `gdada` is a process skill, and `pixel-art-gen` is a 94-line random
rodent generator. The right move was to search the owner's whole repository list (not only the attached ones), report
what was and was not found, build the missing tool, and file it where the owner expected it (this repository).

### 11a. A critic's fix can point the wrong way; measure it before applying
The accessibility seat asked to darken blue toward #4a86f0 to improve contrast with grass. By its own luminance
numbers that blue equals the grass (0.25 against 0.25, a 1.0:1 ratio), worse than the 1.27:1 it was fixing. The fix that
worked was lighter blue (#7db4ff, 1.65:1 against grass) while the validator kept a 3.3:1 gap to red. **Rule:** compute
the effect of a requested change before applying it; an overrule may refuse the fix and still accept the finding.

### 11b. A dithered overlay is noise at play size
The first scaffold ghost (every second pixel of the finished building) read as speckle at 3x zoom (Krug, R4). A solid ghost,
roofline in full colour and lower half dimmed one shade, with thinner posts, shows what is being built.

### 11c. Grades across rounds
R1 (units only): owner B to C. R3 panel B, B-, C+, D+. R4 panel B+, B-, C+. The accessibility seat moved the most (D+ to
C+) because its findings were measurable and became validator checks; the usability seat moved on shape changes
(modern tower, roofs). The round cap ended the run with no PASS: ship the strongest variant and log the open items.

### 11. Overrules name the trade in the player's units
Refused moves in this run: a team-colour ring baked into every sprite (costs 6 to 10 body pixels per sprite for a cue the
game already draws), a turretless light tank (removes the one shape that says "tank"), a 30 percent infantry silhouette
floor (humanoids share about half their pixels; reaching it needs a different body type), per-side banner shapes
(doubles every sprite per side). Each is logged with what it would cost.

### 12. Facts worth keeping
- Headless Godot 4.3 renders screenshots under `xvfb-run` with `--rendering-driver opengl3`.
- Godot's `--shot` path is resolved against the working directory only if absolute; use absolute.
- Python bytecode (`__pycache__`) ends up in commits unless `.gitignore` has it before the first `git add -A`.
- Sub-agent seats finish a short, file-backed brief in 20 to 45 seconds; three at a time with a verdict file each was
  reliable (no lost verdicts in 11 seats).
- Bob (a one-pixel drop) is the cheapest second walk frame for vehicles; humanoids need leg and arm changes or the cycle
  reads as a flicker (validated by a 8-pixel minimum difference).

## Tidewatch modern warfare and banners (Nov 2026)

Context: owner direction "focus on modern warfare ... tanks and whatnot to do hoi4 type battles do per banner colors yes".
Run 3: three new modern units, six factions with their own colours, emblems and flags. One panel round: Meier C+,
Norman C, accessibility B-. The grades fell from the B the owner had just given the art because the panel judged new
content and a mechanical question (is there a real choice?) the earlier rounds never asked.

### 13. A game-design seat belongs in an art-and-roster run
Meier (interesting decisions) computed time-to-kill and cost-efficiency for every unit pair from the rules data and found
what no screenshot shows: the heavy tank was a must-build (4.75x a rifleman, 4.5x a medium tank), two units were
near-dominated, and the AI never fielded the heavy tank in 9 matches. **Rule:** when a run adds units, seat a mechanics
critic with the rules data and a script, and print the pairwise matrix in the log.

### 14. The AI is part of the balance: it must be able to afford the design
Cheap barracks and stable units spent every coin before a 130/220 vehicle was affordable, so heavy armour was never built
(0 in 9 matches). Letting the workshop reserve its pick's cost and hold it for 600 ticks took heavy tanks to 27 in 9
matches without changing the win rates (4, 5 and 3 wins). **Rule:** after a balance change, count what the AI fields
(per kind, over several matches), not only who wins.

### 15. A metric floor can force a worse design; check it with a reader
The silhouette floor (22 percent) made the tank destroyer a tall slab, which the usability seat read as a fridge. A low
wedge that looks like a tank destroyer measured 19.9 percent. The floor was lowered to 19 with the reason written next to
the constant. **Rule:** when a validator and a reader disagree, the reader wins and the threshold is changed in a commit
that says why; never edit a sprite until it passes a number it should not have had to pass.

### 16. Faction identity is a data-driven property of every asset, and it is checkable
Six factions, each a colour pair, a 3x3 emblem and a flag shape, are baked per faction; the validator checks that any two
factions differ by at least 3 pixels on every unit and building (the mark is really there), that every light faction is
at least 2:1 in luminance from every dark one, and that emblems are distinct. A match always pairs light with dark.
Emblems on dark factions needed a 1 px ink halo (1.75:1 against the lifted highlight before it).

### 17. Draw the mark last, and neutralise anything that borrows a faction colour
Emblems drawn before the body were clipped on rider, wagon and heavy tank (3 to 4 of 6 pixels visible). Health bars that
took the faction colour read as damage when the faction was crimson. **Rule:** identity marks are the last draw call in a
sprite; status UI uses fixed colours and a neutral frame.

### 18. Screenshot cost is a design input
Software rendering reached tick 5,700 in under three minutes and could not reach tick 8,000 in ten, so no late-game
armoured battle was shown to the panel. **Rule:** add a staged-scenario flag (a fixed army placed at a fixed tick) before
the run needs a panel to see late-game content, and say in the brief what the panel was not shown.

### 19. State what the run did not build
The brief said "HoI4-type battles". The run built combined-arms units, bigger armies and faction identity; it did not build
fronts, supply lines or provinces, and the panel brief said so in its first paragraph. **Rule:** when the owner names a
reference game, list which of its systems the run builds and which it does not, in the brief and the final reply.

## Tidewatch grand-strategy pass (Nov 2026)

Context: owner direction "more hoi style now ... frontlines but not the tile provinces ... redo the vehicle art more to be
bigger and more menacing ... more grand strategy". Run 4: a front line with soft territory, strategic counters, a muted
map palette, 24x24 vehicles. One WHOLE round: Arnheim B+, Norman C+, accessibility C+.

### 20. A strategy overlay needs a scoreboard and an honest label
The front line and territory tint read as a combat boundary (chevrons, a bold line), but the run had given them no
rules effect. Norman (C+): "a strong signifier points at a mechanic that does not exist", and nothing quantified who was
winning. Fixes: a Ground split bar in the top bar (two faction colours and the numbers), and a first-use notice that the
front is information only. **Rule:** every overlay that looks like a mechanic gets (a) a number somewhere the player
reads, and (b) a line in the game saying whether it does anything. Whether it should matter is an owner decision; put it
at the top of the open items.

### 21. When a contrast target cannot be reached, change the cue, not the target
The accessibility seat asked for a 2:1 brightness split between the two territories. Measured: 1.04 to 1.24:1, and 2:1
needed a tint so heavy it hid the terrain. The refusal named that price, and the finding was met with a different cue: a
diagonal hatch (a canvas shader, so no extra art) on one side's land. The same "side 1" cue family runs through the
screen: hollow chevrons, clipped-corner counters, hatched land. **Rule:** pick one non-colour cue for each side and use it
on every overlay; keep the colour channel for faction identity.

### 22. Make the overlay computable and test it without a screen
The front is data (`front.gd`: influence field, marching squares, control share) with a headless test: control sums to 1,
the front is a line of finite length within the span of the keeps, removing the enemy's troops moves control the right
way, the tint is 24x24 nodes for 96x96 tiles (soft, not tiles). Shaders and drawing stay outside the test. **Rule:** a
visual system is logic plus a drawing; test the logic headlessly and judge the drawing with screenshots.

### 23. Bigger and more menacing is mass, slope and a low stance, not detail
Vehicles at 24x24 (a tile and a half beside 16 px infantry) read as heavier at once. What made them menacing: dark
gunmetal under olive, sloped hulls, side skirts, many road wheels, long guns with brakes, a twin-gun heavy tank, amber
sights. What made them toy: tall whip aerials and upright boxes (Arnheim). Removing the aerials and angling the bodies
helped more than adding detail. The size change also needed per-size thresholds (`UNIT_BIG`) and size-aware drawing
(anchor, ring radius and health bar position from the texture size), not a constant 16.

### 24. Palette changes and readability trade against each other; measure the unit against the new ground
The muted campaign-map palette made the terrain calmer and the front lines clear, and it cost units contrast (tank
body 1.0 to 1.4:1 against ground, no better than before). Lifting the olive highlight fixed part of it. **Rule:** when the
background is regraded, re-measure unit-against-ground contrast in the same round, not the next one.

### 25. Counters are a second drawing of the same data; test the switch
Below zoom 1.3 sprites give way to counters (box in faction colour, arm icon, count). First pass: icons and digits were
illegible and the two sides' counters overlapped (Norman). Fixed by 30 percent larger counters, 16 px digits and fanning
the sides apart; a hover tooltip and a legend are still open. **Rule:** any zoom-dependent representation needs a legend
or tooltip, and a screenshot at the switch threshold in the brief.

## Tidewatch run 5: bringing it together (Nov 2026)

Context: owner direction "bring everything together battle planning etc keep developing dont stop until questions push it
to quality", then a captured-mines economy (metal, oil, uranium). Built: the front as a rule, battle plans (player and AI),
the mines economy, sound, tests, docs. One WHOLE round (R9): Meier, Norman and Swink, all C+.

### 26. Make the overlay a rule, then give the rule its feedback
Run 4 left the front as information only and Norman marked it down for that. Run 5 made it matter (supply and attrition by
territory, a ground victory), and the same seat then marked down the missing feedback: a tooltip that still said
"information only", no sign of which troops were out of supply, no warning before a win on ground. **Rule:** a new rule
ships with its signifiers in the same round: a tooltip with the real terms, a ring or icon for the state it creates, a
countdown for any timed outcome, and a notice at each threshold.

### 27. Time-to-afford is the number that says whether a resource gates anything
Meier computed that a heavy tank needed 12 uranium and one mine paid 30 a minute: 24 seconds. The real gate was oil. After
slowing uranium to 10 a minute the cost is 72 seconds of one mine, and the AI chases uranium only while it holds none.
**Rule:** for every gating resource print cost divided by income of one source; if it is under a minute the gate is
decoration.

### 28. Free-to-hold income is a snowball; give holding a cost
Mines paid for ever once captured. Fixes that created tension without new UI: half pay without a nearby friendly unit, no pay
while an enemy stands beside it, half for 30 seconds after a capture, home mines always full. **Rule:** a captured income
source needs an upkeep in attention (troops nearby), not coins.

### 29. A test that passes when nobody plays is a bad test
Changing the economy left the AI issuing 0 commands for 30 minutes (its build steps were gated on worker counts the new
economy never reached) and every match "ended" in a draw. `ai_match` now fails any match with fewer than 20 commands.
**Rule:** assert that the thing under test acted, not only that nothing crashed.

### 30. Tune a rare exit by its tests, not its frequency
The ground victory ended 0 of 36 matches in the first report and 2 of 18 at 4:30 after a loosening (too early to mean
anything). Setting a minimum match time and keeping it rare (0 of 18) is acceptable if a headless test proves the exit works
and the HUD announces it. **Rule:** an exit that needs dominance should be rare; verify that it works and that it cannot
fire early, not that it fires often.

### 31. Fast-forward and transitions fight each other
A cross-fade between successive fronts looked broken in screenshots because the capture fast-forwards the simulation: every
frame restarted the blend, so the line mixed stale and new positions. Two fixes: the glide length follows game speed, and
screenshots skip it. Vanishing segments must fade out and new ones fade in, or the line breaks during any glide.
**Rule:** any animation driven by the simulation's update cadence is checked at x1, at x8 and under a fast-forwarding
screenshot.

### 32. Events in the world need a place in the world
Mine captures and losses were text only. Notices now carry a position and the scene draws a ring there, with a sound; plan
completion, cancellation and loss each say which. **Rule:** a notice about something on the map carries a map position.

### 33. Generated sound is enough to stop the silence fault
No audio files were needed: short tones synthesised into a `AudioStreamWAV` at start-up (order, plan, capture, loss, warning,
plan done, win, lose), a six-player pool and a mute key. The game-feel seat had graded the silence as a fault for a command
game. **Rule:** cues for command acknowledgement and for losses; mute on one key.

### 34. A cut-off message is information: say what was understood and carry on
The owner's message arrived truncated ("Also we ha"). The run stated its reading of the rest in `VISION.md`, built to it,
listed the cut as an open item and asked nothing that did not block work. **Rule:** log the cut, state the reading, keep
moving, and show the reading in the first line of the reply so the owner can correct it cheaply.

### 35. A personality built on a lever that no longer exists has no identity
The AI's "boomer" wins by building the biggest economy. In a mines economy income is flat (it comes from fixed sites),
so there is nothing to boom and the early-aggression "rusher" wins about 70 percent. Number tuning (first wave, outposts,
grace period) moved it from 76 to 71 percent and no further. **Rule:** when an economy changes, ask what each AI
personality's plan was optimising and whether the new rules still have that lever; if not, redefine the personality (for
example: the boomer holds more mines and garrisons them, the turtle fortifies mines) instead of tuning numbers.

### 36. Scale a held income with the effort of holding it
Mine pay by garrison size (25 percent with no troops, 100 percent at three) gave a continuous trade-off (spread thin or
concentrate) where an on/off garrison rule tied up one troop only (Meier, R10). A persistent bar under each mine shows the
current rate, so the rule is visible in the world, not only in a tooltip.

### 37. Re-grade after fixes, but cap the rounds
Run 5 went C+, C+, C+ (R9) to B-, B-, B- (R10) with fixes in between and a round cap of three. Two rounds raised every seat one
step; the remaining objections were new (small) rather than repeats, which is the sign that the panel is converging.

### 38. A freely rotating view needs models, not drawings
A world that rotates freely (isometric, run 8) needs every unit from every heading. Hand-drawing 16 facings per unit is not
realistic and the facings would not match. Draw each unit once as a few solid parts (boxes, wedges, prisms) in materials and
project it (`tools/sprites/iso.py`): shading, outline, shadow, team colour and faction emblem come out the same at every angle,
and the existing validators (team pixels, distinct frames) carry over per facing. Limits seen: no round wheels or thin
diagonals, painter sort by part centre (split long parts), flags vanish edge-on.

### 39. Split art authoring across agents by file, and look at the sheet yourself
Three agents modelled infantry, vehicles and buildings in separate files against one tested example and one validator. All
three reported 0 build problems and three honest lists of flaws; the build does not catch a muddled silhouette, so the
orchestrator still opened the contact sheets. Keep a shared registry that merges the per-author modules, forbid edits to the
renderer from authors, and ask for renderer wishes in the report.

### 40. Project the whole view, not the sprites
Isometric in a 2D engine is one affine transform for the flat layers (terrain, fog, tint) plus the same function applied to
every drawn point, with sprites staying upright (billboards) and sorted by projected y. Route every world-to-screen and
screen-to-world conversion through two functions and test the round trip at several angles; the real-input play test then
keeps working with small edits.

### 41. Relief is a mesh, and it must be un-projected
Hills in a 2D engine: one mesh whose vertices are projected with the height, hill shading in the vertex colours, triangles ordered far to near for the current view angle, every ground layer (fog, tint, tide) sharing it. Everything that stands on the ground uses the same height lookup, and clicks need the inverse: iterate (screen position plus the height at the guess, a handful of rounds). Test the round trip with relief on; three rounds were not enough (60 milli-tiles of error), six were.

### 42. A test that passes because the world already does the thing
Two terrain and towing checks were first satisfied by something else: an enemy standing out of supply loses health on its own, which looked like the howitzer firing. Check the cause (the shot record), not the effect (health went down).

### 43. Always check the concept art, side by side, after every render
The owner supplied two reference sheets (run 7) and later asked for ships "from the concept". Models are judged by what differs
from the concept, not by whether they look fine alone: crop the matching panel, open the render beside it, list the
differences, fix, repeat. Put the crop in the brief of any sub-agent and put a comparison sheet in the log. This is now a rule in
SKILL.md ("Concept art is a rule: always check it").

## Computer-player work (Tidewatch, runs 18 and 19)

* **Measure what each seat actually does, not only the result.** Four separate defects hid in AI-versus-AI matches that "worked": a gate written on raw ticks that could never fire for players 1 to 3 (so every result had a hidden first-player advantage), a target search that went silent when the keep was never clearly sighted (the AI stood still for 38 minutes), money saved for a rare unit that starved the army, and soldiers that could not path to an aircraft parked on a solid airfield. Each was found by printing per-player state at fixed times and then forcing the order by hand to see whether the order or the decision was broken.
* **Give every AI feature a staged scenario test** (build the situation, run the AI, assert the outcome) *and* print its counters in a full match; the scenario proves it can work, the counters prove it does.
* **Smart means deciding from what was seen.** Keep a sightings memory with an age; choose targets from it, never from the world state.
* **A stalemate is a bug report.** If matches hit the time limit, look at what the idle units are doing before changing numbers.
