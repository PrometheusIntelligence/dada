# VISION.md template

One file per game, beside the game, written in the person's own words. The run reads it first and is judged against it.
Keep it short. Quote the person verbatim (mask only what must not be published) and tag each line `owner` (the person
said it) or `inferred` (the agent concluded it, to be confirmed).

```markdown
# Vision: <game name>

## Pitch
One or two sentences, the person's words first. `owner`

## What the player feels
The feeling over the first minute and the first hour. `owner` / `inferred`

## Pillars
3 to 5 short statements the game keeps when anything else is cut.

## Verbs
What the player and the characters do. Each verb needs a decision or a pleasure.

## World and look
Camera and projection, setting, characters, palette, tone.

## Must-haves
Numbered. Each one is checkable in the running game and carries its source quote or date.
1. ... (`owner`, "quote", date)

## Will not do
Things the person ruled out or the scope excludes.

## Success tests
Measurable checks (a bot run, a time, a size) that show the Must-haves hold.

## Platform and stack
Engine, language, hosting, performance constraints.

## Open questions
Each with an owner and a decide-by.

## Change log
Newest last. Date, the person's words verbatim, and what it added or changed above.
```

Rules:
- Direction from the person goes into the Change log and the Must-haves **before** any planning or building.
- A Must-have is only removed by the person. The agent may mark one `blocked` with a reason.
- The final reply of a run lists every Must-have as built and checked, or as an open item.
