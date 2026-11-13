# Historical regression inputs

`historical_roms_v1.json` records nine original whole-ROM identities, their
canonical source, ordered batch recipes, source hashes and original manifests.
These inputs support legacy native-layout and audit regressions after generated
ROM retention removes the old `.nds` files.

`historical_fixture_support.py` replays only the allowlisted source-locked data
transformations, validates the original whole-ROM SHA-256, and caches the result
as `<sha256>.romfixture` under `out/test-fixtures/historical/`. No fixture is
accepted on the basis of a filename, a partial file match or the current ROM.
Corrupt cached inputs and changed canonical/batch sources are rejected.

These are historical test inputs. Some contain known bugs or retired text that
the current playable builder correctly refuses. They are never playable test
candidates, release parents or translation sources. Passing a historical
regression does not approve the archived release. The live release registry,
revocation checks and final story-percent guards remain unchanged; dedicated
negative tests retain their rejection behavior.

The ten migrated tests keep every original assertion. Only fixture acquisition
changes. Reproduction needs the project's original canonical ROM and the
hash-locked translation batches; no copyrighted ROM is checked into this folder.

The two September 18 route fixtures use archived ARM9 batch versions under
`historical_batches/`. Their original manifests predate nine dynamic-name
pointer additions, the full-width F name-pool revision, and two full-name
separator additions to batches that retained their filenames. The original
manifest record lists identify the earlier scope; replaying these records
reproduces both original whole-ROM hashes. These older records must remain
isolated here because the later runtime-name repairs are intentional.
