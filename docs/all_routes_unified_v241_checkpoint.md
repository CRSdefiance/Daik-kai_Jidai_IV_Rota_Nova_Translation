# Combined V241: navigator Sort and Filter popup

V241 is **experimental**, built from the immutable canonical baseline with the
complete registered V218 stack. The full graphics goal remains active and
incomplete. The previous turn made progress on actual gender source crops; this
turn found and corrected an additional Japanese runtime menu during live testing.

## Source and correction

Normal New Game, town, sailing, Deck View and navigator-selection input reaches an
X/Sort popup. V218 still displayed `ソート` and `しぼり込み`. They mean **Sort**
and **Filter** in this context. Both canonical-source records have individual
source/context/localization/naturalness/formatting reviews. Complete English words
and their NUL terminators fit the original 8-byte and 12-byte slots.

The original label pointer table at `02119DC4/02119DC8`, code, fonts and allocations
remain unchanged. A final registered stage applies only these two original string
slots after the complete V218 stack. Earlier source hash guards remain intact;
the canonical source bytes and exact incoming V218 ARM9 are both required.
Altered incoming/canonical data is rejected. No dialogue, macro or renderer rule
changed. This is a generated menu-text correction, not a newly edited PXL/FLS asset.

## Preservation and physical display

After the shared builder change, the entire V218 ROM reproduces byte for byte.
The V241 manifest retains all467 inherited batches, required layers and previous
changed-record declarations, adding the two explicit terminal-stage records.
Every internal file, ARM7, overlay and runtime instruction remains identical.
**Only16 ROM bytes differ**, all inside the two original ARM9 string slots.

A fresh V241 cold boot replays the exact normal-button navigation recorded in
V218. The displayed **Sort** and **Filter** match the original native ASCII font
across all ink and blank cells:111 foreground pixels, including every first/last
letter. Bounds are Sort`[116,272,140,283]` and Filter`[110,292,146,303]`, within the
bottom screen. The popup naturally adjusts its width for English. All changed
framebuffer pixels remain inside`[85,259,171,317]`; the surrounding Deck screen
is exact. Twenty-two earlier complete captured frames match V218 byte for byte,
covering the opening, selection, story, town, sailing and Deck View sequence.

The DeSmuME core is pinned to git95b4d79, DLL SHA-256
`42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b`.
Native256×384 software rendering, interpreter and English firmware are used.
No savestate, RAM injection or emulator-memory hook is used; all callback-error
lists are empty and both live runs are terminal. The optional capture-tool pause
mode only schedules ordinary button input; unattended defaults are preserved.

The attempted navigator-information navigation did **not** display a gender icon.
Do not claim V240's male/female CPU crop proof became a physical display proof.
That remaining check is still open. Sort/Filter action submenus and unrelated
screens are not globally cleared by this popup observation.

## Artifacts and release identity

| Item | Value |
|---|---|
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA-256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Candidate | `out/all_routes_combined_v241_candidate.nds` |
| Candidate SHA-256 | `d863f74ba3e5466f5a221ba93e00d53fd1588a32cecdd349006b7eb0698e8027` |
| Profile | `all-routes-unified-v241`, experimental;467 inherited batches and the new final popup stage |
| Exact clean-source patch | `out/all_routes_combined_v241_candidate.xdelta` |
| Patch SHA-256 | `8902dbdad6376f69acc7ffd6cbd53ec3e0a6a5f477ea1695cf78f69dd6a9f9b7` |
| Only changed internal component relative to V218 | `/__arm9__.bin`, two data strings only |
| Manifest | `out/all_routes_combined_v241_candidate.manifest.json` |

The patch is applied back to the pinned clean ROM and reconstructs V241 exactly.
No canonical promotion is performed. User cold-boot acceptance remains pending;
the changed Deck View navigator popup is the specific screen to check.

## Evidence

- `translations/navigator_selection_menu_manuscript_v1.json` and source-locked
  `navigator_selection_menu_release_v1.json`.
- `dk4tool/patch/navigator_selection_menu.py`.
- `scripts/verify_navigator_popup_release_v241.py`: full inheritance, complete ROM
  diff boundaries and exact patch reconstruction.
- `scripts/verify_navigator_popup_live_v241.py`: complete font masks, surrounding
  framebuffer and22 earlier frames.
- `work/analysis/navigator_popup_v241/saved_proof.json` and`live_pixels.json`.
- `work/emulation_v193/navigator_popup_v241/`: cold-boot report and captures.
- `work/emulation_v193/gender_live_v241/navigation/`: original Japanese popup,
  actual controller schedule and continuous source run.
- All changed Python files pass Ruff.

Four unreadable Online bodies, remaining embedded/environmental/alternate display
consumers, name consistency and full-scope visual/gameplay verification remain
unfinished. The goal is not complete. At eventual completion, revisit older
record-based checks as requested.
