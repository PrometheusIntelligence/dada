# Backends

A backend is whatever turns a game's source into a running game. GDADA does not care which; it needs the backend to
answer five questions with an exit code or a line of text. The manager registers one entry per backend.

| Question | Contract |
|---|---|
| Is the runtime here? | `runtime_available` plus the evidence (a version string, a file path) |
| Does the tree pass the host rules? | `check <game-dir>` exits 0 |
| Does the compiler accept it? | `build` / `run` output, or a verdict line |
| Do the tests pass unattended? | a final line such as `BACKEND_OK` or `BACKEND_FAIL=<n>` |
| Can it be played and recorded? | screendumps or a bot trace saved beside the log |

## TempleOS (HolyC)

Repository: `SolutionsAsService/TempleOS`, a fork of the TempleOS V5.03 source. Its `Backend/` directory holds:

- `tools/gamec.mjs`: `check`, `build` (a data disc via xorriso), `run` (QEMU headless, serial log).
- `Lib/Host.HC`: the game-side link that prints the verdict on COM1.
- `games.json`: that repo's own view; this manager's `registry.json` is the one GDADA acts on.

The game provides a `shadw.json` manifest (`id`, `title`, `version`, `language: "HolyC"`, `runtime`, `entry`, `load`,
`install_path`, `tests.templeos_auto`, `tests.fail_counter`). ThirdTemple is the reference game.

Runtime needs a TempleOS V5.03 boot ISO, which is a user-supplied file: the cloud sandbox cannot reach templeos.org or
archive.org. Until one is supplied the backend's `runtime_available` is `false` and every HolyC game stops at G0.

## Art tooling

`SolutionsAsService/cpp-sprites`: a C++17 viewer that reads a HolyC game's tiles, sprites, maps and palettes and writes
PNGs (`make test` smoke-tests it). It lets art be judged before a runtime exists, and so serves the "played" evidence only as
a *look*, never as G4. Games must follow the ThirdTemple art conventions (8x8 hex-digit rows, 16-colour palettes).

## SHADW Game Suite

A TempleOS game also runs under the SHADW Game Suite: `engine: templeos` in `shadw.game.json`, `shadw game test` runs `gamec run`
under SHADW Forge (network off, read-only tree, hashed artifacts). See [shadw-stack.md](shadw-stack.md).
