# Sail-angle caption V267

## Source and localization

Original 帆回転 means sail rotation. The source-locked cargo/sea UI batch identifies
it as the R-button sail-rotation command; the sailing tutorial specifies L for
left and R for right. L/R adjusts the sails. My prior interpretation as a camera
control was incorrect; that assumption is withdrawn. The unsuccessful V266 trip
is navigation evidence only and supplies no occupied-equipment clearance or proof
that the game's ship-control code is broken.

The footer now labels the controlled object **Sails**, making the L/R context
explicit. This replaces the ambiguous standalone Rotate caption. Logical English
is five letters; its stored sixth cell is blank, keeping the original measurement,
ASCII pair phase and eight-byte allocation. No other button caption or control
behavior is changed. The original source span, current bytes and its sole native
caption-table pointer are source-locked.

## Actual verification

An ordinary32720-frame DeSmuME cold boot follows the exact V266 controller/stylus
schedule. All55 native-font ink pixels of Sails match the independent ROM font in
eight captured footer states at x47,y370. Both leading and final S are complete,
and the padded sixth cell is empty. All76 other comparable whole frames are
byte-identical. In the eight changed frames, every differing pixel lies in the
caption's bounded39x14 region. Other footer controls, viewports, fonts, backgrounds,
numbers, story progression and captured actor states are unchanged.

The fullV263 build reproduces byte-for-byte through the shared builder. Every
file, route/COMMON record, artwork, ARM7, overlay and all native executable code
are exactV263. Only the existing eight-byte ARM9 caption allocation differs.
All467 inherited accepted/experimental batches, required stages and previous
changed records remain in the manifest. The clean-input patch reconstructs the
candidate exactly. Ruff passes the targeted module and verifier. These are targeted
emulator/display checks, not a completed route or hardware verification.

## Registered combined build

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v267` |
| Candidate | `out/all_routes_combined_v267_candidate.nds` |
| ROM SHA256 | `c5f506153f8bba73e9a19032726610602490e3e17db08118f5d0e6cabd364c1e` |
| Patch | `out/all_routes_combined_v267_candidate.xdelta` |
| Patch SHA256 | `9d4abbdf1e176eec33bce75182054ce3ca356fe632359915cb15dea2c481dcd5` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch input | `work/clean.nds` |
| Clean SHA256 | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Changed internal component versus V263 | ARM9 caption data only |

Experimental; user cold-boot acceptance pending and canonical unchanged. On the
user's emulator, check title/New Game, the established opening/town screens,
Sea View L/R caption and its complete letters, and the retained Deck View help.
The manifest beside the candidate lists all inherited and experimental batches.

## Continuing full goal

Both V266 navigation and V267 replay ended with final reports. V266 did not buy
or equip an item. The next ordinary voyage must use verified L/R sail-angle
controls and confirm wind/speed behavior; do not repeat the camera-control guess
or present either capture as occupied equipment. The requested normal equipped
save is still pending. Scurvy alert word wrapping remains to review.

All18 plaque/hint entries and Armor/Weapon variants remain incomplete in both
audits. Four Online body sources, raw comic/native display, other contextual/native
and gameplay checks, naming consistency and the full final graphics audit remain
open. Revisit older record-based checks at actual goal completion.

Proof: `work/analysis/sail_angle_v267/saved_live_proof.json`.
Verifier: `scripts/verify_sail_angle_release_v267.py`.
Source-locked release config: `translations/sail_angle_caption_release_v1.json`.
