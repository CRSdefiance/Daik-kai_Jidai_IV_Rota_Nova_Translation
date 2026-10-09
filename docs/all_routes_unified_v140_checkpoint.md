# Combined V140 checkpoint

## Current checkpoint: experimental combined V140

V140 integrates all nine complete map tooltip/creature translations after every
V139 route, shared-text, UI/graphics, caption and Golden Route layer. Native
formatting gates are approved; physical palette/routing and cold-boot gameplay
remain pending. No canonical promotion or new commit/push is claimed.

- ROM: `out/all_routes_combined_v140_candidate.nds`; SHA-256
  `c2ff532c9014b82d1e21c289dee5e18a30226e6ce38be2ba7ede27e2d7255173`.
- ARM9 SHA-256: `d937be33b97b654038d03f1aed57ae30a2a49e0afce7d96ae1e2c972c1b758b3`.
- Patch: `out/all_routes_combined_v140_candidate.xdelta`; 748,324 bytes; SHA-256
  `a897295b17b21607219804266478e37616755dd21259cef0029aa165100b2ed1`.
  Exact clean-ROM patch roundtrip passes.
- Canonical base remains `out/raphael_natural_v2_accepted_base.nds`; SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile `all-routes-unified-v140` retains the complete 435-entry batch order
  from V139 and every accepted registry layer. The unchanged COMMON rebuild,
  full scene captions and Golden Route release run before the new strict
  `map_tooltip_release_v1.json` component. Adjacent manifest records full lineage,
  current registry/dependency hashes, changed paths/records and experimental limits.
- New English: Pirates, Monster, ???, the complete class/Armament formats,
  Monster Fish, Giant Squid, Shark and Whale. No label is shortened. Machine LF
  guards preserve both first-row parities and every leading second-row letter.
- Repacking uses 151/172 string bytes and relocates the two-entry Golden Route
  heading table under its verified sole literal consumer. All six viewer strings
  and native heading/footer/modal output are preserved. Fonts, tracking, native
  instructions and geometry are unchanged.
- Saved-ROM verifier, canonical baseline check, 104 targeted tests and Ruff pass.
  All 164 captions, 3,668 native COMMON selections and every other V139 component
  are byte-exact. Nine changed canonical paths remain: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, and `/data/SC0.DK4` through `/data/SC3.DK4`.
- Native formatting evidence includes 2,162 tooltip pixel cases, sixteen inherited
  Golden rasters, all39 classes, eighty faction/route selections, 768 percentage
  cases, twenty numeric/ring boundaries, and actual eighteen-byte editor/nineteen-
  byte serialized name extent. CP932 pixels use the real ITCM painter and exact
  clean font; the six-panel native-ink preview is reviewed. Remaining contracts
  are font disk loading, bitmap origin/clear/physical composition, keyboard UI and
  physical save I/O. Malformed saved-field NUL validation is absent.

Cold-boot testing still needs title/New Game/character selection, an established
story scene, town UI, map unknown/pirate/monster/known-faction tooltips, the four
creature classes, maximum-length names, percentage/armament rows, map placement
near screen edges, Golden Route controls, saves, sound and transitions. Use a
fresh boot; user acceptance is required before promoting the canonical baseline.

Fresh COMMON inventory is `work/analysis/common_remaining_v140.json`. Its content
is unchanged by this ARM9-only stage: 133 Japanese-bearing physical records and
245 selections (31 promotional and 214 scene/artwork/name copies). Their separate
consumers, remaining ARM9/UI/graphics, Reports/Sailing Help/BGM presentation and
older English fidelity remain in the full active goal. At completion, record the
requested follow-up to revisit older record-based checks.

Evidence: `work/analysis/map_tooltips_v140_saved_rom_proof.json`,
`map_tooltips_v140_patch_roundtrip.json`, `map_tooltips_v140_baseline_verification.txt`,
and strict `translations/map_tooltip_native_evidence_v1.json`.
