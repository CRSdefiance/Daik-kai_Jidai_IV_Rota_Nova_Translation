# RACE record boundaries and generated-mode investigation V212

2026-10-07. Previous goal turn localized the embedded START prompt and registered
V211. This turn verifies the complete RACE read partition and identifies additional
generated-text consumers to investigate. **No ROM changes; V211 remains current.**

## Complete native RACE reads

All seven indices execute the unchanged native open/indexed seek/read/close fragment
at `020F71B0..020F71F8`. Only SDK filesystem operations are bridged. Preceding stack
index and buffer context are explicit fixtures. Every byte, buffer guard, stack and
handle check passes. Sorted by file offset, the records cover all **851,296 bytes**
with no gap, overlap or ignored tail.

| Index | Offset | Bytes | Native metadata width×height | Metadata-sized bytes |
|---|---:|---:|---|---:|
| 0 | 0 | 101120 | 320×158 | 101120 |
| 1 | 101120 | 164000 | 410×200 | 164000 |
| 2 | 513120 | 116000 | 290×200 | 116000 |
| 3 | 629120 | 85376 | 232×184 | 85376 |
| 4 | 714496 | 136800 | 320×150 | 96000 |
| 5 | 265120 | 152000 | 380×200 | 152000 |
| 6 | 417120 | 96000 | 380×180 | 136800 |

The two size discrepancies at indices 4/6 are present in clean code/data as well.
Do not alter either table from a guessed transpose, or claim an overflow defect
without establishing the actual caller/selection/buffer contract. Later native
border writes are outside this read-only fragment.

## Interpretation remains open

Size-matched diagnostic views form seven recognizable geographic grids. Their
16-bit words have 739 distinct values, maximum `0395`, and are heavily concentrated
at zero and small integers. Direct BGR555 coloring produces artificial stripes
and is **not** a valid display/color interpretation. The numeric fields, possible
tile/terrain semantics, palette and actual consumers still require mapping.

All seven diagnostics were inspected as spatial evidence only. They do not support
a claim that all rendered artwork is text-free or that this file is non-graphics.
Original bytes remain untouched; no image translation or retain clearance is
invented from the diagnostic. Native metadata and source-record interpretation
remain separate in the proof.

## DSCHR generated text follow-up

The raw-mode reader at `020CDE20` has a direct caller at `020CE6D0`. Two paths
reference preserved Japanese instructions at `0215F72C` and `0215F870` concerning
Exploration Mode and Declare War Mode. They call the overlay entry `01FFB4B0`,
whose trampoline points to `01FFB4BC`; its code parses source character pairs and
calls the native font-map lookup.

These are generated-text paths, rather than evidence that the same words are
baked into DSCHR pixels. Their actual selection, display and relationship to any
already translated alternative have not been established. Do not prematurely
declare them an active untranslated screen or overwrite their executable/format
state. This discovery changes the next action: trace the parent selection and
render contract before preparing faithful English and its layout.

## Evidence and scope

Script: `scripts/research_race_records_v212.py` (focused Ruff passing).
Proof: `work/analysis/race_raw_v212/native_record_proof.json`.
Diagnostics: `frame0_size_matched_diagnostic.png` through `frame6_...png`.

The raw interpretation is incomplete. Four Online screenshot bodies, confirmed
names, other raw/embedded/contextual consumers, remaining native/gameplay checks
and the final combined ROM/patch audit remain in the full graphics objective.
No candidate promotion or full-goal completion is implied.
