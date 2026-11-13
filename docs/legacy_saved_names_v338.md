# Legacy saved item names V338

## Observed defect and cause

Ordinary V326 gameplay from an isolated older cartridge save reaches Stockholm's
Guild and shows **宝石を食う宝石の地図１**. The English category and description are
already correct. The exact Japanese title is "Gem-Eating Gem Map 1" under the
existing reviewed item dictionary. The original save contains these Japanese
name fields; normal loading restores them despite the ROM's English initializer.

Native load routine 020102AD0 reads the saved promotional owner, then rebuilds
metadata pointers. Its original instruction at ARM9 offset102AF0 is now a call to
an owned helper, which returns with that original ADD r6,r4,#0x22 executed.
The helper converts only complete exact matches from the clean Japanese dictionary:
10 original item names and their40 numbered map names. It reuses the established
English spellings. All30 fixed32-byte name fields are checked. No match reads beyond
32 bytes, and every known replacement fits with its terminator. Unknown/custom
names, near matches and unterminated fields remain unchanged.

Item identities, selected item indices, inventory, flags, attributes and RNG are
preserved. The original input save is unchanged. No save editing, savestate,
unlock alteration or live RAM injection is used. The older save's earlier gameplay
provenance is unknown; this test does not establish legitimate prior progression.

## Verification

- 53 native cases cover all50 known names, first/middle/final slots, the actual
  older loaded owner, idempotent English and unknown/custom/unterminated fields.
- Writes are restricted to name fields and bounded stack space. Registers, condition
  flags, stack, surrounding guards and every other owner byte pass.
- 100 native rasters check every complete English name in both4-bit and16-bit formats,
  including first/final letters and blank cells within the supplied title geometry.
- Startup copy, cache-line coverage, modeled dirty/stale cache handling, ARM7 sections
  and allocation bounds pass for the expanded owned pool.
- The same-save8200-frame replay shows all246 name pixels,144 category pixels and317
  description pixels. Only770 pixels in the old12-pixel-high title region change;
  all other pixels of that item screen match exactly. The initial11-pixel comparison
  gate was corrected after measuring the original Japanese glyph height, without
  changing artwork or widening the region beyond the actual title row.
- All30 names in read-only actual RAM exports match translation/preservation.
- 34 comparable earlier saved-game frames are exact;81 fresh-game frames across
 31200 frames match V326, including title, character selection, opening, town and
 sailing. Both emulator runs terminate normally without callback errors.
- CompleteV326 reproduces byte-exact. All470 batches and prior stages/records remain.
 Only ARM9 changes. The clean-input patch reconstructs V338 exactly. Focused Ruff passes.

These are targeted automated emulator checks, not a completed route or physical-device
verification. Actual native map paintings, occupied weapons/armor and other graphics
requirements remain open. All18 plaque/hint entries and variants remain incomplete.
Low-resolution Online images remain excluded by user request.

## Integrated experimental candidate

| Artifact | Identity |
| --- | --- |
| ROM | `out\all_routes_combined_v338_candidate.nds` |
| ROM SHA256 | `667d5c3a32a779300f52fae61dc6d3e7aa1c6bbdb87563f941b174167c757fd9` |
| Patch | `out\all_routes_combined_v338_candidate.xdelta` |
| Patch SHA256 | `75b7f6d622ad3c6c2efd5d18196a1691429f3b35473d565c35b4321b36c4ffa4` |
| Profile | `all-routes-unified-v338` |
| Canonical base | `out\raphael_natural_v2_accepted_base.nds` |
| Canonical SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |

Canonical promotion awaits explicit user cold-boot acceptance. Both graphics audits,
the requirements ledger and progress documents record the correction. The full goal
remains incomplete. Revisit older record-based checks at actual completion.

Evidence: `work/analysis/legacy_names_v338/release_proof.json`, `native_proof.json`,
`startup_proof.json`, `name_raster_proof.json`, `actual_loaded_names.json` and the
capture reports for `ordinary_map_v338`, `legacy_names_v338` and
`legacy_names_v338_new_game`. Verifiers: `scripts/prepare_legacy_names_v338.py`
and `scripts/verify_legacy_names_v338.py --live`.
