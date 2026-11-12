# GDADA sprite tool

Pixel-art units and buildings from shapes in materials, with automatic shading, outline, shadow, two-frame walk cycles,
ghost scaffolds, per-faction identity (colours, a 3x3 emblem on every sprite, flag shapes), and a validator. Pillow is the only dependency.

    python3 build.py --roster example --out art/units.json --sheet sheets/   # --factions example/factions.json by default

- `kit.py`: the drawing kit (Sprite: rect, ellipse, poly, line, dots; 20 material ramps; `team` is a placeholder ramp the
  game fills per side).
- `validate.py`: the checks (team colour pixels and share, fill, clipped outlines, stray pixels, silhouette distinctness,
  walk-frame change, side luminance ratio). Change thresholds only with a measured reason, and log it.
- Canvas sizes: infantry 16x16, buildings 32 or 48, vehicles 24x24 (`vehicles.py`); `validate.UNIT_BIG` scales the team-colour and fill
  thresholds for the larger vehicle canvas. `kit.mark(s, x, y, scale)` draws the faction emblem at 1x or 2x.
- `props.py` (in `example/`): neutral 24x24 map props (the three mines), baked under `props` in the output JSON.
- `example/`: the Tidewatch roster (8 medieval and 11 modern units, 7 buildings per era) and `factions.json` (six fictional
  factions: light ones are paired with dark ones, and the validator asserts a 2:1 luminance gap and distinct emblems).
  Copy it, rename kinds, redraw.
- Output: one JSON file (`materials`, `legend`, `eras`, `buildings`) that a game engine paints at load time; Tidewatch's
  `game/scenes/sprites.gd` is the reference loader.

Lessons from using it: [../../references/lessons.md](../../references/lessons.md). Use it for any run whose art is
drawn on a grid; then add the art measurements in [../../references/measurement-checklist.md](../../references/measurement-checklist.md).
