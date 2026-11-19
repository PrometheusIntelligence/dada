#!/usr/bin/env python3
"""Run a floor from the run manual against a site and print which assertions hold.

    python3 skills/dada/scripts/check_floor.py --web DIR [--page index.html] [--floor mobile] [--manual FILE] [--json]

This is the manual executed, not described: it reads the floor's measurements, runs each through `tools/measure.py`
(the `measure_page` instrument) at the floor's own viewports, and evaluates every `assert` row against what came
back. A row the instrument did not return is `MISSING` and fails; nothing is inferred. Exit 0 only if every
assertion holds at every viewport. Standard library only; needs Chromium for tools/measure.py (set CHROME to point at
it).

    python3 skills/dada/scripts/check_floor.py --web ../esoteric-languages/site
"""
import argparse
import json
import operator
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANUAL = ROOT / "skills" / "dada" / "runtypes" / "dada.manual.json"
OPS = {"==": operator.eq, "!=": operator.ne, "<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge}
MISSING = object()


def dig(obj, path):
    for part in path.split("."):
        if isinstance(obj, dict) and part in obj:
            obj = obj[part]
        else:
            return MISSING
    return obj


def run_measure(preset, widths, fold, web, page):
    cmd = [sys.executable, str(ROOT / "tools" / "measure.py"), "--preset", preset,
           "--widths", ",".join(str(w) for w in widths), "--fold", str(fold), "--page", page]
    if web:
        cmd += ["--web", str(web)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    results, width = {}, None
    for line in proc.stdout.splitlines():
        if line.startswith("=== "):
            width = int(line.strip("= ").strip())
        elif width is not None and line.startswith(preset + ": "):
            try:
                results[width] = json.loads(line[len(preset) + 2:])
            except ValueError:
                results[width] = {"error": line}
        elif line.startswith(preset + ": ERR"):
            results[width] = {"error": line}
    if proc.returncode and not results:
        raise SystemExit(f"measure.py failed:\n{proc.stderr[-800:]}")
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--web", type=Path, help="site directory (default: this repo's web/)")
    ap.add_argument("--page", default="index.html")
    ap.add_argument("--floor", default="mobile")
    ap.add_argument("--manual", type=Path, default=MANUAL)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    manual = json.loads(a.manual.read_text(encoding="utf-8"))
    floor = next((f for f in manual.get("floors", []) if f["id"] == a.floor), None)
    if floor is None:
        raise SystemExit(f"no floor {a.floor!r} in {a.manual}")
    report, failed = [], 0
    for m in floor["measurements"]:
        if m["instrument"] != "measure_page":
            raise SystemExit(f"check_floor.py runs measure_page only; {m['id']} uses {m['instrument']}")
        widths = [v["w"] for v in m["at"]]
        res = run_measure(m["with"]["preset"], widths, m["at"][0]["h"], a.web, a.page)
        for w in widths:
            got = res.get(w, {"error": "no result for this width"})
            for row in m["assert"]:
                val = MISSING if "error" in got else dig(got, row["metric"])
                ok = val is not MISSING and OPS[row["op"]](val, row["value"])
                failed += not ok
                report.append({"floor": floor["id"], "measurement": m["id"], "w": w, "metric": row["metric"],
                               "op": row["op"], "want": row["value"], "got": "MISSING" if val is MISSING else val,
                               "ok": ok, "why": row.get("why", "")})
    if a.json:
        print(json.dumps({"failed": failed, "rows": report}, indent=1))
    else:
        for w in sorted({r["w"] for r in report}):
            rows = [r for r in report if r["w"] == w]
            bad = [r for r in rows if not r["ok"]]
            print(f"{w}px: {len(rows) - len(bad)}/{len(rows)} hold")
            for r in bad:
                print(f"  FAIL {r['metric']} {r['op']} {r['want']}  (got {r['got']})  {r['why']}")
        print("PASS" if not failed else f"FAIL: {failed} assertion(s) do not hold")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
