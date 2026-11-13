# Lil ending pan: remaining source rows V596

This checkpoint addresses the specific V578/V583 gap for M31 texture1 rows64–127.
Production stays experimental V593; no translated artwork or release changes.

## Actual display and original animation state

Two fresh26,600-frame cold boots use the established Lil New Game inputs and
the authorized one-byte ending-state fixture at18000. No battery save or
savestate is loaded. These are synthetic ending tests, not an earned route finish.
Both emulator processes exit successfully.

The source M31 movie is byte-identical to clean. Its three pan tiles are256x128.
The full original texture1 was extracted and reviewed again: buildings, water
and the cloaked woman's lower body; no readable Japanese caption. Source art
remains intact, including the part outside the observed viewport.

The original selector and quad functions bind the actual top-to-bottom tile
order3,2,1. All2,344 complete opaque upper-screen composites match independent
windows of that source canvas. Their source-window origins span0 through128.
This accounts for every row of tiles3/2 and rows0–63 of tile1 in those displays.

Starting with the actual18096 RAM snapshot,2,452 original per-frame updates reach
20548, including the transition to inactive pan geometry at20547. Nineteen actual
snapshots match all0x1B18 controller bytes. The original renderer's six-instruction
polygon-ID increment runs for each drawable quad; this byte is not exempted.
The original selector/quad/update instructions execute without SDK or geometry
bridges. Geometry places tile1 no higher than screenY128, so source row64 begins
at or belowY192. All GPU raster-edge conclusions additionally use the actual
paired captures below. Later scenes and full-controller replay beyond this pan
are not claimed.

## Altered-row control and timing discovery

A clearly labeled research-only clone changes16,358 palette indices exclusively
in texture1 rows64–127, including all256 pixels of row64. The existing palette
provides a bright edge and high-contrast checker pattern. Every header, record,
extent, palette, other texture, timeline, other ROM file and ARM9 byte is exact.
The changed movie fits its original slot. This is never a playable handoff ROM.

At18120/19400/20400, both snapshots contain their respective complete32,768-byte
decoded tile at the same address. The original unmodified tile is absent from
the altered run's main RAM. The altered data really reached decoded memory.

The first same-frame comparison failed, rather than proving a graphic defect:
193 frames differ during fades or subpixel movement. Actual controller fields
show the altered run one original update ahead. One original update plus original
draw-ID instructions reproduces the entire altered controller from the production
snapshot at all three decoded-tile anchors. The cause of that phase difference
is not established; changed compression/load timing is only a possible explanation.

The final verifier uses a fixed offset, never a per-image best match: production
frames18028–21000 compare with control frame−1. All other selected frames compare
at their original frame number. All3,007 complete two-screen pairs then match:
2,973 use that fixed offset;2,814 also match without alignment. The original
same-frame failure is retained in the proof. These checks support exclusion of
the marked lower rows from this pan; they do not establish general timing
equivalence or a complete alpha/GPU compositor.

## Outcome, preservation and remaining work

The specific unobserved64-row pan gap now has source geometry, actual controller,
decoded-resource and paired native-frame evidence. No English lettering was
missing from that source region, and no production correction is needed.
Other ending effects, legacy graphics consumers, Confirm/miniature/marker parents,
the wider material audit and final acceptance remain open. All18 original
plaque/hint entries remain incomplete and all22 historical objects remain exact.

Evidence: `work/analysis/ending_pan_rows_v596/pan_rows_proof.json`, the two
capture reports under E:/Rota Nova translations/Generated/work/emulation_v193/
ending_pan_v596_lil*, and the scripts named in that proof. Unmodified full test
screenshots, the original source extraction, reports and hash receipts are
archived under Screenshots/Test fixtures/V596 Lil ending pan rows on E.
No guide/publication or physical-device credit is claimed. Current V593 SHA256
remains `d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642`.
