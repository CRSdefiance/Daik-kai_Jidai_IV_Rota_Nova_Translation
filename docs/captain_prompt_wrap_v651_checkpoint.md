# V651: complete captain-instruction modal word wrapping

V650's ordinary five-ship/dock run identified two real word splits. This batch
fixes their complete four-message family269..272 through the existing guarded
modal formatter. English wording, Japanese source meaning, fonts and graphics
remain unchanged. The full graphics goal stays active.

## Source and bounded repair

Original269 asks the player to choose the ship whose captain will change.
Original272 warns that changing the flagship may clear crew room assignments.
The reviewed English paragraphs remain:

- Choose the ship whose captain you want to change.
- Changing your flagship may cancel the crew's room assignments.

Original270/271 retain the existing subordinate/crew-selection instructions.
The source message IDs and packed COMMON entries are unchanged. Connected native
replays execute the original captain call fragments, real COMMON lookup, macro
expansion and dispatcher. Both actual problem calls establish parent020546E8.
The272 fragment explicitly supplies FP272 from the original MOV at0205A944;
this is not claimed as a complete captain-menu function replay.

Only the existing128-byte ITCM wrapper01FFC900..01FFC980 changes. Its new gate
adds269..272 to the existing127..134/321/327 scope for that exact modal parent.
Conditional copying fits the original owned span. No section, pool, cache, arena
or startup allocation grows. Every other ARM9 byte and every other ROM file is
exact V640, including all graphics and the complete COMMON text file.

All3668 native message IDs are exercised: exactly four gain wrapping and3664
retain byte-exact behavior.48 other-parent controls and nine empty/oversized
existing-wrapper cases pass. All four complete native text rasters retain glyph
order and keep each word on one row. The two short instructions have native
coverage; new actual screen-display coverage is claimed only for269/272.

## Actual complete screen and bitmap evidence

Four independent cold boots replay identical old/new inputs, without gameplay
fixtures or savestates:

- Two56600-frame five-ship/dock/captain/Save runs from isolated original donor copies.
- Two24100-frame ordinary New Game/story/town/Market runs without a battery save.

All89 unique New Game screen pairs are exact. Of154 unique fleet screen pairs,
149 are exact across both complete screens. The other five are32600,34800,35000,
35800,36600. Four show269; one shows272. Original full-line masks independently
confirm each old split. Every repaired glyph and blank cell matches the native
raster, with2660 complete ink-point comparisons across the five states. All
changed pixels are exactly the old/new glyph-mask symmetric difference; all
other screen pixels are exact. First/final glyph-erasure controls are rejected.
Both displayed lines share x22. The complete words and first/final characters
are preserved, including `want` and `the` on their continuation rows.

The first comparison expected only two changed captures. Three additional
captures visibly repeat269. That failed expectation and the review sheet remain
as diagnostics; all five receive the same complete checks, with no excluded
frames or pixels.

Actual captured CView geometry is228x48 inside288x48 backing storage. The original
font uses6x12 source cells, foreground index15/BGR5558020, and the original modal
compositor spaces12-pixel source rows16 pixels apart. Its frame origin0,96 plus
original16/8 text offsets gives the lower-screen view origin16,296 independently
of lettering. The inherited margin helper places both visible lines at22.

An initial generic bitmap model assumed16-pixel source rows/index1; its mismatch
is retained. The final replay executes the actual captured view, original context
setup, original prepared-text pointer and original6x12 font, without a text/getter
bridge. Both representative states match all10944 declared view indices each:
21888 complete native cells, full draw/ABI and backing guards. Undrawn60-column
storage padding is not assumed blank. This model correction requires no ROM or
font change.

## Reusable five-ship save

A separate fifth3200-frame cold boot loads V650's normal slot6 save into V651.
Original model getters verify Vestaros hull48/crew19 and four Latina hull25/crew0.
The source copied battery remains unchanged. The saved fixture is reusable, but
its support ships need crew before battle. No new battle, capture or loot-screen
coverage is claimed.

## Integrated candidate and handoff

- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v651_candidate.nds`.
- Candidate SHA256: `a11e57dfb6e021244122e002cd4804051db2298ae387b753eb16dc22ef6a573f`.
- Profile: `all-routes-unified-v651`, **experimental**.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`.
- Base SHA256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- All470 inherited batches and114 accepted layers retained, plus the named
  experimental `captain_prompt_wrap_v1.json` stage after the complete V640 stack.
- Only internal `/__arm9__.bin` differs from V640; its owned128-byte wrapper is
  the entire change. All921 decoded graphics views in675 containers and all57
  embedded preservation extents inherit byte-exact V640 contents.
- Patch: adjacent `all_routes_combined_v651_candidate.xdelta`, SHA256
  `6906b86f3d6cc26c7cd45bdc13777d76d333f83acd3745b15608a9285a561874`.
- Patch input: `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- Exact complete-ROM patch reconstruction passes. Neighboring manifest records
  the full release stack, batches, changed paths/records and enforced checks.
- Verifiers: `probe_captain_prompt_wrap_v651.py`, `probe_captain_caller_v651.py`,
  `verify_captain_prompt_wrap_v651.py`; Ruff passes for the changed implementation.
- User cold-boot review still required before acceptance/promotion: title/New
  Game, normal town menus, Dock > Captain instruction and flagship warning.

Proof: `work/analysis/captain_prompt_wrap_v651/release_proof.json`.
Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V651 Captain instruction wrapping`.
Two unmodified ordinary-input screenshots are also guide candidates, with
provenance; publication approval is not inferred. No commit/push or canonical
promotion. Only the latest compiled experimental pointer advances toV651.
All18 original plaques remain incomplete and all22 historical requirement
objects retain their scope. Miniature/Confirm parents, legacy/card/material
investigations, older-record review and final acceptance remain open.
