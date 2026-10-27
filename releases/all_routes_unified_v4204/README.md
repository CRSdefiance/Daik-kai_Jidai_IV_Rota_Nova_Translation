# Main promoted English build: V4204

Promoted on 2026-10-26 at the user's request. Tag: `promoted-v4204`.

This cumulative build contains544 manuscript batches and114 accepted layers, including the completed Lil B168 review. Earlier releases and all local ROMs/translations are preserved.

## Apply the patch

Supply your unmodified Japanese ROM with SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`:

```powershell
python -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4204/translation.xdelta --out out/all_routes_combined_v4204_candidate.nds
```

Expected ROM SHA-256: `c4bf500bd4ab5a291259558188ce60d4560ffb85ab0c850714739c11c5de2670`.

Patch SHA-256: `92b8cf46009deeb7623b66dfc4a0390e711ca0c7a2f5fe1ca44ca954277380af`.

The complete clean-input patch reconstruction was rerun byte for byte at promotion. ROMs, saves and raw RAM captures remain local. Retained ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v4204_candidate.nds`.

## Verification and coverage

Registered profile: `all-routes-unified-v4204`. Against V4160 only SC2 B168 changes; all335 other SC2 blocks and every other file/component, ARM9, COMMON, fonts, graphics and123040-byte staged payload remain exact. All54 complete native speech/system planes,432 logical/compiled and216 stored alignment cases pass.

Existing paired20001-frame Japanese/English cold boots cover51 selected B168 speeches, original effects and normal town return. Three conditional remarks have offline native coverage only. Two additional registered opening/town cold boots pass31 whole-frame comparisons and five actor/captain checks. Viewed startup and completion receipts supersede earlier pending flags in the historical release/startup receipts. The inherited town battery is test data. These targeted automated headless emulator tests do not establish natural event eligibility, full-route completion, hardware verification or the item-information X mechanic. Promotion adds no new emulator or user cold-boot claim.

At promotion78 existing integrated-release, dialogue-review, wrapping, pair-phase, relocation and literal-guard tests passed.

## Unfinished work

The ledger retains5656 completed contextual reviews (3595 historically revised/2061 retained) and5659 source/prose reviews. B169 has36 draft objects:19 proposed revisions and17 justified retentions. **Those revisions are outside this ROM and remain uncredited.** Its automatic layout has three findings; full native/visual approval and later integration checks remain pending. The packaged B169 status identifies exact resume references.

Full contextual editorial review remains active across remaining storylines, shared shop/town dialogue, random scenes, Help and other player-facing prose. B169 has36 uncredited draft objects outside this ROM. Preserve COMMON750-752, canonical Maria32 SC3 B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency, Samwell full-catalogue middle-field lead, B157 provenance amendment, separate graphics/all18 plaques and the later older-record technical re-audit/queued0D gap.

See the [current handoff](../../docs/editorial_handoff_current.md).

## Reproduction records

`build_manifest.json.gz` and `build_release_stack.json.gz` preserve exact original build-time bytes; decompressed hashes are in `promotion.json`. The current registry changes only its promotion pointer. `checksums.json` covers every other packaged file. `verification/` contains scoped receipts, fresh reconstruction and final audit.

Immutable construction baseline: `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. Frozen builders, canonical inputs and accepted-layer status are preserved. Registry buildable profiles retain experimental status; `translations/promoted_build.json` designates the main build.
