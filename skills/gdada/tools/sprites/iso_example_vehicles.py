"""Modern-era vehicle models (batch B): light/medium/heavy tanks, howitzer, anti-tank gun, tank destroyer."""
from __future__ import annotations
from iso import Model


def _tracks(m, x0, length, ys, width, h, skirt=True, skirt_h=2.2, mat="rubber", wheels=True):
    """Track belts on both sides at y offsets `ys`=(left_y, right_y), with sprockets/idlers and optional skirt plates."""
    for sy in ys:
        m.box(x0, sy, 0, length, width, h, mat)
        m.wedge(x0 - 0.8, sy + 0.2, 0.3, 1.6, width - 0.4, h - 0.3, mat, slope=1.0)          # front idler lift
        m.box(x0 + 0.5, sy, h, length - 1, width, 0.5, "gunmetal")                         # top run / fender lip
        if wheels:
            n = max(3, int(length // 3.6))
            for i in range(n):
                wx = x0 + 1.6 + i * (length - 3.2) / (n - 1)
                outer = sy - 0.15 if sy < 0 else sy + width - 0.05
                m.box(wx - 0.7, outer, 0.5, 1.4, 0.2, h - 0.9, "iron")
        if skirt:
            outer = sy - 0.5 if sy < 0 else sy + width
            m.box(x0 + 1, outer, h - skirt_h + 0.8, length - 2.5, 0.5, skirt_h, "gunmetal")


def light_tank() -> Model:
    m = Model("scoutcart", 32, 32, scale=1.0, ground_y=0.72)
    _tracks(m, -6.5, 13, (-4.9, 2.4), 2.5, 2.6, skirt=False)
    m.wedge(-6.3, -3.0, 1.8, 12.6, 6.0, 2.4, "olive", slope=2.0, back=0.5, taper=0.3)      # hull w/ glacis
    m.box(-6.3, -3.0, 4.2, 4.4, 6.0, 0.5, "gunmetal")                                      # engine deck
    m.box(-5.6, -2.2, 4.7, 1.4, 4.4, 0.35, "iron")                                         # grille
    m.box(-7.0, -2.6, 2.0, 0.8, 1.6, 1.4, "iron")                                          # exhaust
    m.box(-7.2, 2.0, 2.2, 1.6, 1.2, 1.4, "khaki")                                          # stowage
    m.prism(0.3, 0, 4.0, 3.3, 2.4, "team", sides=8, ry=3.0, taper=0.5)                     # turret
    m.box(3.0, -0.5, 4.9, 6.0, 1.0, 1.0, "iron")                                           # gun
    m.box(8.8, -0.7, 4.8, 1.2, 1.4, 1.2, "steel")                                          # muzzle
    m.box(-6.0, -1.0, 4.7, 2.0, 2.0, 0.7, "team")                                         # rear deck panel
    m.prism(-0.8, 1.3, 6.0, 0.9, 0.6, "gunmetal", sides=6)                                 # hatch
    m.pole(-2.8, -1.5, 6.0, 3.0, "iron", t=0.3)                                            # antenna
    m.mark_at = (-0.2, -0.8, 6.05)
    return m


def medium_tank() -> Model:
    m = Model("wagon", 32, 32, scale=1.05, ground_y=0.74)
    _tracks(m, -8.5, 17, (-6.0, 3.2), 2.8, 3.0)
    m.wedge(-8.3, -3.7, 2.0, 16.6, 7.4, 3.0, "olive", slope=2.6, back=0.6, taper=0.3)
    m.box(-8.3, -3.7, 5.0, 5.5, 7.4, 0.6, "gunmetal")                                      # engine deck
    m.box(-7.6, -2.6, 5.6, 2.0, 5.2, 0.35, "iron")                                         # grille
    m.box(-9.4, -3.2, 2.2, 1.2, 2.0, 1.5, "iron")                                          # exhaust
    m.prism(-9.4, 2.4, 2.0, 0.9, 2.2, "wood", sides=6)                                     # fuel drum
    m.box(-4.0, 3.2, 5.6, 3.0, 0.8, 1.0, "khaki")                                          # stowage
    m.prism(-0.5, 0, 5.0, 4.4, 2.4, "team", sides=10, ry=3.7, taper=0.7)                   # turret
    m.box(3.2, -0.3, 6.0, 1.6, 0.6, 1.6, "gunmetal")                                       # mantlet
    m.box(3.8, -0.7, 5.9, 1.0, 1.4, 1.8, "gunmetal")
    m.box(4.6, -0.5, 6.4, 7.0, 1.0, 1.0, "iron")                                           # gun
    m.box(11.4, -0.8, 6.2, 1.6, 1.6, 1.6, "steel")                                         # muzzle brake
    m.prism(-1.8, 1.4, 7.4, 1.2, 0.8, "gunmetal", sides=6)                                 # cupola
    m.box(-1.2, -2.6, 7.4, 1.0, 1.0, 0.7, "khaki")                                         # turret bin
    m.pole(-3.8, -1.8, 7.4, 3.5, "iron", t=0.3)
    m.mark_at = (-0.6, -1.0, 7.5)
    return m


def heavy_tank() -> Model:
    m = Model("bulwark", 40, 40, scale=1.0, ground_y=0.74)
    _tracks(m, -11, 22, (-8.0, 4.4), 3.6, 4.0, skirt_h=3.4)
    m.wedge(-10.8, -4.8, 2.4, 21.6, 9.6, 3.8, "olive", slope=3.4, back=0.6, taper=0.5)    # hull
    m.wedge(5.0, -4.6, 5.0, 5.5, 9.2, 1.0, "olive", slope=1.0)                             # upper glacis plate
    m.box(-10.8, -4.8, 6.2, 7.5, 9.6, 0.7, "gunmetal")                                     # engine deck
    m.box(-9.8, -3.4, 6.9, 2.6, 6.8, 0.4, "iron")                                          # grille
    m.box(-6.4, -3.4, 6.9, 2.6, 6.8, 0.4, "iron")
    m.box(-12.0, -4.2, 2.6, 1.4, 2.4, 2.0, "iron")                                         # exhausts
    m.box(-12.0, 1.8, 2.6, 1.4, 2.4, 2.0, "iron")
    m.prism(-12.4, -0.5, 2.0, 1.1, 2.8, "wood", sides=6)                                   # fuel drums
    m.prism(-12.4, 1.0, 2.0, 1.1, 2.8, "wood", sides=6)
    m.box(-5.0, 4.4, 7.0, 4.0, 0.9, 1.3, "khaki")                                          # stowage
    m.box(-5.0, -5.3, 7.0, 3.0, 0.9, 1.3, "khaki")
    m.prism(-1.0, 0, 6.1, 6.4, 3.2, "team", sides=10, ry=5.2, taper=1.0)                   # huge turret
    m.box(-7.6, -2.6, 6.4, 1.8, 5.2, 2.2, "team")                                          # turret bustle
    m.box(4.6, -2.0, 7.0, 1.8, 4.0, 2.4, "gunmetal")                                       # mantlet
    m.box(6.2, -0.8, 7.6, 7.0, 1.6, 1.6, "iron")                                           # gun
    m.box(13.0, -0.7, 7.7, 4.0, 1.4, 1.4, "iron")
    m.box(16.6, -1.1, 7.4, 2.4, 2.2, 2.2, "steel")                                         # muzzle brake
    m.box(6.2, 1.2, 7.0, 4.0, 0.5, 0.8, "gunmetal")                                        # coax
    m.prism(-3.0, 2.4, 9.3, 1.5, 1.0, "gunmetal", sides=6)                                 # commander cupola
    m.prism(-2.0, -2.6, 9.3, 1.1, 0.5, "gunmetal", sides=6)                                # loader hatch
    m.box(-5.0, -0.6, 9.3, 1.0, 1.2, 0.6, "iron")
    m.pole(-6.0, -4.0, 9.3, 4.0, "iron", t=0.35)
    m.mark_scale = 2
    m.mark_at = (-1.0, -1.6, 9.35)
    return m


def howitzer() -> Model:
    m = Model("ballista", 36, 36, scale=1.0, ground_y=0.74)
    _tracks(m, -9.5, 19, (-6.4, 3.4), 3.0, 3.0, skirt=False)
    m.wedge(-9.3, -3.8, 2.0, 9.0, 7.6, 2.8, "olive", back=0.4, taper=0.3)
    m.wedge(-0.3, -3.8, 2.0, 9.6, 7.6, 2.8, "olive", slope=2.0, taper=0.3)
    m.box(-9.3, -3.8, 4.8, 5.0, 7.6, 0.6, "gunmetal")
    m.box(-8.3, -2.6, 5.4, 2.0, 5.2, 0.35, "iron")
    # gun superstructure: open-topped team-colour fighting compartment at the rear, raised barrel
    m.wedge(-6.0, -3.6, 4.8, 8.0, 7.2, 3.4, "team", slope=1.2, back=0.6, taper=0.4)
    m.box(-4.4, -2.4, 8.2, 3.6, 4.8, 0.3, "team")                                      # top plate
    m.box(-9.6, -3.6, 4.8, 3.0, 0.9, 1.6, "khaki")
    m.box(-9.6, 2.7, 4.8, 3.0, 0.9, 1.6, "khaki")
    m.box(1.6, -1.3, 6.2, 2.0, 2.6, 2.8, "gunmetal")                                       # cradle / mantlet
    m.box(3.4, -0.6, 7.4, 4.0, 1.2, 1.2, "iron")                                           # barrel (raised)
    m.box(7.2, -0.6, 8.0, 4.0, 1.2, 1.2, "iron")
    m.box(10.8, -0.6, 8.6, 3.6, 1.2, 1.2, "iron")
    m.box(13.8, -1.0, 8.4, 2.2, 2.0, 1.8, "steel")                                         # muzzle brake
    m.box(-0.6, -0.4, 6.0, 2.6, 0.8, 0.7, "iron")                                          # recoil cylinder
    m.wedge(-10.2, -3.2, 1.6, 1.2, 6.4, 1.8, "gunmetal")                                   # rear spade
    m.prism(-3.0, -2.0, 8.2, 0.9, 0.5, "gunmetal", sides=6)
    m.prism(-10.2, 0, 2.0, 1.0, 2.2, "wood", sides=6)
    m.mark_at = (-4.0, -1.0, 8.55)
    return m


def at_gun() -> Model:
    m = Model("atgun", 28, 28, scale=1.0, ground_y=0.74)
    for sy in (-4.6, 3.6):                                                                 # upright wheels
        m.box(-2.2, sy, 0.8, 4.4, 1.0, 2.8, "rubber")
        m.box(-1.5, sy, 0.0, 3.0, 1.0, 4.4, "rubber")
        m.box(-0.6, sy + (-0.15 if sy < 0 else 0.95), 1.4, 1.2, 0.2, 1.2, "steel")        # hub
    m.box(-0.8, -3.6, 1.8, 1.6, 7.2, 0.8, "gunmetal")                                      # axle bar
    for ty in (-1.0, 1.0):                                                                 # split trail
        m.wedge(-8.4, ty * 3.0 - 0.5, 0.0, 7.4, 1.0, 1.4, "gunmetal", back=0.0)
        m.box(-9.4, ty * 3.0 - 0.9, 0.0, 1.2, 1.8, 0.5, "iron")                            # spade
    m.box(-1.4, -1.3, 2.2, 3.2, 2.6, 1.8, "team")                                          # breech carriage
    m.box(-4.0, -0.5, 3.4, 3.0, 1.0, 1.0, "iron")                                          # breech
    m.box(0.6, -0.5, 3.6, 4.2, 1.0, 1.0, "iron")                                           # barrel
    m.box(4.6, -0.5, 3.7, 3.6, 1.0, 1.0, "iron")
    m.box(8.0, -0.8, 3.5, 1.6, 1.6, 1.5, "steel")                                          # muzzle brake
    m.wedge(1.0, -3.6, 2.2, 1.8, 7.2, 3.8, "team", slope=0.8, taper=0.2)                   # gun shield
    m.box(1.2, -3.4, 2.4, 1.0, 0.8, 0.6, "team")
    m.box(1.0, -0.6, 3.2, 0.5, 1.2, 1.2, "gunmetal")                                       # shield aperture
    m.box(-2.6, 1.2, 2.2, 1.4, 1.4, 1.0, "team")                                          # ammo crate
    m.mark_at = (1.2, -1.2, 5.95)
    return m


def tank_destroyer() -> Model:
    m = Model("tankdestroyer", 36, 36, scale=1.0, ground_y=0.74)
    _tracks(m, -9.5, 19, (-6.0, 3.2), 2.8, 2.8, skirt=True, skirt_h=2.0)
    m.wedge(-9.3, -3.6, 1.8, 9.0, 7.2, 2.6, "olive", back=0.4, taper=0.3)
    m.wedge(-0.3, -3.6, 1.8, 9.6, 7.2, 2.6, "olive", slope=2.4, taper=0.3)      # low hull
    m.box(-9.3, -3.6, 4.4, 4.4, 7.2, 0.5, "gunmetal")
    m.box(-8.6, -2.4, 4.9, 1.8, 4.8, 0.35, "iron")
    # sloped casemate, no turret
    m.wedge(-4.6, -3.4, 4.4, 10.4, 6.8, 3.0, "team", slope=3.0, back=1.0, taper=0.8)
    m.box(-4.4, -2.6, 7.0, 4.0, 5.2, 0.4, "team")                                          # roof extension
    m.box(5.0, -2.0, 4.6, 1.8, 4.0, 1.6, "gunmetal")                                       # gun mantlet
    m.box(6.6, -0.6, 5.2, 5.0, 1.2, 1.2, "iron")                                           # gun
    m.box(11.4, -0.6, 5.2, 4.0, 1.2, 1.2, "iron")
    m.box(15.0, -1.0, 5.0, 2.0, 2.0, 1.8, "steel")                                         # muzzle brake
    m.prism(-2.4, 1.6, 7.3, 1.1, 0.7, "gunmetal", sides=6)                                 # commander hatch
    m.box(-1.0, -2.6, 7.3, 1.4, 1.2, 0.6, "gunmetal")
    m.prism(-9.8, 0.4, 1.8, 1.0, 2.0, "wood", sides=6)
    m.box(-9.9, -3.0, 2.2, 1.0, 1.8, 1.2, "iron")
    m.box(-4.6, 3.4, 4.4, 3.0, 0.8, 1.2, "khaki")
    m.pole(-3.0, -2.6, 7.3, 3.5, "iron", t=0.3)
    m.mark_at = (-3.2, -1.0, 7.45)
    return m


UNITS = {"modern": {
    "scoutcart": light_tank, "wagon": medium_tank, "bulwark": heavy_tank,
    "ballista": howitzer, "atgun": at_gun, "tankdestroyer": tank_destroyer,
}}
