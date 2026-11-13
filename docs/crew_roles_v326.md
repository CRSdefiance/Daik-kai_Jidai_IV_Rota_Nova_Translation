# Shared crew-role localization V325/V326

## Actual defect and table-wide correction

An isolated current-ROM cold boot from an existing desktop cartridge save reached
Stockholm's Hodram fleet. Gerhard's Sailor Info screen showed untranslated **副官**.
The native role selector at `02086314` uses a 16-entry Japanese table. It returns
the address of the selected pointer field, or zero for an invalid index.

The item screens already have a complete reviewed English role table in the
owned, copied runtime pool. V326 redirects the selector's single table-address
literal at ARM9 offset `0x86334`, from `021197A0` to `023889C8`.

This fixes every valid role selected through that shared function. Original
logic, bounds, index order and fallback behavior are unchanged. The original
Japanese table/strings, existing English text, pool size, startup copy, cache
maintenance, fonts and artwork are all preserved. No new allocation or helper
is introduced. It does not claim that every unrelated literal/consumer is English.

| Index | Source Japanese | Complete English |
|---|---|---|
|0|艦長|Captain|
|1|副官|First Mate|
|2|参謀|Strategist|
|3|主計長|Purser|
|4|測量士|Surveyor|
|5|操帆手|Sail Handler|
|6|操舵手|Helmsman|
|7|見張り|Lookout|
|8|斬込隊長|Boarding Leader|
|9|砲撃手|Gunner|
|10|宣教師|Missionary|
|11|船医|Surgeon|
|12|料理長|Chief Cook|
|13|船大工|Shipwright|
|14|飼育員|Animal Keeper|
|15|甲板要員|Deckhand|

These retain the existing item-role dictionary and its source meanings. Existing
odd-length labels have a trailing blank cell to preserve their stored pair phase;
no word is shortened. The blank cells and every visible letter are verified.

## Native and actual evidence

- 259 native selector inputs pass: all byte values, negative and signed extremes.
  Valid indices select the complete existing English fields; invalid indices
  retain the original zero fallback. Native returns/registers/stack are checked.
- All 16 complete labels render in both 4-bit and 16-bit modes: 32 exact rasters,
  including leading/internal/trailing letters and blank cells.
- The normal buffer helper inherited by the current ROM is validated byte for
  byte before execution. An initial historical-harness rejection of this helper
  was resolved in the dedicated harness with an optional explicit buffered-text
  contract; no production renderer was altered to pass the check.
- A 17,600-frame saved-game cold boot repeats the ordinary Stockholm navigation.
  Gerhard displays the complete First Mate label and complete name. Every other
  pixel of the same Sailor Info screen matches the parent capture exactly.
- Twenty whole plaque instances across Hodram and Gerhard match the source-locked
  integrated assets and palette. All 18 ongoing entries remain incomplete.
- A separate fresh 31,200-frame New Game run covers title, character selection,
  opening, town and sailing. Four title/character/opening/recruitment frames are
  exact V324; six retained Rotate/Sails/Inspect masks pass.

The original role logic and all 470 inherited batches remain intact. Complete
V324 reproduces byte for byte through the updated builder. Only the four-byte
table literal changes versus V324. The clean-input patch reconstructs V326
exactly. Manifest/inheritance, source-lock, native selector/raster, actual masks/
frames and focused Ruff pass. Both emulator processes ended normally.

## Save provenance and further navigation

Read-only inspection found 162 desktop DSV files, six distinct hashes and two
files with a DK4R game header. The selected older save is
`../desmume-0.9.13-win64/Battery/extras_options_sound_common_v6_candidate.dsv`,
SHA256 `28ff98d46e3b2ce1b1d9525059988f18a4ddf0d5bedac9140a183285493fdc2e`.
Each run starts from a byte-exact isolated copy; the original file stays unchanged.
Its earlier gameplay provenance is unknown. No historical progression, legitimate
unlock, completed route or hardware-device claim is made from its contents.
No savestate, edited save, unlock patch or live RAM injection is used.

The save loads a level-15 Hodram fleet in Stockholm. Observed Guild stock is
Snow-Silk Robe, Supreme Loupe and a map. The middle icon was investigated as a
possible weapon, but it is a magnifying glass and its category is Gift. The
ordinary replay purchases the Supreme Loupe in its isolated copy; this earns
no occupied weapon/armor evidence. Gerhard's displayed Survey is 124, above
the previously observed 120 Survey requirement. Assignment and successful
Auto Move still need testing; eligibility is not declared achieved here.

The observed Guild clue wraps crystal c / ontaining and ea / ts across lines.
Retain this concrete legacy word-wrap issue for the older record-based checks;
this role-table correction does not fix or certify that prose.

## Registered experimental build

| Item | Identity |
|---|---|
| ROM | `out/all_routes_combined_v326_candidate.nds` |
| ROM SHA256 | `fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1` |
| Patch | `out/all_routes_combined_v326_candidate.xdelta` |
| Patch SHA256 | `acd56ccb8a9ddc4eded5c3cf96e15e1fcc3be8fd48d47fed0d42676a877c4299` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Profile | `all-routes-unified-v326` |
| New stage | `translations/crew_role_labels_release_v1.json` |
| New changed internal file versus V324 | `/__arm9__.bin`, one table-address literal |
| Manifest | `out/all_routes_combined_v326_candidate.manifest.json` |

All 41 inherited changed paths against the canonical base are enumerated in the
manifest. No path is added. Canonical unchanged; experimental and user acceptance
pending. On the user's emulator check title/New Game or Continue, the established
opening/town, and Sailor Info for assigned crew: Gerhard should show First Mate
with the complete leading F and final e. Wider role contexts remain to audit.

## Goal and evidence

Both graphics audits and progress documents record this checkpoint. All 18 plaque/
hint entries and Armor/Weapon variants remain incomplete. Actual occupied weapon/
armor, alternate conditions, final FLS GPU composition, legacy viewers and wider
contexts remain open. Low resolution Online images stay exempt. The graphics goal
remains active; revisit older record-based checks at actual completion.

Evidence: `work/analysis/crew_roles_v326/native_proof.json`, `release_proof.json`,
parent reproduction and exact reconstruction; the V325 source discovery capture
and both V326 capture reports under `work/emulation_v193/`.
Reproduce verification with `scripts/prepare_crew_roles_v326.py` and
`scripts/verify_crew_roles_v326.py --live`.
