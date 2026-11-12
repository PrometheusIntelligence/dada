"""Modern vehicles on a 24x24 canvas (a tile and a half), drawn bigger and harder-edged than the 16 px infantry:
sloped armour, side skirts, many road wheels, long guns with muzzle brakes, amber sights. All face right.
Team colour sits on the turret or casemate (with the faction mark) so sides read from far away."""
from kit import Sprite, mark

W = 24


def V(name, phase, shadow=(12, 22.6, 10.5, 1.6)):
    return Sprite(name, shadow, w=W, h=W, bob=phase)


def tracks(s, x0, x1, y0, y1, phase, wheels):
    """A track belt with rounded ends, road wheels (steel hubs) and a drive sprocket at the front."""
    r = (y1 - y0) / 2
    s.rect(x0 + int(r), y0, x1 - x0 - 2 * int(r) + 1, y1 - y0 + 1, "rubber")
    s.ellipse(x0 + r + .5, y0 + r + .5, r + .5, r + .5, "rubber")
    s.ellipse(x1 - r + .5, y0 + r + .5, r + .5, r + .5, "rubber")
    cy = round(y0 + r)
    for i in range(wheels):
        cx = round(x0 + r + (x1 - x0 - 2 * r) * i / max(1, wheels - 1))
        s.dots([(cx, cy), (cx + (1 if (i + phase) % 2 else 0), cy - 1)], "steel", "mid")
        s.dots([(cx - 1, cy), (cx + 1, cy)], "iron", "hi")


def armoured_car(phase=0):
    s = V("rider", phase, (12, 22.6, 9.5, 1.5))
    s.poly([(3, 18), (3, 12), (8, 10), (18, 10), (21, 14), (21, 18)], "olive")   # angular armoured body
    s.rect(3, 15, 18, 2, "gunmetal")                                         # armoured sill
    s.poly([(12, 11), (13, 8), (17, 9), (17, 11)], "glass")                  # raked windscreen slit
    s.rect(4, 10, 8, 4, "team")                                              # rear bed in faction colour
    s.rect(7, 6, 1, 4, "iron"); s.rect(5, 5, 5, 1, "iron")                   # MG pillar and shield
    s.rect(9, 6, 7, 1, "iron"); s.rect(15, 5, 1, 3, "steel")                 # gun and flash hider
    for cx in (6, 17):
        s.ellipse(cx, 19.5, 3, 3, "rubber"); s.dots([(cx, 19), (cx + phase, 20)], "steel", "mid")
    mark(s, 6, 10)
    return s


def self_propelled_gun(phase=0):
    s = V("ballista", phase, (12, 22.6, 10, 1.5))
    tracks(s, 2, 17, 18, 22, phase, 4)
    s.rect(3, 13, 14, 6, "olive")                                            # chassis
    s.poly([(4, 13), (5, 8), (13, 8), (16, 13)], "team")                     # open fighting compartment
    s.poly([(9, 11), (11, 8), (22, 1), (22, 4)], "iron")                     # long elevated barrel
    s.rect(20, 1, 3, 5, "steel")                                             # muzzle brake
    s.poly([(1, 19), (3, 15), (3, 22)], "gunmetal")                          # recoil spade
    s.rect(16, 12, 4, 5, "khaki")                                            # ammunition stowage
    s.dots([(6, 9)], "fire", "mid")
    mark(s, 7, 9)
    return s


def light_tank(phase=0):
    s = V("scoutcart", phase, (12, 22.6, 8.5, 1.4))
    tracks(s, 4, 19, 18, 22, phase, 4)
    s.rect(5, 16, 13, 3, "gunmetal")                                         # skirts
    s.poly([(5, 17), (5, 14), (8, 12), (16, 12), (19, 14), (18, 17)], "olive")
    s.rect(7, 14, 10, 1, "team")
    s.poly([(7, 12), (8, 8), (15, 8), (16, 12)], "team")                     # low angular turret
    s.rect(15, 9, 6, 2, "iron"); s.rect(20, 8, 2, 4, "steel")                # autocannon and brake
    s.line(7, 7, 7, 12, "iron")                                              # short aerial
    s.dots([(13, 11)], "fire", "mid")
    mark(s, 9, 8)
    return s


def medium_tank(phase=0):
    s = V("wagon", phase, (12, 22.6, 10.5, 1.6))
    tracks(s, 2, 22, 16, 22, phase, 6)
    s.rect(3, 13, 18, 4, "gunmetal")                                         # skirts
    s.poly([(3, 15), (3, 11), (7, 9), (18, 9), (22, 12), (21, 15)], "olive")
    s.rect(5, 11, 14, 1, "team")
    s.ellipse(12, 7.5, 5, 2.6, "team")                                       # rounded cast turret in faction colour
    s.rect(15, 7, 8, 2, "iron"); s.rect(22, 6, 1, 4, "steel")                # gun and brake
    s.rect(1, 10, 3, 4, "khaki")                                             # rear stowage
    s.dots([(14, 8)], "fire", "mid")
    mark(s, 10, 6)
    return s


def heavy_tank(phase=0):
    s = V("bulwark", phase, (12, 22.7, 10.8, 1.6))
    tracks(s, 1, 22, 16, 22, phase, 8)
    s.rect(3, 12, 19, 5, "gunmetal")                                         # slab side armour
    s.dots([(x, 14) for x in range(5, 21, 3)], "steel", "hi")                # rivets
    s.poly([(1, 15), (1, 11), (5, 7), (19, 7), (22, 11), (21, 15)], "gunmetal")  # sloped black-steel hull
    s.rect(4, 9, 15, 2, "team")
    s.poly([(4, 7), (6, 2), (17, 1), (21, 7)], "olive")                      # tall faceted turret
    s.poly([(4, 7), (5, 3), (8, 3), (8, 7)], "gunmetal")                     # spaced-armour wedge
    s.rect(9, 3, 9, 4, "team")
    s.rect(17, 3, 6, 2, "iron"); s.rect(17, 6, 6, 2, "iron")                 # twin guns
    s.rect(21, 2, 2, 7, "steel")                                             # shared muzzle brake
    s.dots([(19, 5), (7, 8), (3, 11)], "fire", "mid")                        # glowing sights
    mark(s, 12, 3)
    return s


def anti_tank_gun(phase=0):
    s = V("atgun", phase, (11, 22.6, 9.5, 1.4))
    s.line(8, 19, 1, 22, "iron"); s.line(10, 19, 4, 22, "iron"); s.line(9, 20, 2, 22, "iron")   # splayed trail
    s.ellipse(9, 18.5, 3.4, 3.4, "rubber"); s.dots([(9, 18), (10 + phase, 19)], "steel", "mid")
    s.rect(11, 12, 12, 2, "iron"); s.rect(21, 10, 2, 6, "steel")             # very long barrel and brake
    s.poly([(6, 17), (6, 12), (9, 10), (14, 11), (15, 17)], "team")          # wide low gun shield
    s.rect(3, 15, 3, 4, "khaki")                                             # ready-use ammunition
    mark(s, 8, 12)
    return s


def halftrack(phase=0):
    s = V("halftrack", phase, (12, 22.6, 10.5, 1.5))
    s.rect(2, 17, 12, 5, "rubber")                                           # rear tracks
    for x in range(4 + phase, 13, 3):
        s.dots([(x, 19)], "steel", "mid")
    s.ellipse(18, 19.5, 2.7, 2.7, "rubber"); s.dots([(18, 19)], "steel", "mid")
    s.rect(2, 12, 19, 6, "olive")                                            # hull
    s.poly([(3, 12), (4, 5), (15, 5), (17, 12)], "khaki")                    # canvas hood over the squad
    s.rect(4, 8, 12, 4, "team")
    s.rect(17, 9, 5, 6, "olive"); s.rect(18, 10, 3, 3, "glass")              # cab
    s.rect(17, 7, 5, 1, "iron"); s.rect(19, 3, 1, 4, "iron"); s.rect(19, 3, 4, 1, "iron")   # ring-mounted MG on a raised post
    s.ellipse(3, 11, 2.2, 2.2, "rubber")                                     # spare wheel on the rear
    mark(s, 8, 8)
    return s


def tank_destroyer(phase=0):
    s = V("tankdestroyer", phase, (12, 22.6, 10.5, 1.5))
    tracks(s, 1, 22, 18, 22, phase, 7)
    s.poly([(1, 19), (1, 15), (7, 11), (17, 11), (22, 14), (21, 19)], "olive")   # low wedge to the ground
    s.rect(5, 14, 12, 3, "team")
    s.poly([(7, 10), (8, 7), (15, 7), (17, 10)], "gunmetal")                 # fixed casemate
    s.rect(14, 8, 9, 2, "iron"); s.rect(21, 7, 2, 4, "steel")                # very long gun and brake
    s.dots([(x, 12) for x in (4, 6, 8)], "iron", "dk")                       # engine grille
    s.line(5, 3, 5, 10, "iron")
    s.dots([(12, 8)], "fire", "mid")
    mark(s, 9, 14)
    return s


ROSTER = {"rider": armoured_car, "ballista": self_propelled_gun, "scoutcart": light_tank, "wagon": medium_tank,
          "bulwark": heavy_tank, "atgun": anti_tank_gun, "halftrack": halftrack, "tankdestroyer": tank_destroyer}
