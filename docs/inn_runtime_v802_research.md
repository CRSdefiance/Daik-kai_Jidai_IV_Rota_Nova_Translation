# V802: bounded Inn runtime and rendered prose research

This is research on V799, not a new playable V802 ROM. The authoritative combined
candidate, manifest and patch remain V799. No canonical promotion is authorized.

## Fixed existing storage

`dk4tool/patch/inn_editorial_runtime.py` retains the seven exact original parent
contracts and adds only source-mapped Inn consumers: ordinary 1178, 1179,
1181–1185, 1194–1198; yes/no 1177, 1180, 1199; queued ordinary table 021180E0.
No permissive gaps or caller normalization are introduced.

The existing private data allocation remains 168 bytes: 142 selector bytes,
two alignment bytes and 24 phrase-index bytes. The packed-index location and
status code are unchanged. Only the selector's table literal moves; every gate
instruction remains identical.

The complete `luxury goods` string moves to an explicitly owned, aligned source
string address, 02143DD8. It shares the old 40-byte month-string allocation with
`This month` and `%s months ago`. `Last month` uses the 12-byte original
Military Investment string slot at 02143E04, which the V799 menu repair made
unreferenced. A fresh full reference census proves that slot has no incoming
references. All four month literals are rebound; both identical numeric formats
share one string. Every NUL fits its allocation; the adjacent Reclaim allocation,
RTTI, other labels and all other bytes are preserved.

Sections, BSS, cache plan and the entire 123040-byte staged payload stay exact.
No storage growth, new code instruction or shorter English phrase is used.

## Executed native checks

- 35,320 exact selector, parent, pointer-stride and ABI/SP/LR cases pass.
- 140 complete status-output/8 MiB guard/ABI cases pass after the phrase move.
- 144 original month-provider cases produce full English phrases, with the
  original full-width numeric formatter and 128-byte native string slots.
- 1,169 paragraph layouts cover all 23 Inn IDs through their correct original
  caller contract. Every original town, goods and company name is exercised
  against the longest counterpart; every relative-month form is exercised with
  longest subjects. A 23-letter synthetic company name is explicitly included.
  This is not a full Cartesian event-eligibility test.
- 95 complete native font planes match independent source-font assembly. All
  eight generated sheets were visually inspected. The initial 1180 duration
  break was refined in manuscript V2; three new complete native font planes show
  3, 10 and 30 nights on one line. All other paragraphs remain byte exact.

Some image-tool thumbnails appeared to omit month words. Exact top-row pixels
for the five corresponding images are identical (SHA-256
`c9b11bee27344176bb94ec1de02f86356d8b32cea53b3723a0a1a670295c250e`);
the underlying complete native/independent planes retain the words. No game
defect is inferred from that thumbnail behavior.

## Evidence and remaining production work

Runtime proofs/image: `work/analysis/inn_runtime_v802/`.
Full initial layouts/sheets: `work/analysis/inn_runtime_v802/layout/`.
V2 duration refinement: `work/analysis/inn_runtime_v802/layout_v2_delta/`.
Current draft: `translations/inn_editorial_manuscript_v2.json`.

Next, repack all 23 reviewed paragraphs with exact preservation of the other
3645 COMMON selections and opaque payloads. Verify complete warm/cold native
copies for every affected block. Carry the corrected V2 duration into the
production layouts; retain the original V1 proof for the other 22 records.
Register and build through the combined release workflow, reconstruct its patch
exactly, and exercise revised stay, insufficient-funds, report and market/news
paths with source-bound isolated fixtures as needed. Verify full glyphs,
consistent margins, page transitions and ordinary returns. No revised-English
gameplay, completed Inn entry or full-goal completion is claimed yet.
