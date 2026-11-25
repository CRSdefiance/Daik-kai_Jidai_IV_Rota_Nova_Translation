# Original environmental town assignments V425

V414 remains unchanged. This audit resolves the normal source assignments of the
retained facility icons and paintings; it does not credit actual visits or unlocks.

## Japanese-style facility icons

The original town constructor at020B6650 computes the current town index through
020B65E4. Its exact initializer at020B6674–020B668C sets fieldFF0 to1 only for
indices58–60. Caller020B6CBC passes that field to the facility constructor, which
stores it at894 and uses it for both image and caption-anchor selection.
Original town metadata names these towns **Nagasaki, Osaka and Naha**. All other
towns select the standard icon family. The alternate facility table selects
kbj04 for Tavern and kbj08 for Inn, as established by V206.

The initializer fragment executes for all114 indices in clean and current native
machines:228 cases. Only its four-byte field changes in the guarded supplied owner.
This is a supplied-index fragment test, not a complete live town construction.

## Retained paintings

Complete original020B7294 executes for all12 facility IDs and all86 towns with
static background selection, in clean and current machines:2064 matching results.
Original metadata determines whether non-port facilities use the adjacent street
painting; no invented state or replacement predicate is supplied.

| Painting | Original town | Facility IDs |
|---|---|---|
|32|Hangzhou|1,2,3|
|33|Hangzhou|0,4–11|
|35|Seoul|0,4–11|
|37|Osaka|0,4–11|

All four paintings and both Japanese-style icons remain byte-exact to the clean
ROM. The relevant current selector/constructor instruction ranges also match clean.
Towns86–113 have development-dependent branches and are explicitly excluded from
the background census. No conclusion about their variable backgrounds is made.

## Remaining verification

Capture ordinary visits to Seoul and Osaka to verify paintings35/37, and visits
to Nagasaki/Osaka/Naha to verify alternate icon and English caption composition.
Prior Hangzhou display and forced-icon Lisbon tests retain their documented scope.
These findings resolve unknown assignments; live GPU pixels, occlusion, input and
legitimate route progression remain open. All18 plaques remain fully_completed:false.
The full graphics goal remains active. Revisit older record-based checks at completion.

Verifier:scripts/verify_environment_assignments_v425.py. Proof:
work/analysis/environment_assignments_v425/assignment_proof.json. Targeted Ruff passes.

## Encounter continuation retained

V424 normally replays the Copenhagen donor through23200 frames. Normal Sea View
returns after the tutorial. At22000 Gerhard displays What's happening?!; later
sailing shows seven crew and a nearby ship. All67 capture hashes, the original
donor hash and unchanged V414 hash pass. No battle outcome, Lubeck docking, armor
acquisition or completed save is credited. The failed V423 zero-duration command
is excluded from finalized evidence. Proof:
work/analysis/lubeck_voyage_v421/continuation_proof_v424.json.
