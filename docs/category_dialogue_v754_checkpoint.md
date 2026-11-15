# V754: full category names in the forecast

COMMON730 completes editorial review. Cumulative coverage is103 entries:69 revised and34 retained. The earlier730-746 source packet is now complete. Further Market/shared prose, every route, remaining player-facing prose and the separate graphics audit remain open. The full goal stays active.

## Natural English and complete arguments

> Something in the %s market is sure to catch on soon.

The source predicts one unspecified good within the named category will catch on soon, rather than every good in the category. The new paragraph preserves certainty and future sense in natural merchant language. Full arguments replace Cond., Delic., Metals, Jewels, Med and Goods only in this dialogue: Seasonings, Delicacy, Precious Metals, Jewelry, Medicine and Sundries. Other already complete category words remain unchanged. The clean Japanese category table binds all18 names; the existing UI category-name capitalization is retained. Actual shop/menu captions retain their original shorter words.

## Owned storage and schema

The global18-word table at ARM9 file11B444 is now an explicit private packed lookup: high8 bits hold the compact string's byte offset into the140-byte family at15A090; low24 bits hold the full pointer minus01800000. Getter C5BA0 decodes the appropriate value. Only original730 caller returnPC0205FC48 selects full names. Every other caller uses compact names. Future tools must call the native getter or use the pinned decoded maps, rather than interpret these words as raw pointers.

The complete compact family plus Seasonings, Precious Metals and Sundries fits138 bytes by sharing the complete Metals suffix. Existing read-only Delicacy/Jewelry/Medicine strings supply the other expansions. The old nested Square category helpers are consolidated without changing their Delicacy/Jewelry overrides. Existing code slots, two duplicate Fleet label slots and the already-unreferenced Dock B slot hold the decoder. The three Fleet header owners now point to the complete immutable Fleet suffix in Create Fleet. Exact source Japanese slots, all byte-aligned/unaligned data-pointer owners, every branch into the replaced code, source helper bytecode and the single table owner are checked. No mutable caption buffer or runtime-owned name tail is reused.

No section, staged payload, startup/cache wrapper, allocator, font, graphics palette or view grows. The decoder preserves the tested original negative/sentinel return values and caller ABI. Ownership reports list every changed span and restore all other bytes exactly. All3667 other message texts and40 other COMMON blocks remain byte-exact; only730's native offset changes. Earlier68 revisions,675 graphics and the full470-batch/114-layer stack are preserved.

## Native and actual visual verification

-108 original getter/caller cases:18 categories for five menu callers and the original730 caller; caller return, stack and saved registers pass.
-18 complete native Square caption planes and their contexts are byte-exact, including all768 palette indices; four fallback surfaces are also exact.
-36 negative/sentinel cases preserve original returns. Three Fleet header fields give complete Fleet bytes through the actual native printf routine, including the unaligned immutable suffix.
-18 executions of the unchanged original730 caller reach its original direct portrait call with the complete full-name pointer.
-18 complete native dialogue font planes match every glyph, first/last letter, blank cell and bound. All fit two readable lines and all previews were visually inspected. All18340 wrapper dispatch cases remain unchanged.
-120 guarded warm/cold native copies across block9 and its boundaries, seven rejection controls and final release guards pass. The clean-input patch reconstructs the entire ROM byte for byte.

Six terminal6501-frame cold boots pair V753/V754. Declared fixtures change only an original town trend pair and SDK seed, selecting actual runtime product categories. Static resource category byte6 differs from some initialized objects; fixtures therefore read the actual product category byte exactly as original5FC40 does. Products14/38/75 yield Seasonings/Precious Metals/Medicine. Six complete4600/4800 holds match every glyph and blank-paper pixel. Every outside pixel, including the compact Cond. Shop/Metals Shop/Med Shop captions, portraits, borders and palettes, matches baseline. Entire resident cache blocks are exact. All51 complete menu/return/control pairs match without phase masking. Other15 argument classes have native font/caller coverage, not claimed physical visits. Exact UI RNG draw count and earned trend creation are not claimed.

An ordinary4000-frame New Game cold boot uses no save or fixture and matches all seven V753 frames through intro, captain selection and story. Protected original and disposable donor saves retain their original hash. These are targeted emulator tests, not a hardware test or full-route playthrough.

## Artifacts

- Candidate: `out\all_routes_combined_v754_candidate.nds`
- SHA256: `a44acfb6431fd2ec48e1ae5b5899ddbf1744bcac8a68e1ca6c5ec1fbc14fd246`
- Profile: `all-routes-unified-v754` (experimental)
- Patch: `out\all_routes_combined_v754_candidate.xdelta`
- Patch SHA256: `38bd22b2571c2c60e74bd3fb9cc0bdaab47f04071fba3ed822996f88e79f501f`
- Clean input SHA256: `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`
- Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Changed internal file: `/COMMON/MESFILE.DK4`; ARM9 changes are the owned lookup code/data, three Fleet-label pointers and730 native offset.

ROM/patch, exact reconstruction proof, native evidence and labeled fixture screenshots are on E. No live producer/harness/config dependency was edited. The initial owner count was corrected to the actual three Fleet owners; Dock B has no word-pointer owner. An internal branch inside the old helper is explicitly accounted for. Earlier research files without these completed guards are superseded. Canonical promotion still requires explicit user acceptance.

## Next work

Continue Market750-752,754-761 and767 onward, including false stock/referral placeholders; then wider shared prose, Lil and every other route. The source packet being closed here is only one part of the editorial goal. Graphics audit/original18 objects, Online exclusions, preserved brown marks and later older-record follow-up remain unchanged.
