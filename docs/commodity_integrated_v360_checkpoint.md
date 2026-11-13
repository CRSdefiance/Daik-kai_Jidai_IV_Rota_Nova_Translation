# Combined commodity/UI checkpoint V360

Status: experimental combined candidate; full graphics goal remains incomplete.
Canonical baseline is unchanged. V356 and V358 are superseded checkpoints after
the Price Info clipping and duplicate Cargo printf defects were found.

## Changes and verification

- All49 newly confirmed Japanese commodity names have full source-reviewed English.
  All124 table entries and original metadata are checked. No shortened substitutions
  or Maria visibility/rare-stock research changes are in the release.
- Town specialties use compact spacing and separate source rows, preserving the
  shared date/percentage cells. Registered-ROM Continue reaches Lisbon and all five
  actual specialty masks match their full source names, including singular Almond.
- Goods Info displays full names; the Local/Cargo caption wraps longer names at
  word boundaries within its original column. Independent private surfaces retain
  the original shared atlas. All124 native cases pass.
- Price Info's separate name updater also uses compact, origin-aware rendering.
  All124 native cases fit the96-pixel view. Actual Black Glacier Sword has all215
  ink pixels and blank cells exact;293 changed pixels are confined to that label.
- Both duplicate native printf templates now end in `%%`. Native execution with
  unchanged arguments reproduces the old Japanese suffix read beyond NUL and
  verifies its removal. Separate Shortage/Trending labels retain their predicates.
  The release stage guards both known format-pointer fieldsC3EF8/C4074.
- Normal stylus dragging moves Olive Oil from Local to Cargo in the genuine
  cartridge save. Actual Cargo name/category/percent masks are exact after the
  duplicate correction; other pixels, icons and planned amounts are unchanged.
  Spent418/Net26982 are pending transaction totals, not proof of a completed purchase.

The only V358→V360 changes are three Cargo literal pointers. All earlier feature
code, maps, names, sprites and route data remain exact. V360 preserves all470
inherited batches, all inherited native stages and the immutable canonical base.
Only ARM9 differs from V342. The clean-ROM patch reconstructs the candidate exactly.

## Artifacts

Candidate SHA-256: `8edfa3912876fe806ff5e2c69430df6c21a4e5594192364f2a58fe504619595a`.
Patch SHA-256: `4d181ead20929cd7c1ce82b2c18128af5ead43c8ea7aa39ad021e2daec525c9a`.
Canonical base:`out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
All accepted layers remain baked into that canonical base; all470 inherited
experimental batches and all inherited native stages are retained. The added
experimental stage is `commodity_ui_release_v3.json`; its complete dependency and
internal change records are in the manifest. Only `/__arm9__.bin` changes from V342.

User cold-boot checks: title/New Game, town specialties, Goods Info/Local/Cargo,
Price Info and ongoing Sailor Info/Assign Sailors variants. Candidate remains
experimental and the canonical parent is not promoted.

- Candidate:`out/all_routes_combined_v360_candidate.nds`
- Profile:`all-routes-unified-v360`
- Manifest:`out/all_routes_combined_v360_candidate.manifest.json`
- Patch:`out/all_routes_combined_v360_candidate.xdelta`
- Release config:`translations/commodity_ui_release_v3.json`
- Release module:`dk4tool/patch/commodity_ui_release.py`
- Evidence:`work/analysis/commodity_release_v360/release_proof.json`
- Price evidence:`work/analysis/commodity_price_v357/`
- Cargo evidence:`work/analysis/commodity_cargo_v359/`

The first V360 builder run saved a matching ROM/manifest but failed printing a
Unicode character under Windows' default encoding. Its UTF-8 rerun completed with
exit0. The final production-ROM checks passed: normal New Game and33 complete
town/market/Cargo captures matching the verified replay. This was an output-encoding
failure, not a claimed boot fix. See `scripts/verify_commodity_release_v360.py`.

## Evidence limits and remaining goal

New Game/story and genuine-save town checks are targeted cold-boot emulator tests,
not full route playthroughs or hardware verification. Long-label Price Info uses
a documented supplied-label/Maria-visibility fixture; Cargo uses an ordinary save
and normal drag controls. Actual shortage/trend eligibility, broader/repeated scene
coverage and other unresolved graphics consumers remain open. V393 resolves the
particular opening-wipe frame's source-pixel concern and checks current genuine
Lisbon loading; broader transition timing/context remains unproven. See
`town_transition_v393_checkpoint.md`. All18 plaque/hint entries and variants
remain incomplete.
Online low-resolution images remain exempt. Revisit older record-based checks at
actual full goal completion. Do not promote this candidate without user acceptance.
