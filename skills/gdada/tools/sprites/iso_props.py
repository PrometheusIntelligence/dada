"""Isometric terrain props: trees, bushes, boulders and rubble, drawn as standing sprites on the relief ground. Each prop has a few
variants (different seeds); they are drawn at one facing because they look the same from every side."""
import random
from iso import Model


def _rnd(seed):
    return random.Random(seed * 7919 + 13)


def pine(seed):
    r = _rnd(seed)
    m = Model("pine", 22, 32, scale=1.0, ground_y=0.9, shadow=0.8)
    m.box(-0.9, -0.9, 0, 1.8, 1.8, 4, "wood", 2)
    s = r.uniform(0.9, 1.2)
    m.cone(0, 0, 2.5, 5.6 * s, 7.5 * s, "olive", None, sides=8)
    m.cone(0, 0, 7.5 * s, 4.6 * s, 6.5 * s, "olive", None, sides=8)
    m.cone(0, 0, 11.5 * s, 3.3 * s, 6.0 * s, "olive", None, sides=8)
    return m


def oak(seed):
    r = _rnd(seed)
    m = Model("oak", 24, 28, scale=1.0, ground_y=0.9, shadow=0.9)
    m.box(-1.0, -1.0, 0, 2.0, 2.0, 5.5, "wood", 2)
    s = r.uniform(0.9, 1.15)
    m.prism(0, 0, 4.5, 6.2 * s, 4.5 * s, "olive", None, sides=9, taper=1.2)
    m.prism(r.uniform(-1.5, 1.5), r.uniform(-1.5, 1.5), 8.5 * s, 4.2 * s, 3.8 * s, "olive", None, sides=8, taper=1.2)
    return m


def bush(seed):
    r = _rnd(seed)
    m = Model("bush", 14, 12, scale=1.0, ground_y=0.85, shadow=0.7)
    m.prism(0, 0, 0, 3.6, 2.6, "olive", None, sides=8, taper=0.8)
    m.prism(r.uniform(-1.6, 1.6), r.uniform(-1.6, 1.6), 0, 2.4, 2.2, "olive", 1, sides=7, taper=0.6)
    return m


def rock(seed):
    r = _rnd(seed)
    m = Model("rock", 16, 14, scale=1.0, ground_y=0.85, shadow=0.8)
    w, d = r.uniform(4, 6.5), r.uniform(3.5, 6)
    m.wedge(-w / 2, -d / 2, 0, w, d, r.uniform(3, 5), "stone", None, slope=r.uniform(0.8, 2), taper=0.9)
    m.wedge(r.uniform(-3, 0), r.uniform(-3, 0), 0, 3, 3, r.uniform(1.8, 3), "iron", None, slope=0.8)
    return m


def rubble(seed):
    r = _rnd(seed)
    m = Model("rubble", 20, 14, scale=1.0, ground_y=0.85, shadow=0.7)
    for _ in range(6):
        w, d, h = r.uniform(1.5, 4.5), r.uniform(1.5, 4.5), r.uniform(0.8, 2.8)
        m.box(r.uniform(-6, 4), r.uniform(-5, 3), 0, w, d, h, r.choice(["concrete", "stone", "dark", "iron"]), r.choice([1, 2, 3]))
    return m


VARIANTS = 3
PROPS = {"pine": pine, "oak": oak, "bush": bush, "rock": rock, "rubble": rubble}
