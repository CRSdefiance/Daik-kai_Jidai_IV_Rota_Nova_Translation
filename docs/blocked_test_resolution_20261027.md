# Historical test blockers resolved — 2026-10-27

All ten files blocked in the patch interaction audit now pass: **47 recovered
tests, zero remaining fixture blockers**. The final targeted run passes **86
tests across 13 files**, including 14 new fixture safety tests and 25 existing
release/percentage guard tests. Every original assertion in the ten migrated
files is unchanged. No production code, playable ROM, release registry,
canonical baseline or cosmetic asset was changed for this recovery.

## Cause and repair

Retention had removed nine historical ROM inputs. Six historical profiles are
revoked; three others contain old story-percent text rejected by today's
playable builder. Rebuilding those as playable releases would violate the
current safeguards. The tests now obtain archival inputs through
`tests/historical_fixture_support.py` and its hash-locked recipes instead.

The helper replays allowlisted source-locked data transformations and accepts
only the **original whole-ROM SHA-256**. Cached inputs use `.romfixture`, with
explicit test-only receipts. They are never playable candidates or release
parents. Changed canonical sources, changed batch locks, altered cached bytes
and unknown fixture identities are rejected. Atomic publication is tested
with concurrent readers/builders. Six negative controls confirm that the
revoked playable profiles remain rejected. Existing release and story-percent
guard tests also pass unchanged.

Seven fixtures reproduce directly from retained batches. The two early route
fixtures required an older version of two ARM9 batches that had retained their
filenames. Their original manifests predate nine dynamic-name pointer additions,
the full-width F pool revision and two full-name separator additions. The older
records are frozen under `tests/fixtures/historical_batches/`; their complete
ARM9 record lists match the original manifests. Replaying them reproduces:

| Original input | Original and reconstructed SHA-256 |
|---|---|
| Hodram deep route V32 | `858bee37209a62767ee99c8dcb6a711ee9a586f589d0c1c4157c0ddc324df4f9` |
| Raphael deep route V93 | `66d2628477cbf2f9ed160d2f187722470a39b45ac9f1db33701d9ae04ff66c2e` |

The later name repairs remain in the active translation inputs. No source
hash, expected ROM identity, audit check or release rejection was weakened.

## Verification and limits

Run from the repository root with the project Python dependencies available:

```powershell
$env:PYTHONPATH='.;.runtime_deps;.deps;tests'
C:\Python314\python.exe scripts/run_blocked_tests_20261027.py --mode all
```

The runner uses one pytest process per file, preserving the native-engine
isolation used by the original audit. Its destination must be new; preserve
existing logs before choosing a new output directory for a repeat run.

Combining the previous audit's unchanged passing results with this run gives
**493 files, 2,457 passed tests and seven intentional skips**. This is combined
evidence, not a fresh execution of every file. The new run itself is 13 files
and 86 passes. It adds no emulator sessions, full-route coverage or gameplay
acceptance of the user's exact tutorial/crowd state.

The protected hashes remain:

- Square repair ROM: `89860905d61e348ae053d40836159bc86bff5d85d3206ce3a0961a6d60142077`.
- Canonical baseline: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Release registry: `c54902e5c82bf84fa16830f94dc200702308faa7af09509bcb53f84c4ba2ddf4`.

One initial test process exhausted memory while C: was nearly full. The old
generated audit capture tree was moved to approved E: storage, preserving all
4,783 file hashes and original paths through a junction. The affected test and
the complete final targeted run pass afterward. No original failure log was
discarded. The final retention preview succeeds: 473 ROMs retained, zero
deletions proposed or applied.

Machine evidence is under `work/blocked_test_resolution_20261027/`:

- `final_resolution_receipt.json`: counts, all nine original fixture identities,
  protected hashes and assertion-preservation result.
- `all/results.json` and individual logs: the final 13-file run.
- `combined_effective_results.json`: exact provenance for combined suite totals.
- `test_fixture_migrations.json`: unchanged original assertions.
- `audit_storage_move.jsonl` and `audit_storage_move_result.json`: storage move.
- `retention_preview.log`: final no-deletion retention plan.

The historical test blocker is closed. The Square repair remains experimental;
the gameplay and coverage limits in the original audit remain open. No cosmetic
change or promotion was made.
