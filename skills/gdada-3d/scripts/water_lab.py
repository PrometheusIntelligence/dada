#!/usr/bin/env python3
"""water_lab.py: a workbench for stylised water in a 16-colour, low-resolution game (GDADA 3D / 2D art tool).

Renders a sea band in several styles on a given palette, writes a contact sheet PNG and prints MEASURES, so water is judged by numbers
as well as by eye (the owner's complaint that started this tool: "water nowhere near enough detail").

  python3 water_lab.py --out water.png                     # all styles on the Last Frequency palette
  python3 water_lab.py --style hokusai --seed 3 --out a.png --size 640x200
  python3 water_lab.py --check hokusai --min-detail 40     # exit 1 when a style falls under the floors

Styles: flat (the old: one fill and dashes), scallop (seigaiha rows, one size per row), layered (depth bands with colour steps and haze),
hokusai (layered + swell lines + crest curls with claw foam + foam lace + glitter + island + wake).  The port to a game is the recipe printed with
--recipe: counts and tones per depth band, which the game draws with its own primitives (HolyC: Sea() and WSea() in Last Frequency).

MEASURES (all on the finished image):
  tones        distinct palette entries used (target 6+ of the sea's family)
  edges/row    mean colour changes along a row (detail; the flat sea is under 6)
  rows_unique  share of rows that differ from the row above (a flat sea is near 0)
  tile_repeat  strongest horizontal self-similarity at a shift of 16..160 px (1.0 = wallpaper; target under 0.55)
  depth_grad   ratio of feature size near the bottom to near the horizon (perspective; target 1.8 and up)
"""
import argparse, math, random, sys
from PIL import Image, ImageDraw

PAL = [(20,14,28),(36,30,84),(30,78,104),(156,152,184),(240,228,200),(244,170,52),(200,64,64),(64,176,176),
       (150,84,40),(86,74,122),(206,186,156),(255,246,222),(110,200,100),(150,96,206),(52,30,78),(132,52,56)]
INK,NAVY,OCEAN,FOG,CREAM,AMBER,RED,FOAM,BRASS,FOGD,PAPER,CREAMHI,GREEN,WET,DEEP,REDD = range(16)

def arc(d, cx, cy, r, c, th=1, flat=0.5):
    """an upper half-ellipse arc, drawn as points so it stays crisp (no antialias)"""
    for a in range(0, 181, 3):
        x = cx - r*math.cos(math.radians(a)); y = cy - r*flat*math.sin(math.radians(a))
        x = int(round(x)); y = int(round(y)); d.rectangle([x, y, x+th-1, y+th-1], fill=c)

def scallop(d, cx, cy, r, fill, edge, flat=0.5):
    pts = [(cx - r*math.cos(math.radians(a)), cy - r*flat*math.sin(math.radians(a))) for a in range(0, 181, 12)]
    d.polygon(pts + [(cx + r, cy+1), (cx - r, cy+1)], fill=fill)
    arc(d, cx, cy, r, edge, 1, flat)

def band_t(y, h, y0):
    """0 at the horizon, 1 at the bottom of the image"""
    return (y - y0) / max(1, h - y0)

def style_flat(img, rnd, hz):
    d = ImageDraw.Draw(img); W, H = img.size
    d.rectangle([0, hz, W, H], fill=OCEAN)
    for i in range(12):
        x = (i*97) % 700 - 40; d.rectangle([x, hz+8+i*9, x+70+i*5, hz+9+i*9], fill=FOGD)

def style_scallop(img, rnd, hz):
    d = ImageDraw.Draw(img); W, H = img.size
    d.rectangle([0, hz, W, H], fill=OCEAN); d.rectangle([0, hz, W, hz+2], fill=CREAM); d.rectangle([0, hz+3, W, hz+10], fill=WET)
    for r in range(9):
        sc = 8 + r*3; yy = hz + 12 + r*r*2 + r*7
        for c in range(-1, W//(sc*2)+2):
            scallop(d, c*sc*2 + (r % 2)*sc, yy, sc, WET if r % 2 == 0 else OCEAN, FOAM)

def style_layered(img, rnd, hz, hokusai=False):
    d = ImageDraw.Draw(img); W, H = img.size
    # depth bands: haze at the horizon, then steps toward the viewer; each band has its own tone and its own feature size
    bands = [(0.00, FOGD), (0.05, WET), (0.14, DEEP), (0.30, OCEAN), (0.55, NAVY), (0.80, OCEAN)]
    for i, (t0, col) in enumerate(bands):
        y0 = hz + int(t0*(H-hz)); y1 = hz + int((bands[i+1][0] if i+1 < len(bands) else 1.0)*(H-hz))
        d.rectangle([0, y0, W, y1], fill=col)
    d.rectangle([0, hz, W, hz], fill=CREAM)
    # swell lines: long low curves, wider and further apart toward the viewer, in the next tone up
    for k in range(26):
        t = (k/26.0)**1.7; y = hz + 3 + int(t*(H-hz-6)); L = int(30 + 220*t); x = rnd.randint(-L//2, W-L//2)
        col = FOG if t < 0.3 else (WET if t < 0.7 else FOAM)
        for xx in range(x, x+L, 2):
            yy = y - int(math.sin((xx-x)/L*math.pi)*(1+3*t)); d.rectangle([xx, yy, xx+1, yy], fill=col)
    # scallop crests, larger and sparser toward the viewer, alternate rows offset, a foam edge only on the lit side
    rows = 11
    for r in range(rows):
        t = (r/(rows-1.0))**1.5; yy = hz + 8 + int(t*(H-hz-14)); sc = 5 + int(30*t)
        base = WET if r % 2 == 0 else OCEAN
        if t > 0.6: base = DEEP if r % 2 == 0 else NAVY
        for c in range(-1, W//(sc*2)+2):
            jitter = rnd.randint(-sc//3, sc//3) if hokusai else 0
            x = c*sc*2 + (r % 2)*sc + jitter
            scallop(d, x, yy, sc, base, FOAM if t > 0.15 else FOG)
            if hokusai and t > 0.35 and rnd.random() < 0.5:
                d.rectangle([int(x-sc*0.4), int(yy-sc*0.2), int(x+sc*0.3), int(yy-sc*0.2)+1], fill=CREAMHI)

def crest(d, cx, cy, s, rnd):
    """a Hokusai crest: a tall curling wave with a flat dark underside, a ring of claw fingers, foam dots"""
    pts = [(cx - s, cy)]
    for a in range(0, 200, 10):
        pts.append((cx - s + s*1.1*(a/200.0)*1.6 + math.sin(math.radians(a))*s*0.2,
                    cy - s*0.9*math.sin(math.radians(a*0.9))))
    pts += [(cx + s*0.8, cy - s*0.15), (cx + s*0.9, cy)]
    d.polygon(pts, fill=OCEAN); d.line(pts, fill=INK, width=1)
    for k in range(6):                      # claw fingers hanging from the lip
        fx = cx + s*0.1 + k*s*0.14; fy = cy - s*0.8 + abs(k-2.5)*s*0.05
        d.polygon([(int(fx), int(fy)), (int(fx+s*0.06), int(fy+s*0.18)), (int(fx-s*0.06), int(fy+s*0.16))], fill=CREAMHI)
    for k in range(9):
        px_, py_ = int(cx + rnd.randint(-s//2, s)), int(cy - s*0.9 + rnd.randint(-s//5, s//2)); d.rectangle([px_, py_, px_+1, py_+1], fill=CREAM)

def finish_hokusai(img, rnd, hz):
    d = ImageDraw.Draw(img); W, H = img.size
    # foam lace: thin broken curves under every crest row near the viewer
    for k in range(40):
        t = rnd.random()**0.6; y = hz + 6 + int(t*(H-hz-8)); x = rnd.randint(0, W); L = int(8 + 40*t)
        for xx in range(x, x+L, 3):
            d.rectangle([xx, y + int(math.sin(xx*0.4)*1.2), xx+1, y + int(math.sin(xx*0.4)*1.2)], fill=CREAM)
    # moon glitter path: short bars narrowing toward the horizon, jittered
    mx = int(W*0.68)
    for q in range(10):
        t = (q/10.0)**1.3; y = hz + 4 + int(t*(H-hz)*0.55); w = 3 + int(24*t); x = mx + rnd.randint(-6, 6) - w//2
        d.rectangle([x, y, x+w, y+1 + (1 if t > 0.5 else 0)], fill=CREAMHI)
    # far island with a shrine roof, ink on the haze, and a small lit window
    ix = int(W*0.14)
    d.polygon([(ix, hz), (ix+40, hz-14), (ix+75, hz-6), (ix+110, hz)], fill=INK)
    d.polygon([(ix+36, hz-14), (ix+44, hz-26), (ix+52, hz-14)], fill=INK)
    d.line([(ix+34, hz-14), (ix+54, hz-14)], fill=INK, width=2)
    d.rectangle([ix+42, hz-17, ix+45, hz-14], fill=AMBER)
    # one big crest in the near water, and a small boat's wake
    crest(d, int(W*0.3), hz + int((H-hz)*0.85), 64, rnd)
    wx, wy = int(W*0.52), hz + 24
    d.polygon([(wx-3, wy), (wx+8, wy), (wx+8, wy-3)], fill=INK)
    for k in range(1, 6): d.line([(wx-4-k*5, wy+1+k//2), (wx-8-k*7, wy+2+k//2)], fill=CREAMHI)

STYLES = {"flat": lambda i, r, h: style_flat(i, r, h), "scallop": lambda i, r, h: style_scallop(i, r, h),
          "layered": lambda i, r, h: style_layered(i, r, h, False),
          "hokusai": lambda i, r, h: (style_layered(i, r, h, True), finish_hokusai(i, r, h))}

def render(style, seed, size):
    W, H = size; rnd = random.Random(seed); hz = int(H*0.12)
    img = Image.new("P", (W, H), FOGD); img.putpalette([c for p in PAL for c in p] + [0]*(768-48))
    d = ImageDraw.Draw(img); d.rectangle([0, 0, W, hz], fill=NAVY)     # the sky strip above the horizon
    for k in range(14): d.rectangle([rnd.randint(0, W), rnd.randint(0, hz-3)]*2, fill=CREAM)
    STYLES[style](img, rnd, hz)
    return img, hz

def measure(img, hz):
    W, H = img.size; px = img.load(); rows = [[px[x, y] for x in range(W)] for y in range(hz+1, H)]
    tones = len(set(v for r in rows for v in r))
    edges = sum(sum(1 for x in range(1, W) if r[x] != r[x-1]) for r in rows)/len(rows)
    uniq = sum(1 for i in range(1, len(rows)) if rows[i] != rows[i-1])/(len(rows)-1)
    best = 0.0   # edge-position self-similarity: how much of a row's edge pattern recurs at some shift (1.0 = tiled wallpaper)
    for r in rows[::4]:
        E = {x for x in range(1, W) if r[x] != r[x-1]}
        if len(E) < 6: continue
        for sh in range(16, 161, 2):
            best = max(best, len({x for x in E if (x+sh) in E})/len(E))
    # feature size by depth: mean run length of equal colour near the horizon (top fifth) and near the bottom (last fifth)
    def run(rr):
        n = 0; tot = 0
        for r in rr:
            c = 1
            for x in range(1, W):
                if r[x] == r[x-1]: c += 1
                else: tot += c; n += 1; c = 1
        return tot/max(1, n)
    k = max(1, len(rows)//5); depth = run(rows[-k:])/max(0.5, run(rows[:k]))
    return {"tones": tones, "edges/row": round(edges, 1), "rows_unique": round(uniq, 2), "tile_repeat": round(best, 2), "depth_grad": round(depth, 2)}

RECIPE = """RECIPE (hokusai), per depth band t = 0 (horizon) .. 1 (viewer); port with the game's own primitives, never copy pixels:
  bands      6 colour steps: FOGD haze 0-5%, WET 5-14%, DEEP 14-30%, OCEAN 30-55%, NAVY 55-80%, OCEAN 80-100%; a cream horizon line
  swell      26 long curves, y = t^1.7, length 30..250 px, tone FOG (far) / WET / FOAM (near), 1-4 px sag
  crests     11 scallop rows, y = t^1.5, half-width 5..35 px, alternate rows offset by half, +-1/3 jitter, foam edge on the arc, cream dash on t>0.35
  foam lace  40 broken curves, 8..48 px, cream, more of them near the viewer
  glitter    10 bars under the moon, 3..27 px wide, +-6 px jitter per bar and per 8 ticks (animate by tick, never by random)
  island     ink hump on the haze, a roof and one lit window; a crest 64 px tall with 6 claw fingers in the near water; a boat wake of 5 chevrons
  cost       about 450 polygon+line calls for a full-width band: draw the glass band (a window) with a third of that, scaled by width
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--style"); ap.add_argument("--seed", type=int, default=1); ap.add_argument("--out", default="water.png")
    ap.add_argument("--size", default="640x200"); ap.add_argument("--recipe", action="store_true")
    ap.add_argument("--check"); ap.add_argument("--min-detail", type=float, default=40.0)
    a = ap.parse_args(); W, H = map(int, a.size.split("x"))
    if a.recipe: print(RECIPE); return
    names = [a.style] if a.style else (list(STYLES) if not a.check else [a.check]); sheet = Image.new("RGB", (W, (H+4)*len(names)), (0, 0, 0)); bad = False
    for i, n in enumerate(names):
        img, hz = render(n, a.seed, (W, H)); m = measure(img, hz)
        print(f"{n:9s} " + "  ".join(f"{k}={v}" for k, v in m.items()))
        sheet.paste(img.convert("RGB"), (0, i*(H+4)))
        if a.check and (m["edges/row"] < a.min_detail or m["tile_repeat"] > 0.55 or m["tones"] < 6 or m["depth_grad"] < 1.8): bad = True
    sheet.save(a.out)
    if a.check and bad: print("CHECK FAIL: under the detail floors"); sys.exit(1)

if __name__ == "__main__": main()
