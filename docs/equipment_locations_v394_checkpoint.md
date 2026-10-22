# Source-backed equipment acquisition lead V394

Unchanged registered V388 is the candidate, SHA-256
`1629f2823aa953507c0ec3029556701509fd28d364824aefb6ce2aa61109abcc`.
No ROM, graphics, battery save or live emulator RAM was modified.

## Original native data

`scripts/verify_equipment_locations_v394.py` imports the verified read-only RAM
export from the genuine V393 Lisbon load into an isolated native machine. All218
original item category queries execute. Fifty-four records are Weapon or Armor,
including four additional Mystery Hunt items. Their original name, category,
price and location-descriptor getters execute with preserved ABI and output
guards. The complete captured4MiB RAM is unchanged after every query.

Golden Cutlass, item29, is the only Weapon/Armor record with descriptor type4
in this save. The original item-detail branch displays Price for this type.
It returns category2 (Weapon), price30,000 and location index22. Original accessor
`020CD6B8` selects the native116-byte city metadata row; that row names Istanbul.
The destination is therefore verified from this DS ROM and genuine save data,
superseding the earlier external walkthrough lead as a native location finding.

The other53 records return descriptor type6 in this snapshot. Extra fields in
that descriptor are unwritten; the harness initializes them with guard bytes
and does not interpret stale values as city IDs. The separate32-byte crew-name
table can contain city-related labels but is not used to determine destination.

Proof: `work/analysis/equipment_locations_v394/proof.json`.
Snapshot provenance: `work/emulation_v193/town_transition_v393_v388/capture_report.json`.
Targeted Ruff passes. Initial default-codepage manifest reading failed before any
native execution; the verifier now explicitly reads the UTF-8 manifest.

## Gameplay and remaining goal

This is a source-backed acquisition target, not an Istanbul arrival, observed
Guild stock, completed purchase or occupied equipment screenshot. The currently
captured Rafael save is in Lisbon; the saved Hodram voyage is in the North Sea.
Normal arrival, affordability/purchase eligibility, acquisition and equipping
still need gameplay evidence. No simulated equipment screen is added to the guide.

All eighteen plaque/hint entries remain `fully_completed:false`; Weapon/Armor,
further condition states and deeper original graphics contexts remain open.
All twenty-two historical requirements remain in the ledger. The graphics goal
is active and incomplete. Low-resolution Online translation remains user-exempt.
Revisit older record-based checks at full goal completion.
