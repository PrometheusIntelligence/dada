"""Generate one file per panel seat in seats/ from the anchor graph and seats/personas.json.

    python scripts/build_seats.py            # write seats/<node_id>.md and seats/README.md
    python scripts/build_seats.py --check    # exit non-zero if any seat file is missing or stale

A seat is one authority arguing from its own literature (SKILL.md Step 2c: one agent per reference). Its file
holds what the graph says about it (label, literature, the edges it judges with, its dotted rivals) and the
stable persona it brings to every run (personas.json). The persona hash is recorded with every verdict in the
ledger, so a seat's rating belongs to the persona that earned it.
"""
import hashlib
import json
import pathlib
import re
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
GRAPH = SKILL / "references" / "anchor-graph.md"
SEATS = SKILL / "seats"
PERSONAS = SEATS / "personas.json"


def frontmatter(d):
    """YAML frontmatter for flat values and lists, written without a YAML library (JSON strings are valid YAML)."""
    return "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in d.items())


NODE = re.compile(r'^\s+(\w+)\["([^"]+)"\](?::::(\w+))?')
EDGE = re.compile(r"^\s+(\w+)\s+(-->|-\.->)\|([^|]+)\|\s+(\w+)")
SUBGRAPH = re.compile(r'^\s*subgraph (\w+)\["([^"]+)"\]')


def parse_graph():
    nodes, edges, cluster_of = {}, [], {}
    cluster = None
    for line in GRAPH.read_text(encoding="utf-8").splitlines():
        m = SUBGRAPH.match(line)
        if m:
            cluster = m.group(1)
            continue
        if line.strip() == "end":
            cluster = None
            continue
        m = NODE.match(line)
        if m and m.group(1) not in nodes:
            nodes[m.group(1)] = m.group(2)
            cluster_of[m.group(1)] = cluster
            continue
        m = EDGE.match(line)
        if m:
            edges.append((m.group(1), m.group(2), m.group(3).strip(), m.group(4)))
    return nodes, edges, cluster_of


def persona_hash(persona):
    return hashlib.sha256(json.dumps(persona, sort_keys=True).encode()).hexdigest()[:12]


def seat_record(sid, nodes, edges, cluster_of, persona):
    label = nodes[sid]
    m = re.match(r"Critic: (.+?) \((.+)\)$", label)
    concern, authority = (m.group(1), m.group(2)) if m else (label, label)
    surname = authority.split()[-1].lower()
    judges = [(lab, dst) for src, kind, lab, dst in edges if src == sid and kind == "-->"]
    lit = [nodes[d] for _, d in judges if d in nodes and surname in nodes[d].lower()]
    rivals = sorted(
        {(dst if src == sid else src, lab) for src, kind, lab, dst in edges if kind == "-.->" and sid in (src, dst)
         and (dst if src == sid else src).startswith("crit_")}
    )
    return {
        "id": sid,
        "label": label,
        "concern": concern,
        "authority": authority,
        "literature": lit,
        "judges_with": [f"{lab} → {nodes.get(d, d)}" for lab, d in judges],
        "rivals": [{"seat": r, "edge": lab, "label": nodes.get(r, r)} for r, lab in rivals],
        "persona_version": persona["version"],
        "persona_hash": persona_hash(persona),
        "persona": persona,
    }


PROMPT = """You are one seat on a DADA critic panel, round {{round}}: "{label}". Argue only from {authority}'s own doctrine{lit_clause}. Do not read or react to any other seat's file.

Who you are, every run: {temperament} You always check: {checks}. You never accept: {never} Your question: {question} Your known blind spot, which you do not pretend to cover: {blind}{duties}

Read the evidence file first: {{evidence}}. Then the artifact: {{artifact}}. Every fact you rely on must come from the evidence file or the artifact itself; if the conductor's prompt states a fact neither holds, say so. Point at something observable for every judgment and name the work you argue from.

Output, under {{words}} words:
- Anchor used: (the work, and the idea in it)
- Observed: (what, where)
- Findings: numbered F1, F2 ...; each one line tagged [defect], [claim] or [premise]
- Verdict: PASS or OBJECT
- Requested change: (per finding, or "none")

Write your report to {{panel_dir}}/{id}.md as your last action (load the Write tool or use a shell command), then return the same text. If the connection drops, the file is the verdict."""


def render(rec):
    p = rec["persona"]
    lit = rec["literature"]
    lit_clause = f", as set out in {'; '.join(lit)}" if lit else ""
    duties = p.get("duties") or []
    duties_txt = f"\n\nYour duties when the conductor briefs them: {'; '.join(duties)}." if duties else ""
    prompt = PROMPT.format(
        label=rec["label"], authority=rec["authority"], lit_clause=lit_clause, temperament=p["temperament"],
        checks="; ".join(p["always_checks"]), never=p["never_accepts"], question=p["signature_question"],
        blind=p["blind_spot"], duties=duties_txt, id=rec["id"],
    )
    words = len(prompt.split())
    front = {
        "id": rec["id"], "label": rec["label"], "concern": rec["concern"], "authority": rec["authority"],
        "literature": rec["literature"], "rivals": [r["seat"] for r in rec["rivals"]],
        "persona_version": rec["persona_version"], "persona_hash": rec["persona_hash"],
    }
    rivals = "\n".join(f"- `{r['seat']}` ({r['label']}), dotted edge: {r['edge']}" for r in rec["rivals"]) or "- none in the graph"
    judges = "\n".join(f"- {j}" for j in rec["judges_with"]) or "- none"
    return f"""---
{frontmatter(front)}
---

# {rec['label']}

Generated by `scripts/build_seats.py` from `references/anchor-graph.md` and `seats/personas.json`. Edit the persona,
never this file; bump the persona's `version` when its character changes, so its ratings start a new record.

## Persona (version {rec['persona_version']}, hash `{rec['persona_hash']}`)

- **Temperament:** {p['temperament']}
- **Always checks:** {'; '.join(p['always_checks'])}
- **Never accepts:** {p['never_accepts']}
- **Signature question:** {p['signature_question']}
- **Blind spot:** {p['blind_spot']}
- **Voice:** {p['voice']}
{('- **Duties when briefed:** ' + '; '.join(duties)) if duties else ''}

## In the graph

Literature: {'; '.join(lit) if lit else 'see the graph edges below'}

Judges with:
{judges}

Rivals (pair one of these on the panel to meet the dotted-pair rule):
{rivals}

## Seat prompt ({words} words before the conductor fills the braces; the panel protocol caps prompts at about 350)

```text
{prompt}
```

## Ratings

See `references/seat-ratings.md`, built from `ledger/runs.jsonl` by `scripts/rate_seats.py`.
"""


def main(argv):
    check = "--check" in argv
    nodes, edges, cluster_of = parse_graph()
    personas = {k: v for k, v in json.loads(PERSONAS.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    seats = [n for n, c in cluster_of.items() if c == "CRITICS" and n.startswith("crit_")]
    missing = [s for s in seats if s not in personas]
    extra = [p for p in personas if p not in seats]
    if missing or extra:
        raise SystemExit(f"personas.json out of step with the graph: missing {missing}, unknown {extra}")
    stale, index = [], []
    for sid in seats:
        rec = seat_record(sid, nodes, edges, cluster_of, personas[sid])
        text = render(rec)
        path = SEATS / f"{sid}.md"
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(sid)
        else:
            path.write_text(text, encoding="utf-8", newline="\n")
        index.append((rec["concern"], rec["authority"], sid, rec["persona_version"], rec["persona_hash"], len(rec["rivals"])))
    readme = ["# Seats", "",
              "One file per panel seat: the graph's critic node, its literature and rivals, and the persona it brings to every",
              "run. Generated by `scripts/build_seats.py`; edit `personas.json`, never the seat files. Non-graph roles that",
              "testify but do not judge are in `witnesses.md`. Ratings: `../references/seat-ratings.md`.", "",
              f"{len(index)} seats.", "", "| Concern | Authority | Seat | Persona | Rivals |", "|---|---|---|---|---|"]
    readme += [f"| {c} | {a} | [`{s}`]({s}.md) | v{v} `{h}` | {r} |" for c, a, s, v, h, r in sorted(index)]
    readme_text = "\n".join(readme) + "\n"
    if check:
        if (SEATS / "README.md").read_text(encoding="utf-8") != readme_text:
            stale.append("README.md")
        if stale:
            raise SystemExit(f"stale seat files (run scripts/build_seats.py): {stale}")
        print(f"{len(seats)} seat files current")
    else:
        (SEATS / "README.md").write_text(readme_text, encoding="utf-8", newline="\n")
        print(f"wrote {len(seats)} seat files")


if __name__ == "__main__":
    main(sys.argv[1:])
