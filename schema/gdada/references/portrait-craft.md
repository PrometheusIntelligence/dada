# Portrait craft: dialogue faces (the Maurice recipe)

Faces that pop up over a dialogue box are the most-looked-at art in a talking game. This is what the person graded, and the recipe it produced.
Read it before any portrait or animal-head work; append lessons to [sprite-lessons.md](sprite-lessons.md) (L41 on).

## What was graded
- **A:** Maurice Bell, the bird-headed salesman (the reference for every animal head); the liked lizards; Harold-7, the retired robot; the company secretary; the gatekeepers (after they were given a sash / a key ring); Anubis was asked for by name.
- **B:** the first ten animal heads built on Maurice's recipe (scarab, hippo, owl, cobra, lion, baboon, vulture, bull, frog, hare); the Mayor.
- **C:** the first animal heads drawn by a separate renderer (a head on a body, not Maurice's build); the noisy 80x80 faces; faces where every person had cheeks.
- **Words from the person:** "too generic, too noisy, refine to professional indie dev pixel like Stardew"; "cheeks don't work for most characters, just on a few"; "make the pop-ups bigger".

## The recipe
1. **One build for everyone.** Humans and animals share the same round head, shoulders and clothes; a species is a small set of overrides on that build (skin triple, eyes, snout or beak, ears or horns, one overlay). A separate renderer for animals graded C; the shared build graded A.
2. **Silhouette first.** A round head about two thirds of the frame. Each species gets one big silhouette lever (tall ears, long beak, horns, mane, hood, antennae, great bulging eyes). Check the shape in black before any colour.
3. **Big readable eyes.** White (or the species' ring), a coloured iris, a black pupil, one or two highlight pixels. Species eyes: slit for reptiles and cats, round gold for owls and ibis, horizontal bar for rams and goats, dark compound for beetles.
4. **A colour triple per species and per cloth: (light, mid, shade).** Flat fills, one light edge, one shade side. Strong, simple colours (teal beetle, purple hippo, ginger cat); no noise, no dither, no scatter of lone pixels on skin, hair or cloth. Texture is allowed only as clean bands or strokes.
5. **One signature prop each.** A sash, a key ring, a lanyard, a striped headdress, a stethoscope: a thing taken from the person's description, so two people of one species still differ. Hats are coloured per person (eight hat colours), not one colour per hat type.
6. **Opt-in cheeks.** Blush is a per-person flag, on a few characters only. Default off.
7. **Mood decides the mouth.** The cast file's mood word chooses smile, flat or frown; the mouth opens while text types. Keep the mouth centre at the same pixel in every portrait so the talking overlay works on all of them.
8. **Resolution.** Draw at 48 in a scaled space, store 80x80 (smooth shapes filled natively), shown at 2x (160px) above the box. Store run-length encoded (colour, count) or the source file is half a megabyte.
9. **A black outline, a light edge on the light side, a shade side on the other.** That is the whole style.

## Checks
- Contact sheet of at least 40 faces at 1x and 8 faces at 4x before showing anything. At 1x no face may read as noise; at 4x no stray single pixel may sit alone.
- Every species has a preset (`cast/presets/<species>.json`: render, voice hints, reactions); `npc_check.mjs` fails a species without one.
- Same person, same face: the generator reads the cast file (`look.*`), never a random call.

## Eye lessons (2026-11-10, after "some eyes are too kawaii, asymmetric, wrong size")
- **E1. Draw one eye and mirror it; never draw two.** Two eyes drawn by one loop still drift apart: a highlight placed at `cx-2` on both sides, a polygon not flipped with the side, a 48-space shape scaled to 80 (one eye 12 px wide, the other 11; one pupil 2 px, the other 1). Draw the viewer's-left eye and brow once, record every pixel it touched, and copy each to `axis2 - x` (`faces80.mirrored`). Put a symmetry check in the face tool (`face_preview.py --sym`: the eye-and-brow band mirrored about the centre line, skin mid/shade as one colour, drawn without hair and hat), allow `look.eyes_asym: true` for an eyepatch or a lazy eye, and prove the check fails on the old art before trusting it passes on the new.
- **E2. An adult eye is an almond, not a disc.** The kawaii read came from size and roundness: a 12x12 white disc, an iris filling it, two highlights, no lid. The fix: width about a fifth of the face (4-5 px half-width at a 46-px face, from the face width), three rows of white, a dark upper lid that covers the top of a 3-wide iris, a 1x2 pupil, ONE highlight pixel, a skin-shade lower lid, a lash flick for women. `look.eyes` and mood move the lids (raised, lowered, a fold, a squint, a bag) and the brows (lifted, knitted); the eye's size never changes. Dark eye colours read as dark grey irises, not blue. Glasses are frames over the eye, never white lenses with a second eye painted inside.
- **E3. Whatever sits over or near one eye unbalances the pair: check the face, not just the eye.** The lopsided eyes here were mostly not the eyes: a forehead highlight ellipse that sat on the left eye (a pale or yellow patch around one eye on dark skin), a hairline shadow pass that flooded the face black when hair matched a skin tone (a mask over both eyes), curls and fringe teeth patterned on `x // 5` instead of `|x - centre| // 5`, and an owl whose facial disc was painted over its eyes (no eyes at all). Frogs and crocodiles had two pairs (bulges on top and eyes in the face): a species gets one pair, in its true place (on top for frogs and crocs, with a horizontal bar pupil for frogs).
