# V523: all original Event Scenes galleries and caption bounds correction

The automated V522 run visited all164 positions: Rafael46, Hodram41, Lil39 and
Maria38. Each selected frame has actual framebuffer and read-only4MiB RAM evidence.
The run used an authorized checksum-valid copied Gallery save; no production ROM
cheat, savestate, original donor change or earned-unlock claim. Maria starts at1
and ends at0; exact source image/caption comparisons prove every38 positions once.

## Defect found and source-faithful correction

Maria position35, original `総見式のマリアたち`, was translated as
`Maria and Her Companions at the Grand Review`. Its44 characters occupied220pixels,
overlapping both original carousel arrows. The actual V522 screenshot loses leading
and trailing letters. V522 is retained as diagnostic evidence, not a complete pass.

Reviewed English: `Maria's Party at the Grand Review`. Party denotes Maria and
her companions; the title preserves the group and Grand Review ceremony without
inventing a particular friendship, fleet or army. Its33 characters occupy165pixels
and fit the original space between arrows. No authored wrapping or clipping.

The registered late correction replaces only the existing45-byte NUL-terminated
ARM9 slot at0x1398C0, padding within the owned allocation. Thirty-eight data bytes
change from V518. Code, pointers, neighbors, palettes, borders, dimensions, pool
sizes and all other components remain exact. Historical caption manuscripts and
profiles stay reproducible. Separate COMMON consumers retain their prior wording;
their layout is distinct from the Gallery's arrow-bounded title field.

The build guard resolves all164 final titles from actual pointer tables, including
the original staged-pool copy, and requires full glyph bounds inside[32,224]. It
rejects the old title; every corrected title passes. Future derived profiles must
retain this guard. This is a Gallery-specific geometry guarantee, not a claim
that every text format elsewhere shares the same layout.

## Corrected combined release evidence

- All164 complete256x192 source images match8,060,928 native-color pixels;
  there are159 distinct source images across the route tables.
- All164 title masks, Event Scenes headings and captain descriptions match complete
  glyphs/blank cells, using each screenshot's actual RAM pointers and strings.
- Four full carousel wraps and all four Gallery popup labels pass. Original arrow
  visibility after the first input is explicitly accounted for.
- Exactly one of168 Gallery selection/wrap frames changes versus V522:37600.
  Only pixels inside the original caption band change. The corrected title is
  complete at both ends; all other images and captions remain exact.
- All56 fresh title/New Game/story/town/Help frames match V518 exactly, using the
  same controls without a fixture save. Touchscreen support is enabled as required
  by that established schedule; the earlier launch without it failed before boot.
- All470 inherited batches and114 accepted layers retained. All675 PXL/FLS and
  every other component are byte-identical to V518. All921 source-preservation
  entries inherit by exact container equality.
- Clean-ROM xdelta reconstruction is byte-exact. Targeted Ruff passes.

Candidate: `out/all_routes_combined_v523_candidate.nds`.
Profile: `all-routes-unified-v523`, experimental.
SHA-256: `76cb6645e040a68f7470f25e0a70bcd965bb1b2450cdecf6c383cae4647ee3fa`.
Patch SHA-256: `29ac4f09e814a5c346fcb3e402850eaaa5214a7943b561413131a831066f2364`.
Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Canonical unchanged. Only `/__arm9__.bin` differs from V518.

Verifiers: `scripts/verify_gallery_carousels_v522.py` (parameterized) and
`scripts/verify_gallery_release_v523.py`.
Proofs: `work/analysis/gallery_caption_v523/all_carousels_proof.json`,
`release_proof.json` and `preservation_proof.json` in that folder.
The ROM, patch and manifest are published with verified copies to
`E:/Rota Nova translations`. Labeled Gallery captures are archived separately at
`E:/Rota Nova translations/Screenshots/Test fixtures/gallery_v523`.

Characters gallery, original ending/movie playback, raw legacy consumers,
restoration and other original graphics requirements remain open. These are
scoped automated emulator tests, not full playthroughs or hardware verification.
All22 original requirements and all18 incomplete plaques remain under audit;
full graphics goal active. Revisit older record-based checks at full completion.
