# V187 complete opening-logo correction

2026-10-05. The user's unfaded V186 screenshots show different gold
graphics: the opening retains a thick white fringe while the menu has shaded
edges. The earlier fade explanation did not address that difference. V187
replaces opening gold with a transparent extraction of canonical menu gold
lettering and dark/neutral shadows. The approved blue wordmark, menu artwork,
copyright, backgrounds and runtime rendering remain unchanged.

Five focused tests, byte-exact full V186 reproduction, all 463 registered batches
and terminal stages, saved artwork/manifest and exact clean-ROM patch
reconstruction pass. Only `/FLS/M28.fls` and `/_pxl/logo.pxl` change versus V186.
The matte is color-derived and reviewed offline. Native V187 appearance and
cold-boot acceptance remain pending. V187 is experimental; the broader graphics
goal stays paused. See [V187 checkpoint](all_routes_unified_v187_checkpoint.md).

## Required handoff details

- Candidate: `out\all_routes_combined_v187_candidate.nds`
- Candidate SHA-256: `a04d405c5e2de45d268dd999d8de65e260c0d1746c32d022b1d5f88d7c9b638e`
- Canonical base: `out\raphael_natural_v2_accepted_base.nds`
- Canonical SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Profile: `all-routes-unified-v187`, experimental.
- All accepted layers are baked into the canonical base; 0 additional accepted batches applied.
- Experimental batches: 463; full V186 stack with exactly two batch replacements.
- Changed versus V186: `/FLS/M28.fls` texture5 and `/_pxl/logo.pxl`.
- Changed versus canonical: 34 paths, listed in the neighboring manifest.
- ARM9 unchanged: `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf`.
- Patch: `out\all_routes_combined_v187_candidate.xdelta`
- Patch SHA-256: `805b25dabe03702e28afb0791f1d75edc4b2a594321180cc90e76e284ea7ed24`
- Clean patch base: `work/clean.nds`, SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- Checks: five focused tests, Ruff, byte-exact full V186 reproduction, full stack/terminal stage/unrelated record inheritance, saved artwork and ROM/manifest identity, golden menu anchors and exact patch reconstruction.
- Cold-boot review pending: opening video and unfaded logo, title menu, New Game character selection, established story scene and town UI. Use a fresh boot without savestates.
- No canonical promotion; broader goal paused/incomplete.

## Source and verification limits

Menu source is reconstructed from canonical title03 bytes and the established
V186 wordmark/caption recipe. No authoring input comes from a derivative ROM.
All 1,221 warm-gold core pixels survive exactly in the shared RGBA extraction.
Warm gold and neutral dark edges within the original Latin silhouette are retained;
the opening white fringe and blue scenery are omitted. Its matte is color-derived,
not recovered original alpha. Original palettes separately quantize the colors.

M28 texture4 blue wording is byte-exact. Every original movie record, palette,
dimension and byte outside texture5's pixel slot is unchanged. Standalone logo
retains its original black palette key (255, not index0), header/palette and
unowned pixels. Its two old main/caption ownership records become one complete
`DK4_ROTA_LOGO_COMPLETE_V3` record; other IDs and terminal stages are retained.

The water preview is an illustrative projection of original M28 background art,
not proof of video UVs, timing or GPU alpha. Native cold-boot review is pending.

## Artifacts

- Author: `scripts/title_logo_match_v187.py`
- Tests: `tests/test_title_logo_match_v187.py`
- Gold source: `translations/assets/menu_gold_logo_v187.png`
- Batches: `translations/rota_title_logo_art_v3.json`, `translations/opening_m28_title_art_v3.json`
- Preview: `work/qa/title_logo_match_v187/comparison.png`
- Saved proof: `work/analysis/title_logo_match_v187_saved_proof.json`
- Exact V186 reproduction: `work/analysis/v186_complete_logo_reproduction.nds`
