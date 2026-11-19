# GDADA games on the SHADW stack

How a game GDADA manages plugs into the SHADW Game Suite (PrometheusIntelligence), what is proven, and what the Holy Temple's lessons
suggest the suite should take next. Status 2026-11-12.

## The stack

| Stage | Product | Repository | What a game gives it |
|---|---|---|---|
| Project file and CLI | SHADW Game Suite | `PrometheusIntelligence/shadw-gamesuite` | `shadw.game.json` at the game's root: engine, test, keys, deploy |
| Worlds | SHADW Terrain | `PrometheusIntelligence/shadw-terrain` | `world.params` (optional; a hand-made world like the Holy Temple's has none) |
| Sandboxed build and test | SHADW Forge | `PrometheusIntelligence/shadw-forge` | the test command (argv), run network-off on a read-only copy; artifacts hashed, events hash-chained |
| Keys and signing | SHADW KeyForge | `PrometheusIntelligence/shadw-keyforge` | `kfb1` build manifests (G2) |
| Selling | SHADW Game Store | `PrometheusIntelligence/shadw-game-store` | a `catalog.json` entry; later a signed build and prices; the buyer gets a deed |
| Site | SHADW Game Suite site | `PrometheusIntelligence/shadw-gamesuite-site` | a games-page section with its measured test result |
| Hosting | shadw.cloud | `PrometheusIntelligence/shadow` | `deploy` (G3) |

## The TempleOS engine (built 2026-11-12)

- `engine.name: "templeos"` (version 5.03, export desktop) in `shadw.game.json`; `shadw game init --engine templeos` writes one.
- `test.command: ["gamec", "run", ".", "--seconds", "900"]`: the suite maps `gamec` to `$SHADW_TEMPLEOS/Backend/tools/gamec.mjs` (the
  TempleOS fork) and appends `--tos $SHADW_TEMPLEOS_ISO`. Needs QEMU, dosfstools + mtools, the TempleOS V5.03 ISO.
- `test.exclude`: top-level names left out of the staged copy (the Holy Temple excludes `dist` and `.claude`: 2.5 GB down to 35 MB).
- Under Forge `gamec run` writes the serial log and screenshots to `$SHADW_ARTIFACT_DIR` and the 64 MB disk image to the temp dir (Forge's
  artifact budget is 64 MiB); QEMU runs with `-nic none` (TempleOS has no network; Forge's local runner does not enforce network-off).
- Proven: The Holy Temple, `shadw game test` -> Forge completed, exit 0, TempleOS verdict PASS (TWORLD PASS, save v14 -> v15), 75 s,
  8 hashed artifacts, event chain intact; the game tree mounted read-only. Suite tests 16/16.

## What the Holy Temple taught that the suite should take (proposals, in order)

1. **`shadw game build` per engine** (G1 is open on `build`): for `templeos` it is `gamec dist` (installed disk, autostart, first boot at
   build time, run scripts, VirtualBox, SHA256SUMS: [release-craft.md](release-craft.md)); for Godot the web/desktop export. One verb, the
   engine decides.
2. **A "played" proof beside the bot test**: `gamec play` drives the shipped build through its own launcher (waitscreen, key, shot,
   poweroff, boot, expect-file). The suite could run a `play` script under Forge and hash its screenshots, the same way `test` does: the
   gap between "its tests pass" and "a person can play it" (gdada gate G4).
3. **Saves outside what the store owns**: the store's owned-copy bundle and launcher (deed, build manifest, proof of possession) should keep
   the game disk read-only and saves in the player's folder, as the Steam and itch builds do (release-craft R-ship-3).
4. **Sign what you ship**: the bundle's SHA256SUMS become a KeyForge `kfb1` manifest (G2); the store's catalogue entry then gets a `build`.
5. **Ties audit for worlds**: Terrain makes maps; GDADA's `world_graph.py` / `zone_audit.py` prove a world's regions are reachable more than
   one way and tied by what the player earns ([world-ties.md](world-ties.md)). A Terrain world could be checked the same way.
6. **gdada as the design manager across suite games**: list Shipwright, Tidewatch and Shadow Duel in gdada's `registry.json` beside the
   Holy Temple, with gates mapped to the suite's phases (G1 build and test, G4 played, G5 panel), so one table says what each game needs next.
7. **Credit**: every repository credits only SolutionsAsService (a `CLAUDE.md` rule in each; production R17).

## How to add another GDADA game

1. `shadw game init --engine <engine>` at the game's root; fill `test` with the game's own headless check (exclude build outputs).
2. `SHADW_FORGE=... node <suite>/src/cli.ts game test`, then record the run's verdict and duration in the game's docs and the site.
3. Add a catalogue entry to the store (status `in development`, `build: null`, no prices until the owner sets them).
