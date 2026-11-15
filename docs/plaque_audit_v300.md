# Current plaque audit V300

V300 is an audit checkpoint on the unchanged V299 ROM, not a new ROM candidate.
The user asked that all 17 plaques and the Equipped Items hint remain in the
ongoing audit. All 18 entries and Armor/Weapon variants retain completion false.

## Current source and wording

Candidate: `out/all_routes_combined_v299_candidate.nds`, SHA256
`9f551e849f7cb8fbabee2bb4e9586fb527789c4b8a0ed97c084a21adaa49768f`.
Its registered profile, exact patch and complete naming/art integration remain
those documented in [V299 release evidence](reviewed_name_release_v299.md).

The original-source review in
[crew/sailor wording](crew_sailor_ui_translation_v247.md) still applies. Fleet Crew
is the total fleet count, Unassigned the available pool and Endurance the sailing
duration explicitly displayed in days. Quarters represents marine quarters,
not a marine head count. Cannon is the cannon type, with the actual cannon name
to its right. Fore/Aft represents fore-and-aft performance, including more than
lateen sails; Square is square-sail performance. Health is physical condition;
Mood is current mental condition, while Spirit is the permanent mental attribute.
Other stat/skill labels retain their source-backed meanings. No new shortening,
name policy or artwork edit is introduced.

## Fresh actual screens and complete pixels

Two production V299 cold boots use ordinary input, no loaded states or live RAM
injection. Both processes exited successfully and all captures/hash/error checks
pass. The crew run stops at 11,200 frames and the person run at 14,400 frames.

Assign Sailors is verified with crew16/unassigned0, Lo crew0/unassigned16 and Hi
crew16/unassigned0. Need9 and Max24 remain visible; Hi is constrained by the actual
available crew pool. Lo permits zero allocation, including below the sailing
requirement. This does not claim every possible total, fleet or numeric state.

Sailor Info is visited for Lil, Camille, Emilio and Fernando. All ten plaques on
each character and all seven plaques in each crew state match complete source
PXL pixels: **61 complete plaque instances**. An independent decode of every
untrimmed native font glyph also matches all plaque ink. The five-pixel advance
removes only the blank sixth column, with no missing first/interior/final ink.
Entire paper textures and bevels match the inherited port-paper style.

All 40 complete lower skill/value lines pass native font masks, including every
blank and digit. Physical three-digit values such as Command103, Finance104,
Observe101 and Vigor102 are complete and remain inside their native fields.
Healthy and Normal display complete font masks in each of four current contexts.

Equipped Items is verified at three different selections/positions. Armor and
Weapon are also verified with empty slots: five complete hint surfaces in total.
Every paper pixel, foreground glyph, border and bound passes. The four source
gender cells match all 256 pixels in their actual palette bank48, including Lil's
female symbol and the three male symbols.

Lil Argot, Camille Marinus Overijssel, Emilio Ferog and Fernando Dias have complete
actual name-caption foreground masks. The latter two use the established protected
CP932 full-width F, verified independently from the native Kanji font as well as
the ASCII cells. The initial verifier assumed Ferox and ordinary ASCII F; it was
corrected to the actual native fields. Original Japanese surname `フェローグ`
supports the existing Ferog spelling. No game name was changed to satisfy a test.

## Current native scope

The current V299 native selectors pass all 256 byte values for each condition
group, matching clean pointers, fallbacks, stack, registers and actor memory:
512 current cases. All 13 condition captions execute their complete native
48x16 font raster, with first/final letters, pixels and bounds exact.

All ten current skill getters and 50 original formatter cases at0/9/97/107/500
pass with every seven-label/three-value cell and output guard intact. All235 paper
widths from10 to244 execute on both native framebuffers:470 complete pixel cases.
The current fresh ITCM export supplies the original fill for the three existing
hint widths. All bytes outside each rectangle and framebuffer guards remain exact.
There is no GPU draw instruction bridge in these controlled paper cases. Current
inherited helper/pool bytes remain identical to V270. Ruff passes.

These are controlled native condition/paper inputs and targeted actual screens,
not proof that all alternate conditions or occupied items were played.

## Remaining audit

Keep all 18 plaques/hints in the ongoing audit. Occupied Armor/Weapon name geometry,
actual alternate Health/Mood states (including Excited), other route/character/
fleet contexts and user review remain open. The former Rafael-name mismatch is
resolved by V299; this audit does not revive that stale issue. Broader graphics
consumers, Gallery/deep scenes and the full graphics goal remain incomplete.
Low-resolution Online promotional images remain exempt by user instruction.

The current tests find no new defect requiring a ROM change. V299 remains the
latest experimental candidate. At actual full goal completion, revisit older
record-based checks as requested, including encoded metadata and mixed font
assumptions.

Evidence: `work/analysis/plaque_audit_v300/native_proof.json`, `live_proof.json`,
`current_plaque_review.png`, logs, and the two fresh
`work/emulation_v193/plaque_audit_v300_*` capture reports/PNG/native exports.
