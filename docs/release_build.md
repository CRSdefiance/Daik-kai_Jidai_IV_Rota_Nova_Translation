# Integrated release-build policy

## Accepted parent

Every new playable ROM must descend directly from `out/all_goods_roundtrip.nds`, whose
SHA-256 is:

`8e61fd4e8c444b25566cc273dd676b3e5bea5d683ad167db2f92444c10df9764`

This ROM is immutable. `work/clean.nds` is research input only and must never be used as
the parent of a playable candidate. Intermediate, probe, stage, and route-only ROMs are
not release parents.

## Authoring a new text batch

Export the target file from the accepted parent, not the clean ROM. For example:

```powershell
dk4tool extract-mesfile out/all_goods_roundtrip.nds `
  --file-path /data/SC1.DK4 `
  --out work/baseline_sc1.csv
```

The JSON batch's `source_file_sha256` must be the SHA-256 of that exact internal file.
After one accepted release changes a file, later batches for the same file must be
rebased onto the newly accepted parent before they can be used.

## Building

The only supported command for a playable candidate is:

```powershell
python scripts/build_integrated_release.py `
  --base out/all_goods_roundtrip.nds `
  --batch translations/example_baseline_batch.json `
  --out out/example_integrated.nds
```

The builder refuses any parent with the wrong ROM hash and refuses batches locked to a
different version of their internal file. Multiple batches targeting the same file are
combined against one verified source state.

For executable UI labels, use a source-locked `dk4-arm9-fixed-text-batch-v1` batch.
Every record declares an offset and the exact original bytes expected there; its English
replacement may only fit within that original byte range. This is the only supported way
to change ARM9 captions in a playable candidate.

Before saving, the builder proves that:

- no undeclared ROM file changed;
- no undeclared ILNK record changed, even inside an allowed file;
- block and record counts did not change;
- the accepted English main menu remains present;
- the baseline's accepted UI and graphics remain present;
- no additional `see below` fallback was introduced; and
- the saved ROM round-trips to the exact verified internal-file set.

Each successful build writes a neighboring `.manifest.json` containing the parent hash,
candidate hash, changed internal paths, exact changed record IDs, input batches, and all
passed checks. A candidate without that manifest must not be handed off for testing.

## Promoting a new parent

Automated verification establishes that no past bytes were accidentally lost. It does
not replace emulator testing. A candidate becomes the next accepted parent only after:

1. its generated manifest passes review;
2. a cold-boot smoke test covers the title menu, character selection, one accepted story
   scene, town UI, and the specifically changed scene; and
3. the user explicitly confirms that build as accepted.

Until all three happen, keep using `out/all_goods_roundtrip.nds` as the parent.
