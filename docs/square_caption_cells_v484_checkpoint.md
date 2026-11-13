# V484 complete Delicacy Shop caption

## Integrated release

- Candidate: `out/all_routes_combined_v484_candidate.nds`.
- SHA-256: `f2036bafc3736a353cb0a2de8f40bd5eee8bed3cd16e779f68e3ebb1914b875c`.
- Profile: `all-routes-unified-v484`, experimental, not promoted.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- All 470 inherited batches/stages and 114 accepted layers are retained.
- Only `/__arm9__.bin` differs from the complete V474 parent. All other files,
  components, route/shared/help text and graphics remain byte-identical.
- Exact clean-ROM patch reconstruction passes; adjacent manifest is required.

## Faithful wording and layout

Original category2 is 珍味, delicacies. The Square now reads **Delicacy Shop**.
Other shared category labels are unchanged. The original six-pixel glyph-cell
check had suppressed the final letter of the proposed full label even though
its actual ink fitted the 64-pixel view.

The scoped painter renders into a private 68x12 bitmap and copies the visible
64x12 region into the original caption bitmap. It restores the original view,
header binding and clipping rectangle. Halfword copies preserve row alignment;
extra rendering columns do not overwrite the following row's leading letters.
Original font, palette, frame, selectable rectangle and visible extent remain.
Contracts outside the exact Square 64x12, 4-bit view delegate to the old painter.

The private bitmap and helper occupy868 bytes of the existing zero gap C1A0-C600
in the4096-byte owned SDK bank. Source market code ends at C19C, its vtable starts
at C600 and its persistent heap pointer lives at C680. Market image pixels are
heap-allocated. No existing aligned literal enters the new owned span.
All section sizes, startup wrapper, heap boundary and cache sequences are exact
to V474. No bank or startup-pool growth is required.

## Verification

- All18 native Square captions match complete independent font masks and blank
  cells. The other17 captions and contexts match V474 exactly.
- Four native nonmatching contracts preserve original fallback output/context.
- Shared category getters, source buffers, private-buffer guards, complete saved
  register/stack ABI, startup/cache/arena tests pass.
- Genuine Istanbul save: all four selections, focus borders, complete Delicacy
  Shop first/final glyphs and all other labels match. All matched frame changes
  are confined to the changed caption. Shop activations and complete dialogue
  remain intact; both dialogue lines start at x22.
-56 whole fresh-game frames match V474, covering title, selection, story, town
  and help. Both runs are cold boots; no savestate, inventory or unlock fixture.
- All921 original graphics format/flag/palette/dimension/extent invariants pass.
  The84 previously edited entries are retained.
- Clean patch reconstructs every candidate byte. Targeted Ruff passes.

Native verifier: `scripts/verify_square_caption_cells_v483.py --fixed`.
Release verifier: `scripts/verify_square_caption_release_v484.py`.
Evidence: `work/analysis/square_caption_cells_v484/native_proof.json`,
`release_proof.json` and `preservation_proof.json`.
Captures: `work/emulation_v193/square_cells_v484` and `square_cells_fresh_v484`.
ROM/patch/manifest and genuine guide screenshots are copied with SHA verification
to `E:\Rota Nova translations`.

## Rejected V483

The append-only variant V483 passed isolated native boot/cache tests but both
actual cold boots remained black with a START prompt. Its profile is revoked;
it is not a release or parent. V484's fixed-size variant passes actual boot.
This establishes a working repair, not the exact cause of V483's startup failure.

## Remaining goal

All22 historical graphics requirements and all18 incomplete plaque entries remain
in the audit. Other cities/categories, legacy art consumers, regional visits,
Gallery/endings and full graphics gameplay verification remain open. No hardware
or full-playthrough claim. User cold-boot acceptance is required before canonical
promotion. At actual full-goal completion, revisit older record-based checks.
