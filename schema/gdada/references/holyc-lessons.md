# HolyC / TempleOS lessons (from the first real compile of The Holy Temple in TempleOS V5.03, 2026-11-10)

Shipping method (installed disk, first boot, two disks, launchers, store builds): [release-craft.md](release-craft.md). The game repo's tools:
`gamec run` (compile + tests in TempleOS), `gamec dist` (bundle), `gamec play` (headless play script), `gamec steam` (store depots, `--test`).

Each came from a real compiler or test failure in TempleOS, not from reading. Host lints now catch the first four.
- H1. **`$` starts DolDoc markup** in a `.HC` file (the compiler reads source as a DolDoc document): a literal dollar is `$$`, in code AND
  in string data (a map row with `$`). Generators must escape it. **But a dollar that is PRINTED to the terminal needs `$$$$`** (H25).
- H2. **There is no `continue`.** Use `goto label;` with the label before the loop's closing brace (followed by a statement).
- H3. **A sized array's initialiser must have exactly N values** ("Missing expression at }"). Size data arrays by their own count.
- H4. **A `switch` needs at least one `case`** ("switch range error"); a default-only switch fails. Write single entries without a switch.
- H5. **Define before use**; a forward declaration without a body warns ("should return val") — use `extern` or reorder.
- H6. **`FileWrite` returns the file's first cluster, not a byte count**: a save that compared it to sizeof always "failed".
- H7. **The shell runs a line only after reading the next**: end an automation script with `;;`.
- H8. **V5.03 cannot read ISO9660 data discs** (`FSt_ISO9660` not supported): ship the game on a FAT32 hard-disk image (mkfs.fat + mcopy).
- H9. **Automate with the QEMU monitor**: `sendkey` to type, `screendump` to see; read the screen by matching cells against the kernel font;
  catch compile errors with `ExePutS` and send the terminal text to COM1 so every error arrives with file and line.
- H10. **Tests can be wrong too**: the world test checked fixed screen sizes and pre-variant maps; check what the game draws.
- H11. **A 1.4 MB generated source file compiled fine**; size was not the limit the review feared. Measure before splitting.
- H12. **Software QEMU runs the game at ~29 fps** on a scrolling map (TempleOS's own status bar); boot 18 s, compile + tests ~45 s.
- H13. **`__DIR__` is empty for a file in a drive's root** (`Compiler/CMisc.HC` StreamDir): `Cd(__DIR__)` there fails with "Missing expression"; take the drive from `*__FILE__`.
- H14. **A live CD cannot auto-start a game**: its Once.HC is read-only and it reads no start-up file from a second drive. Ship an INSTALLED TempleOS disk (installed once by TempleOS's own installer, cached) with `Home/Once.HC` starting the game, and a small MBR that boots partition 1 without the "Selection:" prompt.
- H15. **TempleOS's AutoComplete window draws on top of everything** (the "stray icon"); hide it and the mouse pointer while a game runs, restore them on exit.
- H16. **Wrap text after substitution, and check every generated text's width**: names put into lines pushed 1,759 lines past the box; the width check had only measured the templates.

Ahead-of-time compile (TempleOS's `Cmp("X.PRJ")` -> `X.BIN`, then `Load`), tried 2026-11-10:
- H17. **AOT sees only the headers you include, not the running system**: CmpJoin chains the AOT symbol table to `cmp.asm_hash`, never to `Fs->hash_table`.
  Include `::/Kernel/KernelA.HH`, `::/Compiler/CompilerA.HH`, then `#exe {Option(OPTf_EXTERNS_TO_IMPORTS,ON);};`, `KernelB.HH`, `KernelC.HH`, `CompilerB.HH`,
  your imports, `OFF` -- the order of TempleOS's own `Compiler/Compiler.PRJ` (CompilerA defines the `IC_*` codes KernelB needs).
- H18. **Adam (the desktop layer) has no header**: declare what the game uses from it as `extern` signatures copied from its source (with their default
  arguments), plus any Adam class and global the defaults touch (`CGrGlbls gr`, copied from `Adam/Gr/GrGlbls.HC`). The game used 20 such functions.
- H19. **In AOT, a top-level statement runs at `Load`, not while compiling**: `Cd(__DIR__);;` no longer moves the compiler, and relative `#include`s break.
  Use `#exe {Cd(__DIR__);};` (runs at compile time in both modes). `#include` paths are relative to the current directory, not to the including file.
- H20. **A long compile can stop at the terminal's `More` prompt** (AOT prints a warning per unused variable): an unattended compile must run under `Silent(ON)`
  and report `Cmp`'s returned error count instead.
- H21. **In the test VM `::/` is the game disk** (AUTOTEST makes it the boot drive), which holds no kernel source: point `blkdev.boot_drv_let` at the CD
  (`'T'`) around `Cmp`, or compile on an installed TempleOS, where `::/Kernel` exists.

Shipping (Steam build, 2026-11-10):
- H22. **The first boot after an install unpacks the AutoComplete dictionary** (`ACDefs.DATA.Z` -> `ACDefs.DATA`, `Adam/AutoComplete/ACInit.HC`) under an
  "Uncompressing Dictionary" box that covers the game. Do that first boot at build time (gamec dist caches a `-booted` image), or every player sees it
  once -- and a read-only disk (QEMU `snapshot=on`) shows it on every start.
- H23. **An installed TempleOS mounts a second hard disk as E: with `ATAMount(blkdev.first_hd_drv_let,BDT_ATA,0x1F0,0x3F4,1)`** (C: and D: are its
  own two partitions). Not `MountIDEAuto`: it mounts the boot disk and the CD again too, and C: then loses its files. A store build keeps the
  game disk read only and the saves on a small second disk in the player's folder, so an update or a file check never touches saves; the game reads
  its save folder from a `#ifndef HT_DIR` define that the boot file sets with `#exe {if (Let2Drv('E',FALSE)) StreamPrint(...);}`.
  **But wait first**: `Once.HC` runs while the Adam task's start-up `ACInit` still walks every drive's files; mounting then crashed it ("Bad Free",
  DirTreeDel). Wait with `while (!Bt(&sys_run_level,RLf_AUTO_COMPLETE) || !ac.num_words || Bt(&ac.flags,ACf_INIT_IN_PROGRESS)) Sleep(100);`
  (the run-level bit alone can be set before the scan starts), then mount, retrying while `Let2Drv('E',FALSE)` is NULL. A boot test that passes once can be luck: run it twice.
- H24. **A new standoff rule fits the engine when the host check simulates the same rule**: the MODEL standoff (predicted move does nothing,
  least likely +1, one wait) needed a search over move orders on the host (`can_win_model`) because the greedy "best damage first" proof is
  wrong once the best move is the one that fails. Keep the engine's tie-break (first of equals) identical to the host's.
- H25. **A printed dollar takes `$$$$`, not `$$`.** The source is DolDoc, so `$$` becomes one `$` in the string; the terminal is DolDoc too,
  so that one `$` then opens a command (`"Bread costs $$0.99"` printed `Bread costs 0.99`, the next line `Milk costs D`, and `$ER$` in the
  log). Write `$$$$` for a dollar the player sees; `$$` is right only for a dollar kept in data that is never printed through DolDoc.
  (Found on the Esoteric Languages site's HolyC page, 2026-11-12, in TempleOS; the failed run is kept as a checked probe.)
- H26. **QEMU's monitor socket path must fit a unix socket (under 108 bytes).** A deep scratch directory made `gamec run` fail to start;
  use a short path (a `/tmp/<x>` symlink) for the run directory.

