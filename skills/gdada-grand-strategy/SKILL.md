---
name: gdada-grand-strategy
description: "GDADA playbook for Paradox-style grand strategy and other large simulation games: a seeded world of Voronoi provinces (Lloyd relaxation, adjacency graph, coasts, rivers, climate, resources), province-polygon rendering and picking at scale, a persistent clock with scheduled hour/day/week/month/year updates and staggered AI, data-driven definitions, an economy as a flow simulation with test scenarios, supply as a graph, fronts and battle plans compiled to unit commands, notifications, map modes as cheap re-colourings, save/load as seed plus command log plus snapshot, performance budgets, UI density with critic panels, and a vertical-slice roadmap with measurable exit criteria. Each rule is marked as Tidewatch evidence or untested practice. Use when asked to build or plan a grand strategy, 4X, empire or nation simulation game, or any game with thousands of regions and many AI actors."
---

# GDADA grand strategy and large simulations

Companion to `gdada`. Born from IRONFRONT (a top-down, province-based, Paradox-style game started 2026-11-14) with the
lessons of Tidewatch, a real-time strategy game built over 38 GDADA runs. Tidewatch is not a grand strategy game: it had a
front line, supply graph, battle plans, an economy, a clock and 17 to 41 generated worlds, but one battlefield and two to
eight sides. So every rule below carries one of two tags:

* **[evidence: Tidewatch run N]** a rule the Tidewatch log or dada-lessons shows (L-numbers are dada-lessons lessons);
* **[practice, untested here]** established practice for the genre that no Tidewatch run exercised. Treat it as a
  hypothesis to measure in the first slice, and say so in the log.

Read first: `skills/gdada/references/lessons-tidewatch-distilled.md` (the one-page-per-theme digest), then `gdada-procgen`,
`gdada-art-subagents` and `gdada-pixel-style` as needed. The process rules (owner words verbatim, looked-at versus
measured, honest open items) apply unchanged.

## 1. World generation

1. **Preview first.** Write the preview (provinces shaded by height or owner to a PNG) before the generator; judge a
   contact sheet of many seeds by eye before adding invariants, because a generator can pass every check and still be a
   rubber stamp. [evidence: Tidewatch run 36, Terrain log 2026-11-14; L132]
2. **Voronoi provinces from jittered seed points, relaxed by Lloyd iterations (2 to 4).** Seed points by blue-noise
   (Poisson disc) with density higher near coasts and mountains so borders follow terrain; clip cells to the map; relax
   until area variance is under a target. Store each province as an integer-coordinate polygon. [practice, untested here]
3. **Heights and coasts from processes, not noise alone.** Domain-warped and ridged noise, erosion, a sea level chosen by
   quantile so water share is exact; per-kind and per-size relief bands; a measurable fingerprint per map kind. [evidence:
   Tidewatch runs 24, 36; L150; Terrain log 2026-10-31 exact-rank water]
4. **Adjacency graph is the primary product.** Build it once from shared polygon edges (neighbour, border length, border
   kind: land, river, strait, coast). Everything else (supply, movement, fronts, AI) reads the graph, never the pixels.
   [practice, untested here]
5. **Rivers by flow accumulation from highlands to sea; rivers are edges or border kinds in the graph, and fords and
   bridges are crossings with a cost.** Make narrow water cheap to cross for the road builder or no bridges exist (cost
   8 against 30 or 600). [evidence: Tidewatch runs 13, 24; L136]
6. **Climate and resources as pure functions of the seed.** Latitude and height give temperature, wind and distance to sea
   give rainfall, biome by lookup; deposits by noise thresholds with guaranteed minimums per region. [practice, untested
   here]
7. **Reach and fairness are validated, not hoped for.** Every start reaches every other by the consumer's rule; reach
   checks fail rather than return partial paths; per-start resource and route spread is measured (AoE-style bands: 15
   percent for 2, 4 and 8 starts). [evidence: Tidewatch runs 16, 38; L112, L146; Terrain log 2026-11-14]
8. **Repair what you guarantee.** Enforce connectivity and minimum deposits after the last generator stage, so a later stage
   cannot break them silently. [evidence: L147; Terrain log 2026-11-12]
9. **Grade a gallery of seeds before the schema invariants grow;** include a variety measure (distinct province shapes,
   coast complexity, nation start fairness). [evidence: Terrain log 2026-11-14 rubber stamp]
10. **Low-key beats dense.** A few big features and mostly undeveloped land read as a world; 120 to 300 structures per small
    map read as a stamp. Make density a measured stat. [evidence: Tidewatch run 38]
11. **Per-era generation, not re-skin** if the game spans ages: layouts, building mix and routes differ per age; the plain
    output keeps its pinned hashes. [evidence: Tidewatch run 36; L125]
12. **A generator-renderer vocabulary contract** (the styles, glyphs and kinds the renderer draws), tested in the build,
    plus a schema grown additively with a parity `--check`. [evidence: L126, L143, L145]

## 2. Rendering and selecting provinces at scale

1. **The simulation owns provinces; the renderer owns polygons.** Nothing visual enters the state hash. [evidence:
   Tidewatch run 1; L91]
2. **Cache layers as textures.** Draw the base map (terrain, borders, rivers) once to a texture per zoom band; draw owner
   tint, fog and selection as thin layers on top. Cached structures cut drawing from 37 to 56 ms a frame to 1 to 3 ms with
   176 structures; benchmark with a flag (`--bench N`). [evidence: Tidewatch run 36; L139]
3. **Picking by a spatial index.** A uniform grid or quadtree over province bounding boxes, then point-in-polygon on the
   few candidates; or an ID map (one colour per province rendered off-screen, read one pixel). [practice, untested here]
4. **Chunk the map** into tiles of fixed world size; rebuild only chunks whose provinces changed owner or state; load
   and unload by camera rectangle. [practice, untested here]
5. **Level of detail by zoom.** Far: province fill and nation borders only, no labels except nations; mid: provinces, rivers,
   capital icons, army counters; near: terrain texture, buildings, unit figures. Counters replace figures below a zoom
   threshold, with a hover tooltip. [evidence: Tidewatch run 4 (counters below zoom 1.3), run 5 (hover text); the rest
   practice]
6. **Border lines drawn once per shared edge,** with owner colour on both sides offset in, not one line per province.
   [practice, untested here]
7. **Pixel-snap vertices and give every big shape a dark outline** of its own colour so provinces and nations do not fade
   into the background; keep terrain quieter than the overlays. [evidence: Tidewatch runs 32, 37; L138]
8. **Labels need their own pass.** Curve names along the province's long axis, hide below a size, avoid overlap by
   priority. [practice, untested here]

## 3. The persistent clock

1. **A fixed tick, integers, a command log, a state hash.** The simulation steps in whole ticks; time is an integer count
   (one tick = one hour); speed 1x to 16x changes how many ticks per frame, never the tick length. [evidence: Tidewatch
   run 1, L89]
2. **Scheduled updates: hour, day, week, month, year.** Each system registers a period and an offset; the clock fires
   `on_hour`, `on_day`, `on_week`, `on_month`, `on_year` from the tick count. Heavy work (economy settlement, AI
   planning, history) belongs to month and year, movement and combat to hour and day. [practice, untested here]
3. **Stagger AI and per-nation work with a due-helper, never raw ticks.** A gate like `(tick + 7*pid) % 30 == 0` never fires
   for some players; use `_due(period, offset)` and test it for every nation index, including the last. [evidence:
   Tidewatch run 19; L95]
4. **Spread nations across the period.** With 200 nations on a monthly cycle, nation `i` plans on day `(i * 7) mod 30`; no
   frame does all the planning. [practice, untested here]
5. **Pause is not a mode of the clock, it is a speed of zero;** commands issued while paused are applied on the next step,
   so tests step before asserting. [evidence: Tidewatch run 7 (town_check) for the step-first rule; the rest practice]
6. **Ticks per second are a budget** (section 11), and the clock must survive a slow frame by capping ticks per frame
   rather than skipping them. [practice, untested here]
7. **Time-driven effects are bounded by what they encode:** a season may change when something happens, not how much exists.
   [evidence: Tidewatch run 1 (tide), L152]

## 4. Data-driven definitions

1. **Nations, goods, buildings, technologies, governments, unit kinds are data files** (JSON) read at start; the engine has
   no hard-coded nation or good. Rules have ids; effects are named, with prerequisites. [evidence: Tidewatch runs 22
   (`rules.json` per era, tech effects as data) and 5 (stats on the site computed from `rules.json`)]
2. **A consistency test over the data:** every unit has a producer, bonus tables name real units, tech prerequisites are
   valid, every good has a source and a sink, two AIs play five minutes without error. [evidence: Tidewatch run 22
   (`era_check`)]
3. **The same kind ids carry every era,** with era-specific additions, so a save and an AI work across ages. [evidence:
   Tidewatch run 22]
4. **Scenarios are data too:** start year, nations, ownership and tuning in a file with a hash, so a result names its
   scenario. [practice, untested here]
5. **Never hard-code a nation.** Names, colours and flags come from generated identity data; the first test builds a world
   with a name nobody wrote. [practice; Tidewatch run 24 named era factions as data]

## 5. Economy as a flow simulation

1. **Model stockpiles, production, consumption, transport and prices per province or market;** a good moves along the
   graph, each step losing time and cost. [practice, untested here; Tidewatch had stockpiles, income and supply but no
   prices]
2. **Do the income arithmetic before any AI run.** Uranium burned faster than a mine paid, manpower piled up to 1,330, a
   heavy tank was 24 s of one mine: all found by arithmetic or bots. Write a table: per-good production per month,
   per-unit cost, break-even. [evidence: Tidewatch runs 1, 5, 7, 14; L105]
3. **Shortages must bite and be visible.** The economy exists when a missing good stops production or lowers readiness,
   and a notice names the missing resource and the building that would fix it. [evidence: Tidewatch run 5 (`can_train`
   names the missing resource), run 1 (timber starvation)]
4. **Holding a source costs attention:** a mine pays by garrison (25 percent with none to 100 percent with three),
   nothing while an enemy stands beside it, half for 60 s after a capture; show the rate under the source. [evidence:
   Tidewatch run 5]
5. **Flat income removes the boomer.** In a flat-income economy the economic personality has no lever and early aggression
   wins. Give growth a lever (investment, development levels, trade). [evidence: Tidewatch run 5; run 6 development
   levels]
6. **Economy test scenarios:** staged small worlds with a known answer (two provinces, one mine, one factory, one road):
   assert production, price, shortage and recovery in numbers; run each as a headless check. [evidence: Tidewatch
   `economy_check`, `town_check`; the flow scenarios themselves practice]
7. **Prices as feedback:** price moves toward a ratio of demand to supply with a damping factor and a cap; assert it does
   not oscillate over 24 months. [practice, untested here]
8. **Bots find economy bugs a description cannot.** Run AI-vs-AI over the economy and report income per nation. [evidence:
   Tidewatch run 1; L105]
9. **Every cap needs a reason and an ending.** Unbounded growth (waves, stocks) ended matches at the cap; bound it and add
   an exit. [evidence: Tidewatch runs 1, 7]

## 6. Supply and logistics as a graph

1. **Supply is a graph:** depots (hubs), ports linked by sea, capital and held sources are nodes; edges are cut where an
   enemy holds ground across them; units outside supply fight at half effect and wear down to a floor. [evidence:
   Tidewatch run 6 (`sim/supply.gd`, 22 checks)]
2. **Attrition in whole numbers and with a floor** (22 permille per 2 s down to 20 percent), so a cut line hurts but does
   not delete the army instantly. [evidence: Tidewatch run 6]
3. **Plans are supply-aware:** show arrows in a warning colour beyond supply, warn on commit, advance in steps limited by
   supply. [evidence: Tidewatch runs 6, 11]
4. **A cut must be visible and fixable:** a ring for out-of-supply units, a toggle for supply radii, development levels
   that extend radius (+4, +8). [evidence: Tidewatch runs 5, 6]
5. **Ports and sea lanes are graph edges with their own capacity;** naval layers use their own grid with clearance.
   [evidence: Tidewatch runs 15, 16]
6. **At province scale, compute supply with a graph search from sources** (Dijkstra with edge cost = distance over road
   quality), refreshed monthly or on a cut event, not per tick. [practice, untested here]
7. **The AI must use the logistics it faces;** a rule the AI never uses is untested play. Count its commands. [evidence:
   Tidewatch run 6 (`rules.ai` hubs/ports); L101]

## 7. Fronts and battle plans as orders compiled to commands

1. **A front is derived, not authored.** Influence from provinces and troops gives control per province; the front is where
   control changes owner. Make it a rule (supply, attrition, ground victory) or say it is information only. [evidence:
   Tidewatch runs 4, 5, 18 (N-sided fronts)]
2. **Battle plans are orders:** an operational plan (offensive arrows, defence lines, hold or push per sector) compiles into
   ordinary unit commands, so replay, AI and tests share one interface. A plan has up to 8 waypoints, concurrent groups,
   numbered arrows, a Cancel button and notices on completion or failure. [evidence: Tidewatch runs 5, 9, 11]
3. **The AI issues plans through the same command.** Waves, hold lines and pushes are plan commands in the log. [evidence:
   Tidewatch runs 5, 9, 26, 34]
4. **A plan has phases the player can read:** gather at the nearest supply node, advance in supply-limited steps, assault,
   hold, fall back after losing about half, at most two retreats. [evidence: Tidewatch run 11]
5. **Assault gates need intel and combined arms.** No attack on an unseen or fortified position without a report, engineers
   or guns and escorts; a blind attack feeds the enemy. [evidence: Tidewatch run 20; L99]
6. **An ending for stalled fronts.** Add attrition, escalation or a growing pressure with the rule that lengthens the war.
   Tidewatch's medieval AI still stalls at 60:00 (open problem 4.11 in the digest): do not assume a grand-strategy AI will
   break a fortified front by itself. [evidence: Tidewatch runs 7 to 17, 36 to 38]
7. **Operational combat at province scale** (formations on provinces, combat width, terrain and river modifiers,
   reinforcement, retreat) is not built in Tidewatch; prototype it on the staged scenarios first. [practice, untested here]

## 8. Notifications and event design

1. **Every signal reaches the player in text with a map marker:** capture and loss, plan complete or lost, shortage,
   threshold reached, ground victory countdown. Silent or generic events were the largest UI finding. [evidence:
   Tidewatch run 5]
2. **First notice tells the player what to do;** a heavy-fighting notice, a warning before a clock event (the tide, 20 s).
   [evidence: Tidewatch runs 1, 25]
3. **Events are data with triggers and options,** fired from the month and year updates, with the AI choosing by the same
   weights as the player sees. [practice, untested here]
4. **Rank and collapse:** a priority, a stack by kind, a cap on visible toasts, a log you can reopen. Never use history as a
   script; events respond to simulation state. [practice, untested here]
5. **Every notice is a log line in the command or event stream,** so tests can count them. [practice; evidence: Tidewatch
   counted commands per type]

## 9. Map modes

1. **A map mode is a re-colouring of cached layers:** political, terrain, supply, economy (per resource), control, fog,
   diplomacy. One function per mode maps province id to a colour; the base texture stays. [practice, untested here]
2. **Recolour by palette index or shader,** not by redrawing polygons: store the province id map, look up the colour
   texture, update only changed provinces. [practice, untested here]
3. **A toggle per overlay with a hotkey from the key table;** check new keys against the whole map. [evidence: Tidewatch
   run 9, L110; `V` toggles supply, `F` the front]
4. **An overlay says what it is:** a tooltip with the terms the rule uses. [evidence: Tidewatch run 5 (Ground bar)]
5. **Colour is never the only channel:** hatching, hollow versus filled symbols and outlines carry the side. [evidence:
   Tidewatch runs 1, 4, 5; L88]

## 10. Save and load

1. **Save = seed + command log + optional snapshot.** Replaying the log from the seed reproduces the state hash; a snapshot
   is a cache of that replay, not the truth. [evidence: Tidewatch run 1 (replay), run 19 (campaign saved as JSON, a file
   for one person, the relay for several); snapshot practice]
2. **Hash every new piece of state.** Re-read the hash function in every run that adds state. [practice from L91; no
   incident logged]
3. **Version the rules and the generator in the save** (generator 0.3.0, 0.4.0, 0.5.0 re-pinned its hashes on purpose);
   a save names its data version, and old saves are replayed with the old data or refused. [evidence: Terrain log
   2026-11-13/14]
4. **Verify desync with a periodic hash;** every 20 turns in lockstep. [evidence: Tidewatch run 18; L117]
5. **Numbers are integers;** JSON floats convert back; engine trig is banned in generation. [evidence: L92, L149]
6. **Test save and load in CI:** run N ticks, save, reload, run M, compare to a straight run of N+M. [practice, untested
   here; replay hash is the Tidewatch analogue]

## 11. Performance budgets

1. **Measure before promising.** Tidewatch: 3000 AI ticks in 2.0 s (96 tiles), 2.4 s (160), 4.1 s (192); a 60:00 match is
   2.4 to 5 minutes of wall-clock. [evidence: Tidewatch runs 11, 16, 17; L94]
2. **Targets to set and measure in slice 1 (practice, untested here):** 3000 to 6000 provinces; 100 to 300 nations; the
   simulation under 4 ms a tick at 16x on the target machine; AI planning under 2 ms a frame averaged; map frame under
   16 ms at full zoom-out; peak memory under 1 GB.
3. **Cache per-unit-per-tile work** (line of sight, paths); invalidate on change events, not per tick. [evidence:
   Tidewatch run 12]
4. **Stagger, do not batch:** per-nation work spread over the period. See 3.4.
5. **Asset size grows silently;** split per era or region before it hurts. 35 MB of sprites loaded whole was never
   measured. [evidence: Tidewatch runs 10, 22, 24, 27; L87]
6. **Stage a fast headless scenario** and report ticks per wall-second in the log; a long game makes every balance run
   slow. [evidence: Tidewatch runs 11 to 17]
7. **Never size arrays for two nations;** test with the largest count. [evidence: Tidewatch run 18; L93]

## 12. UI information density

1. **Dense is fine if it is ordered:** top bar (date, speed, treasury, manpower), left panel (selected province or
   formation), notifications at the side, mini-map, mode buttons. Hotkeys on the buttons, a disabled button says why in
   its tooltip, an F1 help panel. [evidence: Tidewatch runs 1, 5; practice for the Paradox-style layout]
2. **Quiet by default:** hairline health bars shown when hurt or selected, counters not figures when far, a `--clean` mode
   that hides overlays for screenshots. [evidence: Tidewatch runs 25, 32; L84]
3. **Fixed minimum sizes:** 44 px targets, 11 px text floor, outlined numbers, a plate behind pale text. [evidence:
   Tidewatch runs 1, 5]
4. **Critic panels for UI screenshots.** One seat per reference (Norman for signifiers and discoverability, accessibility,
   Swink for feel, Meier for decisions), each grading a rendered screenshot to a file; independent seats, not the author.
   Track their grades: Tidewatch's UI seats gave C+ to B- over two rounds. [evidence: Tidewatch runs 2 to 5; L70]
5. **Test every UI claim through real input events** (`check_play`: a built barracks and trained spearman through real
   input, 19 checks). [evidence: Tidewatch run 1 M5; run 5]
6. **Stage the screenshot:** software rendering cannot reach late game; build flags for scenes (`--battle`, `--spot`,
   `--gallery`, `--intel`). [evidence: Tidewatch runs 3, 20 to 33; L120]
7. **Look at the picture as well as the numbers,** at 1x, in game zoom; say which were only looked at. [evidence: L79,
   L67]

## 13. AI at scale

1. **Hundreds of nations need think-tick gating, intel memory with ages, and the player's command interface.** [evidence:
   Tidewatch runs 4, 8, 19 (intel), L95, L100]
2. **Personalities are weightings** (expand, trade, militarise, turtle), reported per personality and per start. [evidence:
   Tidewatch runs 1, 24]
3. **Prove a behaviour fires** by counting commands per type in AI-vs-AI runs, with a floor (20 commands a match). [evidence:
   L101]
4. **Passivity and stalls are the commonest AI failure.** Print what idle units do before changing numbers. [evidence:
   L96, run 18; open problem in the digest]
5. **Do not script history.** The chronicle is generated from simulation events (wars, treaties, famines) for the
   player, never an authored timeline. [practice, untested here]

## 14. Vertical-slice roadmap with measurable exit criteria

Build in slices; each ends with measured criteria, screenshots, a Not-done list and a pushed commit. [evidence: Tidewatch
log structure; L67, L72] Suggested slices (the numbers are targets to revise after the first measurement):

| Slice | Content | Exit criteria (measured) |
|---|---|---|
| 0 Clock and state | Fixed tick, command log, hash, data files, headless runner | Replay hash identical across 3 seeds; 1 year simulated in under 1 s |
| 1 World | Provinces, adjacency, coasts, rivers, climate, resources, gallery | 16 seeds graded by eye; adjacency graph connected; per-start deviation within 15 percent; variety measure reported |
| 2 Map | Polygon renderer, picking, LOD, three map modes | Pick 1000 random points correct; frame under 16 ms at full zoom-out; screenshots at three zooms |
| 3 Nations and economy | Generated nations, stockpiles, flow economy, shortage notices | Economy scenarios pass; bots report income per nation; no nation starves unintentionally |
| 4 Military | Formations, supply graph, fronts, battle plans | Supply check passes; a plan compiles to commands; a front exists and moves |
| 5 AI | Staggered planning, intel, personalities | Every nation index gets its turns; commands per type counted; match ends by an exit or the stall is logged |
| 6 UI | Panels, notifications, modes, help | Real-input play test; critic panel grades B or better |
| 7 Save and polish | Snapshot, versioning, performance | Save and reload equals straight run; budgets met |

## Anti-patterns

* **Scripted history:** timelines authored in advance. Events respond to state. [practice, untested here]
* **Per-frame AI:** every nation thinks every frame. Stagger by due-helper and period. [evidence: Tidewatch run 19; L95]
* **Simulation in the renderer:** state in nodes, floats, or visuals in the hash. [evidence: Tidewatch run 1 (M1), L91]
* **Hard-coded nations, goods or maps.** Data files and seeds only. [evidence: Tidewatch run 22; practice]
* **Tuning before looking:** changing numbers before finding what the idle units do. [evidence: L96]
* **Claiming the slice:** a green test that printed no pass line, or a vacuous one. [evidence: Tidewatch runs 6, 7, 25, 34]
* **Invariants without a gallery:** a rubber stamp world. [evidence: Terrain log 2026-11-14]
* **Dense by default:** too many castles, too many overlays. [evidence: Tidewatch runs 25, 38]

## Credit and pushing

Commits are authored and committed as the owner's account with no AI credit (see `gdada` and each repository's
CLAUDE.md). Fetch before pushing, replay onto `origin/main` if origin moved, never force.
