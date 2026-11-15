# Tavern announcement repair V383

Experimental combined candidate; graphics goal active. All 22 historical requirements
and all 18 incomplete plaque/hint entries remain. No canonical promotion occurred.

## Actual finding and source review

A normal Stockholm Tavern visit in the genuine older Hodram save triggered the
existing story event, then Order Drink and Treat Everyone. The accepted 208-coin
round exposed the mixed English/Japanese announcement `Today Bergstrom's 旦那 is
buying`. The following patron tip concerned Clifford's fleet heading to Bristol;
no weapon clue or equipment acquisition is credited.

Clean COMMON message 872 reads `はいよ / 今日は%sの / %sのおごりだ！ /
パーッとやってくんな！`. The original caller at `020584E0` supplies message 872,
the named affiliation/surname-style label in r2, and gender-dependent address in r3.
Its original literals at `02143C00` and `02143C08` are `旦那` and `姉さん`.
Those are familiar forms of address, not evidence of a marriage or sibling relationship.

Reviewed natural English: **This round's on %s. Enjoy!**
This keeps the current paid round, dynamic payer label and informal invitation.
The native caller and both arguments remain unchanged; the address argument is
unused. Ten actual SDK sprintf executions cover five names and both original
addresses, with exact complete output and preserved inputs, stack, registers and
buffer guards. The manuscript uses natural-dialogue-v2, clean source/adjacent
records, per-record review gates and one paragraph. Structural QA has no warnings
or errors; its informational change in line-break count is expected.

The text is shorter than its existing 45-byte allocation and padded within that
same span. No address-table, code, allocation or file-size change is made. All
3668 message positions, bounds and copy extents stay exact; only message 872's
content changes. All surrounding native messages are unchanged.

## Verification and failures retained

- The first research wording, `Drinks are on %s today! Enjoy!`, left an exclamation
  mark alone on the next line. It failed visual layout and was not released.
- An initial preparation script used record-relative offsets as block offsets.
  The full-message comparison rejected it before a research ROM was saved.
  The corrected script uses the verified `block_offset`.
- A failed emulator initialization occupied its isolated save folder; the revised
  research used a fresh folder. No existing save or capture was overwritten.
- The builder first finished ROM/manifest output but failed printing Unicode under
  Windows' default encoding. Its UTF-8 rerun finished with exit zero.
- Actual revised text has all 335 exact glyph pixels and blank cells at
  `[16,296,214,307]`, including its full stop and exclamation mark on the same row.
  All 37 comparable surrounding frames are unchanged. The next patron and return
  to the Tavern menu are unchanged.
- Final registered V383 is byte-exact to the verified research ROM. It passes 41
  complete Tavern replay frames and 23 New Game frames. All 470 inherited batches
  and every V378 native stage remain. Only `/COMMON/MESFILE.DK4` differs from V378;
  ARM9, all graphics, routes and other components are exact.
- Exact clean-input patch reconstruction, source locks, manifest/profile checks,
  targeted Ruff and integrated-builder syntax pass.

Evidence: `work/analysis/tavern_release_v383/release_proof.json`,
`work/analysis/tavern_round_v382/native_proof.json` and `live_proof.json`.
Scripts: `prepare_tavern_round_v382.py`, `verify_tavern_round_live_v382.py`,
`verify_tavern_release_v383.py`. These are targeted cold-boot emulator checks with
normal input, not complete routes or hardware tests. Other routes/custom-name
rendering and occupied Weapon/Armor contexts remain open. Older save history is unknown.

## Handoff

Candidate: `out/all_routes_combined_v383_candidate.nds`.
SHA-256: `2259d228e48f8294831d6aeceffbd32654b4502623513d51762387f7b0b512d2`.
Patch: `out/all_routes_combined_v383_candidate.xdelta`.
SHA-256: `a3158ebd53586750ad2abe28ea20e20adfc4a23f6c1539a2c1c50f2edf0ac071`.
Patch input: `work/clean.nds`, SHA-256
`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Profile: `all-routes-unified-v383`. Accepted layers remain baked into the canonical
base; all 470 inherited experimental batches and V378 stages remain. New reviewed
experimental stage: `translations/tavern_round_announcement_v1.json`.
The neighboring manifest lists all identities and changed records/files.

User cold-boot checks: title/New Game, established story/town, Tavern > Treat Everyone
with different captains, the patron tip/return transition, and ongoing plaque/equipment
variants. Explicit acceptance is required before canonical promotion.

Verified candidate, patch and manifest are copied with checked SHA-256 to
`E:\Rota Nova translations`. The finalized announcement PNG is copied unchanged to
its `Screenshots` folder for the future guide. Revisit older record-based checks at
actual full-goal completion.
