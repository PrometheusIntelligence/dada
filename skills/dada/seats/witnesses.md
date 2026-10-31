# Witnesses

A witness testifies to facts; it does not judge the work, does not vote PASS or OBJECT, and does not count toward
a mode's composition rule or the printed seat figures. Witnesses exist because some facts only their owner holds
(dada-lessons 49: on the Kuddo plan the Fidelity Engine changed mid-run, and only a message from the session building
it brought the fact in).

## Content owner (fact witness)

- **Who:** the person or session that owns each system, product or dataset the artifact describes. On a project site,
  one witness per system named on it.
- **When:** before R1, and again before Step 2g on any figure the witness owns.
- **What it files:** `<panel_dir>/witness-<system>.md`, a list of facts with their source and date: what is built,
  what is live, what is planned, each count the artifact prints about that system, and anything that changed since the
  evidence file was written. "Unknown" is a valid answer and stays unknown; the conductor never fills it.
- **How the panel uses it:** the evidence file links the witness file; Cairo reads it before checking claims; a claim
  the witness contradicts is a [claim] finding against the artifact, not a disagreement between critics.
- **Prompt (about 150 words):**

```text
You are the content-owner witness for {system} on a DADA panel, round {round}. You do not judge the design and
you do not vote. Read {artifact} and list every statement it makes about {system}. For each, say: true as of
{date} (with the source: file:line, commit, dashboard, or "owner's word"), false (with the true value), or unknown.
Then list anything about {system} that changed since {evidence} was written. Never guess: "unknown" is an answer.
Write the list to {panel_dir}/witness-{system}.md as your last action, then return the same text.
```
