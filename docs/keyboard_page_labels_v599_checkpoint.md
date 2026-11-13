# V599: English name-keyboard page controls

## Change and source meaning

The name keyboard's functional **英** control opens its Latin alphabet page;
**記** opens its symbols page. They now display **EN** and **#+** respectively.
Both fit the original 12-by-12 cells. The Japanese syllabary and other selectable
characters remain original character-entry choices. No character data is removed.

Earlier retention notes correctly warned that these encoded strings also serve
as lookup identifiers. V599 supersedes the decision to retain their *visible*
Japanese labels by changing one category-paint call only. The provider still
receives the original identifiers. It resolves them to the original pages 50
and 51, with all 52 Latin and 26 Symbol choices unchanged.

## Exact implementation and ownership

The original call at 020B0354 to 020D5404 now uses a display wrapper at 01FFC780.
It substitutes only those two original label pointers, then tail-calls the
original painter. All other 47 original category pointers fall through unchanged.
The original return and saved-register/stack contracts pass all 49 routing cases;
the painter boundary is bridged in that routing probe only. Actual emulator
pixels below independently verify the original painter and real navigation.

The wrapper and its literal labels occupy 52 bytes of the original zero gap
01FFC780..01FFC800 inside the existing 4096-byte autoload section. Its preceding
helper ends at 01FFC77C; later data starts at 01FFC800. An all-byte pointer census
finds no source main/overlay pointer into this owned gap. The patch changes one
four-byte main call and that payload. It changes no font, table identifier,
character choice, section extent, pool size, heap, startup or cache behavior.

## Actual ordinary keyboard test

A fresh 7,900-frame cold boot uses normal New Game, biography Y Edit, and A on
Name. There is no battery save, savestate, RAM injection, inventory/location
fixture or gameplay Save action. Its exact 22-event schedule is recorded.

- Twelve complete EN/#+ masks pass across six primary-grid states. Native text
  origins are (158,320) and (172,320), with the original six-pixel ASCII advance.
  Every leading/trailing letter and the complete blank region are checked.
- At frame 5500, all 52 Latin choices match the original Shift-JIS font/map;
  every foreground position in the full 140-by-84 grid is checked.
- At frame 7000, all 26 Symbol choices match the original font/map; every
  foreground position in the full 140-by-42 grid is checked, including blank cells.
- The actual editor buffer gains full-width a (8281) at frame 5700; Y Delete
  removes the whole character at 5900. B returns to editing at 6100.
- Reopening the keyboard and selecting #+ opens Symbols. A inserts full-width
  zero (824F) at 7300; Y removes it at 7500. X Finish reaches confirmation at
  7700 with the complete name Rafael; B returns to editing at 7900.
- The complete 98,304-pixel edit screen is identical at 4400, 6100 and 7900.
  Initial/post-edit confirmation differs only at the same 182 state-header
  pixels documented previously; the full name and all other pixels are exact.
- Against historical V582 captures, three primary-grid frames differ at exactly
  178 pixels, all inside the two declared 12-by-12 cells. The whole Latin popup
  at 5500 is byte-identical in RGB. Historical V582 used V581; file/ARM9 guards
  separately establish the exact new delta against V593.

The early controlled bitmap diagnostic used a supplied blank bitmap after an
attempt to execute the normal clear routine encountered unmapped hardware.
It is research evidence only and is not needed for the native pixel proof.
Initial five-pixel advance and y=326 guesses were rejected; the complete native
masks prove six-pixel advance and y=320. No renderer was changed to fit a test.

## Ordinary regression and preservation

A second fresh 24,100-frame cold boot replays all 203 ordinary Market inputs
from V598: title/New Game/story/town, purchase and sale staging, confirmation,
cancellation and reentry. All 19 shared captured full frames are RGB-identical
to V598 (1,867,776 pixel positions). This is sampled regression evidence, not a
claim about every intervening frame or a complete route playthrough.

Only `/__arm9__.bin` differs from V593. Every other ROM file/component remains
byte-identical, carrying forward the 921 PXL/FLS and 57 embedded-block checks.
All 470 batches and 114 accepted layers remain present. Applying the distributed
patch to the clean ROM reconstructs the exact candidate. All 18 original plaque
inventory entries remain incomplete and all 22 historical objects remain exact.
The global wood-material, legacy/event/miniature/Confirm and movie gates stay open.

## Candidate and handoff

Status: **experimental**, not promoted or human accepted.

- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v599_candidate.nds`
- Candidate SHA256: `1c72049ca2eba551825d67de2429b4ac9751179183afc2ddb5749666d398eba5`
- Profile: `all-routes-unified-v599`; full V593 stack plus
  `translations/keyboard_page_labels_v1.json` as the new experimental stage.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Canonical base SHA256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Changed internal component from V593: `/__arm9__.bin` only.
- ARM9 SHA256: `85d1b032ebdb16a4337f43de46b4bca4207b7ded8d763ef71eb1960791db0fe7`
- Patch SHA256: `2aa5a523cfef3165db2eae31643b2d66e3e08a75aa709c025066958a144ffc9f`
- Neighboring `.manifest.json` records the complete accepted/experimental stack,
  registry hash, original canonical base, changed paths/records and builder gates.
- Automated checks: `scripts/probe_keyboard_labels_v599.py`,
  `scripts/verify_keyboard_labels_v599.py`, targeted Ruff and Python compilation.
- Human cold-boot checks for acceptance: title/New Game, name editing, EN/#+
  page selection, character insertion/deletion, Finish/Back, and normal town UI.
  Physical hardware and full-route verification are not claimed.

Proofs, schedules and preservation evidence are in
`work/analysis/keyboard_labels_v599`. Original native reports/screenshots are on
E under `Generated/work/emulation_v193/keyboard_labels_v599` and
`keyboard_v599_market_regression`. Eight unmodified ordinary screenshots are
archived under `Screenshots/Guide candidates/V599 Name keyboard`; publication
is unapproved. Source/current comparisons and reproducibility files are under
`Screenshots/Audit comparisons/V599 Keyboard controls`.

The previous status-only goal turn added no graphics completion evidence. This
turn is progress: a registered display correction and source-bound native tests.
The full goal remains active. Revisit older record-based checks at completion.
