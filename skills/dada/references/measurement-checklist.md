# Measurement checklist (web)

What the measurement seat runs, and what the conductor checks before any number reaches the panel. Every item
names the failure that put it here; the lesson numbers refer to `LESSONS.md` in PrometheusIntelligence/dada-lessons.

## Before the panel sees anything: check the instrument

- **Open every capture you hand to the panel**, on every run, not only the first. A headless browser whose window is
  smaller than the emulated viewport can return a capture tiled 2 x 2 on a later run; five seats judged one
  (shadw-MCP R1). Start the browser with a window at least the size of the largest viewport, and clip the capture.
- **Narrow headless captures lie.** Headless Chrome narrower than about 500 px lays out wide and crops (lesson 35).
  Emulate device metrics (DevTools `Emulation.setDeviceMetricsOverride`) or measure in a real viewport, and label every
  capture with the width it was laid out at.
- **Smooth scrolling moves captures.** A capture taken while `scroll-behavior: smooth` is still animating shows a
  header where it is not (lesson 45: five critics, a collision that did not exist). Disable it, or wait for `scrollY`
  to settle.
- **Every probe has a fixture that must fail.** Run each probe once on a page built to fail it. An inverted filter
  reported 0 undersized targets while 18 px cells sat at a 22 px pitch (shadw-MCP R1).
- **The build log is not the DOM.** A build script reported 40 pads while the DOM held 0 (lesson 45). Count in the
  rendered page.

## The first screen (websites)

- The landing graphic's **full bounding box**, bottom edge included, at 1280 x 800 and 375 x 812; no sideways scroll
  inside it; no tile overflowing (lessons 40-42). Measure the union of everything the hero is made of (headline,
  graphic, legend, call to action), not the graphic's top.
- The **five-second test**: from the first screen alone, name the site, three of its topics and the first action.

## Probes

| Probe | Pass | Why it is here |
|---|---|---|
| Horizontal overflow | `documentElement.scrollWidth - innerWidth == 0` on every page at every width | the most common phone defect |
| Text contrast | every visible text node ≥ 4.5:1 (≥ 3:1 large) against its nearest opaque background; **skip visually-hidden text** | screen-reader-only labels measured against the cell behind them gave 1.96:1 false positives |
| Contrast over images | sample the pixels under the text, not the CSS background | UGC's worst defect, found by a script, not a critic (lesson 43) |
| Target size and spacing (WCAG 2.5.8) | report targets under 24 px **that have another target within 24 px**, centre to centre | the inverted version passed failing targets |
| Focus visibility | after a **real Tab press** (a script `focus()` does not set `:focus-visible` in Chromium), the computed outline is visible against the surface *outside* the element | lesson 34; and a later `.x[attr]` outline at (0,2,0) silently replaced a `:focus-visible` ring (lesson 56) |
| `[hidden]` state | after every interaction, every `[hidden]` element computes `display: none` | an author `display` rule beats the attribute; add `[hidden]{display:none !important}` (lesson 55) |
| Smallest label | the smallest text in any figure, measured at the **narrowest supported viewport** | a figure's labels rendered at 3.5 px on a phone (lesson 50) |
| Data encoding | every grid line, tick, bar and animation extent derived from the data scale, checked against the figure it encodes | a time-driven flood kept growing after the data stopped (lesson 46) |
| Printed figures | every number on the page re-computed from its source after the last edit (Step 2g) | figures drift as later moves land |
| Claims about software | every sentence that states a limit, default or refusal checked against `file:line` | copy written from memory of the code overstated it (lesson 44) |
| Links | every internal link resolves; no page without an inbound link | a flagship page with no inbound link (lesson 52) |
| Reduced motion and forced colours | animation stops; meaning carried by colour survives `forced-colors: active` | write cells read as read cells in High Contrast (shadw-MCP R1) |

## Reporting

Give the panel one evidence file per round: what was measured, how, when (after which edit), and the raw numbers in a
file beside it. A number measured before the last edit is stale and is re-run, not reported.
