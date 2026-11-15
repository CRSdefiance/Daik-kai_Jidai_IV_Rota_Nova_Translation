# V502 town stock rendering and movie allocation repair

Status: experimental, verified in targeted cold-boot emulator tests. No canonical
promotion. The full graphics goal remains active.

## Release identity

- Candidate: `out/all_routes_combined_v502_candidate.nds`.
- Candidate SHA-256: `f26a930d91f0df2089a080f0945b9f06a3d1f9718f18a39a6e6dca7edc8842bc`.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`.
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile: `all-routes-unified-v502`.
- All114 accepted layers and all470 inherited batches/stages remain. The complete
  batch/stage identities are recorded in the neighboring candidate manifest.
- Added experimental stage: `translations/town_stock_rows_v1.json`.
- Against V484, only `/__arm9__.bin` changes. All675 PXL/FLS files and every other
  ROM component remain byte-identical, preserving the inherited921 decoded assets.
- Patch: `out/all_routes_combined_v502_candidate.xdelta`, built against
  `work/clean.nds`, SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
  Reconstruction reproduces the complete candidate byte-for-byte.

## High-level repair

The inherited town helper permanently allocated15104 bytes and redirected the
shared numeric bitmap away from its original VRAM backing. V486/V492 controls
showed that additional allocations could suppress the M28 name-card fixture.
Freeing that bitmap around movie startup caused a separate late Help crash;
those earlier candidates remain rejected.

V502 restores the original numeric binding, header height72 and VRAM pixels at
0601BFC8. A stock update captures up to five existing English name pointers. When
the native town view is composed, each name is rendered into one temporary96x16
four-bit stack bitmap, then its original12-row visible crop is copied immediately.
No persistent allocation or free is introduced. All124 name strings and their
metadata remain exact. The longest19-character names fit at five-pixel advance.

The live unfiltered trace V498 established destination023117AC, virtual
composition routine020CFC14 and the original town viewport. Its screen selector
is1 and its origin is(8,0). Earlier prototypes had assumed selector0, drawing to
the other framebuffer. V502 reads the original selector and origin fields instead
of substituting its own. It also uses the original image-binding constructor with
zero color flags; a prior constructor's stack argument had overlapped its header.

Implementation: `dk4tool/patch/town_stock_rows.py` and `.asm`. The builder applies
the source-locked stage after the inherited V484 stack. All autoload extents,
startup/cache wrappers and other sections remain exact. Reclaimed instruction
tails belonged to the abandoned lazy allocator; every current commodity string
is checked separately for byte preservation. The price painter remains intact.

## Verified scope

- Four native combinations of12/16-pixel font cells and original screen
  selectors0/1: all124 complete masks, first/final characters, blank cells,
  cache bounds, fallback behavior and register/stack restoration pass.
- Genuine Istanbul cartridge save: all62 upper-town captures match V484 exactly;
  all three stock captions and four Square selection states retain complete text.
- Rafael's ordinary New Game: all56 full title/story/town/help captures through
  frame21200 match V484 exactly. This includes Lisbon's five visible stock labels.
- A labeled name-pointer rendering fixture displays complete Black Glacier Sword,
  North Sea Ambergris and Fire and Ice Rubies at the actual right-hand boundary.
  All641 ink pixels and blank cells match. This does not prove normal availability
  or acquisition of those goods.
- M28 substituted into M20: the full3047-pixel Hodram name plane matches at3700.
  This restores the previously failing controlled fixture; normal ending invocation,
  unlocks and all remaining movie planes still require their own evidence.
- The registered ROM is byte-identical to the normal prototype used in the
  captures. Screenshot provenance records both paths and that exact identity.

Four lower-screen samples differ from the V484 run: one Trends focus flash and
three complete shopkeeper responses already present in unchanged COMMON data.
All differences are confined to those regions. Their exact timing/selection cause
is not claimed. Native glyph masks verify the current responses in full.

The older Ottoman response uses x16 on its first line and x22 on its continuation.
Its script bytes are unchanged by V502. Retain this concrete example for the
requested revisit of older record-based checks at actual goal completion.

## Evidence and handoff

- Verifier: `scripts/verify_town_stock_rows_release_v502.py`.
- Release proof: `work/analysis/town_stock_rows_v502/release_proof.json`.
- Current preservation proof: `work/analysis/town_stock_rows_v502/preservation_proof.json`;
  all921 per-asset witnesses inherited through exact verified container bytes.
- Exact reconstruction: `work/analysis/town_stock_rows_v502/reconstructed.nds`.
- Native proofs: `work/analysis/town_direct_labels_v501/native*_proof.json`.
- Guide captures: `guide/screenshots/istanbul-stock-and-square-v502.png` and
  `lisbon-five-stock-labels-v502.png`; normal gameplay only.
- ROM, patch, manifest and finalized screenshots are published to the configured
  `E:\Rota Nova translations` destination with every copied hash verified.

Manual cold-boot acceptance still needs the title, New Game, normal town entry,
Help and ordinary movie playback on the user's emulator/device. These are targeted
automated emulator tests, not a whole playthrough or hardware verification.
All22 historical requirements and all18 incomplete plaque entries remain in the
audit; V502 does not mark the full graphics goal complete.

## Additional current-candidate coverage

V503 verifies the two edited M28 title/logo planes and all19 distinct progressive
name images from20 texture entries in the same V502 rendering code. See
[M28 coverage](m28_progressive_v503_checkpoint.md). Normal ending invocation and
other unverified movie scopes remain open.
