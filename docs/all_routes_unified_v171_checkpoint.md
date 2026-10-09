# Combined V171: English month/day initials

2026-10-04. V171 is the latest **experimental** combined candidate. The last two
Japanese date-unit glyphs in the loose shared frame now use conventional English
initials. All twenty earlier labels, other translations, ARM9 and repair stages
remain exact. The full goal is incomplete; acceptance, final packaging and commit/push remain.

## Date-unit localization

| Japanese | English initial | Meaning | Exact original ink cell | Complete glyph |
| --- | --- | --- | --- | --- |
| 月 | M | Month | `[104,116,110,124]`, 6×8 | 5×7 |
| 日 | D | Day | `[128,116,133,124]`, 5×8 | 4×7 |

M/D are conventional English date-field initials. Full Month/Day words do not
fit the original tiny cells; these complete initials preserve the date-unit
meaning inside the original Japanese ink extents. Gold index 9 is retained, with
one blank bottom row. No letter is clipped, resized or pushed into neighboring art.
The adjacent day separator, ornament, calendar numbers, field borders and all
unowned pixels remain exact. Original source cells contain only indices 0 and 9;
only these two cells are restored to their index-zero background and redrawn.

The versioned authored `compact-en-7px-v2` face adds a complete five-column M.
Every v1 glyph and its identity remain exact; D is the same complete v1 shape.
Earlier records retain their v1 face, SHA and word-space options unchanged.
The builder checks each face against its own exact identity; using the v1 SHA
for v2 fails. Runtime font/text code is unchanged. The modified builder reproduces
**the complete V170 ROM byte-for-byte**:
`work/analysis/v170_date_face_builder_reproduction.json`.

Full atlas review now finds **no remaining Japanese lettering in the loose
`/_pxl/__frame.pxl`**, with 22 translated labels/units accumulated. Its matching
CMMNIMG right-half indices are exact. The historical loose-graphics backlog falls
from 13 partially Japanese resources to **12**. CMMNIMG's Japanese left half,
other embedded graphics and unclassified artwork remain. This inventory result
does not prove every native consumer, displayed crop or palette bank.

## Verification and limits

**150 focused graphics tests pass**, including eleven new tests. They reject lost
unit glyphs, wrong unit letters and incorrect date-face identity; pin both face
hashes, preserve all v1 shapes and twenty prior records, verify complete original
cells and both native supplied crop descriptors, preserve nearby separator/ornament
pixels, and check the complete profile and terminal stages. Builder, compact font
module, new script and tests pass Ruff.

Independent glyph-row layout and direct packed-nibble decoding verify all seven
compact captions/units. Original native lookup/draw proofs retain all fifteen
earlier native-font labels. Supplied native crop constructor calls check 6×8 and
5×8 extents, source owner/origin, ABI and memory guards. Controlled header sizing
confirms 256×256. Actual parent consumers, all live crops/contexts, loose/embedded
loading, palette banks/GPU alpha and input/physical gameplay remain pending.

Full source/English atlas and enlarged date-unit previews were reviewed, along
with the complete embedded bank-zero storage view. CMMNIMG's left half, all 83
palette banks, block headers/flags, unrelated blocks and extent remain exact.

- `work/qa/frame_date_v171/review.png`
- `work/qa/frame_date_v171/english_embedded_bank_zero.png`
- `work/qa/frame_date_v171/source_context.json`
- `work/analysis/frame_date_v171_artwork.json`
- `work/analysis/frame_date_v171_native.json`
- `work/analysis/frame_v171_saved_proof.json`

## Exact candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out\raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V170 comparison and exact reproduction | `57ea4b89b889c87f4656d5e286a372dc85bc260051e70cc4ac14762fb63c69a6` |
| Candidate: `out\all_routes_combined_v171_candidate.nds` | `7a51d00eae25b50c9b914b6e3a26cff6ca7b0940b445f67107f7328c60759888` |
| ARM9, exact V170 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Release registry at build | `701ed5e74458db4e1c6f5da3cbce8611552801536b0bc77c8920746cd5e276d8` |
| Registered builder | `0d0eecd9c69af193a0a2d20256e2a9b25a1ff81ae27568a8fd45e1ac75ab1fe5` |
| Compact font module | `324418884f4f71012df7644f26e61b8d1f6efa99ee00612c291d4f2a5a96e39a` |
| v1 glyph face, unchanged | `1f34962fa7ff25491a84dc488219d6e18727654f51fdcfdefbb201b95a0e4b7d` |
| v2 date glyph face | `cfe704c25f3ce6e8e8464201d8b3791a981941c47782bb1bbc5dbc0cf054d16f` |
| Patch: `out\all_routes_combined_v171_candidate.xdelta`, 775423 bytes | `4810cd5a866eec298268bd40298ed59f5e63e3659a8bd5e53be2281d391e0cf7` |

Profile: **all-routes-unified-v171**, experimental. The registered builder applies
the immutable canonical base and all inherited terminal stages. Accepted layers
are baked into canonical; zero additional accepted batches are required. There
are **452** experimental batches: 450 unchanged and two expanded canonical frame
batches retaining every previous record:

- `translations/frame_action_buttons_graphics_v7.json` supersedes v6, preserving
  twenty exact records and adding the two date units (22 labels total).
- `translations/frame_action_buttons_cmmnimg_sync_v7.json` supersedes v6, preserving
  original archive/block locks and ID while synchronizing the expansion.

Older batches/profiles remain reproducibility records. The adjacent
`out/all_routes_combined_v171_candidate.manifest.json` records the complete stack,
baseline/registry identity, changed paths/records, relocations and build checks.
Against V170, **only `/_pxl/__frame.pxl` and `/GRP/CMMNIMG.DK4` differ**.
The 25 canonical changed paths retain their membership:

`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/CMMNIMG.DK4`, `/GRP/SLACKIMG.DK4`, `/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/__frame.pxl`, `/_pxl/deck04.pxl`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`, `/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`, `/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`, `/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`, `/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`, `/evstill/evstill208.pxl`, `/evstill/evstill209.pxl`.

Saved preservation, canonical menu checks, full V170 reproduction and exact
clean-ROM patch reconstruction pass. Every other resource/component, prior
translation, code, graphic, relocation and changed-record set remains exact.

Before acceptance, cold-boot without a savestate: check title/New Game, captain
selection/name entry, an established story, town UI and inherited item/Advice/
Gallery/treasure/fleet/village/button/score screens. Check M/D in their actual date
contexts: intact complete glyphs, month/day meaning, nearby day separator/art,
gold color/alpha and controller behavior; recheck all twenty older frame labels.
Explicit user acceptance is required before canonical promotion.

## Full goal remaining

COMMON remains 245 Japanese selections / 133 physical owners needing actual
consumer/layout integration. ARM9/UI classification, names/source fidelity,
Reports/Sailing Help persistence, BGM audio/input, downloaded states and full
gameplay remain. Twelve historical loose graphics resources still contain Japanese:
marker symbols, title/online/FLS graphics and remaining artwork. CMMNIMG's Japanese
left half, embedded title copy and unclassified embedded art also remain. Actual
consumers/crops and image 207's clipped source mark still require review. Final
packaging/progress, canonical acceptance and GitHub commit/push remain. On full
goal completion, retain the requested note to revisit older record-based checks.
