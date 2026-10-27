# V697: Arcadius's original story-controlled gender symbol

V696 made progress by adding the final comic-art contract and proving a complete
byte-exact V692 rebuild. This turn closes the specific untested identity-8/flag-9
exception in V694's second crew-assignment parent. No production ROM, artwork,
wording, patch, registry or release pointer changes.

## Original source behavior

The clean/current actor table identifies actor 8 as Arcadius. The original actor
identity getter returns 8 and raw gender getter returns 1. The original room
helper `020157D8` treats this identity specially: it calls `02023C60` with flag
index 9, then changes the displayed selector to 0 only when that flag is clear.
The getter returns a bit mask, not Boolean one: 0 or 512 (`1 << 9`).

The exact flag object is `02276F90`; flag 9 occupies bit 9 of the word at
`02276F94`. Complete original setter/getter executions independently reproduce
setting and clearing only that bit, with every other main-RAM byte unchanged.
The original gender helper and flag routines remain clean-ROM identical.

## Declared isolated fixtures

Four 10,800-frame V692 cold boots use the unchanged Hodram Copenhagen donor and
normal menu navigation to a real Deck room. Two runs observe the full selected
checkpoints; two use only the minimal identical fixture writer. None loads a
savestate, changes a ROM, injects graphic pixels or claims earned recruitment.

At the original selection-update entry, guards confirm room 5, the actual
one-entry roster and selected actor 1. The fixture changes only its selected
lookup word to actor 8 and sets or clears flag bit 9. The original actor getter,
story-flag query, selector, view construction, portrait loading and drawing run
normally. The private fixture does not add Arcadius to the real party or force
a gender-view result.

Before frame 10001, both words are restored to their exact original values, then
normal B input leaves the roster. Full before/after RAM dumps prove that install
and restore touch only the declared lookup word and story bit. CPU prefix,
DTCM and ITCM remain unchanged by those writes. The source donor stays byte-exact.
Every report explicitly marks the synthetic fixture and its lack of earned
actor/story progress. No fixture picture is promoted to the guide.

## Actual results

- All 54 observed/minimal-fixture whole two-screen RGB pairs match exactly.
  All 54 corresponding complete 4 MiB capture-RAM pairs, both complete terminal
  RAM pairs and all install/restore before/after states also match.
- Actual original calls report raw gender 1 and identity 8 in both runs. Flag
  getter returns are 0 and 512; processed selectors are male 0 and female 1.
- Actual original draw arguments bind the 16 by 16 view and destination `(80,80)`.
  Two complete original native cache-hit getters bind every Marker file byte and
  return with their saved-register/stack ABI intact, without I/O bridges.
- Eight held complete symbol cells match all 2,048 native-five-bit pixels, with
  every border, background, arrow and cross included. All 24 wrong-sex, palette
  and shifted-placement controls fail.
- Independently comparing the male and female source cells predicts exactly
  25 changed pixels. The full two-screen screenshots differ at exactly those
  source-predicted positions in all four held comparisons, with no other changes.
- All 21 pre-fixture cross-state screenshots and both post-restore screenshots
  are whole-RGB exact. The original Deck screen returns normally.
- The 45 host-prefix and eight bounded-mirror controls pass. All private host
  interpreter slots are restored and the core DLL remains exact.

The actual six-screen comparison sheet was opened. It shows both complete
symbols, Arcadius's unchanged profile and the normal restored Deck screen.
Magnified symbol crops occupy a separate labelled strip below each whole
screenshot; they do not cover the original screenshot pixels.

## Exact native construction prefix and retained limits

Both original selection-update prefixes execute from `0209C1DC` through completed
gender-view construction at `020158DC`. They include the actual actor lookup,
class cast, room lookup, identity/gender getters, flag query and view constructor.
No native call is bridged. At all 14 recorded checkpoints, R0–R14, CPSR, complete
4 MiB RAM, 16 KiB DTCM and 32 KiB ITCM match. Each executed instruction matches
the registered current code. This is not a claim about every internal CPU field.

The larger info-update function continues with other work after this stop.
V694's complete-suffix RAM/DTCM mismatch remains unresolved and is not waived by
this prefix proof. Other consumers and the embedded copy receive no display
credit from these tests. Earned recruitment/reveal, full route playthroughs,
every animation frame and physical hardware are not verified here.

## Recording and remaining goal

Current candidate remains V692, SHA-256
`0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.
All 18 plaque/hint entries remain incomplete and all 22 original historical
requirements remain exact. The full graphics goal, remaining control/card/comic/
legacy contexts, restoration review, older-record follow-up and final acceptance
remain open. No new ROM, patch, guide approval, commit or push.

- Producer/fixture guards: `scripts/run_gender_exception_v697.py`.
- Native prefix: `scripts/replay_gender_exception_v697.py`.
- Whole-screen/source/fixture verifier: `scripts/verify_gender_exception_v697.py`.
- Analysis: `work/analysis/gender_exception_v697`.
- Captures: `E:/Rota Nova translations/Generated/work/emulation_v193/gender_exception_v697_*`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V697 Arcadius gender exception`.
