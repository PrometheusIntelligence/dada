"""Tidewatch sprite kit 2.0.

Draw a unit from shapes (rect, ellipse, polygon, line) in *materials*, not colours. The kit then
does the work a pixel artist does by hand:

  * shading   each shape is lit from the top left: top and left edges take the highlight, bottom
              and right edges the shadow, the middle the base tone (4-step ramp per material)
  * outline   a one-pixel ink outline around the whole silhouette
  * shadow    a soft ground shadow under the feet
  * team      the `team` material is a ramp the game fills with each side's colour at run time

`bake()` returns a Sprite as rows of characters plus a legend; build.py writes them to
game/art/units.json, which scenes/sprites.gd reads. Nothing here is imported by the game.
"""
from __future__ import annotations

SIZE = 16            # default canvas; buildings use 32 or 48
SHADES = ("hi", "mid", "lo", "dk")

# Material ramps, light to dark. `team` is a placeholder: the game replaces it per side.
MATERIALS = {
    "team":    ["#a9d0ff", "#7db4ff", "#3a6fd0", "#1f3f7a"],
    "skin":    ["#f0c9a2", "#e2b48c", "#c08a64", "#8f5f44"],
    "steel":   ["#e6e9f0", "#b4bac6", "#7f8694", "#4d5361"],
    "iron":    ["#a6adb9", "#767d8b", "#525866", "#343845"],
    "wood":    ["#b98a55", "#8f6238", "#68431f", "#46290f"],
    "leather": ["#a87a4c", "#7d5532", "#573a20", "#382412"],
    "cloth":   ["#e9e2cf", "#c8bfa5", "#9b917a", "#6d654f"],
    "gold":    ["#fbe58a", "#e8c547", "#b08a22", "#7a5a10"],
    "horse":   ["#b9835a", "#8f5d3a", "#6a4128", "#442817"],
    "olive":   ["#8fa05f", "#52602f", "#2f391d", "#1d2412"],
    "khaki":   ["#cdbd8a", "#a99a63", "#7f7248", "#574e2e"],
    "rubber":  ["#5a5c66", "#3c3e47", "#2a2c33", "#1a1b20"],
    "glass":   ["#cfeaf5", "#8fc4dc", "#5a93b0", "#34586c"],
    "fire":    ["#fff2b0", "#ffc94a", "#f08a2a", "#b8481a"],
    "stone":   ["#b9b9c2", "#8d8d96", "#62626b", "#3d3d46"],
    "thatch":  ["#e6c96f", "#c8a64c", "#9c7b35", "#6f5521"],
    "tile":    ["#d97a62", "#ae4b3b", "#7e3126", "#52201a"],
    "concrete":["#cfcfc7", "#a7a79f", "#7b7b74", "#4e4e49"],
    "dark":    ["#4d3d2d", "#2f2419", "#1f1710", "#120d09"],
    "smoke":   ["#d8d8dc", "#b4b4ba", "#8e8e96", "#6a6a72"],
    "gunmetal":["#7d8591", "#515965", "#353b45", "#1e2229"],
    "glow":    ["#dcffb8", "#8cf05a", "#4fb52b", "#2a6e14"],
}
INK = "#16141c"

# Faction identity, set by build.py before each bake. Emblem: a 3x3 mark drawn on the team-coloured
# surface of every unit and banner (so sides read in greyscale). Flag: the banner shape.
EMBLEMS = {                       # pairwise differ by at least 3 pixels (checked in validate.factions_ok)
    "bars":  [(0, 0), (1, 0), (2, 0), (0, 2), (1, 2), (2, 2)],
    "cross": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    "vee":   [(0, 0), (2, 0), (0, 1), (2, 1), (1, 2)],
    "block": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "ell":   [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
    "slash": [(2, 0), (1, 0), (1, 1), (0, 1), (0, 2)],
}
EMBLEM = {"pts": EMBLEMS["bars"], "mat": "dark", "shade": "mid"}
FLAG = "square"
SHADOW = "#000000"


class Sprite:
    def __init__(self, name: str, shadow: tuple | None = None, outline: bool = True, w: int = SIZE, h: int = SIZE, bob: int = 0):
        self.name = name
        self.w, self.h = w, h
        self.bob = bob                # frame 2 of a walk cycle: the body drops one pixel (the shadow stays)
        self.px: dict[tuple[int, int], tuple[str, int, str | None]] = {}
        self.n = 0
        self.shadow = shadow          # (cx, cy, rx, ry) ground shadow, or None
        self.outline = outline

    # ------------------------------------------------------------ primitives
    def _fill(self, cells, mat, shade):
        assert mat in MATERIALS, f"{self.name}: unknown material {mat}"
        self.n += 1
        for (x, y) in cells:
            if 0 <= x < self.w and 0 <= y < self.h:
                self.px[(x, y)] = (mat, self.n, shade)

    def rect(self, x, y, w, h, mat, shade=None):
        self._fill([(i, j) for j in range(y, y + h) for i in range(x, x + w)], mat, shade)

    def ellipse(self, cx, cy, rx, ry, mat, shade=None):
        cells = [(i, j) for j in range(self.h) for i in range(self.w)
                 if ((i + .5 - cx) / rx) ** 2 + ((j + .5 - cy) / ry) ** 2 <= 1.0]
        self._fill(cells, mat, shade)

    def poly(self, pts, mat, shade=None):
        def inside(px, py):
            hit, j = False, len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]; xj, yj = pts[j]
                if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
                    hit = not hit
                j = i
            return hit
        self._fill([(i, j) for j in range(self.h) for i in range(self.w) if inside(i + .5, j + .5)], mat, shade)

    def line(self, x0, y0, x1, y1, mat, shade=None):
        cells, dx, dy = [], abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            cells.append((x0, y0))
            if (x0, y0) == (x1, y1):
                break
            e2 = 2 * err
            if e2 >= dy: err += dy; x0 += sx
            if e2 <= dx: err += dx; y0 += sy
        self._fill(cells, mat, shade)

    def dots(self, pts, mat, shade="mid"):
        """Single pixels with a fixed shade: eyes, rivets, glints."""
        self._fill(list(pts), mat, shade)

    # ------------------------------------------------------------ bake
    def _auto_shade(self, x, y):
        mat, sid, fixed = self.px[(x, y)]
        if fixed:
            return SHADES.index(fixed)
        same = lambda a, b: self.px.get((a, b), (None, 0, None))[1] == sid
        score = (not same(x, y - 1)) + (not same(x - 1, y)) - (not same(x, y + 1)) - (not same(x + 1, y))
        return 0 if score > 0 else 2 if score < 0 else 1

    def bake(self):
        """Returns {(x, y): (material, shade) | 'O' | 'S'} for every painted pixel."""
        out = {(p[0], p[1] + self.bob): (self.px[p][0], self._auto_shade(*p)) for p in self.px}
        if self.outline:
            for (x, y) in list(out):
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < self.w and 0 <= ny < self.h and (nx, ny) not in out:
                        out[(nx, ny)] = "O"
        if self.shadow:
            cx, cy, rx, ry = self.shadow
            for j in range(self.h):
                for i in range(self.w):
                    if ((i + .5 - cx) / rx) ** 2 + ((j + .5 - cy) / ry) ** 2 <= 1.0 and (i, j) not in out:
                        out[(i, j)] = "S"
        return out


def mark(s, x, y, scale=1):
    """Draws the current faction's emblem with its top-left at (x, y); scale 2 draws each cell as 2x2 (big vehicles).
    Dark factions get a 1 px ink halo so the light emblem holds contrast on the team highlight
    (accessibility seat, R6: 1.75:1 without it)."""
    pts = {(x + i * scale + a, y + j * scale + b) for i, j in EMBLEM["pts"] for a in range(scale) for b in range(scale)}
    if EMBLEM.get("halo"):
        halo = {(a + dx, b + dy) for a, b in pts for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - pts
        s.dots(sorted(halo), "dark", "dk")
    s.dots(sorted(pts), EMBLEM["mat"], EMBLEM["shade"])


# Character legend: one fixed character per (material, shade), plus . O S.
_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNPQRTUVWXYZ0123456789!#$%&*+-:;<=>?@^_~|/()[]{},'"
LEGEND = {}
for _i, (_m, _ramp) in enumerate(MATERIALS.items()):
    for _s in range(4):
        LEGEND[_CHARS[_i * 4 + _s]] = [_m, _s]
_REV = {tuple(v): k for k, v in LEGEND.items()}


def rows(baked, w: int = SIZE, h: int = SIZE) -> list[str]:
    out = []
    for y in range(h):
        row = ""
        for x in range(w):
            v = baked.get((x, y))
            row += "." if v is None else v if isinstance(v, str) else _REV[v]
        out.append(row)
    return out


def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
