# V831: Refit help editorial completion

All31 help descriptions (1247-1255 and1268-1289) are reviewed against clean
Japanese:18 revised and13 retained. Full source/current references, glosses,
decisions and generated lines are in `translations\refit_help_editorial_final_review_v1.json`. Spoken1256-1267 and separate
HELP articles are outside this family and remain part of the wider review.

## Meaning and formatting

The revisions clarify cure versus treatment, slower fatigue, following winds,
alternative stern fittings and the final sail's square-sail identity. All room
limits, equipment names and directional restrictions are preserved. Four initial
single-word tails were resolved through natural prose, without authored breaks
or alignment. All31 current native complete font planes match562464 independent
pixels with complete leading/trailing letters, guarded buffers and blank later
heading/detail rows.

The original block16 would be4098 bytes, four beyond the4096-byte cache bound.
Complete native selections are repacked in existing blocks16-18;403 selections
move,18 text strings change and3650 remain exact. All opaque spans and the other
38 blocks are exact. All7336 native warm/cold copies pass. Only COMMON and ARM9
directory/offset metadata differ from V829. Executable code, fonts, BSS, memory
bounds, caches and the123040-byte late payload remain unchanged. All graphics,
HELP, SC0-SC3 (including the V829 cliff fix), ARM7 and overlays are exact.

## Actual emulator verification

Paired20600-frame cold boots use an unmodified disposable copy of the existing
five-ship Copenhagen test save; no new gameplay RAM/code fixture or savestate.
23 complete help holds cover13 distinct messages, including9 revised texts.
Independent glyph/background models match every pixel of all62 captured screen
pairs. All first/final glyph erasure controls fail as expected. Entry, normal
cancel, Shipwright and Port return pass;five ship models and25975 funds match
at six checkpoints. Seven ordinary4000-frame startup/New Game capture pairs
without a save or fixture match. This is targeted testing, not31 ordinary visits,
a full playthrough or hardware verification. All31 have controlled native tests.
The12-screen actual contact sheet is visually reviewed.

An initial verifier called the fleet helper with the wrong arguments. Its
signature was corrected, capture RAM hashes checked, and verification rerun on
the same terminal captures; no successful emulator run was restarted or retimed.

## Registered release

- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v831_candidate.nds`
- SHA-256: `3d6f3d28deedb42f9d5c333fd5a70b0722438f04e76a089b84672c2299c84d95`
- Profile: `all-routes-unified-v831` (experimental, not canonically promoted).
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`.
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- All471 batches and114 accepted layers retained; prior profiles untouched.
- Changed internal components relative to V829: `/COMMON/MESFILE.DK4`, `/__arm9__.bin` metadata.
- Exact clean-input patch: `all_routes_combined_v831_candidate.xdelta`.
- Patch SHA-256: `03d8906c174f87fb32d27a201a26a87d8219d00d9003ac6d382ca40bceb977be`.
- Clean input SHA-256: `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The registered binary verifier replays the late stage, checks complete preservation
and prior registry ancestry, rejects wrong source COMMON/ARM9 and stale current
records, and reconstructs every candidate byte from the clean-input patch.
The neighboring manifest and `registered_release_verification.json` record the
full stack. Human cold-boot acceptance remains required before canonical promotion.
For that review, inspect New Game and Refit equipment/room descriptions and exit.

## Remaining work

634 completed entries (456 revised/178 retained),637 source/prose reviewed,
three older750-752 drafts pending. Remaining shared, all other route/player prose,
and the raw-source coverage revisit stay open. Graphics and all18 plaques remain
separately unfinished. The older record-based checks must be revisited after the
full goal. Source/manuscript/proofs and guide-candidate captures are archived on E:.
