#!/usr/bin/env python3
"""GDADA sprite tool: bake a roster for every faction, validate it, write one JSON file and contact sheets.

    python3 build.py --roster example --out art/units.json [--factions example/factions.json] [--sheet DIR]

--roster DIR holds units.py and buildings.py, each exposing ERAS = {era: {kind: fn}}; unit fns take a `phase`
(0 or 1: the two walk poses), building fns take nothing, and buildings.py also exposes scaffold(size). Units and
buildings call kit.mark(s, x, y) on a team-coloured surface; buildings draw banners with kit.FLAG shapes.
--factions is a JSON file of {defaults, factions: {id: {name, blurb, main, dark, tone, emblem, flag}}}.
Exit status is 1 if any validation fails. Thresholds live in validate.py: change them only with a measured reason,
and log it.
"""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
def _arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default
ROSTER = os.path.abspath(_arg("--roster", os.path.join(HERE, "example")))
sys.path.insert(0, ROSTER)
import kit, units, buildings, props
import validate as V



def team_ramp(main, dark):
    lift = .5 if V.luminance(main) >= .25 else .3          # dark factions keep a calmer highlight (emblem contrast)
    def mix(a, b, t): return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(kit.hex_rgb(a), kit.hex_rgb(b)))
    return [mix(main, "#ffffff", lift), main, dark, mix(dark, "#000000", .45)]


def render(rows, team, scale=1):
    w, h = len(rows[0]), len(rows)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ramp = team_ramp(*team)
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c == ".": continue
            if c == "O": col = kit.hex_rgb(kit.INK) + (255,)
            elif c == "S": col = (0, 0, 0, 70)
            else:
                m, s = kit.LEGEND[c]
                col = kit.hex_rgb(ramp[s] if m == "team" else kit.MATERIALS[m][s]) + (255,)
            img.putpixel((x, y), col)
    return img.resize((w * scale, h * scale), Image.NEAREST) if scale > 1 else img


def bake(sp):
    return kit.rows(sp.bake(), sp.w, sp.h)


def load_factions():
    return json.load(open(os.path.abspath(_arg("--factions", os.path.join(ROSTER, "factions.json")))))


def bake_faction(fid, f, fail, validate_all=True):
    """Bakes every unit, building and scaffold for one faction (its emblem and flag shape)."""
    kit.EMBLEM = {"pts": kit.EMBLEMS[f["emblem"]], "mat": "dark" if f["tone"] == "light" else "cloth",
                  "shade": "mid" if f["tone"] == "light" else "hi", "halo": f["tone"] == "dark"}
    kit.FLAG = f["flag"]
    eras, blds = {}, {}
    for era, roster in units.ERAS.items():
        eras[era] = {}
        for kind, fn in roster.items():
            fr = [bake(fn(0)), bake(fn(1))]
            eras[era][kind] = fr
            th = V.UNIT_BIG if len(fr[0]) > 16 else V.UNIT
            if validate_all:
                for m in V.validate(era, kind, fr[0], th): fail(m)
                for m in V.validate(era, kind, fr[1], th, 1): fail(m)
                for m in V.frame_pair(era, kind, fr[0], fr[1]): fail(m)
        if validate_all:
            for m in V.silhouette_pairs(era, {k: v[0] for k, v in eras[era].items()}, V.UNIT["min_xor"]): fail(m)
    for era, roster in buildings.ERAS.items():
        blds[era] = {}
        for kind, fn in roster.items():
            r = bake(fn())
            blds[era][kind] = r
            if validate_all:
                for m in V.validate(era, kind, r, V.BUILDING): fail(m)
        if validate_all:
            for size in (2, 3):
                same = {k: v for k, v in blds[era].items() if len(v) == size * 16}
                for m in V.silhouette_pairs(era, same, V.BUILDING["min_xor"]): fail(m)
    for size in (2, 3):
        blds["scaffold%d" % size] = bake(buildings.scaffold(size))
    # A site shows what is being built: the scaffold with a solid ghost of the finished building.
    for era in buildings.ERAS:
        for kind, rows in list(blds[era].items()):
            frame = blds["scaffold%d" % (len(rows) // 16)]
            ghost = []
            for y, row in enumerate(rows):
                line = ""
                for x, c in enumerate(row):
                    fch = frame[y][x]
                    post = fch != "." and kit.LEGEND.get(fch, ["", 0])[0] == "wood"      # posts stay, rails give way
                    body = c not in ".OS"
                    if post:
                        line += fch
                    elif body:                                  # roofline in full colour, lower half dimmed
                        m, sh = kit.LEGEND[c]
                        line += c if y < len(rows) * 0.5 else kit._REV[(m, min(sh + 1, 3))]
                    else:
                        line += fch if fch != "." else "."
                ghost.append(line)
            blds[era]["scaffold:" + kind] = ghost
    return eras, blds


def cells_differing(a, b):
    return sum(1 for ra, rb in zip(a, b) for ca, cb in zip(ra, rb) if ca != cb)


def main():
    fdata = load_factions()
    facs = fdata["factions"]
    out = {"format": "tidewatch.sprites", "formatVersion": 4, "size": kit.SIZE, "ink": kit.INK,
           "materials": kit.MATERIALS, "legend": kit.LEGEND, "defaults": fdata["defaults"], "factions": {}}
    bad = 0
    def fail(m):
        nonlocal bad
        print("FAIL", m); bad += 1
    first = True
    for fid, f in facs.items():
        eras, blds = bake_faction(fid, f, fail, validate_all=first)
        first = False
        out["factions"][fid] = {"name": f["name"], "blurb": f.get("blurb", ""), "main": f["main"], "dark": f["dark"], "tone": f["tone"],
                                "emblem": f["emblem"], "flag": f["flag"], "eras": eras, "buildings": blds}
    for m in V.factions_ok(facs): fail(m)
    out["props"] = {}
    for name, fn in props.ROSTER.items():
        rows = bake(fn())
        out["props"][name] = rows
        for m in V.validate("props", name, rows, dict(min_team_px=0, min_team_share=0.0, min_fill=20, max_fill_share=0.8, min_xor=0.0)): fail(m)
    # every sprite must carry its faction's mark: any two factions with different emblem or flag differ on every unit and building
    ids = list(facs)
    base = out["factions"][ids[0]]
    for other in ids[1:]:
        o = out["factions"][other]
        for era, roster in base["eras"].items():
            for kind, fr in roster.items():
                d = cells_differing(fr[0], o["eras"][era][kind][0])
                if d < 3: fail(f"{era}/{kind}: {ids[0]} and {other} differ by only {d} px; the faction mark is missing")
        for era in buildings.ERAS:
            for kind, rows in base["buildings"][era].items():
                if kind.startswith("scaffold:"): continue
                d = cells_differing(rows, o["buildings"][era][kind])
                if d < 3: fail(f"{era}/{kind}: {ids[0]} and {other} differ by only {d} px; the faction mark is missing")
    path = os.path.abspath(_arg("--out", "sprites.json"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, "w"), separators=(",", ":"))
    print("wrote", path, "-", len(out["factions"]), "factions,", bad, "problems,", os.path.getsize(path) // 1024, "KB")
    if "--sheet" in sys.argv:
        d = _arg("--sheet"); os.makedirs(d, exist_ok=True)
        pad, bg = 6, (96, 120, 72, 255)
        for era in units.ERAS:
            kinds = list(out["factions"][ids[0]]["eras"][era])
            sc = 5
            cell = 24 * sc + pad
            sheet = Image.new("RGBA", (pad + len(kinds) * cell, pad + len(ids) * cell), bg)
            for fi, fid in enumerate(ids):
                fa = out["factions"][fid]
                for ki, kind in enumerate(kinds):
                    sheet.alpha_composite(render(fa["eras"][era][kind][0], (fa["main"], fa["dark"]), sc), (pad + ki * cell, pad + fi * cell))
            sheet.save(os.path.join(d, f"units-{era}.png"))
            bk = [k for k in out["factions"][ids[0]]["buildings"][era] if not k.startswith("scaffold:")]
            sc = 3
            show = [ids[0], ids[3]] if len(ids) > 3 else ids
            sheet = Image.new("RGBA", (pad + len(bk) * (48 * sc + pad), pad + len(show) * (48 * sc + pad)), bg)
            for fi, fid in enumerate(show):
                fa = out["factions"][fid]
                for ki, kind in enumerate(bk):
                    sheet.alpha_composite(render(fa["buildings"][era][kind], (fa["main"], fa["dark"]), sc), (pad + ki * (48 * sc + pad), pad + fi * (48 * sc + pad)))
            sheet.save(os.path.join(d, f"buildings-{era}.png"))
        print("sheets in", d)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
