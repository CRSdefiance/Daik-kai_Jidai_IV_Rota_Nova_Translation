# Lisbon Guild hover and all town facility captions

Status: registered integrated candidate verified and byte-identical to the tested image. Experimental; user 3DS cold-boot acceptance pending. Canonical and promoted builds remain unchanged.

## Build identity

- Final candidate: `out/all_routes_combined_lisbon_guild_fixed_20261101.nds`.
- Candidate/tested SHA-256: `7470d392590fed3ee70d7301f42d9acdbf500e771e2191c522cec575f3c1cd94`.
- Profile: `lisbon-guild-hover-fix-20261101`, experimental; no promotion.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Complete predecessor: registered V8865, SHA-256 `b1592d88c2031dcfeaeaa5002cacf6998ad7612a894114a68c86c6bc81afc0c2`.
- All 114 accepted layers and V8865's complete 648-entry integrated stack are retained. The repair adds one registered runtime configuration: **649 entries and 19 passing release checks** in the final manifest.
- Manifest SHA-256: `485c008bc53ac5d2e3d05e23086c231c72f9bfcc0c146671a82bef9cd6460ba3`.
- Registry SHA-256: `3fdc022b9da2d3f506e7e7403f3910323d4d22fd1d697ef8a1b3b4da67e0846c`.
- Sibling files: `.manifest.json`, `.handoff.json` and the verified clean-input `.xdelta`.

The canonical builder is byte-exact to V8865. Its historical native contracts freeze its source. `scripts/build_integrated_release_with_runtime_bounds.py` executes that builder unchanged from the canonical base, retains the complete intermediate manifest, then applies the registered source-locked runtime stage. The final image must equal the tested image byte for byte. The intermediate `*_stage.nds` is not a handoff.

Only `/__arm9__.bin` changes relative to V8865. All dialogue, names, shared messages, fonts, artwork, other files and ARM7 remain exact. The manifest retains the complete internal-file change list relative to the canonical base.

## Cause and repair

The original modal text consumer pads an odd ASCII run to two-character cells. A centered five-letter label on the 36-pixel tooltip has origin x3. Its synthetic sixth blank cell starts at x33 and writes three pixels past the right edge. With the retained font's Y+1 placement, its last row reaches the adjacent bitmap header and clears the 4-bit mode field from 4 to 0. The label disappears and town navigation becomes unresponsive. The game CPU still executes its drawing loop; this is not a claim that the CPU stopped.

The source native call reproduces that exact header overwrite for **Guild and Ruins**, in both caption layouts. The other ten labels do not overwrite the header in this test.

`dk4tool/patch/ascii_glyph_right_bounds.py` bounds physical ASCII cell writes by the actual bitmap width, in both 4-bit and 16-bit formats. It retains the text, centering, complete visible glyphs, synthetic blank handling, existing Y+1 offset and vertical bounds. The column count shares an unused byte of the existing row-bound stack word. There is no heap, stack, section or staged-pool growth. Immutable helper code uses the tail of the retired Square scratch, after requiring the existing per-call Square repair. The current source has no absolute aliases or ARM branches into that tail.

## Every town building type

The original caption table has twelve entries. Each passes the complete original caption getter, layout, clear, native font and return path under both original layout branches: **24 repaired native cases**. All complete bitmap pixels match an independent font oracle; headers, helper code and saved-register/stack ABI survive. Every visible first, internal and final letter is present. Only the out-of-bounds synthetic blank is clipped.

| ID | Existing English label | Building type |
|---:|---|---|
| 0 | Square | Square |
| 1 | Market | Market |
| 2 | Yard | Shipyard |
| 3 | Port | Port |
| 4 | Tavern | Tavern |
| 5 | Guild | Guild office |
| 6 | Palace | Palace |
| 7 | Govt | Governor's office |
| 8 | Inn | Inn |
| 9 | Ruins | Ruins |
| 10 | Church | Church |
| 11 | Gate | Town gate |

This is initialized native CPU evidence for all twelve types and both caption layouts, not a claim of natural visits, GPU captures or complete service effects for every town. Existing wording and regional icon art are unchanged.

## Actual gameplay and regressions

- A 17,300-frame automated DeSmuME cold boot uses an isolated copy of the existing V470 Lisbon battery save. No savestate, observer or new RAM/code/gameplay fixture is used. The original donor remains unchanged.
- Port, Square, Palace, Tavern, Market, Inn, Guild and Yard each have complete actual hover masks. All eight available Lisbon facilities are entered and returned from. Guild displays its full label, permits moving away, opens the Guildmaster's dialogue and returns normally.
- Nine complete pre-failure control frames equal V8865. All 4,096 helper-section bytes survive the final town run, apart from the original owned mutable footer-cache word.
- A separate fixture-free 4,001-frame Hodram New Game covers title, character confirmation and established opening dialogue. Six complete startup frames equal V8865.
- 1,728 native glyph cases cover both bitmap formats, right-edge/fully-outside positions, multiple heights, origins, descenders and blank cells. Every clipped pixel, image header, canary and saved-register/stack ABI passes. The exact original Guild header becomes 0; the repaired header remains 4.
- All 18 Square shop captions retain exact complete pixels and all helper code. The earlier 128 font-bound cases and complete native footer checks also pass.
- Relevant release/translation/ASCII-guard/pair-phase regressions: 48 passed.
- Both the 24-label sheet and all sixteen Lisbon entry/return captures were directly viewed.

Evidence lives under `../tmp/lisbon_office_fix/`, including `all_town_facility_captions.json`, `actual_gameplay_proof.json`, `native_bounds/proof.json`, `Square_18_regressions.json`, `helper_reference_audit.json`, the capture reports and the two review sheets. Historical failures and source artifacts are preserved.

The required retention preview keeps the repaired candidate, V8865 and the emulator's V189 integrity baseline. Its proposed 210 deletions were **not applied**: a bounded active-source/proof census found references to at least 117 deletion targets before reaching its 15,000-file review limit. Those research dependencies need a separately completed pin audit before any pruning. No ROM was deleted by this task. The repaired candidate is explicitly pinned.

## Patch and hardware check

The clean-input xdelta is independently decoded to the complete tested image:

- Clean input SHA-256: `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- Patch SHA-256: `c4270cbd5e500fc745d3930ef7ed862c3557388f0a4fb3fe9e64de1ccf1f9add`.
- Reconstructed image SHA-256: `7470d392590fed3ee70d7301f42d9acdbf500e771e2191c522cec575f3c1cd94`.

The final registered ROM and patch remain experimental until the user cold-boots them on the 3DS and checks the Lisbon save. Automated emulator and native CPU checks do not establish hardware verification or a complete game playthrough. Canonical and promoted builds are unchanged.

Reproduce the registered build with:

```text
python scripts/build_integrated_release_with_runtime_bounds.py --profile lisbon-guild-hover-fix-20261101 --out out/all_routes_combined_lisbon_guild_fixed_20261101.nds --work work/analysis/lisbon_guild_hover_fix_20261101_build
```

Use a fresh output/work folder for a new reconstruction; never overwrite an existing test artifact.
