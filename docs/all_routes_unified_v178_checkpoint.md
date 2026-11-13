# Combined V178: preserve image207's unidentified source stroke

2026-10-04. **Experimental**; the all-graphics goal remains active and incomplete.

## Correction and proof

The V163–V177 English caption erased an unidentified clipped stroke above the
readable Japanese caption. V178 retains every original index in rows **0–19**:
**279 nonwhite indices**, including original edge shading. No numeral, character
or extra meaning is inferred. Below that region, **New World Village (Developed)**
and every pixel remain byte-identical to V177. Caption placement, complete first
and final characters, header, dimensions, palette and allocation are unchanged.
The complete original/prior/corrected comparison was reviewed.

- **43 focused tests pass**: 8 source-mark regression cases, 19 original village
  cases and 16 Online27 cases. Missing stroke endpoints, missing English first/
  final ink, palette/source mismatch and undeclared layer replacement are rejected.
- Controlled complete native caption glyph and PXL header checks pass with the
  exact inherited candidate ARM9. Supplied table/resource and scratch raster
  probes do not prove actual scene reachability, loading/crops, GPU/palette/alpha
  or gameplay. The stroke's meaning remains unknown.
- Saved manifest, registry/profile, full stack, terminal stages, prior record IDs,
  golden menus and exact one-file delta pass. Builder and ARM9 are unchanged.
- The clean-ROM patch reconstructs the candidate byte for byte.

## Exact registered handoff

| Artifact | SHA-256 |
| --- | --- |
| Canonical `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Prior V177 | `a5dba05534ec334167d0ffd9f506050f35ca11555eaa38cd5d1a17fbf3034d45` |
| `out/all_routes_combined_v178_candidate.nds` | `e03c0c0aee3787ff0b0813e270faadd3c7fdb6fc5ac7d62582b3fdb5e4b0778d` |
| ARM9, unchanged from V177 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry | `b187e51fdc9c7bc7c1cf27c77839e08d07b305285e85f9332bc9d0c86f627481` |
| Builder, unchanged | `09ad79d17085303223c6538c1dc1eb88421b9bf611fe7649c0a740be1cf833ba` |
| `out/all_routes_combined_v178_candidate.xdelta`, 832003 bytes | `cd3a7695929bffcb0bacb970f606f683dece544caff189a73d256499733a9551` |

Profile **all-routes-unified-v178**, **462 experimental batches**. Exactly one
source batch is superseded:
`translations/village_caption_evstill207_graphics_v1.json` →
`translations/village_caption_evstill207_graphics_v2.json`. The same record ID and
English text are retained. Every other V177 batch and terminal repair stage is
unchanged. All accepted layers remain baked into the immutable canonical base;
zero additional accepted batches are applied. No historical profile/batch is
modified. The adjacent `out/all_routes_combined_v178_candidate.manifest.json`
lists the full stack, registry identity, dependencies, changed paths/records and
checks. Only **`/evstill/evstill207.pxl`** differs from V177. The full canonical
delta still contains the same **34 files**, listed in the manifest/saved proof.

Evidence: `work/analysis/image207_mark_v178_saved_proof.json`,
`work/qa/image207_mark_v178/evidence.json`, `native.json`, `review.png`,
`work/analysis/v178_graphics_tests.log`, `v178_build.log`,
`scripts/preserve_image207_v178.py`, `tests/test_image207_preserved_mark.py`.

## Remaining scope

V177's four readable Online27 speech bubbles remain present and exact. Four
historical Japanese-bearing Online files still need faithful dialogue/UI/chat
transcription and localization: Online24/27/31/33. Online27 is only partly complete.

Raw SLACKIMG block-19 inspection revealed **12 text-bearing images** among 21
sketch/comic previews: indices 4/5/6/7/8/10/11/12/13/16/18/19. Japanese captions,
dialogue/effects, Chinese dialogue and creator signatures need translation or
explicit credit decisions. All 21 full-size images were inspected; the block is
unchanged. Its source-locked phrase drafts are in
`translations/embedded_sketch19_source_manuscript_v1.json` and **are not applied**.
Unknown creator names, creature-name interpretation and Chinese wording are not
guessed. Geometry/encoding/native usage remain unproved.

All 42 block-13 portraits were inspected without Japanese captions; its native
partition is still unproved. Six contextual-art retain decisions are documented;
actual native use and separate facility/help captions remain open. Other embedded
formats, full-resolution review, opening Latin name consistency, image207 mark
interpretation/usage, prior title scenery/native gates and full gameplay remain.
See [V177 checkpoint](all_routes_unified_v177_checkpoint.md) for preceding evidence.

Cold boot without savestates: opening, title scenes/menu, New Game, captain/name
entry, established story, town UI and repaired screens. Review image207 if reached:
complete caption and original clipped stroke. Check Online27 readability if
reachable in Extras/Online, earlier titles/scenery/palette/alpha, timing/input and
native embedded consumers. No human acceptance is assumed, including V175.
Repository continuity rules require explicit human acceptance before canonical
promotion. Retain the user's note to revisit older record-based checks when the
**full project goal** is complete. Tracker:
`translations/graphics_completion_campaign_v1.json`.
