# Ledger

The record of DADA runs, used to rate the panel's seats and to choose panels from evidence rather than habit.

| File | What it is | Written by |
|---|---|---|
| `runs.jsonl` | One JSON line per run: its seats' verdicts per round, the outcome of every finding the log's resolution tables credit to a seat, and the person's grade if one was given | `skills/dada/scripts/import_log.py` |
| `../skills/dada/references/seat-ratings.json` | Every seat's counts and score, shipped with the skill so an installed copy can pick panels | `skills/dada/scripts/rate_seats.py` |
| `../skills/dada/references/seat-ratings.md` | The same ratings as a table, shipped with the skill so an installed copy can read them | `rate_seats.py` |

## A run record

```json
{
  "id": "…", "date": "2026-10-31", "project": "shadw-MCP", "repo": "SolutionsAsService/shadw-MCP",
  "log": "https://github.com/…/DESIGN-LOG.md", "mode": "adaptive", "run_type": "full", "rounds": ["R1", "R2"],
  "seat_rounds": [{"seat": "crit_evid_cairo", "round": "R1", "verdict": "OBJECT", "persona_hash": "pre-registry"}],
  "outcomes": [{"seats": ["crit_evid_cairo", "crit_prov_debord"], "finding": "Debord + Cairo: \"1 call to roll back\"", "outcome": "ADAPT"}],
  "grade": {"letter": "B+", "points": 3.3, "words": "the person's words, verbatim"},
  "unmapped_seats": [], "source": "import_log.py"
}
```

Outcomes: `ADAPT` and `SCRAP` (the finding moved the work), `OVERRULE` (a judgment against the seat), `REFUTED` (the
objection's premise failed a measurement), `DEFERRED` (neutral). A grade is recorded only when the person gave one, in
their own words; it is never inferred.

## Workflow

After a run closes (SKILL.md Step 4):

```bash
python skills/dada/scripts/import_log.py path/to/DESIGN-LOG.md --project NAME --repo OWNER/REPO
```

```bash
python skills/dada/scripts/rate_seats.py
```

When the person grades the run, import it again with `--grade B+ --grade-words "…"`; the record is replaced, not
duplicated. Before a run, `python skills/dada/scripts/pick_panel.py --mode adaptive --project NAME` proposes the
panel.

## Since the backfill

- 2026-10-31: shadw-MCP run 2 (Polish, the Shadw deploy fix), the first run seated by `pick_panel.py` and briefed from the seat files (persona hashes recorded). Imported with `--from "# Run 2" --registry`; run 1 of the same log with `--until "# Run 2"`.

## The backfill (31 Oct 2026)

`runs.jsonl` was seeded from the 39 DADA-family logs pushed to SolutionsAsService and PrometheusIntelligence between
27 and 31 Oct 2026, plus the shadw-MCP site run, with the five human grades from dada-lessons' `GRADES.md`. Of the 40
runs, 35 had panel tables the importer could read (440 seat-rounds) and 96 findings had resolutions it could credit. It is
partial in three known ways:

- Older logs did not number findings or keep resolution tables, so their seats are rated mostly on converted
  objections, an OBJECT followed by a PASS from the same seat.
- The 3DADA and P-DADA runs use rosters outside this graph (Dreyfuss, Boothroyd, Brooks, Flyvbjerg), so they are
  listed as unmapped.
- A few logs name a concern without an authority ("Evidence"), and those rows are dropped.

Every row from the backfill carries `persona_hash: "pre-registry"`.
