# Sprite lessons (a ledger; read first, append last)

Every Art run reads this whole file at Step 0 and appends at least one entry at the end. An entry has a number, a date and a
game, **Evidence** (a measurement or the person's own words) and a **Rule**. Entries are never deleted; a wrong one is
superseded by a later entry that names it. `scripts/check_sprite_lessons.mjs` checks the format.

### L1 (2026-11-08, The Holy Temple)
**Evidence:** a first pass built every person from one body template. Measured with `hcviz --metrics`: 34 of 36 sprites had a
near-identical silhouette. After varying height, width, props and posture: 13, 8, 4, then 2 of 36 (mean pair distance 54 -> 66 px).
**Rule:** silhouette before colour. Never build a cast from one template; give each person a height, a width, a posture and one
shape that sticks out past the body, then add colour.

### L2 (2026-11-08, The Holy Temple)
**Evidence:** squashing the body (not the head) to a per-character height moved the near-twin count from 34 to 13 on its own.
**Rule:** height is the cheapest silhouette lever. Give every character a target height in rows and fit to it; keep the head whole.

### L3 (2026-11-08, The Holy Temple)
**Evidence:** props that extend past the body (a cart, a level staff, a long fluorescent tube, a cane, a ledger, a bouquet, a clipboard
taller than the clerk) removed most of the remaining twins; hair colour removed none.
**Rule:** a thing carried does more than a colour worn. Each character carries one thing only they carry, drawn so it breaks the outline.

### L4 (2026-11-08, The Holy Temple)
**Evidence:** the four Wrong Face sprites were flagged as twins of each other and of the player (diff 0 px).
**Rule:** declare twin groups on purpose (same name prefix), make the face the only difference inside one, and keep a group's body
distinct from everyone outside it. Print the declared groups, not only the count.

### L5 (2026-11-08, The Holy Temple)
**Evidence:** the design says of Gerald that his species is not his defining trait, and he is Eddie's cousin.
**Rule:** two characters of one species differ in clothing, height, bearing and the size of the species trait (Eddie: slouch, red cap,
long tail, green; Gerald: upright, shirt and tie and glasses, short tail, teal). Never let the species be the whole character.

### L6 (2026-11-08, The Holy Temple)
**Evidence:** the first metric, intersection over union, flagged 34 of 36 because same-height humanoids always overlap above 0.8.
A metric that flags nearly everything cannot guide a redraw.
**Rule:** measure distinctness as pixels that differ between silhouettes, with a pixel threshold (30 px at 16x24), and print the
count over the denominator. If the first metric flags almost everything or nothing, change the metric before changing the art.

### L7 (2026-11-08, The Holy Temple)
**Evidence:** the person's words after seeing the 8x8 art: "I agree with the art we need to scale it up a bit add more pixels but its
great start continue all that and improve characters sprites a lot also read about the other weirder characters like non humans".
**Rule:** raise the pixel density by drawing the art larger and showing it at the same on-screen size (16x16 tiles and 16x24 people at
2x kept the 32 px tile, so no map or code layout changed). Read the weird characters first; they are where a template fails.

### L8 (2026-11-08, The Holy Temple)
**Evidence:** at 4x the cast looked varied; the silhouette sheet showed one blob; the 1x sheet showed what a player sees.
**Rule:** always judge three renders: colour at the game's scale, flat silhouettes, and 1x. A character that works in only one is not done.

### L9 (2026-11-08, The Holy Temple)
**Evidence:** palette index 12 is dirty pink in town and red in the temple palette, so skin turns red there; index 4 turns blood red.
**Rule:** draw skin and signature colours knowing both palettes. Render with the second palette before calling a sprite finished;
a red suit that is meant to be red in the temple is a feature, a red face on everyone is not.

### L10 (2026-11-08, The Holy Temple)
**Evidence:** drawing the ancient builders, `fit()` can only shorten a figure. A first S_ARCHAEOLOGIST drew 23 rows and was fitted to 17: the face sank into the shirt and the figure read as a hat on a blob. Raising the target to 19 fixed the read. S_LAMASSU drew 20 rows against a target of 17 for the same reason.
**Rule:** draw each sprite at, or just above, its target height; print the drawn top, bottom and natural height before choosing the target. Squashing is for the body, and a head that loses its neck stops reading.

### L11 (2026-11-08, The Holy Temple)
**Evidence:** a closed arc of pale cyan over a pale head (S_PREVIOUS) read as a chalice or a funnel in the 4x preview. Two separate crescent horns rising from the sides of the head, with a gap above it, read as "horned" while the face stayed blank.
**Rule:** a halo or crown on a pale head must break into separate shapes with a gap; a closed ring over a head reads as a vessel.

### L12 (2026-11-08, The Holy Temple)
**Evidence:** the scorpion man's tail, brown and red like his helmet and beard, read as part of a hood. Giving the tail its own colour family (gold and brown beads) and a white stinger tip fixed it; the near-twin distance to the nearest sprite was 98 px.
**Rule:** a prop that wraps the body needs its own colour family and a bright tip, or it merges with the body.

### L13 (2026-11-08, The Holy Temple)
**Evidence:** the first S_LAMASSU wings were a square block with a regular window pattern and read as a building. A stepped, curved sweep leaning back, with a few diagonal feather pixels, read as a wing.
**Rule:** a regular pattern at 16 px reads as a grid, which reads as architecture. Break patterns with a curve and a few off-axis pixels.

### L14 (2026-11-08, The Holy Temple)
**Evidence:** S_WATERBEARER measured nine colours against a limit of eight. Dropping the off-white eye and the shaded mouth gave seven.
**Rule:** reuse existing indices for eyes and mouths (index 0 and a body colour) and spend the colour budget on the signature item.

### L15 (2026-11-08, The Holy Temple)
**Evidence:** wide quadrupeds and low figures separated easily (S_LAMASSU 86 px, S_UNBORNKING 62 px to the nearest sprite). The lowest-distance new sprite was the human-shaped S_ARCHAEOLOGIST at 44 px to S_PLAYER_DOWN.
**Rule:** ordinary human proportions are the real twin risk. Spend the most effort on the plain human, and give the exotic figures the cheapest lever they already have (width, height, an extending shape).

### L16 (2026-11-08, The Holy Temple)
**Evidence:** a long snout reads only in profile. The ibis, hawk, crocodile and the long-snouted beast, drawn side-on with the snout extending right (the crocodile's is 10 px long), read at once in the 1x sheet. Front-facing heads (jackal, baboon) read as dark blobs unless their ears or horns break the outline. The baboon, vulture, cobra and sun-clerk were the weakest reads.
**Rule:** draw a snout or beak in profile; for a front-facing animal head, the ears, horns or crown must break the outline, because the face will not carry the species at 16 px.

### L17 (2026-11-08, The Holy Temple)
**Evidence:** the outline adds a 1 px halo, so a 1 px gap between a prop and the body vanishes in the silhouette sheet. The first Weigher feather and scale and the Midwife's knife read as body bumps.
**Rule:** give a prop at least 2 px of air, or a different silhouette direction; where it must touch the body, stagger it so the contact is one pixel wide.

### L18 (2026-11-08, The Holy Temple)
**Evidence:** with a 6-wide head, the horns or crown carry the species. The ram's curled horns, first drawn as closed white rings, looked like goggles. Opening the ring at the bottom and colouring it gold against a white face made it read as a ram.
**Rule:** horns get a colour that differs from the face, and spirals are open shapes, never closed loops.

### L19 (2026-11-08, The Holy Temple)
**Evidence:** a symmetric half-row helper (write columns 0 to 7, mirror to 8 to 15) made front-facing figures fast and error-free, and asymmetric props stamped on afterwards kept each figure from being a template. Three first drafts ran over eight colours (Nurse 9, Ledger-Bull 9, Counter 8) because ears, collar accents and props each took a new colour; reusing a body colour fixed it.
**Rule:** draw symmetric bodies by mirroring, then add the asymmetric thing only that character carries. Reuse a body colour for ears and accents and spend the budget on the signature prop.

### L20 (2026-11-08, The Holy Temple)
**Evidence:** height and an off-axis prop separated all 18 Registrars: the 14-row Dwarf, the 16-row round Midwife, and the 22-row figures with a staff, oar or feather (the Weigher is 21). All 18 are at least 38 px from every other sprite; a 9 px gold ball beside a hunched beetle-head (the Pusher) scored 85 px.
**Rule:** when a set of figures shares a visual grammar (here, bare chest, collar, kilt), separate them with height and one oversized off-axis prop, not with head detail.

### L21 (2026-11-08, The Holy Temple)
**Evidence:** the world designers asked for seven pieces the cast lacked (a cuneiform tablet, a ledger lectern, a reed boat, a car, a bus, a water tile, a faceless archivist). A car and a bus are wider than a tile: drawing each as one wide canvas and cropping it into 16 px pieces (two for the car, three for the bus) gave seamless vehicles in a few lines; the viewer first drew the dock's water as floor because a boat's tile and the water tile share a switch case that falls through, which the viewer's parser did not follow.
**Rule:** draw anything wider than a tile as one canvas and crop it. When an object must stand on something other than the map's floor (a boat on water), give it its own ground in the ground function, and make every tool that reads that function follow fall-through cases.

### L22 (2026-11-08, The Holy Temple)
**Evidence:** the faceless archivist reads as faceless because the head is a smooth pale oval with a shadow line at its edge and nothing inside it, against a robe pinned with notes; a body detail (the notes) tells the player what it does without a face.
**Rule:** a character with no face is told by what is around the blank: give the blank a shape and an edge, and put the personality in what is pinned to the body.

### L23 (2026-11-08, The Holy Temple)
**Evidence:** drawing two plain adult women for ordinary residents: a first pass with bun hair at height 21 gave a 17 px twin of S_ROSEN. Long hair at height 22 with a prop breaking the top outline (a leek standing out of a bag) cleared every twin.
**Rule:** hair style does not separate two ordinary people; height and a prop do.

### L24 (2026-11-08, The Holy Temple)
**Evidence:** a leek (1 to 2 px wide) on a green coat and pipe smoke vanished at 1x; a carried cable coil drawn as a hollow loop collapsed into a red box once `fit()` squashed the rows, while solid alternating red and black stripes survived and read as cable.
**Rule:** a prop needs a body at least 3 px wide or a colour that contrasts with the clothing beside it. Draw carried items as solid shapes with alternating bands, never as hollow loops, so they survive the squash.

### L25 (2026-11-08, The Holy Temple)
**Evidence:** the Director's shadowed face in index 1 on a grey suit read as a bottle; index 0 inside the 0 outline, with two pale pixels as the only light, gave "a face in shadow". A 22-row figure read as tall only because it had no wide parts below its hat brim.
**Rule:** a face in shadow is index 0 with the eyes as the only light. A very tall figure needs few horizontal details, and one focal point (a lighter clipboard at chest height).

### L26 (2026-11-08, The Holy Temple)
**Evidence:** the figure rule that nothing may draw above row 1 meant hard hats and brims that `human()` plus `hat()` start at row 0 had to be hand-placed from row 1, and an umbrella canopy had to overlap the hair rows rather than sit above them.
**Rule:** anything that must sit above the head loses a row to the margin rule; place it by hand and make the canopy overlap the head.

### L27 (2026-11-08, The Holy Temple)
**Evidence:** drawing 17 new objects (a sphinx, three bush alternatives, a hedge, a gravestone, a telephone pole, a hard-hat rack, a ticket machine, a fax machine, an intercom, an elevator door, a child's throne, a kiln, a green-screen desk, a CRT in a niche, a sealed door): hand-typed ASCII rows drifted in width and the art came out sloppy, so the first pass of every ASCII-grid piece was rewritten with rectangles, circles and shading calls and one `outline()`.
**Rule:** draw pixel art with primitives (rects, circles, lines, shading), not hand-typed rows; rows drift and hide mistakes.

### L28 (2026-11-08, The Holy Temple)
**Evidence:** a round clustered shape (the bush) drawn as overlapping circles painted back to front, each with a lit upper-left rim and a shaded lower-right rim, gave a lit side and a shade side with no speckle; this is why the redrawn bush beat the random-speckle bush graded B.
**Rule:** build a rounded cluster from overlapping circles with one light direction, never from random speckle.

### L29 (2026-11-08, The Holy Temple)
**Evidence:** a seamless tile built from a periodic unit (8-wide lumps, the second course offset by half, `x % 16` wrap) stayed seamless when tiled four across and still looked hand-made.
**Rule:** build a seamless tile from a periodic unit with an offset second course, and test it tiled, not alone.

### L30 (2026-11-08, The Holy Temple)
**Evidence:** a rectangle with two dots and a slot read as a face (the ticket machine's first display and slot looked like eyes and a mouth); a ring meant to read as a gap in the sealed door looked closed until the gap was widened and the ring enlarged to fill the door; overlapping pieces in one hue merged (gold hat brims on gold rails, a white hat on a pale rail) until the rails were made dark gray.
**Rule:** two dots and a slot make a face, so avoid that arrangement on machines; a gap that must read needs a clear gap; give overlapping pieces different hues or values.

### L31 (2026-11-08, The Holy Temple)
**Evidence:** the sphinx's weak paws and chest only showed when its two tile halves were viewed joined; each half looked fine alone.
**Rule:** a multi-tile piece needs a joined crop test, not a per-tile look. The grading sheet joins such pieces for the person.

## L32. A shared light is a cheap polish (2026-11-08)
The person called a whole sheet "B plus, just a bit not polished". A one-light pass (`pixlib.polish`: step the left end of each
wide run one shade lighter and the right end one shade darker) is a mechanical way to answer "not polished". It helps masses
(coats, stone) and hurts busy small props (the fax got messier), so apply it per piece and look before keeping it. The grade
decides; the pass is only a tool.

## L33. The edge pass worked: lit left edge, shaded right edge (2026-11-08)
After the one-light pass the person said "polish helped a lot": six people went B+ to A-, and the Faceless Archivist, Unit 05 and
the Director went to A. The mechanism (L32) was one light from the left on every wide mass: the left end of a run one shade
lighter, the right end one shade darker. Do it to every future sprite as the last step, then look; keep it off small busy props
(runs under 3 to 4 px). The three that reached A are the ones with the largest plain masses (a robe, a boxy body, a suit). If a
piece is stuck at A-, the missing thing is a plain mass for the edge pass to work on, or one clear silhouette lever.

## L34. Scale is part of polish; objects need not fit one box (2026-11-08)
Most objects stayed B "due to weird scales". The person: "dont feel need to fit them all same small box". A 16x16 cell is the
unit of the map, not the size of the object. A person is 16x24, so a lamp, a clock, a bookcase, a statue, an obelisk, a phone box
and a wardrobe are TALLER than a person and must be drawn on two cells: `O_NAME` (the cell the map character names) and
`O_NAMEU` (drawn over the cell above it, normally a wall). Before drawing, write the thing's real height in person-heights
and draw to it. The obelisk "should be way taller" is the test: if it is shorter than the person next to it, it is wrong.
Two things get A on the first try: pieces drawn at their natural size (fax, desk) and pieces with one strong shape (brazier).

## L35. Eldritch furniture is ordinary furniture with one wrong detail (2026-11-08)
A bookcase with spines that have eyes, a wardrobe whose doors do not meet, a chair with six unmatched legs, a table laid for a
guest who is covered, a mirror whose room is not this room, a clock showing a time not on the face. Draw the ordinary object
correctly first (so it reads at a glance), then add exactly one wrong detail the player can notice in a second look.

## L36. Depth is a third pass, after silhouette and edge (2026-11-08)
Tall objects stayed B and small furniture went B-: "lacks depth", and "a little polish on edges". The jars were A: they are a stack
of small bright jars on shelves, which have depth built in (each jar is lit on one side, shelves recede). Flat pieces get depth
from the same rule that worked for edges, applied to the whole object: the top face catches light, the underside and the lowest two
rows fall into shadow, the right side turns away (`pixlib.depth_canvas`, run on the finished outlined canvas so the outline is
untouched). Order for every new piece: 1 silhouette at true scale (L34), 2 edge pass (L33), 3 depth pass (L36), then look.
If it still reads flat, add something that overlaps it (a shelf in front of a back wall, an arm across a body): overlap is the cheapest depth.

## L37. Tie the art to the game's own myth, or it is generic (2026-11-09)
Three statues (a jackal head, a veiled mourner, a winged figure) were graded C: "pretty uninspired, tie them back to Anunnaki,
Egypt stuff". They were stone figures with a theme pasted on. The redo took the grammar of the source and used it as the
design: a was-staff and ankh and a collar in lapis and gold (the Weigher); a seated king with a double crown, striped headcloth,
crook and flail; a five-legged winged bull-man guarding a doorway (so it stands from the front and walks from the side); a sage
in a fish-hood with a bucket and falling water; an eagle-headed genie with raised wings and a cone; a scarab pushing the sun; a
winged sun disc. Rule: when a piece is meant to belong to a myth, list the five or six marks that make that myth readable
(headgear, held objects, pose, materials, one odd detail) and draw those, not a figure with a label. Use colour as myth: gold and
lapis for the Registrars' halls, black stone for the weighing. Never name a real deity; the grammar does the work (see gdada-ancient.md).

## L38. A check that agrees with the wrong thing is broken (2026-11-10)
The scale tool said the 48x32 plane was "right" while the person said "way too small". The tool measured height only, and the target
(1.33 persons) was written from the existing art, not from what the thing is. Same failure as colossus L8: a metric that passes what
the person fails is the thing to fix. Rules: (1) the target in a scale table comes from the object's real proportions in the world
(a jet is several persons long), never from the current drawing; (2) measure every dimension that matters (height and width, and a block's
cells together); (3) when the person contradicts a passing check, change the check first, then the art; log it here.

## L39. An edit to shared drawing code can quietly un-grade another piece (2026-11-10)
The person: "make sure sprites don't break others." An audit (`art_guard.mjs` against earlier commits) found one: the green desk, graded A
with the edge pass, had lost that pass when I added the depth pass and excluded it from the depth list; the exclusion also dropped its edge
pass, so the A piece reverted to its unpolished self. Rules: (1) every art run starts with `tools/art_guard.sh` (it must be clean) and
ends with `tools/art_guard.sh --allow <the pieces this run meant to change>`; anything else that changed is a break to fix before showing
the person anything; (2) a piece graded A is frozen: its hash goes in the baseline and only a person's request changes it; (3) when a
shared pass is added (edge, depth, any pixlib function), list which pieces it applies to by name; never "everything except"; (4) after the
person accepts a run, `--update` the baseline.

## L40. Draw a wall of books book by book (2026-11-09)
Shelves drawn as repeating coloured stripes read as a pattern. Drawn book by book (own width, own height, own colour, a lit left edge, a shaded
right edge, a gilt band on some spines, a gap with a leaning book, a brass label plate) the same tall shelf reads as books, and eight variants
(leather, cloth, scrolls, chained grimoires, a ladder, a card catalogue) pack a room. Give a variant its own palette and seed, and keep the
silhouette, so the eye reads the room as one library of many hands.

## L41. One build for everyone; a species is an override, not a new drawing (2026-11-09)
The person graded the bird-headed salesman A and the first ten animal heads built on his recipe B; the first animals, drawn by a separate head-on-a-body renderer, C. Rule: build humans and animals on one round-head, big-eye, clothed build; a species changes the skin triple, the eyes, the snout or beak, the ears or horns and one overlay. See [portrait-craft.md](portrait-craft.md).

## L42. Noise reads as unprofessional; texture must be a clean band (2026-11-09)
Hair-strand dots, cloth-fold hatching and edge dither were graded "too noisy". Rule: portraits use flat fills, one light edge and one shade side, no scattered single pixels; if texture is wanted it is a band or a stroke of a related colour. When a detail pass adds pixels, view the sheet at 1x: if it shimmers, remove it.

## L43. Features that suit a few characters belong on a few (2026-11-09)
Cheeks drawn on every face "don't work for most characters". Rule: expressive extras (blush, freckles, scars, glasses) are per-person flags with low default rates (glasses on about one person in three, blush on a few); check the distribution in the sheet, not only each face.

## L44. Give every character a prop that comes from who they are (2026-11-09)
The secretary and the gatekeepers went from B to A when they were given a thing (a sash, a key ring, a lanyard, a striped headdress). Rule: one signature prop per notable character, taken from their description; vary hat colours per person.

## L45. Show a face where the player will see it (2026-11-09)
Pop-ups were enlarged from 96px to 160px and the grade moved with the size: the person asked for "increasing pixels size, the faces will be popped up for dialogue". Rule: design at the size it is shown, check it in a mock of the real screen (portrait over the dialogue box), and store large art compactly (run-length encoding).

## L46. A pale ellipse under a chin reads as a neck (2026-11-09)
The reptile's pale throat patch was drawn as an oval and the person flagged it: "careful about that oval neck". Rule: mark a throat or jaw with a clean line or a band of scale strokes, not a filled ellipse; check each species' lower face at 4x for anything that reads as a second head or a neck.

## L47. Variants of one species change colour, crest and eyes, not the build (2026-11-09)
Female lizard variants (frilled, gecko, sage) share the lizard build and change the skin triple, the crest or frill, the eye size and lashes. Rule: add a variant key to the look and branch the three or four parts that change; never fork the drawing.

## L48. In a crowd, the head is the character: scale it up, push one lever (2026-11-09)
The first animal-headed map sprites (6-wide box heads on one shared coat) were graded B with the note "scale them slightly up to differentiate so many characters". v2 gives the head 10-12 of the 16 pixels (about 40% of the figure), pushes one species lever to the canvas edge (ears to the top row, horns to the sides, a beak below the chin, a hood wider than the shoulders), shades the head in three tones and gives the eyes a glint, and spreads five body types (coat, robe, suit, apron, shawl) so two of a kind still differ. Rule: when many people share a screen, spend the pixels on the head; bodies vary by type and colour, not detail. Tool: `tools/sprite_sheet.py OUT.png PREFIX` renders a graded sheet at 4x with a floor tile behind.

## L49. Near a muzzle, anything pale and pointed is a tusk (2026-11-09)
Drawing the enraged Minotaur colossus (B_MINOTAUR_RAGE, 64x64), steam was tried five ways: puffs beside the nostrils read as bolts, a jet into puffs as a barbell, white curls as a walrus moustache, puffs below the jaw as tusks, plumes over the head as a second pair of horns. Only a 2 px grey breath at each nostril survived. The same piece first shaded each muscle as its own lit dome, which gave a cow-hide of light patches; raising the highlight threshold so only the top-most planes light, dropping the dark rings between muscles, and adding one rim light along the fur's upper-left silhouette made it one body. Rule: keep pale effects (steam, sparks, breath) away from a face unless they can sit against the background; and on a big figure, light the silhouette, not every muscle.
