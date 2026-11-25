# V534: complete Historic Sites image descriptions

## Actual viewer and complete source family

The prior V528 checks covered lists and map headers. Opening the image viewer
revealed 19 additional Japanese paragraphs. V534 translates every supported
entry, retaining each description's facts, dates, attribution, discovery port,
and exact influence reward in natural American English. Historical claims are
preserved as the game's account rather than silently rewritten. Established
port names include Sao Jorge, Calicut, Hangzhou, Seoul, and Osaka.

Source-backed supported entries use `/Iseki/Iseki00.pxl` through
`/Iseki/Iseki18.pxl`. The original 21-slot image-owner table at `0x02115748`
contains null entries for IDs1/4; their description slots contain `無い無い`
placeholders. These are excluded from the supported-image fixture. All19 entries
then open, wrap and return normally. The earlier synthetic all21/single1/4
failures are retained as diagnostic evidence, not production translation defects
or proof that those names are globally unused. No game code is changed to hide
the invalid image selection. The preparer and declared supported-fixture preflight
verify the original image table and selected save bits.

## Renderer fix and owned storage

V530's full pixel comparison caught 17 pixels belonging to the next line's
leading `d` drawn at the previous line's end. V532's raw-byte LF parity hypothesis
did not fix it. Both builds are revoked and were not published or promoted.

Native `D5404` handles LF separately from the virtual painter, which buffers
printable ASCII glyphs in pairs. An odd-length printable line can leave a glyph
pending when the cursor moves. The v3 formatter finishes each such line with a
generated empty cell before LF. It wraps at41 characters to reserve that cell
inside the original256-pixel surface. This is compiler output, not translator
padding. Each authored paragraph remains one logical paragraph. Every line
starts at x0; there is no next-line guard indent, truncation, or manual prose wrap.
All19 actual full-paragraph masks prove the corrected placement and complete
first/final letters, including the previously failing `d`.

The 19 original description allocations, 21 already localized site-name
allocations and42 numbered Characters label allocations provide3668 owned
bytes. All82 complete strings fit in3636 bytes. Every source span, current label,
pointer owner and unowned byte is guarded. Apparent unaligned pointer patterns
cross unchanged executable ARM instructions; their exact instruction words are
recorded separately. All42 Character labels and21 site names retain their full
wording. Every164 Event Scenes caption/pointer/bound stays exact.

No section growth, startup copy, allocator boundary, cache wrapper, original
image, palette, border, dimension or other component changes. The original
unsupported placeholders remain unchanged.

## Verification

- All19 complete captions and natural-English paragraph masks pass.
- All933888 pixels of the actual19 source images match their PXL palette/index
  data at native five-bit color precision.
- Every pixel outside the description region matches V528's source control.
- Supported-image list, carousel wrap and return pass without a CPU fault.
- All42 actual Characters frames, full labels, wrap and Back remain exact to
  V525. Their actual RAM contains the complete strings at their new pointers.
- All21 original native site-name getters retain complete bytes and saved-register
  ABI, including unaligned C-string addresses.
- All56 fresh title/New Game/story/town/Help frames remain exact to V528.
- All470 batches,114 accepted layers,675 PXL/FLS and921 preservation entries
  retained; clean-ROM patch reconstructs exactly. Targeted Ruff passes.

These are targeted original-consumer tests under isolated copied-save flags.
Normal discovery/acquisition, original ending triggers and wider legacy contexts
remain under audit. No hardware or full playthrough claim.

## Release and evidence

Experimental candidate: `out/all_routes_combined_v534_candidate.nds`.
Profile: `all-routes-unified-v534`.
SHA-256: `cac800924a1dfb3e2bc6352ef3f47f8f82986229377de20bc5e194046b5a6f45`.
Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Canonical unchanged; only ARM9 differs from V528.

Verifier: `scripts/verify_site_descriptions_v534.py`.
Formatter/layer: `dk4tool/patch/site_descriptions.py`.
Reviewed paragraphs: `translations/historic_site_description_manuscript_v3.json`.
Registered configuration: `translations/site_descriptions_v3.json`.
Proof, preservation chain and copy receipts: `work/analysis/site_descriptions_v534`.
Source review, supported fixture and controls: `work/analysis/site_descriptions_v529`.
Rejected-build evidence remains in `site_descriptions_v530` and `site_descriptions_v532`.

ROM, patch, manifest and BUILD_NOTES_V534 are published with exact hashes to
`E:/Rota Nova translations`. Labeled fixtures and their proof are archived under
`Screenshots/Test fixtures/site_descriptions_v534`. All22 historical requirements
and18 incomplete plaques remain. The full graphics goal is active. Revisit older
record-based checks after the full goal is complete.
