# V624: hidden Tavern scheme menus

Previous goal turn was a status response, with no project change. This turn
revalidated the live V624 research process, continued its actual handle, and
completed five menu translations. The graphics goal remains active. V624 is an
experimental cumulative candidate; its related dialogue is not fully verified.

## Source and complete English labels

The main Tavern table02118BA4 contains a fourth action, 策謀の立案, omitted from
earlier screenshots because original eligibility rules disabled it. Its submenu
is the four-record table02118B64. These are separate from Guild diplomacy.

| Japanese | English | Original pointer field |
|---|---|---|
| 策謀の立案 | Schemes | 02118BD4 |
| 艦隊誘導 | Lure Fleet | 02118B64 |
| 偽文書制作 | Forge Papers | 02118B74 |
| 悪い噂 | Bad Rumors | 02118B84 |
| 買収 | Bribe | 02118B94 |

Schemes names the action category. Forge Papers means producing forged documents;
Bad Rumors retains the malicious sense and distinguishes ordinary tavern gossip.
Bribe does not invent a crew or official target. Full labels fit without an
abbreviation or pool growth.

`dk4tool/patch/tavern_scheme_labels.py` checks the complete V623 ARM9 and clean
Japanese strings, then repacks three source-owned allocations:143B3C..143B44,
143B54..143B5C,143B6C..143B90. All unaligned main/autoload/overlay references into
those spans are exactly the five original menu pointers. Source RTTI, nearby
interjections, availability flags, every code section, staged payload, startup,
arena boundaries, other strings and all other files are retained exactly.

The source-reviewed text is tracked in
`translations/tavern_scheme_labels_review_v1.json`; the final source/native fit
proof is `translations/tavern_scheme_labels_v1.json`. The builder requires the
entire V623 stack before applying the new stage. Five independent256x16 native
font canvases and guards pass before the formatting gates are finalized.

## Eligibility and disclosed isolated fixture

Original020567CC requires a Strategist, at least1000 gold, an eligible opposing
faction, a date/state-dependent threshold below Speech, and a final source status
check. Original020571E0 separately uses the opposing-faction count and Strategist
skill thresholds150/200 for the submenu. A room assignment alone leaves the main
action hidden in this donor: original Speech132 versus threshold463.

The bounded opt-in expert fixture uses isolated copies of the pinned Istanbul
donor, SHA256d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132:

- Change one empty Vestaros room from unused24 to the source Strategist type19;
  clear Gerhard16 from room21 and assign him to that previously empty room18.
- Change Gerhard's one experience word11209 to250000. Original getters report
  combined level111, scheme skill206 and Speech201. The other experience word,
  attributes, health and inventory are exact.
- Advance the calendar word26877 to27021,144 source ticks/three days. Original
  zero-based date decoder changes[6,13,45] to[6,16,45]; the visible date becomes
  July17. The unmodified main availability calculation then gives threshold4.

Only three assignment bytes, one experience word and one calendar word are owned.
The harness validates the entire4MiB after-state. Five negative controls reject
wrong code, RAM size, false/integer requests and an existing assignment. Both
final cold boots use exactly the same fixture and input journal. These are
authorized testing cheats; earned experience, refit, qualification, assignment,
elapsed travel or campaign progress is not claimed. Funds, cargo, opponents,
menu-enable flags, artwork, code and result flags are not injected.

## Actual native menu display

Normal Tavern/Schemes controls reach the four-command submenu. All four selection
states of both menus are captured, producing32 complete text masks. The original
CDataMenu rows bind through their resident containing-menu pointer and source
vtable; stale unbound heap objects are excluded before replay. Original02052FD0
submits views from image022BD79C through01FF92D8. The first three source origins
are[0,0],[0,12],[0,24], and the fourth is[120,0]. Whole source views are84x12 for
the main menu and72x12 for the submenu; the latter fits all12 Forge Papers cells.
Destinations are[86,60+20i] and[92,60+20i], on the lower screen.

Independent game-font masks verify every glyph and blank cell in all32 source
views and corresponding real DeSmuME framebuffer crops. Initial and final letters
pass erasure controls. Source selection-background painting is outside the
native text submission contract; real framebuffer evidence covers visible text
in every selection state. Pixels outside submitted views are not assumed clear.

The old/new runs stop normally at9201. Twelve frames outside changed menus match
V623 completely. Bribe reaches its original faction-choice menu; B returns to the
Tavern menu. Nineteen ordinary no-save/no-fixture New Game/Market frames also
match V623. All470 batches/114 accepted layers,921 PXL/FLS format/palette/extents,
57 embedded extents and exact clean-ROM patch reconstruction pass. Only ARM9
changes; all artwork, COMMON, route files and other components are exact V623.

## New defects remain open

The actual command entry exposes two older problems, reproduced unchanged in the
V623 control. Neither is cleared by the menu-label pass:

1. At6000, COMMON_MESSAGE_909 splits `confuse` and `use` across lines. The existing
   Tavern portrait word wrapper covers820..873, excluding this later scheme
   family. Extend source-bound coverage and verify the actual complete paragraph,
   rather than insert manual line breaks or shorten the wording to fit.
2. At8000, the Bribe confirmation still expands Japanese 買収 from a separate
   general scheme-name table. Fields0214C600/604/608/60C are the Lure/Forge/Rumor/
   Bribe names used beyond the menu. Source/runtime proof and complete English
   substitutions are still required, followed by all four command entry/cancel
   contexts and any newly exposed labels. No all-command outcome pass is claimed.

An exploratory basic-assignment run ended normally at4801; it did not reveal the
Schemes menu and receives no menu-display credit. The final identical journals
also preserve one rejected export request with an invalid default duration; it
applied nothing. The subsequent valid export and terminal reports provide the
actual execution evidence.

## Artifacts and remaining scope

- ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v624_candidate.nds`.
- SHA256: `4eaf22d1f69f6eb49f624a557698a281bd6eedb8b396023007aebcdda35bee63`.
- ARM9 SHA256: `e7c4e62f4fe5b621b1d4bed2123ab26d033698237e47b4b425e6fc9176a5b5a0`.
- Profile: `all-routes-unified-v624`; complete470-batch/114-accepted-layer V623 stack
  plus `tavern_scheme_labels`.
- Patch: adjacent `.xdelta`; exact whole-byte reconstruction recorded in
  `work/analysis/tavern_schemes_v624/patch_proof.json`.
- Full verifier: `scripts/verify_tavern_schemes_v624.py`.
- Primary proof: `work/analysis/tavern_schemes_v624/release_proof.json`.
- Unmodified screenshots/source/proofs:
  `E:/Rota Nova translations/Screenshots/Test fixtures/V624 Tavern scheme menus`.

Canonical `out/raphael_natural_v2_accepted_base.nds` remains SHA256
3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
No promotion is authorized. The three audits retain their verified pointers;
only their latest compiled experimental pointer advances. All18 original plaques
remain incomplete, all22 historical scopes retain their original objects, and
Confirm/five miniatures/eight village cards/legacy/comic/logo/movie/material and
broader gameplay gates stay open. The four low-resolution Online exemptions and
preserved brown marks remain in force. Revisit older record-based checks at
actual full-goal completion.
