#!/usr/bin/env python3
"""world_graph.py -- how the world's regions are tied together, as one picture: design/WORLD-GRAPH.svg / .png, and design/WORLD-GRAPH.md.

Two kinds of tie between regions (a region is a map's `region` line):
  DOORS    solid arrows: doors that cross from one region into another, merged per pair, coloured by the gates on them
           (open / time / know / item / flag, as tools/zone_audit.py reads them); width grows with the number of doors.
  THREADS  dashed arrows: something you earn in one region that matters in another -- a flag set there (a map line's `set`, a
           standoff's win `set=`) or a thing given there (`give=IT_..`, a map line's `give`), that is read elsewhere (a door's flag= /
           lock= / unless=, a move's needs=, a person's `when`, a gift's condition, a map line's condition).
Node size: maps in the region; label: maps and people.  usage: python3 tools/world_graph.py  (needs graphviz `dot`)
"""
import os, re, glob, json, collections, subprocess

import sys
# gdada copy: the game directory is the first argument (default: the current directory). The game must use the world text
# format of The Holy Temple (world/**/*.map with `map`, `region`, `door X Y -> MAP X Y face [gates]` lines; cast/**/*.json).
R = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
os.makedirs(os.path.join(R, "design"), exist_ok=True)
W = lambda *p: os.path.join(R, *p)

maps = {}
for f in glob.glob(W("world", "**", "*.map"), recursive=True):
    t = open(f, encoding="utf-8").read()
    m = re.search(r"^map (\w+)", t, re.M)
    if not m: continue
    reg = re.search(r"^region (\w+)", t, re.M)
    maps[m[1]] = dict(region=reg[1] if reg else "misc", text=t)
regions = sorted({m["region"] for m in maps.values()})
nmaps = collections.Counter(m["region"] for m in maps.values())

# people: a cast file stands somewhere; its region is the region of the map it is placed on (or its folder)
npc_region, npeople = {}, collections.Counter()
for f in glob.glob(W("cast", "**", "*.json"), recursive=True):
    try: c = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    if not isinstance(c, dict) or "id" not in c: continue
    reg = None
    for k in ("map", "home", "place"):
        if isinstance(c.get(k), str) and c[k] in maps: reg = maps[c[k]]["region"]; break
    if not reg:
        d = os.path.basename(os.path.dirname(f))
        reg = d if d in regions else None
    if not reg:   # placed by a map's npc line?
        for mn, m in maps.items():
            if re.search(r"^npc\s+%s\b" % re.escape(c["id"]), m["text"], re.M): reg = m["region"]; break
    if reg: npc_region[c["id"]] = reg; npeople[reg] += 1
    c["_file"] = f
    npc_region.setdefault("_files", {})[f] = (c["id"], reg)

# ---- doors ----------------------------------------------------------------------------------------------------------------
def kinds(rest):
    k = []
    if "hours=" in rest: k.append("time")
    if re.search(r"needs=(answered|asked):", rest): k.append("know")
    if "lock=IT_" in rest: k.append("item")
    if "flag=FL_" in rest or "unless=" in rest: k.append("flag")
    return k or ["open"]
doors = collections.defaultdict(list)          # (from_region, to_region) -> [kinds]
for name, m in maps.items():
    for d in re.finditer(r"^door \d+ \d+ -> (\w+) \d+ \d+ \w+(.*)$", m["text"], re.M):
        if d[1] in maps and maps[d[1]]["region"] != m["region"]:
            doors[(m["region"], maps[d[1]]["region"])].append(kinds(d[2]))

# ---- threads: setters and readers of flags and items ----------------------------------------------------------------------
setters, readers = collections.defaultdict(set), collections.defaultdict(set)
TOK = r"(FL_[A-Z0-9_]+|IT_[A-Z0-9_]+|Q_[A-Z0-9_]+)"
enc_region = {}
for name, m in maps.items():
    reg = m["region"]
    for line in m["text"].splitlines():
        for e in re.findall(r"\bencounter (E_[A-Z0-9_]+)", line): enc_region.setdefault(e, reg)
        for tok in re.findall(r"\b(?:set|give|ask|answer)[ =]" + TOK, line): setters[tok].add(reg)
        for tok in re.findall(r"\b(?:flag|lock|unless|needs)=(?:flag:|item:)?" + TOK, line): readers[tok].add(reg)
        for tok in re.findall(r"\b(?:if|when|needs)[ =:](?:flag:|item:|!)?" + TOK, line): readers[tok].add(reg)
for f in glob.glob(W("cast", "**", "*.json"), recursive=True):
    t = open(f, encoding="utf-8").read()
    _, reg = npc_region.get("_files", {}).get(f, (None, None))
    if not reg: continue
    for e in re.findall(r"\bencounter (E_[A-Z0-9_]+)", t): enc_region.setdefault(e, reg)
    for tok in re.findall(r'"when":\s*"[^"]*?' + TOK, t): readers[tok].add(reg)
    for tok in re.findall(r"\b(?:set|give|ask|answer)[ =]" + TOK, t): setters[tok].add(reg)
    for tok in re.findall(r'"(?:ask|answer)":\s*"' + TOK, t): setters[tok].add(reg)
# standoffs (world/encounters.txt): blocks start at "encounter E_X"; their region is where they are started
enc = open(W("world", "encounters.txt"), encoding="utf-8").read() if os.path.exists(W("world", "encounters.txt")) else ""
for blk in re.split(r"(?m)^(?=enc E_)", enc):
    m = re.match(r"enc (E_[A-Z0-9_]+)", blk)
    if not m or m[1] not in enc_region: continue
    reg = enc_region[m[1]]
    for tok in re.findall(r"\b(?:set|give|ask|answer)=" + TOK, blk): setters[tok].add(reg)
    for d in re.findall(r"\bdrop=([A-Z0-9_,]+)", blk):
        for tok in d.split(","): setters[tok].add(reg)
    for tok in re.findall(r"needs=(?:flag:|item:|knows:|heard:)" + TOK, blk): readers[tok].add(reg)
    for tok in re.findall(r"\b(?:item|deed|flag):" + TOK, blk): readers[tok].add(reg)
# loot / gifts / trades (world/loot.txt): the person's region
loot = open(W("world", "loot.txt"), encoding="utf-8").read() if os.path.exists(W("world", "loot.txt")) else ""
cur = None
for line in loot.splitlines():
    m = re.match(r"\s*(?:loot|gift|trade)\s+(\w+)", line)
    words = re.findall(r"\b[a-z]{2,4}_[a-z0-9_]+\b", line)
    for w in words:
        if w in npc_region: cur = npc_region[w]; break
    if not cur: continue
    for tok in re.findall(r"\b(?:flag|item):" + TOK, line): readers[tok].add(cur)
    its = re.findall(r"\bIT_[A-Z0-9_]+", line)
    if re.match(r"\s*(loot|gift)\b", line):
        for tok in its: setters[tok].add(cur)
    elif re.match(r"\s*trade\b", line) and len(its) >= 2:
        readers[its[0]].add(cur); setters[its[1]].add(cur)

threads = collections.defaultdict(set)          # (from_region, to_region) -> {tokens}
for tok, srcs in setters.items():
    for a in srcs:
        for b in readers.get(tok, ()):
            if a != b: threads[(a, b)].add(tok)

# ---- draw -------------------------------------------------------------------------------------------------------------------
COL = {"open": "#4f7d4f", "time": "#c08a2b", "know": "#3f6fb0", "item": "#9b4fa0", "flag": "#b0413e"}
def door_color(klist):
    ks = sorted({k for ks in klist for k in ks})
    return ":".join(COL[k] for k in ks) if len(ks) > 1 else COL[ks[0]]
start = maps.get("room", {}).get("region", "town")
g = ['digraph world {', '  graph [rankdir=LR, bgcolor="#141414", fontname="Helvetica", fontcolor="#dddddd", pad=0.4, nodesep=0.35, ranksep=1.1,'
     '         label="THE HOLY TEMPLE -- how the regions are tied together\\nsolid: doors (colour = gate: green open, amber time, blue knowledge, violet item, red flag)   '
     'dashed grey: threads (a flag, a thing or a clue earned in one region, used in another)", labelloc=t, fontsize=20];',
     '  node [shape=box, style="rounded,filled", fontname="Helvetica", fontcolor="#111111", color="#888888"];',
     '  edge [fontname="Helvetica", fontsize=9, fontcolor="#aaaaaa"];']
for r in regions:
    fill = "#e8d8a8" if r == start else ("#d9c7f0" if r == "index" else "#cfd8dc")
    w = 1.2 + 0.08 * nmaps[r]
    g.append(f'  "{r}" [label="{r.upper()}\\n{nmaps[r]} maps, {npeople[r]} people", fillcolor="{fill}", width={w:.2f}, fontsize={11 + min(9, nmaps[r] // 4)}];')
for (a, b), kl in sorted(doors.items()):
    g.append(f'  "{a}" -> "{b}" [color="{door_color(kl)}", penwidth={1 + min(4, len(kl) * 0.6):.1f}, label="{len(kl)}", arrowsize=0.7];')
for (a, b), toks in sorted(threads.items()):
    g.append(f'  "{a}" -> "{b}" [style=dashed, color="#8a8a8a", penwidth={0.8 + min(3, len(toks) * 0.4):.1f}, constraint=false, arrowsize=0.5];')
g.append("}")
dotf = W("design", "WORLD-GRAPH.dot")
open(dotf, "w").write("\n".join(g) + "\n")
for fmt in ("svg", "png"):
    subprocess.run(["dot", f"-T{fmt}", "-Gdpi=110" if fmt == "png" else "-Gdpi=72", dotf, "-o", W("design", f"WORLD-GRAPH.{fmt}")], check=True)

# ---- the table --------------------------------------------------------------------------------------------------------------
deg = collections.Counter()
for (a, b) in list(doors) + list(threads): deg[a] += 1; deg[b] += 1
o = ["# World graph: how the regions are tied together", "",
     "Generated by `tools/world_graph.py` (picture: `WORLD-GRAPH.svg` / `.png`). Doors are ways to walk between regions; threads are",
     "things earned in one region that matter in another: a flag, a thing, or a clue (a question asked or answered there, used as a standoff's clue key elsewhere).",
     " Regenerate after any world change.", "",
     f"{len(regions)} regions, {len(maps)} maps, {sum(npeople.values())} placed people; {sum(len(v) for v in doors.values())} doors between regions "
     f"({len(doors)} region pairs); {sum(len(v) for v in threads.values())} threads ({len(threads)} region pairs).", "",
     "| region | maps | people | doors out | doors in | threads out | threads in | ties |", "|---|---|---|---|---|---|---|---|"]
for r in sorted(regions, key=lambda r: -deg[r]):
    o.append(f"| {r} | {nmaps[r]} | {npeople[r]} | {sum(len(v) for (a, b), v in doors.items() if a == r)} | "
             f"{sum(len(v) for (a, b), v in doors.items() if b == r)} | {sum(len(v) for (a, b), v in threads.items() if a == r)} | "
             f"{sum(len(v) for (a, b), v in threads.items() if b == r)} | {deg[r]} |")
o += ["", "## Threads", "", "| from | to | what |", "|---|---|---|"]
for (a, b), toks in sorted(threads.items()):
    o.append(f"| {a} | {b} | {', '.join(sorted(toks))} |")
# data for the interactive page (design/WORLD-GRAPH.json)
areas = collections.defaultdict(list)
if os.path.exists(W("world", "areas.txt")):
    for line in open(W("world", "areas.txt"), encoding="utf-8"):
        m = re.match(r'area \w+ \w+ "([^"]*)" "([^"]*)" (\S+)', line)
        if not m: continue
        for pat in m[3].split(","):
            if pat.startswith("@") and pat[1:] in regions: areas[pat[1:]].append(m[1])
            elif pat.rstrip("*") and any(mn.startswith(pat.rstrip("*")) for mn in maps):
                mn = next(mn for mn in maps if mn.startswith(pat.rstrip("*")))
                if m[1] not in areas[maps[mn]["region"]]: areas[maps[mn]["region"]].append(m[1])
names = {}
for line in open(W("Src", "Defs.HC"), encoding="latin1"):
    m = re.match(r"#define (FL_\w+)\s+\d+\s*//(.*)", line)
    if m: names[m[1]] = m[2].strip()
for line in open(W("world", "items.txt"), encoding="utf-8"):
    m = re.match(r'item (IT_\w+) "([^"]*)"', line)
    if m: names[m[1]] = "the thing: " + m[2].capitalize()
for f in glob.glob(W("world", "questions*.txt")):
    for line in open(f, encoding="utf-8"):
        m = re.match(r'q (\w+) [^"]*"([^"]*)"', line)
        if m: names["Q_" + m[1]] = "the question: " + m[2].replace("|", " ")
json.dump({
  "start": start,
  "names": {t: names.get(t, t) for t in sorted({t for v in threads.values() for t in v})},
  "regions": [{"id": r, "maps": nmaps[r], "people": npeople[r], "areas": areas.get(r, [])[:40]} for r in regions],
  "doors": [{"from": a, "to": b, "n": len(kl), "gates": sorted({k for ks in kl for k in ks})} for (a, b), kl in sorted(doors.items())],
  "threads": [{"from": a, "to": b, "what": sorted(t)} for (a, b), t in sorted(threads.items())],
}, open(W("design", "WORLD-GRAPH.json"), "w"), indent=1)
open(W("design", "WORLD-GRAPH.md"), "w").write("\n".join(o) + "\n")
print(f"world_graph: {len(regions)} regions, {sum(len(v) for v in doors.values())} doors in {len(doors)} pairs, "
      f"{sum(len(v) for v in threads.values())} threads in {len(threads)} pairs -> design/WORLD-GRAPH.svg/.png/.md")
