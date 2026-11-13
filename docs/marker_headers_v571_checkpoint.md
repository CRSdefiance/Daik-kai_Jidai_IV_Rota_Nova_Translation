# V570–V571: complete smaller marker headers

## Source geometry and wording

The smaller marker headers are separate graphics from the standalone banners
repaired in V564/V566. Comparing complete original glyph masks establishes their
source bounds without relying on the historical editing rectangles:

| Source | English | Complete panel | Source Japanese ink | Missed old edge points |
| --- | --- | --- | --- | ---: |
| 一時置き場 | Temp Storage | [184,0,248,16] | [187,1,244,12] | 0 |
| 配布品 | Issued | [168,64,216,80] | [175,66,210,77] | 15 |
| 戦利品 | Spoils | [168,80,216,96] | [175,82,210,93] | 12 |

All 509 white source points match the corresponding original standalone images
at those offsets, including the two leading/trailing columns missed by the old
Issued/Spoils boxes [176,64,209,80] and [176,80,209,96]. The 27 old edge points
were still Japanese white pixels in V569; they are removed by the full repair.
The corresponding 407 source shadow points also map to dark marker pixels.

“Temp Storage” is an unambiguous compact form of Temporary Storage and replaces
the potentially confusing “Temp Store.” Issued and Spoils retain their meanings.
The original game ASCII font supplies complete glyphs with no scaling: five-pixel
advance, three-pixel word space, and only proven blank top rows/last columns
removed. All three captions fit their original panels with margins.

## Material and integration

Visible marker material is preserved. Only the mapped Japanese strokes/shadows
are reconstructed from unlettered original wood in each corresponding standalone
banner. Coherent component patches are selected using visible marker context;
donor colors map to the existing marker palette. All donor hashes and mappings
are recorded. Hidden texture is inferred, not claimed as exact recovery.

| Header | Complete English ink | Visible original material retained |
| --- | ---: | ---: |
| Temp Storage | 143 | 583 |
| Issued | 72 | 468 |
| Spoils | 67 | 477 |

The result changes 993 marker indices. All 282 English ink points and 1,528 visible
source-material points pass. All 83 original palettes, metadata, dimensions and
outer frames remain exact. Outside the three panels, every marker pixel remains
V569, including the corrected Sell/Buy captions, restored bag and gender symbols.
All 65,536 embedded marker indices match the loose marker; the embedded frame half,
block headers and every other archive block remain unchanged.

The registered `all-routes-unified-v571` profile inherits all 470 batches, 114
accepted layers and every V569 stage. Only `/_pxl/__marker.pxl` and
`/GRP/CMMNIMG.DK4` change from V569. All code and other translations/artwork remain
byte-identical. Canonical promotion has not occurred.

- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Candidate: `out/all_routes_combined_v571_candidate.nds`, SHA256
  `4f9e0b8b880590a8918627a02fbc453187f578a8beea3123a2e38fb600f0b23f`.
- Patch: `out/all_routes_combined_v571_candidate.xdelta`, SHA256
  `044a453724aafddd11fbf521c6da3a2c73b37e274dc147fe4a104bee63f0d5fe`.
- Patch input: clean ROM SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The adjacent manifest declares both changed files and the complete stack. The
patch reconstructs the exact candidate from the exact clean ROM.

## Native and regression evidence

Four control/corrected native cases at4300/4600 manually select original marker
crop [168,0,248,96] through the existing renderer. The isolated fixture changes
only ten argument-setup/literal words; it does not substitute artwork files.
Captured views use owner02313F74, source168/0, size80x96, palette0 and flags0.
Original getter020D4170 resolves a resident marker PXL byte-identical to its file.

All 30,720 crop pixels pass, including the complete three captions and surrounding
icons. Two paired full-screen comparisons pass 196,608 pixels. This checks loading
and display under the explicit crop; original header-parent contexts and alternate
palette selections remain unverified. The test screenshots deliberately show an
atlas region in Cargo Setup, not a normal gameplay layout. They are not guide
publication candidates. The source battery save remains unchanged.

A separate ordinary 21,200-frame cold boot passes all 56 unique startup captures
against V569, including the established title/New Game/opening/town schedule.
Ruff passes. This is targeted emulator evidence, not a complete playthrough or
physical-device test.

## Evidence and remaining scope

- `scripts/review_marker_headers_v570.py` and
  `work/analysis/marker_headers_v570/material_and_bounds_review.png`.
- `dk4tool/patch/marker_header_materials.py` and
  `translations/marker_header_materials_v1.json`.
- `scripts/verify_marker_headers_v571.py` and
  `work/analysis/marker_headers_v570/v571_release_proof.json`.
- Native captures on E under `Generated/work/emulation_v193/marker_headers_v571_*`.
- Labeled screenshots and provenance on E under
  `Screenshots/Test fixtures/V571 Marker headers`.

The shared crop fixture preparer now accepts explicit source rectangles and
preserves separate zero palette/flags arguments. It no longer labels a successful
prior fixture rejected when simply reproducing it.

The separate Confirm button remains open. A source-palette comparison against the
two 83-bank atlases found no complete matching palette; that bounded search does
not identify a suitable background donor. Other marker material families, original
contexts and the broader graphics audit also remain open. All 18 original plaque/
hint entries remain incomplete; all 22 historical requirements retain their full
scope. The graphics goal remains active.
