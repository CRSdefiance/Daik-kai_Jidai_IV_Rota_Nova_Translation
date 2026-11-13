# V741 graphics review bundle — existing V712 ROM

This bundle contains the current experimental combined candidate. V741 is the packaging checkpoint; the playable ROM remains V712 with exactly the same bytes. The graphics goal remains open for the unresolved display contexts and final review.

## Open and test

Folder: `E:/Rota Nova translations/Review candidates/V741 Graphics review (V712 ROM)`

1. Open `all_routes_combined_v712_candidate.nds` in your emulator from a power-off state. Start without a savestate.
2. Check the opening logo, Press START screen and main menu. Advance into New Game.
3. Select Lil and check the captain confirmation and first dialogue for complete leading/trailing letters and readable layout.
4. When available, open Assign Sailors and Sailor Info. Check plaque wording, texture/borders, stat labels/bars and equipment hint paper. Existing saves may be tested using a separate copy.
5. Report the emulator/version, the last successful screen and any defects. These short checks provide user cold-boot evidence for these contexts; the remaining original comic/control/card/legacy contexts are listed in the audit snapshot.

## Exact identities

- Candidate: `all_routes_combined_v712_candidate.nds`
- Candidate SHA-256: `6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030`
- Registered build base: `raphael_natural_v2_accepted_base.nds`
- Build-base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Profile: `all-routes-unified-v712` (experimental)
- 114 accepted layers are already baked into the canonical base; 470 registered experimental batches are applied in manifest order. `applied_layers.json` lists every layer, changed internal file and changed record.
- 53 changed internal files relative to the registered base.

## Reconstruct from the exact patch

The build base and patch input are different: the supplied xdelta patches the clean Japanese ROM. Supply your exact clean source with SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`. With xdelta3 available, run in this folder:

```powershell
xdelta3 -d -s "path/to/clean.nds" "all_routes_combined_v712_candidate.xdelta" "reconstructed.nds"
Get-FileHash -Algorithm SHA256 -LiteralPath "reconstructed.nds"
```

The reconstructed hash must equal `6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030`. The prior V721 reconstruction is still byte-exact to this packaged ROM; the unchanged patch and ROM are verified on copy.

## Verification carried forward

The original neighboring manifest records its passing build guards. The V737 reproduction manifest and proof record the added final graphics-copy gate, its 12 corruption controls and a complete registered rebuild byte-exact to V712. V736 records current plaque contexts; V740 records the stored palette-domain inspection. Testing includes targeted emulator runs and declared fixtures, with their limits retained in the audit.

Four low-resolution Online bodies remain excluded. Approved brown marks remain preserved. All 18 original plaque/hint audit objects retain final sign-off pending. The canonical base and original saves are unchanged.
