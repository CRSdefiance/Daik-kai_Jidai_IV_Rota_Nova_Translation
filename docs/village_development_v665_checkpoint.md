# V665: all 24 passwords, developed-port coverage and seven confirmed repairs

This checkpoint tests the unchanged V653 combined ROM. All 24 passwords were
entered through the game's actual Latin/symbol keyboard, confirmed normally,
and accepted by its original comparison/development branch. Each intended
village changes from development0 to2. No password, discovery, development,
story, scene, resource or victory flag is injected.

## Actual coverage

- Every typed prefix is read back from the actual initialized editor, including
  its cursor and18-byte capacity, and independently compared to the complete
  108x11 visible input field. This includes `Sugarloaf Mountain` at its full
  18-character capacity and both answers containing spaces.
- All24 answer confirmations, clue paragraphs, facilities notices and the73
  remaining menu labels after removing Promised Words are checked completely.
  The two indentation defects below receive lettering coverage, not alignment
  approval.
- Twenty-three intended developed ports are reached and their complete title
  names, specialty fields and native two-screen compositions are verified.
  All2,260,992 pixels are included. Destination/foreground checks prevent
  giving another town credit as the intended village.
- Karibib's password and development are verified, but its return is interrupted
  by an original encounter. Its intended developed-port screen remains open.
- All3 actually selected village backdrops are complete resident files and
  source-exact. None of the8 complete white village-card files appears in the
  sampled development/return RAM snapshots. This does not establish global
  non-use, exclude transient loads, or close their ordinary display contexts.

## Five actual port-name discrepancies

The original Town name getter and live header masks confirm:

| Village / established name | Current developed-port label | Original metadata name field |
|---|---|---|
| Cape Cod | Cod | 021250E0 |
| Dikson | Dixon | 02125398 |
| Leveque | Lebeque | 02125568 |
| Tiksi | Tsukushi | 021257AC |
| Korf | Corfu | 02125820 |

These are the same places as the already localized discovery/docking names.
The choices and source rationale remain in `village_names_v610_decisions.md`.
Each Town metadata word can point at its existing approved VillageModel name
string. The original Town getter then supplies the consistent name throughout
its callers. No new string allocation or broad search-and-replace is needed.

## Two actual clue-indent defects

Valparaiso and Wanganui have a36-character first row starting at x16 and a
continuation starting at x22. All letters are present, but the six-pixel indent
is inconsistent. The complete actual foreground masks retain this failure.

The proposed compiler uses35 content cells on every row instead of36 on the
first row and35 thereafter. All24 clues are recompiled and checked; only these
two change. Words, punctuation, paragraph meaning, string lengths and pointers
remain identical. The changed bytes move generated line breaks/guard spaces.
This is a formatter repair, not newly authored prose or manual editorial breaks.

## Prepared repair, not yet a playable release

`dk4tool/patch/village_port_consistency.py` implements the five existing metadata
aliases and two reflows. It is pinned to the complete V653 ARM9 and restores all
other bytes exactly. Every section length, native instruction, font, graphic,
answer and cache/arena boundary is preserved. Target ARM9 SHA256:
`b92df335942af8db216b149f54c0eac75626ddde2cf573b6f41c20f3e217bda8`.

The research ARM9 and proposed release configuration are saved in
`work/analysis/village_development_v665/`. They are not a playable ROM. The next
step is registration, an integrated candidate/clean patch, and actual captures
of all five corrected headers and both aligned clue boxes before claiming repair.
V653 and its registry/release pointers remain unchanged in this checkpoint.

## Verification assumptions and retained attempts

The actual Common296 template begins with full-width CP932 `Ｉ`, followed by
ASCII `s %s all right?`. Its complete9-pixel native KANJI glyph and the remaining
ASCII field match. An all-ASCII expectation would falsely report a missing I;
no leading-character waiver or ROM change was made.

Town scenes have different facility-node counts. The new isolated native replay
follows every actual original visibility result and selected callback, rather
than requiring Narvik's historical18 nodes/17 draws in every village. It poisons
both destination surfaces, checks all bytes were assigned before being read,
excludes visible VRAM as source, and retains ABI/code/source bounds.

Perth and Wanganui had already consumed the transient footer submission in their
captured CPU state. The earlier fragment therefore omitted the entire1600-pixel
footer when replayed. The corrected component contract executes the original
cached-descriptor API and the original CPage submission instructions
020C9DC4..020C9DD4 using its initialized actual owner. Only the transient queue
word changes in that isolated setup; cached strings, geometry, palette, pixels
and DTCM remain exact. All720 active cache cells and140 English glyph pixels are
independently ROM-font verified. Complete subsequent screens then match without
masking the footer. This supplied registration phase is disclosed; it does not
claim a complete emulation of the original UI update timing.

Eight initial return attempts sailed out of range. Fresh replays add one
coordinate-only approach and reach their real intended ports; their common
prefixes match. All originals remain retained. Karibib's extended exploratory
sequence reaches defeat/Game Over and later Syracuse, so it receives no Karibib
return credit. One further controller stopped before checking its final available
Sea frame; a revised attempt applies an extra approach but still fails the real
Karibib header check. These failures remain evidence; no guessed scene or outcome
flag is used to manufacture a passing destination.

## Archive and remaining scope

Captures and derived comparison sheets are archived under
`E:/Rota Nova translations/Screenshots/Test fixtures/V665 Village development`.
All screenshots retain their original bytes. The derived sheets label the
location fixtures and pending repairs. No guide publication approval is inferred.

The proof is `work/analysis/village_development_v665/proof.json`. All18 original
plaque/hint entries remain incomplete and all22 historical requirement objects
remain exact. The seven repairs, Karibib return, eight card contexts, other
unresolved controls/legacy consumers, material acceptance, older record checks
and final release acceptance remain in the active graphics goal.
