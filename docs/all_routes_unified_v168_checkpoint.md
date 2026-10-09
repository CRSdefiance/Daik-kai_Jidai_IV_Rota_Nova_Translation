# Combined V168: Type, Price % and Arrival

2026-10-04. V168 is the latest **experimental** combined candidate. Three more
shared frame headings are English in both copies. All twelve earlier labels,
other translations, ARM9 and repair stages remain exact. The full goal is incomplete.

## Translation and complete glyphs

| Original | English | Context | Original lettering rectangle | Color index |
| --- | --- | --- | --- | --- |
| 種類 | Type | Category/type heading | `[195,1,222,16]` | 9, gold |
| 相場% | Price % | Market price expressed as a percentage | `[184,18,220,29]` | 9, gold |
| 入荷月 | Arrival | Stock-arrival month, above the original 1–12 month grid | `[128,18,161,29]` | 15, white |

Source meanings are read from the exact clean Japanese bitmap. Arrival keeps the
complete natural word; the numbered month grid supplies the month context and
remains exact. Type and Price % use fixed native five-pixel advance (20 and 35
pixels). Arrival uses complete native ink with blank side bearings removed (27
pixels in 33). Only the two proven blank top font rows are trimmed. No visible
letter ink is cropped or resized; first letters, the percentage sign and the
Price % separator remain intact. Actual runtime contexts/crop consumers remain pending.

Cargo/Ship/End/Rank/Cancel captions occupy eight-pixel-high atlas rows. The current
native ASCII font has nine visible rows, so those captions remain pending a
suitable complete font and crop contract. Date fields and other Japanese remain.

The builder now permits per-record color and erasure palette overrides. Existing
defaults and all older batches retain their exact behavior. Gold source faces
are erased only inside their owned rectangles; white Arrival faces use their
original color. Other unowned art, all twelve earlier English labels, month grid,
header, palette, flags and encoded extents remain exact. No runtime font/text code
was changed. The modified builder reproduces the **entire V167 ROM byte-for-byte**:
`work/analysis/v167_color_builder_reproduction.json`.

## Verification and limits

**105 focused graphics tests pass**, including ten new heading tests. They reject
lost leading letters in all three headings, wrong packed glyphs, invalid palette
overrides and eight-row clipping, and check native gold/white ink, word space,
month-grid preservation, twelve exact prior records and full profile/stage inheritance.
Builder, new script and tests pass Ruff. Complete source/English atlas previews,
enlarged headings and embedded bank-zero storage preview were reviewed:

- `work/qa/frame_upper_v168/review.png`
- `work/qa/frame_upper_v168/english_embedded_bank_zero.png`
- `work/qa/frame_upper_v168/source_context.json`
- `work/analysis/frame_upper_v168_artwork.json`
- `work/analysis/frame_upper_v168_native.json`

The actual native font lookup/draw routines execute full eleven-row cells in the
source 256×256 four-bit PXL format. Fixed labels execute together; proportional
letters execute separately, since native six-column cell clearing would erase
overlapped prior ink. Their complete native ink is composed offline and checked
against every packed English face pixel. Registers, ABI, header/palette and memory
canaries pass. Controlled source-header image sizing confirms 256×256.

`/GRP/CMMNIMG.DK4` block 5's right half matches the translated frame exactly. Its
left half, 83 palette banks, other blocks and flags are exact. This proves storage
and native glyph shapes, not actual image loading, live crops/contexts, embedded
bank selection, GPU palette/alpha, controller behavior or physical gameplay.
Those remain pending. Automated checks cannot guarantee every screen in the game.

## Exact candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out\raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V167 comparison and exact reproduction | `7ac37ac46a36c21bb753af83b0db05d5cb9adb94cf9f5b12c07c4701bf2bccec` |
| Candidate: `out\all_routes_combined_v168_candidate.nds` | `fd04046af8de3343b6017c16c1ef03ac422588d110d8e08d2e8cade87d33aff6` |
| ARM9, exact V167 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry at V168 build | `944200c50da66cddae31dedc59841079252d07389c70c94df4528eb73f8a81a9` |
| Registered builder | `baa8e045ff99a7cb8ca6282f00f6dc6f1e51392a6c27064f4ec8ce126baf9edb` |
| Patch: `out\all_routes_combined_v168_candidate.xdelta`, 774465 bytes | `e781c48d0ccbfb79fd927a5f3dff6f3a7e7bc23f28aa0155f3eec50de8da28e2` |

Profile: **all-routes-unified-v168**, experimental. The immutable canonical base
and all inherited terminal stages are applied by the registered builder. There
are **452** experimental batches: 450 unchanged batches and two explicitly
expanded canonical frame batches. Every prior record is retained:

- `translations/frame_action_buttons_graphics_v4.json` supersedes v3,
  preserving twelve records exactly and adding the three headings (15 total).
- `translations/frame_action_buttons_cmmnimg_sync_v4.json` supersedes v3,
  retaining its archive/block source locks and ID while synchronizing the expansion.

Accepted layers are baked into canonical; zero additional accepted batches are
required. Older batches/profiles remain reproducibility records. The adjacent
`out/all_routes_combined_v168_candidate.manifest.json` names the complete stack,
base/registry identity, changed files/records, relocations and all build checks.

Against V167, **only `/_pxl/__frame.pxl` and `/GRP/CMMNIMG.DK4` differ**.
All prior text/code/graphics/components and stages remain exact. The 25 canonical
changed paths are unchanged in membership:

`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/CMMNIMG.DK4`, `/GRP/SLACKIMG.DK4`, `/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/__frame.pxl`, `/_pxl/deck04.pxl`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`, `/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`, `/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`, `/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`, `/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`, `/evstill/evstill208.pxl`, `/evstill/evstill209.pxl`.

Saved verification, canonical menu checks, complete V167 builder reproduction
and exact clean-ROM patch reconstruction pass. Evidence:
`work/analysis/frame_v168_saved_proof.json`.

Before acceptance, cold-boot without a savestate and check title/New Game,
captain selection/name entry, an established story, town UI and inherited
item/Advice/Gallery/treasure/fleet/village/button/score screens. Check Type,
Price %, stock-arrival month labels and all twelve earlier frame labels for
complete characters, spacing/crops, original colors/alpha and controller behavior.
Explicit user cold-boot acceptance is required before canonical promotion.

## Full goal remaining

COMMON still has 245 Japanese selections / 133 physical owners needing actual
consumer/layout integration. ARM9/UI classification, names/source fidelity,
Reports/Sailing Help persistence, BGM audio/input, downloaded states and full
gameplay remain. The historical graphics inventory still has 13 resources with
other Japanese: remaining frame/calendar/selection labels, marker symbols,
title/online/FLS graphics, CMMNIMG left-half lettering, embedded title copy and
unclassified art. Actual consumers/crops and image 207's clipped original source
mark require review. Final packaging/progress, canonical acceptance and GitHub
commit/push remain. On full goal completion, retain the requested note to revisit
older record-based checks.
