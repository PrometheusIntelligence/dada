# Design packs

A design language as data, so a run starts from a tested look and the next run learns from the last one's grade.

| Pack | Status | Grade | Source | Use it for |
|---|---|---|---|---|
| `prometheus-seal` | adopted | B (owner) | prometheus-stack, round 2 | stack maps, security posture, roadmaps: warm charcoal, a flame sealed in a shield, a chain of relationships |
| `sentinel-instrument` | draft | none | sentinel D1 to D5 | monitoring and evidence tools: navy, signal green, severity palette |
| `esoteric-plate` | draft | none | esoteric-languages | catalogues and reference lists: black on paper, one breakpoint, fluid type |
| `study-ledger` | adopted | B+ (owner) | ThomasSowell redesign (panel R1) | reading guides and pages of claims with uneven sourcing: paper, ink, a trust mark on every quotation that tells the reader what to do with it, a shelf of books by year |
| `lab-notebook` | adopted | B+ (owner) | ScienceEncyclopedia redesign (panel R1) | science, maths and engineering references: graph paper, ink, teal, a mark on every number, the table as the picture |
| `shell-session` | adopted | A- (owner) | LearnBash redesign (panel R1) | tutorials and references for commands or tools: real output in terminal blocks, a mark per command for what it can do, a verdict that says Can't tell |
| `vga-sixteen` | adopted | A- (owner) | HolyC site (panel R1) | a site that looks like its subject: 16 colours enforced by the build, windows on a desk, marks on facts of uneven reliability |
| `label-sheet` | adopted | B+ (owner) | CannabisCo site (panel R1) | a site where each product is shown as its package label: a shared-scale data wheel, strict sample marking, a build that refuses thin real labels |
## Use

```
python3 skills/dada/scripts/apply_pack.py prometheus-seal --out styles.tokens.css      # tokens, type, 44px targets, reduced-motion guard
python3 skills/dada/scripts/apply_pack.py prometheus-seal --check styles.tokens.css    # exit 1 if the page drifted from its pack
python3 skills/dada/scripts/validate_designpacks.py                                    # every pack, every rule
python3 skills/dada/scripts/check_floor.py --web <site dir>                            # the Mobile Floor still applies
```

## What a pack must contain

- **Tokens** for each mode, and `pairs` naming the foreground/background combinations the pack uses with a minimum ratio. The validator computes the ratio; a pair that does not meet its own minimum fails, and text pairs may not declare under 4.5.
- **A signature** whose `carries` says which fact it encodes and `derived_from` says where the numbers come from. A drawing that carries nothing is decoration and is refused. The asset must be `aria-hidden`: the same facts are printed as text.
- **A status encoding** where each state has a colour, a shape and a word, and no two share a shape.
- **Motion** that switches off under `prefers-reduced-motion`, and hover that is gated.
- **Floors** (`mobile`), because a look cannot waive the floor.
- **Provenance:** the run, the date, what was measured, what is still open, and a grade. `adopted` needs a grade from someone other than the run that made it.

## Never

- Do not adopt a pack on its author's own grade.
- Do not copy a pack's drawing without its data: the motif is only honest while its numbers come from the page's own source.
- Do not fork a pack to change a colour. Version it, or make a new pack and say what it is for.
