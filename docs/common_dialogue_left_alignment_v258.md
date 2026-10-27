# Consistent dialogue left margins V258

The user's shopkeeper screenshot has first-line x28 and continuation x22.
V258 aligns both to x22, retaining the established textbox padding and every letter.

## Mechanism and verification

The actual portrait/modal dialogue draw is02054924, inside020548A8. A source-locked
wrapper paints the two initial empty guard spaces at three-pixel advance, then
restores six-pixel letter advance and renders the original remaining string.
Source guard bytes, stored strings, clip bounds and LF handling are unchanged.
No visible glyph is condensed or cropped. Three-or-more-space indentation,
control prefixes, nonzero tracking and undersized views retain original behavior.
Normal CP932/full-width F/I starts are supported. Null strings delegate to the
original function. Code/data live in the existing owned staged pool; no RAM cave.

Twelve native complete-letter/phase/Janus/CP932 cases and six fallback/small-view
cases pass, including input/header/pixel guards, return pointers, tracking and
saved-register/stack ABI. Native boot/cache/ARM7 ownership and arena checks pass.
A fresh20000-frame DeSmuME cold boot uses ordinary input without loaded savestates
or RAM injection. The user's actual shopkeeper sentence has280 first-row and246
continuation ink pixels, all matching the unchanged native font at x22. Every
continuation pixel is unchanged. Five changed captured rows retain every original
foreground pixel shifted left6; all48 other full frames are exactV255. Title,
selection/opening/town/Square and all three sign selections are traversed.
This is targeted emulator verification, not an exhaustive playthrough/device test.

## Failed experiment preserved

V257 applied the same padding treatment at Basic02007F5C, which this box does not
use. Native isolated tests passed but the actual shopkeeper image remained unchanged.
That candidate/profile is revoked and was not handed off. V258 derives from fullV255,
with the actual modal caller selected. Historical config defaults preserve the
old caller's reproducibility; the new config explicitly records02054924.
The earlier guard-cursor experiments that lost Janus's J are not reused: V258
changes neither LF processing nor continuation cursor positions.

## Complete inherited build

EntireV255 reproduction is byte-for-byte exact. All467 batches, required layers,
prior stages and changed records are retained. Every file, story/COMMON string,
art asset, ARM7 and overlay is exactV255; only ARM9 gains the scoped wrapper and
updated owned startup/cache extent. Clean-base xdelta reconstructs exactly.
Ruff and native/saved-ROM/glyph checks pass. Canonical remains unchanged.

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v258` |
| Candidate | `out/all_routes_combined_v258_candidate.nds` |
| ROM SHA256 | `da3826983959c31104b7c1e3b66b65e3f69abb89fb71501a4d2a4c63a5bac613` |
| Patch | `out/all_routes_combined_v258_candidate.xdelta` |
| Patch SHA256 | `43e51c5a34afe1c42bab3cdcc65f3a067699ec38e92da055a6f0955a06d7d40f` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Native proof | `work/analysis/common_alignment_v258/native_proof.json` |
| Actual capture/glyph proof | `work/analysis/common_alignment_v258/saved_live_proof.json` |
| Before/after sheet | `work/analysis/common_alignment_v258/shopkeeper_glyph_review.png` |

Experimental candidate; user cold-boot acceptance pending. Review dialogue margins
and complete first/last letters on the user's emulator. All18 plaque/hint entries
and Armor/Weapon variants remain incomplete. Broader graphics/source/native/gameplay
requirements and the full graphics goal remain open. Revisit older record-based
checks at actual goal completion.
