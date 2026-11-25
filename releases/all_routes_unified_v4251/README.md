# Main promoted English build: V4251

Promoted on 2026-10-26 at the user's request. Tag: `promoted-v4251`.

This cumulative build contains 545 manuscript batches and 114 accepted layers, including the completed Lil B169 review. Earlier releases and every local ROM and translation remain preserved.

## Apply the patch

Supply your unmodified Japanese ROM with SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`:

```powershell
python -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4251/translation.xdelta --out out/all_routes_combined_v4251_candidate.nds
```

Expected ROM SHA-256: `ff9917225f4e8812ac890973c454a352b5416bee27a7263a5b3258efe9b91b12`.

Patch SHA-256: `49fca69ff751bc8228066b1b30b3fbcb3150a88ea35fa2cf57dc13ae3f9b7f90`.

The complete clean-input patch reconstruction was rerun byte for byte at promotion. ROMs, saves and raw RAM captures remain local. Retained ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v4251_candidate.nds`.

## Verification and coverage

Registered profile: `all-routes-unified-v4251`. Against V4204 only SC2 B169 changes. All 335 other SC2 blocks and every other file/component, ARM9, COMMON, fonts, graphics and the 123040-byte staged payload remain exact. All 36 complete native planes, 288 logical/compiled and 144 stored alignment cases pass.

Existing paired 20001-frame Japanese/English content-fixture cold boots cover 33 selected B169 speeches, original effects and normal town return. Three conditional remarks have offline native coverage only. Two further registered opening/town cold boots pass 31 whole-frame comparisons and five actor/captain checks. The viewed startup and completion receipts supersede historical pending flags. The inherited town battery is test data. These targeted automated headless emulator tests do not establish natural event eligibility, earned flags, full-route completion or hardware verification. Promotion adds no new emulator run or user cold-boot claim.

At promotion, 78 integrated-release and dialogue regression tests passed.

## Unfinished work

The ledger retains 5725 fresh contextual rereads: 5692 completed and 33 pending, with 5728 source/prose reviews. B170 has 33 pending speeches: 21 revisions and 12 justified retentions. **Those revisions are outside this ROM.** Contextual/native approval and research relocation, stored text, loader, reference and relocated-control checks are complete; representative gameplay and registered integration remain pending. The packaged B170 status gives exact resume references.

The full contextual editorial goal remains active across every remaining storyline, shared shop/town exchange, random scene, Help and other player-facing prose. B170 has33 pending reviews outside this ROM; B171-B180 has198 physical speech leads, not a full-project denominator. Preserve COMMON750-752, canonical Maria32 SC3 B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency, Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques stay separate. Retain the later older-record technical re-audit/queued0D gap.

See the [current handoff](../../docs/editorial_handoff_current.md).

## Reproduction records

`build_manifest.json.gz` and `build_release_stack.json.gz` preserve the exact original build-time bytes; decompressed hashes are in `promotion.json`. The current registry changes only its promotion pointer. `checksums.json` covers every other packaged file. `verification/` contains scoped receipts, fresh reconstruction and final audit.

Immutable construction baseline: `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. Frozen builders, canonical inputs and accepted-layer status are preserved. Registry buildable profiles retain experimental status; `translations/promoted_build.json` designates the main build.
