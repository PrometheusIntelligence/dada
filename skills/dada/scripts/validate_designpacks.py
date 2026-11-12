#!/usr/bin/env python3
"""Check every design pack against its schema and against the rules a schema cannot say.

    python3 skills/dada/scripts/validate_designpacks.py [PACK ...] [--schema SCHEMA]

Standard library only. Beyond the schema, a pack fails when:
 - a colour pair's computed WCAG contrast is below its own `min_ratio`, or `min_ratio` is below 4.5 for text roles
   (the declared pairs are computed here, never trusted) in any mode the pack defines;
 - a pair or a status names a colour that is not a token of that mode;
 - the type floor is above the base (a floor is a minimum) or the base is below the Mobile Floor's 15px;
 - two status encodings share a shape, or a status leaves `shape` or `word` empty (colour is never the only carrier);
 - the signature motif carries nothing, its asset file is missing, or the asset has no `aria-hidden` (decorative);
 - `status: adopted` without a grade and a `graded_by` that is not the run's own author.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE.parent / "schema" / "dada-designpack.schema.json"
PACKS = sorted((HERE.parent / "designpacks").glob("*.pack.json"))


def load_check():
    spec = importlib.util.spec_from_file_location("validate_runtypes", HERE / "validate_runtypes.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.check


def lum(hexcolor):
    h = hexcolor.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def cross(pack, path, errs):
    for mode, colors in pack["tokens"]["modes"].items():
        for p in pack["tokens"]["pairs"]:
            for side in ("fg", "bg"):
                if p[side] not in colors:
                    errs.append(f"pair {p['fg']}/{p['bg']} ({p['role']}): {side} {p[side]!r} is not a {mode} token")
                    break
            else:
                got = ratio(colors[p["fg"]], colors[p["bg"]])
                if got < p["min_ratio"]:
                    errs.append(f"{mode}: {p['fg']} on {p['bg']} ({p['role']}) is {got:.2f}:1, below its own minimum {p['min_ratio']}")
                if p["role"].startswith("text") and p["min_ratio"] < 4.5:
                    errs.append(f"{mode}: text pair {p['fg']}/{p['bg']} declares {p['min_ratio']}; text needs 4.5")
        for s in pack["status_encoding"]:
            if s["color"] not in colors:
                errs.append(f"status {s['state']!r}: colour {s['color']!r} is not a {mode} token")
    t = pack["tokens"]["type"]
    if t["floor_px"] > t["base_px"]:
        errs.append("type: floor_px is above base_px (a floor is a minimum)")
    shapes = [s["shape"].strip().lower() for s in pack["status_encoding"]]
    for dup in {x for x in shapes if shapes.count(x) > 1}:
        errs.append(f"status_encoding: shape {dup!r} is used twice, so it cannot tell two states apart")
    for s in pack["status_encoding"]:
        if not s["shape"].strip() or not s["word"].strip():
            errs.append(f"status {s['state']!r}: shape and word are both required; colour is never the only carrier")
    sig = pack["signature"]
    if not sig["carries"].strip():
        errs.append("signature: carries nothing; a motif that encodes no fact is decoration")
    if sig["asset"] != "none":
        f = path.parent / sig["asset"]
        if not f.is_file():
            errs.append(f"signature: asset {sig['asset']} does not exist")
        elif 'aria-hidden="true"' not in f.read_text(encoding="utf-8"):
            errs.append(f"signature: asset {sig['asset']} is not marked aria-hidden (the same facts must be in text)")
    pv = pack["provenance"]
    if pack["status"] == "adopted":
        if "grade" not in pv or not pv.get("graded_by", "").strip():
            errs.append("status adopted needs provenance.grade and provenance.graded_by")
        elif pv["graded_by"].strip().lower() in ("claude", "self", "the run"):
            errs.append("status adopted: the grade must come from someone other than the run that made the pack")
    if pack["status"] == "draft" and not pv["open"]:
        errs.append("a draft must say what is still open")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("packs", nargs="*", type=Path)
    ap.add_argument("--schema", type=Path, default=SCHEMA)
    a = ap.parse_args()
    packs = a.packs or PACKS
    if not packs:
        raise SystemExit("no design packs found")
    schema = json.loads(a.schema.read_text(encoding="utf-8"))
    check = load_check()
    bad, ids = 0, {}
    for path in packs:
        pack = json.loads(path.read_text(encoding="utf-8"))
        errs = []
        check(pack, schema, schema, "", errs)
        if not errs:
            cross(pack, path, errs)
            if pack["id"] in ids:
                errs.append(f"id {pack['id']!r} is already used by {ids[pack['id']]}")
            ids[pack["id"]] = path.name
            if path.name != pack["id"] + ".pack.json":
                errs.append(f"file name must be {pack['id']}.pack.json")
        grade = pack.get("provenance", {}).get("grade", "ungraded")
        print(f"{'FAIL' if errs else 'ok'}: {path.name} ({pack.get('status', '?')}, grade {grade})")
        for e in errs:
            print("  -", e)
        bad += bool(errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
