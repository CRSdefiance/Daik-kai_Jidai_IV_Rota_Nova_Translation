# Current Porto Estado artwork review V329

The current ROM remains V326, SHA256
`fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1`.
No ROM, artwork, release profile or patch was changed.

## Source and current visual review

Full source/current pairs were extracted directly from the clean and current ROMs:

- `/_pxl/startmenu0.pxl`, 256x192, ocean background.
- `/_pxl/winframe00.pxl`, 256x192, ship medallion background.
- `/GRP/WINFRAME.DK4` block 0, 320x240, embedded medallion title.

All six complete images were visually inspected at native stored size. The
Japanese 大航海時代IV retains the established localized title Uncharted Waters IV.
The small ポルト・エシュタード caption uses the source's already established gold
Latin name Porto Estado. No new nationality/name interpretation is invented.
The gold PORTO ESTADO lettering, ornate E, surrounding medallion/ocean and
copyright details remain in their original context.

The current words are retained. The ocean restoration uses original title04
water with palette correspondence. The medallion versions use bounded harmonic
reconstruction beneath removed Japanese ink/shadows. Their hidden scenery is
approximate; this review does not claim recovery of unavailable original pixels.
No speculative repaint or new source-transcript claim was made.

## Complete letters and source protection

The verifier independently recreates the pinned font's six complete word planes
from their saved line positions, including the reviewed subtitle word gap.
Their mask hashes match authoring evidence. On the actual current ROM, all
**13,164 quantized ink and outline pixels** match, covering nine text lines.
Every line's whole bounds remains inside its declared edit rectangle.

Eighteen negative checks erase ink from each line's first/final occupied edge;
the complete-plane comparisons reject every erasure. These checks confirm that
leading/trailing ink participates in validation; they do not stand in for a
native viewer or final display test.

Whole source comparisons also verify:

- Original dimensions, palettes, headers, flags and byte extents.
- Every pixel outside the declared edit rectangles.
- Every original gold index and declared protected bevel/adjacent-shadow pixel.
- Every other block of the embedded WINFRAME archive.

The English is complete in storage. Actual legacy loading, parent selection,
scaling/crops, palette/alpha composition and viewer readability remain unproved.
The historical supplied-header/view fixtures are not promoted to gameplay proof.

## Goal and artifacts

Both graphics audits, the requirements ledger and progress documents now record
this source/restoration/lettering review separately from the open native-display
gate. All 18 plaque/hint entries and Armor/Weapon variants remain incomplete.
Legacy viewers, other final-rendering/gameplay requirements remain open. Low
resolution Online screenshots stay exempt by user instruction. The graphics goal
remains active; revisit older record-based checks at its actual completion.

Evidence: `work/analysis/porto_review_v329/inventory.json`, `proof.json`, and
the three source/current PNG pairs. Verifier: `scripts/verify_porto_art_v329.py`;
focused Ruff passes.

### Current stored previews

![Ocean title](<C:/Projects/Personal Projects/g-p-6a676ab5787c819181af4a29d5cebfbc/dk4-translation-tool/work/analysis/porto_review_v329/startmenu0_current.png>)

![Medallion title](<C:/Projects/Personal Projects/g-p-6a676ab5787c819181af4a29d5cebfbc/dk4-translation-tool/work/analysis/porto_review_v329/winframe00_current.png>)

![Embedded title](<C:/Projects/Personal Projects/g-p-6a676ab5787c819181af4a29d5cebfbc/dk4-translation-tool/work/analysis/porto_review_v329/embedded_current.png>)
