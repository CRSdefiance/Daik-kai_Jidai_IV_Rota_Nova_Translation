# V705: ordinary five-ship Sell/Refit and confirmed help wrapping defects

## New ordinary contexts

The previous goal turn made progress through V704's complete portrait initializer
and half-blend contracts. This turn changes direction to actual ship-selection
menus that differ from the previous Buy/Cargo Setup and battle/Spoils tests.

Current production V692 cold-boots from the isolated V652 saved Copenhagen fleet.
Ordinary input opens Yard > Sell, previews all four support-ship rows and two sale
quotes, declines the quotes, returns to the Yard menu, and opens Remodel/Refit for
the flagship. The Refit grid is navigated across mast, figurehead, equipment, room,
cargo and cannon controls. No inventory, location, money, condition, story, outcome
or image/crop fixture is applied. The donor save is unchanged.

Original typed getters verify the five ship names/models and25,975 funds at six
states from3200 through19700. The final screen is the Cancel remodeling?
confirmation. It is **not** evidence of completing that confirmation, committing
a refit, selling a ship or saving the changed game.

## Terminal runs and read-only drawing evidence

A completed interactive discovery and two frozen59-input replays each terminate
normally at19,700 frames. One replay uses the existing read-only host interpreter
observer; the other runs without it. No savestate is loaded. All59 complete
two-screen RGB pairs and all59 complete4MiB capture-RAM pairs match. The same59
screens match the discovery run too. The last captured RAM is from the exact last
emulated frame; a separate final RAM export was not requested.

Thirteen native host-only controls pass. All275,702 original primitive entry
records have valid argument guards, original entry words and unchanged host call
arguments. Complete source comparisons bind85,072 Frame selections and6,132
Marker selections. The remaining184,498 records are other/unsupported resources,
not claimed newly decoded graphics. All65 selected source/bank/primitive
combinations and15 caller return sites are retained.

No whole-Frame source footprint in this schedule intersects Pick Cargo, Pick Ship,
Done, Rank or Cancel, and the separate Confirm file is not selected through these
three primitives. This narrows these **specific** ordinary menus; it does not prove
global non-use, exclude another renderer or complete the six normal-parent gates.
The original private-process handler is restored and the core DLL remains exact.

## Actual defects found in Refit help

The ordinary grid navigation exposes a shared fixed-character wrapping problem.
Five entire168x75 body foreground/blank-cell planes match independent original
font masks, including the split words and continuation indentation:

|Frame|Native message ID|Actual broken word|
|---:|---:|---|
|13400|1287|`tailwin` / `ds.`|
|14600|1248|`damag` / `ed`|
|15800|1255|`b` / `uyouts.`|
|16100|1249|`ail` / `ments`|
|16400|1250|`fat` / `igue.`|

The original UI displays28 six-pixel character cells per line in these cases.
Existing manual line breaks can also create another short indented line, such as
the carpenter explanation's separate `ships.` line. This is visible formatting
evidence, not a missing-glyph or source-image corruption diagnosis.

Every selected complete current message is bound to its actual live text buffer
and stable native global message ID. Clean Japanese source is read through the
original message table as well. Reblocked current record numbers are **not**
treated as original source identities. The initial broad same-record extraction
is retained, superseded by the authoritative stable-ID mapping.

The family includes30 help entries:1248..1255 and1268..1289. Source meanings and
current text are recorded in `refit_repair_queue.json`. They include crew-role
effects, room capacities, sail behavior and equipment placement restrictions.
They require source-reviewed natural paragraphs and shared word wrapping for the
actual consumer. The intervening spoken messages1256..1267 are a separate consumer
and must not be swept into a generic help-text rewrite. This checkpoint identifies
the family; it does not claim all30 have been visited or fixed.

Next work: trace the original Refit text setup/paint, establish its width, line
advance and protective-break behavior, then implement and verify the complete
help-family correction. Do not hand-author isolated byte-positioned fixes or
silently weaken the source meaning to fit the old drafts.

## Retained diagnostic corrections

- The first noninteractive discovery reached3200 and exited1 at input EOF. Its
  captures are retained but earn no terminal-run credit. Only after that explicit
  exit did the console discovery start. All three later runs exited0.
- A verifier initially requested a separate `final_arm9_ram.bin` that this capture
  configuration does not export. The corrected verifier uses the actual last-frame
  capture and both terminal reports; it does not invent a separate export.
- Windows path spelling in a frozen-file lookup was corrected without changing
  the observer/producer or any emulation run.
- The first mast hint's live allocation is0218CD78; later tested room hints use
  0218D418. Each whole string is bound to its own actual address. A fixed-address
  verifier assumption is retained as rejected evidence, not a game defect.

No running producer was edited. Verification changes did not require replaying
successful emulator runs or changing their evidence.

## Review, archive and release

The24-panel complete discovery sheet was visually inspected. It shows all four
sale highlights, the five-ship Remodel selector, Refit help/context and the final
cancel prompt. Original captures and source-bound findings remain on E:; no guide
promotion or completed playthrough claim is made.

- Analysis: `work/analysis/yard_selection_v705/`.
- Captures: `E:/Rota Nova translations/Generated/work/emulation_v193/yard_selection_v705_*`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V705 Yard selection and Refit findings`.
- Runner/verifier: `scripts/run_yard_selection_v705.py`, `scripts/verify_yard_selection_v705.py`.

Production V692 remains SHA256
`0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.
ROM, graphics, patch, manifest, registry, canonical parent, source donor and release
pointers are unchanged. All18 original plaque/hint entries remain incomplete;
all22 historical requirement objects remain exact. Comic/legacy contexts,
material restoration, older record checks and final acceptance remain open. The
full graphics goal remains active. No commit or push.
