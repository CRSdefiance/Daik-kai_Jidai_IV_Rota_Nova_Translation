# Auto Move source owners and footer defect V317

V316 remains the playable candidate. This checkpoint identifies an existing
footer defect and prepares a native correction; no new ROM or patch is released.

## Retained Japanese bytes versus active text

Comparing original pointer owners with the current owned text pool shows four
related strings are already translated:

| Original source | Current active text | Pointer owner |
|---|---|---|
| 自動移動 |automatic travel|0782D0|
| 自動移動中 |Auto Sail|068A20|
| 高速移動中 |Fast Sail|068A24|
| 自動移動できません |Automatic travel is unavailable.|099638|

Their old Japanese literals remain in the binary but current references point
to complete English in the owned staged pool. Editing those abandoned source
slots would not fix a live caption. These are relocation/source facts, not new
physical gameplay clearance for the automatic-sailing modes.

自動移動停止 remains active at0147A48, referenced by footer descriptor field
011915C. It means **Stop Auto Move**. The complete14-letter/space command plus
NUL fits its original16-byte slot. The native stop descriptor begins011914C;
the ordinary sailing descriptor begins0119134.

## Existing odd-length footer defect

The actual native footer function020CA780 measures a label as
`floor(byte_length / 2) * 12`. That preserves12-pixel CP932 pairs but budgets
only36 pixels for the7-byte ASCII label **Sea Map**, whose complete lettering
requires42 pixels. In the packed raster, Menu begins at the final p's position,
overwriting it. This defect was reproduced using the actual descriptor and
the current renderer; it is separate from the newly translated confirmation.

A proposed two-instruction correction computes byte_length times6 while leaving
the12-row surface height untouched. Even byte lengths, including CP932 pairs,
retain their original widths. Odd ASCII labels gain the missing6-pixel cell.
This applies to the footer measurement function rather than shortening wording.

## Native research verification

The proposed buffer includes the full Stop Auto Move label and corrected width
calculation. Native measurement executes for byte lengths0–128:129 cases.
All retain surface height12; even widths are unchanged and odd widths include
every ASCII cell. This arithmetic check does not certify every mixed-font input.

Complete native footer raster/placement runs pass in both4-bit and16-bit modes:

| Label | Left | Width | Packed source X |
|---|---:|---:|---:|
| Menu |45|24|126|
| Sea Map |91|42|84|
| Stop Auto Move |155|84|0|

Every native pixel matches the independent full-string font raster. All label
rectangles fit256 pixels and do not overlap. Source descriptor transfer,
measurement, rendering and return execute. The bounded bitmap view/origin
contracts remain those documented by the existing footer harness; physical
HUD/GPU/input clearance is still pending.

A dedicated harness adds only the two mapped sailing descriptors and permits
the exact inherited buffered-cursor helper bytes. The historical raster harness
is unchanged. Initial attempts rejected the unmapped descriptor/helper; another
attempt changed a register also used for surface height and was rejected. The
final proposal preserves that height and fixes only width arithmetic.

## Required next step

Audit the other footer descriptor families and CP932/native layout compatibility,
integrate the full inherited stack through a registered profile, reconstruct its
patch, and verify the complete Sea Map footer in ordinary cold-boot sailing.
Keep the proposed Stop caption's actual automatic-sailing context open until it
is legitimately reached. The current crew's Survey120 eligibility requirement
still prevents ordinary Auto Move in the saved game.

Both authoritative audits record the defect and research evidence. All18 plaque
entries and variants remain incomplete; low resolution Online images remain
exempt. The full goal remains active. V316 has not received this repair yet.

Evidence: `work/analysis/auto_move_contexts_v317/proof.json`,
`proposed_arm9.bin`, `native_run.log`; scripts
`research_auto_move_contexts_v317.py` and `execute_sailing_footer_v317.py`.
