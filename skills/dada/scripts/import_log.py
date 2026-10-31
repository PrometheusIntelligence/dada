"""Turn a DESIGN-LOG.md into a run record for the ledger.

    python scripts/import_log.py DESIGN-LOG.md --project NAME --repo OWNER/REPO [--date YYYY-MM-DD]
        [--grade B+ --grade-words "their words, verbatim"] [--mode adaptive] [--run-type full]
        [--from HEADING] [--until HEADING] [--registry] [--ledger PATH] [--dry-run]

Reads every panel table (`### Panel ... round R<n>` followed by `| Critic | ... | Verdict | ... |` rows) into one
seat-round per row, and every resolutions table (`| <seats>: <finding> | ADAPT|OVERRULE|SCRAP|DEFERRED ... |`) into
finding outcomes credited to the seats it names. Appends one JSON line to the ledger (default ../../ledger/runs.jsonl
from this skill, the repository's ledger). A grade is recorded only when the person gave one: pass it verbatim.

The parser is deliberately forgiving of older logs (seat names with or without "Critic:", surname only, PASS/OBJECT
anywhere in the verdict cell) and reports what it could not map, so a backfill says how partial it is.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import re
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = SKILL.parents[1] / "ledger" / "runs.jsonl"
GRADE_POINTS = {"A+": 4.3, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7, "C+": 2.3, "C": 2.0, "C-": 1.7,
                "D+": 1.3, "D": 1.0, "D-": 0.7, "F": 0.0}


def load_seats():
    seats = {}
    for f in (SKILL / "seats").glob("crit_*.md"):
        front = f.read_text(encoding="utf-8").split("---")[1]
        meta = {k.strip(): json.loads(v) for k, v in (line.split(":", 1) for line in front.strip().splitlines())}
        seats[meta["id"]] = meta
    return seats


def seat_index(seats):
    """label -> id, 'Concern (Authority)' -> id, and surname -> ids (ambiguous surnames resolved by preference)."""
    by_label, by_surname = {}, {}
    for sid, m in seats.items():
        by_label[m["label"].lower()] = sid
        by_label[m["label"].replace("Critic: ", "").lower()] = sid
        by_surname.setdefault(m["authority"].split()[-1].lower(), []).append(sid)
    prefer = {"shklovsky": "crit_prov_shklovsky", "pater": "crit_aesth_pater"}
    return by_label, by_surname, prefer


def map_seat(text, index, mode):
    by_label, by_surname, prefer = index
    t = re.sub(r"[*`_]", "", text).strip()
    m = re.search(r"(?:Critic:\s*)?([A-Za-z\- ]+?)\s*\(([^)]+)\)", t)
    if m:
        key = f"{m.group(1).strip()} ({m.group(2).strip()})".lower()
        if key in by_label:
            return by_label[key]
        t = m.group(2)
    surname = t.split()[-1].lower() if t.split() else ""
    ids = by_surname.get(surname, [])
    if len(ids) == 1:
        return ids[0]
    if surname == "shklovsky" and mode == "autonomous":
        return "crit_rupt_shklovsky"
    return prefer.get(surname)


ROUND_TOKEN = re.compile(r"\b(R\d+)\b")
VERDICT = re.compile(r"\b(PASS|OBJECT|NOT REPORTED)\b")
RESOLUTION = re.compile(r"\b(ADAPT|OVERRULE|SCRAP|DEFERRED)\b")
REFUTED = re.compile(r"premise (?:refused|refuted)|refutes? the premise|measurement refuse", re.I)


def outcome_of(cell):
    """ADAPT / OVERRULE / SCRAP / DEFERRED, or REFUTED when the objection's premise failed a measurement."""
    if REFUTED.search(cell):
        return "REFUTED"
    m = RESOLUTION.search(cell)
    return m.group(1) if m else None


def panel_round(heading, in_reports):
    """The round a heading opens: it names R<n> and is a panel heading (or sits under 'Panel Reports')."""
    m = ROUND_TOKEN.search(heading)
    if not m:
        return None
    if in_reports or re.search(r"panel|whole|premortem", heading, re.I):
        return m.group(1).upper()
    return None


def parse(text, index, mode):
    seat_rounds, unmapped, outcomes = [], set(), []
    current_round, in_resolutions, in_reports = None, False, False
    for line in text.splitlines():
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            if line.startswith("## ") and not line.startswith("### "):
                in_reports = bool(re.search(r"panel reports", title, re.I))
            in_resolutions = title.lower().startswith("resolutions")
            current_round = None if in_resolutions else panel_round(title, in_reports)
            continue
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= set("-: "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if in_resolutions and len(cells) >= 2:
            res = outcome_of(cells[1])
            head = cells[0].split(":")[0]
            names = [n for n in re.split(r"\s*(?:\+|,|\band\b)\s*", head) if n.strip()]
            sids = [s for s in (map_seat(n, index, mode) for n in names) if s]
            if res and sids:
                outcomes.append({"seats": sorted(set(sids)), "finding": cells[0][:160], "outcome": res})
            continue
        if current_round and cells and cells[0].lower() not in ("critic", "seat"):
            v = next((VERDICT.search(c) for c in cells[1:] if VERDICT.search(c)), None)
            sid = map_seat(cells[0], index, mode)
            if v and sid:
                seat_rounds.append({"seat": sid, "round": current_round, "verdict": v.group(1)})
                # a panel row that carries its own resolution (lite logs: | Seat | Verdict | Resolution |)
                if v.group(1) == "OBJECT":
                    res = next((outcome_of(c) for c in cells[2:] if outcome_of(c)), None)
                    if res:
                        outcomes.append({"seats": [sid], "finding": f"{current_round} {cells[0][:60]}", "outcome": res})
            elif v:
                unmapped.add(cells[0][:60])
    # one verdict per seat per round (a log may repeat a seat in a confirmation row: keep the last)
    dedup = {}
    for sr in seat_rounds:
        dedup[(sr["seat"], sr["round"])] = sr
    return list(dedup.values()), sorted(unmapped), outcomes


def section(text, start, stop):
    """The part of a log from the first heading containing `start` to the next heading containing `stop`."""
    lines = text.splitlines()
    begin = 0
    if start:
        begin = next((i for i, l in enumerate(lines) if l.startswith("#") and start in l), None)
        if begin is None:
            raise SystemExit(f"no heading contains {start!r}")
    end = len(lines)
    if stop:
        end = next((i for i, l in enumerate(lines) if i > begin and l.startswith("#") and stop in l), end)
    return "\n".join(lines[begin:end])


def guess(text, pattern, default):
    m = re.search(pattern, text[:4000], re.I)
    return m.group(1).lower() if m else default


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--project", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--date")
    ap.add_argument("--mode")
    ap.add_argument("--run-type")
    ap.add_argument("--grade")
    ap.add_argument("--grade-words")
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--registry", action="store_true", help="the seats were briefed from seats/<id>.md: record their persona hashes")
    ap.add_argument("--from", dest="from_heading", help="start at the first heading containing this text (one run of a log that holds several)")
    ap.add_argument("--until", dest="until_heading", help="stop at the first heading after the start containing this text")
    a = ap.parse_args(argv)
    if a.grade and a.grade not in GRADE_POINTS:
        raise SystemExit(f"grade must be one of {list(GRADE_POINTS)}")
    text = pathlib.Path(a.log).read_text(encoding="utf-8", errors="replace")
    text = section(text, a.from_heading, a.until_heading)
    seats = load_seats()
    mode = a.mode or guess(text, r"\b(Adaptive|Autonomous)\b", "unknown")
    run_type = a.run_type or guess(text, r"\*{0,2}\b(Full|Polish|Extend|Landing)\b\*{0,2}\s+run", "unknown")
    lite = bool(re.search(r"dada-lite|lite dada|\(lite\)", text[:2000], re.I))
    seat_rounds, unmapped, outcomes = parse(text, seat_index(seats), mode)
    for sr in seat_rounds:
        sr["persona_hash"] = seats[sr["seat"]]["persona_hash"] if a.registry else "pre-registry"
    dates = sorted(re.findall(r"20\d\d-\d\d-\d\d", text))
    date = a.date or (dates[0] if dates else datetime.date.today().isoformat())
    record = {
        "id": hashlib.sha256(f"{a.repo}|{a.log and pathlib.Path(a.log).name}|{date}|{a.from_heading or ''}".encode()).hexdigest()[:10],
        "date": date,
        "project": a.project,
        "repo": a.repo,
        "log": f"https://github.com/{a.repo}/blob/main/DESIGN-LOG.md",
        "mode": mode,
        "run_type": "lite" if lite and run_type == "unknown" else run_type,
        "rounds": sorted({sr["round"] for sr in seat_rounds}),
        "seat_rounds": sorted(seat_rounds, key=lambda s: (s["round"], s["seat"])),
        "outcomes": outcomes,
        "grade": {"letter": a.grade, "points": GRADE_POINTS[a.grade], "words": a.grade_words} if a.grade else None,
        "unmapped_seats": unmapped,
        "source": "import_log.py",
    }
    if a.dry_run:
        print(json.dumps(record, indent=2, ensure_ascii=False))
        return
    ledger = pathlib.Path(a.ledger)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    existing = [json.loads(l) for l in ledger.read_text(encoding="utf-8").splitlines() if l.strip()] if ledger.exists() else []
    existing = [r for r in existing if r["id"] != record["id"]]
    existing.append(record)
    ledger.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sorted(existing, key=lambda r: (r["date"], r["id"]))), encoding="utf-8", newline="\n")
    print(f"{a.project}: {len(seat_rounds)} seat-rounds over {len(record['rounds'])} rounds, {len(outcomes)} outcomes, "
          f"unmapped {len(unmapped)}{' ' + str(unmapped) if unmapped else ''}{', grade ' + a.grade if a.grade else ''}")


if __name__ == "__main__":
    main(sys.argv[1:])
