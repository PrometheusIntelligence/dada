"""Neutral map props: the three kinds of mine in the modern era, 24x24, drawn over a captured outpost's flag."""
from kit import Sprite


def _s(name):
    return Sprite(name, (12, 22.6, 9.5, 1.5), w=24, h=24)


def metal_mine():
    s = _s("mine_timber")
    s.poly([(2, 21), (5, 13), (12, 10), (19, 21)], "gunmetal")        # heaped ore
    s.dots([(6, 14), (9, 12), (11, 16), (7, 18), (13, 13)], "steel", "hi")
    s.line(13, 21, 17, 4, "iron"); s.line(21, 21, 17, 4, "iron")      # headframe legs
    s.rect(14, 11, 6, 1, "iron"); s.rect(15, 16, 5, 1, "iron")        # cross braces
    s.ellipse(17, 4, 2.2, 2.2, "steel"); s.dots([(17, 4)], "iron", "dk")   # sheave wheel
    s.rect(2, 19, 9, 3, "iron")                                       # ore cart
    s.ellipse(4, 22, 1.4, 1.4, "rubber"); s.ellipse(9, 22, 1.4, 1.4, "rubber")
    return s


def oil_field():
    s = _s("mine_salvage")
    s.line(5, 22, 10, 1, "iron"); s.line(15, 22, 10, 1, "iron")       # derrick legs
    for y, w in ((6, 3), (10, 4), (14, 5), (18, 6)):
        s.rect(10 - w, y, 2 * w, 1, "iron")                            # cross bars
    s.rect(1, 20, 18, 2, "gunmetal")                                   # base plate
    s.rect(17, 13, 6, 8, "steel"); s.ellipse(20, 13, 3, 1.5, "steel")  # storage tank
    s.rect(17, 16, 6, 1, "gunmetal")
    s.dots([(10, 2)], "fire", "hi"); s.dots([(10, 3)], "fire", "mid")  # flare at the top
    return s


def uranium_mine():
    s = _s("mine_uranium")
    s.poly([(4, 22), (7, 9), (17, 9), (20, 22)], "concrete")           # cooling tower
    s.rect(5, 16, 14, 3, "glow")                                       # hazard band
    s.ellipse(12, 6, 4.5, 3, "glow")                                   # glowing vapour
    s.rect(1, 17, 4, 5, "olive"); s.rect(1, 18, 4, 1, "glow")          # waste drum
    s.rect(20, 18, 3, 4, "olive"); s.rect(20, 19, 3, 1, "glow")
    return s


ROSTER = {"mine_timber": metal_mine, "mine_salvage": oil_field, "mine_uranium": uranium_mine}
