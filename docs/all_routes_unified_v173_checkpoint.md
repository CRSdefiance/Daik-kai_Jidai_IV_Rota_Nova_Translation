# Combined V173: complete standard gender symbols

2026-10-04. V173 is **experimental**. Original 男 / 女 icons are now standard ♂ / ♀
symbols in both loose marker and embedded CMMNIMG. All 24 prior marker captions,
all 22 frame labels/units and every prior text/code/repair stage remain exact.
The all-graphics goal remains active and incomplete.

## Localization and ownership

| Source | Replacement | Meaning | Original owned lettering cell | Complete new symbol |
| --- | --- | --- | --- | --- |
| 男 | ♂ | Male | `[235,98,246,109]` | 7×7 |
| 女 | ♀ | Female | `[243,114,254,124]` | 5×7 |

These are existing standalone gender icons beside zodiac symbols. Conventional
symbols preserve their meaning without abbreviating or clipping a word. Source
cells contain only black index 1, white index 15 and original lettering shadows
9/11. The cells are restored to black and complete circles/arrow/cross drawn in
white. Every border, adjacent zodiac icon, other caption and unowned pixel is exact.
Only **78 marker indices** change. Native glyphs/runtime fonts/code are untouched.

The new versioned seven-row face adds only the two authored symbols, preserving
all earlier v1/v2 glyphs and their exact identities. Full V172 reproduces byte for
byte before the V173 build. Independent raw packed-nibble checks verify all pixels,
including complete top/bottom symbol ink and unchanged prior art. Full atlas and
larger icon crops, plus embedded bank-zero storage view, were reviewed.

**176 focused graphics tests pass**: ten new gender checks plus 166 prior checks.
Tests reject lost symbol edge ink, wrong face identity, overflow, wrong source,
unowned-border damage and loss of previous glyphs/batches/stages. Ruff passes.
Generic native crop constructor calls verify both supplied cell origins/extents,
owner field and ABI/canaries; controlled PXL header sizing verifies 256×256.
These controlled inputs do not establish actual marker loaders/parent consumers,
live crops, palette-bank selection, GPU alpha, controller or physical gameplay.

All embedded palette banks, headers/flags, unrelated blocks/extent and the entire
right-half V171 frame remain exact. Saved ROM/resource/record/stack/relocation
checks and exact clean-ROM xdelta reconstruction pass.

## Remaining full graphics scope

Full reviewed marker atlas now has no Japanese lettering; 26 captions/symbols are
localized. The original historical audit has **11 remaining Japanese-bearing
entries in 10 unique files** (FLS textures 4/5 count separately):

- `/_pxl/logo.pxl`
- `/_pxl/startmenu0.pxl`
- `/_pxl/winframe00.pxl`
- `/_pxl/online/Online24.pxl`
- `/_pxl/online/Online27.pxl`
- `/_pxl/online/Online31.pxl`
- `/_pxl/online/Online33.pxl`
- `/_pxl/title/title03.pxl`
- `/_pxl/title/title05.pxl`
- `/FLS/M28.fls` texture 4
- `/FLS/M28.fls` texture 5

Five title-source previews and exact palette/dimension/source identities are
prepared under `work/qa/remaining_titles/`. The DS logos contain 大航海時代IV,
ROTA NOVA and small ロッタ ノヴァ; PC Porto Estado art contains the Japanese
franchise title and ポルト・エシュタード alongside Latin PORTO ESTADO. Source
transcription, English title treatment, text/background ownership and native
composition still require completion.

The eleven-entry count does **not** clear other embedded title copies, unclassified
archive blocks/formats, environmental signs, image207's clipped source mark,
opening Latin name-card fidelity or complete native/gameplay verification. All 921
PXL/FLS thumbnails were screened historically; full-resolution and native checks
remain a broader requirement. `translations/graphics_completion_campaign_v1.json`
records the complete goal scope and pending evidence. No goal completion is claimed.

## Exact artifacts and inherited stack

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out\raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Prior V172 / exact reproduction | `051ffe4725434a9dcff1d1d1b34be72c81fc8d1d8cde76d7d59bac92ce0fdc92` |
| Candidate: `out\all_routes_combined_v173_candidate.nds` | `19df444510eca115d1facc118180a793ef99cdcbc104f484428d3c0575b4f29f` |
| ARM9, unchanged V172 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry | `5a4a2902a4225c71ce21610ef1dd961c63d4a07785f61bae030aecd592574d61` |
| Builder | `97391ce61446ba585273e2a6deb5ff21f534ef7e3daf342cfff57a0d0becc368` |
| Compact font module | `baa10adf5c5e3f283ddef5bdcd394d99952b0cf5f37b4ad6179eb8e817a547ac` |
| Authored v3 symbol face | `d872e68d6b0abdb0c56be3f6a2bcd8af5bc27323e0854596b43a87d2fc5dabb7` |
| Patch: `out\all_routes_combined_v173_candidate.xdelta`, 780736 bytes | `518b2d14d315132a9dbf4245239a953701de26122348113bec9fe1640840035f` |

Profile **all-routes-unified-v173**, experimental, has **454 batches**: all V172
layers/stages retained, one new canonical-source marker gender batch, and the
marker sync explicitly expanded from v1 to v2. The frame sync is unchanged.
Accepted layers remain baked into immutable canonical; zero additional accepted
batches are needed. Adjacent candidate manifest names baseline/registry/full
stack/record IDs/relocations/checks. Against V172, only `/_pxl/__marker.pxl` and
`/GRP/CMMNIMG.DK4` differ. The 26 canonical changed paths are:

`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/CMMNIMG.DK4`, `/GRP/SLACKIMG.DK4`, `/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/__frame.pxl`, `/_pxl/__marker.pxl`, `/_pxl/deck04.pxl`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`, `/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`, `/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`, `/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`, `/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`, `/evstill/evstill208.pxl`, `/evstill/evstill209.pxl`.

Evidence: `work/qa/marker_gender_v173/review.png`, `embedded.png`, `evidence.json`,
`native.json`; `work/analysis/v173_graphics_tests.log`,
`v172_gender_face_reproduction.json`, `marker_gender_v173_saved_proof.json`.
Reproducible script: `scripts/marker_gender_v173.py`.

Before acceptance, cold-boot without a savestate: title/New Game, captain/name
entry, an established story, town UI and inherited repaired screens. Check both
gender icons in their actual contexts, male/female semantics, complete circle/
arrow/cross, bounds, borders, colors/alpha and controller behavior; recheck prior
24 marker captions and 22 frame labels. Actual embedded loader reachability is
still unproved. Explicit human acceptance is required before canonical promotion.
On full project-goal completion, retain the requested follow-up to revisit older
record-based checks.
