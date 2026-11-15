# V636: complete faithful commodity labels

## Source review and final terminology

V634's original-ROM cargo control identifies commodity90 as 鉄鉱石, iron ore.
The shared provider still returned the legacy abbreviation Iron. Review of the
same table exposed16 more incomplete labels or lost material/product distinctions.
Seventeen clean-source labels now have complete natural English:

| ID | Japanese | Previous | Current |
|---|---|---|---|
|15|ヤシ油|P. Oil|Coconut Oil|
|20|フカヒレ|Shk Fin|Shark Fins|
|24|シナモン|Cinnam.|Cinnamon|
|40|白金|Plat.|Platinum|
|43|漆器|Lacquer|Lacquerware|
|47|生糸|Silk|Raw Silk|
|49|毛織物|WoolCl.|Wool Cloth|
|50|綿織物|CotClth|Cotton Cloth|
|52|麻織物|HempCl.|Hemp Cloth|
|60|乳香|Incense|Frankincense|
|65|ベッコウ|T-Shell|Tortoiseshell|
|80|ウコン|Turmer.|Turmeric|
|90|鉄鉱石|Iron|Iron Ore|
|91|銅鉱石|Copper|Copper Ore|
|106|鯨肉|Whale|Whale Meat|
|107|黒羊毛|B. Wool|Black Wool|
|118|鮭の燻製|Smoked|Smoked Salmon|

The final oil decision corrects the intermediate V635 draft. Japanese ヤシ油
means coconut oil. The [MEXT food-composition explanation](https://www.mext.go.jp/b_menu/shingi/gijyutu/gijyutu3/attach/1299201.htm)
and [Japan Oilseed Processors Association's ingredient reference](https://www.oil.or.jp/kiso/seisan/seisan01_02.html)
identify it with coconut oil and distinguish palm oil separately. Both source
entries15/120 therefore use Coconut Oil. Their original IDs, prices, categories,
production fields and gameplay behavior remain separate. An invented refining,
quality or palm/coconut distinction is not added to the names.

V635 passed structural/pixel tests but its Palm Oil interpretation was wrong.
It is revoked before handoff or promotion. Its ROM, proofs, captures and support
snapshot remain as diagnostics. V636 is rebuilt from the complete V633 profile,
using the corrected v2 configuration rather than V635 as a parent. Successful
rendering is never used as evidence that a translation's meaning is correct.

Each changed label has a clean source pointer/bytes, context, source gloss,
localization note and individual source/context/localization/naturalness/formatting
reviews in `translations/commodity_fidelity_manuscript_v2.json`. The other107
existing names are preserved; this does not approve every older wording choice.

## Storage and preservation

The94 reused source-name spans total1124 bytes and exclude every earlier native
layout-helper block. All nonzero bytes in those spans must belong to the exact
existing name strings. Every-byte pointer analysis rejects additional start or
interior owners. The prior overlay census covers the identical source spans and
is retained with explicit provenance rather than described as a new scan.

The124 complete labels use111 stored root strings,995 bytes total. Twelve labels
share complete word-boundary suffixes, such as Wool Cloth within Alpaca Wool Cloth.
Entry15 shares the identical complete Coconut Oil string with120. All aliases end
at the original root's NUL and return full names. The separate old shared Whale
string and every noncommodity owner remain unchanged while commodity106 gets
its own complete Whale Meat label.

Only ARM9 differs from V633. All124 price/category/production metadata fields,
native helpers, fonts, palettes, bitmap/view geometry, startup/copy code, heap
bounds, section sizes and staged payloads remain exact. No memory pool expands.
All other internal files and components remain byte-identical to V633.

## Native and actual verification

- All124 original native table getters return the complete intended strings.
- All248 Town-format rasters, two original pixel modes per label, match complete
  independent original-font masks and fit the existing96-pixel view.
- All124 Market/Local cases pass complete184x36 private-image checks, stale
  background clearing, long/short height reset, original shared-atlas preservation
  and one reused native allocation. The category/percentage line is a supplied
  component input, not a trade-arithmetic test.
- All124 Price Info updater cases use their real current table pointers, including
  suffix/duplicate aliases, and match the entire captured bitmap. First/final
  letters fit the original96-pixel name view.
- All124 freshly initialized live name objects match before any fixture and at
  the end of the ordinary two-ship run.
- A22600-frame ordinary copied-save run replays V634's full two-ship sequence.
  All80 sampled whole two-screen compositions match V633 exactly, except the
  complete expected Iron Ore hint overlays in six frames. Every pixel is checked;
  no region is masked out and no capture is retimed.
- A separate17800-frame controlled-label run exercises all17 complete tooltips
  in the real Cargo Setup UI. Each case changes only the initialized name pointer
  for the existing Iron commodity; quantities, stock IDs, prices, categories,
  metadata and icons remain unchanged. Full white hint background, padding, first/
  final glyphs and every other screen pixel match independent expected composites.
  These are disclosed label-substitution cases, not ordinary acquisition or stock
  evidence for the other16 goods. No framebuffer, graphic or drawing result is injected.
- The24100-frame fresh no-save New Game/Market run matches all19 V633 frames.
  Additional paired19700-frame startup runs explicitly capture title, New Game
  captain selection and established opening-story states for the release gate.
- Five invalid source/name/storage/callback controls and three invalid fixture
  inputs are rejected. The new test-harness flag permits only the already verified
  V62196-byte compact-origin callback, checked by its exact hash. The ROM's font
  and drawing code are unchanged. An early preview decoder used the wrong16-bit
  stride; it was corrected and visually reviewed before registration. That was
  an analysis-image defect, not a shipped ROM graphics change.

All runs cold boot without savestates. Ordinary runs have no gameplay fixtures;
the separate label run is explicitly opt-in and records every changed byte. The
unchanged copied donor SHA256 is
`958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb`.
These are targeted automated emulator tests, not complete route or hardware tests.

## Registered release and exact patch

- Experimental ROM: `out/all_routes_combined_v636_candidate.nds`.
- SHA256: `c4ff537ddcd4da5eb1743fb28cd0eb160492e9b660af080ddae44e94a9f4d95d`.
- Profile: `all-routes-unified-v636`, complete470 inherited batches and114 accepted
  layers, all V633 native stages and the corrected `commodity_fidelity` stage.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Neighboring manifest: `out/all_routes_combined_v636_candidate.manifest.json`.
  It records the exact registry hash, all batches/stages,53 paths changed from
  canonical and all changed records. Only ARM9 changes from V633.
- Patch: `out/all_routes_combined_v636_candidate.xdelta`, SHA256
  `e9d80fc5084d9d52553846a0a3830f8f6abda675c2a424b11f523c276623bda5`.
- Patch input: `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The patch reconstructs every byte of the saved candidate. Fresh921 PXL/FLS
header/palette/dimension/extent checks and57 embedded block extent checks pass.
Physical ROM/manifest/patch location is `E:/Rota Nova translations/Generated/out/`.
All relevant changed-tool Ruff and syntax checks pass.

Preparation: `scripts/prepare_commodity_fidelity_v636.py --register`.
Native consumers: `scripts/verify_commodity_consumers_v636.py`.
Actual/release verifier: `scripts/verify_commodity_release_v636.py`.
Proofs and inputs: `work/analysis/commodity_fidelity_v636/`.
The v636 adapters select corrected paths/labels while preserving the full existing
v635 verifier bodies. Both adapter and implementation source are archived.

User cold-boot review remains: title/New Game, ordinary goods labels in towns,
Market/Price Info/Cargo and ongoing plaque/equipment/condition variants. Automated
checks do not constitute user acceptance or canonical promotion.

## Audit and next work

The source fidelity follow-up for Iron in V634 is resolved by this complete shared
provider correction. Historical observations are preserved with an additive
resolution entry. All18 original plaque/hint objects remain incomplete and exact;
all22 historical requirement objects/scopes remain exact. Only the latest compiled
experimental pointer advances to V636. V610 verified and canonical pointers remain.

Five miniature/Confirm ordinary parents, village cards, legacy/environment/raw
comic consumers, remaining movie/material variants, other older wording and human
review remain open. Source-equivalent oil names do not alter that wider scope.
The graphics goal remains active. Older record checks remain due at full completion.
Unmodified captures and proofs are archived under
`E:/Rota Nova translations/Screenshots/Test fixtures/V636 Complete commodity names`.
Only ordinary current captures go to the separate guide-candidate folder; controlled
label screenshots are explicitly excluded from guide acquisition evidence.
