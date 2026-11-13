# Complete roster role crop V341

## Observed defect and shared correction

Ordinary V340 playback shows **First Ma** on Gerhard's roster card, while Sailor
Info correctly shows First Mate. Independent font masks confirm that the roster
contains all94 prefix pixels but lacks the final two letters.

The shared roster composition descriptor at ARM9 offset14F4B0 has three rows:
role48x12, stat60x12 and name204x12. The role crop, rather than its stored English
name or font, removes those letters. Its width word at14F4C4 changes from48 to204.
This adopts the already-established full name-row width and fits the complete16
shared role names plus longer ship/rank captions returned by the same producer.
The initial96-pixel research crop covered the16 table roles; reviewing the other
producer formats led to the full204-pixel correction before any handoff.

All strings, font code, original role selection, cache/pool allocation, backing
bitmap, other crop rows, coordinates, flags and artwork are unchanged. Only one
four-byte width word changes. The crop remains inside the existing204-pixel
caption extent and ends at screen x216, without reaching the next text row.

## Evidence

-32 complete native role rasters pass in4-bit and16-bit formats, with original
 odd-length padding retained and every first/final letter and blank cell present.
-14 further native cases cover the producer's existing ship/rank formats with
 supplied18-letter names and F/I-initial captions. Those are bounded fixtures,
 not every actual fleet state.
-The real roster now matches all119 First Mate pixels at(12,316), including the
 missing25 pixels. Two comparable frames change only those25 role pixels.
 Other56 comparable saved-game frames are exactV340.
-Thirty complete plaque instances across Gerhard, Manuel and Charles match their
 integrated source-locked assets. All18 ongoing plaque/hint entries remain
 incomplete, as explicitly requested by the user.
-All81 comparable frames from a separate31200-frame fresh New Game run matchV340,
 including title, captain selection, opening, town and sailing.
-Both emulator runs terminate normally without callback errors or loaded savestates.
 The original cartridge save remains unchanged; its earlier progression is unknown.
-No RAM injection, save editing, artificial unlock or synthetic role assignment
 is used for the actual screen captures.
-CompleteV340 reproduces byte-exact. All470 inherited accepted/experimental batches,
 required layers and prior stages/records remain. Only ARM9 changes. The clean-input
 patch reconstructs V341 exactly. Focused Ruff passes.

## Conditional diplomacy findings

The actual Sailor Info screens show Speech112 for Gerhard,110 for Manuel and108
for Charles. Clean source confirms skill index7 is説得力, Speech. Reassigning these
officers does not provide Speech200 or create eligible foreign factions.

The unmodified eligibility function0205BB4C executes separately against a read-only
captured runtime state. Its mode0-5 eligible target counts are1,1,0,0,1,1; native
nonempty lists contain opaque target ID5. No faction identity is invented from that ID.
Sign Pact needs at least two eligible targets plus Speech80. Break Pact needs an
eligible target and Speech100. Truce needs an eligible target and Speech120.
Threaten also has a Speech200 gate and additional original conditions. These
findings explain the missing commands under this captured state. They do not
verify their unavailable actual displays or alter live gameplay state.

## Integrated experimental candidate

| Artifact | Identity |
| --- | --- |
| ROM | `out\all_routes_combined_v341_candidate.nds` |
| ROM SHA256 | `5ec1616e74b12ecece040aa83d3325cc07be55d31b6f3c05c2bc547b6884f5dd` |
| Patch | `out\all_routes_combined_v341_candidate.xdelta` |
| Patch SHA256 | `7aad2f52d5917757ec8c1e676b1911d4aa9dc36c08d3f4c6f6ecc04f78c42b57` |
| Profile | `all-routes-unified-v341` |
| Canonical base | `out\raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |

The manifest lists all inherited accepted/experimental batches and the new crop
stage. The canonical baseline remains unchanged; V341 is experimental until user
cold-boot acceptance. Test title/New Game, town navigation, roster role labels and
Sailor Info. This is targeted automated emulator verification, not a complete
route or physical-device test.

Both graphics audits and progress documents are updated. Occupied weapons/armor,
alternate conditions, unavailable diplomacy commands, regional/legacy map viewers,
other embedded-art/ending/Gallery contexts and the remaining requirements stay
open. Low-resolution Online images remain user-exempt. Revisit older record-based
checks at actual full-goal completion.

Evidence: `work/analysis/roster_role_crop_v341/release_proof.json`, `native_proof.json`,
`rank_ship_caption_proof.json`, `conditional_guild_v341/actual_state_eligibility.json`,
source captures in `work/emulation_v193/conditional_guild_v341` and the two V341
capture reports. Reproduce with `scripts/prepare_roster_role_crop_v341.py` and
`scripts/verify_roster_role_crop_v341.py --live`.
