# V1492 promoted checkpoint and current research

On 2026-10-22 the user explicitly requested committing and pushing all work and
marking the latest build promoted. V1492 is the latest compiled registered build;
its exact ROM/patch hashes and promotion are recorded in
`translations/promoted_build.json`, the release registry's `latest_promoted_build`
and `releases/all_routes_unified_v1492/`. Tag: `promoted-v1492`.

This is a promoted cumulative checkpoint, not a declaration that localization or
all gameplay tests are complete. The immutable construction baseline remains
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
`accepted_baseline.json` and historical source locks are retained. The builder's
profile status remains `experimental` because its current schema requires that
value for every buildable profile; the separate promotion record is authoritative
for the user's checkpoint designation. No new user cold-boot result is inferred.

## Newly preserved original encounter

V1501/V1502/V1505 record an original neutral-faction declaration, natural battle
damage, automatic captain duel, defeat, flagship evacuation, retreat and normal
sailing with four surviving ships. The original flagship loses its crew while
retaining hull; the replacement destination is another ship, not a port. Sole
fixture: 40 prebattle own-ship location bytes. Actor identities, abilities, HP,
equipment, RNG and outcomes are not edited. The run terminates normally at frame
9200; input, whole 4MiB RAM, PNG and unchanged donor/save checks pass. This grants
no new completion credit to the 32 battle reactions, 16 sinking notices or 24
loss/surrender entries.

## Open retreat-name repair

The original first-mate caller selects 2683-2689; voice 3 falls back to 2683.
The observed Gerhard/voice-1 transfer selects 2684. V1492 displays Latina correctly
but native probes confirm names such as FALCON, ICARUS and FIFOFOFU can be consumed
as speech codes by this unscoped caller.

V1506/V1507 preserve source context and a seven-entry manuscript (three proposed
revisions, four retentions). V1509b/V1511b add an unintegrated 186-byte selector
within the existing 188-byte span; the 172-byte gate, allocations and staged size
remain exact. V1510 verifies 529429 native selector/ABI cases and inherited controls.
V1512 verifies 208 native/independent full font planes, 206 actor choices, seven
CPU-only role counterfactuals and 15 rejected compiler inputs. Four of eight review
sheets were viewed; four still await inspection. Automated bounds pass, but some
wraps strand clause heads such as Get/Fall on the preceding line. Visual refinement,
final manuscript approval, copy/cache regressions, registered integration and a
revised original transfer replay remain open. Failed initial 185-byte assumptions
are preserved as failed producers and superseded explicitly.

**These research bytes are not included in the promoted V1492 ROM or patch.**
The seven entries have not been added to the authoritative editorial ledger.
Counts remain 1323 complete (985 revised, 338 retained), 1467 source/prose reviewed
and 144 reviewed-incomplete COMMON entries. Broader shared/routes/raw review,
graphics/all 18 plaques and later older record-based re-audit remain open.

## Git preservation

All current source, manuscripts, scripts, tests and project documents are included.
Frozen source/evidence directories preserve exact bytes through Git rather than
normalizing line endings and invalidating stored hashes. Generated ROMs, raw RAM,
saves, dependency caches and bulk test captures remain on E; concise selected
verification records and the exact reconstructable patch are packaged in Git.
The two downloaded Chinese reference PDFs remain local, with their file hashes
recorded in `guide/references/other-versions/local_reference_checksums.json`; the
189 MB strategy guide exceeds GitHub's ordinary-file limit. Authored guide work,
source indexes and screenshots are included.
