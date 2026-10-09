# Combined V170: Pick Cargo and Pick Ship

2026-10-04. V170 is the latest **experimental** combined candidate. The cargo and
ship selection captions now have complete natural English in both frame copies.
All eighteen previous labels, other translations, ARM9 and repair stages remain
exact. The full goal is incomplete; canonical acceptance and final commit/push remain.

## Source meaning, boundary and complete words

| Japanese | English | Meaning | Source lettering rectangle | Complete phrase width |
| --- | --- | --- | --- | --- |
| 積み荷選択 | Pick Cargo | Select cargo | `[208,32,256,40]` | 37 of 48 pixels |
| 船選択 | Pick Ship | Select a ship | `[208,40,240,48]` | 31 of 32 pixels |

Both English phrases retain the explicit selection action. The source bitmap
clearly separates its rounded input-field ornament (x<=207) from lettering cells
beginning at x=208. Earlier exploratory x=206 rectangles included chrome and were
never inserted into a candidate. Correct ownership preserves every original
input-field pixel at x=181..207,y=30..47. The source cargo cell has indices
0/6/9, and the ship lettering cell has 0/4/5/6/9; these include original text faces
and shading. Only the two lettering cells are restored to their index-zero backdrop.
All adjacent borders, the complete input field and unowned art remain exact.

Both phrases use the existing complete seven-row authored bitmap face with
original gold index 9. No glyph ink is cropped or resized; first letters of both
words and final letters remain complete. Both words retain a three-column blank
separator. The ship phrase leaves column 239 blank before the existing Done cell
at x=240, with its original lettering unchanged. Every eighth/bottom row is blank.

The first preview used the face's default word spacing, making Pick Ship occupy
all 32 columns and putting its last ink against the adjacent Done cell. It was
rejected before any ROM build. The new explicit `compact_word_space_width: 1`
uses one blank space cell plus the two ordinary separating columns; all glyphs
remain exact. Older labels retain their default spacing. The bitmap builder and
font layout enforce one to three blank space columns. This is a baked-image
option; runtime font/text code is unchanged. The modified builder reproduces
**the complete V169 ROM byte-for-byte**. Evidence:
`work/analysis/v169_word_space_builder_reproduction.json`.

## Verification and limits

**139 focused graphics tests pass**, including fifteen new tests. New checks reject
missing first letters in either word and missing final letters, verify three-column
word spacing and the clear Done boundary, preserve the input field and eighteen
prior records, reject invalid word-space widths and the rejected trial's packed
shape, verify both supplied native crop descriptors, and preserve the entire profile
and inherited terminal stages. Builder, compact font module, script and tests pass Ruff.

Independent glyph-row layout and direct packed-nibble decoding verify all five
compact captions. Native glyph lookup/draw proofs retain all fifteen earlier
native-font labels. The real generic crop constructor checks supplied 48×8/32×8
caption cells, source owner/origin, ABI and memory guards; controlled source-header
sizing confirms 256×256. Actual parent callers, live crop coordinates/contexts,
loose/embedded loading, palette banks/GPU alpha and controller/gameplay remain
pending. Controlled crop inputs and storage proofs do not clear every game screen.

`/GRP/CMMNIMG.DK4` block 5's right half exactly matches the translated frame.
Its left half, all 83 palette banks, header/flags, other blocks and extent remain
exact. Full source/English previews and the embedded bank-zero view were reviewed.

- `work/qa/frame_cargo_v170/review.png`
- `work/qa/frame_cargo_v170/english_embedded_bank_zero.png`
- `work/qa/frame_cargo_v170/boundary.png` (cyan line marks x=208)
- `work/qa/frame_cargo_v170/source_context.json`
- `work/analysis/frame_cargo_v170_artwork.json`
- `work/analysis/frame_cargo_v170_native.json`
- `work/analysis/frame_v170_saved_proof.json`

## Exact candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out\raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V169 comparison and exact reproduction | `3a8df5e28429281c476c56742de585d0ebf6fd5303f959d2de4ba1b35194ab34` |
| Candidate: `out\all_routes_combined_v170_candidate.nds` | `57ea4b89b889c87f4656d5e286a372dc85bc260051e70cc4ac14762fb63c69a6` |
| ARM9, exact V169 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Release registry at build | `e81a045a544ab7f773a7400b13d6495cd515b517da7f4e4c2adae04efbb36466` |
| Registered builder | `9bc8fcd0f84a086abe0b8d5e4ee07217f1e18cb9a68a6062c8da4d55ed1d3878` |
| Compact font module | `c863f19a0e1480b612e01cdc328564f05a6ad0791e5a1216b5d1e6aa3411692f` |
| Compact glyph shapes | `1f34962fa7ff25491a84dc488219d6e18727654f51fdcfdefbb201b95a0e4b7d` |
| Patch: `out\all_routes_combined_v170_candidate.xdelta`, 775284 bytes | `d334dd81f8b5566c4e64344f211430bdc05347f27cbdf0e7c136516e574c919b` |

Profile: **all-routes-unified-v170**, experimental. The registered builder applies
the immutable canonical base and all inherited terminal stages. Accepted layers
are baked into canonical; zero additional accepted batches are required. There
are **452** experimental batches: 450 unchanged and two expanded canonical frame
batches retaining every previous record:

- `translations/frame_action_buttons_graphics_v6.json` supersedes v5, preserving
  eighteen exact records and adding these two phrases (20 labels total).
- `translations/frame_action_buttons_cmmnimg_sync_v6.json` supersedes v5, preserving
  original archive/block locks and ID while synchronizing the expanded image.

Older batches/profiles remain reproducibility records. The adjacent
`out/all_routes_combined_v170_candidate.manifest.json` records the complete stack,
baseline/registry identity, changed files/records, relocations and all build checks.
Against V169, **only `/_pxl/__frame.pxl` and `/GRP/CMMNIMG.DK4` differ**.
The 25 canonical changed paths retain their membership:

`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/CMMNIMG.DK4`, `/GRP/SLACKIMG.DK4`, `/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/__frame.pxl`, `/_pxl/deck04.pxl`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`, `/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`, `/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`, `/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`, `/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`, `/evstill/evstill208.pxl`, `/evstill/evstill209.pxl`.

Saved preservation, canonical menu checks, complete V169 reproduction and exact
clean-ROM patch reconstruction pass. Every other component/resource, prior text,
code, graphic, relocation and changed-record set remains exact.

Before acceptance, cold-boot without a savestate. Check title/New Game, captain
selection/name entry, an established story, town UI and all inherited
item/Advice/Gallery/treasure/fleet/village/button/score screens. Check Pick Cargo
and Pick Ship in their actual selection contexts: complete words/spacing, full
input-field border, gold color/alpha, correct cargo/ship choice and controller
behavior; recheck all eighteen earlier labels, especially neighboring Done.
Explicit user acceptance is required before canonical promotion.

## Full goal remaining

COMMON remains 245 Japanese selections / 133 physical owners needing actual
consumer/layout integration. ARM9/UI classification, names/source fidelity,
Reports/Sailing Help persistence, BGM audio/input, downloaded states and full
gameplay remain. Thirteen historical graphics resources still contain other
Japanese, including date fields/other frame art, marker symbols, title/online/FLS
graphics, CMMNIMG left-half lettering, the embedded title copy and unclassified art.
Actual consumers/crops and image 207's clipped source mark still require review.
Final packaging/progress, canonical acceptance and GitHub commit/push remain. On
full goal completion, retain the requested note to revisit older record-based checks.
