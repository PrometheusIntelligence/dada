# Case study: The Holy Temple (2026-11-03..12)

The first game GDADA carried from an idea to store-ready builds. A surreal exploration RPG written in HolyC, running inside TempleOS V5.03,
in the look of "an obscure RPG made by one extremely strange programmer in 2001". Repositories: `SolutionsAsService/ThirdTemple` (the game),
`SolutionsAsService/TempleOS` (the OS fork and its backend, `Backend/tools/gamec.mjs`), `SolutionsAsService/cpp-sprites` (the `hcviz`
viewer), `SolutionsAsService/temple-music` (the browser listener), `SolutionsAsService/holy-temple-map` (the atlas site), this skill.
Read it as a worked example: what was built, in what order, what the person's grades taught, and which tools made scale possible.

## Where it ended

| | |
|---|---|
| World | 23 regions, 365 maps (scrolling districts up to 80x56), 367 people with faces and JSON files, 3,223 reactions, 3,835 examine texts |
| Systems | 39 standoffs (stats BRAWN/WIT/CHARM/NERVE, clue keys from other regions, a model standoff with odds), 433 notebook questions, 29 dossier entries (never resolved), 23 found journals, loot with gifts and trades (every thing has several roads), a director that paces encounters by played time, a cross-run memory, hidden opinions, a clock with schedules |
| Content from a real archive | THE INDEX (an index, not a finding; the sorting table), the Room Rule, Room 8F, the Approach, the Institute for Long Thought, Foxbone Park and Robert Handsome |
| Sound | 27 one-voice tunes (A-B-A', 10-20 s loops, a motif per region), WAV previews and a browser listener |
| Ties | 85 doors between regions, 144 threads; 0 zones failing the playground test; every region with threads in and out |
| Proof | compiles and passes its tests in real TempleOS (`gamec run`, verdict PASS); the bundle and the Steam/itch Linux build played headless end to end (save, power off, continue); save format v15 reads v12-v14 |
| Release | zip bundle (QEMU), VirtualBox setup, Steam depots and SteamPipe scripts, itch.io channels with manifests, store art, licence (game EULA; TempleOS public domain, credited to Terry A. Davis); one command (`tools/release.sh`) builds all and uploads nothing |

## The order that worked

1. **Vision first** ([vision-template.md](vision-template.md)): the person's words, quoted, numbered as Must-haves (59 by the end), a dated
   change log. Every later direction went in before it was built (rules 57-59 record the person's decisions on real references).
2. **Engine proven small, in the real OS early enough.** The first TempleOS compile found six classes of error no host lint knew
   (holyc H1-H6); each became a lint. Until then everything was "source-only", and said so.
3. **The world as text, not code** (world L1): `world/**/*.map`, `cast/**/*.json`, `world/*.txt`, compiled to HolyC by `tools/make_world.py`
   with host validators (`check_world.mjs`, `map_rules.mjs`, `lint_order.py`, `npc_check.mjs`). This took the game from 15 to 178 maps in a
   day, then to 365, written by many helpers at once.
4. **Regions by helpers, each in isolation, merged by the lead** (world L4-L6, production R1-R2): a wired entry, a private build, a one-command
   check; shared limits checked at merge (world L2).
5. **Grades from the person drive every polish pass.** Maps graded B became A- by placement rules learned from the grades ([map-craft.md](map-craft.md)
   P1-P16); sprites by silhouette metrics ([sprite-lessons.md](sprite-lessons.md)); faces by the Maurice recipe and the eye rules
   ([portrait-craft.md](portrait-craft.md) E1-E3); music by "too short" ([music-craft.md](music-craft.md) M1-M11).
6. **Playground, then threads** ([world-ties.md](world-ties.md)): every zone two roads in, then every region tied by something earned.
7. **Distribution** ([release-craft.md](release-craft.md)): installed disk, autostart, first boot at build time, saves outside the store's
   folder, launchers, store builds, one release command.

## What the person's words changed (a sample)

| Words | Became |
|---|---|
| "too same" (maps) | region colour themes; one field, one runner, one feature per room (world L22) |
| "the bus is wrong" (scale) | measure every object against the person in cells (map P14-P16); a scale audit |
| "multiple ways to get to new zones ... playground style" | the zone audit and 8 new roads (world L26) |
| "eyes a bit too kawaii ... asymmetric" | draw one eye and mirror it; an adult eye is an almond (portrait E1-E2) |
| "encounters should use closeups generally" | the standoff's face close-up at 3x for the person you face |
| "sand is an A but needs to be drawn out" | answer a graded motif instead of padding it (music M3); a motif keeper in `music_check.py` |
| "NONO MAKE THE PAVILION BLUE AND WHITE" | never "fix" an owner's deliberate reference; flag, ask, record (world L25) |
| "it's okay to have direct references; the game is about what humans know and don't know" | VISION 58; [archive-craft.md](archive-craft.md) |
| "there has to be a way to use gdada without slowing too much" | the Quick run (SKILL.md) |

## What failed, and what it taught

- A force-directed atlas overlapped; a layered layout by door distance did not (world-ties).
- An audit's zeroes were a bug (`encounter E_` vs `enc E_`): verify an audit against one traced example (world L31).
- The ahead-of-time compile hung TempleOS; recorded as open with what was learned (holyc H17-H21), compile-on-launch stays.
- A boot race passed once and failed the next run (holyc H23, production R10).
- Hand edits to generated files were wiped (production R7); a broad `pkill` and a broad `rm -rf` cost a helper's run and the scratchpad
  (production R3).

## Open at the end

QEMU for Windows to bundle (needs a PC with internet), a real Windows/Mac/Deck run, store accounts and uploads (the owner's), the
precompile option, 5 item slots left before the next save widening, a faint stripe on the Institute floor, standoff labels unseen on screen.
