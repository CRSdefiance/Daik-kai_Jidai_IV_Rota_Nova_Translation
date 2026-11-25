# V261 World Map selection headers

## Observed remaining Japanese and source-faithful correction

Ordinary input opens Forces, shows the player faction and an Unknown Force with
concealed values, and opens World Map using Y. Its lower title is 海域. X changes
selection type and exposes 艦隊・村. These are actual visible UI headings, not a
Japanese reading inferred from painted terrain. The first A attempt in Forces had
no effect; it is recorded, not claimed as list/detail activation.

The lower headings are now **Sea Areas** and **Fleets/Villages**. The upper mode
label formerly said Fleet/Town even though its original source is also 艦隊・村.
It now says **Fleet/Village**, preserving original village meaning and consistency.
Three source-locked pointer fields are relocated into the owned pool. Clean and
current source text is validated; neighboring data and all art stay intact.

## Verification

All three complete English strings pass original native font rendering, bounded
headers/views/pixels, return/saved-register/stack and inherited boot/cache/ARM7/arena
checks. The supplied172-pixel native test width is separate from real menu geometry.
Actual fresh36000-frame DeSmuME cold boot uses ordinary recorded input, without
loaded savestates or RAM injection, and reaches both selection modes.

- Sea Areas:105 complete native ink pixels, centered at x101,y194.
- Fleets/Villages:172 complete pixels, centered at x83,y194.
- Fleet/Village: select one.:263 complete pixels at x64,y64. Category and colon
  retain cyan; the remaining instruction retains white. Every first/internal/final
  letter is present, with no extra glyphs and no overflow.
- All540 actual glyph pixels match independently decoded source font masks.
- The complete world-map picture, markers and bottom controls are exact toV260 in
  each mode. All23 comparable earlier full frames match, including title/selection,
  dialogue margins, Guild purchase/inventory, map fleet rank and Forces states.
- Unknown Force/? fields are recorded as concealed UI; identities are not invented
  from portraits. Alternate rank parents were not reached and remain open.

FullV260 reproduces byte-for-byte through the updated registered builder. All467
batches, required layers/stages and earlier changed records remain. Every file,
route, artwork, ARM7 and overlay is exactV260; only ARM9 label pointers and the owned
startup/cache extent change. Clean-base xdelta reconstructs exactly. Native and
saved-ROM/actual-pixel verifiers pass; changed code passesRuff. Captures are terminal.

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v261` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Candidate | `out/all_routes_combined_v261_candidate.nds` |
| ROM SHA256 | `50319a1623c5118ac9274f231c6b602fa1dc071e1510c287e649a25a7b90e135` |
| Patch | `out/all_routes_combined_v261_candidate.xdelta` |
| Patch SHA256 | `145c361b31db6f074a5ee05f7f7d77f961dcd38632df70b45c6c9ca82180c999` |
| Native proof | `work/analysis/world_headers_v261/native_proof.json` |
| Saved/live proof | `work/analysis/world_headers_v261/saved_live_proof.json` |
| Both-mode review sheet | `work/analysis/world_headers_v261/both_modes_review.png` |

Experimental candidate; user cold-boot acceptance and device review pending. Test
both World Map selection modes, complete centered labels and the retained fleet
rank/dialogue margins. Canonical unchanged. All17 plaques plus Equipped Items and
Armor/Weapon variants remain explicitly incomplete. The four Online source bodies,
occupied equipment, legacy/Gallery/environmental native use, map palette/UV source,
other status/route contexts, name consistency and final full-game verification remain
open. The graphics goal stays active. Revisit older record-based checks at completion.
