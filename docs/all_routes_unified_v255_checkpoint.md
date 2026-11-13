# Combined V255: shared literal F/I macro repair

## Root cause and high-level correction

V254's actual native macro preparation reproduced the stored shopkeeper sentence
as `Business? air.` followed by Japanese 僕 in place of English `I `.
The defect occurs before glyph rendering. Native53914 treated every capital F as
a macro prefix and dropped it even when its suffix was invalid; every capital I
entered pronoun expansion and consumed the next byte. Existing dynamic-name
escaping did not protect ordinary authored ASCII prose in this path.

The terminal source-locked stage validates F suffixes before entering the native
FA/FI/FO/FU handlers. Invalid F prefixes use the existing single-byte literal copy.
IC keeps the actor-sensitive source pronoun. Printable ASCII suffixes and a terminal
I use literal copy; legacy non-Latin/control suffix behavior remains unchanged.
Original dispatcher, model callbacks and macro-result copy logic are retained.
The shared function serves multiple native callers; this fixes the preprocessing
rule instead of replacing the shopkeeper's sentence with a workaround.
Recognized macro spellings remain controls; ambiguous literal uppercase sequences
still require the existing authored-literal encoding and later context review.

## Verification scope

- All3668 current COMMON entries expand byte-for-byte to their stored strings.
- Native before/after comparison repairs110 previously corrupted entries, including
  generic confirmation13 and shopkeeper658. Full IDs/outputs are in the native proof.
- All3668 original Japanese entries are compared under two controlled actor results:
  7336 cases unchanged, including every source IC expansion.
- FA/FI/FO/FU, terminal F/I, punctuation and ordinary English words pass native tests.
  Fourteen focused tests pass. Original saved-register/stack ABI, input/output guards,
  inherited pool bytes, boot/cache/ARM7 ownership and arena checks pass.
- Actor/model getter results are explicit native-harness contracts. This is complete
  prepared-text coverage, not3668 physical or GPU display tests.
- A fresh20000-frame DeSmuME cold boot follows ordinary input through title, New Game,
  selection/opening/town, all three Square sign selections and Jewelry activation.
  No savestate is loaded and no RAM is injected. The entire shopkeeper sentence
  matches526 independently decoded ASCII-font ink pixels:280 on the first line and
  246 on the continuation. First/internal/final letters are intact; no injected
  Japanese glyph remains. Only297 first-line pixels differ fromV254; the complete
  continuation row and51 earlier full captured frames are exact. Generic confirmation13
  is covered by native preparation; this run does not separately prove its UI owner.

The first native legacy-I synthetic test omitted its required suffix byte before
Japanese text and failed the guard check in the original routine too. The corrected
explicit control-suffix input passes. No shipped text is altered by that harness fix.
Ruff passes. Build and capture processes are terminal.

## Integration

The updated builder reproduces all ofV254 byte-for-byte. V255 retains all467 batches,
required layers/stages and changed record IDs. Every ROM file, story/COMMON string,
art asset, ARM7 and overlay is exactV254; only ARM9 gains the two guards and owned
startup/cache extension. The clean-base xdelta reconstructs the candidate exactly.
No graphics, translation wording or canonical base is replaced.

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v255` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Candidate | `out/all_routes_combined_v255_candidate.nds` |
| ROM SHA256 | `9d8553cb2d1566a6754eb21269515e1af1677b51a4cce11450d4cdb92068ddc4` |
| Patch | `out/all_routes_combined_v255_candidate.xdelta` |
| Patch SHA256 | `907b6a62598d60e76c8e29ea2f9a0ac085dfbdd7ebb45b6a86935d622e502371` |
| ARM9 SHA256 | `1df6b503368237b5b508d91fe2177a7c0c23419d86a1e0e44a561644e59b2944` |
| Native proof | `work/analysis/common_literal_prefix_v255/native_proof.json` |
| Saved/live proof | `work/analysis/common_literal_prefix_v255/saved_live_proof.json` |
| Review sheet | `work/analysis/common_literal_prefix_v255/shopkeeper_glyph_review.png` |

Experimental candidate; user cold-boot acceptance and device review pending. Test
confirmation/dialogue and town/ship/equipment screens on the user's emulator.
All17 plaques plus Equipped Items and Armor/Weapon variants remain explicitly
incomplete in both audits. Other health/mood/occupied-item contexts, source transcripts
for Online24/27/31/33, embedded/Gallery/environmental native gates, locked-name consistency
and older English wording remain open. This is not a full-game display guarantee.
The graphics goal remains active; revisit older record-based checks at actual completion.
