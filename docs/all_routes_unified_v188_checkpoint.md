# V188 opening title edges and speckle correction

2026-10-05. User rejected the V187 title preview: the opening looked
jagged and pale dots remained around the gold logo. V187's hard color cutout
included original ship/background pixels; black-matted blue edges also looked
harsh over water. V188 removes those pixels, recovers 868 fractional gold-edge
pixels from the canonical menu/background pair, retains all 1,221 warm-gold
core pixels, and uses the menu's blue face shades with soft outer coverage.
Edges are preblended against the opening water artwork for its native indexed
textures. Menu title artwork, backgrounds, copyright and ARM9 remain unchanged.

Eight focused tests, byte-exact full V187 reproduction, all 463 registered
batches/record IDs/terminal stages, saved artwork/manifest and exact clean-ROM
patch reconstruction pass. Only `/FLS/M28.fls` and `/_pxl/logo.pxl` change versus
V187. V188 is experimental: native appearance needs cold-boot review. V187 is
superseded for title-art quality. The broader graphics goal remains paused.
See [V188 checkpoint](all_routes_unified_v188_checkpoint.md).

## Required handoff

- Candidate: `out\all_routes_combined_v188_candidate.nds`
- SHA-256: `a2783f08ea8920cfa3fdaddc3fb0e2f61755d268f99c4d9ea557c97157c0a251`
- Canonical base: `out\raphael_natural_v2_accepted_base.nds`
- Canonical SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Profile: `all-routes-unified-v188`; experimental, no canonical promotion.
- All accepted layers are baked into the canonical base; 0 additional accepted batches applied.
- Experimental batches: 463; complete V187 stack with only two batch replacements.
- Changed versus V187: `/FLS/M28.fls` texture4/5 pixel slots and `/_pxl/logo.pxl` owned title rectangle.
- All 34 changed paths versus canonical are listed in the manifest.
- ARM9 unchanged: `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf`.
- Patch: `out\all_routes_combined_v188_candidate.xdelta`
- Patch SHA-256: `0e3ae78fd6eb050b72563068bd9f44cb2d7a6e41d3be20f8a250ff20c895bac2`
- Clean patch base: `work/clean.nds`, SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- Verification: eight source-coverage/soft-edge/speckle/native-asset/clipping tests, Ruff, exact full V187 reproduction, all saved batch/record/stage/manifest identities, golden menus, unrelated files and exact xdelta reconstruction.
- Cold-boot review: opening video including unfaded title, title menu, New Game selection, one established story scene and town UI. Do not load savestates.
- Broader goal remains paused/incomplete.

## Source, method and limits

Authoring uses canonical menu/background pixels and the existing approved
wordmark recipe, not a derivative ROM as translation input. Warm-gold source
cores are exact in RGBA. Background-only pixels differing by at most 25 color
levels are excluded; retained shadow components must connect to actual gold.
Partial edges are estimated using nearby foreground colors and the original
background, then unmatted. The six known pale N/background samples are now
transparent. All 868 fractional gold edges are retained through background
preblending before native palette projection.

Blue faces reuse canonical-authored menu RGB where original coverage is at least
96/255. Lower-coverage edges are unmatted using their original background and
retain soft alpha. Native indexed textures do not carry that per-pixel alpha:
edges are preblended against original M28 texture2's water projected to 256x192,
then quantized into unchanged native palettes. Palette conversion and the
estimated matte are approximate. Native video UVs, relative placement during
animation and GPU composition still need review; the offline preview is not
live emulator evidence. Fade effects remain unchanged.

Headers, palettes, dimensions and native movie records are unchanged. All movie
bytes outside texture4/5 pixel slots, all standalone unowned pixels and every
unrelated ROM file are exact versus V187. Every record ID and terminal stage is
retained. Background/color-key index semantics are preserved (standalone black
is palette index255). Menu copies and their artwork are byte-identical.

## Artifacts

- `scripts/title_edges_v188.py`
- `scripts/title_logo_matte_v188.py`
- `tests/test_title_edges_v188.py`
- `translations/assets/menu_gold_logo_v188.png`
- `translations/rota_title_logo_art_v4.json`
- `translations/opening_m28_title_art_v4.json`
- `work/qa/title_edges_v188/comparison.png`
- `work/qa/title_edges_v188/user_report.png`
- `work/analysis/title_edges_v188_saved_proof.json`
- `work/analysis/v187_soft_edges_reproduction.nds` (exact V187)
