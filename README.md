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

## Validation

Run `python3 scripts/validate_skills.py` with PyYAML installed. It checks the skill's metadata, references and discovery link, and that the seat files, the ratings and the ledger match their sources. GitHub Actions runs it for pushes and pull requests. The skill's own scripts (`build_seats.py`, `import_log.py`, `rate_seats.py`, `pick_panel.py`) need only the Python standard library.
