# V622/V623: original Spoils and Distributed Goods contexts

Previous goal turn: progress, with V621's shared bitmap-origin correction and a
completed boarding-duel replay. This turn follows its post-battle Cargo Setup,
verifies Spoils in the actual event, traces the separate Square distribution path,
and localizes its previously hidden Japanese action. The graphics goal stays
active. All18 original plaque/hint entries remain incomplete; all22 historical
requirements retain their original scope. V622 is a research checkpoint, not a
new playable ROM.

## Post-battle Spoils through original controls

Unchanged V621 replays the pinned Copenhagen donor and the same single disclosed
ship-recovery/proximity fixture. Original combat, capture and victory handling
lead to Cargo Setup. At24800 its original field+10 is3, and the copied header
view references owner02313A4C, initialized as `_pxl/senrihin.pxl`. Original
getter020D4170 resolves a whole resident file identical to the production art.
Nine captured states independently verify this owner, file and mode.

The initial Armor tooltip covers301 banner pixels, all within source x16..49,
y5..15. Normal Down moves to an empty slot and reveals the entire Spoils header.
Five states match every4096 header pixel, totaling20480 pixels: complete Spoils
lettering, original border/palette and current repaired wood. This is actual
post-battle reachability, unlike V567's supplied header-choice instruction.
It does not newly prove the historical inferred texture beneath erased source
glyphs; that material/user-review scope remains recorded.

Normal Y/Unload empties both original Iron slots from the active ship's temporary
cargo list. Normal selection/A reloads one slot. Finish/X opens the complete
two-line warning, B cancels and retains the selected cargo state, and a subsequent
Finish/Right/Yes exits. Three warning states pass complete original-font masks.
Original loot/victory/resource flags and inventory are not injected. These are
original controls after an authorized proximity fixture, not an earned voyage
or full campaign playthrough.

Proof: `work/analysis/post_battle_cargo_v622/release_proof.json`.
Verifier: `scripts/verify_post_battle_cargo_v622.py`.

## Distributed Goods is the Square's free-sample action

Original0205E3A8 enables the second Plaza action only if the main fleet has goods
and original role10 lookup020825E4 returns an assigned Missionary. Role10 maps
through02007B60 to Chapel type18. The Istanbul donor already has two Iron cargo
slots, but its role getter returns208 (none), so earlier Square visits showed
only Trends. This is why those captures missed the second label.

The original table at02143F78 has two exclusively owned text pointers:
Trends at02143E98 and the still-Japanese `交易品の配布` at02143EA4. The second
action reaches0205ED34, then020832E0 constructs Cargo Setup mode2. Its header
is owner023139E8, `_pxl/haifuhin.pxl`, meaning goods designated for distribution.

An exploratory ordinary V621 run visits the Square, Market and Palace, obtains
the normal trade contract, and starts the original Angelo Port event. It does
not establish Missionary eligibility or the distribution menu. Its full report
and snapshots are retained as diagnostic observations, not display clearance.

## Bounded Missionary test fixture

Under the user's standing permission for testing cheats, the final old/new
comparison uses one explicit three-byte fixture on isolated Istanbul copies:

1. Vestaros room18: original unused type24 becomes Chapel type18.
2. Clear Manuel23 from his former Survey room3 to none208.
3. Assign Manuel23 to the formerly empty room18.

The code pins V621/V623, original getters and room layout, actual Vestaros and
Manuel identities, original empty target, old assignment and two existing cargo
slots. Original role lookup then returns Manuel23. No attributes, qualifications,
health, goods, money, town/location, menu-enable byte or result flag changes.
It does not claim a legitimate refit, earned qualifications or normal staffing.
Five negative controls reject wrong code, size, false/integer requests and a
second assignment. Every live write is limited to the declared three bytes and
the entire4MiB after-state is checked. No source battery is modified.

The fixture module is `scripts/native_missionary_fixture_v623.py`; the harness
requires `--allow-missionary-fixtures` and explicit `missionary_fixture:true`.
Source proofs and rejected controls are in `work/analysis/plaza_distribution_v623`.

## Complete English label without storage growth

Source `交易品の配布` means distributing trade goods; the following original
confirmation explicitly says they are free samples. **Distribute Goods** is the
complete verb-object action label. The separate **Distributed Goods** artwork
continues to name the goods selected for this action. Trends is unchanged.

V623 repacks these two exclusively owned strings into their existing28-byte
source span143E98..143EB4 and updates only the second table pointer143F88.
Both complete English strings use24 bytes. All unaligned main/autoload/overlay
references to the old span are exactly the two original table entries. RTTI,
menu flags, original availability rules, all code, other text, section extents,
staged pool, cache/startup wrappers and arena bounds remain exact V621.

Two native full256x16 font checks establish complete six-pixel English cells and
image guards. Actual old/new cold boots then show the Japanese control versus
the full English label, in both selection states. The original row draw routine
02052FD0 submits source96x12 views at[0,0] and[0,12] to native destinations[80,80]
and[80,100]. Independent complete font masks match both source views and actual
screen pixels, including the initial D, final s and every blank cell.

The larger shared256x36 font buffer contains stale text outside these views.
An initial zero-filled whole-buffer expectation was too broad; the original
native crop requests establish the actual owned96x12 regions. No stale pixels
outside them are submitted, cleared or credited as translated display. The
renderer harness captures submission arguments; it does not emulate the GPU.
Real DeSmuME framebuffer pixels independently prove the visible result.

## Actual mode2 header and distribution behavior

Normal Down/A selects the action in both builds. Right/Yes confirms free samples.
Original Cargo Setup then selects mode2 and loads the actual Distributed Goods
resource. Three complete4096-pixel banners match, including all lettering, wood,
borders and palette. No header-choice or artwork substitution is applied.

Normal Y/Unload selects the two existing Iron cargo slots for distribution, and
Finish/X runs the original action. Complete original confirmations and the
two-line free-sample announcement pass four line masks. The original cargo query
changes from2 to0. The subsequent Square menu again shows only Trends because
no goods remain. Ten complete post-menu frames match V621's original behavior
exactly. The fixture supplies the missing role/room, not goods or an outcome.

Nineteen ordinary no-save/no-fixture New Game/Market frames match V621 exactly.
The full470-batch/114-accepted-layer build and all builder checks pass. Only ARM9
changes versus V621; all artwork, COMMON, routes and other components stay exact.
All660 PXL/261 FLS preservation checks and57 embedded extents pass. The clean-ROM
patch reconstructs every candidate byte. Targeted Ruff passes. A first build
stopped on tuple/list proof serialization before saving a ROM; the final build
normalizes proof owners and succeeds.

## Artifacts and next work

- Experimental candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v623_candidate.nds`.
- ROM SHA256: `4c7f8098d2e793514204fe78b54f922cc190daf39502811c51ec43751719b6d9`.
- ARM9 SHA256: `9a05ef9a25367d53dc7affa1c24e70b84fa9123388701adefcf94e0d21add280`.
- Patch SHA256: `06d0afeeb13936a3da7acabdc7a835aefa7d7d9e5a71b773a6ec02feb6d0e499`.
- Profile: `all-routes-unified-v623`, complete V621 plus `plaza_distribution_label`.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Primary proof/verifier: `work/analysis/plaza_distribution_v623/release_proof.json`,
  `scripts/verify_plaza_distribution_v623.py`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V623 Spoils and distribution`.
- Complete runs on E: `post_battle_cargo_v622_actual`,
  `plaza_distribution_v622_actual` (exploratory), `distribution_menu_v621_fixture`,
  `distribution_menu_v623_fixture`, `plaza_distribution_v623_market`.

Reproduce the final menu runs using the pinned Istanbul donor and first four
original inputs in `work/analysis/post_battle_cargo_v622/istanbul_prefix.json`,
pause3200, the opt-in fixture flag, and the archived navigation journals through
their normal stops at8001. Use separate fresh output folders; never load a
savestate. The journals alone are input records; terminal capture reports and
hashed images/RAM provide execution evidence. The final dialogue/selection
states, default source saves and canonical parent are unchanged.

The ordinary contexts of these two wooden headers are now verified within the
disclosed fixtures. Confirm and the five miniature captions, eight village cards,
remaining legacy/comic/logo/movie/material contexts and broader gameplay remain
open. No global non-use, route completion or hardware claim follows. All18 original
plaque/hint entries remain incomplete; latest-verified/canonical pointers stay
unchanged. The four low-resolution Online exemptions and preserved brown marks
remain in force. Revisit older record-based checks at actual full-goal completion.
