# Experimental combined V151: staged persistent-name boot repair

The user reports V148 and later stop at a black screen, while V147 reaches the
title screen. V148–V150 remain revoked. The real DeSmuME capture records the SDK
terminal halt caller throughout 300 frames; it does not identify its initiating
caller. A cross-CPU autoload test exposes the new V148 pool overlapping ARM7's
initial boot source. Under ARM9-first loading, 1,464 source bytes are overwritten
and ARM7's copied WRAM code differs from original. V147 changes none.

## Repair

ARM7's initial image is 02380000..023A71E8. V151 stages the complete persistent
name payload plus a 48-byte copy routine at 023A7200..023A7810, beyond that image.
The previously empty startup hook at 020008E4 calls this routine after ARM9 BSS
clearing. It copies all 1,504 reserved bytes to 02387A20..02388000 before static
constructors run. This retains the final main heap lower boundary, every relocated
name reference and all reviewed name wording. Temporary staging is within memory
available to the later main heap; no staging data is needed after the hook returns.

This repairs the proven source-overwrite hazard. Actual dual-CPU scheduling,
cache/MPU behavior and complete cold boot remain unverified until tested in the
emulator. Earlier narrow passing fixtures do not establish release viability.

## Candidate identity

- ROM: `out/all_routes_combined_v151_candidate.nds`.
- ROM SHA-256: `d61241e3f9d29debcc41cedcf7824aa06ac36e5e07643c714e7b045465c40345`.
- ARM9 SHA-256: `75fac17b97382fb4428ce0823ae5a8ca2b698537fcc8e0f00e213247c4adcd57`.
- Patch: `out/all_routes_combined_v151_candidate.xdelta`, 744,074 bytes.
- Patch SHA-256: `8fccd256eaafd3022fe6ec089e1e90b0c5d9eef2d116d93ccd4152c154af14f1`.
- Manifest: `out/all_routes_combined_v151_candidate.manifest.json`.
- Profile: `all-routes-unified-v151`, experimental; all 435 inherited V150
  batches and postprocessing stages, then the terminal boot repair.
- Canonical build base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- V150 is a preserved comparison artifact, not the builder's parent.

## Verification

The saved candidate differs from V150 only in ARM9 and matches the strict repair
transform exactly. All other components, 3,668 COMMON selections, inherited batch
order, candidate/base/registry identities and manifest lineage pass. Both ARM7
sections remain byte-exact under native autoload execution. The actual saved
startup BL reaches the copy routine, preserves r0–r3 and the stack, returns to
020008E8, and restores the full payload. Canonical-baseline verification passes
with the established nine changed paths:

`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
`/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and `/data/SC0.DK4`–`SC3.DK4`.

The clean-ROM patch reconstructs V151 byte for byte. Evidence:
`work/analysis/persistent_name_boot_v151_saved_proof.json`,
`persistent_name_boot_v151_baseline_verification.txt`,
`persistent_name_arm7_boot_overlap.json`, and `v148_desmume_boot_trace.log`.
Source identity and all unrelated main/ITCM/DTCM bytes are guarded; lint passes.

## Required runtime check

Cold-boot V151 without a savestate. Confirm title, New Game, character selection,
an established story scene and town UI. Then inspect complete item/shopkeeper,
crew and fleet names, including leading/final letters. Retain inherited Options,
Deck, Help, BGM, map and route checks. This candidate is experimental and must
not be promoted without explicit user cold-boot acceptance. The full translation
goal and older record-check follow-up remain open.
