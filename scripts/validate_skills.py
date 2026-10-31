from pathlib import Path
import re
import yaml

root = Path(__file__).resolve().parents[1]
skills = [path for path in (root / "skills").iterdir() if path.is_dir()]
if not skills:
    raise SystemExit("No skill packages found")
for skill in skills:
    entry = skill / "SKILL.md"
    text = entry.read_text(encoding="utf-8")
    sections = text.split("---", 2)
    if len(sections) != 3 or sections[0].strip():
        raise SystemExit(f"{entry}: YAML frontmatter required")
    metadata = yaml.safe_load(sections[1])
    if not isinstance(metadata, dict):
        raise SystemExit(f"{entry}: metadata must be a mapping")
    if metadata.get("name") != skill.name or not re.fullmatch(r"[a-z0-9-]{1,64}", skill.name):
        raise SystemExit(f"{entry}: skill name must match its folder")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise SystemExit(f"{entry}: description must contain 1 to 1024 characters")
    ui = yaml.safe_load((skill / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    interface = ui["interface"]
    if not 25 <= len(interface["short_description"]) <= 64:
        raise SystemExit(f"{skill}: short description must contain 25 to 64 characters")
    if "$" + skill.name not in interface["default_prompt"]:
        raise SystemExit(f"{skill}: default prompt must invoke the skill")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if "://" not in target and not target.startswith("#"):
            reference = (skill / target.split("#", 1)[0]).resolve()
            if not reference.is_relative_to(skill.resolve()) or not reference.is_file():
                raise SystemExit(f"{entry}: invalid local reference {target}")
    discovery = root / ".agents" / "skills" / skill.name
    if not discovery.is_symlink() or discovery.resolve() != skill.resolve():
        raise SystemExit(f"{skill}: workspace discovery link is invalid")
    print(f"Valid skill: {skill.name}")

# The seat registry and the ratings are generated; they must match their sources.
import json
import subprocess
import sys

dada = root / "skills" / "dada"
for script in ("build_seats.py", "rate_seats.py"):
    subprocess.run([sys.executable, str(dada / "scripts" / script), "--check"], check=True)
seat_ids = {path.stem for path in (dada / "seats").glob("crit_*.md")}
grades = {"A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"}
ledger = root / "ledger" / "runs.jsonl"
for number, line in enumerate(ledger.read_text(encoding="utf-8").splitlines(), 1):
    run = json.loads(line)
    for key in ("id", "date", "project", "repo", "mode", "run_type", "seat_rounds", "outcomes", "grade"):
        if key not in run:
            raise SystemExit(f"{ledger}:{number}: missing {key}")
    for row in run["seat_rounds"]:
        if row["seat"] not in seat_ids or row["verdict"] not in ("PASS", "OBJECT", "NOT REPORTED"):
            raise SystemExit(f"{ledger}:{number}: bad seat-round {row}")
    if run["grade"] and run["grade"]["letter"] not in grades:
        raise SystemExit(f"{ledger}:{number}: bad grade {run['grade']}")
print(f"Valid ledger: {number} runs, {len(seat_ids)} seats")
