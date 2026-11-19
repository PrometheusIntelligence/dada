---
name: gdada-art-subagents
description: "How to run GDADA art production with parallel sub-agent authors: split a roster by file ownership, write the brief as a contract (kinds, sizes, conventions, concept sheet to compare against), forbid concurrent builds, validate with a counter script, send failing models back to their own author, build the sprite sheet once at the end, and report what still differs from the concept art. Use when a game needs dozens of sprites or models (units, buildings, props, eras) and one agent cannot hold them all, or when art must be checked against concept art."
---

# GDADA art with sub-agents

Born in Tidewatch (runs 21 to 24): five authors produced 62 isometric models in parallel, a sixth pass tuned 50 buildings, and one lead built everything once.

## Workflow

1. **Owner words first.** Put the request in `VISION.md` verbatim before anything else; save any concept images beside the game (`design/reference/`). The concept art is the judge.
2. **Split by file, never by line.** One author owns one file (`iso_models_j.py`). Register the file in the loader the lead edits (a try/except import list), so authors never touch a shared registry.
3. **Brief = contract.** Kind list with a one-line look per kind; canvas sizes and anchors to keep; the team-colour rule; what the renderer can do (read the kit first); the concept sheet to read as an image; the file they may touch; the commands they may run. Say what NOT to do: do not run the shared build, do not edit the shared output, do not commit.
4. **One build, by the lead.** Concurrent builds overwrite one output. Authors preview with their own script into a scratch directory and read the PNGs; the lead runs the build once.
5. **Validators fail loudly.** The build checks every facing (team-colour pixels, body pixels, distinct facings). Send each failing kind back to its own author (SendMessage) with the exact rule and the way to count it; do not fix other people's models yourself.
6. **Check against the concept.** Every report must say what still differs from the concept art. Authors' reports are claims: look at the roster sheet yourself (labelled sheet of every kind, one facing) before believing them.
7. **Show the owner.** Roster sheets per era, before-and-after sheets, in-game parade screenshots. Say what was only looked at once.

## Pitfalls seen

* 247 validator failures on the first four-era bake: the authors fixed their own, so budget a fix round per author. Authors skip the concept comparison unless the brief demands a "what still differs" line; in four rounds they skipped it at least four times.
* A validator that passes does not mean the silhouettes read: the lead still opens the contact sheet made from the final baked output.
* Team colour on one surface (a shield) vanishes from behind: require it on back and both flanks.
* A khaki ground slab under every building reads as a footprint, not a plinth: ask for irregular edges or a small terrace.
* Authors say "I did not re-view after the last tweak": ask for a final read of the sheet.
* A shared preview script edited by another author breaks silently: each author keeps its own.
* A 30 MB sprite JSON loads slowly: split per era before it gets there.
