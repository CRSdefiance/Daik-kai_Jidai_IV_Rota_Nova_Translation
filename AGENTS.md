# Release-build invariants

For extended resume configurations that also carry `percent_relocation_guard`,
use the versioned v6 chain. It preserves the original final-stage bodies and
binds the original story-format check to exact clean and final offsets for the
relocated source speaker controls. Carry the qualified proof forward only while
its owned blocks and controls still match. See `docs/build_continuity_protocol.md`.

For extended resume configurations containing `prepared_profile`, use the current
`scripts/resume_extended_release_with_Fernan_field_v3.py` chain and
`registered_canonical_extension_resume_v3.py`. It preserves the v2 guards and
additionally compiles the indented original extension block in its proper function
context. The v2 attempt failed before producing a canonical ROM; retain it as
failure evidence. A same-checkpoint configuration without an appended transaction
continues to use the separate validated v1 resume workflow below.

The v2 `resume_extended_release_with_Fernan_field_v2.py` chain additionally
permits one registered source-bound late editorial transaction after an exact
verified canonical prefix. `registered_canonical_extension_resume_v2.py` requires
the verified predecessor, registered preparation and semantic rejection proofs,
then executes the canonical builder's original extension and complete final
safety-contract source before all eight original final-stage bodies. Prefix-only
proofs apply only to unchanged dependencies. The manifest must disclose the
prefix provenance, appended extension, executed final-contract source hash and
versioned stage derivations. This does not permit replacing or skipping any
native, source/current, allocation, bounds, inverse or release guard.

Profiles with `canonical_checkpoint_resume` use the versioned
`scripts/resume_integrated_release_with_Fernan_field_v1.py` continuation chain.
It reuses an exact completed canonical-builder checkpoint through
`scripts/registered_canonical_checkpoint_resume_v1.py`, then executes the original
eight final-stage bodies and all their guards/inverses. This narrow workflow
requires an explicit new experimental profile, exact original manifest/ROM and
dependency locks, unchanged accepted layers and previous profiles, and a qualified
versioned expected contract. Every final manifest must disclose the original
profile/registry and checkpoint hashes; reuse must never be reported as a fresh
canonical-builder run. No original builder or final-stage driver is edited.

Profiles carrying `owned_Fernan_name_field` additionally require
`scripts/build_integrated_release_with_Fernan_field.py`. It runs the registered
seven-stage reviewed-text-data pipeline unchanged, then applies only actor35's
exclusive given-name F-width correction. Require its configuration and
`registered_Fernan_name_field_and_complete_parent_target_inverse` in the final
manifest. All earlier runtime/name/tutorial stages remain mandatory; the
seven-stage output is an intermediate for this profile.

Profiles carrying `owned_reviewed_text_data` additionally require
`scripts/build_integrated_release_with_reviewed_text_data_v3.py`. It runs all six
earlier final-stage drivers unchanged, then applies only the six qualified,
disjoint tutorial/name data spans. Require the configuration in the final manifest
and `registered_reviewed_text_data_and_complete_parent_target_inverse` before
handoff. Its static-text predecessor is an intermediate for that profile.

## Generated ROM retention

After completed build/test work, follow `docs/rom_retention.md`: keep all ROMs from
today and the previous two Indianapolis calendar days, then one or two older daily
checkpoints plus protected baselines/source copies and explicit research pins.
Use `scripts/prune_generated_roms.ps1` to preview and apply an audited plan. Pin
older ROM inputs needed by ongoing research before cleanup. Preserve all non-ROM
records and never prune synced `sources/` or the original `work/clean.nds`.

These rules apply to every future ROM build in this repository.

Before changing or building a ROM, every model (including Luna, Terra, and Sol) must
read `docs/build_continuity_protocol.md`, `translations/release_stack.json`, and the
relevant portion of `docs/known_issues.md`. This is mandatory, not optional context.
Before authoring dialogue, every model must also read and follow
`docs/natural_dialogue_workflow.md` and `docs/dialogue_delegation_protocol.md`.
New dialogue batches must use `natural-dialogue-v2`; v1 is retained only for
already-authored migration work. Natural-dialogue batches must opt into the
machine-enforced policy; manual byte-positioned line breaks are not acceptable prose.
The required target is localized American English (`en-US`), not literal Japanese.
Honorifics and familiar forms of address must never be rendered in a way that invents
family relationships, ranks, or other story facts.

## Canonical integration baseline

- The user-designated safe integrated ROM is `out/raphael_natural_v2_accepted_base.nds`.
- Its SHA-256 is `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- The prior accepted baseline is preserved as
  `out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds`, SHA-256
  `0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2`.
- This is an intentional re-baseline. Later ROMs, including `lil_route_roundtrip.nds` and all Lil repair/probe builds, are historical research artifacts only and must not be used as a parent or distributed as a release.
- Never present a ROM built directly from `work/clean.nds`, an isolated route ROM, or an intermediate `*_stage.nds` as the next integrated release.
- New work must be layered onto the canonical integration baseline, or the complete sequence of previously accepted UI, graphics, shared-text, and route layers must be rebuilt explicitly.
- `translations/release_stack.json` is the sole registry of accepted and experimental layers. Do not maintain a separate batch list from memory.
- Every layer under `accepted_layers` must be present in every playable candidate. The integrated builder adds them automatically.
- Sound Setup candidates must use `--profile sound-setup`; never pass only the two sound batches manually. The profile requires Options/UI, SFX, and BGM layers together.
- Playable candidates must be created with `scripts/build_integrated_release.py`. Direct `dk4tool insert-script` builds are research probes only and must never be handed to the user.
- A profile carrying `ascii_glyph_right_bounds` additionally requires `scripts/build_integrated_release_with_runtime_bounds.py`. That pipeline runs the canonical builder unchanged, then applies the registered final runtime layer and verifies the complete parent/target identities. A direct canonical-builder output is only an intermediate for these profiles and must not be handed off. Require the runtime configuration in the final manifest's batch list and the `registered_runtime_bounds_and_complete_parent_target_inverse` check.
- A profile carrying `owned_name_glyph` additionally requires `scripts/build_integrated_release_with_owned_names.py`. A profile also carrying `owned_name_fields` requires `scripts/build_integrated_release_with_owned_fields.py`, which runs all earlier drivers unchanged before its source-qualified fixed-slot field stage. Require every configured final stage in the manifest and its complete parent/target inverse check; intermediate ROMs are research only. Do not hide ARM9 metadata changes in the component-preserving scene framework or code-only bounds layer.
- A profile also carrying `owned_name_fields_next` requires `scripts/build_integrated_release_with_next_owned_fields.py`. It runs the existing owned-fields driver unchanged, then applies the next registered exclusive fields. Require both field-stage manifest entries and `registered_next_owned_name_fields_and_complete_parent_target_inverse`; the prior-fields output is only an intermediate. Preserve the earlier Emilio/Fernando/Samwell corrections.
- A profile carrying `owned_name_fields_grouped` additionally requires `scripts/build_integrated_release_with_grouped_fields.py`. It runs the existing next-fields pipeline unchanged, then applies only the source-qualified complete owner groups. Require `registered_grouped_owned_name_fields_and_complete_parent_target_inverse` and the grouped stage in the manifest. Preserve Follower/Diogo and all earlier runtime/name stages; the next-fields output is an intermediate for this profile.
- A profile carrying `owned_static_text` additionally requires `scripts/build_integrated_release_with_static_text.py`. It runs the grouped-fields pipeline unchanged, then applies the separately source-qualified fixed-slot static labels. Require `registered_owned_static_text_and_complete_parent_target_inverse` and the static stage in the manifest. The grouped-fields output is an intermediate for this profile; preserve all earlier runtime/name stages.
- Preserve the registered ASCII right-bound layer in future derived profiles. Guild and Ruins share the demonstrated town-tooltip header overwrite; do not revert to the uncorrected V8865 runtime when continuing dialogue work.
- A generated `.manifest.json` is required beside every candidate handed off for testing.
- Do not hand off a candidate unless its manifest names the release-stack hash, profile, all accepted batches, changed paths, and changed records.

## Regression checks

- Before handing off a route-only build, run:
  `python scripts/verify_release_baseline.py out/raphael_natural_v2_accepted_base.nds <candidate.nds>`
- A Raphael-only patch may change `/data/SC0.DK4`; every other ROM file and component must remain byte-identical to the baseline.
- Confirm the ARM9 still contains `Continue`, `New Game`, `Options`, `Grand Race`, `Extras`, and `Gallery`.
- Preserve previously translated graphics. Do not rebuild from a source that predates them.
- Treat every leading byte below `0x20` in a story record as executable speaker/layout state, not ordinary text. Do not translate a record carrying one until its complete preamble and its portrait/name effect have been mapped in a live probe. Keeping only the first byte is not sufficient: the following bytes may be part of the same command.
- A leading raw `FE` is a system-panel selector. Preserve it as a control byte,
  never as a decoded CP932 private-use character (`F8 F2` after re-encoding).
  Its native modal consumer is distinct from progressive dialogue. Audit exact
  glyphs and panel bounds for its formatting; guard counts alone do not prove
  missing text. Every playable build rejects the known converted selector.
- Treat ARM9 text renderers as format-specific. The Options report and sailing-help prompts use a fixed-width Shift-JIS renderer; plain ASCII replacement corrupts them even when the byte-level diff is otherwise valid. Use CP932 full-width Latin text there, preserve `%s` substitutions, and cold-boot test the result. The BGM/SFX selector names are a separate packed `MESFILE` table and must not be patched as ordinary independent rows until their internal offsets are mapped.
- Do not copy established manual line breaks into newly localized prose. Legacy
  breaks are evidence to audit, not layout instructions. Migrate each record to one
  logical paragraph and let the profile formatter place ordinary line breaks. Retain
  an explicit break only for a reviewed dramatic pause with a written reason.
- Never use generic placeholders such as `see below` or `ok` as shipped dialogue. These are translation defects, not acceptable fallbacks.
- Before claiming that a route layer is present, inspect the exact records in the candidate ROM. Lil's actual opening is `/data/SC2.DK4` block 22. Do not rely only on an output-ROM name, and do not ship English for that block until its portrait/name control preamble is proven intact by live testing.
- Any build touching shared names or crew-acquisition messages must test that the first letter of an ASCII name survives rendering. Do not preserve unverified leading byte controls from Japanese name records.
- Write literal story percentages as the word `percent`. A phrase such as `3% of`
  is valid C formatting syntax (`% o`) and consumes an argument the Japanese
  record never provided. Every playable build checks final English SC0-SC3
  records against clean-source formatting commands, after all release stages.
  Preserve real source placeholders and source-leading `25` presentation state;
  lexical printf validity alone is insufficient. Do not globally double percent
  bytes or reinterpret a story presentation state as text.

## Handoff

- State the exact base ROM, changed internal files, verifier result, and candidate SHA-256.
- Never call a partial route build a final or integrated build.
- Never promote a candidate to the canonical parent until the user has cold-boot tested and explicitly accepted it.
