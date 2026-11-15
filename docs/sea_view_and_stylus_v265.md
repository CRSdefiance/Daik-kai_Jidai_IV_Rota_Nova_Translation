# Ordinary stylus and Sea View source evidence V265

V265 is a gameplay/research checkpoint. V263 remains the current registered ROM
and patch. The preceding turn classified generic archive consumers; this turn
adds ordinary DS stylus input and actual resident graphics identity. No ROM,
artwork, translation batch, release profile or canonical baseline changed.

## Normal input capability and exact replay

The old headless frontend supplied joypad input but returned zero for all pointer
requests. Optional `--touchscreen` now enables the pinned core's normal pointer
path. Native bottom-screen pixel centers are normalized into its256x384 layout;
only libretro input callbacks are used. No inventory or emulator RAM is injected.
Default runs retain their prior mouse/input mode. Touch events store exact bottom
coordinates, duration and start frame in the same report as controller events.

The mapping is read from the official pinned DeSmuME source at commit95b4d79,
`desmume/src/frontend/libretro/libretro.cpp`. Source URL and whole-file hash are
saved in `stylus_source_provenance.json`; pointer normalization is not guessed.

A fresh33000-frame Lil boot is replayed from ordinary recorded inputs, then
continued to34000 frames with stylus enabled. All85 corresponding whole cold-boot
framebuffers before touch are exact to the first run. Tap102,100 selects Deck View;
tap88,64 activates it. Neither event carries a button press. The resulting real
Deck View has all2299 help glyph pixels exact, including first/final letters.
This verifies the actual input effect and retained V263 help formatting.

Both processes ended normally with final reports and full actual input schedules.
The final native-state export is read-only: serialized RAM equals the direct
same-frame export and remains unchanged afterwards. No state is loaded. This is
a targeted automated emulator test, not a full route/hardware test.

## Actual loaded graphics: seaarea, not seamap

The same-frame RAM contains one complete exact copy of each current-ROM file:

| Resource | Actual header address | Complete bytes |
|---|---|---:|
|/_pxl/__frame.pxl|02314000|35444|
|/_pxl/__marker.pxl|0236A9E0|35444|
|/_pxl/chara00.pxl|02323C80|133652|
|/_pxl/seaarea.pxl|023446B0|156436|

Every header, palette and pixel byte is included. The actual registered seaarea
owner0231336C points to `_pxl/seaarea.pxl`; its fields are preserved in the proof.
The seaarea atlas is unchanged from clean,244x1280 with eight244x160 pages.

All64 page/palette alternatives were compared against every39040 pixels of the
actual upper map rectangle[6,16,250,176]. Page0 supplies37490 matching background
pixels. Its eight palettes are identical and tie; screenshot colors alone cannot
establish the selected bank. The1550 unmatched composite pixels are counted and
retained as unresolved. Routes, cities and ships are visible overlays, but their
complete independent reconstruction is not claimed here. Native parent draw/palette
dispatch and the entire composited map remain pending.

The previously researched `seamap.pxl` is a distinct sepia resource. A zero-match
comparison of its stored palettes and a weaker inferred recoloring hypothesis
were rejected. The actual full `seaarea.pxl` resident identity supplies the stronger
source evidence; do not change the seamap/raw304x200 interpretations to force a
match or equate these separate resources. Retain original unlabeled cartographic
art. Text captions and symbols remain separate localization consumers.

## Equipment and formatting gates remain open

The trip did not obtain or equip an item. Supplies ran out before a purchase.
A DS guide suggested Gallic Wars in London, but that stock was not reached or
verified in this ROM. Stylus support now permits ordinary steering and interface
selection in further runs. Replay must trim the exploration segment after the
sailing tutorial and supply a direct route, rather than repeat the supply failure.
The normal equipped-save request is still pending.

The scurvy alert at frame31200 visibly splits `have` across rows. No missing letter
is inferred, but that common-message layout needs source/consumer verification.
This is recorded as a formatting issue, not silently treated as complete English
layout. The later Food has run out alert is captured separately.

All18 plaque/hint entries and Armor/Weapon variants remain incomplete. Four Online
body sources, raw comic display, other native/contextual displays and the full
final graphics/ROM/patch audit remain open. Revisit older record-based checks at
actual goal completion.

Proof: `work/analysis/equipment_gameplay_v265/saved_live_proof.json`.
Verifier: `scripts/verify_sea_view_and_stylus_v265.py` (Ruff passing).
Captures: `work/emulation_v193/equipment_gameplay_v265` and `equipment_touch_v265`.
