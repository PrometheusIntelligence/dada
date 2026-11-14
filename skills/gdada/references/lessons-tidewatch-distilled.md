# Tidewatch lessons, distilled (one page per theme)

Read this before the first week of a new game. It is a digest of Tidewatch's `GDADA-LOG.md` (runs 1 to 38), the
"Games" lessons 65 to 152 in dada-lessons `LESSONS.md` (cited as L65 to L152), the five gdada skills, the SHADW Terrain
`DESIGN-LOG.md` addenda (realm port, era packs, the rubber-stamp gallery, the low-key rebalance) and Tidewatch's
`SHADW.md`. Each lesson is a statement plus its evidence in 2 to 5 lines. "Run N" is a Tidewatch GDADA run; "Terrain log"
is the shadw-terrain DESIGN-LOG. Where a lesson comes from working practice rather than a log entry, it says "practice".
Themes are ordered by what a new game needs first: 1 process, 2 determinism, 3 simulation, 4 AI, 5 balance, 6 art
pipeline, 7 legibility, 8 procedural generation, 9 stack integration, 10 tooling, 11 credit and push.

## 1. Process and honesty

1.1 **Write the owner's words down first, verbatim, before planning.** Every message, typos included, became a dated
    change-log line and a numbered Must-have in `VISION.md` (68 by the end), marked `owner` or `inferred`; plan and stop
    test were judged against that file. Run 7's brief was nine directions at once and only Must-have 19 was built; the
    rest was staged in `GAME-PLAN.md`, not claimed. From run 25 quotes stayed only in log heads: a gap. (L65; runs 1, 7, 25)

1.2 **Record the reading you took; keep unreadable messages as open items.** "floating A on that tank" was read as a
    flat faction badge over the turret and fixed by projecting the emblem onto the turret top (run 10); the cut-off
    "Also we ha" stayed an open item through runs 5 and 6. Neither was silently guessed. (L66; runs 5, 6, 10)

1.3 **"Looked at" and "measured" are different claims; every entry ends with a Not-done list.** From run 6 on each entry
    names what was not built, not measured or seen once ("the new menu was seen only in code", "sound never heard by a
    human"). Run 1 printed a claim audit: 11 measured, 6 computed, 3 assumptions. The next run started from the lists.
    (L67; runs 1, 6, 11, 18, 25 to 34)

1.4 **Never write that a test passed when it printed no pass line.** Runs 25 and 34 logged `multi_check` and
    `net_check` as unconfirmed, not green. Run 6 is the opposite failure: an AI patch silently did not apply (wrong
    path), tests passed vacuously and a commit message claimed behaviour that was not there (corrected in 8ddc866).
    Assert that a patch applied by exercising the behaviour it adds. (L68; runs 6, 25, 34)

1.5 **A test that passes because the world already does the thing is not a test.** Run 7's `town_check` asserted before
    the command ran (commands apply on the next step: step first); run 11's fan test passed with the squad scattered over
    24 tiles (a bound was added); run 12's checks were satisfied by out-of-supply attrition (check the shot record); run
    16's connectivity check used a path search that returns a partial path. (L69; runs 7, 11, 12, 16)

1.6 **A single voice is not a panel, and a round cap needs an honest ending.** Run 1 wrote every seat itself and left the
    compliance line unticked. Runs 2 to 5 hit the round cap with no PASS (best grades B+, B-, C+) and were marked
    incomplete, the strongest variant shipped, open items given an owner, post-cap fixes labelled "measured, not
    re-judged". (L70; runs 1 to 5)

1.7 **Test a critic's premise before spending a move.** The accessibility seat asked to darken blue toward #4a86f0; it
    measured 1.0:1 against grass (0.25 vs 0.25), so the request was overruled with numbers (run 2). A 2:1 tint split was
    refused the same way (real split 1.04 to 1.24:1) and a hatch used instead (run 4). Turn each measured finding into
    a validator. (L85; runs 2, 4)

1.8 **Commit and push every run; a log entry for unpushed work is a claim about nothing.** The owner twice asked for
    pushes to main; run 6's inaccurate commit was found and corrected by hash. Keep the run's commit, pushed hash and log
    entry together. (L72; run 6; VISION change log 2026-11-10. The stop-hook idea is practice.)

1.9 **Say what the agent did not do for want of access.** Run 35: the owner's backup repository could not be added, remote
    branch deletion was refused, history rewrite was left as the owner's call. Each was written down, not worked around.
    (run 35)

1.10 **Stop-test items that are not met are stated, not renamed.** Runs 1 to 5 each printed S1 to S7 with "not met" where
    true and the line "marked incomplete under the round cap; the strongest variant ships". From run 6 the entries are
    short "Built / Measured / Not done" notes and no longer print the stop test; keep both. (runs 1 to 6)

## 2. Determinism and replay

2.1 **One deterministic simulation behind the screen and the tests: fixed tick, integers, command log, state hash.**
    Integer milli-tile positions at a fixed 10 Hz; every order, the AI's included, goes through `command()` into a log;
    replaying the log reproduces the state hash. Run 1: 100 commands for seed 1, identical hash every time; `ai_match`
    re-checked it after nearly every sim change (runs 6 to 38). Because the AI uses the player's interface, each test is
    a fact about what a player can do. (L89; runs 1, 6 to 38)

2.2 **Nothing visual in the hash; every new piece of sim state goes into it.** Relief, projection, ghosts, fog hatch and
    effects live in the screen; hit rolls are deterministic seeded rolls in the sim (run 13); terrain changes (rubble,
    bridges) are a sim table the screen repaints (run 14). The silent hole is a new rule (fronts, supply, fuel, programme
    meter, entrenchment) left out of the hash: replay and desync checks pass while the match has diverged. Re-read the
    hash function in every run that adds sim state. The log records no incident; this follows from how the check works.
    (L91; runs 13, 14. Practice for the hole.)

2.3 **Replay hash identical is the minimum gate after any sim or AI change, and it is cheap.** "ai_match replay hash
    identical" closes runs 6, 8, 11, 13 to 20, 27, 34, 37, 38, including on new maps (Terrain maps, revolution
    urban_sprawl, medieval flatlands). A matching hash proved determinism, not balance or liveness: the same runs ended
    on stalls. (runs 6 to 38)

2.4 **Networked JSON turns integers into floats.** Integer-keyed dictionaries missed unit ids in networked orders and
    `[0.0].has(0)` was false, so every seat looked like a computer player. Convert whole floats back to ints. Float use
    across browsers remains an unverified desync risk. (L92; run 18)

2.5 **Lockstep over plain HTTP works when the sim is deterministic: exchange orders, never state.** 5 ticks make a turn;
    an order given in turn T runs in T+2 everywhere; a relay holds a turn until all orders are in and never runs the
    game; computer players run identically on every machine; a state hash every 20 turns warns of desync. Measured: two
    machines, two computer players, local relay, 1500 ticks, identical hashes. Never run: Vercel, other browsers, 3+
    people. (L117, L118; run 18)

2.6 **Do not size state for two players.** `Front`, `spot_until`, `ground_ticks` crashed with four sides. Start
    positions must be spread (`pick_spawns`): four spawns 0 to 3 put two sides 16 tiles apart and one died by 9:00.
    (L93; run 18)

2.7 **Cross-engine determinism needs its own arithmetic.** The Terrain port bans `Math.sin`, `exp` and `pow` (an ulp
    difference between engines can flip a threshold) and uses hash-addressed noise with IEEE-only operations. Verified
    in Node and by the browser module equalling the Node module; not run in Firefox or Safari. (L149; Terrain log
    2026-11-12)

## 3. Simulation architecture

3.1 **Simulation separate from the screen from day one.** Godot nodes and physics were rejected for a plain simulation
    in integer milli-tiles; one simulation behind both screen and headless tests means every test is a fact about the
    playable game. (L89; run 1, M1)

3.2 **Write speeds in the sim's own units and print one check in player terms.** Speeds written as tenths of a tile
    per tick made units crawl at 0.2 tiles/s (a spearman covered 0.5 tiles in 2.5 s). Fixed to 1.4 to 2.3 tiles/s; a
    real-input check that the move arrives within 6 s; mean match fell from 16:44 to 7 to 12 min. Keep the conversion
    (100 milli-tiles per tick = 1 tile/s) in the carry-forward ledger. (L90; run 1, M9)

3.3 **Time-driven effects are bounded by the data they encode.** The tide floods 332 tiles for 50 s of every 180 s with a
    20 s warning; a clock may change when a thing shows, never how much. Terrain's flood area grew while hosts stayed 14;
    area became a function of fallen hosts. (L152; run 1, M3; shadw-terrain M3)

3.4 **The tide, front, supply and plans are rules owned by the sim, or they are decoration.** Run 4's front line had no
    rules effect and Norman objected "the line looks like a mechanic and there is none"; run 5 moved it into
    `sim/front.gd` (supply, attrition, ground victory). Information-only overlays are allowed if the game says so.
    (runs 4, 5)

3.5 **Terrain change is a table over the map, repainted by the screen.** Collapse rubble, bridges, trenches: one
    `tile_over` table in the sim. The screen reads it; it never writes it. (run 14)

3.6 **Budget wall-clock time per match and per tick; cache anything per-unit-per-tile.** 3000 AI ticks took 2.0 s at 96
    tiles, 2.4 s at 160, 4.1 s at 192; an archipelago match took almost five minutes; line of sight was cached per unit
    and tile. Long games make every balance run slow. (L94; runs 11, 12, 16, 17)

3.7 **A shared map rule cascades through every map; keep the sweep in the loop.** Ports needing tidal flats moved every
    shoreline and removed a river (run 15); five tests assumed the old geometry (run 24); the first city had 4 buildings
    on too-steep ground (run 21). Run the stats table for all kinds after each shared change. (L114; runs 15, 21, 24)

3.8 **New rules mean new gates, and each gate needs an exit.** The AI's gate on raw ticks never fired for players 1 to
    3; an unfinishable site re-issued `assist` 1217 times; stuck work must expire (90 s with no progress). (L95, L98;
    runs 6, 19)

3.9 **Terrain generator and game agree on the connectivity rule.** The game marks a tile a cliff when any neighbour
    differs by more than 18 in rounded height and floods tidal flats at high tide; a float edge-step check called maps
    connected that the game cannot cross. Mirror the consumer's rule in the validator. (L146; Terrain log 2026-11-12)

3.10 **Decide hotkeys from a table and grep it.** Rotation on Comma and Period clashed with "idle worker" and "army";
    Return on H clashed with help; P clashed with pause. (L110; run 9)

3.11 **Assets grow silently.** Sprite bundle 5.6 MB (run 10), 31 MB (run 22), 35 MB at the end, loaded whole; "split per
    era" was logged open in runs 22, 24, 27 and never done. Measure load time and web size before the third doubling.
    (L87; runs 10, 22, 24, 27)

## 4. AI (the computer player)

4.1 **The AI plays through the player's `command()` and never writes state.** Opponents that play the same rules feel
    fair and the tests prove what a person can do; every AI action is in the command log and the replay passes. (L89;
    run 1, M4)

4.2 **Gate behaviour with a think-tick helper, never raw ticks.** The AI thinks on ticks where `tick + 3*pid` is a
    multiple of 10, so `(tick + 7*pid) % 30 == 0` can never fire for players 1 to 3. Crewing, research and invasion ran
    only for player 0: every earlier two-AI result had a hidden first-player advantage. Use `_due(period, offset)`.
    Found because a test's guns were never crewed. (L95; run 19, defect a)

4.3 **Passivity is the commonest failure: no sighting means no war.** `_enemy_keep()` returned nothing when every start
    was seen but the keep was not (hills block sight) and `_control()` returned early for ever: 14 attackers idle 68
    tiles away for 38 minutes. Found by printing attacker states at 22:00 and forcing a plan. Fix: fall back to the
    enemy's public start position, plus a pressure timer (send everything after eight minutes without an attack).
    "A stalemate is a bug report": look at what idle units are doing before changing numbers. (L96; run 18, defects c, d)

4.4 **Decide from what was seen; no cheating.** No bonuses, no free look at the map. The AI keeps an intel memory with
    ages (entries die after 900 ticks), marches to unexplored starts under fog and counts only enemies it has seen. The
    rusher stays plain on purpose; boomer and turtle use everything. (L100; runs 1, 8, 19)

4.5 **Intel and escorts before attacks; a blind attack feeds the enemy.** Run 20, five defects on one staged fort: the AI
    attacked before scouts reported (no intel counted as no defence) and lost 21 units; scouts circled a never-seen
    start at 13 tiles; the battery waited for an escort the held-back army could not give; with escorts relaxed it died
    on the way; three engineers walked past the line and killed the undefended keep. Fixes: scouts go to the place, an
    assault gate waits for a fort report, escorts travel with guns, charges cut. (L99; run 20)

4.6 **Reserving for a rare unit starves the army; check what production really does.** The airfield was never built
    (build step wanted 7 workers; the cap was 6), then aircraft never trained because ground production spent every
    coin; saving for guns left player 0 at 10 army supply at 16:00 (now waits for 14); stables built vehicles nobody
    drove (crews first); no invasion because all infantry were crews. (L97; runs 9, 17, 18, 19)

4.7 **Prove an AI behaviour fires: count commands per type in AI-vs-AI runs, and also stage a scenario.** The scenario
    proves it can work, the counters prove it does. Run 19's scenario tests passed while a full boomer-vs-turtle match
    showed garrisons and pillboxes but no raid and no battery volley in 24 to 35 minutes. Runs 26 and 34 counted
    stances, deploys, charges and ambushes issued (7 ambushes on highland_forest); `ai_match` fails a match under 20
    commands. (L101; runs 5, 19, 26, 34)

4.8 **Personalities are different rule weightings, not different cheats.** Rusher, boomer, turtle; later era
    personalities with a `favor` (Hellenic Phalanx, Legion, Horde, Feudal Host, Line of Battle). Report wins per
    personality and per spawn. A personality whose plan has no lever in the economy loses its identity: the modern boomer
    had no economy to boom because income was flat, so early aggression won (run 5, open). (runs 1, 5, 24)

4.9 **The AI counters what it sees.** Training picks counters by weight (archers draw riders; riders against shield wall,
    engines against turtle, archers against spear wall); stances respond to threats (spear wall when riders near,
    turtle on a long walk under 6+ missile troops). One test per counter (`stance_check`: 8 riders vs 8 spears left 752 hp
    in spear wall against 516 open). (L107; runs 1, 26)

4.10 **Unreachable work, unreachable targets and unreachable sites expire.** A hub site the AI could not finish blocked all
    construction (two 60:00 caps, about 6,900 commands; assists fell 1217 to 167 after the fix); a helicopter parked
    inside its solid airfield could not be boarded by anyone. (L98; runs 6, 19)

4.11 **AI STALL: OPEN PROBLEM.** Medieval AI-vs-AI matches ran the full 60:00 with no keep falling on the new Terrain
    medieval map (run 36, terrain_flatlands), on the old Python flatlands with no castles (confirmed by the Terrain log:
    "not a map defect"), and on the low-key AoE-style age maps (run 38, ancient and medieval); revolution urban_sprawl
    ended at 22:18 with no keep fall (run 37). It is also a long-standing pattern in modern: caps in 2 of 6 (run 7),
    2 (run 8), 3 of 6 (run 13), 2 (run 14), 3 of 4 (run 15), 3 of 3 (run 16), 2 of 4 (run 17), 2v2 bay_war no decision in
    40:00 (run 18; armies of 60 to 100 idle or trickling in 12 to 14 unit packets that die).
    **Tried:** capped waves and an early attack when clearly stronger (run 1); the pressure timer (run 18); sites must be
    reachable and stuck work expires (run 6); the gate fix for players 1 to 3 (run 19: keeps fell 3 of 4, from 2 of 4);
    the nuclear race (caps 3 to 2, run 14); scouts, assault gate, escorts, siege batteries (run 20: 4 of 4 coast matches
    ended by a fallen keep); formations, charges and ambushes (run 34); removing per-spawn forts and the map's castles
    (runs 36 to 38: the stall did not change, so the map is not the cause).
    **Not tried or not measured (hypotheses only, none confirmed):** whether the assault gate (needs a fort report,
    engineers and guns) never opens against a walled keep; whether the medieval roster trains siege engines at all in
    matches (count trebuchet and bombard commands); whether waves launch and die in packets below the size a keep needs
    (as in run 18); whether the pressure timer fires; what the idle units are doing at 30:00 (the run 18 method).
    **Next step:** run the run-18 method on a stalled medieval match: print per-state unit counts and commands per type
    at 15:00, 30:00, 45:00 and 59:00, then force a plan at the keep to prove orders work. Do not tune numbers first.
    (runs 36, 37, 38; Terrain log 2026-11-14)

4.12 **A stalemate needs an ending mechanism added with the rule that lengthens the game.** Caps climbed with every
    rule that lengthened play; the race cut caps from 3 to 2 but not to 0. On the archipelago the AI "won" at 14:00 to
    18:00 by each side holding its own island, so ground victory is off there. Add the ending (attrition of a stalled
    front, escalation to heavier armour, a growing pressure) with the rule, not after. (L106; runs 7, 13 to 19)

## 5. Balance

5.1 **Do the income arithmetic before the AI run.** Uranium burned 1 per 6 s, more than a mine paid, so no programme
    finished (now 15 s); manpower 1 per 3 s piled up to 1,330 (now 1 per 9 s); a heavy tank was 24 s of one mine (now
    72 s). Run 1: timber was the only bottleneck (2,000 salvage, 10 timber); before the fix 3 of 9 matches ended by a
    fallen keep, after 9 of 9. (L105; runs 1, 5, 7, 14)

5.2 **Bot runs are the main instrument for economy balance, not only solvability.** The bots found what a description
    could not (the speed bug, timber starvation); the graph gained an edge `bots --> machinations`. (L105; run 1)

5.3 **Balance by cost-equal set pieces, and know what "Lanchester close" means.** Equal money (5000 a side) in a square-law
    fight should leave the winner a small remnant. Run 27: winners kept 4 to 14 percent (ancient 403 vs 0, medieval 559
    vs 0, revolution 216 vs 0, modern 692 vs 168) but side 0 won all four, never a draw: position bias not isolated. Run
    24's first set pieces were lopsided (Athenians 4 vs Romans 31) and a modern mirror ended 8 vs 25: a mirror must be
    even. (L103; runs 24, 27)

5.4 **Set pieces and AI matches answer different questions: use both.** The Horde was shredded head-on yet destroyed
    Valemont's keep at 15:26 in an AI match because the rusher rushes before the heavy troops exist. (L104; runs 1, 24)

5.5 **Report per personality and per spawn.** Run 1: spawn-4 won 10 matches, spawn-0 won 3: a map question, not an AI
    one. Hidden gate bugs (4.2) made player 0 stronger in every earlier result. (L104; runs 1, 19)

5.6 **Scenario spread: a scenario needs several spots and several maps.** `--spot N` (the Nth best open field at least 36
    tiles from the better ones) was added because "all around the same house". Spawn pairs used in tests ([0,1], [6,4],
    [7,4], [5,7]) are carried forward because results depend on them. (L102, L115; runs 1, 33)

5.7 **Test one counter per rule, with numbers from the first run, not "it passes".** Stance tests give 752 vs 516 hp;
    tactics tests give 5 of 5 lurkers in trees; supply 22 checks; nuke 24 checks. (L107; runs 6, 14, 26, 34)

5.8 **A cause named is not a fix.** Run 5: modern rusher won 67 percent; trimming outposts and wave sizes brought it to
    about 71 percent of 17 from 76 and the log says so, naming the cause (no lever for a boomer in flat income) and
    leaving it open. Run 6: the turtle, built to punish rushes, was weakest at 1 of 7. Say "not fixed". (runs 5, 6)

5.9 **Measure the long game on the long maps.** Mountain and city games ran 41:31 and 44:46 (old map about 30); coast with
    hit chances 38:25 mean with three caps of six; sea maps 53:27 mean. Longer is what the owner asked for; caps are
    still defects. (runs 13, 15, 16)

5.10 **Fair starts are an identical start area, not an identical fort.** Run 38 replaced per-spawn forts with an AoE-style
    start (clearing, two wood groves, salvage, stone, berries, game) on a ring; measured worst-start deviation: forest
    0, resource sites 0, route to nearest neighbour 11.1 percent, landmark route mean 10 to 12 percent (worst 19.6 to
    31.3); still unbalanced for sea kinds (shore access 55 to 62 percent). (Terrain log 2026-11-14; run 38)

5.11 **Balance of the AI on low-key maps is untested.** With no forts to defend the AI's behaviour on the new starts is
    unmeasured; the 16 maps per age were measured for terrain fairness, not match win rates. (run 38; honest gap)

## 6. Art pipeline

6.1 **Split by file ownership, brief as a contract, one build by the lead.** Run 8: three agents in separate files; run
    22: five in parallel; run 24: six. Each author owns one file hooked in by a list the lead edits, gets the kit, sizes,
    team-colour rule and concept crop, previews into its own scratch directory, never runs the shared build. In run 22
    the build gave 0 problems after authors fixed their own 247 first-bake failures. (L73; runs 8, 22, 24, 28)

6.2 **Validators fail the build; the failing kind goes back to its own author.** 247 team-colour failures in ten models
    were fixed by their authors. A validator never replaces looking: three authors reported 0 problems and a list of
    flaws the build could not see (muddled silhouettes, boxy wheels). (L74; runs 8, 22)

6.3 **Authors over-grade: put an independent critic after every round.** Authors graded A- and B+; the critic graded "no
    A, most C+/C" with defects they had not named (pale team ramp, 1 px weapons, shared grey-ball helmets, flat back
    facings, knight and rider near-duplicates). Round 3's first A- (ancient legionary) was still a self-grade. Plan two
    rounds at least and label self-grades. (L75; runs 28 to 31; sprite-critique files)

6.4 **Density is a budget: raise the pixel budget before asking for detail.** A 14 to 20 px figure cannot carry faces or
    weapon heads. Run 25 upscaled foot soldiers 1.5x; run 28 2.0x (canvas 20 to 40 px) and then asked authors to spend
    it; faces were still 3 to 5 px. (L76; runs 25, 28, 30)

6.5 **Then scale density to the world.** "Units way too large for building scale": run 34 re-rendered at 0.72 of the dense
    canvas (foot about 29 px, pixel-aligned, not resampled) and storeys 6.5 to 7.5 px so a man is about one storey beside
    a house. Decide the ratio when setting the budget. (L77; runs 28, 34)

6.6 **Write the rubric before polishing.** Eight points graded A/B/C by someone who did not draw it: silhouette, anatomy,
    three details, value structure, team colour on every facing, facing consistency, era truth against concept art,
    pixel hygiene. Run 27 had no rubric and the owner said "c grade". (L78; runs 27, 28)

6.7 **The 1x view is what players see; judge there.** At 1x nearly every foot unit was a 10x16 px vertical blob; authors
    previewed at 6x; the medieval author made no 1x renders. Require 6x and 1x on green in every report and a silhouette
    test at 1x (never run in run 28). (L79; runs 28, 31)

6.8 **Make contact sheets from the baked output and look before believing a report.** Runs 28 to 31 each say "built but
    not viewed by me" for an era; critic 2 found two sheets showing only 6 and 5 of 8 facings (sheet layout, not the
    sprites). Sheets come from the final json. (L80; runs 28 to 31)

6.9 **Fix a global finding in the shared tool.** The pale cyan team ramp was changed once in the bake and `_paint` (lit
    tone = mix(main, dark, 0.4)); every sprite improved. (L81; run 29)

6.10 **Thin things vanish; the canvas edge is a hazard.** 1 px shafts drop out at 1x and at facings toward or away from
    the camera; shafts became 2 px with bright heads; the sarissa was levelled to about 25 degrees because a 45 degree tip
    left the canvas. (L82; runs 29, 31)

6.11 **Compare every art claim with the concept art, side by side.** The owner made it a rule; authors skipped it in runs
    29, 30, 31 and 33. Put the crop path in the brief, require "what still differs" per report, and where no concept art
    exists say so. (L71; runs 14 to 16, 21, 29 to 33)

6.12 **Decide the non-colour side cue early.** Per-side sprite shapes were overruled twice (doubles every sprite); the game
    draws a ring for own units and a diamond for the enemy; the sprites alone are not distinguishable in greyscale. Pick
    one cue once and let a validator check it. (L88; runs 1 M6, 2, 3, 32)

6.13 **Map data and renderer agree on a drawing for every style in every age.** "Buildings still do not appear, just the
    footprint": every map structure drew as wall and floor tiles; the medieval era had no isometric models (run 21). Keep
    map data neutral and cast per age; check each (style, age) pair has a drawing. (L86; runs 21, 22, 23)

6.14 **A visual rule that can be a number should be one.** Side luminance 3.3:1, team pixels per facing, silhouette
    floor 22 percent (19 for vehicles, an overrule with the measured minimum 19.9), sprite size per class. Run 32 and 34
    had "no test for visuals" and "judged by eye". (L124; runs 2, 3, 32, 34)

## 7. Legibility

7.1 **Health bars: 1 px hairlines, only when hurt (below 70 percent) or selected; neutral-framed with a green, amber, red
    fill.** "Health bars too big and distracting" (run 25). A faction-coloured bar read as damage (run 3). (L84; runs 3, 25)

7.2 **Team discs, not rings.** Rings turned crowds into tangles of circles; a soft team-coloured disc under each man read
    (run 32; run 25 had already limited rings to own units). (L84, L88; runs 1, 25, 32)

7.3 **Quiet effects, felt battles.** Dust and smoke puffs at half opacity, casualties (corpses, wrecks, sparks, muzzle
    smoke), sounds (clash, arrow, death, boom, horn), marching bob, lunge, recoil, topple. Send each man across on his own
    file so the crowd does not collapse to a point. (L84; runs 25, 27, 32)

7.4 **A `--clean` mode hides overlays so screenshots can be judged.** `--clean`, `--battle`, `--siege`, `--parade`,
    `--pair`, `--spot N`, `--intel` all feed screenshot sheets. Software rendering is too slow to reach tick 8000; stage
    the scene. (L102, L120; runs 3, 20 to 24, 33)

7.5 **Big buildings are outlined in a dark tone of their own colour; terrain is quieter than figures.** A big building
    without an outline looks like terrain; terrain with figure-strength texture looks clutter. Run 2: terrain keeps 50 to
    70 percent of its texture; run 32: the first themed terrain was too busy and toned down by eye; run 36b/37: ink
    outline baked into every cached structure ("they fade into the background"). (L83, L138; runs 2, 32, 33, 36b, 37)

7.6 **No green slabs for earthworks.** "No green hedge walls": ramparts and bastions became a brick scarp with stone
    cordon, a dark earth parapet faced with fascines, gabions, embrasures, glacis only a muted dirt tint. (L137; runs 36b,
    37)

7.7 **Surface detail lives behind a texture cache with a benchmark.** Each structure drawn once into a texture; 176
    structures: 37 to 56 ms a frame down to 1 to 3 ms (software GL 97 to 280 ms down to 40 to 67 ms); banners, smoke and
    sails recorded and replayed. Stalls in the first frames of a shot can lack outlines while the cache fills. (L139; runs
    36, 37)

7.8 **Every signal has a text and a sound path.** Notices with a map marker for captures and losses; plan complete,
    cancelled, lost; `can_train` names the missing resource; hover text for counters and the Ground bar; generated cues;
    `M` mutes. Norman's findings "silent or generic" were the largest UI group in run 5. (runs 5, 6)

7.9 **A sprite colour that means damage cannot mean a team.** The hit flash tints red; a blue vehicle read red (run 2,
    overruled: the flash is hit feedback). Keep status colours and team colours disjoint where cheap. (run 2)

7.10 **A tested shape the camera hides is not yet a feature.** Square against wedge is not readable at the game camera;
    players cannot drag a line's facing or width. (L109; run 34)

7.11 **Colour-only distinctions fail accessibility seats.** Ground bar label contrast failed once the blue share was small
    (dark plate fix); a hatch on side 1's territory, hollow chevrons and a clipped counter corner carry the side without
    colour; plan numbers 1.8:1 at 9 px became outlined 11 px. (runs 4, 5)

## 8. Procedural generation

8.1 **Preview first, and keep a gallery per age.** Three layout bugs (ragged outline, missing cathedral, empty bailey) passed
    every assertion and were seen at once in a preview (`tools/preview-realm.ts`). The renderer has the same gate: a
    style gallery (`--gallery ancient|medieval|revolution|modern`, `--shot`, `--bench N`) and `gallery_check.gd`. (L132;
    Terrain log 2026-11-13; run 36)

8.2 **Grade the sheet by eye BEFORE adding invariants: the rubber-stamp lesson.** The 64-map demo gallery (4 ages x 8 kinds x
    2 phrases) had `checkForGame` at 0 problems, yet every 96 and 128 land map was the same square moated fort at eight
    evenly spread spawns, so flatlands, river valley and highland forest differed in ground, not layout; urban_sprawl was
    one giant square walled city (about 80 percent of the map); revolution plazas were cross-shaped fields of bastions.
    A generator that passes every invariant can still be a rubber stamp. Put a variety measure in the gallery (distinct
    fort footprints per map, structure-style entropy) and grade the sheet first. (Terrain log 2026-11-14)

8.3 **Low-key beats dense: a few big structures, mostly undeveloped terrain.** The owner: "generating way too many big
    castles". Before: 120 to 300 structures and 8 forts per 96-tile map. After (0.5.0): 20 to 51 structures, 1 to 2 big,
    72 to 76 percent undeveloped dry land. The measure is "share of dry land with no structure, field, plaza or road
    within 3 tiles", so tracks have a cost (7 of 48 maps fell below the 65 percent target). (run 38; Terrain log)

8.4 **AoE-style fair starts, not fort starts.** Identical small start area on a ring: clearing, two groves (21 tiles each),
    salvage and stone patches, berries and game, ground levelled within 14 tiles, no structure within 11, 9x9 clearing;
    neutral resource clumps between neighbours as rotations of one found clump; the landmark placed where every start is
    about as far; fair roads (fords and ramps) where a river or ridge favours one player; players 2 to 8 on a ring. Then
    tests assert 15 percent bands (25 for 3, 5, 6, 7 players). (run 38; Terrain log 2026-11-14)

8.5 **Fix what the first ring broke by measuring.** First ring: 30 to 40 percent forest deviation because `clearTrees`
    removed the groves and tracks ran through them (groves are now protected occupancy); a start drifting from water came
    within 21 tiles of a neighbour (starts do not drift on land kinds; the ground is made alike); the first landmark
    search stood 6 tiles off the middle (route deviation up to 90 percent). (Terrain log 2026-11-14)

8.6 **Generate per age; never re-skin at draw time.** The ages must differ in layouts, building mix, defences, fields, roads
    and ruins; one optional `era` parameter, one pack per age; the plain output unchanged and its eight hashes pinned
    beside 24 era hashes. Renaming one city's styles (runs 22, 23) gave four ages with one plan. (L125; run 36; Terrain
    log 2026-11-13)

8.7 **A generator-renderer vocabulary contract, tested.** `ERA_STYLES` lists the styles the renderer draws per age (checked
    against `_draw_block`/`_era_style`) and `MODERN_ONLY` what an era map must never contain; a test asserts each style
    is allowed, nothing overlaps, nothing in water, every door on floor. Where the renderer lacks a style, approximate
    (moat as `~` and `H` tiles, vines as a green `field`) and log a renderer request; plaza and garden decor were later
    drawn (run 37). (L126; Terrain log 2026-11-13; runs 36, 37)

8.8 **Fix the contract between generator modules, with hooks and a fallback.** Map generator v2 was written by separate
    authors against `CONTRACT.md` (signatures, tile glyphs, sea level, cliff step, structure dict, known styles, who
    calls `mapgen.reach`); the lead wired it with hooks and kept the old generator as a fallback until the new one
    passed. (L111; run 24; mapgen-CONTRACT.md)

8.9 **Grow the schema additively.** Tidewatch's maps failed Terrain's schema with 185 to 723 errors each; the schema gained
    `kind` as any lower-case word, width and height from 1, optional `floors`, `style`, `scenery`, `district`,
    `decor[]`, `sites[]`, `generator.note`: errors to 0 and all 84 tests still passed. Nothing renamed. (L143; Terrain
    log 2026-11-12)

8.10 **Parity export and `--check`.** `export-for-godot --registry` writes the game's files; `--check` fails when they differ
     from committed; a six-step parity per map type; compare by statistics because the same seed is a different world
     (urban_sprawl seed 10: 131 vs 119 structures); keep the old generator until people have played. (L145; run 35)

8.11 **Reach checks must fail, not return a partial path; run on every map and kind.** Run 16's check reported islands as
     connected; `map_check` grew 5, 6, 8, 9 maps and per-kind checks; archipelago is the one intended exception.
     (L112; runs 13, 15, 16, 21, 23)

8.12 **Repair, do not only generate, any property you guarantee.** Spawn connectivity is enforced after cities and sites (a
     road is laid for any stranded spawn); doors shut in by a neighbour move; spawns on cliffs move to open ground. Scan
     placements: a farm house overlapped a ruined outpost on 3 of 9 maps, found only by an overlap scan over 240 maps.
     (L147, L148; Terrain log 2026-11-12)

8.13 **A walled place is a closed ring plus gaps; test by flood fill.** 8-connected from outside with gates walled up
     (enclosed at least 20 tiles), then open (every gate reachable); at least 40 rings over the seed matrix; at most 8
     percent of gates not opening the ring. (L127; Terrain log carry-forward)

8.14 **Great places first, scatter last; build over the road, then lead it to the gate; dry-run destructive steps.** Twelve
     early outposts blocked every castle site; a town half built (roads uprooted) then failed its gates, so `fortify({dry:
     true})` now runs first; lay the square and church before the lanes. A ward of 12 cannot hold a gatehouse between two
     towers: 13 or 17. (L128 to L131; Terrain log 2026-11-13)

8.15 **Spawn spacing by farthest-point sampling; spawn order after the water is final.** Random spawns gave gaps of 16, 12, 8;
     farthest-point gave 19 to 28 at 96; sea maps put starts on the largest sea; roads pay 600 to cross water; narrow
     water costs 8 so bridges exist. (L113, L136, L151; runs 16, 17, 24)

8.16 **Relief is per kind and per size, and a layout needs level ground.** Continents and archipelago have little land to lift
     at 96 (stddev 5 to 12 against 14 to 26 at 192); city flattening dropped urban relief from 21 to 11.7; raise hills,
     use per-kind per-size bands. (L133, L150; Terrain log 2026-11-12)

8.17 **Search seeds, and pin the winners.** Urban seed 10 and archipelago seed 3 forced searches; probe several offsets
     in a test (a fixed probe tile held a building). Pin hashes: eight modern and 24 era, later re-pinned on purpose with
     the generator version (0.3.0, 0.4.0, 0.5.0). (L115; runs 21, 24; Terrain log)

8.18 **Per-spawn fairness is a measurement.** Concentric castles landed at the first two spawns only; report win rate per
     spawn on every era map. The log has no such match balance run for era maps. (L135; run 36)

8.19 **When the owner names a tool you cannot find, write a format-compatible stand-in, say so and ask.** Run 13's
     `tools/mapgen/mapgen.py` wrote `shadw.terrain.tactical-map` v1 so the real generator could replace it; the real one
     arrived in run 35. (L116; runs 13, 35)

8.20 **Hash-addressed generation: every decoded value must be on the control's step.** A 0.05 slider step snapped 0.82 to 0.8
     and changed the content hash; steps were set to 0.01 and 200 phrases tested. (Terrain log 2026-10-31)

## 9. Stack integration

9.1 **Stage a generator port: core, relief, cities, eras.** Phase 1 noise, roads, reach, spawn pickers, eight height fields
    behind a `CityHooks` seam (84 tests unchanged, hashes did not move); phase 2 the 1,875-line `cities.py` (0.2.0); phase
    3 era packs (0.3.0). Each phase gated by the game's own `map_check.gd` on a temporary copy of the exported maps.
    (L142; run 35)

9.2 **Suite lock files: tolerate with `report` first, then drive to zero deviations.** `world.lock.json` v2 records each
    world's file hash, content hash and deviation causes and counts; `world --check` fails if either changes. Run 35
    locked eight maps with 336 to 723 recorded deviations ("not a pass"); after the schema grew, 41 worlds lock and
    only the Python maps keep `report`. A recorded and checked tolerance cannot drift. (L144; runs 35, 36; SHADW.md)

9.3 **A worlds list and file import let the game load any map file.** `shadw.game.json` root file (17 worlds, then 41),
    `maps.json` `eras: {age: file}`, `_map_file` picks the age's file; `--mapfile` loads any map (demo gallery worlds).
    (runs 35, 36; SHADW.md)

9.4 **Run the suite's tests under Forge with expectations.** `ai-match` (summary `replay` true, `matches` 2), `map-check`,
    `tactics-check`, `stance-check`: 4 of 4 passed, 188 s for two matches; staged with `"stage": ["game"]`; Forge's local
    runner is not a security boundary. (SHADW.md; run 35)

9.5 **A port inherits the original's bugs; scan the placements.** (see 8.12.) Also keep the old generator until the 20-match
    batch, play on every map by people and a balance run per map have been done. (L148; SHADW.md "Not done")

9.6 **Server features need screens.** The campaign for several people had a relay store but no lobby screen; the faction
    field was never seen; log "built, not seen". Without Redis the relay is a single-process toy. (L118, L119; run 19)

9.7 **Never claim the backup or sibling repo was synced if the tool refused.** Run 35: dada-changes not synced, branch
    deletion refused. (run 35)

## 10. Tooling

10.1 **Screenshots: headless Godot under `xvfb-run`, absolute output paths.** The headless window is 64x64 until the root is
     resized after the first frame (`check_play` depends on it); real-input round trips need a 12 milli-tile tolerance.
     (L120, L121; runs 1, 12)

10.2 **Build staged scenario flags early.** Run 3's panel judged mid-game frames because rendering did not reach tick
     8000; the flags (`--siege`, `--battle`, `--parade`, `--spot`, `--intel`, `--gallery`) were built over runs 20 to 36.
     (L120; runs 3, 20 to 36)

10.3 **Background tasks and polling rules.** Run 12's 6-match balance run "stalled at 4 matches while other jobs ran".
     Check a report's timestamp and match count before quoting it; poll a long task with a time limit rather than a bare
     sleep; expect a background task to be killed at its time-out (a 60:00 match is 2.4 to 5 minutes wall-clock). The
     runs record the stalls; the polling advice is practice. (L122; runs 12, 13, 16, 17)

10.4 **A stale log is not a result.** A balance report that did not finish, or one made before a rule change, describes the
     old game. Regenerate or label it. (L122; runs 7, 12, 14)

10.5 **Rate limits and resumed agents (practice, untested in the log).** When a sub-agent hits a rate limit, resume it with
     its own brief and the validator output rather than restarting the roster; keep authors' files separate so a
     half-finished author does not block the lead's build.

10.6 **Merge conflicts when origin moved: replay your commits onto `origin/main` (practice).** `git fetch -q origin main`,
     then rebase or cherry-pick your commits onto it and re-run the validator; never force-push. Check the branch you
     are on before pushing `HEAD:main`.

10.7 **Re-run the whole test sweep after renderer and sim changes, and say when you did not.** Runs 25 and 33 re-ran only
     the nearest tests; run 34 named the two unconfirmed. Keep one command that runs all 20+ headless scripts and prints a
     pass line each. (L123; runs 25, 33, 34)

10.8 **Know your harness's quirks and keep them in the carry-forward ledger.** Spawn pairs, unit conversions, the 64x64
     window, probe tiles; the real-input round trip is checked at four projection angles. (L121; runs 1, 8, 12)

## 11. Credit and push rules

11.1 **Commits credit only the owner's account.** In these repositories every commit is authored and committed as
     `SolutionsAsService <152567394+SolutionsAsService@users.noreply.github.com>` with no `Co-Authored-By`, no
     `Claude-Session`, no "Generated with" line and no other tool credit, in commits, pull requests, issues, release
     notes or files. This overrides default attribution a tool would add. (CLAUDE.md owner rule 2026-11-12; run 35)

11.2 **Check the history before you claim it is clean.** Run 35: Tidewatch's main history already carried
     `Co-Authored-By`/`Claude-Session` trailers and six remote feature branches still did; rewriting was the owner's call.
     gdada's CLAUDE.md records its own history as rewritten to the rule on 2026-11-12. (run 35)

11.3 **Push to main, fetch first, never force.** `git fetch -q origin main && git merge --ff-only origin/main`, then
     `git push origin HEAD:main`; if origin moved, replay your commits onto `origin/main` (10.6). Delete branches whose
     content is on main when the repo's rules say so. (CLAUDE.md; run 35)

11.4 **Two copies stay in step.** dada keeps the gdada skills in step with gdada (copy, plus discovery symlinks under
     `.agents/skills/`); the validator `python3 scripts/validate_skills.py` runs before every commit and a commit is made
     only when it passes. (dada CLAUDE.md; runs 35, 36)

## Where each lesson lives

L65 to L124 are the "Games" lessons of dada-lessons; L125 to L141 the world generation and rendering by age; L142 to
L152 the stack. The skills (`gdada-art-subagents`, `gdada-sprite-quality`, `gdada-pixel-style`, `gdada-procgen`) carry the
art and generation rules in short form; this page is the one to read first and cite from, and
[../../gdada-grand-strategy/SKILL.md](../../gdada-grand-strategy/SKILL.md) applies it to large simulation games.
