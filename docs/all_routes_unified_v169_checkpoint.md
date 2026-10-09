# Combined V169: miniature Done, Rank and Cancel

2026-10-04. V169 is the latest **experimental** combined candidate. Three more
miniature shared frame captions are English in both atlas copies. All fifteen
V168 labels, translations, ARM9 and repair stages remain exact. The full goal
is incomplete; canonical acceptance, final packaging and commit/push remain pending.

## Meaning and original cells

| Original | English | Meaning | Lettering rectangle | Complete word width |
| --- | --- | --- | --- | --- |
| 終了 | Done | Finish the current selection | `[240,40,256,48]` | 16 pixels |
| 等級 | Rank | Grade/rank heading | `[184,48,207,56]` | 16 pixels |
| キャンセル | Cancel | Cancel the current selection | `[208,48,249,56]` | 22 pixels |

The exact original bitmap supplies these meanings. Done is the natural completion
action; Rank retains the original grade/rank meaning; Cancel retains cancellation.
Actual runtime contexts still require native parent mapping.

The cells are eight pixels high. The original runtime ASCII face has nine visible
rows, so a new authored **compact-en-7px-v1** bitmap face supplies seven complete
rows with one blank separating column between letters. All letters are complete,
with one blank bottom row in each original cell. Original gold palette index 9 is
retained. No native letter is cropped, compressed or replaced in the runtime font.
The new face is baked into these three graphics only. Its explicit row strings,
supported letters and pinned SHA are in `dk4tool/graphics/compact_font.py`.
Unsupported characters, changed font identity and insufficient cells fail the build.

These three isolated lettering cells have index-zero backgrounds; only their
rectangles are restored and redrawn. All fifteen prior labels, the input-field
ornament, cargo/ship captions, month grid, adjacent borders, unowned art, header,
palette and encoded extent are exact. CMMNIMG block 5's matching right half is
synchronized; its left half, all 83 palette banks, headers/flags and other blocks
remain exact. Native bank selection remains unproved.

Cargo/ship selection captions abut the input-field ornament and contain multiple
source palette indices. Their precise lettering/chrome ownership and actual native
crops require mapping before replacement. Both remain Japanese. Date fields and
other frame art remain. No trial cargo/ship translation was inserted into this ROM.

## Verification and actual limits

**124 focused graphics tests pass**, including nineteen new tests. They reject
missing first/final letters for all three captions, unknown letters/font faces,
wrong font hashes and short/narrow cells; verify complete gold glyphs, seven-row
cells, word widths, clear inter-letter columns and blank bottom rows; preserve
all fifteen previous records and the exact input-field/cargo/ship pixels; verify
the complete profile/stages and three native generic crop descriptors. Builder,
compact font module, new script and tests pass Ruff.

An independent layout decoder reads the explicit seven-row glyph strings and
compares every owned pixel directly against low/high nibbles in the saved four-bit
PXL. Existing native font lookup/draw proofs still cover all fifteen earlier
labels. The new authored face is **not** described as native font output.

The real native generic crop constructor executes for supplied original cells,
checking source owner, origins, full dimensions, ABI and memory guards. Controlled
source-header sizing confirms 256×256. These supplied crop/sizing inputs do not
prove actual parent callers, loose/embedded loading, every live crop/context,
native palette bank/GPU alpha or controller/gameplay behavior. Those remain pending.

Reviewed full source/English atlases and enlarged miniature captions:
`work/qa/frame_select_v169/review.png`; embedded bank-zero storage preview:
`work/qa/frame_select_v169/english_embedded_bank_zero.png`.
Source meanings: `work/qa/frame_select_v169/source_context.json`.
Artwork review: `work/analysis/frame_select_v169_artwork.json`.
Glyph/storage/crop evidence: `work/analysis/frame_select_v169_native.json`.

The updated builder reproduces **the complete V168 ROM byte-for-byte**.
Reproduction evidence: `work/analysis/v168_compact_builder_reproduction.json`.
Saved V169 verification preserves every other resource/component, all prior
translations, stages, relocations and changed-record IDs. Canonical menu checks
and exact clean-ROM xdelta reconstruction pass.
Evidence: `work/analysis/frame_v169_saved_proof.json`.

## Exact build and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out\raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V168 comparison and exact reproduction | `fd04046af8de3343b6017c16c1ef03ac422588d110d8e08d2e8cade87d33aff6` |
| Candidate: `out\all_routes_combined_v169_candidate.nds` | `3a8df5e28429281c476c56742de585d0ebf6fd5303f959d2de4ba1b35194ab34` |
| ARM9, exact V168 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Release registry at build | `725b451aef05ea64efaacb64ceb0d4b4071fc810b60167660cb03de6a8f0822d` |
| Registered builder | `61785e02a447a9276868418eb17e2b3445c7dbd9f3c90c2a6746c806b2a7a5bd` |
| Compact font module | `d013b84f4844f72ec9782fd5eb40458fe6f09c4cb1aa1c3105085e667dda1b82` |
| Compact glyph row identity | `1f34962fa7ff25491a84dc488219d6e18727654f51fdcfdefbb201b95a0e4b7d` |
| Patch: `out\all_routes_combined_v169_candidate.xdelta`, 774880 bytes | `bfe314e59c9c2b1f2bc181327cee83593d35dfeb69b619007edbe09b429a39dd` |

Profile: **all-routes-unified-v169**, experimental. The integrated builder applies
the immutable canonical baseline and all inherited terminal stages. All accepted
layers are baked into canonical; zero additional accepted batches are required.
There are **452** experimental batches: 450 unchanged and two expanded canonical
frame batches retaining every earlier record:

- `translations/frame_action_buttons_graphics_v5.json` supersedes v4,
  preserving fifteen exact records and adding three miniature captions (18 total).
- `translations/frame_action_buttons_cmmnimg_sync_v5.json` supersedes v4,
  retaining original archive/block source locks and ID while syncing the expansion.

Older batches/profiles remain reproducibility records. The adjacent
`out/all_routes_combined_v169_candidate.manifest.json` records the complete stack,
base/registry identity, changed paths/records, relocations and build checks.

Against V168, **only `/_pxl/__frame.pxl` and `/GRP/CMMNIMG.DK4` differ**.
The 25 canonical changed paths retain their membership:

`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/CMMNIMG.DK4`, `/GRP/SLACKIMG.DK4`, `/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/__frame.pxl`, `/_pxl/deck04.pxl`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`, `/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`, `/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`, `/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`, `/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`, `/evstill/evstill208.pxl`, `/evstill/evstill209.pxl`.

Cold-boot without a savestate before acceptance: check title/New Game, captain
selection/name entry, an established story, town UI and all inherited
item/Advice/Gallery/treasure/fleet/village/button/score screens. Check miniature
Done/Rank/Cancel for complete first/final letters, spacing/crops, gold color/alpha,
correct completion/cancellation behavior and controller input; recheck all fifteen
earlier frame labels. Explicit user acceptance is required before canonical promotion.

## Full goal remaining

COMMON remains 245 Japanese selections / 133 physical owners needing actual
consumer/layout integration. ARM9/UI classification, names/source fidelity,
Reports/Sailing Help persistence, BGM audio/input, downloaded states and full
gameplay remain. Thirteen historical graphics resources still contain other
Japanese, including remaining frame/calendar/cargo/ship labels, marker symbols,
title/online/FLS graphics, CMMNIMG left-half lettering, embedded title copy and
unclassified art. Actual consumers/crops and image 207's clipped source mark still
need review. Final packaging/progress, canonical acceptance and GitHub commit/push
remain. On full goal completion, retain the requested note to revisit older
record-based checks.
