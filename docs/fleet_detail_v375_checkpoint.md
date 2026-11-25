# Fleet detail and sort checkpoint V375

Status: experimental combined candidate. The full graphics goal remains active;
all18 plaques/hints and their remaining variants remain incomplete. Every22
historical audit requirement is retained. Low-resolution Online images remain
exempt. Canonical baseline is unchanged.

## Actual findings and fixes

An ordinary saved-game voyage followed by Info > Fleet Info exposed untranslated
`レベル` and `%s総帥（%s）` captions. The complete related lookup also exposed
`担　当`, `キャンセル` and the profession `征服者`.

Eight source-reviewed captions are now English: three numeric Level formats,
the sort Level label, Role, Cancel, the faction Leader/profession caption and
Conqueror. The Level formats preserve their integer and minimum-width contracts.
Role denotes the assigned duty. Leader distinguishes the faction head from an
individual fleet Admiral. Conqueror preserves the original profession meaning.
Existing Trader/Pirate/Soldier labels and all selector values remain unchanged.

The faction name remains complete in its existing green title. The portrait
line reads `Leader (Soldier)`, preserving the profession and leadership meaning.
Captain name, level values and other information retain their original rows.
The duplicate faction name formerly caused the combined caption to clip.

The actual four-column roster sort popup also clipped the final strokes of
Command, Finance and Observe. Its original36-pixel source cells and dimensions
are retained. A caller-specific painter uses five-pixel advance with the whole
original6x11 glyphs. All12 static labels now fit with exact full strokes and blank
cells. Inputs, palette, source points and non-ASCII/long-label fallback are preserved.

The older save's native full-name getter returned `Hodram Joachim Bergstrom`.
The player middle-name getter now displays the locked `Joakim` only when all three
fields match that known old default tuple. Other tuples and already-current names
use the original field pointer. Input fields and donor save files are untouched.
The surname getter is unchanged.

## Evidence and preserved failures

- V368's full combined caption clipped the profession; it is research only.
- V372 assumed the save stored first/middle/last. Actual getters prove the storage
  is first/last/middle: offsets20/31/42, with the middle virtual at148EBC. The
  corrected V374/V375 implementation uses that actual order. V372 is research
  only and receives no successful naming credit.
- Twenty-two full native caption rasters and15 original selector cases verify
  all four professions and numeric/lookup boundaries.
- Six native old-default/current/custom-name cases preserve fields, surrounding
  guards, condition flags and saved registers. All12 sort captions match full
  independent native font masks inside the original cells.
- Actual fleet masks verify the faction title, complete Leader label, both full
  `Hodram Joakim Bergstrom` names and both numeric Level captions. The complete
  name has281 ink pixels in each view. All12 actual sort labels pass full masks.
  Other pixels of the final fleet frame are unchanged from the parent context.
- Final registered V375 matches46 verified fleet frames,34 sort frames,23 normal
  New Game frames and30 ordinary Rafael book purchase/equip frames:133 total.
- Every470 inherited batch and every V366 native stage, including commodity and
  equipment-confirmation fixes, is retained. Only `/__arm9__.bin` changes from
  V366; all route/COMMON/HELP data, graphics, ARM7, overlays and other components
  are exact. Inherited code/payload, heap/arena bounds and palette/font data are
  preserved by source-locked stage checks. New code/data fit the previously
  declared ITCM allocation. No synthetic unlock or inventory changes are included.
- Integrated builder, targeted Ruff, saved-ROM/manifest checks and exact clean
  patch reconstruction pass. An automatic permission review timeout prevented
  one verifier creation; its authorized retry/recreation succeeded. No timeout
  was treated as a safety rejection or proof of a stopped emulator process.

These are targeted cold-boot emulator tests, not complete routes or hardware tests.
The older donor's historical progress is unknown. No weapon/armor acquisition,
new port or treasure discovery is credited. Native Conqueror/fallback and other
caption coverage does not establish every profession/context through gameplay.

## Remaining findings and scope

Native item types prove Snow-Silk Robe and Supreme Loupe are gifts, not armor or
weapons. All208 actor slot getters in the older V326 capture were empty. The
DS-specific purchase/search guide links are leads in
`work/analysis/equipment_availability_v367/availability_proof.json`; the current
ROM and actual gameplay remain authoritative for eligibility and acquisition.

Ordinary scurvy dialogue has complete first/final letters:166 and126 ink pixels.
It is a fixed COMMON warning, not proof that the separate shared26-condition
name table produced it. Its first line begins at x16 and its guarded continuation
at x22; this additional alignment variant remains open. Source message396 has a
valid full-width CP932 I, not a replacement-character corruption. The broader
legacy wording/formatting review remains separate and open.

Occupied weapon/armor, alternate plaque conditions, deeper Gallery/ending scenes,
retained environmental/legacy consumers and other historic requirements remain.
Revisit older record-based checks when the full goal is actually complete.

## Handoff

Candidate: `out/all_routes_combined_v375_candidate.nds`.
SHA-256: `b0dc3fe3796bbf79855aedc7541927f4ae3630645155e5f5065e26a56d5e1d83`.

Patch: `out/all_routes_combined_v375_candidate.xdelta`.
SHA-256: `9f596ecbd06e3292cd6e64211ece09a4fca7d5c926f38479d9b8cbddfc1b1d63`.
Patch input: `work/clean.nds`, SHA-256
`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Profile: `all-routes-unified-v375`. Accepted layers remain baked into the base;
all470 inherited experimental batches and all native stages are retained. Added
experimental stage: `translations/fleet_detail_release_v1.json`.
Complete identities/internal change records are in the neighboring manifest.

User cold-boot areas: title/New Game, established story/town, Items > Equip,
Info > Fleet Info, Sailors > Sort and the continuing Sailor Info/Assign Sailors
variants. Experimental; explicit user acceptance is required for canonical promotion.

Evidence: `work/analysis/fleet_release_v375/release_proof.json`,
`work/analysis/fleet_detail_v374/live_proof.json`, `shim_proof.json`, and
`work/analysis/fleet_detail_v370/native_proof.json`.
Verifiers: `scripts/verify_fleet_detail_native_v370.py`,
`scripts/verify_fleet_shims_v374.py`, `scripts/verify_fleet_live_v374.py`,
`scripts/verify_fleet_release_v375.py`.
