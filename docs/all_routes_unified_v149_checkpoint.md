# Experimental combined V149

V149 adds complete natural-English **Pirate %s** and **Unidentified fleet**
labels after every V148 layer. The captain-name substitution is preserved.
Two native literal references are redirected; complete strings fit in the
original fallback slot and the verified companion pool's spare tail. All other
ARM9 bytes, including the reserved persistent-name section, remain unchanged.

## Identity and ancestry

- Candidate: `out/all_routes_combined_v149_candidate.nds`.
- ROM SHA-256: `7261f62222a055b7265fe93e6afc1471926c997b792fdbe722a5d70daee950ad`.
- ARM9 SHA-256: `30ae21c22c5f2d1e42a986331aa52a0df6e9d69fcf6a8f9d195726e751f4ea66`.
- Patch: `out/all_routes_combined_v149_candidate.xdelta`, 744,010 bytes.
- Patch SHA-256: `812f2fe0fb9e604d65f32c9fd795823f1475599d6e34d417cd475d87fb030778`.
- Manifest: `out/all_routes_combined_v149_candidate.manifest.json`.
- Profile: `all-routes-unified-v149`, experimental; all 435 inherited accepted
  and experimental batches in V148 order and all prior postprocessing stages.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Compared V148 parent SHA-256:
  `024b02f68ab37ad5494f9ec2e0c407ed352ec3dbf8e298d82cff29f6b223d23a`.
- Clean patch input: `work/clean.nds`, SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The nine canonical changed paths remain `/COMMON/HELP.DK4`,
`/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/personinfo.pxl`, and `/data/SC0.DK4` through `/data/SC3.DK4`.

## Verification and limits

- Saved ARM9 exactly matches the reviewed native research bytes. Every other
  V148 component and all 3,668 COMMON selections are byte-identical.
- Manifest baseline/registry/candidate hashes and full inherited batch order pass.
- All-byte ARM9/decompressed-overlay storage scans find only the mapped original
  fallback reference, with no interior references into reused allocations.
- 456 connected native selection/getter/formatter/glyph cases pass independent
  pixel comparisons in both mapped fleet displays: 414 ordinary-name cases,
  forty stored player-name cases across four routes, and two null-sentinel cases.
- Ten native panels reviewed: complete leading/final glyphs and full labels,
  including seventeen-byte ordinary and sixteen-byte saved-player boundaries.
- Saved native companion, Options formatting/responses and neighboring
  parenthesized-name cases pass. Twenty-eight focused tests and lint pass.
- Canonical baseline verifier passes; the clean-ROM patch reconstructs the
  candidate byte for byte.

Native captain byte/current-character values are fixtures. Ordinary constructors
execute; stored player interface/vtable and valid saved fields are initialization
fixtures. Live captain setters/eligibility, malformed fields, other virtual name
consumers, parent composition/input and physical gameplay remain unverified.
This checkpoint does not establish that every ordinary actor is a valid captain.

Evidence: `work/analysis/fleet_names_v149_saved_proof.json`,
`fleet_names_v149_baseline_verification.txt`, durable `translations/fleet_name_*`
production inputs and `docs/fleet_name_native.md`.

## Remaining full goal and gameplay

Cold-boot title/New Game/character selection, established story/town, ordinary
and renamed-player fleets, pirate/unknown labels in both fleet views, and map
tooltips. Check complete names, leading letters, centered/fixed placement and
screen edges. Retain inherited item/crew/Options/Deck/save/help/sound/tribute/
caption/race checks. Canonical promotion requires explicit user acceptance.

Remaining COMMON: 245 Japanese selections/133 physical records (31 promotional
and 214 scene/artwork/name copies). Two Japanese ordinary given names, remaining
ARM9/UI/graphics and older-English fidelity review remain in the active goal.
No full goal completion, canonical acceptance or new commit/push is claimed.
After full completion, revisit older record-based checks as requested.
