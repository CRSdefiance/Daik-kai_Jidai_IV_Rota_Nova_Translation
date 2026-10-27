# Combined V145 checkpoint

Experimental V145 integrates the complete damaged-save message with generated
word-boundary wrapping. The original native slot number precedes the natural
English sentence: "This save is corrupted and could not be loaded." The source
meaning, numbers, leading/final characters and complete words are preserved.

## Artifacts and lineage

- ROM: `out/all_routes_combined_v145_candidate.nds`, SHA-256
  `f6f5e44fef6317706c8cadd9495ba1ccbe7a47b1fb3fe5d0839ee2facef241ab`.
- Patch: `out/all_routes_combined_v145_candidate.xdelta`, 749,175 bytes, SHA-256
  `34ca64aca7af844639d1a72d8c2580ad51827f5dcf16278c9fa95d470eeec492`.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile: `all-routes-unified-v145`; all 435 V144 batches in exact order,
  including required accepted layers. The damaged-save stage follows every
  inherited COMMON, caption, Golden viewer, tooltip, blizzard, placeholder,
  tribute and narrow Options stage.
- Manifest: `out/all_routes_combined_v145_candidate.manifest.json`.
- ARM9 SHA-256:
  `092f5a7f365286c8683728843df8774b26a7ba4ca507f4e6b5d368be82e07e34`.

## Verification

Only the original 52-byte suffix at ARM9 offset 12EB4C differs from V144.
The entire source allocation, original literal consumer and native copy context
are locked. The formatter generates a protected break from one authored paragraph;
no prose is shortened and no executable code changes. The suffix occupies 52 bytes
including NUL; the largest tested complete message uses 58 of 60 destination bytes.

All 256 incoming unsigned-byte cases execute native number conversion, copying,
concatenation and the actual modal formatter/macros with preserved buffer guards.
The actual caller reads an unsigned byte; this test does not claim all values are
valid save slots. Twelve native raster cases cover one-, two- and three-digit
numbers in both pixel formats. Every glyph and independently decoded pixel agrees;
six panels are visually reviewed with no split words. Thirteen targeted release
and Options regressions and changed-tool lint pass.

Saved-ROM verification preserves all 3,668 native COMMON selections and every
other V144 component, including routes, UI, fonts and graphics. Manifest lineage
and registry identity, canonical menu/file invariants and byte-exact clean-ROM
patch reconstruction pass.

The same nine canonical paths change: `/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`,
`/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and
`/data/SC0.DK4` through `/data/SC3.DK4`.

## Remaining checks

Disk reading/checksum validation, full load-error caller/widget composition,
physical screen routing/input dismissal and cold-boot gameplay remain pending.
Native preparation and raster execution use separate invocations. Cold-boot
title/New Game, an established story scene, town UI, valid save/load and the
damaged-save error where available; retain all inherited Options, tribute, map,
caption, Golden Route, sound, help and race checks. Canonical acceptance is false.
No new commit/push or baseline promotion is claimed.

The full goal remains active: remaining COMMON consumers/messages, exhaustive
ARM9/UI classification and translation, Japanese graphics, older-English fidelity
and physical gameplay validation remain. After full completion, revisit older
record-based checks as requested.

Evidence: `work/analysis/damaged_save_v145_saved_proof.json`,
`damaged_save_v145_baseline_verification.txt`,
`translations/damaged_save_native_review_v1.json` and
`docs/damaged_save_message_native.md`.
