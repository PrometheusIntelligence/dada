# Polishing creature models (a Polish run on a Mod's creatures)

Use when the creatures exist and read as good (A minus) but have rough details: faces that look off, a beak or hand that is the wrong shape, a
weapon pointing at the floor. A polish pass changes model details only: not behaviour, not stats, not the page system. Read
[mob-craft.md](mob-craft.md) and [mod-lessons.md](mod-lessons.md) (L22 to L26) first. Measured once: it took one round for the faces of seven
Asgard creatures and one for eight Khemet creatures, because the checks below are specific.

## The order (do not reorder)

1. **Photograph every creature from six angles and look at each face close-up first.** Faces are where "looks off" lives; a silhouette that
   works from ten blocks does not tell you the eyes are hidden. The face camera is part of the tool: give `model_sheet.py` the head's height
   *and how far in front of the feet it is* (a wolf's head is a block ahead, a bird hovers). A close-up that shows a belly, the sky or the
   inside of a skull is a bad camera, not a finding: fix the camera, shoot again.
2. **Run `shadw-mod mob <mod> lint`**: it prints `polish:` notices (a head with no face decals; a head box lying in the face's front plane;
   fewer than 12 parts).
3. **Fix by category**, then shoot only the creatures you touched:
   - **Faces** (`shadwlib.figure.face`): brow (a dark line across the eyes), eyes (a dark socket row over a glowing row, a pupil on the inner
     pixel), nose bridge and nostrils on the centre line, cheek hollows, mouth line and teeth on the last row. Set the ones the creature has;
     an eyeless-looking mask almost always lacks the brow and the socket row. Eyes sit on rows 2 and 3 of a 6-row face, and on the *side*
     faces for birds, snakes, crocodiles and a jackal's long head.
   - **Covers**: a cap, band, hair or brow box may cover the top rows of a face but never the eye rows: raise it, shorten it, or move the eyes.
     A box in the same plane as the face and larger than it hides the face or flickers (z-fighting): move it forward by a pixel or up.
   - **Held items**: a held item's rotation adds to the arm's. Compute the arm's total angle (upper plus forearm) and rotate the item to oppose it
     (a sword up and forward, a club down and forward), then look at the side view.
   - **Silhouettes of a named animal**: a beak is deep at the base and tapers, with a ridge, a hook and a finer lower half; a wolf's legs are about
     1.2 to 1.5 times the body's depth; a crocodile's legs splay out then bend back under it; a cobra's hood sits behind and below its head.
   - **Wraps and bands** go above the eyes and under the mouth, never across them.
4. **Re-measure what the change could touch** (a bigger hitbox, a new part count) and update the site's pictures: the photographs ARE the evidence.

## What not to do

Do not "improve" a creature that reads well by adding parts; a polish pass that grows a model by half again has stopped being polish. Do not
fix a camera problem by editing the model. Do not claim a face is right from the six-angle sheet alone: the close-up is the test.

## Record

Append to the mod's `DESIGN-LOG.md` what the close-ups found, what was fixed, what was not, and keep the version bump (a polish pass is a
major version only when the owner calls it one: the owner called both of these 2.0).
