# V204: opening Hodram artwork reconciled

## Candidate and ancestry

- Candidate: `out/all_routes_combined_v204_candidate.nds`.
- SHA-256: `fe7ab2b79abc45478767ffe3d1156a8d95177ec8e65970ceea4badd5458ecd50`.
- Profile: `all-routes-unified-v204`, experimental.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- All 114 accepted layers remain baked into that base. All 465 active batches and
  all prior terminal stages are retained. One M28 batch is replaced by a superset:
  `opening_m28_title_and_hodram_art_v5.json` preserves its two original title recipes
  verbatim and adds 20 name-art records. Every previous changed-record ID remains.
- Only `/FLS/M28.fls` changes relative to V190; scripts, ARM9, ARM7 and all other
  files/components are byte-identical. The manifest lists full changes from canonical.
- Patch: `out/all_routes_combined_v204_candidate.xdelta`, SHA-256
  `c457db5b484b0986d70fd9c4b0f694ca521f2b5cdb19621f16873112b1344641`.
  Applying it to pinned `work/clean.nds` (SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`)
  reconstructs the exact candidate.

## Faithful lettering and native allocations

The confirmed first name **Hodram** replaces original artwork's **Hoodlum**, whose
unwanted English meaning prompted the user-approved adaptation. Joakim Bergstrom
stays. The native reveal frames already supply all required glyphs, so this uses
the original cyan serif lettering, including its opaque black shadow index seven.
No generated substitute font, palette changes, reduced glyphs or bitmap resampling
are used. The imagegen skill was evaluated; its editable-native-asset guidance led
to reusing the source font system instead of generating different artwork.

Textures 25/26 (H/Ho) stay exact. Textures 27–46 receive the reconstructed word and
original middle/surname pixels shifted six pixels left. There are still 22 reveal
slots; texture 31 holds the completed shorter first name until Joakim begins at
the original time. All original timing metadata, palettes, dimensions and flags
remain intact. All 20 new preview frames were reviewed completely.

The existing compressed slots were too small. A more efficient encoder was tested
and did not solve every allocation, so it was discarded. The source has 96 verified
zero alignment bytes between each relevant palette and pixel stream. The batch
reclaims **608 bytes total, at most 80 per texture**, entirely inside that padding.
Only pixel offset/slot-length fields change, and every original slot end is fixed.
Palette allocations and every other declared native stream are protected; three
unsafe map cases fail closed. No archive growth or shared runtime alteration occurs.

The builder's mapping is opt-in. The full V190 build reproduces its original SHA
byte-for-byte before V204 integration. The final archive remains 4,394,624 bytes;
every unowned serialized byte, including the earlier main-title artwork, is exact.

## Complete native verification

Fresh DeSmuME cold boots use the existing pinned interpreter/software core with
ordinary inputs and no savestate or memory injection. All **22 complete reveal
states** match native five-bit pixels at their observed four-frame cadence,
including black shadows, first/last letters and absence of extra bright strokes.
These checks cover **35,330 displayed pixels** across the states. The final name
matches all **3,047 nonzero pixels** at bounds **[13, 167, 241, 187]**, inside the
top display. Complete preview and saved-native-frame visual review passes.

The 9,000-frame regression run reaches the title/menu, New Game captain selection,
confirmation, Lisbon arrival and established opening dialogue. Reviewed captures
include the complete name card, title/menu, captain screen, town/arrival and both
Claudio/Raphael dialogue samples. There are no callback errors. Golden content,
full inheritance, exact patch reconstruction and focused Ruff pass.

A separate 16,000-frame cold boot selects Prepare alone and reaches the actual
Lisbon town menu at frame 14,900, with trade goods, company share, funds, date and
facility controls visible. This completes the town-UI regression gate; the earlier
arrival/walking scene is not used as a substitute for that menu. Later scripted
inputs enter the port tutorial normally. Its complete capture report/hash is
checked alongside the opening and name-reveal runs.

Evidence: `work/analysis/hodram_opening_v204/saved_proof.json`,
`preintegration_preservation.json`, `padding_negative_checks.json`, `preparation.json`,
the reproduction/build logs and exact patch reconstruction in that folder. Native
frames/reports are under `work/emulation_v193/hodram_opening_v204/`, including
`fine_reveals/`. Scripts: `prepare_hodram_opening_native_glyphs_v204.py` and
`verify_hodram_opening_v204.py`.

## Scope still open

V204 is experimental, not a promoted baseline or the completed graphics goal.
The other confirmed-name fields/text migration remains unregistered: old text
spellings elsewhere are not resolved by this artwork change. Continue the complete
editorial/preview and COMMON/help/caption/biography work, four unfinished Online
bodies, legacy/archive/contextual art and broader native/gameplay verification.
The current graphics audit and progress retain this full scope. User/device testing
should check the opening card and normal menu/New Game progression. No acceptance
is assumed. At eventual goal completion, revisit the older record-based checks.
