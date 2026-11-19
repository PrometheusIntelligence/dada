# GDADA area names (the title that pops up on arriving somewhere new)

The person (2026-11-10): "we need cool names that pop up for areas, designed with DADA in the different themes." An area is a group of maps that
share a name, a subtitle and a style. The name is shown for four seconds the first time you enter the area (not on every map).

## Format (game data, not code)
`world/areas.txt`:  `area ID style "NAME" "subtitle" pattern,pattern`   (pattern: a map name, `prefix*`, or `@region`; first match wins, list the specific first).
Styles are data (colours and an ornament per theme) so the engine and the art viewer draw the same banner: town, civic, company, ancient, archive, backrooms, dream,
undercity, eldritch, island, sand, watchers, office. Preview all banners with `hcviz <game> <out> --banners`.

## How to name an area
1. **The name is the place's own claim about itself**, in its own institutional voice: THE OFFICE OF OFFICES, THE MUNICIPAL ANNEX, THE QUIET EDGE.
2. **The subtitle is the one wrong thing**, understated, never an explanation: "Room twelve is not available", "Every book there could be, and none of them yours".
3. **Style follows the theme**: a key pattern for civic, hazard dashes for the Company, dots for the ancient, ink running down for the eldritch, stripes for the island, a stamp box for the office.
4. **Short**: names under 28 characters (they are letter-spaced), subtitles under 50.
5. Every map belongs to exactly one area; the build reports a map with none.

Lessons for this craft go into world-lessons.md when the person grades the banners.
