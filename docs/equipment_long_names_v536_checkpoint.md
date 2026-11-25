# V536: captain's five long equipped-item hints (V534 unchanged)

## Isolation and source-backed setup

Automatic approval review rejected an emulator command that named the original
Maria save, because it could be treated as a mutable battery-save target. A
separate byte-verified test copy was created first; the successful run names only
that copy. Both original and test-copy source hashes remain unchanged. The harness
also creates its own working battery copy. No original save or ROM is modified.

Current V534 support was added to the bounded inventory helper after its native
transfer/getter/history regions matched V502 exactly. A dry run and replay prove
the fixture changes only11 bytes within the five selected item records/history
vector. The items are Red-Haired Pirate Sword40, Saladin's Silver Armor71,
Alexander's Campaigns92, Self-Sharpening Plane98 and Aristarchus Telescope126.
This is synthetic inventory setup, not normal acquisition evidence.

Normal UI controls equip all five items on Maria. The action is **Y Equip**;
initial A attempts did not change ownership. The picker puts equipped items at
the end, so fixed right-arrow steps briefly toggled the telescope off. Those
attempts receive no occupied-slot credit. Selecting the first unassigned item
finishes the two remaining slots. Original native owner getters confirm type2,
actor3 for all five final items. Maria is the active captain, unlike the earlier
ordinary-officer/Hodram context.

## Complete actual display

| Item | Frame | Full paper rectangle |
| --- | --- | --- |
| Red-Haired Pirate Sword |15600|(16,208)-(158,224)|
| Saladin's Silver Armor |15400|(64,208)-(200,224)|
| Alexander's Campaigns |15200|(94,208)-(224,224)|
| Self-Sharpening Plane |15000|(94,208)-(224,224)|
| Aristarchus Telescope |14800|(94,208)-(224,224)|

All five complete text masks pass, including first/final letters and blank cells.
Every paper background, bevel and border pixel matches the native style. The
three accessory popups move left while retaining their complete right edge.
All5120 pixels of the five actual32x32 item icons match their original atlas.

Empty Weapon, Armor and Equipped Items hints also match complete wording and
their entire40/34/88-by16 paper rectangles. All ten Sailor Info plaques match
their current PXL source pixels. Healthy and Relaxed labels remain complete;
no condition injection was used. All ten skill labels and displayed numeric
fields pass full masks, including increased multi-digit values after equipment.
This does not independently verify combat/stat mechanics.

## Evidence and remaining scope

Verifier: `scripts/verify_equipment_long_names_v536.py`.
Compatibility, save-copy provenance, bounded transfer trial and final proof:
`work/analysis/equipment_long_names_v536`.
Actual run: `E:/Rota Nova translations/Generated/work/emulation_v193/equipment_long_names_v536`.
Selected labeled screenshots are archived at
`E:/Rota Nova translations/Screenshots/Test fixtures/equipment_long_names_v536`.
Targeted Ruff passes.

ROM remains experimental V534, SHA-256
`cac800924a1dfb3e2bc6352ef3f47f8f82986229377de20bc5e194046b5a6f45`.
Its patch/manifest and canonical baseline are unchanged. No V536 ROM is needed
for this evidence-only batch. Other items, owners, role/fleet/condition contexts,
normal acquisition and older legacy/restoration gates remain under audit. All22
historical requirements and all18 plaque/hint entries retain completion false.
Full graphics goal active; revisit older record-based checks after full completion.
