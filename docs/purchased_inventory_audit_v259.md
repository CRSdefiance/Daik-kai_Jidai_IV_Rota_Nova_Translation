# V259 actual Guild purchase and inventory audit

V259 is gameplay evidence, not a new ROM. Current candidate remains
`out/all_routes_combined_v258_candidate.nds`, SHA256 `da3826983959c31104b7c1e3b66b65e3f69abb89fb71501a4d2a4c63a5bac613`.

## Ordinary navigation and acquisition

Two fresh DeSmuME cold boots use ordinary controller inputs, no loaded savestates
and no RAM injection. The first follows the established Square route and visits
actual facilities. UP from Square selects Guild; guessed spatial/icon associations
were not used as identity evidence. Buy Items is opened through normal dialogue.

The observed stock is Rainbow Marbles, Moya Lead and Old Dagger Map1. The Guild's
ancient-dagger pitch refers to a treasure clue: the actual item category is
**Ancient Map**, not Weapon/Armor. This actual observed stock is not inferred from
older Amsterdam stock notes. It supplies no occupied-equipment clearance.

Normal A confirmation accepts the3000-coin purchase; the Guild says Thank you.
The second cold boot replays the recorded purchase and returns through Guild/town
and the Info radial menu to actual player Items. Displayed funds change from35000
to32000. Those are observed values, not an independent internal-economy proof.
Frame32000 shows the acquired map in the player's one-item inventory.

## Exact full display evidence

The saved player-inventory screenshot independently matches the native font:

- Old Dagger Map1:191 ink pixels at x56,y24, five-pixel advance.
- Ancient Map:144 ink pixels at x8,y64, five-pixel advance.
- Map fragment. Collect all four.:317 ink pixels at x8,y112, five-pixel advance.
- All652 glyph pixels, including every first/internal/final character, match.
- Every1024 pixels of the32x32 image matches the unchanged native `/_pxl/item.pxl`
  atlas at native five-bit RGB precision. Unique matching index202; no transparency
  pixels or overlay mismatches are excluded. 

The original parchment illustration is retained; no graphic is rewritten from
this screenshot. Names/category/lore remain separate English text consumers.
The verifier checks report ROM hash, cold boot/no-savestate flags, terminal frame
count, callback errors, every captured PNG hash and incomplete plaque inventory.
Focused Ruff passes. Both capture processes ended normally and have final reports.

## Artifacts and remaining scope

- `scripts/verify_purchased_inventory_v259.py`.
- `work/analysis/equipment_purchase_v259/saved_live_proof.json`.
- Actual interactive schedules and PNGs under
  `work/emulation_v193/equipment_purchase_v259` and `purchased_inventory_v259`.
- Reproducible purchase/return schedule in
  `work/analysis/equipment_purchase_v259/purchased_inventory_inputs.json`;
  the second final report also records its additional interactive menu steps.

Occupied weapon/armor names and unknown hint widths remain open. A normal in-game
.dsv/.sav with equipped items has been requested while independent graphics work
continues. The acquired map cannot be used as a proxy for an occupied equipment slot.
All17 plaques plus Equipped Items and Armor/Weapon variants remain explicitly
**incomplete, pending continued audit** in both authoritative registries.
The broader graphics/source/native/gameplay goal remains active. No ROM, patch,
production code or canonical baseline changed in this evidence batch.
