# Occupied equipment and variable paper V270

## Ordinary acquisition and source review

A fresh Rafael boot reaches Lisbon. The Guild facility is confirmed by its displayed
name, using Square then UP; icon guesses are not identity evidence. The Guild
lists **Travels of Marco Polo**, original clean Japanese **東方見聞録**, item88,
price10000, Equipment / First Mate / Effect34. A normal purchase is confirmed by
the Guild's Thank you, and the owned inventory contains the book. Y Equip assigns
it to Rafael; the third Sailor Info slot shows its icon. The displayed Speech
value changes from88 to122, matching the displayed effect34. This is an observed
UI change, not an independent saved-stat arithmetic proof. No balance-debit claim
is made from the cached town HUD.

All1024 pixels of the original32x32 inventory image match the unchanged native
item atlas at five-bit precision. The full21-letter English name is source-faithful
and retained. The existing Raphael runtime spelling still differs from locked
Rafael policy; that separate consistency gate remains open.

## General paper repair

The occupied130x16 name tooltip was flat tan because the earlier paper dispatcher
supported only34/40/88 widths. V270 tiles the same source paper over every width
10..244 at height16, preserving two-pixel corners and repeating its40-column
interior. All known34/40/88 cases delegate to the original verified helpers.
Only the matching active tooltip manager and two source-native framebuffers are
eligible. Invalid screen/geometry and inactive scopes delegate to the original
function. No other graphics file, font, item name, statistic or gameplay code is
changed. Native framebuffer and clipping addresses come from the original fill
routine and same-frame read-only export; they are not new RAM caves.

470 native cases execute every supported width on both real framebuffer layouts,
including the original native fill for the three old shapes. Every paper pixel,
all untouched framebuffer bytes, guard bytes, saved registers and stack returns
match. Nine invalid/inactive cases make no new framebuffer writes. Boot/cache,
ARM7 source ownership and arena checks pass.

V269's slower run-based experiment passed a draw-request bridge but failed its
actual whole-ROM screenshot comparison, with changes below the tooltip. It is
revoked and was not handed off. A separate actual-fill reproduction remained
bounded. The failure's exact scheduling cause is not proved; no unsupported
register-clobber diagnosis is adopted. V270 uses direct bounded framebuffer stores,
avoiding hundreds of small calls, and passes the actual frame comparison. V269's
profile and research artifacts remain reproducible.

## Full saved-ROM display check

An ordinary28400-frame cold boot replays the exact purchase/equip/controller/stylus
schedule. All2080 pixels of the130x16 occupied tooltip, including paper, corners,
blank cells and all223 black letter pixels, match at native precision. Both first
and final letters survive. The full original inventory icon is included in the
proof. The other73 comparable whole screenshots are identical; all changed pixels
are confined to the tooltip[94,208,224,224]. Native donor/font/palette dimensions
and all17 plaque assets are retained. This is targeted emulator verification,
not a complete playthrough or physical-device test.

## Registered candidate

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v270` |
| Candidate | `out/all_routes_combined_v270_candidate.nds` |
| ROM SHA256 | `a5af5d3940e434738fa034bac7862b768e55c7bbf41f0d15c80a9de2e90f1485` |
| Patch | `out/all_routes_combined_v270_candidate.xdelta` |
| Patch SHA256 | `c8999350d2afe83c00b05c5d7799cade807074a868d96b7eff2367b53362ed2b` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch input | `work/clean.nds` |
| Clean SHA256 | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Changed component versus V267 | ARM9 only |

Full V267 reproduces exactly through the shared builder. All467 inherited accepted
and experimental batches, required stages and previous changed records remain in
the neighboring manifest. Every story/COMMON file, artwork, ARM7 and overlay is
exactV267. Source locks and canonical baseline remain unchanged. The clean-input
patch reconstructs the complete candidate exactly. Ruff passes targeted files.
Experimental; explicit user cold-boot acceptance pending. Check title/New Game,
Rafael's established opening/town, Guild purchase, Y Equip, full item name and
paper edges on the user's emulator before acceptance.

## Newly observed FE continuation defect

The Rafael tutorial at frame22000 prints eck View on its second row. Stored
SC0_B43_R45 contains Deck View, FE remains the original selector, and its three
continuations carry one guard space. The modern native owned-pool/font draw
reproduces the defect: one-guard input has883 ink pixels; two-guard input has916.
The older flat-source harness rejects the current owned helper, so its historic
claims cannot approve current output without a new calibrated test.

An exact all-route inventory identifies325 ASCII FE records with fewer than two
continuation guards;61 cannot gain the required guards/initial padding within
their allocations. These are at-risk records, not325 individually proven live
failures. Preserve all controls, macros, wording, allocations and meaningful
indentation. The next repair should address the modal runtime guard contract and
prove complete letters, consistent margins, bounded buffers and fallback behavior;
do not duplicate a lost letter or silently expand fixed records.

Census: `work/analysis/equipment_start_town_v268/modal_guard_census.json`.
Original real purchase/equip run: `work/emulation_v193/equipment_start_town_v268`.
Latest exact display proof: `work/analysis/direct_equipment_v270/saved_live_proof.json`.
Verifier: `scripts/verify_direct_equipment_release_v270.py`.

All18 plaque/hint entries and Armor/Weapon variants remain incomplete as requested.
Occupied weapon/armor names, other conditions and parent contexts, four Online
source bodies, raw comic/native display, naming consistency and full final goal
verification remain open. Revisit older record-based checks at actual completion.
The graphics goal is active, not achieved or paused.
