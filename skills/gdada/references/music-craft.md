# Music craft (one-voice 8-bit: PC speaker, chip square waves)

The person's grades on The Holy Temple soundtrack (2026-11-10): "very good", but "too short"; sand A ("needs to be drawn out");
labyrinth A. Every rule below comes from that run; add to it the same way (evidence, rule).

## The medium
- ONE square-wave voice. Chords are arpeggios: the voice cycles the chord's notes every ~25 ms (the classic 8-bit shimmer). Two or three
  notes read as a chord; four start to blur; never more than four.
- Useful range on a PC speaker: about 80 Hz to 2 kHz (E2 to C7). Below A2 it buzzes rather than sings; above C7 it hurts.
- Silence is an instrument: every tune loops, then rests (`gap`). Long gaps in safe places (town 10 s), short in tense ones (a standoff 0.4 s).
- Write tunes as text (one token per step: `C5`, `-` hold, `.` rest, `[C4E4G4]` arpeggio), compile them into the game, and render a
  host preview (WAV, and a browser listener) so the person can grade without the target machine.

## Form (from "too short")
- M1. **A loop under ~8 s feels like a jingle, not a place.** Aim for 10-20 s per loop (12-24 bars of 4 steps), plus the gap.
- M2. **A-B-A'.** A states the motif (keep it if it was graded), B answers it (a fifth away, the relative key, or the motif's inversion),
  A' returns it changed (an ornament, an octave, a wrong note in the last bar only). Repetition is what makes a motif memorable; variation
  is what makes it bearable on the fortieth loop.
- M3. **Draw out a graded motif by answering it, not padding it** (sand: motif, its answer a fifth lower, a long rising middle in held notes,
  the motif ornamented). Held notes (`-`) are the cheapest way to add length with weight.
- M4. **A loop must end where it can begin again**: the last bar resolves to the tonic (or is a rest), so the seam is invisible.

## Character (from what was graded A)
- M5. **One idea per region, in the region's body**: the labyrinth is hooves on stone (a low ostinato with a gap in it: `D3 D3 . D3`); the
  town is a radio jingle from 1998; the offices are lift music in major sevenths, slightly too slow; the Backrooms are a hum a semitone apart.
- M6. **Wrongness is one note, once.** The town's last bar has a flat seventh where a leading note should be, once per loop, never in A.
- M7. **Modes do the atmosphere**: Dorian for folk (Midsummer), Phrygian and harmonic minor for the ancient and the sand, the whole-tone scale
  for the eldritch (no tonic to rest on), a waltz whose third goes flat for dreams.

## Checks (scripts/music_check.py)
Length per loop, form (distinct bars: a loop that is one bar repeated fails), range, chord size, the last bar resolving or resting, and
that every graded tune still contains its graded motif (`keep` list).

## From expanding (v1 "too short" -> v2 "beautiful, great work", graded A)
- M8. **Extend by section, never by stretching.** Doubling the step length or repeating the loop made nothing better; adding an answering B
  section and a changed A' did. Every v2 tune kept its v1 bars verbatim as A, so the graded identity survived the expansion.
- M9. **Lock graded motifs before editing** (`music_check.py --keep`), then extend around them; the check is what lets an agent lengthen a
  tune the person loved without "improving" the part they loved.
- M10. **Let the checker set the floor, the ear set the ceiling**: the length rule caught two loops still under 8 s (archive, island); a
  slower step fixed one, a fourth phrase the other. Tunes the person graded A were extended most (sand to 18 s), because a good motif
  carries length; a weak one is better short.
- M11. **Give the person something to hear without the target machine** (WAV renders, a browser listener in its own repo): grading
  happened in minutes once the music could be played in a browser.
