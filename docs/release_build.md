# Integrated release-build policy

## Accepted parent

Every new playable ROM must descend directly from
`out/raphael_natural_v2_accepted_base.nds`, whose
SHA-256 is:

`c94e1fd7221c5e929c851a39f1e722c8b127992bea743dd9992ca1ff027afcdf`

This ROM is immutable. `work/clean.nds` is research input only and must never be used as
the parent of a playable candidate. Intermediate, probe, stage, and route-only ROMs are
not release parents.

## Authoring a new text batch

Export the target file from the accepted parent, not the clean ROM. For example:

```powershell
dk4tool extract-mesfile out/raphael_natural_v2_accepted_base.nds `
  --file-path /data/SC1.DK4 `
  --out work/baseline_sc1.csv
```

The JSON batch's `source_file_sha256` must be the SHA-256 of that exact internal file.
After one accepted release changes a file, later batches for the same file must be
rebased onto the newly accepted parent before they can be used.

## Building

Before building a new playable feature, register its complete batch set as a named
profile in `translations/release_stack.json`. Unregistered batches are rejected. The
only supported command for a playable candidate then uses that profile:

```powershell
python scripts/build_integrated_release.py `
  --profile feature-name `
  --out out/feature_candidate.nds
```

The accepted Options/UI, pair-phase renderer, Raphael route layers, and parity-safe
opening expansion are baked into the canonical baseline and therefore inherited
without being reapplied. Feature work with mutually dependent tables must use a named
profile.

The old `sound-setup` profile is source-locked to the former baseline and is marked
`rebase-required`. Do not run it: the integrated builder rejects it until the ARM9 SFX
table and packed BGM title table have been rebased and revalidated against the accepted
parent.

The former `raphael-full-natural-v2` profile is superseded, and the accepted parity
profile is marked `accepted-baked`. Both are deliberately rejected as new build
profiles because their changes are already present in the canonical baseline.

The revoked long-dialogue experiment remains registered as
`raphael-b44-long-dialogue-poc`:

```powershell
python scripts/build_integrated_release.py `
  --profile raphael-b44-long-dialogue-poc `
  --out out/raphael_b44_long_dialogue_relocation_poc.nds
```

Do not run this command. Cold-boot testing rendered one expanded record and then skipped
directly to town, proving the interior reference inventory incomplete. The map is now
marked incomplete, so the builder deliberately rejects the profile. It is retained in
the registry only to document the revoked experiment and prevent accidental reuse.

The phase-preserving follow-up is registered as
`raphael-b44-parity-relocation-probe` and produces
`out/raphael_b44_long_dialogue_parity_poc.nds`. Its map requires every relocated CS
record to preserve source byte parity and records any automatic one-space parity pads
in the manifest. It remains a disposable runtime probe until the complete opening and
transition beyond the fifth box pass from a cold boot.

The hybrid route profile `raphael-full-natural-v2-parity-opening` combines that
five-record opening expansion with all 299 non-overlapping, build-safe records from
the three reviewed Raphael v2 batches. The relocation batch explicitly overrides its
five compressed fixed-size counterparts. The builder applies relocation first, then
source-locks every fixed replacement against the canonical segments and verifies the
final hybrid SC0 exactly. Its candidate remains experimental pending a cold-boot route
test.

The dialogue audit fails closed if a pair-phase-protected first row is exactly 216
pixels wide before a newline. That layout would auto-wrap on the invisible phase byte
and then advance again on the newline, leaving a blank row in game.

The builder refuses any parent with the wrong ROM hash and refuses batches locked to a
different version of their internal file. Multiple batches targeting the same file are
combined against one verified source state.

For executable UI labels, use a source-locked `dk4-arm9-fixed-text-batch-v1` batch.
Every record declares an offset and the exact original bytes expected there; its English
replacement may only fit within that original byte range. This is the only supported way
to change ARM9 captions in a playable candidate.

Inline ARM9 renderer changes use that container with
`content_type: arm9-inline-code-v1`. Each record must declare a `runtime_address`
equal to `0x02000000 + offset` and an exact-width `replacement_hex`. The builder
rejects any such range overlapping runtime-owned data at `0x02171E48` through
`0x02172463`. The source-locked pair-phase repair lives in
`translations/dialogue_pair_phase_arm9.json`; include it only as a dependency of a
named dialogue profile, never as an ad hoc patch.

Before saving, the builder proves that:

- no undeclared ROM file changed;
- no undeclared ILNK record changed, even inside an allowed file;
- block and record counts did not change (a mapped relocation may change only its
  declared block size and dependent outer offsets);
- the accepted English main menu remains present;
- the baseline's accepted UI and graphics remain present;
- no additional `see below` fallback was introduced; and
- the saved ROM round-trips to the exact verified internal-file set.

Each successful build writes a neighboring `.manifest.json` containing the parent hash,
candidate hash, changed internal paths, exact changed record IDs, input batches, and all
passed checks. It also records the named profile and mandatory accepted layers. A
candidate without that manifest must not be handed off for testing.

## Promoting a new parent

Automated verification establishes that no past bytes were accidentally lost. It does
not replace emulator testing. A candidate becomes the next accepted parent only after:

1. its generated manifest passes review;
2. a cold-boot smoke test covers the title menu, character selection, one accepted story
   scene, town UI, and the specifically changed scene; and
3. the user explicitly confirms that build as accepted.

The user accepted the centered Lisbon tutorial-choice build on 2026-08-20 and promoted
its exact bytes to `out/raphael_natural_v2_accepted_base.nds`. The immediately previous
parent is retained as `out/raphael_natural_v2_pre_lisbon_accepted_rollback.nds` with
SHA-256 `fe7cdcaf7cfa24f18c1c48608ddddf58dc9a7555cb93c8131163037e814c8586`.
