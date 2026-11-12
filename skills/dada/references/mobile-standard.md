# The Mobile Floor

Every DADA run whose artifact is read in a browser ships a page that is **great on a phone**, whatever the mode and
whatever the run type. It is a floor and not a run type: no run type's freeze, cap or bound waives it, and a run that
leaves it unmeasured is incomplete. It is declared as data in `runtypes/dada.manual.json` under `floors`.

The phone first screen is the design. Desktop is the expansion of it, never the reverse: a layout that is composed at
1440px and then "made responsive" by shrinking it is how a page ends up with 9px card names and 36px buttons.

## What the two reference pages show

Measured with `python3 tools/measure.py --preset mobile --web <dir> --widths 390` on 2026-11-08.

| | esoteric-languages (good on a phone) | emoji-encyclopedia, before | emoji-encyclopedia, after a polish that set an 11px floor |
|---|---|---|---|
| Targets under 44px | 12 | 139 | 121 |
| Text under 12px | 0 | 280 | 161 |
| Inputs under 16px (iOS zooms the page) | 0 | 2 | 2 |
| Breakpoints | 1 (760px) | 4 or more, each shrinking type | 4 or more |
| Type | `clamp()` everywhere, floors at 12 to 15px | fixed sizes, 8 to 10px at the small breakpoints | same |

What the good page does: one breakpoint, **fluid type with a floor** (`clamp(12px, 1.05vw, 17px)`), a single column
that simply stops widening, and nothing shrunk to fit. What the other did: shrank the content (card names to 9px, the
codepoint to 6.5px) so a four-column desktop grid could survive at 375px, instead of changing the grid.

## The rules, each with its probe

Every rule has a number a run type can assert on. `measure.py --preset mobile` reports them at 360, 390 and 430px with
a coarse pointer and no hover, at a fold of 800px. `n: 0` is clean.

| | Rule | Probe key | Pass |
|---|---|---|---|
| M1 | No sideways scroll, and no visible box past the edge at any phone width | `ovf`, `clipped` | `ovf == 0` |
| M2 | `width=device-width`; pinch-zoom left alone (no `user-scalable=no`, no `maximum-scale=1`) | `viewport.n` | `0` |
| M3 | Touch targets at least 44 x 44 CSS px. A positioned `::after` counts as hit area. The whole field box is the target for a search input, not the 23px `<input>` inside it. Inline links in a sentence are exempt. 24px is the WCAG 2.2 AA hard minimum | `under44.n`, `under24.n` | `0`, `0` |
| M4 | No text under 12px; body copy at least 15px (16px preferred). Decorative text carries `aria-hidden="true"` | `tiny.n`, `body.n` | `0`, `0` |
| M5 | Inputs, selects and textareas at least 16px, or iOS zooms the page on focus. Fix the size, never `user-scalable=no` | `inputZoom.n` | `0` |
| M6 | Every `:hover` rule inside `@media (hover: hover) and (pointer: fine)`, or it sticks after a tap | `hoverUngated` | `0` |
| M7 | No bare `100vh` for fixed-height UI: `100svh` on a hero, `100dvh` on an app shell or a bottom-pinned bar | `vh100` | `0` |
| M8 | Fixed and sticky bars together cover no more than 15% of the viewport height | `bars.pct` | `<= 15` |
| M9 | The `h1` is inside the first 800px | `h1InFold` | `true` |
| M10 | Contrast at 4.5:1 (3:1 large) at phone widths; reduced motion honoured. Text inside `aria-hidden="true"` is decorative and exempt, as it is from M4 | `contrast` preset | `n == 0` |
| M11 | Content under a notch or home bar uses `env(safe-area-inset-*)` and the page says `viewport-fit=cover`, or the value is `0` | `viewport.safeAreaNeedsCover` | `false` |

Judged by the panel from screenshots at 390 x 844, the fold and the full page, because no probe can: the five-second
test on the phone screenshot (Krug), one-handed reach of the primary action, and whether the order of content on one
column is the order the page means. A Polish run that touches only words is judged the same way.

## Never do

- Do not shrink type to make a desktop layout fit. Change the layout: one column, a horizontal scroller for a filter
  row, a drawer for a sidebar.
- Do not add a breakpoint to reduce a size. Use `clamp()` with a floor; the floor is the rule.
- Do not hide the problem: `overflow-x: hidden` on `body` turns M1 green and the page still clips.
- Do not declare it fixed from device emulation. Emulation measures the layout, not the thumb, the keyboard or the
  notch. Write what could not be verified on hardware under "What needs a phone" in the Panel Report.

## Fixes

When a row fails, the fix library is the `mobile-native` skill in `SolutionsAsService/skills`, registered in
`registry/registry.json` as the floor's `fix_with`. Its symptom table maps to these rows: stuck hover after tap (M6),
the `100vh` bug (M7), the page that zooms into an input (M5), content under the notch (M11). The two-line baseline it
ships (`viewport` meta with `viewport-fit=cover`, `text-size-adjust`, 16px inputs, `touch-action: manipulation` on
controls, hover gated) is the starting point of every new page.

## Where it sits in a run

- **R0 premortem** measures the inherited page at 360, 390 and 430 and lists every failing row as a Frontier candidate.
- **Step 2b** renders every move at 390 x 844 as well as the wide viewport.
- **Step 2g** re-measures the Mobile Floor at the final state; the figures printed in the log come from that run.
- **Stop conditions:** S2 and S3 do not hold while a floor row is open.
