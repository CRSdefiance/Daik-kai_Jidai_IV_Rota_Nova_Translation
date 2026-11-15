# Combined V141 checkpoint

V141 restores three blizzard alerts that V140 incorrectly selected as fragments
of a generic story/letter/faction placeholder. Fresh Japanese-source English:

- 389: Admiral, a blizzard has started!
- 390: Admiral, we've hit a blizzard!
- 391: Admiral, a blizzard!

All three selections belong to clean COMMON B5 R30. Their actor-variant table is
02118980, selected at 02030B10 through wrapper 02053F0C. Complete-owner repacking
retains the source alignment prefix and every native message/NUL identity.
Expansion uses only terminal padding from two single-entry donor records; native
cache block sizes remain unchanged. All three reviewed exact-font previews fit
on one row with intact leading/final characters. No LF or manual wrapping is used.

## Artifacts and lineage

- Experimental profile: `all-routes-unified-v141`; every V140 batch remains in the
  same 435-entry order. The strict blizzard repair runs after COMMON, full scene
  captions, Golden Route viewer and map tooltip stages.
- ROM: `out/all_routes_combined_v141_candidate.nds`; SHA-256
  `c32db16159db6d6da0db3aaf2fa774c342cda2c3af8abdc3b77acca86a201310`.
- ARM9 SHA-256:
  `e8728fa77fbc37d39b2bcb99aa796b8cc11cde07c67934d59692621ff6676c4b`.
- COMMON SHA-256:
  `6080ef4e113871609c806e7dc088e7138c1b4a85534aad53be4d492588622485`.
- Patch: `out/all_routes_combined_v141_candidate.xdelta`; 748,335 bytes; SHA-256
  `2ad59d4daeaa55d5f491d3ec303d63f8d73fc732cffba52c9bd41c2e252bc488`.
- Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.

## Verification and remaining work

Thirty-six focused tests and Ruff pass. The saved-ROM verifier compares all 3,668
native selections and every V140 ROM component. Only the three authored messages,
terminal donor padding and 45 uint16 message offsets change. Every other visible
selection, route, UI, graphic, caption and tooltip is preserved. Canonical baseline
invariants pass; the clean-ROM patch reconstructs V141 exactly.

The nine changed canonical paths remain `/COMMON/HELP.DK4`,
`/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/personinfo.pxl`, and `/data/SC0.DK4` through `/data/SC3.DK4`.

Cold-boot blizzard warnings, including crew-category alternatives and the adjacent
storm warning, remain to be tested along with V140's title/story/town/map/Golden
Route/save/sound checks. User acceptance is required for canonical promotion.
No new commit/push or gameplay acceptance is claimed.

This repairs older English; it does not reduce the remaining Japanese inventory
of 133 physical records/245 selections. Shared promotional/scene consumers,
ARM9/UI/graphics, Reports/Sailing Help presentation, sound gameplay and broader
English fidelity remain goal work. At completion, record the requested follow-up
to revisit older record-based checks.

Proofs: `work/analysis/common_blizzard_v141_saved_rom_proof.json`,
`common_blizzard_v141_patch_roundtrip.json`, and
`common_blizzard_v141_baseline_verification.txt`. Manuscript and preview review
are locked by `translations/common_blizzard_release_v1.json`.
