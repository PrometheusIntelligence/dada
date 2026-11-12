"""The Tidewatch roster, drawn with kit.py. One function per unit, per era. All face right."""
from kit import Sprite, mark
import vehicles


def _human(s, torso="team", legs="leather", boots="rubber", arm="skin", phase=0):
    if phase == 0:                       # standing / contact pose
        s.rect(6, 11, 2, 3, legs); s.rect(9, 11, 2, 3, legs)
        s.rect(6, 13, 2, 1, boots); s.rect(9, 13, 2, 1, boots)
    else:                                # passing pose: rear foot lifted, front leg reaching
        s.rect(5, 11, 2, 2, legs); s.rect(5, 12, 2, 1, boots)
        s.rect(10, 11, 2, 3, legs); s.rect(10, 13, 2, 1, boots)
    if phase == 0:
        s.rect(5, 7, 1, 4, torso)        # rear arm hangs
        s.rect(6, 6, 5, 5, torso)
        s.rect(11, 7, 1, 3, arm)         # front arm
    else:
        s.rect(4, 7, 1, 3, torso)        # arms swing the other way
        s.rect(6, 6, 5, 5, torso)
        s.rect(11, 6, 1, 3, arm)
    s.ellipse(8.5, 4, 2.3, 2.3, "skin")
    s.dots([(10, 4)], "iron", "dk")      # eye


def _shadow():
    return (8, 14.6, 5.5, 1.4)


# ============================================================================ medieval
def m_worker(phase=0):
    s = Sprite("worker", _shadow())
    _human(s, torso="team", legs="cloth", phase=phase)
    s.poly([(4, 3), (6, 1), (11, 1), (13, 3)], "cloth")           # straw hat
    s.ellipse(4, 8.5, 2.2, 3.2, "cloth")                             # big sack
    s.line(12, 3, 12, 13, "wood")                                    # pick handle
    s.rect(10, 2, 5, 1, "steel"); s.dots([(10, 3), (14, 3)], "steel", "lo")
    mark(s, 7, 7)
    return s


def m_spearman(phase=0):
    s = Sprite("spearman", _shadow())
    _human(s, torso="cloth", legs="leather", phase=phase)
    s.rect(6, 1, 5, 3, "steel")                                      # helm
    s.rect(6, 4, 1, 1, "steel")
    s.line(13, 14, 13, 2, "wood")                                    # spear
    s.poly([(12, 3), (13, 0), (14, 3)], "steel")
    s.ellipse(10, 9, 3.6, 4.4, "team")                              # shield
    mark(s, 8, 8)
    return s


def m_archer(phase=0):
    s = Sprite("archer", (8, 14.6, 6.5, 1.4), bob=phase)
    s.rect(3, 12, 5, 2, "cloth"); s.rect(3, 13, 2, 1, "rubber")      # kneeling rear leg
    s.rect(9, 10, 2, 4, "cloth"); s.rect(9, 13, 3, 1, "rubber")      # front leg
    s.rect(4, 7, 2, 5, "wood")                                       # quiver
    s.dots([(4, 6), (5, 6)], "team", "mid")                          # fletching
    s.rect(6, 8, 5, 4, "leather")
    s.rect(7, 9, 3, 3, "team")                                       # tabard
    s.rect(11, 9, 1, 2, "skin")
    s.ellipse(8.5, 5.5, 2.3, 2.3, "skin"); s.dots([(10, 5)], "iron", "dk")
    s.poly([(5, 5), (6, 2), (11, 2), (11, 5)], "team")               # hood
    s.line(11, 1, 13, 3, "wood"); s.line(13, 3, 14, 7, "wood"); s.line(14, 7, 13, 11, "wood"); s.line(13, 11, 11, 13, "wood")
    s.line(11, 1, 11, 13, "cloth", "hi")                             # string, bow drawn tall
    mark(s, 7, 9)
    return s


def m_rider(phase=0):
    s = Sprite("rider", (8, 14.6, 6.5, 1.4), bob=phase)
    s.rect(4, 11, 1, 3, "horse"); s.rect(6, 12, 1, 2, "horse")
    s.rect(9, 12, 1, 2, "horse"); s.rect(12, 11, 1, 3, "horse")
    s.ellipse(8.5, 10, 5.2, 2.7, "horse")
    s.poly([(11, 8), (13, 5), (15, 7), (14, 9), (12, 11)], "horse")  # neck
    s.rect(13, 6, 2, 2, "horse")                                     # head
    s.line(3, 8, 2, 11, "leather")                                   # tail
    s.rect(6, 8, 5, 3, "team")                                       # blanket
    s.rect(7, 4, 3, 4, "steel")                                      # rider
    s.rect(7, 5, 3, 2, "team")
    s.ellipse(8.5, 3, 1.8, 1.8, "skin")
    s.rect(7, 1, 3, 2, "steel")
    s.line(9, 7, 13, 4, "wood")                                      # lance
    s.rect(13, 3, 2, 2, "steel")
    mark(s, 7, 8)
    return s


def m_ballista(phase=0):
    s = Sprite("ballista", (8, 14.6, 7, 1.4), bob=phase)
    s.rect(2, 8, 11, 2, "wood")                                      # stock
    s.rect(3, 3, 7, 5, "team")                                       # banner plate
    s.line(12, 2, 14, 9, "iron"); s.line(14, 9, 12, 14 - 3, "iron")  # bow arm
    s.line(12, 2, 12, 11, "cloth", "mid")
    s.line(3, 7, 14, 7, "steel", "mid")                              # bolt
    s.poly([(13, 6), (15, 7), (13, 8)], "steel")
    s.ellipse(5, 12.5, 2.5, 2.5, "wood"); s.ellipse(11, 12.5, 2.5, 2.5, "wood")
    s.dots([(5, 12), (11, 12)], "iron", "hi")
    mark(s, 5, 4)
    return s


def m_scoutcart(phase=0):
    s = Sprite("scoutcart", (8, 14.6, 7, 1.4), bob=phase)
    s.line(3, 3, 3, 8, "wood")                                       # mast
    s.rect(1, 2, 3, 2, "team")                                       # pennant
    s.rect(3, 8, 9, 3, "wood")
    s.rect(4, 8, 7, 3, "team")                                       # painted side
    s.poly([(12, 8), (15, 10), (12, 12)], "steel")                   # ram spike
    s.ellipse(8, 5.5, 1.8, 1.8, "skin"); s.rect(6, 3, 4, 2, "team")  # driver and cap
    s.ellipse(5, 12, 2.5, 2.5, "wood"); s.ellipse(11, 12, 2.5, 2.5, "wood")
    s.dots([(5, 12), (11, 12)], "iron", "hi")
    mark(s, 6, 8)
    return s


def m_wagon(phase=0):
    s = Sprite("wagon", (8, 14.6, 7.5, 1.4), bob=phase)
    s.rect(2, 3, 9, 2, "wood")                                       # roof beam
    s.rect(2, 5, 10, 6, "iron")                                      # plated body
    s.rect(2, 8, 10, 3, "team")
    s.dots([(4, 6), (7, 6), (10, 6)], "iron", "dk")                  # arrow slits
    s.dots([(3, 5), (6, 5), (9, 5), (11, 10)], "steel", "hi")        # rivets
    s.poly([(12, 6), (14, 8), (12, 10)], "steel")                    # ram
    s.line(6, 1, 6, 3, "wood"); s.rect(7, 1, 3, 2, "team")           # banner
    s.ellipse(5, 12, 2.6, 2.6, "wood"); s.ellipse(10, 12, 2.6, 2.6, "wood")
    s.dots([(5, 12), (10, 12)], "iron", "hi")
    mark(s, 6, 8)
    return s


def m_bulwark(phase=0):
    s = Sprite("bulwark", (8, 14.8, 8, 1.2), bob=phase)
    s.rect(1, 10, 13, 3, "iron")                                     # chassis
    s.rect(2, 2, 11, 9, "iron")                                      # tower
    s.rect(2, 1, 3, 1, "iron"); s.rect(6, 1, 3, 1, "iron"); s.rect(10, 1, 3, 1, "iron")   # crenels
    s.rect(3, 2, 9, 3, "team")
    s.rect(3, 7, 9, 2, "team")
    s.dots([(4, 5), (7, 5), (10, 5)], "iron", "dk")                  # slits
    s.dots([(3, 3), (11, 3), (3, 8), (11, 8), (7, 3)], "steel", "hi")
    s.poly([(12, 5), (14, 9), (12, 12)], "steel")                    # great ram
    for cx in (3, 6, 9, 12):
        s.ellipse(cx, 13, 1.7, 1.7, "wood")
    mark(s, 6, 2)
    return s


# ============================================================================ modern
def _helmet(s, mat="olive"):
    s.poly([(5, 4), (6, 1), (11, 1), (11, 4)], mat)


def d_worker(phase=0):
    s = Sprite("worker", _shadow())
    _human(s, torso="team", legs="khaki", phase=phase)
    s.rect(5, 2, 7, 2, "khaki"); s.rect(6, 1, 5, 1, "khaki")          # hard hat with brim
    s.line(12, 7, 13, 12, "iron"); s.rect(12, 5, 3, 2, "steel")      # wrench
    mark(s, 7, 7)
    return s


def d_spearman(phase=0):
    s = Sprite("spearman", _shadow())
    _human(s, torso="olive", legs="olive", boots="rubber", phase=phase)
    s.rect(6, 6, 5, 3, "team")                                       # team chest rig
    _helmet(s, "team")
    s.rect(3, 7, 3, 4, "leather")                                    # field pack
    s.rect(9, 9, 6, 1, "iron"); s.rect(8, 9, 2, 2, "wood")           # rifle
    mark(s, 7, 6)
    return s


def d_archer(phase=0):
    s = Sprite("archer", (8, 14.6, 7, 1.4), bob=phase)
    s.rect(3, 12, 5, 2, "olive"); s.rect(3, 13, 2, 1, "rubber")      # kneeling rear leg
    s.rect(9, 11, 2, 3, "olive"); s.rect(9, 13, 3, 1, "rubber")
    s.rect(5, 8, 6, 4, "team")
    s.rect(2, 7, 3, 4, "khaki")                                      # ammo box
    s.line(3, 1, 3, 6, "iron")                                       # radio whip
    s.ellipse(8.5, 6, 2.3, 2.3, "skin")
    s.poly([(5, 6), (6, 3), (11, 3), (11, 6)], "team")               # team helmet
    s.rect(9, 8, 6, 2, "iron"); s.ellipse(9.5, 6.5, 1.8, 1.6, "khaki")  # heavy gun and ammo drum
    s.line(11, 10, 10, 13, "iron"); s.line(13, 10, 14, 13, "iron")   # bipod
    mark(s, 6, 9)
    return s


ERAS = {
    "medieval": {"worker": m_worker, "spearman": m_spearman, "archer": m_archer, "rider": m_rider,
                 "ballista": m_ballista, "scoutcart": m_scoutcart, "wagon": m_wagon, "bulwark": m_bulwark},
    "modern":   {"worker": d_worker, "spearman": d_spearman, "archer": d_archer, **vehicles.ROSTER},
}
