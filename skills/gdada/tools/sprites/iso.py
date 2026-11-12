"""Isometric sprite kit: build a unit or building as a few solid parts (boxes, wedges, prisms) in materials, then render it
from any heading. The game rotates its world freely, so every unit and building needs a sprite per facing; drawing 16 by
hand is not realistic, so the model is drawn once in 3D and projected.

Model space: x is the unit's forward axis, y its right, z up; the origin is the middle of its footprint on the ground. A unit is
a handful of parts:

    m = Model("tank")
    m.box(-7, -4, 0, 14, 8, 3, "olive")                     # x, y, z of the low corner, then size x, y, z
    m.wedge(-6, -3.5, 3, 12, 7, 3, "olive", slope=3)        # a box whose front top edge is lowered by `slope`
    m.prism(0, 0, 6, 3, 2, "team", sides=8)                 # a round turret: centre x, y, z, radius, height
    m.decal_top(..)                                         # the faction mark on a top face

Rendering turns the model by `yaw` (radians, 0 faces down-right on screen), projects it with the same 2:1 view the game uses
(rotate, squash y to half, z scaled by cos 30), sorts the parts back to front, shades each face by its normal against a fixed
light (top light, then screen-left, then screen-right), outlines the silhouette and puts a ground shadow under it.
Output is the same {(x, y): (material, shade) | 'O' | 'S'} dictionary as kit.Sprite.bake(), so everything downstream
(rows, legend, per-faction team ramps, validators) is shared with the flat sprites.
"""
from __future__ import annotations
import math
import random
import kit
from kit import MATERIALS, SHADES

Z_SCALE = math.cos(math.radians(30))
# The light, in the screen-aligned frame (x right, y toward the viewer, z up). Top light, a little from the left.
LIGHT = (-0.45, 0.35, 0.82)


def _norm(v):
    n = math.sqrt(sum(c * c for c in v)) or 1.0
    return tuple(c / n for c in v)


LIGHT = _norm(LIGHT)


class Part:
    def __init__(self, verts, faces, mat, shade=None, team=False):
        self.verts = verts            # [(x, y, z)]
        self.faces = faces            # [[vertex index]] each counter-clockwise seen from outside
        self.mat = mat
        self.shade = shade            # a fixed shade (0 to 3) overrides lighting
        self.centre = tuple(sum(v[i] for v in verts) / len(verts) for i in range(3))
        self.dim = 0                  # darkens the part by this many shade steps (scorching)


class Model:
    def __init__(self, name: str, w: int = 24, h: int = 24, scale: float = 1.0, ground_y: float = 0.78, shadow: float = 1.0):
        self.name = name
        self.w, self.h = w, h
        self.scale = scale
        self.ground_y = ground_y       # where the footprint's centre sits vertically on the canvas
        self.shadow = shadow           # shadow size factor, 0 for none
        self.parts: list[Part] = []
        self.decals: list[tuple] = []  # (x, y, z, pts, mat, shade): flat marks on a horizontal surface
        self.mark_at: tuple | None = None   # (x, y, z): where the faction emblem goes (a horizontal surface, usually the turret top)
        self.mark_scale = 1

    # ------------------------------------------------------------ parts
    def box(self, x, y, z, w, d, h, mat, shade=None):
        return self.wedge(x, y, z, w, d, h, mat, shade, slope=0.0)

    def wedge(self, x, y, z, w, d, h, mat, shade=None, slope: float = 0.0, back: float = 0.0, taper: float = 0.0):
        """A box with optional shaping: `slope` lowers the top at the front (+x) edge, `back` lowers it at the rear, `taper`
        pulls the top's side edges inward (a hull whose sides lean in)."""
        x0, x1, y0, y1, z0, z1 = x, x + w, y, y + d, z, z + h
        t = taper
        v = [
            (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0 + t, z1 - back), (x1, y0 + t, z1 - slope), (x1, y1 - t, z1 - slope), (x0, y1 - t, z1 - back),
        ]
        # vertices 0..3 bottom (x0y0, x1y0, x1y1, x0y1), 4..7 top
        f = [[4, 5, 6, 7], [0, 3, 2, 1], [1, 2, 6, 5], [3, 0, 4, 7], [0, 1, 5, 4], [2, 3, 7, 6]]
        # top, bottom, front (+x), back (-x), left (-y), right (+y); winding fixed by _orient below
        p = Part(v, f, mat, shade)
        self._orient(p)
        self.parts.append(p)
        return p

    def prism(self, cx, cy, z, r, h, mat, shade=None, sides: int = 10, ry: float | None = None, taper: float = 0.0):
        """A round column (turret, drum, tower): `sides` faces, radius r (ry for an oval), top taper pulls the top ring in."""
        ry = r if ry is None else ry
        v, f = [], []
        for i in range(sides):
            a = 2 * math.pi * i / sides
            v.append((cx + r * math.cos(a), cy + ry * math.sin(a), z))
        for i in range(sides):
            a = 2 * math.pi * i / sides
            v.append((cx + (r - taper) * math.cos(a), cy + (ry - taper) * math.sin(a), z + h))
        f.append(list(range(sides, 2 * sides)))
        f.append(list(range(sides - 1, -1, -1)))
        for i in range(sides):
            j = (i + 1) % sides
            f.append([i, j, sides + j, sides + i])
        p = Part(v, f, mat, shade)
        self._orient(p)
        self.parts.append(p)
        return p

    def cone(self, cx, cy, z, r, h, mat, shade=None, sides: int = 8):
        """A pointed roof or nose cone."""
        v = [(cx + r * math.cos(2 * math.pi * i / sides), cy + r * math.sin(2 * math.pi * i / sides), z) for i in range(sides)]
        v.append((cx, cy, z + h))
        f = [list(range(sides - 1, -1, -1))]
        for i in range(sides):
            f.append([i, (i + 1) % sides, sides])
        p = Part(v, f, mat, shade)
        self._orient(p)
        self.parts.append(p)
        return p

    def roof(self, x, y, z, w, d, h, mat, shade=None, ridge_x: bool = True):
        """A gabled roof: a prism with a ridge along x (or y) at height h."""
        x0, x1, y0, y1 = x, x + w, y, y + d
        if ridge_x:
            ym = (y0 + y1) / 2
            v = [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z), (x0, ym, z + h), (x1, ym, z + h)]
            f = [[0, 1, 5, 4], [3, 4, 5, 2], [0, 4, 3], [1, 2, 5], [0, 3, 2, 1]]
        else:
            xm = (x0 + x1) / 2
            v = [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z), (xm, y0, z + h), (xm, y1, z + h)]
            f = [[0, 1, 4], [3, 5, 2], [0, 4, 5, 3], [1, 2, 5, 4], [0, 3, 2, 1]]
        p = Part(v, f, mat, shade)
        self._orient(p)
        self.parts.append(p)
        return p

    def loft(self, bottom, top, z, h, mat, shade=None):
        """Two outlines of the same number of points, `bottom` at height z and `top` at z + h (each a list of (x, y) in order
        round the shape), joined by side faces; both ends are closed. A hull is a loft: a pointed plan view at the waterline
        opening out to the deck, or one outline for a straight-sided extrusion (pass the same list twice)."""
        n = len(bottom)
        assert n == len(top) and n >= 3
        v = [(x, y, z) for (x, y) in bottom] + [(x, y, z + h) for (x, y) in top]
        f = [list(range(n, 2 * n)), list(range(n - 1, -1, -1))]
        for i in range(n):
            j = (i + 1) % n
            f.append([i, j, n + j, n + i])
        p = Part(v, f, mat, shade)
        self._orient(p)
        self.parts.append(p)
        return p

    def extrude(self, outline, z, h, mat, shade=None):
        return self.loft(outline, outline, z, h, mat, shade)

    def pole(self, x, y, z, h, mat, shade=None, t: float = 0.7):
        return self.box(x - t / 2, y - t / 2, z, t, t, h, mat, shade)

    def decal(self, x, y, z, pts, mat="dark", shade=1):
        """A flat mark lying on a horizontal surface at (x, y, z): pts are (dx, dy) cells of 1 unit."""
        self.decals.append((x, y, z, pts, mat, shade))

    def _orient(self, p: Part):
        """Make every face counter-clockwise seen from outside, using the part's centre. The face normal comes from Newell's
        method, so concave polygons (a ship's plan view) orient correctly."""
        for fi, face in enumerate(p.faces):
            vs = [p.verts[i] for i in face]
            n = [0.0, 0.0, 0.0]
            for i in range(len(vs)):
                x0, y0, z0 = vs[i]
                x1, y1, z1 = vs[(i + 1) % len(vs)]
                n[0] += (y0 - y1) * (z0 + z1)
                n[1] += (z0 - z1) * (x0 + x1)
                n[2] += (x0 - x1) * (y0 + y1)
            fc = tuple(sum(v[k] for v in vs) / len(vs) for k in range(3))
            out = _sub(fc, p.centre)
            if _dot(tuple(n), out) < 0:
                p.faces[fi] = list(reversed(face))

    # ------------------------------------------------------------ damage
    def _bounds(self):
        xs = [v[0] for p in self.parts for v in p.verts]
        ys = [v[1] for p in self.parts for v in p.verts]
        zs = [v[2] for p in self.parts for v in p.verts]
        return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)

    @staticmethod
    def _lowered(p: Part, zmin: float, frac: float) -> Part:
        verts = [(x, y, zmin + (z - zmin) * frac) if z > zmin else (x, y, z) for (x, y, z) in p.verts]
        q = Part(verts, [list(f) for f in p.faces], p.mat, p.shade)
        q.dim = p.dim
        return q

    def damaged(self, level: int) -> "Model":
        """A copy of the model in a damage state: 1 scorched and smoking, 2 broken (parts gone, the rest slumped, rubble),
        3 a ruin (stubs of the ground floor and rubble). Deterministic per model and level; no faction emblem."""
        m = Model(self.name + f"#d{level}", self.w, self.h, self.scale, self.ground_y, self.shadow)
        rnd = random.Random(sum(map(ord, self.name)) * 31 + level)
        x0, x1, y0, y1, z0, z1 = self._bounds()
        for i, p in enumerate(self.parts):
            ground = min(v[2] for v in p.verts) <= z0 + 1.0
            if level == 1:
                q = Model._lowered(p, z0, 1.0)
                q.dim = 1 if i % 3 == 0 else 0
            elif level == 2:
                if not ground and i % 3 == 1:
                    continue                                   # blown away
                q = Model._lowered(p, z0, 0.55 if not ground else 0.8)
                q.dim = 1 if i % 2 == 0 else 2
            else:
                if not ground:
                    continue
                q = Model._lowered(p, z0, 0.22)
                q.dim = 2
            m.parts.append(q)
        def rubble(n, hmax):
            for _ in range(n):
                cx = rnd.uniform(x0 * 0.85, x1 * 0.85)
                cy = rnd.uniform(y0 * 0.85, y1 * 0.85)
                w, d, h = rnd.uniform(1.5, 4.5), rnd.uniform(1.5, 4.5), rnd.uniform(0.8, hmax)
                m.box(cx - w / 2, cy - d / 2, z0, w, d, h, rnd.choice(["concrete", "stone", "dark", "iron", "wood"]), rnd.choice([1, 2, 3]))
        def smoke(n, base):
            for k in range(n):
                cx = rnd.uniform(x0 * 0.5, x1 * 0.5)
                cy = rnd.uniform(y0 * 0.5, y1 * 0.5)
                for s in range(4):
                    r = 1.6 + s * 0.5
                    m.box(cx - r / 2 + rnd.uniform(-0.7, 0.7), cy - r / 2 + rnd.uniform(-0.7, 0.7), base + s * 3.0, r, r, 2.6, "smoke", min(3, 1 + s // 2))
        def fire(n, base):
            for _ in range(n):
                cx = rnd.uniform(x0 * 0.6, x1 * 0.6)
                cy = rnd.uniform(y0 * 0.6, y1 * 0.6)
                m.box(cx - 0.8, cy - 0.8, base, 1.6, 1.6, 2.2, "fire", 1)
        top = z0 + (z1 - z0) * (1.0 if level == 1 else 0.55)
        if level == 1:
            fire(2, top - 1.0)
            smoke(1, top + 1.0)
            rubble(3, 1.6)
        elif level == 2:
            fire(3, z0 + 1.0)
            smoke(2, z0 + (z1 - z0) * 0.5)
            rubble(8, 2.6)
        else:
            rubble(12, 2.2)
            fire(1, z0 + 0.6)
            smoke(1, z0 + 2.0)
        return m

    # ------------------------------------------------------------ render
    def project(self, p, yaw):
        x, y, z = p
        c, s = math.cos(yaw), math.sin(yaw)
        rx, ry = x * c - y * s, x * s + y * c
        # the game's view: rotate then squash y; here the screen axes are (rx - ry) and (rx + ry) at 45 degrees
        sx = (rx - ry) * 0.7071 * self.scale
        sy = (rx + ry) * 0.7071 * 0.5 * self.scale - z * Z_SCALE * self.scale
        return (self.w / 2 + sx, self.h * self.ground_y + sy), (rx + ry)

    def render(self, yaw: float = 0.0, mark_fn=None):
        """Returns {(x, y): (material, shade) | 'O' | 'S'} for one facing."""
        c, s = math.cos(yaw), math.sin(yaw)
        order = []
        for p in self.parts:
            cx, cy, cz = p.centre
            rx, ry = cx * c - cy * s, cx * s + cy * c
            order.append((rx + ry + cz * 0.25, cz, p))
        order.sort(key=lambda t: (round(t[0], 3), t[1]))
        buf: dict[tuple[int, int], tuple] = {}
        pid = 0
        for _, _, part in order:
            pid += 1
            faces = []
            for face in part.faces:
                pts3 = [part.verts[i] for i in face]
                scr = [self.project(v, yaw)[0] for v in pts3]
                area = sum(scr[i][0] * scr[(i + 1) % len(scr)][1] - scr[(i + 1) % len(scr)][0] * scr[i][1] for i in range(len(scr))) / 2
                if area <= 0.01:      # back face (screen y points down, so visible faces wind clockwise: positive area)
                    continue
                n = _face_normal(pts3, yaw)
                depth = sum(self.project(v, yaw)[1] for v in pts3) / len(pts3)
                faces.append((depth, scr, n))
            faces.sort(key=lambda t: t[0])
            for _, scr, n in faces:
                shade = part.shade if part.shade is not None else _shade(n)
                shade = min(3, shade + part.dim)
                for (px, py) in _raster(scr, self.w, self.h):
                    buf[(px, py)] = (part.mat, shade, pid)
        for (x, y, z, pts, mat, shade) in self.decals:
            for dx, dy in pts:
                (sx, sy), _ = self.project((x + dx, y + dy, z), yaw)
                for (px, py) in ((int(sx), int(sy)), (int(sx) + 1, int(sy))):
                    if (px, py) in buf:
                        buf[(px, py)] = (mat, shade, 9999)
        out = {k: (v[0], v[1]) for k, v in buf.items()}
        if self.mark_at:
            # The emblem lies on a horizontal surface: each of its cells is projected as a small square, so it turns with the
            # unit and sits on the turret instead of floating over it as a flat badge.
            mx, my, mz = self.mark_at
            s = 1.55 * self.mark_scale
            cells = set()
            for i, j in kit.EMBLEM["pts"]:
                quad = [self.project((mx + (i - 1.5 + dx) * s, my + (j - 1.5 + dy) * s, mz), yaw)[0] for dx, dy in ((0, 0), (1, 0), (1, 1), (0, 1))]
                cells.update(_raster(quad, self.w, self.h))
            if kit.EMBLEM.get("halo"):
                ring = {(a + dx, b + dy) for a, b in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - cells
                for (hx, hy) in ring:
                    if 0 <= hx < self.w and 0 <= hy < self.h and (hx, hy) in out:
                        out[(hx, hy)] = ("dark", 3)
            for (px, py) in cells:
                if 0 <= px < self.w and 0 <= py < self.h:
                    out[(px, py)] = (kit.EMBLEM["mat"], SHADES.index(kit.EMBLEM["shade"]))
        # outline
        for (x, y) in list(out):
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < self.w and 0 <= ny < self.h and (nx, ny) not in out:
                    out[(nx, ny)] = "O"
        if self.shadow:
            (gx, gy), _ = self.project((0, 0, 0), yaw)
            ext = max(max(abs(v[0]) for p in self.parts for v in p.verts), max(abs(v[1]) for p in self.parts for v in p.verts))
            rx, ry = ext * 1.0 * self.scale * self.shadow, ext * 0.5 * self.scale * self.shadow
            for j in range(self.h):
                for i in range(self.w):
                    if ((i + .5 - gx) / max(rx, 1)) ** 2 + ((j + .5 - gy) / max(ry, 1)) ** 2 <= 1.0 and (i, j) not in out:
                        out[(i, j)] = "S"
        return out


# ---------------------------------------------------------------- geometry helpers
def _sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def _dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def _cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _face_normal(pts3, yaw):
    a, b, c = pts3[0], pts3[1], pts3[2]
    n = _cross(_sub(b, a), _sub(c, a))
    n = _norm(n)
    co, si = math.cos(yaw), math.sin(yaw)
    rx, ry = n[0] * co - n[1] * si, n[0] * si + n[1] * co
    # to the screen-aligned frame: x right = (rx - ry)/sqrt2, y toward viewer = (rx + ry)/sqrt2
    return ((rx - ry) * 0.7071, (rx + ry) * 0.7071, n[2])


def _shade(n):
    d = _dot(n, LIGHT)
    return 0 if d > 0.72 else 1 if d > 0.38 else 2 if d > 0.0 else 3


def _raster(scr, w, h):
    xs = [p[0] for p in scr]
    ys = [p[1] for p in scr]
    cells = []
    for j in range(max(0, int(math.floor(min(ys)))), min(h, int(math.ceil(max(ys))) + 1)):
        for i in range(max(0, int(math.floor(min(xs)))), min(w, int(math.ceil(max(xs))) + 1)):
            if _inside(i + 0.5, j + 0.5, scr):
                cells.append((i, j))
    return cells


def _inside(px, py, pts):
    hit, j = False, len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
            hit = not hit
        j = i
    return hit


def facings(model: Model, n: int = 16, mark_fn=None):
    """One baked frame per facing; facing k looks along yaw = 2 pi k / n."""
    return [model.render(2 * math.pi * k / n, mark_fn) for k in range(n)]
