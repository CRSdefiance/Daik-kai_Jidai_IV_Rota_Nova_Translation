# Combined V254: full Square sign selections and continued audit

## Corrected diagnosis

Extended normal gameplay shows every complete caption before the Trends choice
menu appears and during actual sign selection. Trends is a temporary contextual
menu. Its caller, generic menu creation and placement code are byte-identical to
the original Japanese ROM. The earlier V253 permanent-overlap classification is
superseded; original behavior is retained. The help-dialog border also covers one
bottom scanline in frame17200; unobscured frame18000 verifies full Jewelry Shop.
Source/context proof: `work/analysis/square_sign_bounds_v254/v253_extended_gameplay_proof.json`.

## Actual scoped correction

V253 enlarged the caption backing, but the selectable sign rectangle still ended
16 pixels before it. The sole native reference uses a private Square rectangle.
V254 changes its right coordinate100 to116, keeping x20, y positions, icons,
palettes, caption backings, glyphs and original outer window/menu borders exact.
Only one byte in one four-byte ARM9 coordinate word differs from fullV253.
All five native possible rows fit the original frame. Native focus painting adds
its original two-pixel padding: measured selected rows are100x28 pixels, and their
right edge stops before the frame at x186.

A fresh20000-frame DeSmuME cold boot uses ordinary controller inputs, no loaded
savestate and no injected RAM. Food Shop, Liquor Shop and Jewelry Shop are each
selected. Every first/internal/final native glyph pixel matches in all three states:
111/122/136 ink pixels per caption. The complete compared Food selection screen
differs only in448 new background pixels in the16x28 focus extension. Eleven
comparable earlier full frames matchV253, including title/selection/story/town and
Square contextual menu. Activating Jewelry reaches Square Shopkeeper at frame20000.

## Open text finding; candidate remains experimental

The activated shopkeeper line needs a separate rendering-fidelity investigation.
The candidate stores full `Business? Fair. I wish a good` followed by
`opportunity would arise.` in `/COMMON/MESFILE.DK4`, native message658,
record `DK4_MES_B08_R0008`. The captured first sentence appears to lose F;
the native font matches the observed `air.` word exactly at x88,y296. The full
preprocessing/cursor trace and a source-faithful natural-English review remain
pending. This graphics verifier does not certify complete dialogue fidelity.
Evidence: `work/analysis/square_sign_bounds_v254/shopkeeper658_followup.json`.

All17 plaques plus Equipped Items and Armor/Weapon variants remain explicitly
**incomplete, pending continued audit** in both authoritative registries. Other
health/mood conditions, occupied equipment, other city/category parents, source
transcripts, Gallery/environmental native gates and locked-name consistency remain
open. Higher-resolution originals for Online24/27/31/33 have been requested.
The full graphics goal remains active. Revisit older record-based checks at actual
completion; this runtime finding reinforces why stored text alone is insufficient.

## Reproduction and integration

EntireV253 reproduces byte-for-byte through the updated registered builder. All467
batches, required layers, prior changed records and every inherited stage remain.
All files/routes/art, ARM7 and overlays are exactV253. The source-locked ARM9
stage changes only the private rectangle coordinate. Clean-base xdelta reconstructs
the candidate exactly. Native bounds, full selected-caption/saved-ROM verification,
Ruff and the focused existing plaque tests pass. Capture processes are terminal.

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v254` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Candidate | `out/all_routes_combined_v254_candidate.nds` |
| ROM SHA256 | `a7eaadff1f08166fd5db986525b442195b151f7093e7252b9a3ec40286176489` |
| Patch | `out/all_routes_combined_v254_candidate.xdelta` |
| Patch SHA256 | `49458b1572ad6c10641e4d8970faa0346a85ba3d540808b12ddfcaf1f59afefd` |
| ARM9 SHA256 | `1c6a248091defe2b7b5a5f94906782125c86476402d058a79efac7f595b7ba20` |
| Native proof | `work/analysis/square_sign_bounds_v254/native_proof.json` |
| Saved/live proof | `work/analysis/square_sign_bounds_v254/saved_live_proof.json` |
| Review sheet | `work/analysis/square_sign_bounds_v254/all_three_selected_review.png` |

Experimental research candidate; dialogue-fidelity follow-up and user acceptance
pending. Canonical unchanged. No claim of full-game or physical-device verification.
