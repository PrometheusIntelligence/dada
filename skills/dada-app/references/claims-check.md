# Claims check after every edit (Step 2g for an app)

1. List every number, ratio, count and "held by" statement in `docs/`, `README.md`, the legend, the footer and the
   tooltips.
2. Next to each, write the command that reproduces it (`floor_probe.cjs`, `npm test`, a DOM read) and its value now.
3. After **any** edit that could move a figure (a layout change, a new element, a font change), re-run the commands
   and correct the prose in the same commit. In the OperatorOS run the first-screen numbers moved three times after the
   docs were written (432/678, then 538/783, then 543/788).
4. Print the zero with its denominator ("0 of 84 marks under 24px"); say what was not run.
5. A statement the artifact cannot back is deleted, not softened.
