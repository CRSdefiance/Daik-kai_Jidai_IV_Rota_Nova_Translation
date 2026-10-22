# Genuine cartridge-save Continue V314

V309 remains unchanged, SHA256
`b099a1016d08870adbdbff8693be9b5fba2f0fa611c82358bafcd507199d5289`.
This checkpoint makes longer ordinary gameplay tests practical by verifying
persistent cartridge saves and loading through the game's Continue menu.

## Correction to previous persistence claims

The prior assertion that the headless runs produced no DSV files was incorrect.
A full workspace inventory finds155 battery files in the headless test tree.
Most are blank/new-cartridge data; the V306/V307 ordinary in-game save contains
actual saved data. The file header is `DK4R`, not the assumed contiguous ASCII
`DK4R6`. The latter search missed a valid save.

The two ordinary Gallery runs produced the same262,266-byte DSV:
SHA256 `58d7c0d4cc43a43579cc218ef2a391a4a71fec83e77803924189b6d023ca8af0`.
Its content differs from a blank cartridge file at42,837 byte positions.
The V307 capture report records its normal save operation during a fresh
31,200-frame run without a loaded state or gameplay-memory fixture.

The [DeSmuME core documentation](https://docs.libretro.com/library/desmume/)
describes `.dsv` files as cartridge battery saves in the frontend's save directory.
The core already persists them directly; adding a save-RAM memory API is unnecessary.

## Current cold-boot load

`headless_desmume_v193.py --battery-save <source.dsv>` copies the unmodified file
into a fresh isolated save directory under the current ROM's filename. It checks
the DSV footer/size, refuses an existing destination and records source, hash,
size and destination. Default runs retain their previous behavior.

The source file is never overwritten. This loads cartridge data through the
core's normal filesystem path before boot; no serialized emulator state,
ROM unlock patch or live gameplay RAM injection is used.

The V309 run reaches:

| Frame | Actual observed screen |
|---:|---|
|2000|Title with Continue enabled|
|2400|Rafael's saved slot, Lisbon Docked, five unused slots|
|2800|Load this data? confirmation|
|3200|Loaded Lisbon town, Castor Co., observed date1M11D|

Every capture/report/ROM/source-save hash is checked. The loaded town confirms
that the file is usable game progress, rather than relying on header inspection.
The source save's hash remains unchanged after the test.

The compact date/company HUD was initially tested against a full-size dialogue
font mask. That assumption did not match the HUD renderer. No glyph-formatting
approval is inferred from that failed check; these fields are recorded as
visually observed. This checkpoint verifies save loading, not a new HUD font fix.

## Continuing the graphics goal

Ordinary acquisition runs can now save through the in-game menu, exit, and
cold-boot from an isolated copy through Continue. Preserve a source save and its
capture/input provenance at each useful checkpoint. This removes the need to
restart every long acquisition attempt from New Game.

This particular save does not contain an occupied weapon/armor or legitimate
hidden Gallery unlock. Those checks remain open, as do all18 plaque/hint entries
and broader raw/native/GPU contexts. Low resolution Online images remain exempt.
V309 remains the registered combined ROM with its unchanged exact patch; the
full graphics goal remains active.

Evidence: `work/analysis/battery_continue_v314/proof.json`,
`work/emulation_v193/battery_continue_v314/capture_report.json`,
and the source file under `work/emulation_v193/gallery_menu_v307/saves/`.
Updated scripts pass Ruff. The emulator process exited successfully.
