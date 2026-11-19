#!/usr/bin/env python3
"""Turn a design pack into the stylesheet it describes, so a run starts from tokens and not from a blank page.

    python3 skills/dada/scripts/apply_pack.py PACK_ID [--out FILE] [--check FILE]

Writes `:root` custom properties for the first mode (and a `prefers-color-scheme` block for a second), the type
stack and floors, the 44px target, and the reduced-motion / hover-gating guards the Mobile Floor needs. `--check`
exits non-zero if FILE is not what the pack would generate, so a page cannot drift from its pack. Standard library only.
"""
import argparse
import json
import sys
from pathlib import Path

PACKS = Path(__file__).resolve().parent.parent / "designpacks"


def css(pack):
    t, sh = pack["tokens"]["type"], pack["tokens"]["shape"]
    modes = pack["tokens"]["modes"]
    first = next(iter(modes))
    lines = [f"/* generated from design pack {pack['id']} {pack['version']} ({pack['status']}); do not edit, edit the pack */"]

    def block(sel, colors):
        return [f"{sel} {{"] + [f"  --{k}: {v};" for k, v in colors.items()] + ["}"]

    lines.append(f"/* mode: {first} */")
    lines += block(":root", modes[first])
    lines += [":root {", f"  --font-display: {t['display']};", f"  --font-text: {t['text']};", f"  --font-mono: {t['mono']};",
              f"  --text-base: {t['base_px']}px;", f"  --text-floor: {t['floor_px']}px;",
              f"  --radius: {sh['radius_px']}px;", f"  --target: {sh['target_px']}px;",
              f"  color-scheme: {' '.join(modes)};", "}"]
    for other in list(modes)[1:]:
        lines.append(f"@media (prefers-color-scheme: {other}) {{")
        lines += ["  " + l for l in block(":root", modes[other])]
        lines.append("}")
    lines += ["html { -webkit-text-size-adjust: 100%; }",
              "button, a.btn, input, select, summary { min-height: var(--target); }",
              "input, select, textarea { font-size: max(16px, 1em); }",
              "@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; scroll-behavior: auto !important; } }"]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pack")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--check", type=Path)
    a = ap.parse_args()
    f = PACKS / f"{a.pack}.pack.json"
    if not f.is_file():
        raise SystemExit(f"no pack {a.pack!r}; have: {', '.join(p.name[:-10] for p in sorted(PACKS.glob('*.pack.json')))}")
    out = css(json.loads(f.read_text(encoding="utf-8")))
    if a.check:
        if not a.check.is_file() or a.check.read_text(encoding="utf-8") != out:
            print(f"STALE: {a.check} is not what pack {a.pack} generates")
            sys.exit(1)
        print(f"ok: {a.check} matches pack {a.pack}")
    elif a.out:
        a.out.write_text(out, encoding="utf-8")
        print(f"written {a.out}")
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
