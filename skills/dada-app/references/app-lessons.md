# What the OperatorOS run measured (the evidence behind the rules)

Source: the OperatorOS world-picture polish run, 2026-11-27 (`DESIGN-LOG.md`, `CARRY-FORWARD.md`, `docs/design/` in
SolutionsAsService/operatoros). Adaptive mode, Polish run type, three WHOLE rounds, five seats, 209 unit tests and a
36-check browser harness. Numbers are at 390x844 unless stated.

| Finding | Measured | Rule it became |
|---|---|---|
| Marks sized in map units vanish on a phone | a 6-unit glyph drawn at 0.34x is about 2px; 142 of 142 hit targets under 24px | size marks in screen pixels; non-scaling strokes |
| The control stack above the map | map top 678, bottom 1018 vs fold 844; 0 markers visible at 375x812 | fold non-data controls behind one labelled button; map first |
| Floors that nothing holds | 1,155 text elements under 12px beside a doc saying "never below 11px"; 643 controls under 44px | floors held by a stylesheet test plus a rendered probe |
| Bubble size that does not encode the count | radius 9 + 1.8 log2 n capped at 16: lie factor about 0.1 | area proportional to count with a stated minimum and cap |
| Mixed group drawn in its mode colour | a 6-bubble of 3 + 3 read as one category | one arc per category by share |
| Reference locations counted as observations | footer "235 observations", legend 62 references inside it | references drawn differently, counted on their own line, never inside a group |
| Legend sliced to 7 and omitting wars | 4 categories shown, wars and fleet missing | legend lists everything drawn; one count source |
| A layout push that looked right | a two-column phone key moved the map from 538 to 555px (390x844) and 538 to 571px (375x812) | measure every push; revert when it moves the wrong way |
| Doc numbers that drifted | "496 / 740" in the doc vs 432 / 678 measured; later 538 / 783 vs 543 / 788 after one more edit | re-run 2g after every doc edit |
| `span:last-child` hid a nested label | the pill read a bare "274" | scope row-level rules with `>` |
| A transparent hit circle on a later layer | a `.first()` click landed on a war marker | tests pick the mark whose own centre is topmost |
| The panel had no phone-behaviour seat | "tappable" argued from sizes (28px targets, 0 under 24px) | seat a phone-interaction critic that runs touch scripts |

## Claims the claims seat found in every round (read before writing a doc)
A limit stated in prose ("never below 11px", "one tab stop", "every positioned signal") needs the number from the code
beside it (the cap, the count, the file:line). The verification section must say what was not run (no screen reader,
no real phone, harnesses that could not run, bytes before first use).
