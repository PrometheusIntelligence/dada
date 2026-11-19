# GDADA Art run: characters and sprites

The **Art** run type improves how a game's people look. It exists because a first pass at characters tends to give everyone the
same body, and nothing in the other run types would catch that. It reads from a ledger of what earlier Art runs learned
([sprite-lessons.md](sprite-lessons.md)) and always writes back to it. A run that does not append a lesson is not complete.

## Use it when

A game has characters (people, creatures, machines, or the unclassifiable) and their art is a first pass, is being scaled up, or a
design has added characters that have no art yet. Mode (Authored or Player-first) is chosen as usual; run type is **Art**.

## Inputs

- The **cast list**: every person, with species or kind, occupation, the one thing only they carry, and the line in the design that
  says so. Quote the source; do not invent a species. Weird characters (non-humans, machines, the unclassifiable) are read *first*,
  because they are where a template fails.
- The game's **art conventions**: pixel size, palette, how many colours, how a sprite stands on its tile.
- A **viewer and metrics tool**. For HolyC games: `SolutionsAsService/cpp-sprites` (`hcviz <game> <out> --metrics`), which writes
  the sprite sheet, a flat-silhouette sheet, a 1x sheet and `metrics.txt`.

## The grading loop (every Art and Colossus run)

The near-twin metric measures how different pieces are, never how good they are (colossus-lessons L8). The person grades quality, and the grades steer the work.

1. **Step 0 also runs the queue:** `node scripts/art_queue.mjs` prints what to work on from `references/art-grades.json`: pieces redrawn and awaiting a grade first, then
   assigned pieces below A (lowest grade first), then pieces praised but never graded, then the wishlist. Do the queue before inventing new work.
2. **Show a grading sheet at the end:** `hcviz <game> <out> --sheet NAME,NAME,...` writes `grade_sheet.png`, each piece large with a label (G1, G2...) and its name. A sheet mixes
   new pieces, redrawn pieces, and (when a piece was graded B or lower) an alternative or two so the person can compare. Ask for grades.
3. **Record the grades verbatim** in `art-grades.json` (`grade`, `said`, `date`, `status`), then update the queue: A leaves it; B, C, D stay and become the next run's assignment.
   A redrawn piece is set to `redrawn_awaiting_grade` until it is graded again.
4. **Keep expanding the library:** every run adds the next items from the wishlist (the characters and objects that maps and designers asked for) and puts them on the sheet for grading.
5. Learn from grades: a piece that earned A says what A looks like here (one clear idea, clean edges, a couple of deliberate details); add that to the lessons ledger.

## Step 0 (Art)

1. **Read `sprite-lessons.md` in full** before anything else. Every Frontier item that repeats a recorded mistake is a defect of the run.
2. Read the cast quotes. Premortem R0: *how will a player fail to tell two people apart, or fail to read one at all?*
3. Run the metrics and print the **baseline**: near-twin count over the sprite count, the mean pair distance, and the worst pair.
   A zero printed with its denominator (`0 of 36`), never a bare zero.

## The loop (one character, or one failing pair, per pass)

Write the Decision Record **before** drawing:

```
## Move An: <character or pair>
- Source: the quote that says what they are
- Silhouette plan: height in rows, width, the one shape that sticks out past the body, posture (stoop, lean, slouch)
- The thing only they carry:
- Palette: which indices, and what each becomes under the other palette
- Read at 1x: what is visible at the size a squinting player sees
- Metric before -> after: nearest neighbour and its distance in px
- Result: KEEP | ADAPT | SCRAP
```

Order of levers (cheapest first): **height, width, a prop that extends past the body, posture, headgear, hair volume, and only then colour.**

## Measurements (print them in the Panel Report)

| Check | How | Pass |
|---|---|---|
| Near twins | `hcviz --metrics`: pixels in one silhouette and not the other, for every pair | none closer than 30 px, except a **declared twin group** (same name prefix) |
| Declared twins | a group meant to look alike (the four Wrong Faces) differs only in the face | the face is the only difference |
| One-thing | each character carries one thing only they carry | listed in the record |
| 1x read | view the 1x sheet | each is still told apart without zooming |
| Silhouette-only read | view the silhouette sheet | each is told apart with no colour |
| Both palettes | render with the second palette (`--mix 1`) | no character becomes unreadable or changes who they are |
| Colour budget | colours per sprite, outline excluded | at most 8 |
| Species | a non-human is never defined by species alone | two of one species differ in clothing, height and bearing |
| Seen by the person | the renders were shown to the person | their words are logged verbatim as a lesson source |

## Panel seats (exact labels from the graph)

- `Readability: silhouette, contrast, one focal point (Solarski, Drawing Basics and Video Game Art)`
- `Twelve principles: anticipation, squash, follow-through (Thomas and Johnston, The Illusion of Life)` (posture and exaggeration)
- `Environmental storytelling (Jenkins, Game Design as Narrative Architecture)` (what a character carries says who they are)
- `Believable agents: readable intent, personality in movement (Mateas and Stern, Facade; Millington, AI for Games)`

## Stop test (Art)

- **A1** every character passes the metrics or is in a declared twin group.
- **A2** silhouette-only and 1x reads shown for the whole cast.
- **A3** both palettes viewed.
- **A4** the person has seen the renders, and what they said is logged.
- **A5** `sprite-lessons.md` was read first and has at least one new entry from this run, each with evidence and a rule.
- **A6** the game still passes its host checks, and the art conventions it states are still true.
- **A7** the queue was read first, a grading sheet was shown, the grades are recorded verbatim in `art-grades.json`, and the next run's assignment follows from them.

Round cap 3. A gate (no viewer, no metrics) is an open item: the run goes on source-only and says so.


## Portraits and animal heads
Dialogue faces and animal-headed characters follow [portrait-craft.md](portrait-craft.md) (the Maurice recipe, L41-L45).

## Guard: do not break other pieces

Run `art_guard.mjs` (game wrapper: `tools/art_guard.sh`) before an art run (must be clean) and after it with `--allow` naming exactly the
pieces the run meant to change. Anything else that changed is a break. Pieces graded A are frozen. See sprite-lessons L39.
