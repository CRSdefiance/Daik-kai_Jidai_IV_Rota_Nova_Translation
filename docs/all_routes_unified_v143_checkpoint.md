# Combined V143 checkpoint

Experimental V143 integrates all eight source-faithful tribute paragraphs with
display-only F/I name protection and scoped native word wrapping for town and
monthly portrait messages. Names, amounts and leading characters survive native
formatting and rendering; complete prose is retained without authored wrapping.

## Artifacts and lineage

- ROM: `out/all_routes_combined_v143_candidate.nds`, SHA-256
  `2c4cf489bfaaff8b187744e085a0ee8314dc10e4054048f60e9156cf5d786984`.
- Patch: `out/all_routes_combined_v143_candidate.xdelta`, 749,164 bytes, SHA-256
  `aa567622d6d6b973ba17a597eaa5c833518520642abf094bf0ef017b7690b44c`.
- Base: immutable `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile: `all-routes-unified-v143`. All 435 V142 batches remain in exact order,
  including all required accepted layers. The tribute stage follows all inherited
  COMMON, captions, Golden viewer, tooltip, blizzard and placeholder stages.
- Manifest: `out/all_routes_combined_v143_candidate.manifest.json`.

## Verification and limits

Saved-ROM verification checks all 3,668 native selections and every V142 ROM
component. Only tribute COMMON and ARM9 outputs differ from V142; all inherited
routes, UI, graphics, captions and other components remain exact. The repack changes
22 physical records and 83 uint16 offsets. The 652-byte ITCM extension is reserved
by the native arena initializer and loads exactly.

Final-output native regressions pass 192 warm town, 12 cold town with host I/O
contracts, eight monthly caller and 26 pixel cases. Fourteen monthly and six final
town panels are inspected. Thirty-three focused tests and lint pass. Canonical
menu/file invariants pass with the nine declared combined paths. The patch
reconstructs V143 byte-exact from the clean ROM.

The same nine canonical paths change: `/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`,
`/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and
`/data/SC0.DK4` through `/data/SC3.DK4`.

Full widget/portrait construction, physical palette/routing/input, hardware cache
and cold-boot gameplay remain pending. Test title/New Game, an established story
scene, town UI, monthly tribute and exclusive-contract town tribute, especially
player names containing F/I and long names. All inherited gameplay checks remain.
No canonical promotion, gameplay acceptance or new commit/push is claimed.

Proofs: `work/analysis/common_tribute_final_native_proof.json`,
`common_tribute_v143_saved_rom_proof.json`,
`common_tribute_v143_patch_roundtrip.json` and baseline verification text.
Remaining COMMON Japanese coverage is unchanged: this repairs existing English.
The broader translation goal remains active. At full completion, record the
requested follow-up to revisit older record-based checks.
