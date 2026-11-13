# V725: embedded copy consistency and contextual icon review

This is a current stored-art audit of V712. It adds no ROM change or emulator
run. V724 made progress by verifying the two current generic image widgets.

## Complete indexed-copy comparison

All 57 blocks in the six GRP archives retain their clean-source extents. The
type-16 decoder identifies 31 images in 30 blocks, including both concatenated
portraits in CMMNIMG block 1. Each image retains its complete source header,
palette, flags and dimensions.

Pairing uses the complete clean pixel plane, dimensions and bit depth. This
finds 19 complete loose counterparts. Every current embedded pixel plane equals
its current loose counterpart, including both translated name/button resources.
No stale Japanese counterpart was found in this defined matched set.

The original palettes are preserved separately:

- Sixteen counterpart palettes are identical.
- The name atlas and button prompt differ only in original bit-15 flags.
- The CHARA block-0 palette differs from its loose counterpart in the original
  game. Both complete palettes remain exact to their respective clean sources.

Neither palette format was normalized to force equality. Pixel-plane equality
alone does not establish native bank selection or transparency equivalence.

The three separate palette/pixel pairs also retain their complete palettes and
pixel headers. CMMNIMG's entire 512 by 256 plane consists of the two complete
current Marker and Frame halves: 65,536 exact indices each. This covers the
embedded gender cells and all translated Frame controls as stored graphics,
without claiming an original embedded display consumer. Both complete MAPPOINT
pairs remain byte-exact to clean source.

## Unmatched image and environmental review

All twelve type-16 images without a complete loose counterpart were opened
beside their clean sources, across six native-resolution comparison sheets:

- Four portraits: two BUSTUP images and the two concatenated CMMNIMG portraits.
- The dark ship backdrop and blank wooden plaque backdrop.
- The translated Porto Estado title, with complete English wording; its native
  scene relationship remains the separate historical open requirement.
- The original Latin PORTO ESTADO medallion, two blank panel backgrounds,
  original KOEI logo and original English HOIST THE SAILS! graphic.

The eleven untranslated images are source-exact and contain no Japanese caption
to replace in these reviewed planes. The already localized Porto title remains
unchanged. No new translation defect was identified.

Two additional sheets show every MAPPOINT palette bank: twelve for blocks 0/1,
nine for blocks 2/3. The first atlas is architectural, nautical and heraldic
decoration. The second includes East Asian building signs and a painted lantern.
The new evidence-based decisions retain these physical setting marks, without
inventing English shop identities from indistinct source strokes. The lower
resolution four-bit icons are not exact copies of the eight-bit kbj sprites;
neither pixel equivalence nor a shared native consumer is inferred.

See `translations/contextual_embedded_graphics_decisions_v725.json`. The retained
marks have no independent instruction or menu-caption role established by this
stored-art review. Native facility captions and original consumer identification
remain distinct requirements.

## Limits and audit integration

All eight sheets were visually reviewed. Storage images do not establish native
loading, alpha, palette-to-cell assignments, screen crops or gameplay. The other
raw and animation blocks are outside this type-16 and separate-palette decoder;
their existing evidence and unresolved consumer requirements are retained.

These completed current-copy consistency and contextual-icon source decisions
leave the routine active queue. Ordinary legacy consumers, comics, village
triggers, small-control states and final verification remain open. All eighteen
original plaque/hint objects remain incomplete and all twenty-two historical
requirement objects remain exact. The four Online body exclusions, accepted
materials, approved marks and later older-record follow-up are preserved.

V712 ROM, manifest, patch, registry and canonical hashes are unchanged. The V724
matrix is preserved before updating the current matrix. No canonical promotion,
new playable candidate, commit or push is made.

Evidence and eight comparison sheets are archived under
`E:/Rota Nova translations/Screenshots/Audit comparisons/V725 Embedded copy consistency`.
These are derived storage reviews, not gameplay or guide screenshots.
