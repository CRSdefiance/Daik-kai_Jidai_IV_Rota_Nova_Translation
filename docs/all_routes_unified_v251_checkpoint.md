# Combined V251: old Japanese call fringe removed

The previous goal turn reviewed raw embedded banks. This turn reviews the existing
comic wording, adds final five-bit character checks, and fixes a source-lettering
remnant. The full graphics goal remains active and incomplete.

## Source and wording review

The original artwork was re-extracted from the immutable canonical source and
reviewed at integer enlargement. Existing natural English is retained. The
recruitment heading and kana creator credits remain Recruiting New Crew / Nanae
Hosokawa / Kyoko Nakamura (Madogiwa Deka). The source cow/bullfighter joke retains
its explicit Sea cow adaptation. Maria's Chinese invitation remains natural
English for visiting and asking whether she has time; no speaker split is invented.
The tiny seal keeps the full established Uncharted Waters IV title.

## Concrete source-fringe defect and fix

The old red Japanese `ヤダー` call left43 faint source-colored pixels. The old
outline predicate protected colors whose channel spread was at most1; it therefore
misclassified almost-neutral red antialiasing as a gray bubble outline.

The new versioned `source-chase-call-mask-background-v8` rule excludes red-tinted
fringe from that neutral protection. Erasure still requires membership in the
existing source-connected glyph mask. It changes exactly43 BGR555 pixels (86 bytes)
in frame5's owned caption region. Each old pixel has red greater than both other
channels by1. All genuinely neutral pixels, all other source pixels, the English
wording, picture borders and earlier translations remain byte-identical to V247.
Covered original outline/scenery estimates remain explicitly approximate.
The old v4 rule remains unchanged for historic profiles.

## Final-letter and integration checks

All18 stored comic word planes reproduce exactly from their source-locked renderer.
The new checker removes only full-line/segment English painting in a separate
research rendering while retaining the same source restoration. Against that
backing, every one of331 character bounds has final five-bit color contrast.
All letters are in bounds and their sequence exactly matches the English text.
Thirty-six first/final-letter erasure checks detect damaged lettering.
This checks complete saved planes and surviving character bounds, not native
Gallery readability, unique per-glyph pixel attribution or original hidden scenery.

The complete V247 ROM reproduces exactly after the versioned renderer addition.
All467 inherited batches,114 accepted layers baked into the canonical source,
prior record IDs and terminal runtime stages remain. ARM9, ARM7, overlay, routes,
all other files and all other SLACKIMG blocks are unchanged. All direct-color high
flags and file/ILNK allocation are unchanged.

The original ILNK constructor/directory/read/copy/close code retrieves all3,225,600
bytes of block19, in bounded chunks with canaries and original caller ABI. Only
SDK filesystem calls are bridged to this exact ROM. This is generic native archive
readback with valid supplied indices/buffers, not a Gallery-viewer or GPU fixture.

Fifty-three source-outline, character deletion and raw-art preservation tests pass;
all changed Python files pass Ruff. Two fresh ordinary New Game cold boots cover
title/selection/story/town and the crew/sailor paths. All49 captured framebuffers
are byte-identical to V247. The repaired raw comic is not displayed by those paths.
The exact clean-ROM xdelta reconstruction is byte-identical to the candidate.

## Full handoff identity

| Item | Identity |
|---|---|
| Canonical build base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA-256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Profile | `all-routes-unified-v251`, experimental |
| Complete stack |467 inherited batches; all required accepted layers/stages retained |
| Candidate | `out\all_routes_combined_v251_candidate.nds` |
| Candidate SHA-256 | `500345a239fedb4b0db24522f023fbcffc0d269d5d9958056d67b08c41ccfd0b` |
| Patch | `out\all_routes_combined_v251_candidate.xdelta` |
| Patch SHA-256 | `3a7285a80bc1fc4e33235205b5a6fa4c775ae210ccd3167ebf041455e9ed758c` |
| Manifest | `out/all_routes_combined_v251_candidate.manifest.json` |
| Changed path vs V247 | `/GRP/SLACKIMG.DK4`, block19 only |

Preview: `work/analysis/comic_fidelity_v251/new_chase_preview.png`.
The raw art interpretation is21×320×240 BGR555; its native Gallery loading,
geometry/crops/alpha/display remain unproved. User cold-boot acceptance is pending.
Please check title/New Game/story/town and the ongoing crew/sailor screens. If the
recruitment comic can be reached, check its lettering and bubble boundaries; no
such native path is claimed by this checkpoint. The canonical baseline is not
promoted.

## User-required ongoing plaque audit

All17 redesigned plaques and Equipped Items remain **incomplete, pending continued
audit and user review** in both authoritative audits. Regression screenshots do
not close those18 entries. Other exact Online sources, native/embedded/environmental
coverage, naming consistency and final whole-goal review remain open. Revisit older
record-based checks at eventual goal completion, as requested.

## Evidence

- `scripts/verify_comic_final_letters_v251.py` and `current_letters/proof.json`.
- `scripts/verify_comic_fringe_release_v251.py` and `release_proof.json`.
- `work/analysis/comic_fidelity_v251/fringe_delta.json`: all43 exact changed words.
- `translations/gallery_chase_fringe_raw_art_v8.json`: explicit v7 supersession.
- `work/emulation_v193/comic_fringe_v251/{crew,person}/capture_report.json`.
