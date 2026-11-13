# Auto Move confirmation V315/V316

## Ordinary discovery and navigation

A fresh V309 cold boot loads the genuine Gallery-test battery save through
Continue. Port > Depart > Auto Move opens the destination map. Ceuta can be
selected using ordinary stylus input and the native confirmation displays
untranslated自動移動. Source capture: frame6000 in
`work/emulation_v193/ordinary_voyage_v315/`.

Confirming reports **No surveyor aboard.** Deck View shows Survey / Skill: Survey /
Need120 and **No eligible crew.** Lookout, Mast, Survey and Helm room views and
the navigator roster are traversed with normal inputs. No role assignment is
committed and no voyage or weapon/armor purchase is achieved. The discovery run
ends normally at17,600 frames; its report and all input events are retained.
Sextant eligibility/stat effects have not been established by this run.

## Source-safe caption fix

自動移動 means automatic movement. **Auto Move** matches the already translated
port command and keeps the complete meaning. Original caption is at ARM9 offset
14DD10, in a12-byte allocation. Its sole descriptor pointer at119DA4 remains
unchanged. Native descriptor references are observed at02096610/02099628.

The English9-character label plus NUL fits the original slot. Source/canonical/
current bytes and sole pointer ownership are locked. No caller, menu descriptor,
gate, actor control, font, palette or navigation behavior changes.

Complete native raster checks pass. A fresh6,000-frame V316 cold boot replays
the exact saved-game inputs to the same Ceuta confirmation. All123 first/internal/
final lettering pixels match at(101,282), six-pixel advance, colour(8,8,8).
Every earlier comparable whole frame is exact. The999 changed pixels of the
confirmation frame stay within the native popup, including its resized border.
The original menu sizes itself for the full English caption.

The first comparison bound started one row below the observed border; its failed
assertion is a verifier-bound error. The corrected bound includes the actual
popup border and every changed pixel. No image/ROM was altered to satisfy it.

## Registered experimental handoff

| Item | Identity |
|---|---|
| Candidate | `out/all_routes_combined_v316_candidate.nds` |
| ROM SHA256 | `bdc9e7e60d2f706b2b20f194901a2b382cc0de2534df3660ea5deb65038ab495` |
| Patch | `out/all_routes_combined_v316_candidate.xdelta` |
| Patch SHA256 | `ef67a8f9dc6dcb34f0526e0bf56c3c930348af492bc9f112c5942945ff6412a3` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Profile | `all-routes-unified-v316` |
| Stack |All470 inherited batches/native stages; accepted layers retained through canonical base|
| New experimental stage |`translations/auto_move_caption_release_v1.json`|
| New changed internal file versus V309 |`/__arm9__.bin`, original12-byte label only|
| Full manifest |`out/all_routes_combined_v316_candidate.manifest.json`|

All other files/components, graphics, route/COMMON/HELP data, ARM7 and overlays
match V309. All accepted and experimental inherited batches and changed records
remain in the manifest. Against the canonical base, inherited changed files
are the same41 paths documented for [V309](sailing_condition_names_v309.md);
the manifest enumerates them explicitly. No accepted layer is removed or promoted.

Full V309 reproduces byte-for-byte before and after the optional builder stage.
The clean-input patch reconstructs V316 exactly. Source/native raster, release/
inheritance/patch, actual cold-boot/glyph/frame checks and Ruff pass.

Experimental; canonical unchanged and user cold-boot acceptance pending.
On the user's emulator, check title/Continue or New Game, the established opening/
town, and Port > Auto Move > destination confirmation. The confirmation can be
reviewed even when the crew does not qualify to sail automatically.

## Remaining scope

Other Auto Move literals/contexts remain Japanese in the ARM9 and require their
own consumer review; this checkpoint does not claim all navigation UI is complete.
The inline footer table, moving/stopped captions and ineligible-action message
are recorded leads. Do not substitute the fixed-slot approach for an unmapped
packed footer or assume its font/renderer matches this menu.

All18 plaques/hints and Armor/Weapon variants remain incomplete. Continue ordinary
equipment/navigation, alternate conditions and legacy/native/GPU contexts. Low
resolution Online images remain exempt. The full graphics goal remains active;
revisit older record-based checks at actual completion.

Evidence: `work/analysis/auto_move_caption_v316/native_proof.json`,
`release_proof.json`, `replay_inputs.json`, the V309 reproductions and exact
reconstructed ROM, plus `work/emulation_v193/auto_move_caption_v316/capture_report.json`.
