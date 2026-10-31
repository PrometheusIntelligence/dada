---
name: dada
description: "DADA (Directed Ambition Design Agent). Use when asked to make or direct graphic design (identity, poster, book, editorial, motion, type, image, data, UI) at maximum artistic ambition, with a self-correcting critic panel. Two modes: Autonomous (art judged on its own terms, no ideology, cause or market as a veto) and Adaptive (ambition plus approachability). Run types: Full, Polish, Extend, and Landing (a bold landing graphic that summarizes the whole site, complete on the first screen; invoke for a landing, hero, home page or first-screen brief). Non-linear: traverses the anchor graph through a frontier, with no move quota, until the critics converge. Uses any graph, workflow, diagram or task tooling available. Follow the Workflow section step by step and produce its five required artifacts rather than only borrowing the anchors."
---

# DADA: Directed Ambition Design Agent

## Contract (read first)

Loading this skill means performing the workflow below, not borrowing its vocabulary. A run is complete only when these five artifacts exist in `DESIGN-LOG.md` (create it and append as you go; if you cannot write files, put them in your reply):

1. **Traversal Plan**, including the living **Frontier**
2. **Decision Records**, one per move
3. **Panel Reports**, one per round
4. **Anchor Ledger**
5. **Compliance Check**

**There is no move quota.** The run ends when the stop conditions in Step 4 hold, however many moves, rounds or revisits that takes. A move count is an outcome, never a target: do not stop because you reached some number, and do not pad to reach one. Lite mode (one move, one panel round) only if the person explicitly asks. If an external limit forces you to stop before the stop conditions hold, write the Open frontier in the log, say the run is incomplete, and give the resume point. If `DESIGN-LOG.md` already exists with an Open frontier, resume from it instead of starting over.

In your final reply state the mode you ran, the tools you used, the stop conditions as met or not met, and every step you skipped. Never describe the process as followed if it was not.

## Mode (choose once, state it in the Traversal Plan)

| | Autonomous | Adaptive |
|---|---|---|
| Use when | The brief is art on its own terms, or says no ideology, cause or market constraints | The work serves an audience, client or public, or the brief names approachability |
| Governing criterion | Inner necessity and significant form (Kandinsky, Bell, Fry). Reception (MAYA, perceptual legibility) is an optional dial, never a veto | MAYA, Most Advanced Yet Acceptable (Loewy): the advanced pole and the acceptable pole must both hold; if either is weak, revise the move |
| Required critics | Critic: Apollonian Order (Wölfflin, Gombrich), Critic: Dionysian Excess (Nietzsche, Venturi), Critic: Rupture (Shklovsky, Marinetti), Critic: Detachment (Ortega y Gasset, Sontag), plus at least 1 more (5 to 7 total) | Critic: Provocateur (Debord, Shklovsky), Critic: Inclusion (Holmes, Mace), plus at least 3 more chosen for maximum difference |
| Extra record field | Reception dial: used or not, and why | Advanced pole and Acceptable pole, each with its anchor |

**Websites are multi-page whenever possible.** When the artifact is a website, plan it as several pages from the Traversal Plan on: a page per service, product, topic or tool, plus home and the contact, about or legal pages that apply, under shared navigation. A single page is only for something that is genuinely one screen (a single-purpose tool or game), and the plan must say why. A redesign of a one-page site splits it into pages as one of its moves.

**First screen rule (websites).** The landing page leads with one bold graphic: the project's signature visual (a chart, map, illustration, mark or photograph) set large enough to read as the page's subject, not a headline alone. That graphic must be **complete in the first viewport** at both 1280 x 800 and 375 x 812: measure its bounding box and assert that its *bottom* edge is above the fold and that it does not scroll sideways inside its own box. Measuring only where it starts is the error this rule exists for: FoodChart moved its chart up, measured its top at y = 386 px, passed seven seats twice, and was graded B because the chart was cut off and the landing had no bold graphic. When the full graphic cannot fit (a 15-column chart on a phone), design a first-screen version that does fit and is complete (a cropped, larger, or summary form of the same visual, with the full one below), and record the choice in a Decision Record.

**The landing graphic summarizes the whole site.** Before choosing it, list every page or topic the site has. On a site with several topics the landing graphic is one composed figure with a mark, a figure and a link for each topic, so the first screen says what the whole site holds; the strongest single chart goes below it or on its own page. A bold, complete chart of one topic still fails this rule: MacroEconomics led with an oil-reserves chart that passed the First screen rule and seven seats, and was graded B because the landing did not summarize its six topics.

**A cheap run is not exempt.** A Lite or one-pass run still leads with one signature visual, and the cheapest strong one is the product's own worked example drawn large: the Electricity Guide's one-pass restyle was graded C for having nothing to remember, and its retry drew the guide's own 12 V x 10 A = 120 W circuit as the hero. The best-graded heroes were the product itself (SHADW Terrain's live map) or a mark generated from its own output (Facet). dada-lessons 57.

If the person does not name a mode, use Autonomous unless the brief names a client, audience or public constraint, and say which you chose and why. In both modes the panel must include at least one pair of critics joined by a dotted edge in the graph.

## Run type (choose once, state it in the Traversal Plan, alongside the mode)

Mode sets the governing criterion. Run type sets **how much of the artifact may change**. The two combine freely: an Adaptive Polish run, an Autonomous Full run. Pick a run type from the table. If the person names none, use Full for new work or a redesign, Polish when they say polish, refine, tidy, finish or "no redesign", Extend when they ask for more of an accepted design (new pages, places, products), and Landing when the brief is the landing page, its hero or its first screen.

| | Full | Polish | Extend | Landing |
|---|---|---|---|---|
| Use when | New work, a from-scratch build or a redesign | The artifact exists and its concept is accepted; the person wants it finished, not rethought | The design system is accepted and the work needs more of it: new pages, sections, places, products or languages | The brief is the landing page or its hero: "make the landing bold", "a landing graphic", "redo the home page", or a grade that faults the first screen. Also invoked inside a Full run as the landing move |
| Frozen | Nothing | The concept; the seeded Breaker and its devices; the page structure and navigation; palette, type and layout system. A frozen element changes only to fix a measured defect, and the record says which | The same freezes as Polish, plus every existing page's layout. The navigation may gain entries only in slots the system already has (a footer group, a hub page) | Every page except the landing; the design system's palette and type (the landing may push them, not replace them); the site's navigation entries. Content that leaves the landing moves to its own page, never deleted |
| Allowed moves | All | KEEP-THE-RULE refinements; fact and content updates from the owner; metadata (SEO, answer-engine optimisation, structured data, social cards); accessibility and performance; honesty sweeps; new pages only if the existing navigation and system absorb them without change; *escalation* of an existing device, never a new one | New pages and sections built only from existing components and tokens; hub pages that index them; corrections that the new content forces in existing copy (a claim the extension makes false must be fixed); all Polish moves | The landing's first screen and what sits below it; moving displaced content to a new page; one new graphic system for the hero (tiles, poster, wall, map) built from the site's own data and pages; the site's social card, which must match the new first screen |
| R0 premortem | If an artifact exists | Required: the inherited artifact is the subject | Required, scoped to what the extension touches: which existing claims, maps and lists it changes | Required: the current landing, measured against the First screen rule and the summary rule |
| Panel minimum | Per mode (above) | Replaces the mode's minimum: 4 seats, one agent per reference. `Critic: Evidence (Cairo)` as the measurement seat, `Critic: Usability (Krug)`, `Critic: Provocateur (Debord)` as the claims check, plus one seat chosen for the polish target (for example Sharp for brand, Mace for access). Keep a dotted pair (Krug ↔ Debord qualifies) | As Polish, with the fourth seat chosen for the extension's audience (for example Holmes for a new locale, Sharp for new places or products) | 4 seats, one agent per reference: `Critic: Formalist (Arnheim)` for visual force and balance, `Critic: Evidence (Cairo)` measuring the first screen at both sizes and every figure shown, `Critic: Usability (Krug)` for the five-second test, `Critic: Provocateur (Debord)` so the hero is a claim, not a brochure. Dotted pair: Krug and Debord |
| S3 | Two consecutive quiet WHOLE rounds | One quiet WHOLE round after the last move | One quiet WHOLE round after the last move | One quiet WHOLE round after the last move |
| S4 | Ambition push on the boldest Breaker | Polish push: the single refinement with the largest measured effect, pushed once more and measured | Consistency push: the new pages measured against the existing ones (same components, same checks passing, no orphan page) | Hero push: the boldest element of the hero made bigger or sharper once more, then re-measured against the First screen rule |
| Round cap | Stop conditions | 3 WHOLE rounds; anything still open is logged, not chased | 3 WHOLE rounds | 3 WHOLE rounds |

**Every run type is judged rendered.** A Polish or Extend run that changes only words can still break the layout (a longer label wraps, a new page has no inbound link), so the panel sees screenshots and measurements of the rendered artifact in every run type, and a Polish run that touches claims or metadata seats a claims critic (Debord, or Cairo with the source in hand). dada-lessons 54.

**The Landing run.** Invoke it with "landing", "hero", "home page graphic", "first screen", or when a grade faults the landing. It exists because the two best-graded landings did one thing (lessons 40 to 42 in dada-lessons): one composed, bold graphic that summarizes the whole site, complete on the first screen. Steps, in addition to the workflow:
1. **Inventory.** List every page, topic, product or item the site holds, with the one figure, image or fact that best stands for each. The hero must show all of them or say why a group stands for the rest.
2. **Choose a form** that composes the inventory into one figure: a poster of tiles on one heavy grid (one tile per topic: a computed figure, a one-line claim, a small glyph drawn from that topic's data, a link), a wall of previews (one image per item on one grid), a map, or one chart whose marks are the topics. Six cards in a row is not a form; a single topic's chart is not a summary.
3. **Compute every figure** shown in the hero from the site's data at build time, and add each one to the site's figure check.
4. **Measure** the hero against the First screen rule at 1280 x 800 and 375 x 812 (bottom edge, no sideways scroll, no tile overflowing), and the five-second test: name the site and three of its topics from the first screen alone.
5. **Move, don't delete.** Whatever the hero displaces (a previous hero, an animation, a single strong chart) goes below the hero or to its own page, linked from the hero.
6. **Push once** (S4): make the boldest element bigger or sharper and re-measure.

**A move that would break a freeze is out of scope for the run.** Log it under the Frontier as DEFERRED (out of run type) and offer it to the person as a Full run.

**Adding a run type.** Add a column to the table and fill every row: when to use it, what is frozen, which moves are allowed, whether R0 is required, the panel minimum, and any change to S3, S4 or the round cap. Then add its name to the Compliance Check line "Run type stated". Candidates not yet defined: *Audit* (panel and measurement only, no moves), *Port* (same design, new medium).

## Bounded runs

The person may cap the run: a number of critic rounds, "one round max, ship", a cost limit. A bounded run is a normal
run with an early stop, not a different process, and it says so:

- **State the bound** in the Traversal Plan with the person's words, and plan the rounds so that S2 is reachable inside
  it (the ADAPTs from round n need round n + 1 to be judged).
- **One round is not a panel's last word on its own fixes.** When the bound is a single round, reconvene at least the
  Inclusion and Usability seats on the ADAPT move before shipping (dada-lessons 51: one author writing six seats in
  sequence cannot disagree with itself, so the fixes went unjudged).
- **Let the panel sit before you push.** Never push a cluster of fixes before the round that judges them has filed;
  blockchain-explain pushed R0's fixes before R1 and shipped a page nobody could reach (dada-lessons 52).
- **Fixes after the last round are measured, not judged.** Apply the objections that have a measurable answer, measure
  them, and log them as "applied, not re-judged". Do not convene a round past the cap to make the log look complete.
- **Close honestly.** S2 and S3 are usually not met; the Stop test says which, the run is reported as incomplete under
  the bound, and the Open frontier names the resume point (which seats, on which state).

## How the traversal works (non-linear)

You do not walk a list from top to bottom. You keep a **Frontier**: the set of candidate moves reachable from the anchors you have already visited, in either direction. Each round of work spends one candidate and usually creates several more.

- **Reach** candidates by following every edge touching a visited anchor: outgoing solid edges (what the anchor grounds or extends), incoming edges (what grounds it: back-references), and dotted edges (counterpoints).
- **Choose the next candidate** in this priority order: (1) open Andon objections, (2) REOPENED moves, (3) dotted counterpoints of BREAK moves not yet applied or declined, (4) the sharpest disagreement between critics in the last panel, (5) incoming-edge anchors that would ground what you have already done, (6) outgoing solid edges. Among candidates of equal rank, take the one that changes the most: a move that alters the artifact's structure outranks one that alters a value, and a deletion that removes a competing system outranks an addition.
- **Branch**: when two or more Breaker candidates are plausible, make each a branch. Write a Decision Record per branch, render each as a spike, run the panel on each, compare them in a Pugh-Matrix in the log, and SCRAP the losers (their records stay, marked superseded).
- **Reopen**: every move records what it depends on. When a move is ADAPTed or SCRAPped, mark every dependent move REOPENED and put it on the Frontier. Settled moves are never final until the stop conditions hold.
- **Merge**: when two moves interact (type against grid, color against scale), the interaction is itself a candidate; add it to the Frontier.

Frontier format, updated after every panel round:

```
## Frontier
| Candidate | Reached via (edge label, direction) | From anchor | Status OPEN / DEFERRED (reason) / TAKEN (Mn) |
```

## Workflow

### Step 0. Tooling inventory (before anything else)

Check your tool list, and any tool-search or registry facility you have, for tooling that handles graphs, workflows, diagrams, task orchestration or knowledge graphs (names or descriptions mentioning graph, workflow, diagram, mermaid, DAG, plan, task, orchestrate, knowledge graph). Use what exists before falling back to plain files. For example, depending on your environment:

| Job | Use, if available | Fallback |
|---|---|---|
| Render and navigate the anchor graph | A Mermaid or diagram renderer, visualizer, graph database or knowledge-graph tool; a Mermaid parser to validate | Mermaid text in `DESIGN-LOG.md` |
| Compute the Frontier | A graph query for unvisited in- and out-neighbours of visited nodes | Read the edge lines of the graph and list them by hand |
| Track workflow state | A todo, plan, task-list or workflow-engine tool: one task per Frontier candidate taken and per panel round | A checklist in `DESIGN-LOG.md` |
| Run the panel | A sub-agent, task or parallel-agent tool: one agent per literary reference (see Step 2c), **launched at most three at a time, each filing its verdict to a panel directory** | Sequential, written one reference at a time |
| Collect panel reports | A panel directory on disk plus `scripts/collect_panel.py`, listing which seats reported | List the panel directory by hand |
| Choose the panel | `scripts/pick_panel.py` (required seats by mode, run type and context; the rest by rating, plus one rotation seat) | The mode's required critics plus seats chosen by hand, each with a written reason |
| Brief each seat | `seats/<seat_id>.md`: the seat's literature, persona and prompt template | Write the prompt from the graph node, keeping the persona fields |
| Record the run | `scripts/import_log.py` into `ledger/runs.jsonl`, then `scripts/rate_seats.py` | A row in the lessons repository's run index |
| Measure the artifact | A render-and-inspect tool (headless browser, pixel sampling, link fetch) driven by a seat or by a script | Quote the numbers you can compute by hand |
| Persist the log | A docs, notes or artifact tool, in addition to `DESIGN-LOG.md` | `DESIGN-LOG.md` only |

Record in the Traversal Plan which tool you used for each job, or "none available". Do not invent tools, and do not claim a tool was used unless you called it.

### Step 1. Traversal Plan (before touching the work)

1. Read the brief and restate it in one sentence. Choose the mode.
2. Choose the **seed** from the graph in [references/anchor-graph.md](references/anchor-graph.md): 1 Stance node, at least 2 Rules nodes (follow solid edges), 1 Breaker node, and 1 counterpoint reached by a dotted edge from a node you chose. The seed is a starting point, not a plan; it will grow.
3. Copy every label exactly. Each label must occur verbatim in the graph (grep for it if you can).
4. Write the chain of labels with the edge label between each pair, then the initial Frontier (every candidate one hop from the seed, in both directions), then the first move or moves, tagged KEEP-THE-RULE or BREAK. At least one BREAK move must eventually be taken.
5. **Premortem, round R0.** If an artifact already exists, convene a WHOLE panel round on it as it stands *before* the first move, and enter its objections as the first Frontier candidates. A run that has never judged what it inherited is optimising a starting point nobody has defended.
6. Render the graph with your graph tooling and mark visited anchors with the `visited` class (for example, `class stanceId,rule1Id visited`), using node ids from the graph. Without tooling, put the marked Mermaid text in the log.
7. **Seat the panel from the record.** Read [references/seat-ratings.md](references/seat-ratings.md) and the grades ledger, then run `python scripts/pick_panel.py --mode <mode> --run-type <type> --project <name>` with the context flags that apply (`--data-graphic`, `--money`, `--signs`, `--not-inspectable`). It returns the required seats, the best-rated seats for the flexible slots, one rotation seat that has not yet earned a rating, and the dotted pair; copy its table, reasons included, into the Traversal Plan. Override it only with a written reason. Every seat is briefed from its own file in [seats/](seats/README.md), so it brings the same persona to every run and its verdicts can be rated. For any system the artifact describes, name a content-owner witness ([seats/witnesses.md](seats/witnesses.md)).

### Step 2. The loop: spend one Frontier candidate per pass

**2a. Decision Record, written BEFORE you make the move:**

```
## Move Mn: <name>  (KEEP-THE-RULE | BREAK)
Depends on: M-ids, or "none"
Anchors: Stance <label> | Rule <label> | Breaker <label> | Counterpoint <label> (dotted edge from <label>)
Intent: what the move does to the eye and the page.
Formal argument: claim, grounds, warrant, citing the anchors.
Alternatives rejected: at least 2, each with the reason.
Consequence: second-order effects and what the move costs.
Fence: for any rule being broken, why that rule exists.
Frontier effect: the new candidates this move opens.
Mode field: Reception dial (Autonomous) | Advanced pole and Acceptable pole (Adaptive)
```

**2b. Make the move** in the actual artifact, then render it (screenshot, export or open it) so the panel can see it. If you cannot render, write "unrendered" in the Panel Report and say so in your final reply.

**Measure the move; do not assume it.** Wherever the medium can be inspected, compare the artifact before and after and record the number that changed: a rendered size, a computed value, a contrast ratio, a byte count. A change that measures as identical has not been applied, whatever the source now says — find the lever that actually moves the work, and log both the inert attempt and the substitute that worked. Assert on the **computed value**, never on the fact that your edit went in: a patch can land and still be overridden by a later rule. Leave no declaration in the artifact whose effect you cannot show.

**2c. Convene the panel** on the rendered artifact.

- Composition: the required critics for your mode, chosen from the CRITICS box.
- Independence: if you have a sub-agent or task tool, **one agent per literary reference, not per critic**. Every thinker named in a panel critic — and every text in the LENSES cluster — is instantiated as its own agent, arguing from that author's own doctrine alone: a two- or three-name critic (`Critic: Apollonian Order (Wölfflin, Gombrich)`) convenes Wölfflin and Gombrich as two separate agents. No reference may be merged into a composite voice, dropped, or reduced to a label, and the run is not compliant while a required critic has never sat on the panel. The panel must still meet the mode's composition rule. Otherwise write each reference's report in full before reading the others, with no voice reacting to another's verdict.
- Evidence rule: every critic must point to something observable in the artifact and name one literature anchor that grounds the judgment. A critic that cites only the plan is invalid; redo it.
- Run the Critical Response Process in this order: (1) statements of meaning, what the work seems to say; (2) artist questions; (3) neutral questions from critics; (4) opinions, only after the artist permits them.
- Any critic may pull the Andon. Stop making new moves until its objection is resolved.
- **Measurement (see [the field notes](references/field-notes.md), §2).** The panel does not measure by default. Where the artifact can be inspected, convene `Critic: Evidence (Cairo)` as a seat briefed to *run measurements* — contrast over images, focus visibility, overflow, target size, link inventory, and for a website the First screen rule (the landing graphic's full bounding box, bottom edge included, at 1280 x 800 and 375 x 812) — rather than to read screenshots, and give `Critic: Inclusion (Mace)` a named focus-visibility check. A finding that appears only in a tool's output is measured on the rendered page before a move is spent on it.
- **Durability (see [the panel protocol](references/panel-protocol.md)).** Run the panel so a transport failure cannot take a verdict with it. Make a panel directory for the round; instruct every seat to write its report to `<panel_dir>/<seat>.md` as its last action and to return the same text; launch at most three seats at a time; keep each seat prompt under about 350 words; check for an existing file before re-running a seat that appeared to fail; bound retries at three per seat; collect from the directory before writing the Panel Report. **A verdict is a file, not a return value.** A required seat whose file never appears is recorded as `NOT REPORTED (3 attempts, transport failure)` — never as PASS, never reconstructed from memory — and its absence leaves the run incomplete.

- **Brief from the seat file.** Fill the prompt in `seats/<seat_id>.md` (round, evidence file, artifact, word budget, panel directory) and add nothing but the duties that apply. Every fact the conductor puts in a seat prompt comes from the evidence file; a seat seeded with a claim the artifact may not make judges the wrong artifact (dada-lessons 48). Seats number their findings (F1, F2 ...) and tag each `[defect]`, `[claim]` or `[premise]`, so the resolution of each can be credited to the seat that raised it.
- **Measure, then hand the panel the measurement (see [the measurement checklist](references/measurement-checklist.md)).** The style seats walk past numbers (dada-lessons 43): seat Cairo from R0 on any real business or interactive artifact with the build, the tests and the measuring script in hand (47), and Tufte as the instrumentation seat on any data graphic, which is measured against the data it encodes (46). For a page that describes software, the evidence file lists every sentence that states a limit, a default or a refusal with its `file:line` (44). For an app that signs or approves anything, Cairo's brief includes a security read of those actions (53). Measure the smallest label at the narrowest supported viewport (50).
- **Check the instrument before the panel sees it.** Open every screenshot you hand to the panel, not only the first run's: a capture can come back tiled or cropped on a later run, and five seats once judged a tiled image (shadw-MCP R1). Give every measuring probe one fixture that must fail, so an inverted test shows itself (the same run's target-spacing probe reported 0 failures because its filter was backwards). A finding seen only in a file, a log or a capture is measured on the live page before a move is spent on it (dada-lessons 45).
- **Witnesses before verdicts.** Where a system the artifact describes is owned by someone else (another session, a client, a dataset), its content-owner witness files the current facts before R1 and again before Step 2g (dada-lessons 49). A claim the witness contradicts is a `[claim]` finding, not a matter of taste.

Panel Report format:

```
### Panel, Move Mn or WHOLE, round R  (artifact examined: <path or screenshot>)
| Critic | Anchor used | Observed in the work | Verdict PASS/OBJECT | Requested change |
Statements of meaning: ...
Artist questions: ...
Critic questions: ...
Opinions: ...
Andon pulled: yes/no, by whom
```

**2d. Resolve every OBJECT** with exactly one of:

Record the resolutions of a round as a table the ledger can read, one row per finding: `| <Seat surname(s)>: <finding> | ADAPT | OVERRULE | SCRAP | DEFERRED: <what was done> |`, joining seats that raised the same finding with `+` (for example `| Debord + Cairo: "1 call to roll back" | ADAPT (M5): ... |`). When a measurement refuses the premise, write `OVERRULE (premise refuted: <measurement>)`; the ledger counts it against the seat's precision, which is how a seat that keeps judging tiled screenshots is found.

- **ADAPT**: change the move, re-render, and re-run at least the objecting critics (maximum 3 rounds on one move, after which treat it as a frame swap).
- **SCRAP**: revert the move and mark its Decision Record as superseded; do not delete it.
- **OVERRULE**: allowed only with a written reason citing the governing criterion of your mode, or with a measurement that refuses the objection's premise. The objection stays in the log.

**Test an objection's premise against the artifact before you spend a move on it.** A critic can be right about what it sees and wrong about what is there. Measure the premise; if the measurement refuses it, the resolution is OVERRULE with that measurement recorded, not ADAPT. A move spent answering a false premise is a move the work did not get. This is also the only honest way to refuse: a deferral that cannot be undone is a refusal wearing patience, and it belongs in the log as one.

Then mark every dependent move REOPENED. If 3 or more critics object to the same move or the same anchor region, stop and perform a frame swap: replace that region with a sibling anchor reached by an existing edge (dotted edges allowed) and log it as a frame swap.

**2e. Update the Anchor Ledger, the Frontier and the live graph** after every panel round:

```
| Anchor | Role | Status KEEP / ADAPT / SCRAP | Evidence | Replacement or note |
```

Every anchor named in any record gets a row. A KEEP must name the strongest objection it survived. Add every new candidate to the Frontier and mark the one you spent TAKEN. Then update the graph through your graph tooling: apply `kept`, `adapted` or `scrapped` to each anchor's node id (for example, `class nodeId scrapped`), add any replacement anchor reached by an existing edge, and re-render. Without tooling, record the updated Mermaid text in the log. Scrapped anchors leave the active path for this project; the reference file itself is not edited. Do not write moves to please the critics' score; the governing criterion decides.

**2f. Deletion review and residual diff.** Once, before the stop test: name the substantial elements of the artifact that predate this run and say what each earns. Anything that earns nothing is SCRAPped, and the record carries the retained-value ledger — what the deletion must preserve so the surviving decisions still read as decisions. For any move that refactors, consolidates or deletes, attach a **residual diff** to its record: every computed value or behaviour that changed, each classified intended / inert / regression, with regressions fixed before the next move. The largest single improvement a run can make is often a deletion; a run that only added has not looked.

**2g. Re-measure the artifact's own evidence at its final state.** Before the stop test, and again after any change made after it: list every number, ratio, count or measured claim the *artifact* displays to its own audience, and re-measure each against the artifact as it now stands, by the procedure the artifact states or implies. A figure recorded when a move was made is evidence about that moment, not about the artifact that will be published, and later moves routinely move the figures of earlier ones — a character count, a contrast ratio, a pixel population. An artifact that invites audit cannot print a number an auditor cannot reach. One row each: the printed figure / the procedure that reproduces it / the value at the final state / reproducible or corrected. Correct or delete every figure that drifted. Evidence the artifact cannot let anyone reach — a number with no stated procedure, or a procedure no one can run — is given a procedure or deleted.

The same rule binds this log: a verification row is evidence only if it was measured *after* the edit it verifies. A row measured before that edit is stale the moment the edit lands, and must be re-run. Run 2g after the last edit to the artifact and never earlier, or it is not a final-state measurement.

### Step 3. Whole-artifact rounds

Moves that pass alone can fail together. Run a **WHOLE** panel round on the entire artifact whenever a cluster of related moves settles, whenever the Frontier changes substantially, and always before the stop test. Objections raised here about interactions become new Frontier candidates or REOPENED moves. Whole-artifact rounds are not capped, but if 3 consecutive whole rounds each produce a new OBJECT, do not make another move: perform a frame swap or a double-loop revision of the criterion, panel or graph instead.

### Step 4. Stop test and close

Do not close until all of these hold and Step 2g has been run against the artifact in its final state. If any fails, go back to Step 2.

- **S1.** The Frontier has no OPEN items; each is TAKEN or DEFERRED with a recorded reason.
- **S2.** A WHOLE panel round returned PASS from every required critic with no Andon.
- **S3.** Saturation: two consecutive WHOLE rounds produced no ADAPT, SCRAP, REOPEN or new OPEN Frontier item.
- **S4.** Ambition push: you deliberately escalated the boldest move (a Breaker pushed further) and logged the result, **including what changed in the rendered work**: a measured delta, or the measured finding that the intended lever was inert and which lever moved instead. A push that cannot be shown to have changed anything does not satisfy S4 — it is a declaration, not an escalation. A push is a move; if it survives, S2 and S3 must be satisfied again with it in place.
- **S5.** Every dotted edge leaving an anchor you used is either applied or declined with a recorded reason.

Then close:

1. **Double loop.** In one paragraph, say whether the criterion, the panel or the graph itself failed the work, and name one concrete amendment (a node to add or scrap, or a critic to change) under "Graph amendments". Then write the **Carry-Forward Ledger**: the durable, domain-specific facts this run established by measurement, of the kind a later run in this medium would otherwise rediscover the hard way (in CSS, for example: a media query adds no specificity, so a later plain rule beats an earlier media-query rule at equal specificity; a percentage width on a grid item sized by an `fr` track is inert, because the track absorbs it). One line each: the fact, the measurement that established it, and the move it changed. Keep it in a carry-forward file beside the log, and read that file before Step 1 of any later run on the same project. Amendments to the *process* belong in the workflow text; facts about the *medium* belong here.
2. **Compliance Check**, each line with a pointer to where it is satisfied:
   - [ ] Tooling inventory done; tool used for each job, or "none available"
   - [ ] Mode stated with the reason
   - [ ] Panel seated from `scripts/pick_panel.py` (or each override reasoned), every seat briefed from its `seats/` file, and any bound stated with the person's words
   - [ ] Seed with exact labels, including one dotted-edge counterpoint, and a living Frontier
   - [ ] Run type stated (Full, Polish, Extend, Landing, or another defined type), and no move broke its freeze
   - [ ] For a website: the landing leads with one bold graphic that summarizes every topic of the site, measured complete (bottom edge above the fold, no sideways scroll) at 1280 x 800 and 375 x 812
   - [ ] At least one BREAK move taken (or Lite mode stated, or a Polish run, where BREAK means escalating an existing device), and no quota used as a stopping rule
   - [ ] A Decision Record written before each move, with all fields filled, including dependencies
   - [ ] A Panel Report per round from a panel meeting the mode's composition rule, each critic citing something observable
   - [ ] Every OBJECT resolved as ADAPT, SCRAP or OVERRULE, with dependents reopened
   - [ ] WHOLE rounds run; S1 to S5 each shown as met, with where
   - [ ] Every figure the artifact displays re-measured at the final state, with the procedure that reproduces it
   - [ ] Anchor Ledger complete and the live graph updated
   - [ ] Double-loop paragraph written
   - [ ] Run recorded in the ledger (`import_log.py`, `rate_seats.py`), or the final reply says it is not
   - [ ] Final reply states the mode, the tools used, the stop conditions and everything skipped

3. **Record the run.** From the dada repository, import the log into the ledger and re-rate the seats:
   `python skills/dada/scripts/import_log.py <DESIGN-LOG.md> --project <name> --repo <owner/repo>`, then
   `python skills/dada/scripts/rate_seats.py`. The importer reads the panel tables and the resolution tables; it
   reports any seat it could not map, which you fix in the log rather than in the ledger. Without the repository at
   hand, say in the final reply that the run is not yet in the ledger.

**Optional human grade.** A run's critics are agents; the person who asked for the work is the one judge that matters. After delivery the person may grade the run, as a letter (A+ to F) plus any words of their own. Only record a grade the person actually gave: never ask for one as a gate, never infer one from praise, and never invent one. When a grade is given, re-import the run with `--grade <letter> --grade-words "<their words>"` so it moves the seats' grade lift, append a **Human grade** section to `DESIGN-LOG.md` (grade, date, the person's words verbatim, and one line on what the run did that the grade most likely rewards or punishes), and, where a lessons repository is kept, add a row to its `GRADES.md` ledger (date, project, mode, rounds, grade, words, link to the log). Read the ledger before Step 1 of a later run: the moves and seats behind the higher grades are evidence about what this person values.

## Anti-skip rules

- An escalation you did not measure is not an escalation, and a patch you did not verify at the computed value is not a change.
- A move count is never a stopping criterion. Stopping because you reached some number, or because the first pass felt complete, is a skip.
- A linear walk down a list is not a traversal: follow incoming and dotted edges, branch, and reopen settled moves.
- A commit message or code comment is not a Decision Record.
- A quick mental check or a one-line "I considered X" is not a panel.
- Naming an anchor is not using it: it must appear in a record's argument or in a critic's observation, tied to something in the work.
- Not looking for graph or workflow tooling is not the same as none being available.
- A seat that returned "failed" may still have filed its verdict: check the panel directory before spending the seat again. Filling a missing verdict from what you think that authority would have said is a fabricated panel.
- Short on effort is not an exemption. If an external limit forces a stop, write the Open frontier and say the run is incomplete; do not claim the stop conditions held.
- A screenshot you did not open is not evidence, and a probe that has never failed has not been tested.
- A seat chosen because it is familiar is not a seat chosen from the record: run the picker, or write the reason.

## Reading the graph

Solid arrows are forward references (grounds, extends, applies). Dotted arrows are counterpoints or back-references. Boxes are clusters; an arrow into the CRITICS box means the whole panel. The mode only changes the governing criterion and the required critics; every anchor stays available in both. Colors: amber stance, grey rules, pink breakers, violet expression, green systems, slate canon, teal reason, orange welcome, red critics, magenta lenses, cyan panel method, lime adaptation, gold autonomy of art, blue existing catalog anchors. Status classes for the live graph: `visited`, `kept`, `adapted`, `scrapped`.

## Anchor graph

Read [references/anchor-graph.md](references/anchor-graph.md) before choosing the seed and the panel. It contains the complete source graph, including all labels, edges and status classes. Copy labels from it exactly.
