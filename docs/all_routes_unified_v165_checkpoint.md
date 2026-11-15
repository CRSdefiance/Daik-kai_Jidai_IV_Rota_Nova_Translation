# Combined V165: six shared action buttons

V165 is the latest **experimental** combined candidate. Six Japanese shared
button labels now have complete natural English words in both the loose frame
and its matching embedded pixel region. Every prior V164 component, translation
and repair stage remains exact. The full goal remains incomplete.

## Source and English

| Japanese | English | Original lettering rectangle |
| --- | --- | --- |
| 装備 | Equip | `[3,122,37,133]` |
| 助言 | Advice | `[3,138,37,149]` |
| はい | Yes | `[3,194,37,205]` |
| いいえ | No | `[43,194,77,205]` |
| はずす | Remove | `[3,210,37,221]` |
| 使う | Use | `[43,210,77,221]` |

Remove retains the meaning of taking equipped gear off. All six labels are
complete words, using the original native font at five-pixel advance. Only the
two proven blank leading font rows are trimmed; every visible glyph pixel is
retained. All eleven original glyph rows execute in the native proof. English
fits inside each original lettering rectangle without touching button chrome.

The loose source `/_pxl/__frame.pxl` is 256×256, four-bit PXL. It matches the
clean Japanese ROM, canonical baseline and V164 exactly. Original white faces
and dark shadows are erased only within the six owned lettering rectangles.
Those background pixels are reconstructed from the nearest original row
colors. The borders, unrelated text, other art, header, palette, dimensions and
encoded extent remain exact. This does not translate the rest of this atlas.

`/GRP/CMMNIMG.DK4` block 5 contains a 512×256 four-bit pixel region. Its right
half matches all loose source frame indices exactly. V165 synchronizes that
half to the translated frame. Only the six lettering areas differ; the entire
left half, block header/flags, palette block 4 with all 83 banks, other archive
blocks and total size remain exact. No builder code change was needed.

The complete loose source/English atlas and enlarged six-button crops were
reviewed. The complete embedded bank-zero storage preview was also reviewed;
this provisional palette view does not prove native bank selection or alpha.
The embedded left half still has historical Japanese captions. Previously
translated loose marker and DSOBJ radial-menu captions remain exact.

Preview: `work/qa/frame_buttons_v165/review.png` and
`work/qa/frame_buttons_v165/english_embedded_bank_zero.png`.
Artwork record: `work/analysis/frame_buttons_v165_artwork.json`.

## Verification and limits

**75 focused graphics tests pass**: 15 new frame tests and all 60 prior
button/name/treasure/fleet/village/score tests. New tests reject a missing first
letter in every label's independent native mask and packed bitmap, border
damage in both atlas copies, changed source bytes, wrong sync reference or
destination, visible font-row trimming and glyph-width truncation. All prior
profile batches and terminal stages are preserved. New code/tests pass Ruff.

The real native font lookup and pixel routines `020D16B4`/`020D1820` execute
every character in a blank bitmap with the **actual source 256×256 four-bit
PXL header and palette**. Complete output matches independently decoded native
font masks and the packed English pixels. Full header, memory canaries, saved
registers and stack pass. The original file descriptor at `0210F19C` names owner
`02313F60` and path pointer `02160558` for `_pxl/__frame.pxl`.

Common native image sizing confirms 256×256 using a **controlled loaded
resource/header and selector binding**. The filename descriptor is source
evidence, not proof of executing its loader. Embedded synchronization proves
pixel-storage equivalence; native palette banks and consumers are not mapped.
Actual loose/embedded loading, all live button crops/contexts, parent composition,
GPU palette/alpha, controller behavior and physical gameplay remain pending.
No global screen-formatting guarantee follows from these scoped checks.
Native evidence: `work/analysis/frame_buttons_v165_native.json`.

Saved-ROM verification proves the entire inherited stack, changed-record sets,
relocations, all previous resources/components and terminal stages exact.
ARM9, COMMON/HELP, every route and every older graphic are byte-identical to
V164. Canonical menu invariants and exact clean-ROM patch reconstruction pass.
Saved evidence: `work/analysis/frame_v165_saved_proof.json`.

## Candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V164 comparison | `b09e54f664c51cadb40ecc8287b19069cc4c544199e3c4eb3cde9b1d4ddf43fb` |
| V165: `out/all_routes_combined_v165_candidate.nds` | `2d40853f541e43d023cf708499c142e6bf81e08614ba865812daf3c89f5f98cd` |
| ARM9, exact V164 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry at V165 build | `692d5ca7e5087393f9e93f19260c1befbcdf9c9b7aafcd70b62067a6dad1c78c` |
| V165 patch: `out/all_routes_combined_v165_candidate.xdelta`, 770928 bytes | `552dc2421d455e2d244f801188ccbdc0c2e109256ae0f5fdfd4c2ba45d24debe` |

Profile: `all-routes-unified-v165`, experimental. The registered integrated
builder starts from the immutable canonical base with all 450 V164 batches and
every terminal stage. It adds these two source-locked experimental batches:

- `translations/frame_action_buttons_graphics_v1.json`
- `translations/frame_action_buttons_cmmnimg_sync_v1.json`

There are **452** batches in total. Accepted layers are baked into the canonical
baseline; zero additional accepted batches are required. The adjacent
`out/all_routes_combined_v165_candidate.manifest.json` records the baseline,
registry, full batch list, changed paths/records, stages and build checks.

Compared with V164, **only `/_pxl/__frame.pxl` and `/GRP/CMMNIMG.DK4` differ**.
Compared with canonical, 25 internal paths differ:
`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/CMMNIMG.DK4`,
`/GRP/SLACKIMG.DK4`, `/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/__frame.pxl`,
`/_pxl/deck04.pxl`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`,
`/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`,
`/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`,
`/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`,
`/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`,
`/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`,
`/evstill/evstill208.pxl`, `/evstill/evstill209.pxl`.

Before acceptance, cold-boot without a savestate. Check title/New Game,
captain selection/name entry, an established story, town UI and earlier changed
item/Advice/Gallery/treasure/fleet/village/button/score screens. In each shared
button context, verify complete Equip/Advice/Yes/No/Remove/Use words, alignment,
actual crop, palette/alpha, borders and controller behavior. Check equipped
items' removal/use and confirmation flows. Native consumer mapping and physical
checks remain open. Explicit user acceptance is required for canonical promotion.

## Full goal remaining

COMMON remains 245 Japanese selections / 133 physical owners requiring actual
consumer/layout integration. Other ARM9/UI and name/source fidelity, Reports/
Sailing Help persistence, BGM physical audio/input, downloaded states and full
gameplay checks remain. The historical graphics inventory still has **13**
resources with other Japanese lettering: the frame is only partly translated.
Its remaining buttons/calendar/trade labels, marker gender symbols, title art,
online screenshot lettering and FLS logos remain; the embedded CMMNIMG left
half, remaining frame labels, matching embedded title and unclassified art
also remain. Exact live graphic consumers/crops and image 207's clipped source
mark still need review. Inventory counts do not clear every physical screen.
Final packaging/progress, canonical acceptance and GitHub commit/push remain.
On full goal completion, retain the requested note to revisit older record-based
checks.
