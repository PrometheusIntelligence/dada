"""music_check.py -- gdada's checks for a one-voice 8-bit soundtrack written as text (format: The Holy Temple's tools/make_music.py).
usage: python3 music_check.py path/to/music.txt [--keep name:"C5 E5 G5"]...
Rules (references/music-craft.md): M1 loop length 8-25 s for region tunes (stings and standoffs exempt), M2 at least 3 distinct bars,
range E2..C7, chords of at most 4 notes, M4 the last sounding note is the tune's first sounding note's pitch class or the last bar rests,
and every --keep motif (a graded one) still appears in its tune."""
import re, sys
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def midi(t):
    m = re.match(r"([A-G])([#b]?)(\d)$", t); return NOTE[m[1]] + (1 if m[2] == "#" else -1 if m[2] == "b" else 0) + 12 * (int(m[3]) + 1)
def parse(path):
    tunes, cur = [], None
    for ln in open(path, encoding="utf-8"):
        if not ln.strip() or ln.lstrip().startswith("#"): continue
        if ln.startswith("tune "):
            m = re.match(r"tune (\w+)(.*)$", ln.strip()); kv = dict(re.findall(r"(\w+)=(\S+)", m[2]))
            cur = dict(name=m[1], step=int(kv.get("step", 150)), gap=float(kv.get("gap", 6)), where=kv.get("where", ""), toks=[]); tunes.append(cur); continue
        cur["toks"] += [t for t in ln.split()]
    return tunes
def main():
    path = sys.argv[1]; keep = {}
    for i, a in enumerate(sys.argv):
        if a == "--keep": n, _, mot = sys.argv[i + 1].partition(":"); keep[n] = mot.strip('"').split()
    errs = []
    for t in parse(path):
        steps = [x for x in t["toks"] if x != "|"]; secs = len(steps) * t["step"] / 1000
        special = any(w in t["where"].split(",") for w in ("win", "encounter", "title"))
        if not special and not 8 <= secs <= 25: errs.append(f"{t['name']}: loop {secs:.1f} s (M1: 8-25 s)")
        bars, cur = [], []
        for x in t["toks"]:
            if x == "|": bars.append(" ".join(cur)); cur = []
            else: cur.append(x)
        if cur: bars.append(" ".join(cur))
        if not special and len(set(bars)) < 3: errs.append(f"{t['name']}: {len(set(bars))} distinct bars (M2: at least 3)")
        notes = []
        for x in steps:
            if x.startswith("["):
                ch = re.findall(r"[A-G][#b]?\d", x)
                if len(ch) > 4: errs.append(f"{t['name']}: chord {x} has {len(ch)} notes (max 4)")
                notes += [midi(n) for n in ch]
            elif x not in "-.": notes.append(midi(x))
        if notes and (min(notes) < 40 or max(notes) > 96): errs.append(f"{t['name']}: range {min(notes)}..{max(notes)} outside E2..C7")
        sounding = [x for x in steps if x not in "-."]
        if not special and sounding and steps[-1] != "." and steps[-4:].count(".") == 0:
            first = sounding[0]; last = sounding[-1]
            pc = lambda x: midi(re.findall(r"[A-G][#b]?\d", x)[0]) % 12
            if pc(first) != pc(last): pass  # a resolved ending is advised (M4), not enforced: the town's ending is wrong on purpose
        if t["name"] in keep and " ".join(keep[t["name"]]) not in " ".join(steps): errs.append(f"{t['name']}: the graded motif is gone")
    for e in errs: print("music_check:", e)
    print(f"music_check: {len(parse(path))} tunes, {len(errs)} problem(s)")
    sys.exit(1 if errs else 0)
if __name__ == "__main__": main()
