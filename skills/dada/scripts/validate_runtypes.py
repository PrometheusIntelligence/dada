#!/usr/bin/env python3
"""Validate a DADA run manual against its schema and against the repository it describes.

    python3 scripts/validate_runtypes.py [MANUAL ...] [--schema SCHEMA] [--parent MANUAL ...]
        [--seats-dir DIR | --seat-ids-from FILE] [--tools-from FILE] [--root DIR]

Standard library only, like the skill's other scripts. Two layers:

1. Schema: a validator for the subset of JSON Schema 2020-12 the manual schema uses (type, enum, const, required,
   properties, additionalProperties, patternProperties, items, minItems/maxItems, minimum, pattern, oneOf, $ref into
   #/$defs). Any other keyword in the schema is an error here, so the schema cannot quietly outgrow the checker.
2. Cross-checks the schema cannot express: ids are unique; every instrument a run type, measurement or fallback names
   exists (inherited ones included, via --parent); `${input.x}` in a call template names a declared input; an assertion
   never rests on a DECLARED instrument; every seat id exists; every `lessons` path resolves under --root; and for the
   dada manual itself, the panel minimums equal pick_panel.RUN_TYPE_REQUIRED so the data and the picker cannot drift.

Exits non-zero if any manual fails, printing every problem found in it.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SCHEMA = HERE.parent / "schema" / "dada-manual.schema.json"
DEFAULT_MANUALS = [HERE.parent / "runtypes" / "dada.manual.json"]
SUPPORTED = {"$schema", "$id", "$ref", "$defs", "title", "description", "type", "enum", "const", "required",
             "properties", "additionalProperties", "patternProperties", "items", "minItems", "maxItems", "minimum",
             "pattern", "oneOf", "default"}


def json_type(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, int):
        return "integer"
    if isinstance(v, float):
        return "number"
    return {str: "string", list: "array", dict: "object"}[type(v)]


def type_ok(v, t):
    jt = json_type(v)
    return jt == t or (t == "number" and jt == "integer")


def check(value, schema, root, path, errs):
    for key in schema:
        if key not in SUPPORTED:
            raise SystemExit(f"schema keyword {key!r} at {path or '/'} is not supported by validate_runtypes.py")
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            raise SystemExit(f"only local $ref is supported, got {ref}")
        target = root
        for part in ref[2:].split("/"):
            target = target[part]
        return check(value, target, root, path, errs)
    if "oneOf" in schema:
        hits = []
        for sub in schema["oneOf"]:
            trial = []
            check(value, sub, root, path, trial)
            if not trial:
                hits.append(sub)
        if len(hits) != 1:
            kind = value.get("call_template_type") if isinstance(value, dict) else None
            detail = []
            if kind:  # report the alternative the author meant, not all four
                for sub in schema["oneOf"]:
                    if sub.get("properties", {}).get("call_template_type", {}).get("const") == kind:
                        check(value, sub, root, path, detail)
            errs.extend(detail or [f"{path or '/'}: matches {len(hits)} of {len(schema['oneOf'])} alternatives (need exactly 1)"])
        return
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(type_ok(value, t) for t in types):
            errs.append(f"{path or '/'}: expected {'/'.join(types)}, got {json_type(value)}")
            return
    if "const" in schema and value != schema["const"]:
        errs.append(f"{path or '/'}: must be {schema['const']!r}, got {value!r}")
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path or '/'}: {value!r} not in {schema['enum']}")
    if "pattern" in schema and isinstance(value, str) and not re.search(schema["pattern"], value):
        errs.append(f"{path or '/'}: {value!r} does not match {schema['pattern']}")
    if "minimum" in schema and isinstance(value, (int, float)) and not isinstance(value, bool) and value < schema["minimum"]:
        errs.append(f"{path or '/'}: {value} < minimum {schema['minimum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"{path or '/'}: needs at least {schema['minItems']} items, has {len(value)}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append(f"{path or '/'}: allows at most {schema['maxItems']} items, has {len(value)}")
        if "items" in schema:
            for i, item in enumerate(value):
                check(item, schema["items"], root, f"{path}/{i}", errs)
    if isinstance(value, dict):
        for req in schema.get("required", []):
            if req not in value:
                errs.append(f"{path or '/'}: missing required {req!r}")
        props = schema.get("properties", {})
        pats = schema.get("patternProperties", {})
        for key, sub in value.items():
            if key in props:
                check(sub, props[key], root, f"{path}/{key}", errs)
                continue
            matched = [p for p in pats if re.search(p, key)]
            for p in matched:
                check(sub, pats[p], root, f"{path}/{key}", errs)
            if not matched and schema.get("additionalProperties") is False:
                errs.append(f"{path}/{key}: property not allowed")
            elif not matched and isinstance(schema.get("additionalProperties"), dict):
                check(sub, schema["additionalProperties"], root, f"{path}/{key}", errs)


def input_refs(template):
    return set(re.findall(r"\$\{input\.([a-zA-Z0-9_]+)\}", json.dumps(template)))


def cross_check(manual, parents, seat_ids, known_tools, root, errs):
    inst = {}
    for p in parents:
        for i in p.get("instruments", []):
            inst[i["id"]] = i
    own_ids = [i["id"] for i in manual.get("instruments", [])]
    if len(own_ids) != len(set(own_ids)):
        errs.append("instrument ids are not unique")
    for i in manual.get("instruments", []):
        inst[i["id"]] = i
    run_ids = [r["id"] for r in manual["runtypes"]]
    if len(run_ids) != len(set(run_ids)):
        errs.append("run type ids are not unique")
    for ref in manual.get("extends", []):
        for p in parents:
            if p["name"] == ref["name"] and ref.get("version") and ref["version"] != p["manual_version"]:
                errs.append(f"extends {ref['name']}@{ref['version']}, but the loaded parent is {p['manual_version']}: "
                            "re-read the parent's run types, then update the fork's version pin")
    parent_runs = {f"{p['name']}/{r['id']}" for p in parents for r in p["runtypes"]}
    for i in manual.get("instruments", []):
        declared = set(i.get("inputs", {}).get("properties", {}))
        for name in sorted(input_refs(i["call_template"]) - declared):
            errs.append(f"instrument {i['id']}: call template uses ${{input.{name}}} which inputs do not declare")
        for fb in i.get("fallback", []):
            if fb not in inst:
                errs.append(f"instrument {i['id']}: fallback {fb!r} is not an instrument")
        ct = i["call_template"]
        if ct["call_template_type"] == "text" and i["evidence"] != "DECLARED":
            errs.append(f"instrument {i['id']}: a text procedure can only be evidence DECLARED")
        if ct["call_template_type"] == "mcp" and known_tools is not None and ct["tool"] not in known_tools:
            errs.append(f"instrument {i['id']}: tool {ct['tool']!r} is not exposed by the pinned MCP (an invented tool)")
    floor_ids = [f["id"] for f in manual.get("floors", [])]
    if len(floor_ids) != len(set(floor_ids)):
        errs.append("floor ids are not unique")
    for f in manual.get("floors", []):
        where = f"floor {f['id']}"
        if root is not None and not (root / f["reference"]).is_file():
            errs.append(f"{where}: reference {f['reference']!r} does not resolve under {root}")
        for m in f["measurements"]:
            tool = inst.get(m["instrument"])
            if tool is None:
                errs.append(f"{where}: measurement {m['id']} uses undefined instrument {m['instrument']!r}")
            elif tool["evidence"] == "DECLARED":
                errs.append(f"{where}: measurement {m['id']} asserts on DECLARED instrument {m['instrument']!r}")
            if not m.get("at"):
                errs.append(f"{where}: measurement {m['id']} names no viewports (`at`); a floor is judged at stated sizes")
    for r in manual["runtypes"]:
        where = f"runtype {r['id']}"
        if "extends" in r and parents and r["extends"] not in parent_runs and r["extends"] not in {
                f"{manual['name']}/{x}" for x in run_ids}:
            errs.append(f"{where}: extends {r['extends']!r}, which no loaded manual defines")
        if r["id"] == "lite":
            errs.append(f"{where}: `lite` is a bound on a run, not a run type (SKILL.md, Bounded runs)")
        for ref in r.get("instruments", []):
            if ref not in inst:
                errs.append(f"{where}: instruments lists {ref!r}, which is not defined")
        for m in r.get("measurements", []):
            tool = inst.get(m["instrument"])
            if tool is None:
                errs.append(f"{where}: measurement {m['id']} uses undefined instrument {m['instrument']!r}")
            elif tool["evidence"] == "DECLARED":
                errs.append(f"{where}: measurement {m['id']} asserts on DECLARED instrument {m['instrument']!r}; "
                            "a declaration cannot satisfy an assertion")
            elif m["instrument"] not in r.get("instruments", []):
                errs.append(f"{where}: measurement {m['id']} uses {m['instrument']!r}, which the run type does not list in instruments")
        pan = r["panel"]
        seats = list(pan["required"]) + list(pan.get("dotted_pair", [])) + [s for c in pan.get("by_context", []) for s in c["seats"]] \
            + [s for g in pan.get("at_least_one_of", []) for s in g["seats"]]
        if seat_ids is not None:
            for s in seats:
                if s not in seat_ids:
                    errs.append(f"{where}: seat {s!r} does not exist")
        if "min_seats" in pan and len(pan["required"]) > pan["min_seats"]:
            errs.append(f"{where}: {len(pan['required'])} required seats exceed min_seats {pan['min_seats']}")
        if pan.get("dotted_pair") and not set(pan["dotted_pair"]) <= set(pan["required"]):
            errs.append(f"{where}: the dotted pair must be among the required seats")
        for lesson in r.get("lessons", []):
            if root is not None and not (root / lesson).is_file():
                errs.append(f"{where}: lessons path {lesson!r} does not resolve under {root}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("manuals", nargs="*", type=Path)
    ap.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    ap.add_argument("--parent", action="append", type=Path, default=[], help="a parent manual the fork extends")
    ap.add_argument("--seats-dir", type=Path, help="directory of crit_*.md seat files")
    ap.add_argument("--seat-ids-from", type=Path, help="a file in which every seat id appears (a graph reference)")
    ap.add_argument("--tools-from", type=Path, help="a Python file defining KNOWN_TOOLS, to refuse invented MCP tools")
    ap.add_argument("--root", type=Path, help="repository root that `lessons` paths resolve against")
    a = ap.parse_args()
    manuals = a.manuals or DEFAULT_MANUALS
    root = a.root or HERE.parents[2]
    schema = json.loads(a.schema.read_text(encoding="utf-8"))
    parents = [json.loads(p.read_text(encoding="utf-8")) for p in a.parent]
    seat_ids = None
    if a.seats_dir:
        seat_ids = {p.stem for p in a.seats_dir.glob("crit_*.md")}
    elif a.seat_ids_from:
        seat_ids = set(re.findall(r"\bcrit_[a-z0-9_]+\b", a.seat_ids_from.read_text(encoding="utf-8")))
    known = None
    if a.tools_from:
        src = a.tools_from.read_text(encoding="utf-8")
        start = src.index("KNOWN_TOOLS")
        end = src.index("\n}\n", start) + 3  # the literal closes with a brace at column 0
        ns = {}
        exec(src[start:end], ns)  # only the KNOWN_TOOLS literal, a set of strings built from comprehensions
        known = ns["KNOWN_TOOLS"]
    failed = False
    for path in manuals:
        manual = json.loads(path.read_text(encoding="utf-8"))
        errs = []
        check(manual, schema, schema, "", errs)
        if not errs:
            cross_check(manual, parents, seat_ids, known, root, errs)
            if manual["name"] == "dada" and (HERE / "pick_panel.py").is_file():
                sys.path.insert(0, str(HERE))
                import pick_panel
                for rid, seats in pick_panel.RUN_TYPE_REQUIRED.items():
                    got = next((r for r in manual["runtypes"] if r["id"] == rid), None)
                    if got is None:
                        errs.append(f"pick_panel.RUN_TYPE_REQUIRED has {rid!r}, which the manual does not define")
                    elif got["panel"]["required"] != seats:
                        errs.append(f"runtype {rid}: panel.required {got['panel']['required']} != pick_panel {seats}")
        print(f"{'FAIL' if errs else 'ok'}: {path} ({len(manual.get('runtypes', []))} run types, "
              f"{len(manual.get('instruments', []))} instruments, {len(manual.get('floors', []))} floors)")
        for e in errs:
            print("  -", e)
        failed = failed or bool(errs)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
