# Combined V253: complete Square caption backing; plaque audit stays open

## User audit requirement

All17 Assign Sailors/Sailor Info plaques plus Equipped Items remain in both
authoritative audits as `pending-continued-audit`, `fully_completed: false`.
Armor/Weapon variants remain incomplete. Nothing in this checkpoint closes them.
Ordinary navigation found an empty new-game inventory, so occupied equipment
names and additional hint widths remain unverified. Full graphics goal stays active.

## Observed repair and limits

The Square generated correct full labels but painted into a48x12 inline bitmap,
dropping the trailing letters. Its pixels abut the header, so in-place enlargement
would corrupt the object. A source-locked final stage supplies18 private64x12
backings, retains the original palette address, and advances the original six-pixel
glyph cells by five pixels without dropping glyph ink. Only this shop caller maps
original 装飾品 / inherited Jewels to natural **Jewelry Shop**; shared commodity
names remain unchanged. Other category spellings are inherited and require later
terminology review where abbreviated. Original menu frames are preserved.

Native verification executes the real view constructor, category getter and text
painter for18 categories plus the out-of-range fallback. Every glyph matches an
independently decoded native font; saved registers, stack, header, palette and
padding checks pass. Header, goods index and cleared backing are explicit harness
inputs. These are not live inventory or GPU proofs.

A fresh16400-frame DeSmuME cold boot follows the recorded ordinary input schedule,
with no loaded savestate or injected RAM. **Food Shop** and **Liquor Shop** match
all111 and122 native ink pixels at their measured origins, including first/final
letters. The18 earlier sampled framebuffers and the entire upper town panel remain
exactV252. The existing Trends button covers most of the third sign row: **Jewelry
Shop visibility is still pending**, although its native backing raster passes.
This overlap is a separate open layout defect, not a completed third-row check.

## Reproduction and integration

FullV252 reproduction is byte-for-byte exact. The final registered builder run
exits0 withUTF-8 output. All467 inherited batches, required layers, prior changed
records, all ROM files/routes/art, ARM7 and overlays remain exactV252; only ARM9
changes. The clean-base xdelta reconstructs the candidate exactly. Nine focused
startup/plaque preservation tests pass and modified Python passesRuff.

The native autoload test's old100000-step ceiling was too small for the expanded
pool. Its bounded budget now derives from section data/BSS sizes; real code and
all native startup/cache/ARM7 checks pass. Earlier failed research attempts remain
in logs. An initial generic pytest faulthandler emitted a Windows native diagnostic
while all nine tests passed; a captured rerun without faulthandler exited0. The
standalone native verifier also exited0. Console Unicode output failed after an
earlier ROM/manifest write; the completeUTF-8 rerun succeeded with identical bytes.

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v253` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Candidate | `out\all_routes_combined_v253_candidate.nds` |
| ROM SHA256 | `e52a4a83af98fed5a870494b3ba34903a77ff1fcb938068bcde74c91d55b49a8` |
| Patch | `out/all_routes_combined_v253_candidate.xdelta` |
| Patch SHA256 | `0a277087fc3f6b3471ac71670c2787412809de983c3909ba5d926b998c211c37` |
| ARM9 SHA256 | `aad56e57a642445c46a7cd5b5b26130e1ecebec502ececcbe17be87bbdd10265` |
| Native proof | `work/analysis/occupied_equipment_v253/native_proof.json` |
| Saved/live proof | `work/analysis/occupied_equipment_v253/saved_live_proof.json` |
| Review sheet | `work/analysis/occupied_equipment_v253/square_caption_review.png` |

Experimental candidate; user acceptance and physical-device verification pending.
Trends overlap, other cities/categories, occupied equipment, health/mood variants,
source/Gallery/environmental gates and locked-name consistency remain open. Revisit
older record-based checks at actual goal completion. Canonical remains unchanged.

## Later V254 evidence supersedes the overlap classification

Extended ordinary gameplay verifies complete Jewelry Shop before/during sign
selection. Trends is the original temporary contextual menu, not permanent
caption loss. V254 corrects the separately observed narrow selection bounds.
See `all_routes_unified_v254_checkpoint.md`; shopkeeper message658 fidelity is open.
