# Run manuals

`dada.manual.json` is DADA's run-type table as data. [`SKILL.md`](../SKILL.md) stays the contract; the manual is its
machine-readable form, so a host, a picker or a fork can read what a run type freezes, who judges it, how it is
measured and when it stops without parsing prose. `scripts/validate_runtypes.py` fails when the two disagree (it
compares the panel minimums with `pick_panel.py`).

The format is [`../schema/dada-manual.schema.json`](../schema/dada-manual.schema.json) and borrows from the two tool
protocols the project cares about:

| | UTCP | MCP | DADA manual |
|---|---|---|---|
| Unit | a *manual* listing tools | a *server* you connect to | a *manual* listing **instruments** and **run types** |
| Call path | `call_template` straight to the native endpoint, no wrapper | JSON-RPC through the server | `call_template` (`mcp`, `cli`, `http`, `text`), so an instrument can be a script, an HTTP endpoint **or an MCP tool** |
| Typed IO | `inputs` / `outputs` JSON Schema | `inputSchema` / `outputSchema` | the same, on every instrument |
| Hints | tags | tool annotations | `annotations` (`read_only`, `idempotent`, `destructive`, `costly`) plus tags |
| Discovery | manual URL | capability negotiation | `requires[]`: each capability names a probe and a **proof call**, and what to do if missing |
| Resources | none | resources, prompts | a run type's `lessons[]`: files read before Step 0, each checked to exist |

What neither carries, and the manual adds:

- **The run contract.** `frozen`, `allowed_moves`, `r0_premortem`, `panel` (required seats, dotted pair, context seats,
  one agent per reference), `stop` (S3 rounds, the S4 push, the round cap) and `judged_rendered`, which is `true` and
  cannot be turned off.
- **Assertions on computed values.** A run type's `measurements` name an instrument, the scope the figure claims, the
  viewports, and `assert` rows (`n == 0`), each with the failure it exists to catch.
- **An evidence class on every instrument.** `MEASURED`, `LOCAL` (an offline stand-in, recorded as such) or
  `DECLARED` (a procedure's claim). The validator refuses an assertion that rests on a `DECLARED` instrument.
- **Fallbacks that end in UNKNOWN.** `fallback` chains instrument to instrument; a value no instrument produced is
  written UNKNOWN with the method that would produce it, never invented.
- **Forks.** `extends` names parent manuals and a run type may `extends` another (`dada/full`). A fork adds
  instruments and run types in its own manual and never edits the parent's file. 3dada's manual is the worked example.

## Floors

`floors` holds standards every run type must meet. A floor names its standard (`reference`, a file that must exist),
the measurements that prove it at stated viewports, what the panel judges because no probe can, and the skills that
carry the fixes (`fix_with`). Its `waivable` is the constant `false`: a manual that says otherwise fails validation, and
run types have no field with which to opt out. `scripts/check_floor.py --web DIR` executes a floor against any site and
exits non-zero if an assertion does not hold.

The first floor is the Mobile Floor, [`references/mobile-standard.md`](../references/mobile-standard.md).

## Adding a run type

Add an object to `runtypes` with every required field, name its seats from `seats/`, list the instruments it uses,
then run `python3 scripts/validate_runtypes.py --seats-dir skills/dada/seats`. If it is a run type SKILL.md already
defines, keep the two in step; if it is new, add its column to the SKILL.md table as well (the Adding a run type
paragraph there lists the rows). `lite` is not a run type; it is a bound on one (SKILL.md, Bounded runs).

## Registry

[`registry/registry.json`](../../../registry/registry.json) lists the skills, MCP servers and manuals dada and its
forks use, and where each skill attaches (which manual, which run types, which phase of the run). It exists so three
things cannot drift apart: the skills on disk, the manuals' instruments, and the people's picture of both.
`skills/dada/scripts/validate_registry.py` fails when a skill is unregistered, a server a manual calls is unregistered,
a `used_by` list is wrong, an attachment names a run type that does not exist, a floor's fix library is not attached, or
an external skill's pinned file changed under us. A fork's registry `extends` this one and only adds.
