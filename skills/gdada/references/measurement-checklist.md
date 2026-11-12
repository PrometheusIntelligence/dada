# GDADA measurement checklist

Run these on the **running build**, print the numbers in the Panel Report, and keep the commands in the log so a stranger
can repeat them. A check that cannot be run yet is labelled *assumption* with the blocker named.

| Check | How | Default threshold |
|---|---|---|
| Replay | Run a fixed seed twice with the same inputs; compare the result hash | Identical |
| Solvable | A perfect bot plays every generated level or night | 100 percent, zero soft-locks |
| Curve | A careless bot (fixed error rate) over levels in order | Mistakes rise gently; no level more than 2x the previous |
| Time to first interaction | Script: load the page, click the first valid target, record ms | Under 10 s from load; under 3 s to see the world |
| Session length | Bot or a timed run at human speed | Matches the stated target; log the assumption otherwise |
| Input latency | Frames between pointer event and first visible change | At most 2 frames at 60 fps |
| Frame time | `performance.now()` deltas in the busiest scene for 5 s | p99 under 16.7 ms; log the machine |
| Readability | Screenshot at 1280 x 800 and 375 x 812; every target inside the play area | Hit targets at least 44 px; no horizontal scroll |
| Contrast | Compute WCAG contrast for text and key icons in both themes | 4.5 : 1 text, 3 : 1 icons |
| Colour-only | Remove colour (grayscale screenshot) and re-read | Every state still distinguishable |
| Keyboard | Play one full level with keyboard only | Possible, with visible focus |
| Reduced motion | `prefers-reduced-motion: reduce` | No flashing, no shake; movement kept only where it is the verb |
| Agents | Count agents that overlap, jitter or stall in a 60 s soak | Zero stalls; overlaps resolved within 1 s |
| Art: team colour | Count team-colour pixels per sprite from the baked data (`tools/sprites/validate.py`) | Units at least 12 px and 12 percent; buildings 4 to 20 percent |
| Art: side separation | WCAG luminance ratio between the two sides' main colours; greyscale and colour-vision simulations of a real screenshot | At least 2 : 1; sides distinguishable in greyscale |
| Art: silhouettes | XOR over union of sprite silhouettes within a set | Units at least 22 percent; buildings of one size at least 15 percent |
| Art: animation | Pixels changed between walk frames | At least 8 per unit |
| Art: in the build | Headless screenshots of base and fight at play zoom, both themes or eras, shown to the panel before any contact sheet | Figure and ground hold against terrain; no sprite clipped by the HUD |
| Claim audit | Count design claims as measured / computed / assumption | Print the three counts |

## Playtest items (not blockers)

Anything only a person can answer goes here with a question and an observer instruction ("watch, do not explain"): did
they know what to click first, did they smile at the first success, when did they stop.

- **Concept art check.** For every asset the concept shows: the crop is saved, the render and the crop were opened side by side, the differences are written down, and a comparison image is in the log.
