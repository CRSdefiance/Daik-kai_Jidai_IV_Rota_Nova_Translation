# Main promoted English build: V4160

Promoted on 2026-10-26 at the user's request. Tag: `promoted-v4160`.

This cumulative build contains 543 manuscript batches and 114 accepted layers, including the completed Lil B166 and B167 reviews. Earlier releases and all local ROMs/translations are preserved.

## Apply the patch

Supply your own unmodified Japanese ROM with SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`:

```powershell
python -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4160/translation.xdelta --out out/all_routes_combined_v4160_candidate.nds
```

Expected ROM SHA-256: `22fb73b7067fc9c5f7f59383efdf9fabc233cff3d6a0391092a7a690959f3425`.

Patch SHA-256: `854fe3cf7229a829e76c9388807e0cea04ee874ca8a903cb14ebce7c320f7763`.

The complete clean-input patch reconstruction was rerun byte for byte at promotion. ROMs, saves and raw RAM captures remain local. The retained ROM is `E:/Rota Nova translations/Generated/out/all_routes_combined_v4160_candidate.nds`.

## Verification and coverage

The registered profile is `all-routes-unified-v4160`. Against V4110 only SC2 B167 changes; every other file/component, font, graphic, ARM9 and 123040-byte staged payload remains exact. Existing B167 tests include four 14401-frame Japanese/English cold boots covering both menu outcomes, 25 distinct speeches/28 English observations and both normal town returns. Two alternative Cesare remarks have offline native coverage only. Two additional registered opening/town cold boots pass 31 whole-frame comparisons and five actor/captain checks. The inherited town battery is test data, not earned progress. These targeted automated headless emulator tests do not establish natural event eligibility, full route completion or hardware verification. Promotion adds no new emulator or user cold-boot claim.

At promotion, 78 existing integrated-release, dialogue-review, wrapping, pair-phase, relocation and literal-guard tests passed. The packaged existing release/startup receipts and viewed startup sheet preserve their original scope.

## Unfinished work

The ledger retains 5602 completed contextual reviews (3567 historically revised/2035 retained) and 5605 source/prose reviews. B168 has 54 draft-reviewed objects (28 proposed revisions/26 justified retentions). **Those revisions are not in this ROM.** Offline checks pass 54 native planes and 432 alignment cases. Final visual approval and subsequent ledger, relocation, representative gameplay and registered release gates remain pending. The packaged B168 status identifies exact resume references; its native proof is explicitly labelled unintegrated.

Full contextual editorial review remains active across every remaining storyline, shared shop/town dialogue, random scene, Help and other player-facing prose. B168's 54 draft-reviewed objects remain unintegrated and uncredited. Preserve COMMON 750-752, canonical Maria SC3 B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency, Samwell's full-catalogue middle-field lead, B157 provenance amendment, separate graphics/all 18 plaques and the later older-record technical re-audit/queued 0D gap.

See the [current handoff](../../docs/editorial_handoff_current.md).

## Reproduction records

`build_manifest.json.gz` and `build_release_stack.json.gz` preserve the exact original build-time bytes; decompressed hashes are in `promotion.json`. The current registry changes only its promotion pointer. `checksums.json` covers every other packaged file. `verification/` contains scoped receipts, the promotion reconstruction and final audit.

The immutable construction baseline is `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. This checkpoint promotion preserves frozen builders, canonical inputs and accepted-layer status. Buildable profiles retain the registry schema's experimental status; `promoted_build.json` designates the main build.
