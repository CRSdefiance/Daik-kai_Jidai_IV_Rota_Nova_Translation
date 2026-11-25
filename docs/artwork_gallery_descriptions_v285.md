# Native Gallery description composition V285

The preceding goal turn verified all164 scene captions through328 real native
selector-to-font cases. This turn covers the Gallery's four-captain description
array, including the V283 locked Rafael spelling.

## Verified path

`verify_artwork_gallery_descriptions_v285.py` executes native event-frame setup
42C2C..42CE4, selected-captain draw42F70..42FD0, original title strlen/centering,
array selection,456A0 wrapper, bitmap clearD393C, context initializationD5160,
font renderingD5404/D16B4 and cleanupD5140. All four descriptions pass on4-bit
and16-bit256x192 surfaces: eight complete title/description composites. All first,
interior and final letters, positions, tracking and complete independent pixels
match. The six unaffected Hodram/Lil/Maria format composites equalV275 exactly.

The initial fixture lacked the original declared overlay at01FFA000. Native
bitmap clear calls that overlay; loading its unchanged6208 bytes and32-byte BSS
resolves the fixture failure. This was a missing test fixture dependency, not a
newly diagnosed game defect. No clear, draw or context instruction is bridged.
A nonzero A5 canvas is fully cleared and painted; headers, surrounding guards,
native stack and caller registers remain intact. All328 V284 scene cases still
pass after the optional Gallery fixture extension. Ruff passes both scripts.

Evidence: `work/analysis/artwork_gallery_descriptions_v285/native_proof.json`.

## Limits and remaining release gates

Frame/index, bitmap, font metrics and overlay-loaded state are supplied native
caller fixtures. Actual unlock conditions, controller navigation, GPU routing and
live display are unproved. The user was asked for a normal unlocked Gallery save
as additional evidence. Work on other requirements can continue while it is pending.

No playable ROM, release profile, translation graphic or canonical baseline was
changed. The V283 name-caption patch still requires complete shared-name/route/
COMMON/HELP integration through the registered builder. V275 stays latest
playable. All18 plaques and Armor/Weapon variants stay incomplete, and the user's
low-resolution Online translation exception remains in effect. Full graphics
goal completion remains unproved. Revisit older record-based checks at completion.
