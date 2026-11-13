# NPC run type: a character is a file, not a sprite

An **NPC run** designs people one at a time and writes each as one JSON file (`cast/<region>/<id>.json`). The file is the source of truth for the
face, the voice, the lines, the behaviour and the links to other people. The build reads the file; nothing about the person lives only in a map,
a sprite or the author's head. Read [world-lessons.md](world-lessons.md) (L15, dialogue voice) and the person's grades first; append what a run teaches.

## The person's own rules (graded, so far)
- A person is made of **a confession and a specific object**, not of a joke shape. A-grade lines: the councillor who abstained *in the gallery, so no one would see*;
  the safety officer whose accidents were *reclassified as events*; the mail sorter who sorts *by feeling*. C-grade lines: wordplay with no person in it; plain bureaucracy with no turn.
- Test every line: **could only this person say it?** If any other person on the cast sheet could, rewrite it or cut it.
- "Too generic and similar" is a failure of the file, not of the art: two people who share a face *and* a voice are one person. The check below counts it.
- Honour canon first. Eddie and Gerald are reptilian, Maurice is a bird-headed salesman, Unit 04 and Harold-7 are robots, the Operator is a shadow with a headset (design/npc-design, gdada-characters.md). Species decides face, diction and what they find strange about *us*.

## The schema (all fields required unless marked)
```
id, name, region, home, sprite
special        null, or a drawn non-person (lamassu, robot, ...)
species        human | reptile | bird | robot | shadow | stone | other (say what)
role           what they do, in six words, and where
look           face-build fields (gender, age, skin, face_w, face_h, jaw, hair_color, hair_style, facial, brows, eyes, eye_color, nose, mouth,
               glasses, hat, top, color, tie, marks[], accessory) + "distinct": the ONE thing a player remembers (a sentence) and the face must show it
mind           traits[3] (at least one that contradicts another), want, fear, secret, keeps (an object), tic, mood
voice          form (their sentence habit, one of: address gossip notice question inventory fragment anecdote surroundings numbers formal chatty nonsequitur stage), register (the way they talk, one sentence), diction[2-4 hard rules: e.g. never contracts, always answers a question with a number],
               never_says[1-3 words or phrases], verbal_habit, sample (one line that is unmistakably them)
behavior       routine (what they do when nobody is talking to them), schedule[] (mirror of schedules.txt, read only), reacts[] of {when, then}: FIVE OR MORE, three or more kinds of trigger,
               where when is one of: first_meeting, returning, talked:N, late_night, morning, afternoon, evening, holding:<IT_X>, flag:<FL_X>, asked:<Q_X>, answered:<Q_X>, mind_low, mind_high, many_questions, in_company_of:<id>, random:N (1 time in N, repeatable)
               and then is one short sentence of what they do or say; on_leave (what they do when the player walks away)
relationships  [{with: id, feeling, what_they_say}]  (at least one, and one must be to someone in another region)
lines          [{text, register}] 4 to 8 lines, registers: intro, banter, confession, lore, reaction; text obeys the 72 column / '|' break rules
links          mentions[] / mentioned_by[] (filled by the build from design/WORLD-LINKS.md)
```
Lines in the file are written into the map's say block between `# cast-begin:ID` and `# cast-end:ID` by `tools/make_cast.py --sync`; hand-written map lines stay. Never edit the block in the map.

## The process (one person at a time; at most 12 per sitting)
1. **Read** the person's map, their existing lines, their neighbours' lines and the links file. Know the room, the hour, who they stand next to.
2. **Decide the one thing** (`look.distinct`) and the contradiction (a thing they say they believe and the thing their desk shows). Everything else follows from those two.
3. **Voice first, then lines.** Write `voice` and `sample` before any line. Then write the lines *in that voice*; every line carries a specific object, number or named neighbour.
4. **Behaviour as data**: three reactions that a bot or a person could observe (a place they are at a time, a thing they say when the player holds an item, an answered question).
5. **Links**: point at people who exist. One relationship must cross a region, so the world is a web, not a set of rooms.
6. **Check**: run `node scripts/npc_check.mjs <cast dir>`; fix every finding; then run the game's own build and dialogue check.
7. **Show lines for grading** (ten at a time, with speaker and place) and record the person's grades in art-grades.json. The grade is the gate.

## The check (`scripts/npc_check.mjs`)
Fails on: a missing or mistyped field; fewer than 4 or more than 8 lines; a line wider than 72 columns; a line copied by two people; any six-word run that appears in the lines of
three or more people (template voice); `voice.sample` missing from the lines' register (must differ from every line); a relationship to an id that is not in the cast; two people
with the same face *and* the same first trait (clones); a species other than human with a human `special: null` look that shows no species feature (`distinct` must name it).
Reports (not failures): the five most similar pairs of people by voice words, and how many people share each hat, hair style and top.

## Species presets and compiled behaviour
`cast/presets/<species>.json` holds the defaults for a kind of person: `render` (which face drawing), `voice_hints` (diction ideas to start the voice from) and `reacts` (reactions every one of that kind has). Presets exist for human, reptile, bird, robot, shadow, stone, faceless and ghost; a new kind of person needs a preset first. The build **compiles behaviour to HolyC**: `behavior.reacts` plus the preset's reacts become `GenReact(n)` in `Src/React.HC`, which `Talk()` calls before a person's ordinary words (first_meeting, returning, late_night, holding:IT_, flag:FL_, asked:Q_, answered:Q_; each once per person per session). A lower-case `then` is a stage direction ("(NAME does it.)"); a sentence is spoken. There is no JSON interpreter in the game: JSON is the source, HolyC is generated.

## Variety rules (from the person's grade: "a lot of the dialogue is I, I, I and sounds like the same voice")
- **No more than 40% of one person's lines may say "I"; no more than 35% across the cast** (the check counts). A confession is one register among several, not the voice.
- Every person has a `voice.form`, a sentence habit that shows in at least three of their lines: **address** (talks to *you*: "You will want the left door"), **gossip** (what other named people did or said), **notice** (signs, rules, announcements, imperatives), **question** (answers by asking), **inventory** (lists, counts, three of something), **fragment** (clipped, verbless), **anecdote** (a short past-tense story about someone), **surroundings** (the room, a thing in it, the weather; no self), **numbers** (dates, sums, measurements), **formal** (long passive sentences), **chatty** (run-ons and tangents), **nonsequitur** (dream logic), **stage** (parenthetical actions only, for the silent).
- Non-humans: the species sets *diction and what they notice*, not just a face. A robot reports, a lizard talks temperature and light, a bird talks perches and flocks and flinches at nets, a shadow speaks in line numbers and holds, stone speaks in oaths and centuries, a ghost uses the wrong tense. Write `look.distinct` as a full sensory description (two sentences: what you see, what you smell or hear), not a label.
- Expression: set `mind.mood`; the face's mouth follows it (bright smiles, tense/wary frowns, drowsy/flat stays flat).
