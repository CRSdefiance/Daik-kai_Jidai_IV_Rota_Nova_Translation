# V558 source-specific name plaque gradients

The previous turn integrated the Ships texture correction with actual display
and startup evidence. This turn reviews and corrects the alternate name plaques.

## Release identity

- Experimental ROM: `out/all_routes_combined_v558_candidate.nds`.
- E location: `E:/Rota Nova translations/Generated/out/all_routes_combined_v558_candidate.nds`.
- Candidate SHA256: `bf62f246f485c7adf9a763c7765bc63476128f73f6cce983717bf297877cff6d`.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile: `all-routes-unified-v558`; all114 accepted layers and470 inherited batches.
- New stage: `translations/name_plaque_gradients_v1.json`.
- Manifest: `out/all_routes_combined_v558_candidate.manifest.json`.
- Patch: `out/all_routes_combined_v558_candidate.xdelta`, SHA256
  `f935bc9b6ee186ce0212cd8ad5540cbea786e8b5f36b7d01dc3cc5af66a43cea`.
- Patch input: `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- No canonical promotion or human acceptance is claimed.

## Source finding and correction

The five dark plaques have different original gradients. Earlier authoring
reused column9 of the first plaque across every label, replacing visible source
material as well as Japanese lettering. The corrected row sequences are:

| Label | Original interior row indices1..9 | Restored background pixels |
|---|---|---:|
|Name|7,7,1,2,3,4,5,6,8|4|
|Middle|7,7,1,2,3,4,5,6,8|3|
|Last|7,7,7,1,2,4,5,6,9|105|
|Company|7,7,7,7,1,2,4,5,6|115|
|Birth|7,7,1,2,3,4,6,8,9|57|

Each original row has a unique most frequent nonwhite material sample. The
correction replaces only original Japanese white strokes with that same row's
material, preserves every other original material pixel, then retains the exact
existing English mask. All284 restored source background pixels and2013 original
nonwhite material pixels outside the English ink are verified. Source frame
highlights share white index15 with lettering; they are verified separately
against original frame pixels instead of counted as extra glyphs.

Both `/_pxl/slackimg12.pxl` and `/GRP/SLACKIMG.DK4` block12 receive identical
pixel indices. The archive block's64-byte header, palette and extent remain exact;
every other archive block is unchanged. The original loose palette has high bits
set that the embedded palette does not. Their15-bit colours are identical, but
the original flag words remain distinct and untouched. A first strict raw-palette
equality assertion correctly stopped preparation; no build was produced by that
attempt. The revision verifies original flags separately and colour equivalence.

Only these two internal files change from V557. All code, other translations,
atlas dimensions, palettes and unrelated storage remain exact.

## Translation review

The existing natural field labels remain Name (名), Middle (ミドルネーム), Last
(姓), Company (勢力名, the player's organization) and Birth (誕生日, date of birth).
They remain consistent with the established captain-selection terminology and
fit the source plaques. No spelling or name-localization decisions are changed.

## Verification and scope

- Registered integrated builder completes from the immutable canonical base.
- `scripts/verify_name_gradient_release_v558.py --static-only` and full verifier pass.
- All five independently decoded font masks preserve every first/final letter.
  Only the two proven blank top font rows are trimmed; all nine ink rows remain.
- Six complete native screen comparisons pass589824 pixels with no exclusions.
  The sprite's full2640 pixels include all59 zero-index positions, whose visible
  background is checked against the unchanged control rather than assumed black.
- Both original image index12 and its index19 alias display all five corrected
  plaques at three frames each:30 complete label appearances.
-56 unique ordinary startup regression frames remain exact to V557;57 records
  include the duplicate final frame. Inputs and core options are identical.
- Exact clean-ROM patch reconstruction matches the entire production candidate.
- Ruff passes for the release module, prototype, fixture generator and verifier.

Native sprite tests are isolated original-event-instruction fixtures. Each alters
only four bytes in SC0 block44 at offset30, using the original clean SC1 block296
instruction template; all other bytes/art remain exact to its declared parent.
Control and candidate fixtures have separate hashes and are not distributed as
playable candidates. No donor save or savestate is loaded. These tests prove
rendering and aliases, not an ordinary story trigger or native use of the embedded
archive copy. Wider alias consumers, original context and transition states stay
open. Startup regression runs the actual production ROM, without a preloaded save.

The first static mask check treated white source chrome as glyph ink and stopped
before fixture creation. Two subsequently attempted absent-fixture loads were
rejected by the core and receive no credit. Corrected `_actual_r2_12/19` captures
are the credited runs; both controls, both candidate fixtures and the ordinary
startup run all finish exit0. Diagnostic folders are retained.

## Artifacts and remaining gates

- `work/analysis/name_gradients_v558/release_proof.json`, static/stage/prototype proofs.
- `name_gradient_review.png`, fixture manifests and navigation schedules.
- `E:/Rota Nova translations/Generated/work/emulation_v193/name_gradient_v558_*`.
- Controlled screenshots/provenance:
  `E:/Rota Nova translations/Screenshots/Test fixtures/name_gradients_v558`.

Screenshots are labeled test fixtures, not guide-approved ordinary gameplay.
User review areas: title/New Game, established story/town screens and any actual
name-plaque context found during play. All22 historical requirements retain exact
scope; all18 original plaque/hint entries remain incomplete. Material families,
embedded/raw legacy native consumers and wider gameplay gates remain open. The
graphics goal remains active.
