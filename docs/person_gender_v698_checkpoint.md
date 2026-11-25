# V698: Sailor Info story-controlled symbol and complete plaque crops

## Scope and result

The previous goal turn answered a status question and made no implementation progress.
This checkpoint completes a distinct display check in the original
`22CPersonInformationView` Sailor Info parent. V697 covered the separate Deck
crew-assignment parent. The current release remains V692; this checkpoint changes
no production ROM, artwork, dialogue, patch, manifest, registry or release pointer.

Four terminal 7,800-frame cold boots use the unchanged V476 Syracuse equipment
test donor. Each uses the declared selected-actor lookup and story-flag fixture;
two additionally record original code checkpoints. The other two are minimal
fixture baselines, not completely unmodified emulator runs.

All 42 whole two-screen RGB pairs and 42 complete 4 MiB capture-RAM pairs match.
Both complete terminal RAM pairs and the full before/after install/restore memory
pairs match. All observers finish without callback errors, with host slots restored.

## Original display inputs and independent source checks

- Parent: `02189E24`; its original class name, five-entry array `02190A58`, and
  selected index are checked from recorded RAM.
- Only the first selected-actor lookup word (Hodram 1 to Arcadius 8) and story flag
  9 change. The original flag word is 1. Flag 9 is cleared/set for the two cases;
  all other RAM bytes and captured CPU/DTCM/ITCM remain unchanged at each write.
- Original input navigation reaches Sailor Info at frame 5913, moves to Manuel
  Almeida with R, and returns to Arcadius with L at frame 6702. Both original
  Arcadius update calls are recorded, including raw gender 1, identity 8,
  original flag getter return 0/512, and processed selector 0/1.
- Original copy arguments use software buffer 1, source `(232,96)` or `(240,112)`,
  size `16x16`, and upper-screen destination `(84,76)`. Buffer numbering is not
  the physical display order.
- Full original native cache getters from both construction and actual draw RAM
  resolve complete current Marker files. The cached header moves from `0232CCC0`
  to `0231CA90` between those snapshots; equality of pointers across frames would
  be an invalid assumption. Complete file bytes match independently in each state.
- Eight complete symbol cells (six Arcadius, two next-officer controls) verify
  2,048 native five-bit pixels. Wrong sex, palette and one-pixel placement controls
  fail for every cell.
- Three held Arcadius screens differ between flag states at exactly the 25 pixels
  independently predicted from the two Marker source cells. All 15 pre-fixture
  captures, the next-officer screen, and both return captures match whole RGB
  across the flag states.

## Plaques and visual review

All ten static Sailor Info plaques match complete current source rectangles in
eight held states: 80 whole plaque crops, 55,200 native five-bit pixels. The
current full Person Info PXL is byte-exact to the V666 asset used in the V671
original/current review packet. The old V542 grain target hash predates later
registered bevel/frame repairs and is not the final artwork hash.

The complete six-screen review sheet was opened and inspected. Health, Mood,
Level, HP, Stamina, Agility, Charm, Wits, Spirit and Luck remain readable; both
symbol states fit their complete boxes. Magnified symbol insets are separately
labelled below uncovered complete screenshots.

All 18 original plaque/hint audit entries remain incomplete. These matching
pixels establish display fidelity in the sampled states; they do not approve the
wood restoration or close other variants, the Equipped Items hint, or user review.

## Fixture artifacts and retained failures

Both original inputs are restored before frame 7401's normal B action. On returning
to the roster, the already cached Arcadius portrait persists beside the restored
Hodram name. This is retained and explicitly classified as a fixture artifact:
the test changes a private UI lookup without performing an original roster
rebuild. These return pictures prove neither ordinary portrait/name consistency
nor earned recruitment. They are not guide candidates.

The first navigation attempt stopped at the Sailors popup without installing a
fixture. Its source/log/captures remain retained. A second completed pilot reached
Sailor Info but used the incorrect software-buffer-0 draw filter. The final four
runs use buffer 1, independently located in the retained V669 draw trace. The
producer is frozen for all final runs; no running helper was edited.

The separate complete original update-prefix replay stops with `UcError()` at
`020E31E4`, after `update_entry` and `actor_ready`. The failure and replayer remain
retained. **No full prefix equivalence is claimed.** This test-tool/model gap has
not been diagnosed as a production game defect. V694's separate full-suffix
RAM/DTCM differences also remain unresolved. Neither gap is masked or cleared by
the successful screenshot/source comparisons.

## Evidence and remaining work

- Analysis: `work/analysis/person_gender_v698/`, including both earlier attempts.
- Final proof: `final/screen1/proof.json` below that directory.
- Captures: `E:/Rota Nova translations/Generated/work/emulation_v193/person_gender_v698_*`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V698 Sailor Info gender exception`.
- No hardware verification, earned Arcadius recruitment/reveal, complete route
  playthrough, guide promotion, commit or push is claimed.

This closes the sampled original Sailor Info Arcadius display exception check.
The six small controls' actual contexts, eight village cards, original comic
playback, remaining legacy/embedded contexts, texture/restoration review, older
record checks and final acceptance remain open. The full graphics goal is active;
all 22 historical requirements and all 18 incomplete plaque/hint objects remain
preserved.
