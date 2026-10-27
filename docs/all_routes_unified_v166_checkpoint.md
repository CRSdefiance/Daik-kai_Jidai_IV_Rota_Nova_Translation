# Combined V166: four crew-screen buttons

V166 is the latest **experimental** combined candidate. It adds four complete
English crew-screen buttons to both frame atlas copies. All six earlier V165
labels, prior translations, code and repair stages remain exact. The full goal
remains incomplete; canonical promotion and final commit/push remain pending.

## Source and natural English

| Japanese | English | Meaning in crew screen | Lettering rectangle |
| --- | --- | --- | --- |
| 水夫編成 | Set Crew | Arrange the fleet's sailors. | `[43,162,85,173]` |
| 平均化 | Balance | Balance crew distribution. | `[43,178,85,189]` |
| 必要最小 | Minimum | Minimum necessary crew allocation. | `[139,162,181,173]` |
| 変更終了 | Done | Finish making changes. | `[139,194,181,205]` |

All words fit inside the original lettering rectangles. Set Crew retains its
word separator; no abbreviation or cropped glyph is used. The native font has
five-pixel advance. Only its two proven blank leading rows are trimmed, and all
visible pixels remain. The complete eleven-row cells execute in native checks.
The square-sail priority and equal-supply buttons remain Japanese; their complete
meanings and layout still need work.

The source is the immutable canonical `/_pxl/__frame.pxl`, 256×256, four-bit
PXL, matching clean Japanese exactly. Source lettering faces and dark shadows
are erased only in the four new rectangles; owned pixels are reconstructed
from nearest original row colors. Button chrome, every earlier English pixel,
unrelated Japanese lettering/art, header, palette and extent remain exact.

`/GRP/CMMNIMG.DK4` block 5's matching right-half pixel region is synchronized.
Its left half, all 83 palette banks, header/flags, other blocks and encoded
extent remain exact. Only the four new lettering areas differ from V165.
The complete source/English atlas, enlarged crew buttons and complete embedded
bank-zero storage preview were reviewed. Bank zero is a provisional storage
view; native palette bank selection, alpha and consumers remain unproved.
Preview: `work/qa/frame_buttons_v166/review.png` and
`work/qa/frame_buttons_v166/english_embedded_bank_zero.png`.
Artwork: `work/analysis/frame_buttons_v166_artwork.json`.

## Checks and practical limits

**85 focused graphics tests pass**: ten new crew-button tests and all 75 prior
graphics tests. Tests reject dropped first letters in independent native masks
and packed output for each added label, verify the Set Crew separator, retain
all six prior records/pixels, reject damage to earlier labels and changed source
bytes, and check explicit profile supersession and every inherited stage.
New code and the shared font-check helper pass Ruff. The helper now handles a
blank space glyph without treating it as missing ink; ROM builder code is unchanged.

Real native font lookup/pixel routines `020D16B4`/`020D1820` execute all ten
labels in a blank bitmap with the **actual source 256×256 four-bit PXL header
and palette**. Complete output matches independent native font masks and the
English packed pixels. Full header, memory canaries, saved registers and stack
pass. Common sizing confirms 256×256 under controlled loaded resource/header
and selector inputs. This does not establish the real loader or parent crops.
Native evidence: `work/analysis/frame_buttons_v166_native.json`.

Embedded checks prove exact storage synchronization and preservation; actual
native palette banks/consumers are not mapped. Actual loose/embedded loading,
all live button crops/contexts, parent composition, GPU palette/alpha,
controller behavior and physical gameplay remain pending. These scoped checks
do not guarantee every screen throughout the game.

Saved-ROM checks preserve all prior components, resources, terminal stages,
relocations and changed-record IDs, including the six earlier frame labels.
ARM9, COMMON/HELP, all four routes and every other graphic are byte-identical to
V165. Canonical menu checks and exact clean-ROM patch reconstruction pass.
Saved proof: `work/analysis/frame_v166_saved_proof.json`.

## Candidate and complete lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V165 comparison | `2d40853f541e43d023cf708499c142e6bf81e08614ba865812daf3c89f5f98cd` |
| V166: `out/all_routes_combined_v166_candidate.nds` | `d53b7d22c913bf862f10f09b4a456326950173870887732bf2eb17c61c415ee5` |
| ARM9, exact V165 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry at V166 build | `881a87f441eea5b9995dab216d58dabc23f736bd421f1e55dc68f393c41125ed` |
| V166 patch: `out/all_routes_combined_v166_candidate.xdelta`, 772366 bytes | `4313dd0f74e133f86a7167656417dc5c214be924de30df2d614982b295e0f022` |

Profile: `all-routes-unified-v166`, experimental. The registered integrated
builder uses the immutable canonical base and all inherited terminal stages.
All 450 non-frame V165 batches are unchanged. Two expanded canonical batches
explicitly supersede their earlier versions, retaining every prior record:

- `translations/frame_action_buttons_graphics_v2.json` supersedes
  `translations/frame_action_buttons_graphics_v1.json`, with six exact prior
  records plus four new records.
- `translations/frame_action_buttons_cmmnimg_sync_v2.json` supersedes
  `translations/frame_action_buttons_cmmnimg_sync_v1.json`, keeping its source
  archive/block lock and record ID while synchronizing the expanded frame.

Both older batches/profiles remain historical reproducibility records. There
are **452** current batches. Accepted layers are baked into canonical; zero
additional accepted batches are required. The adjacent
`out/all_routes_combined_v166_candidate.manifest.json` records every applied
batch, baseline/registry identity, changed path/record, stage and build check.

Compared with V165, **only `/_pxl/__frame.pxl` and `/GRP/CMMNIMG.DK4` differ**.
The canonical changed path set is unchanged at 25:
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
captain selection/name entry, an established story, town UI and inherited
item/Advice/Gallery/treasure/fleet/village/button/score screens. In the crew
screen, check complete Set Crew/Balance/Minimum/Done labels, actual crops,
alignment, borders, palette/alpha and controller behavior. Exercise crew
distribution, minimum allocation and finishing changes. Check the six earlier
Equip/Advice/Yes/No/Remove/Use contexts too. Explicit user acceptance is required
before canonical promotion.

## Full goal remaining

COMMON remains 245 Japanese selections / 133 physical owners needing actual
consumer/layout integration. Other ARM9/UI and name/source fidelity, Reports/
Sailing Help persistence, BGM physical audio/input, downloaded states and full
gameplay checks remain. The historical graphics inventory still has **13**
resources with other Japanese lettering: the shared frame is partly translated.
Its two remaining crew buttons, calendar/trade/selection labels, marker gender
symbols, title art, online screenshot lettering, FLS logos, the CMMNIMG left
half/remaining frame labels, embedded title copy and unclassified art remain.
Live graphic consumers/crops and image 207's clipped source mark still need
review. Final packaging/progress, canonical acceptance and GitHub commit/push
remain. On full goal completion, retain the requested note to revisit older
record-based checks.
