# V663: complete five-slot equipment borders, hints and footer

## Result

Three8063-frame runs finish normally: current V653, V636 regression control and
current V653 with a disclosed read-only host scanline observer. All use the same
ordinary controller/touch inputs and byte-exact Syracuse donor copy. No savestate
or gameplay fixture is used. The donor's shield is already owned; no new item
acquisition or route completion is claimed.

All325 full two-screen current/control pairs match, as do all325 observed/current
pairs. Five64-frame equipment windows account for all15,728,640 lower RGB pixels
without border, hint, footer or animation masks. The current window's selection
border gap is resolved. The historical V637 exclusion remains recorded as it was;
these new captures do not retroactively retest its84 synthetic condition views.

V653 remains unchanged. The graphics goal stays active.

## Ordinary scenes and original draw order

The schedule extends the established plaque-review sequence. Normal touches at
native x30/80/128/176/224 select all five slots. Original controller field
`02189E24 + 6B90` is3/4/5/6/7 in every corresponding captured RAM copy.

Actual lower renderer `023117C4` contains Sailor Info node `021909B8` and its hint
node. Original thunk `02081950` adjusts the node by `-6B94` and reaches original
lower painter `0207FB74`. Original slot geometry `0207FA0C` supplies32x32 item
rectangles. The painter expands the selected rectangle by2 pixels and calls
`020D13A4`, followed by item icons and the later hint. The original traversal
also draws the hint node and shared footer in their actual order.

The selected border has272 geometric pixels before later overlaps. Weapon,
Blue Oak Shield and the first Equipped Items hint cover68 of those pixels;
the fourth slot covers72 and the fifth covers36. Native on/off differences are
therefore204/204/204/200/236 pixels. These are complete source-based compositions,
not a border exclusion or a fitted screenshot crop.

## Native reconstruction and clock contract

For each slot, both source-defined blink states run through original traversal
`020D32B8..020D3314`, original painters and original shared footer. The whole
98,304-byte lower software output is poisoned first. Every byte is assigned,
guards and fragment ABI pass, and no old output is read before writing it.

Both captured visible LCDC outputs are erased in the isolated model. Every VRAM
read excludes those outputs; there are no VRAM writes. Actual ITCM/DTCM and the
source-bound bank aliases supply original code and off-screen glyph inputs.
Every executed instruction matches registered ARM9, overlay or the startup-copied
translation pool. The copy range is validated by `cache_plan`; the late-copy
payload is bound to its actual runtime address, not guessed from its staging VA.

Only SDK `OS_GetTick` is bridged in this isolated model. The two declared inputs
are the captured original origin plus0 or plus`77DAF`. Original `02000F9C` executes
its64-bit calculation using period`88FA4` and cutoff`77DAF`, then original
`020D13F8` derives the cyan fill from RGB0,160,168. No predicate, source getter,
glyph renderer or painter is substituted. These clock inputs are component-test
contracts, not observed CPU-tick arguments or artificial changes to the emulator.

Each slot has55 whole-on and7 whole-off captured screens plus2 mixed transition
frames. The310 stable screens match a complete original native variant exactly.

## Ten mixed frames, with no delay or row-phase fitting

The initial whole-frame-only model correctly rejects frame6425: its upper ring
portion is on and its lower portion is off. This diagnostic is retained. The
same ten mixed frames occur in V636 and V653:

`6425,6433,6825,6833,7225,7233,7625,7633,8025,8033`.

The inherited exact-hash DeSmuME RenderLine observer records all192 original
before-read rows for each mixed frame, including the actual bitmap row and IO.
It temporarily detours only three host entry prefixes in its own diagnostic
process. All original rendering executes once, entry bytes are restored, and the
DLL file remains exact. Twelve native-host prefix/ABI controls and original
VCount-driven HBlank call bindings pass. All325 whole observed/unmodified-core
captures match; no game ROM, RAM, VRAM, registers or inputs are patched.

Every one of491,520 observed source words belongs to the corresponding original
native on/off output at that exact coordinate. Original BG3 direct-bitmap setup,
bank D mapping, affine row address, priority and disabled blend/brightness are
verified for all1,920 rows. The actual source words expand to all491,520 captured
lower RGB pixels exactly. No selected delay, inferred row switch or waived pixel
is used. This explains these inherited blink transitions, not all DMA timing or
physical hardware behavior.

## Complete text, material and source meanings

- All320 hints pass independent full glyph/blank-cell masks: Weapon, the actually
  owned Blue Oak Shield and Equipped Items. Six first/final glyph corruptions are
  rejected. An initial empty-Armor assumption was rejected, not credited.
- All3,200 upper static plaque crops match the source-reviewed V632 packet.
  All18 original plaque/hint entries nevertheless remain incomplete.
- The720 active cached footer cells independently match complete Select/Back
  glyphs and blank cells. Four isolated DTCM cell deletions cause exactly
  15/12/21/15 missing visible pixels for first/final Select and Back letters.
- The10 active skill labels are resolved from the original getter on both clean
  Japanese and current ROM data, rather than an older unused profile:

| Japanese | Current English |
|---|---|
|生命力|Vigor|
|統率力|Command|
|操船術|Sailing|
|測量術|Survey|
|会計術|Finance|
|剣闘術|Swords|
|命中力|Aim|
|説得力|Speech|
|謀略術|Guile|
|観察力|Observe|

These retain the existing compact UI meanings. No new wording, graphics, palette
or font change is authored. The three actual hint texts and full screens for all
five selected slots were visually inspected. Automatic whole-screen comparisons
cover the remaining captured frames; this is not individual visual inspection of
all325 screens or a new independent reconstruction of the whole upper scene.

## Reproduction and archive

- Capture: `python scripts/run_equipment_cursor_v663.py`, then `--control`.
- Native preparation: `python scripts/verify_equipment_cursor_v663.py --prepare-phases`.
- Source rows: `python scripts/run_equipment_scanlines_v663.py`.
- Verify: `python scripts/verify_equipment_cursor_v663.py`.
- Proof: `work/analysis/equipment_cursor_v663/proof.json`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V663 Equipment cursor`.
- Three unchanged ordinary screenshots are copied separately to
  `E:/Rota Nova translations/Screenshots/Guide candidates/V653 Equipment cursor`.
  They are unapproved guide candidates; plaque material review is still open.

The partial-painter attempt, which omitted the hint/footer, and the rejected
whole-blink-frame model are retained. Current ROM SHA256 remains
`c4e9c4faf18c212e5b6572d61e6b2821493f38bbc1dc89d601b37b16058b3ade`.
ROM, patch, manifest, registry, canonical and all release pointers are unchanged.
All22 historical scope objects stay exact. Other control/card/legacy/material,
equipment/character contexts, older record checks and final acceptance remain
open. No new ROM, commit or push occurs in this checkpoint.
