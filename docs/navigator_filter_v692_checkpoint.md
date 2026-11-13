# V692: complete Captain filter caption and retained gender-context gap

The previous turn answered a status question and made no goal progress. This
turn discovered and repaired an actual untranslated caption while investigating
the second gender-symbol consumer. The graphics goal remains active.

## Source and shared repair

Deck View's navigator roster has Sort → Filter → Unassigned / 艦長 / All.
V263 localized the two outer entries; the middle entry remained Japanese.
艦長 means Captain and matches the established ship-role glossary. This is a
role/filter caption, not a person's name or a change to their rank.

The clean and V685 ARM9 contain the complete original eight-byte allocation
at file offset `14F33C`: `8ACD92B700000000`. Its enabled descriptor at `14F470`
still points to `0214F33C`. The repair writes `Captain\0` into that allocation.
Seven bytes differ; the final NUL remains zero. No pointer, executable
instruction, allocation size, font, palette, geometry or filter logic changes.
Every consumer of this shared string receives the same repair.

The opt-in final builder stage is registered in `all-routes-unified-v692`.
The complete build retains all 470 batches, 114 accepted layers, prior profiles,
all previous changed records and both final story-format/material contracts.
Against V685, only this ARM9 caption slot differs. All 675 whole loose PXL/FLS
files, embedded graphics archives, story/COMMON/HELP files, ARM7, overlays and
every other ARM9 byte are exact. The clean-ROM patch reconstructs V692 exactly.

## Actual display and input evidence

Three final 15,200-frame cold boots test V685/Hodram, V692/Hodram and V692/Maria.
They use copied cartridge saves, normal menus and isolated duty changes. No
savestate, live RAM/code/location fixture or observer is used in these final runs.
The Maria donor retains its historical selection-unlock/bypass provenance; this
does not establish an earned unlock. Neither donor is modified.

The normal sequence opens the navigator roster and cycles the Captain, All and
Unassigned choices. The first attempted schedule selected Captain repeatedly
because the popup resets its selection on opening. Those runs are retained;
the follow-up schedule explicitly accounts for that original behavior.

Fourteen complete Captain rows across both current saved routes pass independent
font masks, including initial/final letters and all surrounding blank cells.
The unchanged Unassigned and All controls establish the center and row pitch;
Captain's position is derived as `(107,282)`, not found by searching its letters.
The complete 70×11 row interior contains no leftover Japanese ink. The original
popup border and remaining labels are preserved.

The same-frame source/current comparison has seven caption-bearing changed
frames. Two frames additionally show different selection highlights:

- Frame 9600: 87 pixels in `[88,247,104,268]`, teal versus dark. The complete
  16×32 selected-officer cell matches the retained original appearance at 11600.
- Frame 10800: 1446 non-caption pixels in `[6,208,158,278]`. The complete current
  frame outside the caption row matches the retained original appearance at 14000.

These observations are recorded separately. The baseline frames are not shifted,
and same-frame highlight timing is not claimed proven. The terminal menu-run RAM
has 147 differing bytes; its complete addresses/hashes are retained and no
unqualified equal-RAM claim is made for those menu runs.

A separate ordinary 24,100-frame V692 New Game, without a donor or fixture,
matches all 89 retained V685 whole-screen captures. It covers boot/input,
character selection, opening story, town and trading UI. Its full terminal RAM
matches after replacing only the declared eight-byte source caption slot.
This is targeted emulator verification, not a complete route/hardware test.

The actual before/after/Maria/return-cycle sheet and representative ordinary
selection, story and market frames were opened and reviewed. Captain is complete
and readable; no new caption clipping or Japanese residue was identified.

## Gender investigation: still open

The original RTTI at `02130D00` identifies `18CDeckPersonnelView`; its caller at
`0209C278` invokes gender update `020157D8`. That helper uses the original actor
gender getter and an original identity/story-flag exception before constructing
the 16×16 male/female marker views. This source mapping does not prove a current
visible panel. Twelve exploratory saved-game runs exercised Deck, assignment,
help, sailor counts, navigator lists and departure choices without capturing
that actual helper entry.

The last exploratory observer reached `0209C27C` without a preceding helper
entry. That is an original possible bypass, but the initial observer asserted
instead of classifying it. Its terminal capture report, failure and frozen
producer are retained. The unobserved source run independently matches its
whole pictures through frame 8800, before the schedules diverge. This failure
is not counted as actual gender-helper display coverage or global non-use.

The initial static verifier also assumed that V685's original manifest already
contained V687's final material-contract field. The corrected verifier checks
the actual original ROM with the same final guard; the failed source is retained.
The initial live verifier's overly broad whole-frame expectation is likewise
retained alongside the separate cursor observations above.

Both gender symbols already have Sailor Info evidence. The second consumer and
embedded copy remain open. Six small control contexts, eight white village-card
contexts, comic/legacy/standalone artwork, restoration review, older record-based
checks and final acceptance remain. All 18 original plaque/hint entries stay
incomplete and all 22 historical requirement objects remain exact. The user’s
Online exclusions and brown-mark preservation decision remain in force.

## Experimental handoff

- Candidate: `out/all_routes_combined_v692_candidate.nds`.
- SHA-256: `0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.
- Manifest SHA-256: `1756a15b2d6a370a381e5fb6a44c54754a9020714cef9cc447ec34ca338ccade`.
- Patch SHA-256: `90cc9ab5b34bd66b3215d5fc97c855764ddafb0b11d9498903ece4a7df54281b`.
- Profile: `all-routes-unified-v692`; all 470 inherited batches/114 accepted layers.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Changed internal component versus V685: `/__arm9__.bin`, one eight-byte slot.
- Verifiers: `verify_navigator_filter_v692.py`,
  `finish_navigator_filter_v692.py`, targeted Ruff and final archive verification.
- User cold-boot areas: title/New Game, established story/town, then Deck View →
  navigator roster → Sort → Filter; check Captain and return navigation.
- Experimental; canonical baseline and historical V610 pointers are unchanged.

ROM, manifest and patch are on E through the existing output junction. Evidence:
`work/analysis/deck_gender_v692` and `Screenshots/Test fixtures/V692 Navigator
Captain filter`. Run directories already on E are retained by checked absolute
references in the archive, avoiding duplicate multi-gigabyte RAM copies.
Ordinary guide candidates have separate provenance; fixture-access/duty-test
pictures are not guide-approved. No commit, push or canonical promotion is made.
