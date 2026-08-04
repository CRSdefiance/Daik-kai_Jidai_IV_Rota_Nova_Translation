# Release-build invariants

These rules apply to every future ROM build in this repository.

## Canonical integration baseline

- The user-designated safe integrated ROM is `out/all_goods_roundtrip.nds`.
- Its SHA-256 is `8e61fd4e8c444b25566cc273dd676b3e5bea5d683ad167db2f92444c10df9764`.
- This is an intentional re-baseline. Later ROMs, including `lil_route_roundtrip.nds` and all Lil repair/probe builds, are historical research artifacts only and must not be used as a parent or distributed as a release.
- Never present a ROM built directly from `work/clean.nds`, an isolated route ROM, or an intermediate `*_stage.nds` as the next integrated release.
- New work must be layered onto the canonical integration baseline, or the complete sequence of previously accepted UI, graphics, shared-text, and route layers must be rebuilt explicitly.
- Playable candidates must be created with `scripts/build_integrated_release.py`. Direct `dk4tool insert-script` builds are research probes only and must never be handed to the user.
- A generated `.manifest.json` is required beside every candidate handed off for testing.

## Regression checks

- Before handing off a route-only build, run:
  `python scripts/verify_release_baseline.py out/all_goods_roundtrip.nds <candidate.nds>`
- A Raphael-only patch may change `/data/SC0.DK4`; every other ROM file and component must remain byte-identical to the baseline.
- Confirm the ARM9 still contains `Continue`, `New Game`, `Opts`, `Grand Race`, `Extras`, and `Gallery`.
- Preserve previously translated graphics. Do not rebuild from a source that predates them.
- Treat every leading byte below `0x20` in a story record as executable speaker/layout state, not ordinary text. Do not translate a record carrying one until its complete preamble and its portrait/name effect have been mapped in a live probe. Keeping only the first byte is not sufficient: the following bytes may be part of the same command.
- Treat ARM9 text renderers as format-specific. The Options report and sailing-help prompts use a fixed-width Shift-JIS renderer; plain ASCII replacement corrupts them even when the byte-level diff is otherwise valid. Use CP932 full-width Latin text there, preserve `%s` substitutions, and cold-boot test the result. The BGM/SFX selector names are a separate packed `MESFILE` table and must not be patched as ordinary independent rows until their internal offsets are mapped.
- Keep established manual line breaks from the accepted baseline unless a screenshot demonstrates that a specific line needs adjustment.
- Never use generic placeholders such as `see below` or `ok` as shipped dialogue. These are translation defects, not acceptable fallbacks.
- Before claiming that a route layer is present, inspect the exact records in the candidate ROM. Lil's actual opening is `/data/SC2.DK4` block 22. Do not rely only on an output-ROM name, and do not ship English for that block until its portrait/name control preamble is proven intact by live testing.
- Any build touching shared names or crew-acquisition messages must test that the first letter of an ASCII name survives rendering. Do not preserve unverified leading byte controls from Japanese name records.

## Handoff

- State the exact base ROM, changed internal files, verifier result, and candidate SHA-256.
- Never call a partial route build a final or integrated build.
- Never promote a candidate to the canonical parent until the user has cold-boot tested and explicitly accepted it.
