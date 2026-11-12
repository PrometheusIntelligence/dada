"""Sprite QA: the checks a pixel artist does by eye, as numbers.

Units (16x16) and buildings (32x32, 48x48) share the checks; thresholds differ where the
subject differs (a building needs less team colour share than a 14 px soldier).
"""
import kit

# min_xor was 0.22 until R6: the tank destroyer that passed it was a tall slab the usability seat read as a fridge, and the
# tracked vehicles share a track base, so a floor above 0.19 forced unreadable shapes. Role signifiers (gun length, hull height) carry the rest.
UNIT = dict(min_team_px=12, min_team_share=0.12, min_fill=40, max_fill_share=0.75, min_xor=0.19)
# Vehicles are drawn on a 24 px canvas (a tile and a half): more body, so more team colour in absolute pixels.
UNIT_BIG = dict(min_team_px=22, min_team_share=0.10, min_fill=110, max_fill_share=0.8, min_xor=0.19)
BUILDING = dict(min_team_px=14, min_team_share=0.04, max_team_share=0.20, min_fill=0, max_fill_share=0.85, min_xor=0.15)


def _px(rows):
    return {(x, y): c for y, r in enumerate(rows) for x, c in enumerate(r) if c != "."}


def validate(era, kind, rows, th=UNIT, frame=0):
    tag = f"{era}/{kind}" + (f"#{frame}" if frame else "")
    h = len(rows); w = len(rows[0]) if rows else 0
    if any(len(r) != w for r in rows):
        return [f"{tag}: ragged rows"]
    msgs = []
    p = _px(rows)
    body = {k: c for k, c in p.items() if c not in "OS"}
    team = [c for c in body.values() if kit.LEGEND[c][0] == "team"]
    if len(team) < th["min_team_px"]:
        msgs.append(f"{tag}: only {len(team)} team-colour pixels (need {th['min_team_px']})")
    if body and "max_team_share" in th and len(team) / len(body) > th["max_team_share"]:
        msgs.append(f"{tag}: team colour is {len(team) / len(body):.1%} of the body (max {th['max_team_share']:.0%}); the building would read as a flag")
    if body and len(team) / len(body) < th["min_team_share"]:
        msgs.append(f"{tag}: team colour is {len(team) / len(body):.1%} of the body (need {th['min_team_share']:.1%})")
    if len(body) < th["min_fill"] or len(body) > th["max_fill_share"] * w * h:
        msgs.append(f"{tag}: {len(body)} body pixels outside the allowed fill")
    if any(x in (0, w - 1) or y == 0 for (x, y) in body):
        msgs.append(f"{tag}: touches the canvas edge, so the outline is clipped")
    for (x, y) in body:
        if not any((x + dx, y + dy) in body for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            msgs.append(f"{tag}: stray pixel at {x},{y}"); break
    return msgs


def silhouette(rows):
    return {k for k, c in _px(rows).items() if c != "S"}


def silhouette_pairs(era, roster, min_diff):
    msgs, kinds = [], list(roster)
    sil = {k: silhouette(roster[k]) for k in kinds}
    for i, a in enumerate(kinds):
        for b in kinds[i + 1:]:
            u = len(sil[a] | sil[b]); d = len(sil[a] ^ sil[b])
            if d / u < min_diff:
                msgs.append(f"{era}: {a} and {b} silhouettes differ by only {d / u:.1%} (min {min_diff:.0%})")
    return msgs


def frame_pair(era, kind, f0, f1, min_changed=8):
    """A walk cycle must actually move: frame 2 differs from frame 1 by at least a few pixels."""
    a, b = _px(f0), _px(f1)
    changed = sum(1 for k in set(a) | set(b) if a.get(k) != b.get(k))
    return [] if changed >= min_changed else [f"{era}/{kind}: walk frames differ by {changed} px (need {min_changed})"]


def luminance(hex_colour):
    """WCAG relative luminance of '#rrggbb'."""
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(int(hex_colour[i:i + 2], 16)) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def sides_apart(teams, min_ratio=2.0):
    """The sides must differ in brightness, not only hue (colour-blind and greyscale players)."""
    msgs = []
    for i, a in enumerate(teams):
        for b in teams[i + 1:]:
            la, lb = sorted((luminance(a[0]), luminance(b[0])))
            if (lb + .05) / (la + .05) < min_ratio:
                msgs.append(f"teams {a[0]} and {b[0]} differ in luminance by only {(lb + .05) / (la + .05):.2f}:1 (min {min_ratio}:1)")
    return msgs


def factions_ok(facs, min_ratio=2.0):
    """Every light faction must sit at least min_ratio from every dark one in luminance; emblems and flags must be real."""
    import kit as _k
    msgs = []
    for a, fa in facs.items():
        if fa["emblem"] not in _k.EMBLEMS: msgs.append(f"faction {a}: unknown emblem {fa['emblem']}")
        if fa["flag"] not in ("square", "swallow", "pennant"): msgs.append(f"faction {a}: unknown flag {fa['flag']}")
        for b, fb in facs.items():
            if fa["tone"] == "light" and fb["tone"] == "dark":
                la, lb = luminance(fa["main"]), luminance(fb["main"])
                r = (la + .05) / (lb + .05)
                if r < min_ratio: msgs.append(f"factions {a} (light) and {b} (dark) differ in luminance by only {r:.2f}:1 (min {min_ratio}:1)")
    emb = [f["emblem"] for f in facs.values()]
    if len(set(emb)) != len(emb): msgs.append("two factions share an emblem")
    return msgs
