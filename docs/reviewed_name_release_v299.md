# Reviewed name/text/art migration V299

The complete registered candidate combines all 444 reviewed route paragraphs,
five shared name fields, six COMMON messages, eight HELP pages and the inherited
16 artwork name captions. Rafael, Joakim, Camille and Maria Li now use the user's
locked spellings in ordinary shared names as well as the reviewed prose/artwork.
Every revised paragraph retains the source meaning and complete natural English;
none was shortened to fit storage.

## Candidate and ancestry

| Item | Identity |
|---|---|
| Candidate | `out/all_routes_combined_v299_candidate.nds` |
| ROM SHA256 | `9f551e849f7cb8fbabee2bb4e9586fb527789c4b8a0ed97c084a21adaa49768f` |
| Patch | `out/all_routes_combined_v299_candidate.xdelta` |
| Patch SHA256 | `36e853b6bac16acb9a62c078c35f1e66f74e319f4d3d8edaf8b814ba94f28a32` |
| Profile | `all-routes-unified-v299` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Inherited comparison | `out/all_routes_combined_v298_candidate.nds` |
| Comparison SHA256 | `0e57a87c72d711b3cab3ac29ea8c7bb51c1ab1fd3b30ac3551983d1ee31a5a5b` |
| Clean patch input | `work/clean.nds` |
| Clean SHA256 | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Status | Experimental; canonical base unchanged; user acceptance pending |

The manifest contains all 467 inherited batches and every accepted requirement,
registry/config/dependency hashes, every inherited stage and changed record IDs.
The new stage follows the complete V298 artwork-caption and V296 actor repairs.
Full V298 reproduces byte-for-byte before and after shared builder changes. The
clean-input patch reconstructs V299 exactly. No layer was promoted as accepted.

## Changed files and preservation

Only ARM9, SC0/SC1/SC2/SC3, COMMON/MESFILE and COMMON/HELP change versus V298.
All graphics, fonts, other data files, ARM7, overlays, banner and entry addresses
remain exact. All 197 fixed route edits preserve allocation, every block/archive
extent and following native command address. The 247 full catalog paragraphs use
467 route-scoped keys. A census after fixed edits verifies all intended owners,
no unintended active route matches and two rejected foreign-route matches. All
COMMON messages were also checked for unintended catalog matches: none.

Five shared slots preserve original table pointers, capacities and sole native
ownership: Rafael, Camille, Joakim, Maria's surname Li and middle name Huamei.
All 19,254 original native actor fields are verified against clean source and
stable byte positions; consumed alignment NULs do not shift that actor audit.

Complete NUL-terminated suffixes share storage without truncation. The owned pool
is 120,000 bytes with 8,992 bytes before staging; its inherited 82,880-byte caption
payload prefix remains intact. Native staged loading/cache checks pass. Six COMMON
messages reblock as complete owned records with all 3,662 other messages and their
padding exact. The directory and COMMON bytes match the earlier V276 native proof.
HELP has the exact eight prepared pages, original cross-reference IDs, article
continuations and topic-203 history sentinel from the V282 actual navigation proof.

## Native verification

- 5,604 aligned/caller lookup cases, 1,868 route masks and 1,401 fallback/near-miss
  cases pass with full input/target/register/stack/return guards.
- 5,604 native catalog copies/expansions and all 444 complete route glyph bodies
  pass independent pixels, visible cell bounds/order and full first/final letters.
- All 621 native name getters pass: five changed and 616 unchanged outputs.
- All 18 COMMON warm/cold/neighbor copies pass. Actual modal preparation,
  context/renderer/font/cleanup paths pass for six full bodies on both bitmap
  formats and both portrait variants: 24 complete pixel cases.
- All 328 scene-caption selections and eight Gallery composites remain exactly
  V298 after the larger pool is installed.

The earlier COMMON pixel failure came from sending unwrapped COMMON prose to the
narrow 216-pixel story primitive. The actual COMMON modal path wraps and preserves
all glyphs. This diagnostic remains documented rather than claimed as a game defect.
The new dedicated modal harness executes only source-locked alignment/cursor helper
instructions in the inherited owned pool. The historical item raster harness was
restored byte-for-byte after the builder rejected its script hash change; no item
evidence checks were bypassed. Refactored cursor helper generation reproduces the
historical V272 target exactly. Ruff passes.

Route expansion uses controlled current code and prior captured player data; it
does not prove that all original deep scenes have been played. Native caption
selectors likewise supply caller frames/indexes/views and do not prove unlocks.

## Fresh ordinary gameplay evidence

Production Rafael and Hodram complete 6,000-frame cold boots. Production Lil
completes 20,000 frames through title/New Game, selection, opening, Amsterdam
sign/shop UI. Maria completes a 6,000-frame declared selection test fixture with
one byte at ARM9 `0x9F068` changed from the three-captain limit to four. This is not
a legitimate unlock or playable handoff. No run loads a savestate or injects RAM.
All four processes exit successfully and callback errors/capture hashes pass.

Live frames show the Camille Overijssel nameplate and Rafael's new name in
Claudio's opening dialogue. All 196 Camille nameplate pixels and the complete
Rafael dialogue and Amsterdam shopkeeper text match independent native font
pixels. Results are recorded in `release_proof.json`. The first HELP replay did
not open HELP because old one-frame input events were missed in the changed game
state. It is retained as a failed navigation attempt, not evidence of HELP display.
A fresh step-by-step 30,400-frame navigation run uses ordinary eight-frame button
events. All eight revised HELP pages preserve the complete title and all ten
body rows, matching the previously independently verified captures. Both article
start return links restore complete body pixels. The L/R footer availability
changes with navigation history and is explicitly excluded from the identical
pixel claim. Successful pages were visually inspected. All five successful
processes exited; the separate failed HELP navigation attempt is retained as such.

## Remaining goal gates

Experimental: user cold-boot acceptance, original deep scenes and legitimately
unlocked Gallery navigation/composition remain open. Test new games, normal
dialogue/nameplates and HELP continuation/return links on the user's emulator.
All 18 plaque/hint entries and Armor/Weapon variants remain open for continued
audit. Broader native graphics consumers/crops still need completion evidence.
The eight Japanese HELP topics and 79 generic entries identified in V282 remain
unfinished; this migration does not claim complete HELP translation. Low-resolution
Online promotional images remain exempt by direct user instruction.

The full graphics goal remains active and incomplete. At actual completion,
revisit older record-based checks as requested. Evidence is under
`work/analysis/reviewed_name_release_v299` and the corresponding fresh
`work/emulation_v193/reviewed_names_v299_*` captures. No Git push was requested in
this continuation.
