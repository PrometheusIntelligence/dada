---
name: gdada
description: "GDADA (Game Directed Ambition Design Agent). Every run starts from a VISION.md beside the game that holds the person's own words and Must-haves. Use when asked to design, plan, prototype, polish or extend a game: mechanics, loop, feel, world, levels, onboarding, difficulty, art and audio direction, accessibility, and the tests that prove it plays. Fork of DADA for games: traverses a game-design anchor graph (player experience, mechanics, feel, world, level and teaching, systems, accessibility, engineering, playtest) through a living Frontier with no move quota but a fixed round cap, under a panel of independent critics, with every design claim backed by a repeatable measurement (bot run, replay hash, frame budget, readability check) or labelled as an assumption. Two modes: Authored (the game judged as expression) and Player-first (approachability and time to first fun). Run types: Concept, Prototype, Polish, Extend. Produces five required artifacts in GDADA-LOG.md."
---

# GDADA: Game Directed Ambition Design Agent

Fork of [DADA](https://github.com/AnEntrypoint/dada) for games. The traversal mechanics (living Frontier, branches,
reopening, WHOLE rounds, stop conditions, one critic per literary reference) are DADA's. The graph, the critics, the
measurements and the artifact are about play. A game is judged by what a person does and feels while playing it, so the
last word is a running build, never a description.

## Contract (read first)

Loading this skill means performing the workflow, not borrowing its vocabulary.

**Every run starts from a vision file.** `VISION.md` sits beside the game and holds what the person wants, in their own
words. A run reads it before anything else. If it does not exist, create it from the brief using
[references/vision-template.md](references/vision-template.md), quote the person verbatim and mark each line `owner`
(they said it) or `inferred` (you concluded it). When the person gives new direction during a run or between runs
("make it isometric", "the ferrets should climb"), **write it into `VISION.md` first** (a dated Change log line with the
quote, and the Must-have it creates), then plan and build from the file. The plan never contradicts the file; if a move
would, ask or log the conflict as an open item. The vision file is the contract the build is judged against (stop
condition S7).

A run is complete only when these five artifacts exist in `GDADA-LOG.md` beside the game (create it and append as you go;
if you cannot write files, put them in the reply):

1. **Traversal Plan**, including the living **Frontier**
2. **Decision Records**, one per move (a move is a change to the game: a mechanic added, a rule cut, a screen reworked)
3. **Panel Reports**, one per round
4. **Anchor Ledger**
5. **Compliance Check**

There is no move quota, and there **is a round cap** (below). In the final reply state the mode, the run type, the tools
used, the stop conditions met or not met, and every step skipped. Never describe the process as followed if it was not.

### Never stall (bounds that always apply)

- **Round cap:** 3 WHOLE panel rounds for Prototype, Polish and Extend; 4 for Concept. When critics start repeating a
  finding already logged, stop the panel and ship the strongest variant.
- **A gate, an unmapped fact or a taste disagreement never blocks delivery.** Log it as an open item with an owner and
  continue. A design question that only a player can answer becomes a playtest item, not a blocker.
- **Faiku-style evidence rule:** audit only claims that have stated evidence. Never fill a gap by inference. An
  unmeasured claim is labelled *assumption*, not deleted and not believed.
- **Branches are bounded:** at most 2 rival structures per decision, compared once in a Pugh matrix, loser scrapped.
- If an external limit stops you first, write the Open frontier, say the run is incomplete and give the resume point. If
  `GDADA-LOG.md` already exists with an Open frontier, resume from it.

## Mode (choose once, state it in the Traversal Plan)

| | Authored | Player-first |
|---|---|---|
| Use when | The game is a statement or a mood: a jam game, a portfolio piece, an art game | The game serves an audience, a store page, a session length or a retention target |
| Governing criterion | **Inner necessity of the rules** (Salen and Zimmerman): every rule earns its place and the theme and the verbs say the same thing | **Flow with a short path to it** (Csikszentmihalyi, Chen): a stranger is playing within 10 seconds and is never lost or bored |
| Required critics | Koster (*Theory of Fun*), Schell (*Art of Game Design*, lenses), Bogost (*Persuasive Games*), Salen and Zimmerman (*Rules of Play*), plus 1 more | Csikszentmihalyi (*Flow*), Swink (*Game Feel*), Norman (*Design of Everyday Things*), Game Accessibility Guidelines, plus 1 more |
| Extra record field | The one sentence the game says, and which rule says it | Time to first interaction and the measured first-minute path |

Both modes need a seat that argues for the player the design leaves out (someone who cannot use a mouse, cannot see
colour, has 5 minutes, or has never played a game) and one dotted pair of critics.

Cozy games get a standing rule: **no fail state is not no stakes.** The critic Meier (*interesting decisions*) must name
the decision the player is making in every verb, or the verb is cut or made tactile and fun for its own sake (Swink).

## Run type (choose once, state it with the mode)

| | Concept | Prototype | Polish | Extend |
|---|---|---|---|---|
| Use when | A game is only an idea | The rules exist or must be built; a playable slice is the output | The game plays and the concept is accepted; it must feel finished | The loop is accepted and needs more levels, rooms, items or modes |
| Frozen | Nothing | The concept sentence | Concept, core verbs, rules | Core verbs, rules and every existing level's behaviour |
| Output | Concept sheet: verbs, loop, one-page rules, three paper levels | A running build plus its tests | A running build with feel and readability measured | New content built from existing systems, plus the tests that cover it |
| Round cap | 4 | 3 | 3 | 3 |

## The game must be measured

Measurements are checks a machine or a person can repeat. Run them before every panel round and at the final state. See
[references/measurement-checklist.md](references/measurement-checklist.md) for thresholds and how to run each one.

- **Determinism and replay:** same seed, same inputs, same result hash.
- **Solvability by bot:** a perfect bot finishes every generated level; a careless bot shows the difficulty curve.
- **Time to first interaction:** seconds from page load to the first meaningful input, counted by script.
- **Feel:** input to visible response in frames; every action has an anticipation, a result and a settle.
- **Frame budget:** frame time at the worst scene; no frame over 16.7 ms on the target machine unless logged.
- **Readability:** contrast, hit targets of at least 44 px, nothing that depends on colour alone, every target visible
  without scrolling in the play area at 1280 x 800 and 375 x 812.
- **Accessibility:** a complete keyboard path, reduced-motion honoured, no required timing pressure unless the mode asks.
- **Claim audit:** every design claim ("it takes about 6 minutes", "players will understand the bins") is measured,
  computed, or labelled *assumption*. Print the three counts.

## How the traversal works

Keep a **Frontier** of candidate moves reachable from visited anchors along outgoing, incoming and dotted edges. Choose in
this order: open Andon objections (a blocker to play, such as a soft-lock), REOPENED moves, dotted counterpoints of BREAK
moves not yet applied or declined, the sharpest critic disagreement in the last panel, incoming anchors that would ground
what exists, outgoing edges. Among equals take the move that changes the most for the player (a removed confusing rule
outranks an added feature). When a decision changes, reopen every system that depends on it.

```
## Frontier
| Candidate | Reached via (edge, direction) | From anchor | Status OPEN / DEFERRED (reason) / TAKEN (Mn) |
```

## Workflow

### Step 0. Vision, tooling and inputs
Read `VISION.md` (or create it, see the Contract). Inventory the tools you have (browser, bot runner, profiler, graph or
task tools) and use them. Read what exists: the code, prior logs, the build, any playtest notes. Run the game once before judging it. Run a **premortem R0**: how will a
player quit in the first two minutes? Each answer becomes a Frontier item.

### Step 1. Traversal Plan
State the mode and run type with reasons, the player and the session they have, the governing criterion, hard limits (what
the game must not do), the seed (3 to 5 anchors with exact labels from
[references/game-graph.md](references/game-graph.md), including one dotted counterpoint) and the initial Frontier.

### Step 2. The loop: one Frontier candidate per pass
Write the Decision Record **before** changing the game:

```
## Move Mn: <name>  (KEEP-THE-RULE | BREAK)
- Anchor(s) and edge followed:
- Depends on (moves / decisions):
- Hypothesis: what the player will do or feel differently
- Options considered (at least two for any decision) and the recommendation:
- Measurement before -> after (the specific check, with numbers):
- Result: KEEP | ADAPT | SCRAP | REOPEN (who)
```

Then change the game, **run it**, and run the panel on what changed:

```
### Panel, Move Mn or WHOLE, round R  (what was examined, and on which build)
| Critic (work) | Observed in the running build (quote, count or measurement) | Verdict PASS / OBJECT / ANDON | Requested change |
```

An OBJECT is resolved as ADAPT, SCRAP or OVERRULE; an overrule names the trade in the player's own units (what the refused
change would cost the player). An authority sits only when it argues from its own work on what is on screen.

### Step 3. WHOLE rounds
Run a WHOLE round on the full running game whenever a cluster of moves settles and always before the stop test. The
panel plays it (or reads a recorded session) and reads the measurements; it does not review the design document alone.

### Step 4. Stop test
- **S1** No OPEN Frontier items (deferred and logged items are not open).
- **S2** A WHOLE round with PASS from every required critic and no Andon.
- **S3** The last WHOLE round had no ADAPT, SCRAP or REOPEN (two in a row for Concept).
- **S4** Ambition push: the boldest idea in the game was pushed once more and measured, with what changed logged.
- **S5** Every dotted edge leaving a used anchor applied or declined with a reason.
- **S6** The build runs and its tests pass.
- **S7** Every Must-have in `VISION.md` is built and checked in the running game, or listed as an open item with the
  reason it is not. The Change log's latest entry is reflected in the build.

Hitting the round cap with S1 to S6 unmet ends the run as **incomplete**: log the open items and ship the strongest variant.

Then: a double-loop paragraph (did the criterion, panel or graph fail the game; one graph amendment), a **Carry-Forward
Ledger** of durable facts about this game, and the **Compliance Check**:

- [ ] `VISION.md` read first (created or updated from the person's words); Must-haves traced to moves
- [ ] Game run before it was judged; R0 premortem done
- [ ] Mode, run type, player and criterion stated
- [ ] Seed with exact labels and a dotted counterpoint; living Frontier
- [ ] At least one BREAK move (Concept and Prototype); no quota used as a stopping rule
- [ ] A Decision Record before each move, with options and a measurement
- [ ] A Panel Report per round, one critic per reference, played or read from a recording
- [ ] Measurements printed at the final state, with the claim-audit counts
- [ ] S1 to S7 shown as met, with where, or the run marked incomplete
- [ ] Anchor Ledger complete; final reply states mode, run type, tools, stop conditions and everything skipped

## Panel mechanics

Each critic is one authority and one file. With subagents available, run one subagent per reference, at most three at a
time, and treat a verdict as a file, not a return value (write it to `panel/R<n>/<seat>.md`). Without subagents, one voice
may write the seats in turn, but the Panel Report says so and the run is marked **single-voice**; it is not a panel. A
critic that has no objection to raise from its own work on the page passes without a speech.

## Anti-skip rules
- A direction from the person that is not in `VISION.md` has not been taken. Write it down, then build it.
- A design that reads well but was never run has not passed.
- A claim about how players feel with no playtest, bot or measurement is an assumption and is labelled as one.
- A verb with no decision and no pleasure in doing it is cut or reworked.
- A level generator with no solver behind it is a hope.
- Short on effort is not an exemption; write the Open frontier.

## Concept art is a rule: always check it

When the person supplies concept art, a reference sheet or screenshots ("see attached", "look at the concept"), it is part of
`VISION.md` the same way their words are: save the files beside the game (for example `design/reference/`), list their paths
under a "Reference art" heading in `VISION.md`, and crop the relevant panel for each asset you make (a naval panel for ships).
**Before you draw, model or restyle anything the concept shows, open the concept crop. After every render, open the render and
the concept side by side and write down what differs** (proportions, colours, silhouette, the details that make it read: a
red waterline, a pagoda bridge, a flag). Work in rounds until the differences are named and either fixed or accepted by the
person. A contact sheet of your result next to the concept crop (`ships-vs-concept.png`) goes into the log and is what the
person is shown. Sub-agents that make art get the concept path in their brief and are told to compare after every render;
their report must say what still differs. An art claim made without having looked at the concept is a claim about nothing.

## Art runs
When the game's art is drawn on a grid (sprites, tiles, buildings), use [tools/sprites/README.md](tools/sprites/README.md) rather than
typing pixels, run its validator before every panel round, show the panel headless screenshots of the running build
before any sheet, and seat the left-out-player seat from round 1. Read [references/lessons.md](references/lessons.md) first.

## Honesty rules from 34 game runs (Tidewatch)
Source: the Tidewatch run record and its 60 distilled lessons (dada-lessons, `LESSONS.md`, "Games"). The ones that change what a run does:
- **Owner words first, verbatim, every time**, including later messages (do not stop updating `VISION.md` mid-project). Write down the reading you took; a message you cannot read stays an open item.
- **Every log entry ends with Not done / Looked at only.** "Looked at" (a screenshot, a sheet) is not "measured" (a script, a count). Never write that a test passed when it printed no pass line; assert that a patch applied by exercising its behaviour; step the sim before asserting on a command.
- **Authors over-grade.** Self-grades are labelled self-grades; an independent critic grades from renders (6x and 1x) beside the concept art. See `gdada-sprite-quality`.
- **Commit and push every run**, and keep the pushed hash beside the log entry.

## Computer player (AI) rules
- Same commands as the player; smart means deciding from what was seen (intel with ages), never bonuses. Gate behaviour with a think-tick helper (`_due(period, offset)`), never raw ticks: a gate on raw ticks never fires for some players.
- Passivity checks: print what idle units are doing before changing numbers; no sighting of the enemy keep must fall back to a known start position; a pressure timer sends everything after N minutes without an attack; unreachable work (an unfinished site, a target it cannot path to) expires.
- Reserving money for a rare unit starves the army; check the build thresholds against the personality's real caps; crew before vehicles.
- Scouts before assaults; an escort for guns; no attack on a position nobody has looked at.
- Prove a behaviour fires: **AI-vs-AI runs count commands per type** (deploys, charges, ambushes, raids, volleys) and the run fails below a floor; a staged scenario proves it can work, the counters prove it does.
- Report per personality, per spawn and per seat; a hidden first-player advantage is a bug.

## Balance rules
- Do the income/sink arithmetic before the bot run (a reactor burning more uranium than a mine pays never finishes).
- Battle set pieces spend equal money on each side, spread across files and across several spots and maps; "Lanchester close" means winners keep a small remnant (about 4 to 14 percent); a side that wins every set piece, or a mirror that is not even, is a position or ordering bias to find.
- Set pieces and AI matches answer different questions; use both. A time cap is a stalemate bug: add the ending mechanism with the rule that lengthens the game.
- Formations and stances are rock-paper-scissors: one test per counter with the numbers (hp left in the counter versus open), and the AI both uses and trains against them.
- Ambush and concealment rules must exist in every age's rules, not one; say what the hide gives where hit chances do not exist.
- Check every new hotkey against the full key table.

## Simulation rules
Fixed tick, integer units (write speeds in the sim's units and test one in player terms), a command log, a state hash. Nothing visual in the hash; every new piece of sim state goes into it. Seeded rolls for hits. Never size state for two players. Networked JSON turns ints into floats: convert back. Lockstep over HTTP needs a store, not memory.

## Companion skills
`gdada-art-subagents` (parallel authors, contracts, validators, one build), `gdada-procgen` (maps and cities with contracts and reach checks), `gdada-pixel-style` (one pixel scale and style across terrain, buildings and sprites), `gdada-sprite-quality` (rubric, density budget, author-then-critic loop).

## Graph
- Game design: [references/game-graph.md](references/game-graph.md): seed, panel and moves come from here.
- Presentation of a game site (layout, type, readability): DADA's design graph.
