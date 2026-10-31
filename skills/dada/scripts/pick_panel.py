"""Choose a DADA panel: the seats the rules require, then the best-rated and one rotated seat for the rest.

    python scripts/pick_panel.py --mode adaptive --run-type full [--size 7] [--project NAME]
        [--money] [--data-graphic] [--signs] [--not-inspectable] [--explore 1] [--exclude SEAT ...] [--json]

1. Required seats come from SKILL.md: the mode's required critics (one seat per reference), the run type's panel
   minimum, and the context rules (dada-lessons 43-57): Cairo whenever the artifact can be inspected (47), Tufte as
   the instrumentation seat on any data graphic (43, 46), Papanek on any money decision (29), and Cairo's security
   duty on anything that signs or approves (53).
2. Flexible seats are ranked by their rating shrunk toward a prior of 0.60 by rounds / (rounds + 3), so two lucky
   rounds do not outrank forty good ones. One seat per concern, so the panel stays diverse.
3. Rotation: `--explore` slots (default 1 when two or more seats are flexible) go to the least-tried seats, chosen
   deterministically from the project name so different projects rotate different seats in. This is how a seat
   that has never sat earns a rating.
4. Rest: a flexible seat that sat in each of the last three runs without moving the work (no converted or adopted
   objection) sits this one out.
5. The dotted-pair rule: if no two chosen seats are joined by a dotted edge, the last flexible seat is swapped for a
   rival of a required seat.

Prints the panel with the reason for every seat and the path of each seat file, whose prompt the conductor fills.
"""
import argparse
import hashlib
import json
import pathlib
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
REPO = SKILL.parents[1]
RATINGS = REPO / "ledger" / "ratings.json"
LEDGER = REPO / "ledger" / "runs.jsonl"
PRIOR, K = 0.60, 3

MODE_REQUIRED = {
    "adaptive": ["crit_prov_debord", "crit_prov_shklovsky", "crit_inc_holmes", "crit_inc_mace"],
    "autonomous": ["crit_apollo_wolfflin", "crit_apollo_gombrich", "crit_dionys_nietzsche", "crit_dionys_venturi",
                   "crit_rupt_shklovsky", "crit_rupt_marinetti", "crit_detach_ortega", "crit_detach_sontag"],
}
MODE_MIN_EXTRA = {"adaptive": 3, "autonomous": 1}
RUN_TYPE_REQUIRED = {  # these run types replace the mode's minimum (SKILL.md, Run type table)
    "polish": ["crit_evid_cairo", "crit_use_krug", "crit_prov_debord"],
    "extend": ["crit_evid_cairo", "crit_use_krug", "crit_prov_debord"],
    "landing": ["crit_formal_arnheim", "crit_evid_cairo", "crit_use_krug", "crit_prov_debord"],
}


def load_seats():
    seats = {}
    for f in (SKILL / "seats").glob("crit_*.md"):
        front = f.read_text(encoding="utf-8").split("---")[1]
        seats[f.stem] = {k.strip(): json.loads(v) for k, v in (l.split(":", 1) for l in front.strip().splitlines())}
    return seats


def shrunk(r):
    if not r or not r.get("rounds"):
        return PRIOR
    n = r["rounds"]
    return r["score"] * n / (n + K) + PRIOR * K / (n + K)


def resting(runs, seat):
    recent = [r for r in runs if r["seat_rounds"]][-3:]
    if len(recent) < 3:
        return False
    for r in recent:
        rows = sorted((x for x in r["seat_rounds"] if x["seat"] == seat), key=lambda x: int(x["round"][1:]))
        if not rows:
            return False
        moved = any(rows[i]["verdict"] == "OBJECT" and any(l["verdict"] == "PASS" for l in rows[i + 1:]) for i in range(len(rows)))
        moved = moved or any(seat in o["seats"] and o["outcome"] in ("ADAPT", "SCRAP") for o in r.get("outcomes", []))
        if moved:
            return False
    return True


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["adaptive", "autonomous"], required=True)
    ap.add_argument("--run-type", choices=["full", "polish", "extend", "landing", "lite"], default="full")
    ap.add_argument("--size", type=int)
    ap.add_argument("--project", default="")
    ap.add_argument("--money", action="store_true")
    ap.add_argument("--data-graphic", action="store_true")
    ap.add_argument("--signs", action="store_true")
    ap.add_argument("--not-inspectable", action="store_true")
    ap.add_argument("--explore", type=int)
    ap.add_argument("--exclude", nargs="*", default=[])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    seats = load_seats()
    ratings = json.loads(RATINGS.read_text(encoding="utf-8"))["seats"] if RATINGS.exists() else {}
    runs = [json.loads(l) for l in LEDGER.read_text(encoding="utf-8").splitlines() if l.strip()] if LEDGER.exists() else []

    required = {}
    base = RUN_TYPE_REQUIRED.get(a.run_type, MODE_REQUIRED[a.mode])
    for s in base:
        required[s] = f"required by the {a.run_type if a.run_type in RUN_TYPE_REQUIRED else a.mode} panel minimum"
    if not a.not_inspectable:
        required.setdefault("crit_evid_cairo", "required: the artifact can be inspected, so the measurement seat sits from R0 (lessons 43, 47)")
    if a.data_graphic:
        required.setdefault("crit_evid_tufte", "required: a data graphic gets the instrumentation seat (lessons 43, 46)")
    if a.money:
        required.setdefault("crit_soc_papanek", "required: a money decision gets the Social seat (lesson 29)")
    duties = {}
    if a.signs:
        duties["crit_evid_cairo"] = "brief the security-read duty: every action that signs or approves (lesson 53)"
    for s in a.exclude:
        required.pop(s, None)

    if a.run_type in RUN_TYPE_REQUIRED:
        size = a.size or max(4, len(required))
    elif a.run_type == "lite":
        size = a.size or max(5, len(required))
    else:
        size = a.size or len(MODE_REQUIRED[a.mode]) + MODE_MIN_EXTRA[a.mode] + (1 if "crit_evid_cairo" not in MODE_REQUIRED[a.mode] else 0)
    size = max(size, len(required))
    flexible = size - len(required)
    explore = a.explore if a.explore is not None else (1 if flexible >= 2 else 0)
    explore = min(explore, flexible)

    concerns_taken = {seats[s]["concern"] for s in required}
    pool = [s for s in seats if s not in required and s not in a.exclude]
    rested = [s for s in pool if resting(runs, s)]
    pool = [s for s in pool if s not in rested]

    chosen = {}
    exploit_n = flexible - explore
    for s in sorted(pool, key=lambda s: -shrunk(ratings.get(s))):
        if len([c for c in chosen if chosen[c].startswith("rated")]) >= exploit_n:
            break
        if seats[s]["concern"] in concerns_taken or not ratings.get(s, {}).get("rounds"):
            continue
        chosen[s] = f"rated: shrunk score {shrunk(ratings.get(s)):.3f} over {ratings[s]['rounds']} rounds"
        concerns_taken.add(seats[s]["concern"])
    salt = int(hashlib.sha256(a.project.encode()).hexdigest(), 16)
    least = sorted((s for s in pool if s not in chosen and seats[s]["concern"] not in concerns_taken),
                   key=lambda s: (ratings.get(s, {}).get("rounds", 0), (int(hashlib.sha256(s.encode()).hexdigest(), 16) ^ salt) % 997))
    for s in least[:explore]:
        chosen[s] = f"rotation: {ratings.get(s, {}).get('rounds', 0)} rounds on record, seated to earn a rating"
        concerns_taken.add(seats[s]["concern"])

    panel = {**required, **chosen}
    pairs = sorted({tuple(sorted((x, y))) for x in panel for y in seats[x]["rivals"] if y in panel})
    if not pairs and chosen:
        for req in required:
            rivals = [r for r in seats[req]["rivals"] if r not in panel and r not in a.exclude]
            if rivals:
                drop = list(chosen)[-1]
                del panel[drop]
                panel[rivals[0]] = f"dotted-pair rule: rival of {req} (replaces {drop})"
                pairs = [(req, rivals[0])]
                break

    rows = [{"seat": s, "label": seats[s]["label"], "why": why, "duty": duties.get(s),
             "score": ratings.get(s, {}).get("score"), "rounds": ratings.get(s, {}).get("rounds", 0),
             "file": f"seats/{s}.md"} for s, why in panel.items()]
    result = {"mode": a.mode, "run_type": a.run_type, "size": len(rows), "panel": rows,
              "dotted_pairs": [list(p) for p in pairs], "rested": rested}
    if a.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    print(f"Panel for a {a.mode} {a.run_type} run ({len(rows)} seats, one agent each, launched three at a time):\n")
    print("| Seat | Why | Score | Rounds | File |\n|---|---|---|---|---|")
    for r in rows:
        why = r["why"] + (f"; {r['duty']}" if r["duty"] else "")
        print(f"| {r['label']} | {why} | {'' if r['score'] is None else format(r['score'], '.3f')} | {r['rounds']} | `{r['file']}` |")
    print(f"\nDotted pairs on the panel: {', '.join(f'{x} -.- {y}' for x, y in pairs) or 'NONE (add a rival by hand)'}")
    if rested:
        print(f"Resting this run (sat the last three runs without moving the work): {', '.join(rested)}")


if __name__ == "__main__":
    main(sys.argv[1:])
