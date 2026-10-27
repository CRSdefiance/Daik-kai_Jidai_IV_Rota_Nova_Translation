# Reveal comic research toward V185

2026-10-04. Research only; no V185 profile, playable candidate or approved batch.
V184 remains the latest verified combined ROM. The full graphics goal is active.

## Exact source

Canonical `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
`/GRP/SLACKIMG.DK4` block19 SHA-256
`c95b9d4b968638d488158c8971c03f4116ac6e6ceb8a6863a4de5a1b05b54464`.
Frame7 is an inspected 320x240 BGR555 storage interpretation; native partition,
loader/crop/palette/GPU/display/input/gameplay remain unproved.

## Source-mask and background evidence

`work/qa/reveal_comic_v185/source_analysis.json` pins the exact frame SHA and
5,425 green candidate ink seeds. The full source/mask and enlarged horn overlap
were inspected. Green seeds visually follow the large decorated lettering and
do not visibly mark the horns, blue body, waves or people. This does **not** prove
a complete restoration mask: dots, outlines/fringes, false positives and every
foreground pixel still require review and independent source-word preservation.

Paper background words from the top strip are cream22396 (28,27,21) and
pink19992 (24,16,19). Exact word-to-word adjacent transitions found zero seams
because the boundaries are antialiased. An antialias-aware color classification,
excluding a three-pixel halo around candidate green seeds, found **71 visible
boundary samples** and six top transitions. Line fits are saved with actual
samples, residuals and support counts. They are hypotheses for restoring paper
under old lettering, not native proof or exact hidden-pixel recovery.

| Top intercept | Slope | Samples | RMS pixels |
| --- | --- | --- | --- |
| 52.71 | 0.4696 | 6 | 0.232 |
| 100.85 | 0.2700 | 4 | 0.137 |
| 145.00 | 0.0000 | 6 | 0.000 |
| 181.72 | -0.1742 | 7 | 0.225 |
| 230.20 | -0.4354 | 10 | 0.186 |
| 289.03 | -0.7241 | 16 | 0.286 |

The second fit has low support and may be biased by surviving interior dots or
other occlusion. Do not encode these six lines blindly as exact geometry. Review
the samples against original clear paper, improve the uncertain fit, and account
for rays entering the side boundaries below the top strip. The header still
contains some lettering over water, where a paper-ray model is insufficient.

Evidence: `source_full_size.png`, `source_green_seed_review.png`,
`source_horns_letter_overlap.png`, `paper_ray_fit_review.png` under
`work/qa/reveal_comic_v185/`. No source artwork or V184 bytes were changed.

## Meaning and next implementation

The large elongated ばあ～～ん！ effect announces the sudden creature reveal.
Review its natural English effect wording with panels5/6/8/9 before authoring.
Frame6's small reaction is legible, but the two yellow-brown water marks remain
unclassified. A possible kana reading is not enough to erase them or relabel
them as anatomy. Keep their source reading/classification open.

Required before a V185 handoff: complete source reading or evidence-based art
retention; a bounded ink/dot/fringe mask protecting whole horns/body/waves/people;
complete readable English without foreground occlusion; full final source/English
review; negative first/final-letter tests and independent original-art tests;
final whole V184 reproduction after any shared renderer change; cumulative batch
replacement in the existing 463-layer stack; registered build, manifest, saved
content verification, exact patch reconstruction and updated progress. Actual
native/gameplay gates and all earlier source-fidelity gates stay open.

Two embedded images (6/7), four Online files, embedded/unclassified/contextual
and broad source/native/visual/gameplay requirements remain. No counts are cleared
by these source-only measurements. Keep the goal active and the user-requested
older record-check follow-up note for eventual full completion.
