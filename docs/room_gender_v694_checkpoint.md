# V694: actual second crew-assignment parent and complete gender symbols

The previous goal turn answered a status question and made no goal progress.
This checkpoint makes progress by finding and exercising the previously missing
second loose-marker consumer. No artwork, ROM, patch or release pointer changes.
The experimental candidate remains V692, SHA-256
`0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.

## Why the earlier navigator tests skipped the helper

Actual RTTI identifies the associated parent as `18CDeckPersonnelView` at
`0218BD98`. The selection view is `28CSelectPlayerForcePersonView`; the cast
itself succeeds. The original room getter `0201BAB4` returns null when the
selected room is 32 (None). The original code then bypasses `020157D8`.
This is an intentional game branch, not a failed cast or broken symbol.

Closing the unassigned roster, selecting Deck and opening its officer roster
sets room 5. The original code then calls the full gender/info update with its
actual room argument and selected actor. Normal menu changes temporarily
unassign the navigator; no live actor, location, quest, ROM or renderer data is
injected. The copied Maria donor retains the previously disclosed selection
unlock provenance; earned unlocks are not claimed.

The room automatically selects the officer with the highest relevant ability.
An explicit stylus selection therefore supplies stable Maria holds, followed by
Yukihisa, Maria, Xien Yan and Maria again. The roster button coordinates come
from the actual original button rectangles and sorted actor array.

## Complete source and displayed-cell verification

- Four actual helper chains cover Hodram (actor 1), Maria (3), Xien Yan (10)
  and Yukihisa (12). Original raw sex getters return 0/1; identities match the
  selected actors and the resulting views select the appropriate symbol.
- Four complete original cache-hit getter executions bind the actual owner to
  every byte of `/_pxl/__marker.pxl`, without an I/O or image-getter bridge.
- Both original branches create 16 by 16 views using palette bank 48: male
  source `(232,96)`, female source `(240,112)`.
- The original state-4 drawing code references point `021146A8`, whose two
  signed words are `(80,80)`. Destination placement is derived from this code
  and source data, independently of screenshot symbol detection.
- All 28 complete held symbol cells match: 24 male and four female, 7,168
  native-five-bit RGB pixels including every edge, background cell, arrow and
  cross. Wrong-sex, wrong-palette and one-pixel placement controls all fail.
- Five observed/unobserved run pairs match 165 complete two-screen RGB images
  and all five complete terminal 4 MiB RAM states. Each run is a 13,200-frame
  cold boot with the same copied donor and normal menu input schedule.
- All original read-only observers preserve CPU, WRAM, DTCM/configuration and
  restore interpreter slots. The added ITCM observer also preserves its whole
  32 KiB region. The 35 native host-prefix and eight bounded-mirror controls pass.

The six-screen sheet was opened and reviewed. Both symbols are complete,
consistent with their selected actors and positioned inside their boxes. A
draft sheet label incorrectly called actor 10 Ian; review of the actual screen
corrected that label to Xien Yan before final recording. No production naming
change was needed.

## Full native suffix comparison is still unresolved

The standalone native replay executes each complete original branch through
the actual following PC. Every executed instruction is checked against the
registered candidate code. Captured RAM, DTCM, ITCM, R0 through R14 and CPSR
match at all recorded intermediate checkpoints, including the completed gender
view construction. Actual low ITCM mirrors and captured banked stack/link
registers replace initially missing standalone-machine state.

Both None-room bypasses reproduce the complete return state exactly. The four
full helper executions reproduce return registers, CPSR and ITCM, but their
whole return RAM/DTCM states do not match:

| Actor | Changed main-RAM bytes | Changed DTCM bytes |
|---|---:|---:|
| Hodram | 47 | 19 |
| Maria | 48 | 19 |
| Yukihisa | 53 | 10 |
| Xien Yan | 53 | 20 |

All addresses and actual/expected bytes are retained. Differences include SDK
context storage and two reference-count locations. Their cause is not proven;
frame crossing alone does not explain every case. No expected state is copied
into the replay and no mismatch is removed or classified as exact. The original
failing replayers and diagnostic remain in the archive. This is an unresolved
standalone full-suffix comparison, not evidence of a visible symbol defect or
of complete original-function equivalence.

## Remaining scope

This closes actual display/source coverage for both symbols in this second
loose-PXL parent. It does not verify the embedded copy's consumer or exercise
the original identity-8/story-flag exception. That exception's original code is
preserved. Other control/card/comic/legacy contexts, restoration review, older
record checks and final acceptance remain open. All 18 plaque/hint entries
remain incomplete, and all 22 original historical requirements remain exact.

No new ROM, patch, guide image promotion, commit, push or canonical acceptance.
Full graphics goal remains active.

## Evidence

- `scripts/observe_room_gender_v694.py` and the two frozen schedule runners.
- `scripts/run_room_gender_ITCM_v694.py`: read-only ITCM extension.
- `scripts/replay_room_gender_v694.py`: complete execution with unwaived gaps.
- `scripts/verify_room_gender_v694.py`: live source/cell/baseline verification.
- Analysis: `work/analysis/room_gender_v694`.
- Captures: `E:/Rota Nova translations/Generated/work/emulation_v193/room_gender_v694_*`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V694 Actual room gender symbols`.
