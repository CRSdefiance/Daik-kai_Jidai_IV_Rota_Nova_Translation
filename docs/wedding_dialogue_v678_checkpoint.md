# V678: two source-faithful wedding dialogue repairs

## Changes

The original Japanese and neighboring spoken records were reviewed before
authoring two canonical-source `natural-dialogue-v2` paragraphs for Camille:

- B70 R0397: “You'll always have me by your side to protect you.” This preserves
  his unrestricted promise and removes the previous orphaned final word.
- B70 R0615: “Better hurry! Dressing up like this took me forever!” The source
  refers to unfamiliar clothes and the delay getting dressed, not a dress.

Both use the existing route-aware formatter, original speaker09 and unchanged
64/69-byte allocations. There are no authored line breaks or alignment spaces.
Both previews were opened; QA has no errors or warnings. One informational
diagnostic records the deliberate reduction from three source lines to two.

The new final stage compiles from the immutable canonical Japanese bytes. It
requires the exact complete V666 SC2 hash and manuscript hash. This avoids
changing older registered batches or weakening their source locks. Its explicit
proof is in the integrated manifest. The previous status-only goal turn made no
progress; this turn revalidated the stopped work and completed these repairs.

## Verification

Only the two existing SC2 spans differ from V666. All block lengths, offsets,
speaker prefixes and the original wedding movie command4906 at B70 offset4324
are preserved. ARM9, all other components/files, all675 PXL/FLS files and the
previously inventoried921 views/57 embedded extents remain byte-identical.
All470 inherited batches,114 accepted layers and every older profile remain.
The patch reconstructs the complete candidate exactly from the clean ROM.

Three fresh cold boots finish normally:

- Wedding observed and common-fixture baseline:16000 frames each,73 distinct complete
  two-screen pairs identical (74 capture records including the repeated terminal frame), with identical full terminal RAM.
- Ordinary title, New Game selection, established Rafael story and town/trade:
  24100 frames; all89 distinct sampled two-screen frames match V666.

The wedding test reuses the disclosed V677 fixture: only ARM9 R1 changes22 to70
at the original Lil chapter loader, with complete before/expected-after CPU and
unchanged WRAM verified. No savestate, battery save, script/movie replacement or
quest flags are used. It is targeted testing, not earned wedding progression,
a full-route playthrough or physical-device verification.

Four complete text holds verify all glyphs and blank cells at the established
dialogue origin16,296 with16-pixel row spacing, including first/final letters
and all remaining empty rows. Both lines start at16 in the actual ROM. The
conservative static preview's six-pixel continuation indent is not imposed on
the verified runtime. Ten read-only RAM snapshots contain the complete6764-byte
new chapter and the original VM cursor sequence. Source/canonical corruption
guards reject modified inputs.

At the shared older capture frames, only11400 and14200 differ, exclusively inside
their dialogue rectangles. Portraits, nameplates, surrounding art and every
other shared frame match. Original M26 is requested at the same frame14489;
sampled movie frames, following apology and subsequent dialogue remain intact.
The11-frame wedding/transition sheet, both individual changed boxes and an
eight-frame ordinary-phase sheet were visually inspected. No new missing
letters, blank extra page or texture changes were identified in these views.

## Experimental release and evidence

- Candidate: `out/all_routes_combined_v678_candidate.nds`
- SHA256: `d1aaf37bcb7dec218d200a5fa72a6c58e0fb50ab85a8bcb7766d4e749903e341`
- Profile: `all-routes-unified-v678` (experimental).
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Canonical SHA256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Manifest SHA256: `35ea3c40e5563088ced68b70a71bf92fc41939cf4e6461851b6d4f6754c0e06c`
- Patch: `out/all_routes_combined_v678_candidate.xdelta`
- Patch SHA256: `12007db7d3b77416367a4ddf39e76a450f921e3da61af31cc6fa7f3ac4cb9557`
- Registry SHA256: `3954383a34ea1a5399068303ed36712b6643b0198b347bc6ba82b3bed258083d`
- Layers: complete inherited470-batch/114-accepted-layer stack, plus the
  source-locked `wedding_dialogue_cleanup_v1.json` final stage and its two-record
  canonical manuscript `lil_wedding_dialogue_v2.json`. Full paths/checks are in
  the neighboring manifest. No accepted layer or canonical baseline is promoted.
- Changed internal file relative to V666: `/data/SC2.DK4` only.
- Verifiers: `audit_dialogue_batch`, integrated builder checks,
  `verify_wedding_dialogue_v678`, `finish_wedding_dialogue_v678`, and final archive
  verification. Ruff checks pass for the new scripts/module.
- Analysis: `work/analysis/wedding_dialogue_v678/`.
- ROM/patch resolve through the existing output junction to
  `E:/Rota Nova translations/Generated/out/`.
- Screenshot/evidence archive:
  `E:/Rota Nova translations/Screenshots/Test fixtures/V678 Wedding dialogue`.

User acceptance remains open; appropriate manual cold-boot areas are the title,
New Game, story/town and these two changed wedding records with their following
movie/scene. Fixture screenshots are not promoted as ordinary guide screenshots.

## Full graphics goal remains active

All18 plaque/hint audit entries remain incomplete, including material and border
review. All22 original requirement objects are preserved. The six small controls,
eight white village cards, legacy consumers, comic/restoration contexts, remaining
older record checks and final graphics acceptance are still open. The four
low-resolution Online bodies remain excluded by the user's instruction. This
checkpoint completes only the two documented dialogue follow-ups, not the full
graphics-localization objective.
