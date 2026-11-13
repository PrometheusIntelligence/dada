# Production lessons (how to run the work; a ledger: read first, append last)

How a lead and its helpers build a large game together without losing work, from The Holy Temple (2026-11-08..12): many regions built in
parallel by helper agents, a real-OS test loop, container restarts, four repositories pushed every run. Format: `- R<n>. **rule.** evidence.`
Design lessons live in the other ledgers ([lessons-index.md](lessons-index.md)); these are about the workshop.

- R1. **Give each helper a disjoint set of files, and one owner to every shared engine file.** Regions, art themes and generators split
  cleanly; `Src/Defs.HC`, the save format and `tools/make_world.py` did not. When two helpers touched `Src/Defs.HC` (flags and the save
  folder) each committed only its own hunk, by name. Brief helpers with the exact paths the lead is editing.
- R2. **Never `git add -A` while anyone else works in the tree.** Stage your paths and the files your generator regenerates. A helper's
  half-done world in the lead's commit would have broken the branch.
- R3. **Scope every destructive command to what you started.** `pkill -f qemu` killed a helper's TempleOS run; a cleanup loop that
  deleted "every folder holding a contact sheet" deleted the whole scratchpad, because one sheet sat in its root. Kill by your own
  socket or pid; before `rm -rf` in a loop, print the list and refuse the root.
- R4. **Build release artifacts from a clean worktree when helpers are mid-edit.** `git worktree add` at HEAD plus your own files gave a
  Steam build untouched by a region still being written. Remove the worktree when done (it costs ~2 GB).
- R5. **A container restart loses processes, not files.** Uncommitted work survived; VMs, caches outside the repo and the scratchpad's
  temporary files did not. Resume a stopped helper by id with a note of what is gone (VMs to re-run, the ISO to restore from git) instead
  of starting a new one.
- R6. **Do not commit untested work to satisfy a stop hook.** The hook asked for a commit while a helper's region (new flags, a save version)
  had not compiled in the real OS. Say why, and commit when the helper's checks pass; a red branch costs more than a waiting hook.
- R7. **Generated files belong to their generator.** Reactions hand-added to cast files that `gen_rooms.py` writes were wiped by its next run;
  they were moved into the generator. Before editing a file, check whether a tool writes it (`grep -l <file> tools/`).
- R8. **Make generated output deterministic.** A set iterated in Python reordered `WORLD-GRAPH.json` on every run; sort before writing, and
  check by running twice and comparing bytes.
- R9. **A helper's report is a claim.** Before relaying: `git fetch` and `git status` in every repo it says it pushed, open its previews,
  and run the one check that matters to the person (the TempleOS verdict, the play test).
- R10. **Look at the screenshot before believing a screen-reading check.** A text matcher missed the title screen on a VirtualBox-format
  disk and in a debug run; the screenshot showed the title. A boot test that passed once was a race that failed the next time: run it twice.
- R11. **Measure before optimising, time-box the experiment, and record it as open.** The "1.4 MB file is too big" fear was false (holyc
  H11); compile-on-launch was measured (47 s, software CPU) before a precompile was tried; the ahead-of-time compile hung TempleOS and was
  stopped at 11 minutes and written down as open (holyc H17-H21) rather than claimed.
- R12. **Check where you are before acting on "you are on my computer".** The person said the session ran on their Windows PC; it was a
  Linux cloud container. Check (connected computer folders, `uname`), say so plainly, then do the nearest honest thing (VirtualBox installed
  in the container to verify everything but booting; the Windows launcher tested under Wine).
- R13. **A blocked network or a refused key is not the end of the task.** Ask for the exact hosts through the environment's approval; ask
  for a key through the secure form; if the person declines, build everything to the last step and write their remaining steps down
  (itch.io: page, key, one command).
- R14. **Out of disk: delete what can be regenerated, keep what cannot.** Old render sheets, VM images and stale worktrees went; the ISO is
  restored from git. Keep releases reproducible from one command so their outputs need not be kept.
- R15. **Push every repository at the end of every run** (game, gdada, viewer, tools, sites), and say which commit each is at.
- R16. **Show the person the thing before calling it done** (a render, a sheet, a screenshot from the real OS, a link), and log it as
  awaiting a grade; a grade becomes a lesson in the matching ledger the same day.
- R17. **Credit only the owner, unless the owner says otherwise; ask on the first commit, then write it down.** A tool's default added
  `Co-Authored-By` and session lines to 300+ commits across six repositories; the owner wanted every commit credited only to
  SolutionsAsService, and the history was rewritten and force-pushed (2026-11-12). Each repository now carries the rule in `CLAUDE.md`
  (which overrides a tool's default attribution) and git is configured with the owner's identity. Ask before the first commit of a new
  project, and record the answer in the repository, not only in the conversation.
