# Combined V144 checkpoint

Experimental V144 integrates two complete natural-English Options confirmations:
"Sailing Help is %s. Change to %s?" and "Reports are %s. Change to %s?".
Current/proposed On/Off arguments retain the original order. Complete source
allocations, leading/final glyphs and unrelated preference bits are preserved.

## Artifacts and lineage

- ROM: `out/all_routes_combined_v144_candidate.nds`, SHA-256
  `2e31ea3bf06a46084a06c46cdf652f1a1c0383484799f49b5a3fc410cba84f33`.
- Patch: `out/all_routes_combined_v144_candidate.xdelta`, 749,124 bytes, SHA-256
  `88077f7de2c399019af37eae8f79cefc23f3e03ee230efddc6feb82a4b41eca9`.
- Base: immutable `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile: `all-routes-unified-v144`; all 435 inherited V143 batches in exact
  order, including required accepted layers. The Options stage follows the full
  COMMON, caption, Golden viewer, tooltip, blizzard, placeholder and tribute stack.
- Manifest: `out/all_routes_combined_v144_candidate.manifest.json`.
- ARM9 SHA-256:
  `9c0b2992d7b2a731869b590af1455fb84ed5c4b87b296112f3793ea4a651a8db`.

## Verification and limits

Only ARM9 slots 13880C (56 bytes) and 138844 (52 bytes) differ from V143. Every
other ROM component is byte-exact, including all four routes and translated
graphics. All 3,668 native COMMON selections are unchanged. Strict source,
manuscript, native-review and output hashes gate integration.

Ten native caller/formatter cases, twenty confirm/cancel response cases and eight
native raster cases pass. All four distinct On/Off panels are visually reviewed;
full sentences fit one row with intact leading/final characters. Ten focused
tests and changed-tool lint pass. Saved-ROM and canonical baseline verification
pass; the patch reconstructs the exact candidate from the pinned clean ROM.

The same nine canonical paths change: `/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`,
`/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and
`/data/SC0.DK4` through `/data/SC3.DK4`.

Full widget composition, physical screen routing/input and cold-boot gameplay
remain pending. Cold-boot title/New Game, an established story scene, town UI,
both Options settings in both states, confirmation/cancellation, and persistence
after reopening. Retain all inherited tribute, caption, Golden Route, map, sound,
help, race and save checks. Historical ASCII-corruption warnings still apply to
older builds; this stage requires the exact complete V143 renderer stack.

Canonical acceptance is false. No baseline promotion or new commit/push is
claimed. The broader goal remains active: 245 Japanese COMMON selections across
133 records (31 promotional and 214 scene/artwork/name entries), exhaustive
ARM9/UI/graphics work, older-English fidelity and physical gameplay verification.
At full completion, revisit older record-based checks as requested.

Proofs: `work/analysis/options_narrow_v144_saved_rom_proof.json`,
`options_narrow_v144_patch_roundtrip.json`,
`options_narrow_v144_baseline_verification.txt`, and durable
`translations/options_narrow_native_review_v1.json`.
