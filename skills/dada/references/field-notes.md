# Field notes: what has actually worked in Adaptive runs

Distilled from the runs that produced the strongest artifacts — UGC Events &
Media, WTF, Copperline Plumbing, Highwater Rafting — and from what failed in
them. Each note says where it came from so it can be checked, and each is a
thing to *do*, not a thing to admire.

Read alongside [the panel protocol](panel-protocol.md).

---

## 1. MAYA resolves the Sharp ↔ Shklovsky conflict by address, not by compromise

The recurring split on a public-facing site is Sharp (recognition, deploy the
asset identically everywhere) against Shklovsky (estrangement, do not let the
device become furniture). Both are right, and splitting the difference produces
a site that is half-strange everywhere and memorable nowhere.

**Resolve it by address.** Put the break on the home page and recognition on
every other page. UGC did this: the cut-paper hero lives on the index, the
inner pages are conventionally navigable. Both critics accepted it in writing
(UGC R2 Frontier). Highwater did the same — the gauge is the home page's
display head; trips, guides, safety and basecamp are plain.

Record the resolution in the Frontier, not just in the prose.

## 2. Enroll a measurement seat, because the panel does not measure by default

This is the largest failure found across these runs. In UGC, the two most
serious defects — text contrast over a photograph, and a focus ring clipped
away by `clip-path` — were found by measurement scripts, **not by any critic**.
No seat measured anything unprompted except Mace. Several critics judged from
two or three screenshots when the run had captured six.

So: for any artifact that can be inspected, convene `Critic: Evidence (Cairo)`
as a required Adaptive seat, briefed to *run measurements* — contrast over
images, focus visibility, overflow, target size, link inventory — rather than
to read screenshots. And give Mace a named focus-visibility check.

The corollary, from the Highwater run, is the instrument check: a finding that
appears only in a tool's output must be measured on the rendered page before a
move is spent on it. Two of that run's "failures" were artefacts of the
contrast sampler and of a local static server not running `cleanUrls`.

## 3. The seeded Breaker earns its place only when escalated

S4 asks for an ambition push. It should be an escalation of the Breaker you
already seeded, not a new device bolted on beside it. UGC seeded `Saul Bass: A
Life in Film and Design`, took the cut-paper ridgeline as M3, and pushed it in
M8 to the photograph cut into the mountain — the same idea, harder. Highwater
seeded `Making and Breaking the Grid`, took the flow axis as M2, and pushed it
to a draggable gauge that recomputes every trip state.

An escalation that does not change a measured number is a declaration. Both of
the above logged deltas (hero text 2.0 → 5.1:1; trip states `on,on,on,over,on,on`
→ all six open when the reading moves).

## 4. One generator, and put the guarantees in the build

Every one of these sites that survived later editing is
`_src/build.py` + `_src/layout.html` + `_src/pages/*.html`, with
`_src/data/*.json` wherever a fact is printed more than once. Two payoffs, both
earned the hard way:

- **A fact printed twice will drift.** Highwater's favicon used one vermilion
  and the stylesheet another; the fix was to make the build *write* the favicon
  from the stylesheet's tokens so the colour is typed once.
- **The build is where a guarantee can live.** Highwater's build refuses to
  emit a page whose internal links point at a file it did not write, so a dead
  link fails at build time rather than in a browser. This is what closes
  Debord's standard objection (an image of a business with no referent) in a
  way a critic can verify rather than take on trust.

## 5. The highest-value late moves are deletions of claims

Late in a run, once the form is good, the moves that most improve the work are
removals:

- UGC M13: remove every claim the owner has not made.
- UGC M5 (Redish): copy of fact, not slogans.
- Highwater M6: a June gauge reading printed in October must not say "running".

Debord, Cairo and Redish all converge here, and each time the objection arrived
late because the claim only became visible once the page was worth reading.
Budget a late move for this and expect it.

**Rule of thumb:** every claim the artifact prints needs a source in the repo.
If the source does not exist, either the claim comes out or the artifact says
on its face that it is a placeholder — a concept site whose phone number is a
555 number and whose email uses `.example` is honest; one that prints "Book
now" over a form with no endpoint is not.

## 6. Batching is the honest deviation — record it

Every one of these runs wrote Decision Records in batches before each group of
moves, and ran the panel per WHOLE round rather than per move. The contract
asks for one at a time. Do not pretend otherwise: write the deviation into the
Compliance Check, as UGC did. A fabricated one-at-a-time compliance line is
worse than an admitted batch.

## 7. Deferrals to the owner belong in S1, and on the artifact's face

Owner-dependent gaps — a real email address, capacity figures, a phone number,
footage — are not OPEN Frontier items and not defects. List them under S1 with
the reason, and make the artifact say what it does not have rather than
implying it does. The portfolio run marked a mailto slot in the template and
said in the page that a direct address was on its way; that is the pattern.

## 8. Grow the graph while you run

UGC seeded 6 anchors and closed with 22 in the ledger — Krug, Redish, Berger,
Holmes, Nielsen, Yablonski, Beier, Cairo, Gestalt, Wheeler all arrived because
a move or an objection needed them. The seed is a starting point. Enroll an
anchor only when it does work in a record's argument or in a critic's
observation, and give it a ledger row when you do.

## 61. Measure the rendered artifact, not the source that produced it

From the Microcontroller Encyclopedia run (2026-10-27). A build script reported
40 tagged pin rows; the DOM had 0. The script had replaced a `<table>` with its
`<tr>`s, so the parser discarded every row, and my own verification counted the
file instead of the browser. The same failure shape appeared earlier on the
portfolio run, where five critics reported a phone-header collision that existed
only in the capture.

The rule: before tabling any premise for the panel, take the number from the
rendered artifact — `getComputedStyle`, `getBoundingClientRect`,
`querySelectorAll`, `scrollWidth`. A build log, a commit message and a file
listing are all claims about the source; they are not evidence about the work.
When the two disagree, the browser is right and the script is wrong.

Three concrete traps this run paid for:

- A `<tr>` written outside `<table>` is dropped by the HTML parser with no
  error. Splice tables with a capturing `re.split` that keeps the wrapper.
- Rows whose first cell is a `<th>` vanish if you strip `<th>` before counting
  (a 40-pin board counted as 39). Read cells from `th` and `td` alike.
- `position: sticky` inside the header unsticks when the header leaves the
  viewport; the sticky element has to be a sibling of the scrolling content.
- A relative `src` or `href` on a page in a subdirectory resolves against that
  subdirectory. Subdirectory pages need `../`.

**Graph amendment:** add a node "Measure the rendered artifact" to the Panel
Method cluster with the edge
`c_genchi -->|verify the DOM against the source before tabling a premise for| CRITICS`.

## 62. An Andon about missing facts is answered by sourcing, not by styling

Debord pulled the Andon on a board portrait: a site that stated no millimetre
could not honestly depict a board at scale. The premise was measured (0 hits for
`mm`) and true, so the resolution was ADAPT — footprints quoted from the
manufacturers' own pages, and, where none could be sourced, the page printing
"footprint: not stated" with the drawing labelled schematic. Inventing plausible
dimensions would have been the easier move and the wrong one. When an objection
is about the artifact's *evidence*, the fix is evidence; a style change is a
refusal wearing paint.

## 63. Give a generated graphic a fixed box, or the data sets the layout

Every board drawing letterboxes inside one 300px square. Before that, the
21 × 51 mm Pico rendered 532px tall because the drawing was sized by the data —
a portrait of a tall object is tall. If art is generated from measurements,
constrain the frame and let the drawing fit it; otherwise the subject's
proportions quietly redesign the page.

## 12. A figure that names an extremum is computed at the data's resolution

Ages of Rule printed "Peak (1790)" for the year with the most systems alive. The chart sampled every ten years, so
it missed the true maximum: 18 systems in 1795, not the 16 it printed. Cairo found it by recomputing from the JSON.
Any "peak", "longest" or "most" is computed at the data's own step, never the chart's, and goes on the Step 2g list.
The same run kept a related refusal: a measurement that disagrees with the objection (a duration across BCE years that
does not cross year 0) is an OVERRULE with the measurement named, not a change.

## 13. Adding a large dataset flattens the signature graphic: keep the calm default

166 countries from CountryData were added to a 56-system skyline. Switched on, the ancient and medieval layers shrank
to a line under a modern spike, and the spike itself was partly an artefact (countries start at independence, and only
current states are counted). The landing keeps the curated set as the default, offers the countries behind one click,
and prints the artefact beside the chart when they are on. This is the "calm default state" rule applied to an
expansion; the lesson is that an expansion request changes the *default* only if the first screen survives it.

## 14. A key is drawn from the marks' own tokens

Krug found the timeline's "how to read this" key in blue while every bar was red or orange. The key had been written
once, with a placeholder colour, and never looked at beside the chart. Draw legends from the same CSS tokens as the
marks, or in a neutral ink that claims no colour, and open the key beside a bar when checking it.

## 15. An importer skips what it cannot read and says so

`scripts/import-countrydata.py` takes two things from each CountryData record: government type and the year it began.
Where no start year could be read from the record's own independence, declaration or founding field, the country is
skipped and listed (43 of 191), never given a plausible year. The family is assigned by visible keyword rules and the
source text stays on the page, so Debord's objection to an unverifiable label has something to check. The first
version of the rules put Qatar under "authoritarian" because that word appeared in its type; reordering the rules so a
monarchy is tested before an authoritarian keyword fixed it. Print the distribution and spot-check a dozen named
cases after writing the rules, not before.

## 16. Run the page audit after every scripted edit

Two string-replace edits to one JS file left an unterminated string and broke a page; a six-page audit script
(console errors, horizontal overflow, h1 present, at 1280 and 375) found it in seconds. A scripted `replace` that does
not match fails silently; the audit is the only thing that tells you it did something else.

## 17. A bounded run without its records is a B

The run was graded B ("pretty good"): a strong landing and honest figures, with no Traversal Plan, no Decision
Records, one three-seat round, deferred objections still open (Debord's family labels) and seats briefed by hand
instead of from `seats/`. The log says so in its Compliance Check. A bounded run still writes the five artifacts, even
as short tables, because the ledger and the stop test read them; what the run skipped is the ceiling on its grade.

## 18. Portfolio links follow the deploy rule

Projects in the portfolio link to `<repo name, lower case>.shadw.app`, because that is where the owner deploys them.
A card is written with that URL when the entry is added, even before the deploy; a GitHub URL is only for a project
that is not a deployed site (a reader's guide).

## 19. Run the library: a docs site's code is the first thing to measure

LearnHypercore's inherited examples were never run. Installed against the real package (hypercore 11.40.3) three
crashed or were syntax errors, and the replication example never showed data moving. Cairo's R0 finding was that the
gate must install the package, execute every snippet and diff stdout against what the page prints. That gate
(`scripts/check.mjs`, with `--update` writing the printed output from a run) also failed the inherited site on its first
run, which is the fixture a probe needs. For any page that teaches software: install it, run it, print the run.

## 20. When the README and the registry disagree, print both

The upstream README said "the latest release is Hypercore 10" while npm's `latest` tag was 11.40.3. The page states
the discrepancy and stamps the version it was checked against from one file (`data/verified.json`), so the stamp
cannot drift from the check. A seat that argues from a source only holds when the source is read, so read the
installed package's code for any claim about internals (BLAKE2b leaves, a signed hash of the roots).

## 21. An interactive demo of a real system says "simulation" above the figure

Kahneman's R1 finding: the disclosure sat in small grey text under the readout, and the bold "8 blocks, 1 root"
anchored as a fact about Hypercore. The fix was to put the note above the figure in a larger face, to label the
numbers "this demo", and to say what differs (SHA-256 here, BLAKE2b there). Put the demo's logic in a module the gate
can import (`assets/merkle.js`) so the numbers the page prints are asserted, with a fixture that must fail.

## 22. A control that edits what the system forbids teaches the wrong thing

The first demo had "Alter the selected block" with "Restore". Shklovsky: an append-only log's strange fact is that
there is no edit, and a Restore button lets the visitor undo the one act a log refuses. It became a one-way "Forge
block N" with Reset as the only way back, and the readout says a real core has no edit. When a demo has a verb the
real system lacks, name the verb as the attack, not the feature.

## 23. A seat's confirmation pass catches fixes that did not land

Two scripted string replacements silently matched nothing (the source held typographic characters where the script
had escapes), so a plural and a duplicated label were reported fixed and were not. Cairo's confirmation pass, reading
the live page, found it. After any scripted edit, assert the new text on the rendered page before reporting the fix,
and use the Edit tool, which fails loudly, when the target contains non-ASCII text.

## 24. Padding on a `wrap` element removes the gutter

`main.page { padding: 28px 0 0 }` overrode the 16px horizontal padding of `.wrap`, so every inner page's text touched
the screen edge at 375px. The same mistake appeared on a second site in the same session (`.hero { padding: 18px 0 0 }`).
Set `padding-top` only, and measure the h1's left edge on an inner page at 375, not only on the landing.

## 25. A bounded panel still sits eight seats when the picker says eight

This run seated the picker's eight seats (Debord, Shklovsky, Holmes, Mace, Cairo, Tufte, Krug, Kahneman), three at a
time, each reading its own seat file and filing to a directory: 27 seat reports over three rounds, none lost. R1
produced 8 OBJECTs and R2 7 PASSes, so the cost of the full panel was the finding that two moves were wrong (the
Restore button, the dimming) before they shipped.

## 26. Audit the source data before the first move

Global-Indexes inherited one data file and the brief was to add more. Before any front end: the inherited file was not valid
JSON (a stray brace and a junk tail), 426 of its 500 rows had a rank that contradicted the score, and the first build of the
new files had "Korea" and "South Korea" both in the HDI file (a duplicate that inflated n), "Czechia" beside "Czech Republic",
territories in the denominators and an 18-way tie at a floor value. Cairo's R0 found most of it by recomputing every rank from
its score; the checker needs a fixture that must fail (`--selftest`) or it can pass vacuously.

## 27. Check the archive's file sizes, and list what it could not supply

Five of the fourteen datasets sought in an open archive were 0-byte files and one was a three-value category, not a score.
Only eight were usable. The page says "eight used of fourteen sought" and names the omissions, because the omissions shaped
the site (democracy is represented by a satisfaction survey, not the usual regime indexes).

## 28. A rank is not a magnitude: print the score where the position is drawn

Tufte measured the lie factor: on the violence axis, 20 percentile points in the middle hold under 1% of the score range and
the bottom 10% hold 94%. A parallel chart of ranks cannot show that, so the score at both ends of every axis is printed, with
"high score on top" or "low score on top", and the caption says equal steps are equal in rank, not in score.

## 29. A change over time compares like with like

"Biggest movers" first ranked each year among whoever was covered that year. HDI 1980 covers 104 countries and 2017 covers
189, so Turkey (64th of 104, then 64th of 189) printed a +28 gain it never made. Rank within the countries present in both
years; the corrected figure is +26 (64th to 38th of 104), and the note prints both ns.

## 30. A censored value is not a first place

Hunger's 2.5 is the index's "less than 5" category: 18 countries share it, and a readout said "Best placed: 1st of 128".
Count ties in the summary, print `1st=` and "tied with 17 others", and name the category beside the score.

## 31. An index that counts harm is shown score-first and is not named best or worst

Sontag's rotation seat objected that death rates and hunger sat on a podium: "Highest/Lowest position" naming Brazil's
175th on violence, and a list of the largest drops. A `harm` flag in the manifest now makes the front end show the score first,
leave those indexes out of the highest/lowest sentence and show no movers list, with the reason on the page. A rotation seat
earned its place here: no required seat would have raised it.

## 32. A reviewer's test can be wrong: measure the premise

Krug's R1 finding said clicking a grey country line does nothing. A click at a real point on the line (path.getPointAtLength
through the SVG screen matrix) selected the country; the seat's own R2 run confirmed it. The resolution was OVERRULE with the
measurement, not a move.

## 33. Write scripts that contain a double dollar sign with the Write tool

Three shell commands were refused by the harness's safety check because the command text contained a double dollar sign
(shell PID syntax), for example in JavaScript calling a helper named with two dollar signs, even though nothing was deleted.
The refusal costs a rewrite. Write such files with the Write and Edit tools, and keep the shell for running them. The check
also tripped on the note about it, so the same rule applies to notes.

## 34. A sandbox can run a real Docker daemon, so a lesson can be run

`dockerd --iptables=false --storage-driver=vfs` starts a working daemon: image pulls, user-defined networks, published ports,
Compose and `docker swarm init` all worked; build-time network access did not (the npm registry gave `EAI_AGAIN`). The inherited
LearnDocker lessons failed when run (a container that exits at once, `docker-compose` not found). The rebuild runs all 34
commands in `data/lessons.json` against the daemon and stores the real output. A lab app with no dependencies keeps the build
runnable offline, and the page says why.

## 35. A gate must compare what the page prints with what the command is expected to print

Cairo's R1 fixture changed one `expect` to a string that cannot match and the static gate still exited 0: it checked links and
phrases but not the printed transcripts. The check now fails when a stored `out` does not satisfy its `expect` (unless the output
was filtered with `show` or `tail`). The full gate was already strict; the static one was not.

## 36. Measure a build cache honestly

The first scenario needs an empty cache (`docker builder prune -af`), a FROM step that finishes at once counts as reused (the base
image was already local), parallel BuildKit steps print in finish order and must be sorted by step number, and the lesson's claim
is asserted in the gate (editing server.js leaves `npm install` reused). Cairo rebuilt all five scenarios by hand and the numbers
matched.

## 37. Do not show one measurement under another condition

The "Change the base image" tab showed node:22 with node:24's size and layer count, because the code used one measured layer list
for every scenario. Show "size not measured" for what was not measured. A total must also match its label: "after FROM" excludes
FROM's time, and "9 layers" was history rows, not layers (4 add data).

## 38. Bars with a minimum width need a sentence that says so

A 0.5% minimum width made a 195-byte layer look like 0.9 MB, and the footnote said "to scale". Say "proportional to bytes, with a
minimum width", and print the byte value on the row. Tufte's further point stands: bytes are not the measure of what reran, so the
landing gained a grid of all five builds with the times.

## 39. Name controls by what they act on, and announce one sentence

Holmes: twenty copy buttons all named "Copy to clipboard"; a live region that re-read a 60-word readout on every tab press; a
toggle whose label changed while aria-pressed stayed. Name each copy button by its command, keep a separate short status line for
the live region, and give a toggle one fixed label or one changing label, not both.

## 40. A minus: the run played it safe (LearnDocker)

Graded A- with the words "pretty good playing it a bit safe". The Breaker (the build as layers) landed, but both Shklovsky and
Mondrian said the form was a familiar diagram and the caption did the seeing, and four ambition findings (the cache fact as the
form, failure moments breaking the template, the Dockerfile beside the stack on a phone, time as bar length) were DEFERRED while
every defect finding was ADAPTed. When the correct fixes are all cheap and the bold ones are deferred, the run drifts to safe.
Next run: in R1, take at least one Rupture or Breaker finding as a move, not a deferral, before closing the defect list, and
re-seat every objecting seat in R2.

## 41. A defect list alone yields a B+ (security-site run 1)

Graded B+ ("pretty good site but playing too safe"). Every honesty finding was adopted and every one of the eight seats was
answered, yet the landing was three bars on a cream page: Shklovsky and Nietzsche both said it was restrained to a fault and the
fix was a linear strip, not a new form. A safe-run warning from the ledger (LearnDocker, A-) did not change the brief. Put "name
the boldest version of the landing" in every seat's R0 brief when the previous run was marked safe, and take the Rupture seat's
finding as the move.

## 42. The bold run: take the Breaker finding as the whole landing (security-site run 2, graded A)

"Make the duration felt" became a year wheel (one lap = one year, three concentric arcs from measured hash rates), with a dynamic
theme: one registered CSS number, `--heat`, mixed an OKLab accent from hot pink to lime with the answer. The seats that had
objected to honesty in run 1 objected to the colour in run 2 (is lime a verdict?); capping the colour where the model is blind
and stating its meaning beside the graphic resolved most of it.

## 43. When the bold form saturates, add a labelled second scale

Arnheim and Tufte both found that strong passwords drew three identical full rings. A log ruler (1 second to the age of the
universe, labelled "equal distance = equal ratio", with the wheel's first year shaded) made the saturated states differ. Say plainly
that the two scales differ; do not let the log scale pass as linear.

## 44. A heuristic detector needs a measured false-positive rate

A "word with digits" regex flagged 70% of random strong passwords and told them they looked like words (Cairo measured it on
2,000 strings). The rewrite uses 40 hand-picked base words after stripping leading and trailing digits and symbols and undoing
look-alike swaps; the gate now generates 4,000 random strings and fails above 1%. Ask every seat "what does this wrongly say about
a strong, ordinary case?"

## 45. A stylesheet overrides an SVG presentation attribute

Twice the same trap: `font-size` and `text-anchor` set as attributes were silently overridden by the stylesheet, so a numeral
did not shrink and a label stayed centred and clipped. Set size, anchor and opacity of SVG text through CSSOM. Under a strict
Content-Security-Policy, set geometry through attributes and style through `element.style`, never a `style=""` attribute (an
empty one set with setAttribute may be refused).

## 46. SVG text is read at about half size on a phone

A 690-unit viewBox shown at 343 px halves every glyph: 17 units became 8.5 px. Keep SVG text at 20 units or more, and measure the
rendered size with getComputedStyle times the SVG scale. At 320 px the captions still fall under 10 px; say so.

## 47. Mutate the gate to see it fail

Cairo's mutants showed what the gate missed: a moved tick label, a changed universe tick, a removed amber cap, a 4 px ruler font,
a weakened accent through an appended `:root` rule. The gate now compares tick labels with the times they name and checks the
drawing rules and minimum text sizes; the appended-rule case remains a known gap (it reads declarations, not the cascade).

## 48. Keep grades out of the project repository

The user's rule: grades are recorded in the dada ledger, not in the project repo. A DESIGN-LOG in the project may describe the
user's review in words ("pretty good but too safe") but not a letter grade. The ledger import takes `--grade` and `--grade-words`.

## 49. A graphic draws what the tested model returns, never a recomputation (off-grid-electric)

The first hero's circuit strip computed its own flows from the appliance schedule and showed full delivered power in a blackout
and a full battery as "idle" (Tufte). The simulation was extended to return what really flowed (solar used, sun wasted, battery bus
power, load served) and the hero draws only those; the gate asserts served = solar used - battery power at every step.

## 50. Move every decision into the tested model, pin the reviewed constants, mutate before the panel

Cairo's R1 mutants (fuse 1.25 to 1.0, 48 V rest x4 to x3, beta, sizing margin, ceil to floor, US 120 to 110 V, microwave 1500 to
1000 W, LiFePO4 depth) 9 of 10 survived because the gate tested `power.js` while the pages' glue and `model.json` values were
untested. Rounding, the fuse factor, rest-voltage scaling, string status, wire status and the verdict labels moved into `power.js`;
the gate pins every design constant (a deliberate change must update it) and tests the verdict scenarios. R2: 10 of 11 died; the
survivors (label order, the "tight" boundary, fuse rounding, the metric constant) were pinned the same hour.

## 51. A green verdict needs a "not checked" line, and limits are graded on what is served

"OK, the cabin runs through the night" over a model that ignored current, inverter size, wire, fuses and string voltage was
spectacle (Debord). The verdict became four checks (energy, depth, battery current, inverter), labels ranked NO POWER over
OVERLOAD over TOO DEEP over NEAR LIMIT over OK, the wording "on paper the energy balance holds", and a line listing what is not
checked. Battery current and inverter load are graded on the power actually served, not a hypothetical peak.

## 52. Draw SVG in real pixels so text is the size it is written

A fixed viewBox scaled to the container made 17-unit labels 8.4 to 10 px on a phone (Holmes, Cairo). The hero and chart now set
viewBox from the container's width and redraw on resize, with CSS sizes in px (12 px minimum), and a minimum width of 240 so a 320 px
phone does not scale them down. The gate checks the CSS sizes and that the script draws from clientWidth.

## 53. A fixed chart scale for the chosen system; clip and label what exceeds it

Auto-scaling the power axis to the largest load made the sun's arc shrink to 18% of its height when the microwave was flipped (lie
factor about 4; Tufte, Pater). The axis is now set by the panels, a large load is clipped, and "load peaks at N W" says so.
Potential, used and wasted sun are separate series.

## 54. One body whose fill is the quantity beats a dashboard (and the Rupture finding became the move)

Shklovsky's R1 refused the dashboard (a verdict box, a chart and a circuit strip) and asked for the battery as the hero. A battery
drawn the page's width, ten cells, a red dashed floor and flows in watts, run by a scrubber and a Play button, earned his PASS in R2;
Pater called it a theme. Taking the Rupture seat's finding as the move in R1 (the lesson from the security-site grade) worked.

## 55. Put the first action within one scroll on a phone

The breakers, which the headline tells you to flip, sat 1,320 px down at 375 px (Krug). The controls were split into two boxes so
the breakers follow the hero, then the verdict, then the system sliders. The desktop layout kept two columns.

## 56. Check for a stale card before adding one to the portfolio

The portfolio already had an `off-grid-electric` card with the old title and a vercel.app link; the add script's assertion
failed and the first push only replaced the images. Update the existing entry in place (title, line, tags, `.shadw.app` link).
An earlier one-pass run's grade, stated by the user and written in the project's own log, was imported into the ledger from the old
log and removed from the repository.

## 57. Sweep the model across its whole range before the panel; an instrument that teaches must fail as an event
Source: off-grid-electric run 2 (an interactive multimeter, 9 Nov 2026).

A virtual meter read 0.000 V across a loaded cable from 07:30 to 17:00 because the cable carried only the battery's *net* current
and the panel was charging; it was right at night. Only a seat that swept the day found it. Sweep the model over its range (time,
system voltage, state of charge) and pin each constant against an independent figure, then mutate the gate: eight surviving
mutants were killed before the second round. Two more rules: a diagram that draws no measured quantity is a map (print the values,
ink the live state); and a failure the page exists to teach (a blown fuse) must be an event (motion, sound, an explanation that
stays) rather than a colour swap. Phones: a sticky header of 146 px and an eight-link contents list put the first action 1.9 screens
down; make the header static there and collapse the list.

## 58. A diagnosis exercise is a claim about the model: prove each case solvable and unambiguous in the gate
Source: off-grid-electric run 3 (the multimeter lab, 9 Nov 2026).

Five hidden-fault cases were written and believed solvable. The evidence seat swept the day and found one whose signature a healthy
system reproduced every afternoon, one that displayed another fault's signature, and symptoms quoting numbers (90%, 80%) the
learner could not measure and the simulation contradicted. Put each case's evidence in data, run it through the model in the gate,
and require that it fits no other fault, not a healthy system, and holds at the time the slider can be left on (or lock the slider).
Also: touch drags need touch-action none on the svg, not its children; restore focus to the same control after repainting a panel;
leave the answer out of the picture until the learner commits, then reveal it.

## 59. A theme that is the data beats a theme that is decoration, and "looks like other sites" is a colour and a font problem
Source: boilerplate-site, a Next.js rafting rebuild (9 Nov 2026). First version graded B plus: "color is a bit uninspired but design is good, looks too much like other rafting sites vibe-wise". Second graded A minus.

The first theme was teal, orange and foam: the colours of every rafting brochure. The fix was a different genre, not a different hue: a flood-warning poster (near-black ink, warm paper, hi-vis acid, a hazard-stripe header, a giant mono scoreboard of the gauge) whose page colour is the river level itself on a heat scale. Interpolate the scale in oklch, not oklab: in oklab the middle of acid to cobalt went grey-teal and cobalt to crimson went lilac (the evidence and graphic seats called the middle "safe"). Gate the contrast of text over the page at nine points of the scale in both schemes, and re-check the dark scheme: a readout panel that used the text colour as its background was 1.08:1 in dark.
The structural finding of the run: the model computed each rapid's class and then ignored it when admitting riders. A computed quantity must reach every decision that depends on it, and the sentence, status word and badge must use the same rounded value the rule compares, or the page contradicts itself ("class II+, limit II+"). Also: a number box needs a draft (typing "3" of "3000" was rejected as below the minimum), a unit (cfs) needs a definition at first use, and the first action must be in the first viewport on a phone.

## 60. When you compare your own approach with two others, sweep the comparison model against itself, and hash what you checked
Source: uTCP (a UTCP vs MCP comparison with the DADA manual as the synthesis), 9 Nov 2026.

The first calculator counted UTCP's "one manual" as twelve files and the hybrid's "one manual" as one, and the hybrid won on files in 10,904 of 10,910 swept cases: a metric the author had defined. The same run had a gate for facts but none for fairness. Make the model treat every architecture alike, say plainly when your approach equals a rival on the structural counts, and have the gate fail if any architecture is strictly best on every column. Also: absence is a claim (back it with a search that must return a stated number of files, or mark the cell OUR READING); a quote can sit beside a sentence that undoes it (MCP's "must obtain user consent" is followed by "MCP itself cannot enforce these security principles"); the gate exited 0 with an invented quote when no clones were present until every claim, compare row and crosswalk row was hashed at the moment it was last read against the sources (`verify-sources.mjs --stamp`), so editing a sentence means re-reading its quote; generate chart geometry from the data into a stylesheet (proportional with or without JavaScript, no inline style); and class names are global (a new `.bar` broke the header that already used it).


**61. A fix to a version is a fix to the thing that checks it (uTCP and 3dada, 2026-11-10).** 3dada's manual said 1.0.0 while it pinned its parent at 1.1.0 and had gained floors and a registry; its validator failed when run bare because it loaded a parent only when told to, and CI told it to, so nothing red ever showed. Bump the fork's own version when its contents change, default the validator to the vendored parent so the pin is enforced on every run, and when a copy of a manual lags (dada-changes' is 1.0.0 against the 1.1.0 others vendor) say so instead of syncing a half: its schema and validator lag with it. A site is "configured to deploy" only against the platform's own detector rules (Shadw: a static preset needs a root `index.html` or `outputDirectory`; a `start` script or `server.*` at the root flips it to `node`), so write the config to those and keep the root free of both.

## 64. Carry the hero's notation to the pages whose subject it is (LearnC)

The address rule (note 1) puts the break on the home page. When the break is a
*notation* (LearnC drew the whole site as a C pointer diagram: struct boxes,
parent pointers, arrays, NULL), the inner pages whose subject is that notation
must speak it too, or the device is a cover and not a grammar. Shklovsky
objected in R1 that the Pointers lesson explained `&num` in prose under a
home page that had taught the reader to read wires. The fix drew memory before
the code on the pointer, struct and heap lessons, and opened every language
page with its own struct box wired to its parent. The other inner pages stayed
plain, and Shklovsky passed in R3. The rule is the address rule refined: the
break recurs where the page's subject *is* the device, and nowhere else.

## 65. Size is not estrangement: aim S4 at strangeness, not scale (LearnC)

S4 asks for the boldest element pushed further. LearnC enlarged the root C
glyph from 98 to 129 px and measured it. Shklovsky passed it, but named the
cost: a bigger red C echoed the logo and the headline's red C, so the push
read as branding. Mace found that the bigger glyph now touched the focus ring.
A push that only scales repeats what the eye has already recognised. Push the
device's strangeness instead (here, the C as a char literal `'C'`), and
re-measure the focus and fold rules afterwards, because a push changes
geometry that earlier fixes relied on.

## 66. The evidence file is an instrument and fails like one (LearnC)

Across six rounds of LearnC, every defect the measurement seats found after R1
came either from a page the conductor's script did not measure or from a claim
the conductor paraphrased into the evidence file: a stale y-coordinate, "0
warnings" under narrower flags than the page claimed, a page count of 15
against a site of 22. Write the evidence file from the script's output, not
from memory. Have the script enumerate the artifact, and re-run it after the
last edit, so the panel judges the site rather than the conductor's summary of
it.


## 67. A name that invites a theme is a Frontier candidate, not a cliché to refuse (Learn Java)

Learn Java's Traversal Plan rejected "a coffee cup" as a cliché and led with the true, strange and legible hex dump of `Hello.class`. Every seat judged the dump on its own terms: Tufte measured a lie factor of 1.0, Krug's probe passed and Shklovsky called it estranging. The owner graded it B+: "more coffee type theme … colors too similar". No seat held the question "does the first screen feel like the thing it teaches?", and six pastel tints of one value read as one colour. The café that replaced it (a latte glass whose layers link the site, a chalkboard menu of the lessons) kept the class file on its own page and in every lesson's ribbon. The rule: when a subject's name carries a theme (Java and coffee, Rust and oxidation, Python and snakes), list the theme as a Frontier candidate and let the panel weigh it; seat a subject-character critic (Sharp or Hara) from R1; and give categorical colours different values as well as different hues.

## 68. A seat's prescribed value is a change like any other: re-measure it (blockchain-explain 2.0)

Three things from the blockchain-explain makeover (Adaptive Full, R0 to R4, ungraded at the time of writing).
- **Prescriptions regress.** Greenberg's R3 fix for uneven footer leading (`padding:12px 0` on inline links) left the links 39 px tall, under the 44 px floor; the same seat caught it in R4. Shklovsky's R3 device (the drawn link snaps at a break) exposed a stale status line in R4. Apply a seat's exact value, then run the Step 2g measure before the round closes, not after the next panel.
- **When the vendor's own page cannot be read, say where the words came from.** The case-study source was outside the session's network. The page cites the earlier version of the site at its commit and says it is not a quotation, and the hero's second chain became generic rather than drawing a claim the vendor was not quoted as making. Carry the real source forward.
- **Compute the demo, and show what the copy asserts.** Every hash was computed by the build and recomputed in the browser, with a self-check that the two agree; Tufte still objected that "62 of 64 digits differ" was asserted, not shown. Put both values on the page with the matches marked.

## 69. A framing objection is answered by the structure, not by the wording (blockchain-explain 2.0)

R0 Debord objected that the old site was Autheo's vendor copy. R1 to R4 answered it in the words: "Autheo describes itself as…", unsourced figures cut, a generic Chain B. But the skeleton stayed Autheo's own stack (CometBFT, Cosmos SDK, EVM, "Layer 0"), with a page per component. Nine seats over four rounds passed the site's truth and access. The owner saw it at once: "it's supposed to be about blockchain, more general guide, not just Autheo… it seems bad." The fix was structural: the topics a general reader needs (keys, proof of work and stake, contracts, layer 2, bridges, chains compared, risks) became the pages, and the vendor became one case study.
- When R0 says the work serves one party, re-derive the page list from the reader's questions before writing a word, and have a seat check the nav, not only the copy.
- Brief one seat each round with the owner's brief in their words and the nav list, and ask "is this the site that was asked for?"

## 70. "Sloppy" means no template: give every page one, and measure the figures (blockchain-explain, B-)

The general guide passed R5 on facts and the measuring script on every floor, and the owner still graded it B-: "needs all pages, very sloppy". Full-page screenshots of all 16 pages showed why: the topic pages were long text columns with three-line headings, a different chip strip on each, cramped demo controls, and a home page with two left edges. Nothing was broken; nothing was made.
- When an owner says "sloppy", screenshot every page at full height before touching code, and fix the template, not the pages one by one: a fixed frame (where you are, the one-line idea, one figure, numbered sections, a Try-it panel, the pager) made all 16 pages consistent in one pass.
- Measure the figures, not just the HTML. The measuring script read CSS font sizes, so an SVG label scaled down to 10.9 px at 320 px, a label clipped at the viewBox edge, and a label covered by a box all passed it. Seats found all three by hand. `measure.cjs` now checks every SVG label for clipping, for rendered size and for overlap with a box it is not inside.
- Run the panel on fresh screenshots each round. In R6 one seat flagged the evidence screenshots as stale against the live build.
- The build's deploy check compared `static_dir` but not `routes`, so `fluid.json` shipped with Vercel-style `{"src", "dest"}` routes and Shadw refused it ("missing field `pattern`"). A deploy check compares every field the rule names: here `routes == [{"pattern": "/", "target": "static"}]`.
- The redo was graded A- ("very good but falling into the same colour trap"): the four levels were four values of one green, as Learn Java's first palette was "too similar". A ramp of one hue says "more or less of the same thing"; levels that are different things need different hues, ordered by value so the ramp still reads. Check it on the landing graphic before the panel does.

