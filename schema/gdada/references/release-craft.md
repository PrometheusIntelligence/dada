# Release craft: shipping a game that runs inside another operating system

From shipping The Holy Temple (HolyC, TempleOS V5.03, in QEMU) as a zip, a VirtualBox VM, Steam depots and itch.io channels,
2026-11-10..12. The game repo's `design/DISTRIBUTION.md`, `design/SELLING.md`, `design/STEAM-TODO.md` and `design/ITCH.md` are the worked
example; the backend is the TempleOS fork's `Backend/tools/gamec.mjs` (`dist`, `play`, `steam`) and `Backend/launcher/launcher.c`.
HolyC-specific facts are numbered in [holyc-lessons.md](holyc-lessons.md) (H13-H23); this page is the method.

## The forms, in the order to build them

| Form | Who it is for | What is in it | Proven by |
|---|---|---|---|
| Game disk + installer | people who already run the OS | the game tree on a small FAT32 image, `INSTALL.HC` / `Uninstal.HC` | install, play, uninstall in the real OS |
| Bundle (zip) | everyone with QEMU | an **installed** OS disk with the game, autostart, `run.sh` / `run.bat`, README, licence texts, SHA256SUMS | `gamec play`: boot with nothing typed to the title, save, power off, boot, continue |
| VirtualBox | people with VirtualBox | `setup-virtualbox.*`: `VBoxManage convertfromraw` + a VM made to the OS's needs (IDE PIIX4, BIOS, I/O APIC) | the converted VDI is byte-identical to the tested image; the VM settings read back |
| Store builds (Steam, itch) | buyers | per-OS folders: launcher, read-only game disk, empty save disk, the emulator, store manifests | the Linux build played headless through its own launcher, twice |

## Rules

- **R-ship-1. Ship an installed disk, not a live CD plus a game.** A live CD cannot start a game by itself and cannot read data discs in
  every OS (H8, H14). Install once with the OS's own installer in QEMU (scripted through the monitor), cache the result, copy the game in
  with mtools, and replace the boot loader's menu with a 120-byte MBR that boots partition 1 so the player types nothing.
- **R-ship-2. Do the first boot at build time.** Anything an OS does once after install (TempleOS unpacks its dictionary under a box that
  covers the game, H22) is done by the build and cached (`-booted.img`). A read-only disk would otherwise do it on every start.
- **R-ship-3. Saves live outside what the store owns.** A store rewrites the install folder on every update and "verify". So the game disk is
  booted read-only (`snapshot=on`) and saves go on a second small disk in the player's own folder (`%APPDATA%\<Game>`,
  `~/.local/share/<Game>`), made once from `saves-empty.img`. The game reads its save folder from one overridable define (`HT_DIR`), and the
  store build's boot file sets it after mounting the save disk (H23). Mount only that disk; mount after the OS's own start-up scan.
- **R-ship-4. Test the player's path, headless, end to end.** A play script (`waitscreen`, `key`, `type`, `shot`, `poweroff`, `boot`,
  `expect-file`) drives the real build through its own launcher with a fresh data folder: title with nothing typed, new game, save at a
  terminal, power off without shutdown, boot, continue, quit to the shell. Then assert the game disk is unchanged. Run it twice: a boot race
  can pass once by luck (H23).
- **R-ship-5. Launchers are small, honest programs.** Windows: a C launcher built with mingw-w64 (`-mwindows`, no console), which makes the
  save disk, finds the emulator (bundled, then the default install folder, then an environment variable), starts it with `CreateProcess`,
  logs the command line to the data folder and shows a message box naming the fix when something is missing. Linux/macOS: a POSIX shell
  script that picks KVM/TCG, the audio and display backends the emulator actually has (`-audiodev help`, `-display help`), and the macOS
  ones (cocoa, coreaudio). Double every comma in a `-drive file=` path. Test the Windows launcher under Wine with a stand-in emulator that
  writes its command line to a file.
- **R-ship-6. Bundle the emulator portably, with its licence.** Linux: copy the binary, every `ldd` library except the C library and loader,
  the needed modules (`QEMU_MODULE_DIR`) and firmware (`-L`), plus a `QEMU-SOURCE.txt` naming the exact source package and a written offer
  (GPL-2.0). Windows: fetch a pinned build and its source tarball on a machine with internet (`fetch-qemu-win.ps1`). Never bundle an
  emulator you have not run.
- **R-ship-7. One command builds every form and uploads nothing** (`tools/release.sh`): host checks, bundle, store depots, store channels,
  store art. Uploading is the owner's act (an API key, a store account), done later and on purpose. Write the owner's checklist as a document
  of their steps only (`STEAM-TODO.md`, `ITCH.md`), with what is already done in a table beside it.
- **R-ship-8. Licence before store.** Decide what is yours to sell (the game), what is not (the OS, the emulator) and say so in `LICENSE.txt`
  and `NOTICE`. The Holy Temple: a normal game EULA; TempleOS ships as itself, public domain, credited to Terry A. Davis on the title screen
  and in `TEMPLEOS.txt`; QEMU unmodified under GPL-2.0 with source. Never use the OS author's name or likeness to sell.
- **R-ship-9. Store art from the real build.** Capsules and screenshots are generated (`tools/steam_art.py`) from real runtime screenshots and
  the game's own font at every size the store asks for; regenerate them when the screen changes (a stray icon fixed in the game is still in
  old screenshots).
- **R-ship-10. Precompiling is optional, never assumed.** Compile-on-launch (47 s without acceleration, seconds with it) is the default and
  part of the charm. An ahead-of-time build needs every symbol the game uses from the OS declared (H17-H21) and must pass the same tests;
  until it does, it is an open item, not a feature.

## What a store needs (2026, check before paying)

- **Steam:** Steamworks account (identity, bank, tax form), US$100 Direct fee per game (recouped at US$1,000), a 21-day wait after paying,
  a "Coming soon" page for at least 2 weeks, store page and build reviews, depots per OS uploaded with SteamCMD/SteamPipe, launch options,
  Steam Input layout for the Deck, content survey.
- **itch.io:** a page made in the browser (no API), payout and tax settings for a paid game, builds pushed with butler per channel
  (`linux`, `windows-osx`), a `.itch.toml` per channel so the itch app's Launch runs the right file (`butler validate`).

## Stop test for a release run

- [ ] Every form built by one command; SHA256SUMS written
- [ ] The bundle and the store build played headless end to end (twice for anything with a boot race); game disk unchanged
- [ ] Launchers run (Wine for Windows); missing-emulator path shows the fix
- [ ] Licence, notice and the OS's credit in the build and on the title screen
- [ ] Owner checklist written; nothing uploaded without the owner
