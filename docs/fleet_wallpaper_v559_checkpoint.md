# V559 fleet wallpaper and ordinary Swap Ships consumer

The previous goal turn integrated all five original name-plaque gradients and
their embedded copy. This turn audits the separate patterned fleet-list material.
No artwork, translation, ROM, patch or release registry changes are needed.

## Complete source-material review

The fleet labels use patterned brown wallpaper, not gold wood. Original untouched
left-half samples repeat exactly every32 pixels:4320 independently checked control
pairs. Every pixel in all five50x16 label regions has two independently selected
unlettered source donors,4000 agreeing pairs. All current non-English pixels match
that source repeat, with palette/header/dimensions and unowned pixels exact to clean.
The removed Japanese lettering and shadows do not leave the coarse-fill defect
found in other families. No gold donor is substituted.

All five labels independently match the complete6x11 native font at their existing
positions: Flagship96 ink pixels, Ship2 67, Ship3 68, Ship4 70 and Ship5 70. Every
first/final glyph is included. The wording is natural and faithful: 旗艦 is Flagship;
2番艦 through5番艦 are Ship2 through Ship5. Existing visible labels include spaces.

## Correct ordinary consumer

Common Info > Dock Ships opens a different information screen and receives no
fleet-wallpaper display credit. Code tracing identifies dock.pxl owner022A44B8 in
setup020A9498 and direct callers020A5190/020A5C28/020A66D0. Those are source routing
leads, not a claim that every caller executed during the test.

The actual wallpaper appears through **Shipyard > Dock > Swap Ships**. Ordinary
navigation from the unchanged copied Syracuse gameplay save reaches it in V558.
No cheat, synthetic inventory/location/condition, or savestate is used. The active
flagship's runtime card covers the baked Flagship caption. This is observed
occlusion, not a missing leading character. Ship2–Ship5 remain fully visible.

At frames6700/6900/7100, native view0218FB90 binds original owner022A44B8, source0,0,
bank0 and extent256x192. Complete original resolver020D4170 returns the actual
resident whole dock.pxl at0233E230, byte-exact to the candidate, without SDK bridge
or supplied resource binding. Header/palette and source pixels are all included.
Return and saved-register/stack checks pass. Resident views are independently
rechecked at each frame.

## Actual pixel scope and preserved negative result

Two complete unobscured source rectangles match37120 pixels per frame:
[0,44,256,174] and [128,14,256,44], at stacked-screen origin0,192. Across three
frames this is111360 actual source pixels, including all12 complete appearances
of the four empty-slot labels. The source palette matches the actual scene.

An initial larger comparison beginning at row42 fails256 pixels: the occupied
flagship card's bottom border covers source rows42/43 in the left128 columns.
That failed33792-pixel test is retained as a failure. The credited rectangles
are explicitly outside the card; no full-screen composition or visible Flagship
caption is claimed. Header text, the occupied card and bottom controls are other
native UI elements and are not silently counted as raw wallpaper.

Back returns to the shipyard Dock submenu without swapping any ship or saving.
The interactive run finishes frame7300 exit0. Its original copied-save source
remains SHA256958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb.
Earlier navigation through Deck View and Assign Sailors is retained in the input
schedule; those screens do not receive dock.pxl credit. The separate Common Dock
Ships information run is also retained as a diagnostic.

## Artifacts and remaining scope

- `scripts/verify_fleet_wallpaper_v559.py`; Ruff and complete verifier pass.
- `work/analysis/fleet_wallpaper_v559/source_and_native_proof.json`.
- `all_five_source_current.png`, ordinary navigation schedules and RAM snapshots.
- `E:/Rota Nova translations/Generated/work/emulation_v193/fleet_wallpaper_v559_navigation`.
- Reviewed ordinary screenshot/provenance under E Screenshots/Guide candidates.

Other fleet loadouts/caller contexts and occupied-card composition remain outside
this bounded proof. All22 historical requirements retain their exact scope and
all18 original plaque/hint entries remain incomplete. The wider graphics goal
and global material audit remain active. Current candidate is experimental V558,
SHA256bf62f246f485c7adf9a763c7765bc63476128f73f6cce983717bf297877cff6d.
