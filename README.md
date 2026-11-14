# DADA — Directed Ambition Design Agent

An agent skill for ambitious graphic design, packaged from the Graphic Design Agentic Workflow (gdaw). It supports identity, posters, books, editorial design, motion, typography, imagery, data graphics, and interfaces.

The original anchor catalog and graph structure live in a linked reference. DADA traverses that graph non-linearly through a living Frontier, with no move quota, until the critics converge and the stop conditions hold.

## Install

Install with the skills CLI from any project folder:

```sh
npx skills add AnEntrypoint/dada -s dada
```

The CLI detects your agent, copies the `dada` skill into its skills folder, and records it in `skills-lock.json`. Use `npx skills list` to confirm the install.

This repository also includes `.agents/skills/dada`, a relative link to `skills/dada`, for workspace discovery. After opening this project, the skill is available on the next turn.

To copy the skill by hand instead, copy `skills/dada` into your agent’s skills directory, for example `~/.agents/skills/dada`, or `~/.codex/skills/dada` for Codex. Preserve any existing installation before replacing it.

## Use

Invoke `$dada` with a design brief. DADA always pursues maximum artistic ambition and runs in one of two modes, chosen once and stated in the Traversal Plan:

- **Autonomous** judges the work on its own terms (inner necessity and significant form), with no ideology, cause or market as a veto. It is the default unless the brief names a client, audience or public constraint.
- **Adaptive** adds approachability: MAYA, Most Advanced Yet Acceptable, requires both the advanced and the acceptable pole to hold.

The traversal is non-linear: each pass spends one candidate from the Frontier (outgoing, incoming and dotted edges from visited anchors), branches between rival Breakers, and reopens earlier moves when a dependency changes. A move count is never a stopping rule. The run closes only when the five stop conditions hold: no open Frontier items, a WHOLE panel round with every required critic passing, saturation across two consecutive WHOLE rounds, a logged ambition push, and every dotted edge applied or declined. A Lite run (one move, one panel round) happens only on explicit request, and an interrupted run records its Open frontier and resume point in `DESIGN-LOG.md`.

The workflow records a Traversal Plan with its Frontier, Decision Records, Panel Reports, an Anchor Ledger, and a Compliance Check in `DESIGN-LOG.md`. Read `skills/dada/SKILL.md` for the full contract and `skills/dada/references/anchor-graph.md` for the graph. The verdict on every node of that graph from the most recent traversal is in `skills/dada/references/traversal-ledger.md`.

## Game-development extension (GDADA)

Five more skills sit beside `dada` in `skills/`. They are DADA's games fork and the method that grew out of the Tidewatch
game (34 logged runs; the record and the lessons are in
[dada-lessons](https://github.com/PrometheusIntelligence/dada-lessons) under `tidewatch-game/` and `LESSONS.md`, "Games").
They are maintained upstream in [SolutionsAsService/gdada](https://github.com/SolutionsAsService/gdada).

| Skill | Use it for |
|---|---|
| [`gdada`](skills/gdada/SKILL.md) | The run method for games: `VISION.md` first, modes, run types, a round cap, measurement (determinism, bots, frame budget), plus honesty, AI, balance and simulation rules from Tidewatch |
| [`gdada-art-subagents`](skills/gdada-art-subagents/SKILL.md) | Many sprites or models by parallel authors: file ownership, contracts, validators, one build by the lead |
| [`gdada-procgen`](skills/gdada-procgen/SKILL.md) | Procedural maps and cities: preview first, contracts between modules, reach checks, spawn ordering, per-kind validators |
| [`gdada-pixel-style`](skills/gdada-pixel-style/SKILL.md) | One pixel scale and style across terrain, procedural buildings and sprites |
| [`gdada-sprite-quality`](skills/gdada-sprite-quality/SKILL.md) | A rubric, a density budget and an author-then-independent-critic loop for sprites |
| [`gdada-grand-strategy`](skills/gdada-grand-strategy/SKILL.md) | Paradox-style grand strategy and large simulations: provinces, persistent clock, flow economy, supply, fronts, map modes, save/load, budgets, vertical slices |

Games are not recorded in `ledger/runs.jsonl`: its rows are produced by `import_log.py` from a DESIGN-LOG.md with seat
verdicts, and a GDADA-LOG.md has a different shape (and no seat registry for its critics).

## Seats, grades and ratings

Every critic in the graph is a **seat**: one authority, one agent, one file. [`skills/dada/seats/`](skills/dada/seats/README.md)
holds 52 seat files. Each file has the seat's literature and rivals from the graph, a **persona** and a ready panel
prompt. The persona is the temperament the seat brings to every run, with what it always checks, what it never accepts,
its signature question, its blind spot, its voice and its duties. Personas live in `seats/personas.json` and are
versioned, and each has a hash, so a seat's record belongs to the personality that earned it.
`scripts/build_seats.py` regenerates the files. [`seats/witnesses.md`](skills/dada/seats/witnesses.md) defines the
content-owner witness, which testifies to facts but does not vote.

Every run goes into [`ledger/runs.jsonl`](ledger/README.md): each seat's verdict per round, the outcome of every
finding credited to a seat, and the person's grade when one was given, verbatim. `scripts/rate_seats.py` turns the
ledger into [`references/seat-ratings.md`](skills/dada/references/seat-ratings.md). It scores each seat on:

- **precision:** how many of its objections moved the work, against how many were overruled or had their premise
  refuted by a measurement;
- **yield:** how much it moved the work per round sat;
- **grade lift:** the human grades of the runs it sat on;
- **reliability:** whether its verdict was filed.

`scripts/pick_panel.py` seats the next panel in four steps:

1. It takes the seats the mode, run type and context require.
2. It fills the flexible slots with the best-rated seats, shrunk toward a prior so two lucky rounds do not beat forty
   good ones.
3. It always rotates in one seat that has not yet earned a rating, chosen per project.
4. It rests any seat that sat three runs running without moving the work.

The ledger was seeded from 40 runs pushed between 27 and 31 Oct 2026.

[`references/measurement-checklist.md`](skills/dada/references/measurement-checklist.md) collects the probes the runs
proved necessary, each with the failure behind it. The lessons themselves are kept in
[PrometheusIntelligence/dada-lessons](https://github.com/PrometheusIntelligence/dada-lessons).

## Mobile Floor

Every run that ships a page owes a great phone experience, and no run type waives it. The standard is
[`skills/dada/references/mobile-standard.md`](skills/dada/references/mobile-standard.md): 44px touch targets, no text
under 12px, inputs at 16px, hover gated, no sideways scroll, and the rest, each with a measured probe. Run it against any
site:

```sh
python3 skills/dada/scripts/check_floor.py --web path/to/site
python3 tools/measure.py --preset mobile --web path/to/site     # the raw numbers at 360, 390 and 430px
```

## Registry

[`registry/registry.json`](registry/registry.json) is the one list of the skills, MCP servers and manuals dada and its
forks use, with where each skill attaches to a run. External skills from
[SolutionsAsService/skills](https://github.com/SolutionsAsService/skills) (animation, `mobile-native`, `break-ui`,
`prototype` and the rest) are pinned by commit and file hash and attached to the phase of the run where they help.
`python3 skills/dada/scripts/validate_registry.py` fails when any of it drifts.

## Run manuals

The run types (Full, Polish, Extend, Landing) are also published as data in
[`skills/dada/runtypes/dada.manual.json`](skills/dada/runtypes/dada.manual.json), against the JSON Schema
[`skills/dada/schema/dada-manual.schema.json`](skills/dada/schema/dada-manual.schema.json). It takes UTCP's declarative
manual with direct call templates and MCP's capability detection and tool annotations, and adds the run contract,
assertions on computed values and an evidence class on every instrument. Forks such as
[3dada](https://github.com/SolutionsAsService/3dada) extend it with their own run types (drone, miniatures,
product enclosure). See [`skills/dada/runtypes/README.md`](skills/dada/runtypes/README.md).

## Validation

Run `python3 scripts/validate_skills.py` with PyYAML installed. It checks the skill's metadata, references and discovery link, that the seat files, the ratings and the ledger match their sources, and that the run manual validates against its schema and agrees with `pick_panel.py` (`skills/dada/scripts/validate_runtypes.py`, standard library only). GitHub Actions runs it for pushes and pull requests. The skill's own scripts (`build_seats.py`, `import_log.py`, `rate_seats.py`, `pick_panel.py`) need only the Python standard library.
