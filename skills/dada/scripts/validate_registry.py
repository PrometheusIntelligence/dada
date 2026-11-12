#!/usr/bin/env python3
"""Check that the registry, the manuals and the skills on disk tell the same story.

    python3 skills/dada/scripts/validate_registry.py [REGISTRY] [--parent REGISTRY ...] [--root DIR]
        [--skills-repo DIR] [--strict-pins]

The registry (`registry/registry.json`) is the one list of the skills, MCP servers and manuals dada and its forks
use, and where each skill attaches to a run. It is only worth having if it cannot drift, so this fails when:

 - the file does not match `schema/dada-registry.schema.json`;
 - an id is defined twice, or a fork's registry redefines an id its parent defined;
 - a local skill's file is missing, its frontmatter `name` is not its id, or a `skills/*/SKILL.md` on disk is not
   registered;
 - an attachment names a manual the registry does not list, or (for a manual whose file is here) a run type that
   manual does not define;
 - a skill's status contradicts its attachments (`attached` or `on_demand` with none; `reserved` or `out_of_scope`
   with some or without a note; an `explicit`-invocation skill marked `attached`);
 - a server is named by a skill or a manual but not registered, or a registered server's `used_by` is not exactly the
   manuals whose `mcp` call templates name it;
 - a floor's `fix_with` skill is unregistered or does not attach to that manual as a `fix-source` (a fork's `attach`
   list counts: it adds attachments to parent skills and never redefines them);
 - with --skills-repo DIR, a pinned external skill's file no longer hashes to its `sha256` (the skill moved under us).
   Without it the pin is reported as unverified; --strict-pins turns that into a failure.

Standard library only. Exits non-zero if any check fails, printing every problem.
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCHEMA = HERE.parent / "schema" / "dada-registry.schema.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("validate_runtypes", HERE / "validate_runtypes.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.check


def frontmatter_name(text):
    parts = text.split("---", 2)
    if len(parts) != 3:
        return None
    m = re.search(r"^name:\s*(\S+)\s*$", parts[1], re.M)
    return m.group(1).strip("\"'") if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("registry", nargs="?", type=Path, default=ROOT / "registry" / "registry.json")
    ap.add_argument("--parent", action="append", type=Path, default=[])
    ap.add_argument("--root", type=Path, default=None, help="repository root (default: the registry's parent's parent)")
    ap.add_argument("--skills-repo", type=Path, help="a checkout of the repository the external skills are pinned to")
    ap.add_argument("--strict-pins", action="store_true")
    ap.add_argument("--manual", action="append", default=[], metavar="NAME=PATH",
                    help="where a manual's file lives in this checkout when it is not at the registry's path (a fork's vendored parent)")
    a = ap.parse_args()
    root = a.root or a.registry.resolve().parent.parent
    reg = json.loads(a.registry.read_text(encoding="utf-8"))
    parents = [json.loads(p.read_text(encoding="utf-8")) for p in a.parent]
    errs, notes = [], []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    load_checker()(reg, schema, schema, "", errs)
    if errs:
        report(a.registry, errs, notes)

    # ids: unique here, and never redefined from a parent
    for key in ("manuals", "servers", "skills"):
        field = "name" if key == "manuals" else "id"
        own = [x[field] for x in reg[key]]
        for dup in sorted({i for i in own if own.count(i) > 1}):
            errs.append(f"{key}: {dup!r} is defined twice")
        for p in parents:
            for clash in sorted(set(own) & {x[field] for x in p[key]}):
                errs.append(f"{key}: {clash!r} is already defined by parent registry {p['name']!r}; a fork adds, it never redefines")
    skills = {s["id"]: s for s in reg["skills"]} | {s["id"]: s for p in parents for s in p["skills"]}
    servers = {s["id"]: s for s in reg["servers"]} | {s["id"]: s for p in parents for s in p["servers"]}
    manual_entries = {m["name"]: m for m in reg["manuals"]} | {m["name"]: m for p in parents for m in p["manuals"]}

    # manuals whose file is in this checkout: their run types and floors are checked, the others are noted
    loaded = {}
    override = dict(x.split("=", 1) for x in a.manual)
    for name, m in manual_entries.items():
        path = root / override.get(name, m["path"])
        if path.is_file():
            loaded[name] = json.loads(path.read_text(encoding="utf-8"))
        else:
            notes.append(f"manual {name!r}: {m['path']} is not in this checkout; its run types are checked in {m['repo']}")

    # skills on disk
    for sid, s in ((k, v) for k, v in {x["id"]: x for x in reg["skills"]}.items()):
        src = s["source"]
        if src["type"] == "local":
            f = root / src["path"]
            if not f.is_file():
                errs.append(f"skill {sid}: {src['path']} does not exist")
            elif frontmatter_name(f.read_text(encoding="utf-8")) != sid:
                errs.append(f"skill {sid}: frontmatter name in {src['path']} is not {sid!r}")
        elif a.skills_repo:
            f = a.skills_repo / src["path"]
            if not f.is_file():
                errs.append(f"skill {sid}: pinned file {src['path']} is not in {a.skills_repo}")
            elif hashlib.sha256(f.read_bytes()).hexdigest() != src["sha256"]:
                errs.append(f"skill {sid}: {src['path']} no longer hashes to its pin; the skill changed, so re-read it and re-pin")
        else:
            (errs if a.strict_pins else notes).append(f"skill {sid}: pin {src['ref'][:10]} not verified (no --skills-repo)")
    registered_local = {s["source"]["path"] for s in reg["skills"] if s["source"]["type"] == "local"}
    for p in sorted((root / "skills").glob("*/SKILL.md")) if (root / "skills").is_dir() else []:
        rel = p.relative_to(root).as_posix()
        if rel not in registered_local and not any(rel in {x["source"].get("path") for x in pr["skills"]} for pr in parents):
            errs.append(f"{rel} exists but is not registered")

    # a fork's additions attach to skills it did not define; the skill is never redefined
    extra = {}
    for ad in reg.get("attach", []):
        if ad["skill"] not in skills:
            errs.append(f"attach: skill {ad['skill']!r} is defined by no registry in this chain")
        extra.setdefault(ad["skill"], []).extend(ad["attaches"])
    effective = {sid: list(s["attaches"]) + extra.get(sid, []) for sid, s in skills.items()}

    def check_attach(sid, at):
        if at["manual"] not in manual_entries:
            errs.append(f"skill {sid}: attaches to manual {at['manual']!r}, which the registry does not list")
        elif at["manual"] in loaded:
            ids = {r["id"] for r in loaded[at["manual"]]["runtypes"]}
            for rt in at["runtypes"]:
                if rt != "*" and rt not in ids:
                    errs.append(f"skill {sid}: attaches to run type {at['manual']}/{rt}, which the manual does not define")

    for sid, ats in extra.items():
        for at in ats:
            check_attach(sid, at)
    # status against attachments, and attachments against manuals
    for s in reg["skills"]:
        sid, att = s["id"], s["attaches"]
        if s["status"] in ("attached", "on_demand") and not att:
            errs.append(f"skill {sid}: status {s['status']} but it attaches to nothing")
        if s["status"] in ("reserved", "out_of_scope") and att:
            errs.append(f"skill {sid}: status {s['status']} but it has attachments")
        if s["status"] in ("reserved", "out_of_scope") and not s.get("note"):
            errs.append(f"skill {sid}: status {s['status']} needs a `note` saying why")
        if s["invocation"] == "explicit" and s["status"] == "attached":
            errs.append(f"skill {sid}: invocation explicit cannot be `attached`; use on_demand and have the run propose it")
        for srv in s.get("uses_servers", []):
            if srv not in servers:
                errs.append(f"skill {sid}: uses_servers names {srv!r}, which is not registered")
        for at in att:
            check_attach(sid, at)

    # servers: both directions against the manuals' call templates
    used = {}
    for name, man in loaded.items():
        for i in man.get("instruments", []):
            ct = i["call_template"]
            if ct["call_template_type"] == "mcp":
                used.setdefault(ct["server"], set()).add(name)
    for srv, names in used.items():
        if srv not in servers:
            errs.append(f"manual(s) {sorted(names)} call MCP server {srv!r}, which is not registered")
    for srv in reg["servers"]:
        for name in srv["used_by"]:
            if name not in manual_entries:
                errs.append(f"server {srv['id']}: used_by names manual {name!r}, which the registry does not list")
        if srv["kind"] == "workflow" and srv["used_by"]:
            errs.append(f"server {srv['id']}: a workflow server is not a manual instrument, so used_by must be empty")
        actual = used.get(srv["id"], set())
        claimed = {n for n in srv["used_by"] if n in loaded}
        if srv["kind"] == "instrument" and actual != claimed:
            errs.append(f"server {srv['id']}: used_by {sorted(claimed)} but the loaded manuals that call it are {sorted(actual)}")

    # floors: the fix library must be registered and attached as a fix-source
    for name, man in loaded.items():
        for f in man.get("floors", []):
            for sid in f.get("fix_with", []):
                if sid not in skills:
                    errs.append(f"floor {name}/{f['id']}: fix_with {sid!r} is not a registered skill")
                elif not any(at["manual"] == name and at["role"] == "fix-source" for at in effective[sid]):
                    errs.append(f"floor {name}/{f['id']}: skill {sid!r} does not attach to {name} with role fix-source")

    report(a.registry, errs, notes, reg)


def report(path, errs, notes, reg=None):
    counts = ""
    if reg:
        counts = f" ({len(reg['skills'])} skills, {len(reg['servers'])} servers, {len(reg['manuals'])} manuals)"
    print(f"{'FAIL' if errs else 'ok'}: {path}{counts}")
    for e in errs:
        print("  -", e)
    for n in notes:
        print("  note:", n)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
