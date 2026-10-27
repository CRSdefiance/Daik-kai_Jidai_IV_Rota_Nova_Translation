# Shared item/entity name storage repair

## Status

**DTCM storage rejected; do not integrate these research binaries.** Native
scratch-image constructor `0xCAA4C` creates a 256×12 four-bit image whose pixels
occupy `0x027E0000`–`0x027E0600`, overlapping the proposed persistent names.
`scripts/probe_name_pool_scratch_conflict.py` executes that actual constructor
and the native scratch text path at `0xCA780` through its draw return. A two-
letter input causes 173 native writes and changes 61 bytes of loaded name text.
The exact writes and hashes are saved in
`work/analysis/name_pool_scratch_conflict_proof.json`.

The clean section's zero bytes were scratch contents, not proof of exclusive
ownership. Earlier allocation/ownership wording is therefore superseded. Startup,
getter and pixel comparisons remain useful isolated evidence but do not prove
persistent runtime safety. Keep reviewed full English and native consumer work;
allocate permanent text outside this scratch image and SDK-owned state, then
repeat the complete checks. V147 and the canonical baseline are unchanged.

Connected shopkeeper raster proof now passes all 20 cases. Actual raw-image
header initialization at `0x10DD0C` produces a 4-bit image with pitch 116
halfwords (464 pixels) and height 96, backing the 256×24 bitmap view. Mode five
means a direct raw-image pointer here; the earlier tile-bitmap description was
incorrect and is superseded. Native text-context setup, virtual name getter,
buffered text dispatch and ASCII glyph painter execute together. All pixels
match independent font-mask decoding, including the native trailing blank glyph.
Pixel guards, raw header and bitmap descriptor remain exact; writes are bounded
to owned pixels and the stack/context.

All ten two-row panels in `work/qa/square_shopkeeper_native/native_sheet.png`
have been visually reviewed: complete leading S/final r, no clipping, no row
overlap. Review scope is recorded in the saved context proof. The clear operation
still uses an initially zero image contract. Actual scene eligibility and
physical gameplay remain open; V147 is unchanged.

Twenty native paired-character name preparations now pass for indices 82–91
in both rows. `scripts/probe_square_shopkeeper_name_context.py` executes SDK
loading/BSS clearing, ordinary constructor/getter, native bitmap construction,
text context setup and actual virtual given-name callers. Actual geometry is a
256×24 mode-five tile bitmap, with origins x0/y0 and x0/y12. Complete English is
102 pixels under the configured six-pixel ASCII advance and is received intact
at the draw-call boundary. Evidence:
`work/analysis/square_shopkeeper_paired_name_context_proof.json`.

The bitmap-clear operation is contracted, characters assigned to dialogue fields
are fixtures, and the second-row given-name branch is selected explicitly.
Tile raster, physical composition and actual scene eligibility remain open;
formatting gates are still false. This is not visible-pixel approval.

The joint pool now uses 1,480/1,540 aligned bytes: the eight inherited
`Shopkeeper` references at ordinary indices 84–91 have been source-reviewed as
complete `Square Shopkeeper`, retaining the Japanese location. Each clean
pointer is independently checked against `広場の店主`; the natural-v2 review is
saved in `translations/shared_square_shopkeeper_name_review_v1.json` with the
formatting gate still open. Old-address scanning uses inherited string extents,
so expanded English cannot misclassify adjacent original owners.

`prepare_square_shopkeeper_names.py --joint` composes the original two duplicate
owners at indices 82/83 onto that repair. The combined research now returns
`Square Shopkeeper` for all ten indices 82–91, preserving the other 197 ordinary
given names and all 239 loaded joint-pool references. The complete DTCM section
remains intact after startup/BSS and getters. The only Japanese given names
remaining in this inspection range are indices 61 and 77. Combined output:
`work/analysis/joint_square_shopkeeper_research_arm9.bin`; evidence:
`work/analysis/joint_square_shopkeeper_native_proof.json`. Twenty-nine targeted
tests and lint pass. V147 is unchanged; visible layout and strict integration
remain pending. Earlier 1,472-byte counts describe the pointer-only revision.

Actual global item-object initialization `0xCBE68`–`0xCBED4` now executes for
all 218 20-byte objects. Every object owns vtable `0x0213C38C`, whose name slot
at +8 selects `0x0204A53C`. Two item-specific caller segments (`0x1C7CC` and
`0x1C91C`) then execute the real global-root getter, index calculation, interface
loads, BLX dispatch and name getter, for 436 cases total. All complete strings,
returned pointers and stack positions match. No caller/getter/initializer code
was changed. These are context-name selection paths; downstream raster output
and full context selection upstream of the tested segments remain open.

Latest evidence extends the repair to 239 fields: the original 238 plus the
map's `Monster` alias at `0x705E8`, discovered by an all-byte reference scan.
All 218 actual item index/name getter cases and all four native map-label
selection cases pass in the SDK-loaded/BSS-cleared machine. Items 188–217 are
mutable names. Their actual initializer `0x102AD0` builds all 30 runtime pointers
to object-owned 32-byte buffers; the getter then preserves complete alternating
ASCII/CP932 input names. All ten metadata pairs copied by initialization are
verified, and native writes are guarded to stack, pointer fields and metadata.
Only the serialized input load at `0x46858` is a fixture. Save/new-game input
producers remain open. The first 188 getters use the real fixed catalogue;
separately, all 218 static catalogue selector cases pass with flag zero.
The earlier seeded late-catalogue proof did not model native initialization
and is superseded. The immutable code spans match the clean source.

`scripts/audit_joint_name_pool_references.py` scans the entire serialized ARM9
and the one decompressed ARM9 overlay for starts, interiors and allocation-range
addresses. After repair only two unaligned cross-word matches remain. Both are
exactly clean-source instruction/data bytes, recorded with their byte locks;
there are no unclassified residual matches or overlay matches. This proves
explicit address coverage for these known owners, not computed-pointer or
runtime-write coverage. The following 238-reference account describes the
initial repair before discovery of the extra alias.

Research only. The playable V147 ROM and canonical baseline are unchanged.
This extends the entity-pointer investigation to the overlapping item allocation.

## Ownership and repair

The original item allocation begins at file offset `0x171E48`, 24 bytes before
the original DTCM section at `0x171E60`. Its complete text crosses that section
boundary. The entity pool begins at `0x1720A8`, inside the item's unused tail.
An ITCM extension therefore invalidates a simple file-address interpretation of
these names; a complete item string can also cross two runtime sections.

The original clean DTCM section contains 1,540 zero bytes followed by a 92-byte
SDK pointer table. The two inherited batches supply 37 item and 80 entity string
owners, referenced by 45 and 193 pointer records respectively. Repacking every
complete owner at four-byte alignment uses 1,472 bytes. All known references now
target actual runtime addresses beginning at `0x027E0000`. The 68-byte spare tail
is zeroed, and the final SDK table is preserved exactly. No wording is changed.
All other ARM9 bytes, including ITCM and the old pre-DTCM item fragment, remain
exactly as in V147.

## Evidence

- `scripts/probe_joint_name_runtime_pool.py` pins the V147 ARM9 hash, validates
  original allocation ownership, inherited pointer fields and complete strings.
- Actual native SDK autoload copying and startup BSS clearing execute. All 238
  selected strings remain complete afterward.
- All 207 ordinary given-name constructor/getter fixtures return their exact
  table pointers and printable complete text; all DTCM bytes remain intact.
- `work/analysis/joint_name_runtime_pool_proof.json` records owners, moves,
  hashes, allocation sizes and native getter results.
- `tests/test_joint_name_runtime_pool.py`: five passing checks cover complete
  aligned strings, exact preservation and rejection of altered parent, original
  allocation or SDK table. Ruff passes.

## Remaining gates

Map computed references and other runtime writes, including save/new-game
mutable-name input producers. Execute downstream item/name display paths. Verify
name bounds, full leading/final glyphs, and physical gameplay. Review inherited
wording and remaining Japanese names separately. The square-shopkeeper repair
has not been combined with this research output. Build and verify the complete
registered release stack only after these gates are satisfied.

Cache-maintenance instructions remain a hardware contract in the emulation;
this evidence is not a complete boot or gameplay test.
