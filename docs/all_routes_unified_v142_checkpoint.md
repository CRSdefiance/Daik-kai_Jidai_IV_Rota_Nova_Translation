# Combined V142 checkpoint

V142 restores all four remaining occurrences of the generic story/letter/faction
placeholder found in V141 COMMON. Those physical owners had ten unrelated native
selections: ending narration 344, scurvy warnings 396–397, sky prompts 416–419,
and fog reports 424–426. Each message is translated from its clean Japanese source
with reviewed neighboring context and natural American English.

The narration retains both historical periods and the transformation of the world;
345's following legends narration remains unchanged. Scurvy warnings preserve
uncertainty. Sky prompts do not invent an explanation for what the crew sees.
The fog reports retain worsening visibility and the coarse variant's emphasis.
Full-width reserved I/F follow the established native command-safety convention.

## Artifacts and lineage

- Experimental profile: `all-routes-unified-v142`; complete V141 batch order of
  435 entries retained. Strict placeholder repair follows all route/UI/graphics,
  COMMON, full captions, Golden viewer, tooltip and blizzard stages.
- ROM: `out/all_routes_combined_v142_candidate.nds`; SHA-256
  `c7691fd1455d89f7231cf5616689e4905f0141b6a939670c1550fb6a68f919e4`.
- ARM9 SHA-256:
  `863776d944118cc12418a91ed32e24cac1755aeac70ace682fdfa0897818b7eb`.
- COMMON SHA-256:
  `8dd709b8c8e8e35d61b9999191b326e91601029325884fc8289123f3d945147c`.
- Patch: `out/all_routes_combined_v142_candidate.xdelta`; 748,529 bytes; SHA-256
  `88323f3c7d377d4392b7931b239c3d4742d5aa6a4ad12a57b50dbb9e4dd8951e`.
- Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.

## Verification and limitations

All ten exact-font previews are reviewed; the native layout audit has zero blockers.
Twenty-three focused repair/repack tests and Ruff pass. The saved-ROM verifier
checks all 3,668 native messages and every V141 ROM component. Only ten authored
messages, terminal donor padding and 113 uint16 message offsets change. Twenty-three
physical records change: four authored owners plus nineteen padding donors.
Native cache sizes, NUL identities and every unrelated visible selection remain
unchanged. All code, fonts, routes, UI, graphics, captions, tooltips and V141
blizzard alerts are preserved. Canonical invariants pass; the clean-ROM patch
reconstructs V142 exactly.

The same nine canonical paths change: `/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`,
`/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and
`/data/SC0.DK4` through `/data/SC3.DK4`.

Zero occurrences of this specific generic placeholder phrase remain in COMMON.
That finding does not prove all older English faithful or all remaining work done.
Japanese counts remain 133 physical records/245 selections. Shared-text consumers,
ARM9/UI/graphics, Reports/Sailing Help presentation, sound gameplay and broader
English fidelity remain active work. Cold-boot ending/scurvy/sky/fog cases and all
inherited V140/V141 gameplay checks are pending; canonical promotion requires
user acceptance. No new commit/push or gameplay acceptance is claimed.

Proofs: `work/analysis/common_placeholder_v142_saved_rom_proof.json`,
`common_placeholder_v142_patch_roundtrip.json`, and
`common_placeholder_v142_baseline_verification.txt`. Strict manuscript/preview
locks: `translations/common_placeholder_release_v1.json`. At full goal completion,
record the requested follow-up to revisit older record-based checks.
