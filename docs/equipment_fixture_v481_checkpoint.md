# V481 inventory fixture and item-name coverage

ROM remains V474, SHA-256
`1d513b81762499f0fd6a2edeeabb182a69c334756fc9261f70c07a0110984b9e`.
No ROM changes or canonical promotion.

The user explicitly authorized adding items to inventory to speed up testing.
Fixtures use a copied genuine battery save and the original native transfer
routine at 02049F30. Only equipment categories 2/3/4 are accepted; equipped items,
invalid IDs and non-equipment are rejected. Only the selected item records and
native acquisition-history bit vector may change. This does not establish normal
acquisition, route completion, Gallery or ending unlock behavior.

The emulator requires `--allow-inventory-fixtures` and an interactive command
such as `{"until":3300,"inventory_items":[40,71,83],"buttons":["X"],"duration":8}`.
Every change is included in `synthetic_inventory_fixtures` in its capture report.
The normal guide archiver rejects these reports. Original donor saves are intact.

## Verified coverage

- All 218 original item names: current native getter, measured size, complete
  native raster including first/final glyphs, unchanged source RAM.
- 1,090 native tooltip placement contracts: five anchors per name, paper width
  equals measured text width plus four, inside the native clip bounds. This does
  not assert every item is eligible in each equipment slot.
- Actual DeSmuME fixture captures on Hodram: Red-Haired Pirate Sword (longest
  weapon name), Saladin's Silver Armor (longest armor name), Rocco's Sailing Guide.
  All three inventory names and equipped tooltip names are exact; the tooltip
  paper/corners and all three 32x32 icons match. Native ownership getters confirm
  equipment on Hodram. Total tooltip ink: 731 exact pixels.

Proofs: `work/analysis/equipment_names_v481/name_proof.json` and
`work/analysis/equipment_names_v481/fixture_proof.json`.
Verifiers: `scripts/verify_equipment_names_v481.py` and
`scripts/verify_inventory_fixture_v481.py`.
Capture report: `work/emulation_v193/inventory_fixture_v481_live/capture_report.json`.
Test images are saved separately under
`E:\Rota Nova translations\Screenshots\Test fixtures\equipment-v481`.

## Remaining audit

All 22 historical requirements remain; all 18 plaque entries stay incomplete.
Other names, owners, conditions, normal acquisition and wider graphics contexts
remain open. CPU contracts and these three GPU captures do not prove a complete
playthrough or hardware behavior. The full graphics goal remains active.
At actual goal completion, revisit older record-based checks.
