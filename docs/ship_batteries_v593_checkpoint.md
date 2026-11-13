# V592-V593: distinguish gun batteries from cannon counts

## Original meaning and observed context

V591 retained a Ship Info plaque **Guns** for original **武装砲台**. The original
Help page129 describes the ship's gun positions, where an assigned officer
becomes a Gunner. Existing localized Help uses **Gun Batteries**. The Deck room
selector used **Gun Deck**, and its marine room **海兵詰所** still used **Marines**.

An ordinary copied-save V591 run reaches Deck View through Port > Depart > Deck
View. The empty gun position displays Gun Deck, Aim and requirement90; the marine
room displays Marines, Swords and requirement90. Complete original-font masks at
native origin72,24 prove both observed labels,103 and94 ink pixels respectively.
The original Japanese of both12-byte ARM9 slots is also verified against clean
source. Neither term is inferred only from a thumbnail or an old English name.

The consistent compact terms are now:

| Source | Context | English |
| --- | --- | --- |
|武装砲台|Individual assignable Deck position|Battery|
|武装砲台|Ship Info count of those positions|Batteries|
|海兵詰所|Deck room and existing Ship Info/Assign Sailors labels|Quarters|

This distinguishes batteries from individual cannons and preserves the room and
officer-assignment meaning. Existing Help remains Gun Batteries/Marine Barracks;
its longer explanations are not rewritten. Gunner eligibility, firing behavior,
counts, equipment, room types and officer assignments do not change.

The discovery navigation briefly visits other menus while locating Deck View;
it does not verify shipyard remodeling. The displayed ship, copied save and
ordinary Deck selections are the context actually credited.

## Exact changes and integration

Only two internal files change from V591:

- `/_pxl/shipinfo.pxl`: **Guns → Batteries**,139 pixel indices, all in old/new
  letter masks. The existing source-grain face must match in full before editing.
  Every other grain pixel, original outer frame, palette, header and dimension
  remains exact. The new word retains the original game font and fits the64x16
  face `[132,104,196,120]` without scaling.
- `/__arm9__.bin`:15 differing bytes within two existing12-byte text-data slots:
  original address0212FFFC **Marines → Quarters**, and02130008 **Gun Deck → Battery**.
  Slots remain null terminated and padded, with the same size. All other ARM9
  bytes, fonts, code, pointers, section extents and heap/cache setup remain exact.

The V591 source-grain painter is generalized for reuse; its existing Quarters
output is reproduced byte-exact before the new profile is registered. The old
Quarters stage remains present. No accepted batch or previous artifact changes.
The new registered terminal stage is `ship_battery_labels`, config
`translations/ship_battery_labels_v1.json`, module
`dk4tool/patch/ship_battery_labels.py`.

## Registered candidate and exact patch

- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Comparison parent: `out/all_routes_combined_v591_candidate.nds`, SHA256
  `7f2d10824e18d276adb23b01be48dac2d27adc2c4ec8ec16bb39a93a90dc3d73`.
- Experimental candidate: `out/all_routes_combined_v593_candidate.nds`, SHA256
  `d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642`.
- Profile: `all-routes-unified-v593`, retaining470 batches and114 accepted layers.
- Manifest: `out/all_routes_combined_v593_candidate.manifest.json`.
- Patch: `out/all_routes_combined_v593_candidate.xdelta`, SHA256
  `e6e1097e9caa7577a4c51d9bcc175274eb68e4f8041d86acd05d8ba1f4ad52c7`.
- Patch input: `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The ROM, manifest and patch physically reside in
`E:/Rota Nova translations/Generated/out/`. The registered integrated builder
rebuilds from the canonical base. The patch reconstructs the entire exact V593
ROM. Canonical promotion and human acceptance are not claimed.

## Native tests and complete backgrounds

All successful runs cold boot without a savestate, use the same unchanged copied
source save as V591 and finish with exit0. Its original SHA256 remains
`958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb`.
The final candidate runs use ordinary controls only, without inventory, location,
condition, unlock, assignment or framebuffer fixtures. No gameplay Save is accepted.

### Deck: source, empty-label control and final candidate

The original V591 discovery run ends at6920 frames. A separate, explicitly named
research clone changes only the first byte of each of the two room labels to0.
Its fixture manifest proves those two changes and every other internal file exact.
It supplies actual native background pixels; no stored screenshot or bitmap is
inserted into the framebuffer. This empty-heading control is not a playable
release or an ordinary guide candidate.

V593 and the empty-label clone replay the exact original schedule. Eighteen
complete three-way frame cases verify both source and final native compositions
against those background pixels: **3,538,944 RGB pixel positions**. Eight actual
changed heading appearances pass, four Battery and four Quarters:

| Word | Native full bounds | Complete ink per appearance |
| --- | --- | ---: |
|Battery|[72,24,114,35]|89|
|Quarters|[72,24,120,35]|100|

Every old/new glyph and every blank cell fits, including both word ends. Four
first/final-letter erasure cases are rejected by the same whole-composite
comparator. All pixels outside the intended heading glyphs remain exact. Native
captured text-slot bytes also match the actual candidate.

A broad automatic mask locator was stopped after verifying its owned process
identity because it was unnecessarily costly. A five-pixel-advance hypothesis
also failed. Measured fixed-origin six-pixel original-font masks match exactly;
the failed diagnostics earn no passing coverage and imply no font defect.

### Ship Info: final Batteries plaque

The ordinary sailing inspection schedule from V591 runs again on V593. Twelve
complete control/final frame pairs check **1,179,648 native five-bit color pixel
positions**. Only139 expected plaque letter positions differ in the three Ship
Info frames; all other pixels and the other nine frames are exact. Each complete
1,024-pixel face matches the independently reconstructed final atlas, with the
whole Batteries word present.

Actual original view0218A4D0 has owner02313C90, source `[0,0,256,192]` and resolves
through complete original020D4170 to resident02351210. All resident shipinfo bytes
match the candidate resource. No supplied header or filesystem bridge is used.
The inherited Quarters plaque and normal Back/Assign Sailors output stay exact.

All three final screens were visually reviewed at native resolution. Three
unmodified guide candidates are saved on E with exact ROM/report/input/save
provenance and publication approval false. Source/control and blank research
screens retain separate audit/test labels.

## Artifacts and remaining scope

- `scripts/prepare_ship_batteries_v593.py`, build log and source/current/proposed
  comparison sheet under `work/analysis/ship_batteries_v593/`.
- `scripts/verify_ship_batteries_v593.py`, `release_proof.json` and exact
  reconstructed ROM in that same E-backed directory.
- `scripts/record_ship_batteries_v593.py` records preservation, archive receipts
  and the existing three graphics audits/five progress documents.
- Source discovery: E under `Generated/work/emulation_v193/ship_batteries_v592`.
- Final runs: E under `Generated/work/emulation_v193/ship_batteries_v593_deck_actual`
  and `ship_batteries_v593_ships_actual`.
- Guide candidates: `Screenshots/Guide candidates/V593 Ship room terms` on E.
- Comparisons: `Screenshots/Audit comparisons/V593 Ship room terms` on E.
- Research controls: `Screenshots/Test fixtures/V593 Empty room labels` on E.

This closes the specific marine-room/gun-position terminology concern retained
in V556/V557. It does not close the global material audit, every ship/loadout,
unobserved labels, miniature/Confirm parents, Admiral wording, legacy/comic/
village/movie contexts, full routes or hardware verification. All921 graphics
format/palette/extent entries and57 embedded blocks carry forward through exact
file equality and the checked single atlas. All18 original plaque/hint entries
remain incomplete and all22 historical requirements retain their exact scope.
The graphics goal remains active; older record-based checks remain a follow-up
at its full completion.
