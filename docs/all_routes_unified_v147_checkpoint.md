# Experimental combined V147

V147 integrates the complete natural-English warning **No companions are
available!** for the empty eligible-companion list. All four source-owned strings
are repacked into 108/136 bytes with four-byte alignment. The two full Options
prompts and original parenthesized name format are preserved; four literal
pointers are updated. No executable code or other ROM component changes over V146.

## Identity and ancestry

- Candidate: `out/all_routes_combined_v147_candidate.nds`.
- Candidate SHA-256: `44f5f00bb23a74e5d3202c9dbe20c9c962b9d1e7783cc56960fc1ed5e1909836`.
- ARM9 SHA-256: `33dc6e6ac7ababb513a773647edd6f93cb5c08b19fad2500e7695f95d8629d75`.
- Patch: `out/all_routes_combined_v147_candidate.xdelta`, 749,543 bytes.
- Patch SHA-256: `a35380566c214b7f455afebd8a1ae43815e2e5933b747f7ec8f8db9bc9396f5b`.
- Manifest: `out/all_routes_combined_v147_candidate.manifest.json`.
- Registered profile: `all-routes-unified-v147`, experimental; all 435 inherited
  batches in exact V146 order, including all accepted layers and experimental
  route/shared/UI/graphics layers. Every V146 postprocessing stage precedes the
  new strict companion release.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Compared parent: V146, SHA-256
  `fc9dc01b922aa354b82add5ea6fc29cbb7612966f4d5010481906d723c57e0b3`.

Relative to the canonical base the nine changed paths remain `/COMMON/HELP.DK4`,
`/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/personinfo.pxl`, and `/data/SC0.DK4` through `/data/SC3.DK4`.
The clean patch input is `work/clean.nds`, SHA-256
`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

## Verification

- Production output is byte-identical to the reviewed native research output.
- Native zero-count branch, actual formatter/macros, post-dismissal return and
  positive-count bypass pass against saved bytes.
- Ten inherited Options formatter cases, twenty confirm/cancel response cases,
  and six actual neighboring ASCII/CP932 name-format cases pass against saved bytes.
- Both native pixel formats preserve every glyph on one row. The complete ink
  panel is visually reviewed, including leading/final characters and exclamation.
- All 3,668 COMMON selections and every other V146 ROM component are byte-exact.
- Manifest baseline, registry hash, candidate hash and inherited batch order pass.
- Fourteen focused production/native tests pass across companion, Deck, Options
  and damaged-save releases. New modules/tools/tests pass Ruff.
- Canonical verifier passes with the nine explicit permitted paths.
- Applying the patch to the exact clean ROM reconstructs the candidate byte for byte.

Evidence: `work/analysis/available_companions_v147_saved_proof.json`,
`available_companions_v147_baseline_verification.txt`, durable manuscript/pool/
native-review/release JSONs under `translations/available_companions_*`, and
`docs/available_companions_native.md`.

## Pending gameplay and full goal

Cold-boot the title, character selection, established story scene and town UI;
test an empty and nonempty eligible-companion list, full dialog composition and
dismissal, Options on/off confirmation/cancellation/persistence, and neighboring
parenthesized names. Retain all inherited Deck/save/tribute/caption/Golden Route/
map/help/sound/race/network checks. List backend, full widgets/input and physical
presentation are unverified. Native branch input and dismissal remain fixture
contracts, not complete gameplay execution.

No canonical promotion or user acceptance is claimed. Remaining COMMON stays at
245 Japanese selections / 133 physical records; broad ARM9/UI/graphics inventory,
translation and older-English fidelity review remain in the active goal. After
full goal completion, revisit older record-based checks as requested.
