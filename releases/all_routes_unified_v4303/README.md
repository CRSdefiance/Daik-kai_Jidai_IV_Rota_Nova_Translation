# Main promoted English build: V4303

Promoted on 2026-10-26 at the user's request. Tag: `promoted-v4303`.

This cumulative build contains 546 manuscript batches and 114 accepted layers, including completed Lil B170. Earlier releases and every local ROM and translation remain preserved.

## Apply the patch

Supply your unmodified Japanese ROM with SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`:

```powershell
python -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4303/translation.xdelta --out out/all_routes_combined_v4303_candidate.nds
```

Expected ROM SHA-256: `6e861308863c5e655aea9927364b2ad3e3bd6200e5cbe52c5bb7d789f4069abe`.

Patch SHA-256: `426885bf8defaa6a1a402e85505087ab3caa6aa32374730b90fbaafbaea5abd2`.

The complete clean-input patch was freshly reconstructed byte for byte at promotion. ROMs, saves and raw RAM captures remain local. Retained ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v4303_candidate.nds`.

## Verification and coverage

Registered profile: `all-routes-unified-v4303`. Against V4251 only SC2 B170 changes. All335 other SC2 blocks and every other file/component, ARM9, COMMON, fonts, graphics and123040 staged bytes remain exact. All33 complete native planes,264 logical/compiled and132 stored alignment cases pass.

Existing paired20001-frame Japanese/English content-fixture cold boots cover all33 B170 speeches, original presentations, pause, effects and normal town return. The first end is observed; the second has offline decoder coverage. Later SeaView outcomes differ consistently with documented scheduler entropy; focused repeats and persistent-state comparisons are retained without an equal-world claim. Two registered opening/town cold boots pass31 whole-frame comparisons andfive actor/captain checks. Viewed startup and completion receipts supersede historical pending flags. The inherited town battery is test data. These targeted automated headless emulator tests do not establish natural event eligibility, earned flags, full-route completion or hardware verification. Promotion adds no new emulator run or user cold-boot claim.

At promotion,78 integrated-release/dialogue regression tests passed.

## Unfinished work

The ledger retains5762 fresh contextual rereads:5725 completed and37 pending, with5765 source/prose reviews. B171 has37 contextual/native-approved speeches:24 revisions and13 justified retentions. **Those revisions are outside this ROM.** Relocation, stored references, representative gameplay and registered integration remain pending. See `verification/UNINTEGRATED_B171_status.json` for exact resume scope.

The full contextual editorial goal stays active across every remaining storyline, shared shop/town exchange, random scene, Help and other player-facing prose. B171 has37 pending reviews outside this ROM; B172-B180 has161 physical speech leads, not a full-project denominator. Preserve COMMON750-752, canonical Maria32 SC3B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency, Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques remain separate. Retain the later older-record technical re-audit/queued0D gap.

See the [current handoff](../../docs/editorial_handoff_current.md).

## Reproduction records

`build_manifest.json.gz` and `build_release_stack.json.gz` preserve exact original build-time bytes; decompressed hashes appear in `promotion.json`. The current registry changes only its promotion pointer. `checksums.json` covers every other packaged file. `verification/` contains scoped receipts, fresh reconstruction and final audit.

Immutable construction baseline: `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. Frozen builders, canonical inputs and accepted-layer status are preserved. Buildable profiles retain experimental status; `translations/promoted_build.json` designates the main build.
