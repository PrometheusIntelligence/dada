"""Rate every panel seat from the ledger, so a run can seat the critics that have earned it.

    python scripts/rate_seats.py [--ledger PATH]      # writes references/seat-ratings.json and .md
    python scripts/rate_seats.py --check              # exit non-zero if the committed ratings are stale

What a seat is rated on (all per seat, over every run in the ledger):

- **Converted objections**: an OBJECT in round n followed by a PASS from the same seat later in the same run. The
  work changed and the seat accepted it, so the objection moved the work.
- **Credited outcomes**: findings the log's resolution tables credit to the seat. ADAPT and SCRAP count as
  adopted. OVERRULE is a judgment call that went against the seat. REFUTED, an objection whose premise failed a
  measurement, counts against the seat's precision. DEFERRED is neutral.
- **Precision**: (adopted + converted + 1) / (adopted + converted + overruled + refuted + 2), a Laplace-smoothed
  share of the seat's objections that moved the work.
- **Yield**: adopted plus converted per round sat, capped at 1 after dividing by 0.6. A seat that never objects
  has yield 0, and one that sits three or more rounds without an objection is flagged `rubber-stamp?`.
- **Grade lift**: the mean human grade of the runs the seat sat on, minus the mean of all graded runs, shrunk
  toward 0 by n / (n + 3). Grades are the owner's, verbatim, from GRADES.md, never inferred.
- **Reliability**: verdicts filed / seats convened (NOT REPORTED counts against it).

score = 0.40 * precision + 0.30 * yield + 0.20 * clamp(0.5 + lift / 4) + 0.10 * reliability.

The confidence of a score is the number of rounds behind it. scripts/pick_panel.py adds an exploration bonus to
seats with few rounds, so an untried seat gets a chance and one bad run cannot bench a seat forever.
"""
import json
import math
import pathlib
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
REPO = SKILL.parents[1]
LEDGER = REPO / "ledger" / "runs.jsonl"
RATINGS_JSON = SKILL / "references" / "seat-ratings.json"  # shipped with the skill, so an installed copy has it
RATINGS_MD = SKILL / "references" / "seat-ratings.md"
ADOPTED = {"ADAPT", "SCRAP"}


def load_runs(path):
    return [json.loads(l) for l in pathlib.Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def load_seats():
    seats = {}
    for f in (SKILL / "seats").glob("crit_*.md"):
        front = f.read_text(encoding="utf-8").split("---")[1]
        seats[f.stem] = {k.strip(): json.loads(v) for k, v in (l.split(":", 1) for l in front.strip().splitlines())}
    return seats


def rate(runs, seats):
    graded = [r["grade"]["points"] for r in runs if r.get("grade")]
    mean_grade = sum(graded) / len(graded) if graded else None
    stats = {s: {"runs": set(), "rounds": 0, "objections": 0, "passes": 0, "not_reported": 0, "converted": 0,
                 "adopted": 0, "overruled": 0, "refuted": 0, "deferred": 0, "grades": [], "last": None} for s in seats}
    for r in runs:
        by_seat = {}
        for sr in r["seat_rounds"]:
            by_seat.setdefault(sr["seat"], []).append(sr)
        for sid, rows in by_seat.items():
            if sid not in stats:
                continue
            st = stats[sid]
            st["runs"].add(r["id"])
            st["last"] = max(st["last"] or "", r["date"])
            rows.sort(key=lambda x: int(x["round"][1:]))
            for i, row in enumerate(rows):
                st["rounds"] += 1
                if row["verdict"] == "OBJECT":
                    st["objections"] += 1
                    if any(later["verdict"] == "PASS" for later in rows[i + 1:]):
                        st["converted"] += 1
                elif row["verdict"] == "PASS":
                    st["passes"] += 1
                else:
                    st["not_reported"] += 1
            if r.get("grade"):
                st["grades"].append(r["grade"]["points"])
        for o in r.get("outcomes", []):
            share = 1 / len(o["seats"])
            for sid in o["seats"]:
                if sid not in stats:
                    continue
                key = {"ADAPT": "adopted", "SCRAP": "adopted", "OVERRULE": "overruled", "REFUTED": "refuted",
                       "DEFERRED": "deferred"}[o["outcome"]]
                stats[sid][key] += share
    out = {}
    for sid, st in stats.items():
        moved = st["adopted"] + st["converted"]
        precision = (moved + 1) / (moved + st["overruled"] + st["refuted"] + 2)
        yield_ = min(1.0, (moved / st["rounds"]) / 0.6) if st["rounds"] else 0.0
        n = len(st["grades"])
        lift = ((sum(st["grades"]) / n - mean_grade) * n / (n + 3)) if n and mean_grade is not None else 0.0
        reliability = (st["rounds"] - st["not_reported"]) / st["rounds"] if st["rounds"] else 1.0
        score = 0.40 * precision + 0.30 * yield_ + 0.20 * max(0.0, min(1.0, 0.5 + lift / 4)) + 0.10 * reliability
        flags = []
        if st["rounds"] >= 3 and st["objections"] == 0:
            flags.append("rubber-stamp?")
        if st["refuted"] >= 2 and st["refuted"] > st["adopted"]:
            flags.append("premise-prone")
        out[sid] = {
            "label": seats[sid]["label"], "persona_hash": seats[sid]["persona_hash"],
            "runs": len(st["runs"]), "rounds": st["rounds"], "objections": st["objections"], "passes": st["passes"],
            "converted": st["converted"], "adopted": round(st["adopted"], 2), "overruled": round(st["overruled"], 2),
            "refuted": round(st["refuted"], 2), "deferred": round(st["deferred"], 2),
            "graded_runs": n, "grade_lift": round(lift, 3), "precision": round(precision, 3), "yield": round(yield_, 3),
            "reliability": round(reliability, 3), "score": round(score, 3) if st["rounds"] else None,
            "last_sat": st["last"], "flags": flags,
        }
    return out, mean_grade


def render_md(ratings, runs, mean_grade):
    sat = sorted((r for r in ratings.items() if r[1]["rounds"]), key=lambda kv: (-kv[1]["score"], -kv[1]["rounds"]))
    unsat = sorted(sid for sid, r in ratings.items() if not r["rounds"])
    lines = [
        "# Seat ratings", "",
        "Generated by `scripts/rate_seats.py` from `ledger/runs.jsonl` in the dada repository; do not edit by hand.",
        f"{len(runs)} runs, {sum(len(r['seat_rounds']) for r in runs)} seat-rounds, "
        f"{sum(len(r.get('outcomes', [])) for r in runs)} credited outcomes, "
        f"{sum(1 for r in runs if r.get('grade'))} human grades (mean {mean_grade:.2f} on a 4.3 scale)." if mean_grade is not None else "",
        "",
        "How to read it: `score` is 0.40 precision + 0.30 yield + 0.20 grade lift + 0.10 reliability (see the script's",
        "docstring). `rounds` is the confidence: a score on 2 rounds is a hint, on 20 it is a record. Older runs were",
        "imported from their logs before seats had persona files, so their rows carry `pre-registry` and count toward",
        "the seat, not toward a persona version. Use `scripts/pick_panel.py` to choose a panel from these numbers.", "",
        "| Seat | Score | Rounds | Runs | Objections | Converted | Adopted | Overruled | Refuted | Grade lift | Flags |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for sid, r in sat:
        lines.append(f"| [{r['label']}](../seats/{sid}.md) | {r['score']:.3f} | {r['rounds']} | {r['runs']} | {r['objections']} | "
                     f"{r['converted']} | {r['adopted']:g} | {r['overruled']:g} | {r['refuted']:g} | {r['grade_lift']:+.2f} | "
                     f"{', '.join(r['flags'])} |")
    lines += ["", f"Never seated yet ({len(unsat)}): " + ", ".join(f"[`{s}`](../seats/{s}.md)" for s in unsat), ""]
    return "\n".join(lines)


def main(argv):
    ledger = argv[argv.index("--ledger") + 1] if "--ledger" in argv else LEDGER
    runs = load_runs(ledger)
    ratings, mean_grade = rate(runs, load_seats())
    js = json.dumps({"runs": len(runs), "mean_grade": mean_grade, "seats": ratings}, indent=2, ensure_ascii=False) + "\n"
    md = render_md(ratings, runs, mean_grade)
    if "--check" in argv:
        stale = [p for p, t in ((RATINGS_JSON, js), (RATINGS_MD, md)) if not p.exists() or p.read_text(encoding="utf-8") != t]
        if stale:
            raise SystemExit(f"stale ratings (run scripts/rate_seats.py): {[str(p) for p in stale]}")
        print("ratings current")
        return
    RATINGS_JSON.write_text(js, encoding="utf-8", newline="\n")
    RATINGS_MD.write_text(md, encoding="utf-8", newline="\n")
    top = sorted((v for v in ratings.values() if v["rounds"]), key=lambda v: -v["score"])[:5]
    print("top:", ", ".join(f"{v['label']} {v['score']:.3f} ({v['rounds']} rounds)" for v in top))


if __name__ == "__main__":
    main(sys.argv[1:])
