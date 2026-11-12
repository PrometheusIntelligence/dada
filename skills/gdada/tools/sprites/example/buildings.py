"""The Tidewatch buildings, drawn with kit.py in the same style as the units.

Size 2 buildings are 32x32 px, size 3 are 48x48. Front elevation, light from the top left.
Every building carries team colour somewhere big (banner, shutters, stripe, door) and has a
silhouette distinct from the others of its size.
"""
import kit
from kit import Sprite, mark


def B(name, size):
    px = size * 16
    return Sprite(name, shadow=(px / 2 + 1.5, px - 1.6, px / 2 - 1, 2.6), w=px, h=px)


# ------------------------------------------------------------------ helpers
def courses(s, x, y, w, h, mat="stone", every=5):
    """Masonry or plank joints: a darker line every few rows, with offset vertical joints."""
    for i, yy in enumerate(range(y + every - 1, y + h - 1, every)):
        s.rect(x + 1, yy, w - 2, 1, mat, "lo")
        for xx in range(x + 3 + (i % 2) * 4, x + w - 2, 8):
            s.dots([(xx, yy + 1), (xx, yy + 2), (xx, yy + 3)], mat, "lo")


def planks(s, x, y, w, h, mat="wood", gap=4):
    for xx in range(x + gap, x + w - 1, gap):
        s.rect(xx, y + 1, 1, h - 2, mat, "lo")


def arch_door(s, x, y, w, h, mat="dark", frame="wood"):
    s.rect(x - 1, y - 1, w + 2, h + 1, frame)
    s.rect(x, y + 1, w, h - 1, mat)
    s.poly([(x, y + 1), (x + 1, y - 1), (x + w - 1, y - 1), (x + w, y + 1)], mat)


def flag(s, x, top, length, w=8, h=5):
    """A banner on a pole. Its shape (square, swallowtail, pennant) and emblem belong to the faction."""
    s.line(x, top, x, top + length, "wood")
    x0, x1 = x + 1, x + 1 + w
    if kit.FLAG == "swallow":
        s.poly([(x0, top), (x1, top), (x1 - 2, top + h / 2), (x1, top + h), (x0, top + h)], "team")
    elif kit.FLAG == "pennant":
        s.poly([(x0, top), (x1, top + h / 2), (x0, top + h)], "team")
    else:
        s.rect(x0, top, w, h, "team")
    if w >= 7 and h >= 5:
        mark(s, x0 + 1, top + 1)


def hip_roof(s, x0, x1, top_y, base_y, inset, mat, line_mat=None, step=3):
    """Trapezoid roof: eave from x0..x1 at base_y, ridge inset px narrower each side at top_y."""
    s.poly([(x0, base_y), (x0 + inset, top_y), (x1 - inset, top_y), (x1, base_y)], mat)
    for yy in range(top_y + step - 1, base_y - 1, step):
        t = (yy - top_y) / max(1, base_y - top_y)
        l = round(x0 + inset * (1 - t)) + 1
        r = round(x1 - inset * (1 - t)) - 1
        if r > l:
            s.rect(l, yy, r - l, 1, line_mat or mat, "lo")


def sandbags(s, y, x0, x1, skip=(0, 0)):
    for x in range(x0, x1, 5):
        if skip[0] <= x < skip[1]:
            continue
        s.ellipse(x + 2.5, y, 3, 2, "khaki")


def window(s, x, y, w=3, h=4, mat="dark"):
    s.rect(x, y, w, h, mat)


# ------------------------------------------------------------------ medieval
def m_keep():
    s = B("keep", 3)
    s.rect(8, 16, 32, 28, "stone"); courses(s, 8, 16, 32, 28)
    s.rect(1, 10, 13, 34, "stone"); courses(s, 1, 10, 13, 34)
    s.rect(34, 10, 13, 34, "stone"); courses(s, 34, 10, 13, 34)
    for x in (1, 6, 11, 34, 39, 44):
        s.rect(x, 7, 3, 3, "stone")
    for x in (14, 19, 24, 29):
        s.rect(x, 13, 3, 3, "stone")
    arch_door(s, 19, 28, 10, 16)
    s.dots([(21, y) for y in range(30, 44, 3)] + [(24, y) for y in range(30, 44, 3)] + [(27, y) for y in range(30, 44, 3)], "iron", "mid")
    window(s, 6, 18, 2, 5); window(s, 40, 18, 2, 5); window(s, 11, 30, 2, 4); window(s, 35, 30, 2, 4)
    s.rect(4, 26, 5, 9, "team"); s.rect(39, 26, 5, 9, "team")        # hanging banners
    mark(s, 5, 29); mark(s, 40, 29)
    flag(s, 24, 1, 12, 9, 6)
    return s


def m_barracks():
    s = B("barracks", 3)
    s.rect(2, 26, 44, 18, "stone"); courses(s, 2, 26, 44, 18)                          # low wings
    hip_roof(s, 1, 47, 17, 27, 3, "tile", step=2)
    s.rect(14, 10, 20, 34, "stone"); courses(s, 14, 10, 20, 34)                         # central hall
    s.poly([(12, 10), (24, 3), (36, 10)], "tile")                                       # pyramid roof over the hall
    arch_door(s, 20, 31, 8, 13)
    window(s, 6, 32, 4, 5); window(s, 38, 32, 4, 5); window(s, 18, 15, 3, 5); window(s, 27, 15, 3, 5)
    for cx in (9, 39):
        s.ellipse(cx, 41, 2.8, 2.8, "team")
    s.rect(21, 14, 6, 9, "team")
    mark(s, 22, 16)
    for x in (4, 43):
        s.line(x, 43, x, 31, "wood"); s.dots([(x, 30)], "steel", "hi")
    flag(s, 24, 1, 6, 9, 5)
    return s


def m_stable():
    s = B("stable", 3)
    s.rect(3, 28, 42, 16, "wood"); planks(s, 3, 28, 42, 16)
    s.poly([(2, 29), (24, 3), (45, 29)], "thatch")                                      # steep gable
    for yy in range(7, 29, 3):
        t = (yy - 3) / 26
        s.rect(round(24 - 22 * t) + 1, yy, round(43 * t) - 2, 1, "thatch", "lo")
    s.rect(14, 30, 20, 14, "dark")
    s.rect(13, 29, 1, 15, "leather"); s.rect(34, 29, 1, 15, "leather"); s.rect(13, 28, 22, 2, "leather")
    s.ellipse(24, 38, 4.5, 3.2, "horse"); s.poly([(26, 35), (29, 31), (31, 33), (29, 38)], "horse")
    s.dots([(30, 32)], "dark", "dk"); s.rect(27, 30, 2, 2, "horse")
    s.rect(37, 35, 7, 8, "thatch"); s.rect(37, 35, 7, 1, "thatch", "hi")
    s.rect(4, 31, 7, 6, "team"); mark(s, 6, 32)
    s.rect(22, 12, 5, 6, "team"); mark(s, 23, 13)                                                        # gable pennant board
    return s


def m_workshop():
    s = B("workshop", 3)
    s.rect(3, 24, 42, 20, "wood"); planks(s, 3, 24, 42, 20)
    s.rect(3, 37, 42, 7, "stone"); courses(s, 3, 37, 42, 7, every=4)
    s.rect(2, 12, 22, 32, "stone"); courses(s, 2, 12, 22, 32)                           # tall forge house
    hip_roof(s, 1, 25, 6, 13, 6, "iron", step=2)
    s.rect(30, 14, 15, 10, "iron")                                                      # lean-to roof
    s.rect(34, 3, 7, 12, "stone"); courses(s, 34, 3, 7, 12, every=4)
    s.ellipse(37, 3, 3, 2, "smoke")
    arch_door(s, 6, 28, 14, 16)
    s.rect(8, 37, 8, 5, "fire")
    s.ellipse(35, 32, 4.5, 4.5, "iron"); s.dots([(35, 32)], "steel", "hi")
    s.rect(30, 38, 10, 2, "iron"); s.rect(32, 40, 6, 3, "iron")
    s.rect(41, 26, 4, 10, "team"); s.rect(9, 16, 6, 8, "team")
    mark(s, 41, 29); mark(s, 10, 18)
    return s


def m_cottage():
    s = B("cottage", 2)
    s.rect(4, 15, 24, 14, "cloth"); planks(s, 4, 15, 24, 14, "wood", 6)
    s.rect(4, 15, 24, 1, "wood"); s.rect(4, 28, 24, 1, "wood")
    hip_roof(s, 1, 31, 5, 16, 7, "thatch", step=2)
    s.rect(22, 2, 4, 8, "stone")
    s.rect(13, 20, 6, 9, "team"); s.rect(12, 19, 8, 1, "wood")                         # painted door
    mark(s, 14, 22)
    window(s, 6, 19, 4, 4, "glass"); s.rect(5, 19, 1, 4, "team"); s.rect(10, 19, 1, 4, "team")
    window(s, 22, 19, 4, 4, "glass"); s.rect(21, 19, 1, 4, "team"); s.rect(26, 19, 1, 4, "team")
    return s


def m_storehouse():
    s = B("storehouse", 2)
    s.rect(3, 13, 26, 16, "wood"); planks(s, 3, 13, 26, 16, "wood", 5)
    s.rect(3, 6, 4, 8, "wood"); s.rect(3, 5, 4, 1, "wood", "hi")                        # loading hoist post
    hip_roof(s, 1, 31, 9, 14, 2, "leather", step=2)
    s.rect(9, 18, 14, 11, "dark"); s.rect(8, 17, 16, 1, "wood")
    s.line(10, 19, 21, 28, "wood"); s.line(21, 19, 10, 28, "wood")                    # barn-door braces
    s.rect(11, 10, 10, 3, "team"); mark(s, 14, 10)                                       # sign
    s.rect(24, 23, 5, 5, "wood"); s.rect(24, 23, 5, 1, "wood", "hi")                  # crate
    s.ellipse(5, 26, 2.2, 2.4, "cloth")                                                # sack
    return s


def m_tower():
    s = B("tower", 2)
    s.rect(8, 6, 16, 24, "stone"); courses(s, 8, 6, 16, 24, every=4)
    s.poly([(6, 7), (16, 1), (26, 7)], "tile")                                          # conical roof
    window(s, 15, 10, 2, 5); window(s, 15, 19, 2, 4)
    arch_door(s, 13, 23, 6, 7)
    s.rect(11, 15, 3, 7, "team"); s.rect(18, 15, 3, 7, "team")                          # hanging banners
    mark(s, 11, 16); mark(s, 18, 16)
    return s


# ------------------------------------------------------------------ modern
def d_keep():
    s = B("keep", 3)
    s.rect(4, 24, 40, 20, "concrete"); s.rect(10, 14, 28, 11, "concrete")
    s.rect(8, 12, 32, 3, "stone")
    for x in (13, 19, 25, 31):
        window(s, x, 17, 4, 4, "glass")
    s.rect(4, 34, 40, 3, "team"); mark(s, 8, 34)
    arch_door(s, 20, 31, 8, 13, "iron", "dark")
    window(s, 8, 27, 4, 4, "glass"); window(s, 36, 27, 4, 4, "glass")
    sandbags(s, 42, 2, 46, skip=(18, 30))
    s.rect(34, 6, 2, 7, "iron"); s.ellipse(35, 6, 5, 2.6, "steel"); s.dots([(35, 6)], "iron", "dk")   # radar
    flag(s, 12, 1, 11, 9, 6)
    return s


def d_barracks():
    s = B("barracks", 3)
    s.rect(3, 22, 42, 22, "concrete")
    s.poly([(1, 23), (9, 11), (39, 11), (47, 23)], "olive")                              # long pitched roof
    for x in range(8, 41, 5):
        s.rect(x, 12, 1, 10, "olive", "lo")
    s.rect(21, 6, 6, 6, "olive"); s.rect(22, 8, 4, 2, "dark")                             # roof lantern
    s.rect(3, 24, 42, 2, "team")
    for x in (7, 14, 33, 40):
        window(s, x, 29, 4, 4, "glass")
    for x in (20, 25):
        arch_door(s, x, 32, 4, 12, "iron", "dark")                                       # two doors: a barrack row
    s.rect(19, 25, 10, 5, "dark"); s.line(20, 26, 27, 29, "steel"); s.line(27, 26, 20, 29, "steel")   # crossed-rifles sign
    sandbags(s, 43, 3, 42, skip=(17, 31))
    flag(s, 38, 1, 9, 7, 5)
    return s


def d_stable():
    s = B("stable", 3)
    s.rect(3, 26, 42, 18, "concrete")
    s.poly([(1, 27), (5, 18), (14, 14), (34, 14), (43, 18), (47, 27)], "iron")          # arched hangar roof
    for x in range(5, 44, 4):
        s.rect(x, 17, 1, 9, "iron", "lo")
    for x in (6, 19, 32):
        s.rect(x, 30, 10, 14, "dark")
    s.rect(20, 38, 8, 4, "olive"); s.rect(22, 35, 4, 3, "glass"); s.ellipse(22, 43, 1.6, 1.6, "rubber"); s.ellipse(27, 43, 1.6, 1.6, "rubber")
    s.rect(8, 28, 32, 3, "team"); mark(s, 22, 28)
    return s


def d_workshop():
    s = B("workshop", 3)
    s.rect(3, 22, 42, 22, "concrete")
    for k in range(3):
        x = 3 + 14 * k
        s.poly([(x, 22), (x, 12), (x + 13, 22)], "iron")
        s.poly([(x + 1, 21), (x + 1, 14), (x + 6, 21)], "glass")
    s.rect(38, 3, 5, 18, "stone"); s.ellipse(40, 3, 3, 2, "smoke")
    s.rect(14, 28, 20, 16, "dark"); s.rect(13, 27, 22, 1, "iron")
    s.rect(28, 36, 10, 2, "iron")                                                      # barrel poking out
    s.rect(5, 26, 6, 10, "team"); mark(s, 6, 28)
    s.rect(3, 40, 10, 4, "olive")
    return s


def d_cottage():
    s = B("cottage", 2)
    s.rect(4, 16, 24, 12, "khaki")
    s.poly([(2, 17), (16, 7), (30, 17)], "olive")                                        # gable roof
    s.rect(22, 3, 2, 9, "iron")                                                          # stove pipe
    s.rect(13, 19, 6, 9, "team"); s.rect(12, 18, 8, 1, "iron")                           # painted door
    mark(s, 14, 21)
    window(s, 6, 19, 4, 4, "glass"); window(s, 22, 19, 4, 4, "glass")
    s.rect(4, 27, 24, 1, "iron")
    return s


def d_storehouse():
    s = B("storehouse", 2)
    s.rect(3, 21, 11, 7, "team")
    for x in range(5, 13, 3):
        s.rect(x, 22, 1, 5, "team", "lo")
    mark(s, 7, 23)
    s.rect(3, 15, 10, 6, "olive")
    s.rect(14, 7, 15, 11, "khaki")
    for x in range(16, 28, 3):
        s.rect(x, 8, 1, 9, "khaki", "lo")
    s.rect(20, 20, 9, 8, "wood"); s.rect(20, 20, 9, 1, "wood", "hi"); s.line(20, 20, 28, 27, "wood", "lo")
    s.rect(3, 27, 24, 2, "iron")
    return s


def d_tower():
    s = B("tower", 2)
    s.rect(9, 17, 2, 13, "iron"); s.rect(21, 17, 2, 13, "iron")
    s.rect(11, 22, 10, 1, "iron"); s.rect(11, 26, 10, 1, "iron")
    s.rect(6, 7, 20, 10, "olive")                                                        # armoured cab
    window(s, 9, 10, 14, 2, "dark")                                                      # firing slit
    s.rect(5, 4, 22, 3, "stone")
    s.rect(26, 10, 5, 1, "iron"); s.rect(25, 9, 2, 3, "iron")                            # machine gun
    s.rect(6, 14, 20, 3, "team"); mark(s, 14, 14)
    sandbags(s, 29, 3, 25)
    return s


def scaffold(size):
    s = B("scaffold", size)
    px = size * 16
    s.rect(2, px - 5, px - 4, 3, "leather")
    for x in range(3, px - 3, 14):
        s.rect(x, 6, 2, px - 10, "wood")                                                  # few, thin posts
    s.rect(3, int(px * 0.55), px - 6, 1, "leather")                                       # one rail
    s.line(4, px - 7, px - 6, 8, "wood", "lo")
    s.rect(px - 9, 3, 5, 3, "team")
    return s


ERAS = {
    "medieval": {"keep": m_keep, "barracks": m_barracks, "stable": m_stable, "workshop": m_workshop,
                 "cottage": m_cottage, "storehouse": m_storehouse, "tower": m_tower},
    "modern":   {"keep": d_keep, "barracks": d_barracks, "stable": d_stable, "workshop": d_workshop,
                 "cottage": d_cottage, "storehouse": d_storehouse, "tower": d_tower},
}
