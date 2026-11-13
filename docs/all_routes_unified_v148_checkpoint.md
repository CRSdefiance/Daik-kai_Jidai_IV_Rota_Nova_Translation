# Experimental combined V148

V148 repairs 239 stale item/entity name references using a fourth SDK-loaded
section, reserved after main BSS and before the raised main heap boundary.
All 117 complete owners use 1,480/1,504 bytes. Native DTCM scratch/SDK data is
restored exactly; ITCM is unchanged. All ten square-shopkeeper labels retain
the complete source-faithful English **Square Shopkeeper**.

## Identity and ancestry

- Candidate: `out/all_routes_combined_v148_candidate.nds`.
- ROM SHA-256: `024b02f68ab37ad5494f9ec2e0c407ed352ec3dbf8e298d82cff29f6b223d23a`.
- ARM9 SHA-256: `bb637907df8e9a4334f29219cd8273ea92731992b2bc4f9852525c68f9fed6af`.
- Patch: `out/all_routes_combined_v148_candidate.xdelta`, 743,970 bytes.
- Patch SHA-256: `033a1d2d84f11bf2b272278738d073cd03295c4d907357273236ab85f2ae7d41`.
- Manifest: `out/all_routes_combined_v148_candidate.manifest.json`.
- Profile: `all-routes-unified-v148`, experimental; all 435 V147 batches and
  postprocessing stages precede the strict persistent-name release.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Compared V147 parent SHA-256:
  `44f5f00bb23a74e5d3202c9dbe20c9c962b9d1e7783cc56960fc1ed5e1909836`.
- Clean patch input: `work/clean.nds`, SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The nine canonical changed paths remain `/COMMON/HELP.DK4`,
`/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/personinfo.pxl`, and `/data/SC0.DK4` through `/data/SC3.DK4`.

## Verification

- Saved ARM9 equals the exact native research bytes; every other V147 component
  and all 3,668 COMMON selections are byte-identical.
- Manifest candidate/base/registry hashes and complete inherited batch order pass.
- Native SDK copy/BSS clear, same-machine arena initialization and 173 scratch
  writes preserve the reserved text. All direct references are classified.
- Research on those exact bytes covers 218 native item getters, 218 static
  selectors, 436 virtual callers, 207 ordinary names and four map selections.
- Twenty shopkeeper rasters match independent pixels; ten reviewed panels
  preserve leading/final characters without clipping or row overlap.
- Saved-ROM companion branch, ten Options formatting cases, twenty responses
  and six parenthesized-name cases preserve inherited behavior.
- Forty focused tests and new-code lint pass. Canonical verifier passes with
  the nine explicit paths. Clean-ROM patch reconstruction is byte-exact.

Evidence: `work/analysis/persistent_names_v148_saved_proof.json`,
`persistent_names_v148_baseline_verification.txt`, and durable production inputs
under `translations/persistent_name_*`. See `persistent_name_section.md` for
native fixture boundaries and allocation details.

## Remaining full goal

Physical boot/gameplay and broader name displays/allocation producers remain
unverified. Cold-boot title/New Game/character selection, established story/town,
item lists, crew acquisition, paired character names and map tooltips; retain
all inherited Options/Deck/save/help/sound/tribute/caption/race checks. Inspect
full words and leading characters. Canonical promotion requires user acceptance.

Remaining COMMON: 245 Japanese selections across 133 physical records, consisting
of 31 promotional and 214 scene/artwork/name copies. Two ordinary Japanese given
names, fleet labels, remaining ARM9/UI/graphics and older-English fidelity remain
in the active goal. No new commit/push or full-goal completion is claimed.
After full goal completion, revisit older record-based checks as requested.
