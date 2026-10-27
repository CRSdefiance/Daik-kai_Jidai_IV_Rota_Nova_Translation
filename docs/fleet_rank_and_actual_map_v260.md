# V260: actual Route Map and complete Admiral rank labels

## New observed Japanese UI text

Ordinary cold boot and controller input reach Route Map, then select the nearby
player fleet with RIGHT. The actual fleet view contained untranslated 提督.
Two original `%s提督` formatters and one 地方提督 role label remain in clean/current
ARM9 at the exact pointer fields recorded in `runtime_plan.json`.

The shared formats now read `%s Admiral`; the separate role reads **Regional Admiral**.
This preserves the original rank and substituted identifier without inventing a
relationship or shortening the label. The exact Japanese originals are verified
against clean ARM9. All three complete strings are relocated into the owned pool;
neighboring original strings and all rendering code remain intact.

The photographed line is **１ Fleet Admiral**, not Lil Fleet Admiral. Native35258
gets a numbered fleet identifier, increments its ordinal and runs ABF50's full-width
numeric conversion before formatting the fleet label. The top title separately
shows Lil Fleet and the named captain. This distinction is verified from source and
font pixels; a full-width１ was not mistaken for a lost L or I.

## Native and actual display proof

Forty-five native cases execute original printf/text rendering with full fleet names
up to18 bytes, F/I-starting names, one-to18-letter length tests and the complete
Regional Admiral role. Every leading/internal/trailing glyph matches the original
font. The172-pixel surface is a supplied test contract, not every alternate parent
geometry. Saved registers, stack, header/view/output guards, inherited pool bytes,
boot/cache/ARM7 ownership and arena checks pass. Two other actual parent displays
remain to visit despite their native text/pointer checks.

A fresh34000-frame DeSmuME run follows the recorded ordinary purchase/inventory/map
path with no savestate loaded and no RAM injection. The full-width digit and all
English letters in the actual rank line match165 independent font-mask pixels.
Only215 pixels in the rank-suffix region differ fromV258; the fleet identifier,
portrait, other labels, complete lower map and controls are unchanged. All36
comparable earlier whole frames matchV258, including the aligned shopkeeper text,
Guild purchase and acquired map inventory. Processes are terminal; Ruff passes.

## Actual map evidence and limits

The actual map picture occupies x6..250,y208..368:244x160, fully inside the lower
screen. The city overview and fleet view were both observed through normal input.
Its water is blue, while the previously reviewed seamap source palettes are sepia.
A whole-crop same-position/index-color fit accounts for only21866/39040 pixels
under its best tested page. Marker/route/popup overlays and a different palette or
parent remain unresolved. This is not seamap byte-copy identity or an actual bank/
UV/alpha proof. The previous64 native supplied-view tests remain separate evidence.
No map artwork is copied, resampled or rewritten based on this comparison.

## Complete integrated artifacts

FullV258 reproduces byte-for-byte through the updated registered builder. V260
retains all467 batches, required layers/stages and previous changed records. All
ROM files, routes, artwork, ARM7 and overlays are exactV258; only ARM9 rank pointers
and the owned startup/cache extent change. The clean-base xdelta reconstructs the
candidate exactly. Canonical remains unchanged.

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v260` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Candidate | `out/all_routes_combined_v260_candidate.nds` |
| ROM SHA256 | `31e1118861e95c2e7c4cc4b50d1b59defc71d44ca898d118d35f3a2c0e8828f3` |
| Patch | `out/all_routes_combined_v260_candidate.xdelta` |
| Patch SHA256 | `458eec7285b841dfc69cc3e5250ef26e85932b3de1f1c7285a30a4d3480ee5db` |
| Source/formatter/native proof | `work/analysis/fleet_rank_v260/native_proof.json` |
| Saved-ROM/actual-glyph proof | `work/analysis/fleet_rank_v260/saved_live_proof.json` |
| Before/after sheet | `work/analysis/fleet_rank_v260/rank_review.png` |

Experimental candidate; user cold-boot acceptance/device review pending. Review the
fleet rank display, alternate fleet/detail views and Regional Admiral selection.
All17 plaques plus Equipped Items and Armor/Weapon variants remain incomplete.
Occupied equipment, other status/route contexts, four Online body source transcripts,
legacy/Gallery/environmental native gates, naming consistency and final full-game
verification remain open. The graphics goal stays active. Revisit older record-based
checks at actual completion.
