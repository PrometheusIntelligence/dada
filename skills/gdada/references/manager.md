# GDADA as a manager

GDADA directs one game through a run. The **manager** directs many games across runs: it keeps a registry, judges each
game against a fixed ladder of gates, and names the next step. It exists because a run can stall for a reason outside
the game (ThirdTemple's first run could not execute its build because no TempleOS runtime was on the machine), and a
single-game log cannot see that the same wall stops every game on that backend.

## The registry

`registry.json` at the root of the repo that holds the manager. Schema:

```
{
  "backends": { "<name>": { "runtime_available": bool, "evidence": "how this was found out", "tool": "command" } },
  "games": [ {
    "id": "...", "repo": "Owner/Name", "backend": "<name>", "mode": "Authored|Player-first",
    "run_type": "Concept|Prototype|Polish|Extend",
    "musthaves": { "total": n, "verified": n },
    "gates": { "G1": { "status": "pass|fail|unknown", "evidence": "..." }, ... }
  } ]
}
```

`G0` is not stored per game; it comes from the game's backend (`runtime_available`).

## The gates (climbed in the order G1, G0, G2, G3, G4, G5)

G1 needs no runtime, so a game climbs it first; G0 then stands between the host check and everything that has to run.

| Gate | Question | Passes on |
|---|---|---|
| G0 Runtime | Can the target runtime run here? | the backend's `runtime_available` is true, with evidence |
| G1 Host | Does the tree pass the backend's host check? | the check's exit code |
| G2 Build | Does the target compiler accept the whole tree? | the compiler's own output |
| G3 Tests | Do the game's tests pass unattended in the runtime? | the test run's verdict line |
| G4 Played | Has a person or a bot played it in the runtime? | a recording, screendumps or a bot trace |
| G5 Panel | Did a played WHOLE panel round pass? | the Panel Report in `GDADA-LOG.md` |

A gate passes only with evidence. A gate above an unmet gate in that order is invalid (a game cannot be "played" if it never built),
and the manager reports it as an error instead of believing it.

## Next-step rule

1. For every game find the first gate in climbing order that is not `pass`.
2. If it is G0, the step is to obtain the runtime. It outranks everything, because it blocks every game on that backend.
3. Otherwise rank games by unverified Must-haves (`total - verified`), most first, and name the step that turns that
   game's lowest gate green.
4. Among equals prefer the step that also lifts shared backend code, since it helps every game.

`scripts/gdada_next.mjs registry.json` applies this and prints the result; `--json` prints it for tools.

## Run types, extended

The existing run types (Concept, Prototype, Polish, Extend) direct one game. **Manage** is the run type for the
registry: its output is an updated `registry.json`, a gate table and the next step, and its log is `MANAGE-LOG.md`. It
has no round cap because it takes no design moves; it ends when every game's next step is written and every gate claim
carries evidence.

## Amendment from the ThirdTemple run (double loop)

Step 0 gains a **runtime gate**: before the first move, find out whether the target runtime can run on this machine. If
it cannot, the first Frontier item is to obtain it, and design moves on that game are judged *source-only* until it
exists. This is how the ThirdTemple log asked to amend the graph.

## Focus

The registry may name `focus`, one game id. The manager then plans and reports that game first and parks the rest; the
next step it prints is the focus game's. Change `focus` only when the person says to move on.
