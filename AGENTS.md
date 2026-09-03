# Release-build invariants

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
- Its SHA-256 is `d8cb15aa23e2496510eba8feb18e4536a7da195522b7f5959298b0c1cc0fd1cf`.
- The prior accepted baseline is preserved as
  `out/raphael_natural_v2_pre_extras_common_v6_accepted_rollback.nds`, SHA-256
  `c94e1fd7221c5e929c851a39f1e722c8b127992bea743dd9992ca1ff027afcdf`.
- This is an intentional re-baseline. Later ROMs, including `lil_route_roundtrip.nds` and all Lil repair/probe builds, are historical research artifacts only and must not be used as a parent or distributed as a release.
- Never present a ROM built directly from `work/clean.nds`, an isolated route ROM, or an intermediate `*_stage.nds` as the next integrated release.
- New work must be layered onto the canonical integration baseline, or the complete sequence of previously accepted UI, graphics, shared-text, and route layers must be rebuilt explicitly.
- `translations/release_stack.json` is the sole registry of accepted and experimental layers. Do not maintain a separate batch list from memory.
- Every layer under `accepted_layers` must be present in every playable candidate. The integrated builder adds them automatically.
- Sound Setup candidates must use `--profile sound-setup`; never pass only the two sound batches manually. The profile requires Options/UI, SFX, and BGM layers together.
- Playable candidates must be created with `scripts/build_integrated_release.py`. Direct `dk4tool insert-script` builds are research probes only and must never be handed to the user.
- A generated `.manifest.json` is required beside every candidate handed off for testing.
- Do not hand off a candidate unless its manifest names the release-stack hash, profile, all accepted batches, changed paths, and changed records.

## Regression checks

- Before handing off a route-only build, run:
  `python scripts/verify_release_baseline.py out/raphael_natural_v2_accepted_base.nds <candidate.nds>`
- A Raphael-only patch may change `/data/SC0.DK4`; every other ROM file and component must remain byte-identical to the baseline.
- Confirm the ARM9 still contains `Continue`, `New Game`, `Options`, `Grand Race`, `Extras`, and `Gallery`.
- Preserve previously translated graphics. Do not rebuild from a source that predates them.
- Treat every leading byte below `0x20` in a story record as executable speaker/layout state, not ordinary text. Do not translate a record carrying one until its complete preamble and its portrait/name effect have been mapped in a live probe. Keeping only the first byte is not sufficient: the following bytes may be part of the same command.
- Treat ARM9 text renderers as format-specific. The Options report and sailing-help prompts use a fixed-width Shift-JIS renderer; plain ASCII replacement corrupts them even when the byte-level diff is otherwise valid. Use CP932 full-width Latin text there, preserve `%s` substitutions, and cold-boot test the result. The BGM/SFX selector names are a separate packed `MESFILE` table and must not be patched as ordinary independent rows until their internal offsets are mapped.
- Do not copy established manual line breaks into newly localized prose. Legacy
  breaks are evidence to audit, not layout instructions. Migrate each record to one
  logical paragraph and let the profile formatter place ordinary line breaks. Retain
  an explicit break only for a reviewed dramatic pause with a written reason.
- Never use generic placeholders such as `see below` or `ok` as shipped dialogue. These are translation defects, not acceptable fallbacks.
- Before claiming that a route layer is present, inspect the exact records in the candidate ROM. Lil's actual opening is `/data/SC2.DK4` block 22. Do not rely only on an output-ROM name, and do not ship English for that block until its portrait/name control preamble is proven intact by live testing.
- Any build touching shared names or crew-acquisition messages must test that the first letter of an ASCII name survives rendering. Do not preserve unverified leading byte controls from Japanese name records.

## Handoff

- State the exact base ROM, changed internal files, verifier result, and candidate SHA-256.
- Never call a partial route build a final or integrated build.
- Never promote a candidate to the canonical parent until the user has cold-boot tested and explicitly accepted it.
