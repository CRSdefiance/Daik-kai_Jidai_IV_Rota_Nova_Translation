# V504 five occupied equipment slots and current plaque audit

V502 remains unchanged, SHA-256
`f26a930d91f0df2089a080f0945b9f06a3d1f9718f18a39a6e6dca7edc8842bc`.
No ROM/patch changes, canonical promotion or graphics-goal completion.

## Fixture authorization and isolation

The user authorized artificial inventory items for rendering tests. V502 support
was added to the bounded fixture helper after verifying the transfer, getter and
history routines remain byte-identical to V484. A native trial confirms writes
are limited to selected item records and the existing acquisition-history vector.

A copied genuine Istanbul cartridge save received Tireless Hawser75, Pocket
Watch82 and Rocco's Sailing Guide83. Normal menu actions equip them on Hodram.
Golden Cutlass29 was inadvertently removed through the toggle command, then
re-equipped through ordinary input. The original donor remains byte-identical;
no save, ROM, unrelated unlock flags or character condition was injected.
This is explicitly synthetic inventory evidence, not normal acquisition evidence.

## Actual current-ROM results

| Slot | Item | Frame | Exact tooltip paper rectangle |
| --- | --- | --- | --- |
| 1 | Golden Cutlass |6800|(16,208)-(104,224)|
| 2 | Blue Oak Shield |6900|(64,208)-(158,224)|
| 3 | Tireless Hawser |7000|(112,208)-(206,224)|
| 4 | Pocket Watch |7100|(148,208)-(224,224)|
| 5 | Rocco's Sailing Guide |7200|(94,208)-(224,224)|

- All five full names, including first/final letters and blank cells, match889
  native text pixels. All paper/bevel/corner pixels match the native texture style.
- All five32x32 item icons match their source atlas:5120 exact pixels.
- Native ownership getters confirm all five items equipped on Hodram, type2/index1.
- All three newly inserted item names also match their compact inventory headings.
- The longest126-pixel equipment name remains complete in the fifth slot; the
  popup shifts left while retaining its full right border and final letter.
- All ten Sailor Info plaque regions match their current PXL asset pixel-for-pixel
  at native five-bit precision, including labels, borders and bevels.
- Healthy and Normal status words, and all ten full skill lines and numeric
  values, match independent native font masks.

The small label initially appeared abbreviated during visual inspection. Exact
source and glyph checks confirm **Swords**, matching original剣闘術 (sword-fighting
skill). Its six-character category wording fits the native field and matches the
existing Help terminology. No translation was changed from a visual guess.

## Evidence and limits

- Compatibility proof: `work/analysis/equipment_right_slots_v504/compatibility_proof.json`.
- Actual proof: `work/analysis/equipment_right_slots_v504/fixture_proof.json`.
- Verifier: `scripts/verify_equipment_right_slots_v504.py`.
- Capture report: `work/emulation_v193/equipment_right_slots_v504/capture_report.json`.
- Fixture helper: `scripts/native_inventory_fixture_v481.py`.
- Selected native images are saved under
  `E:\Rota Nova translations\Screenshots\Test fixtures\equipment-v504`.

The run cold boots without a savestate and terminates normally at7200. ROM/report/
PNG/RAM/donor hashes and bounded fixture writes pass. The helper/verifier pass Ruff.
Fixtures remain outside the normal-play guide archive. This is one officer with
Healthy/Normal conditions; other owners, alternate conditions, empty hints and
normal acquisition contexts remain open. All22 historical requirements and all18
plaque entries stay in the continued audit. At actual goal completion, revisit
older record-based checks.
