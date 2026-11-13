# V732: original SC cache-to-interpreter handoff

The previous turn made progress by resolving V731's packed sprite-mask writer
lead. This batch follows the outstanding village-card question through the next
original source path after V727's complete file loader: the parent that hands
an already loaded SC block to its first native instruction read.

## Source and declared inputs

All 1,307 SC blocks in each clean/current ROM are bound individually to V727's
complete native file-loader outputs by whole archive and payload hashes. Those
file loads are carried forward, not repeated or counted as fresh loading tests.

Each test supplies the resulting cached object, a scratch parent stack, the
original two descriptor-class constants, and the active-event field. Mode inputs
0 and 1 are tested separately. Original instructions execute from `02023F4C`,
through the real cache-hit path at `02024134`, parent descriptor setup and
`02023FFC`, to the first instruction read at `0202A524`. Execution stops at
`0202A530`, before the first opcode handler.

These are explicit isolated native contracts. The parent action's reachability,
the preceding whole event, future handlers, frame wait and gameplay are not
silently supplied or claimed. No UI helper, cache return, descriptor result or
SDK outcome is stubbed. An unexpected SDK/file/assertion call fails the test.

## Complete finite result

| Route | Blocks per ROM | Two-mode handoffs per ROM |
|---|---:|---:|
| Rafael | 343 | 686 |
| Joakim | 325 | 650 |
| Lil | 336 | 672 |
| Maria | 303 | 606 |
| **Total** | **1,307** | **2,614** |

Both clean and current pass: 5,228 native handoffs/first reads in total.

- The original cache hit returns success with its expected parent stack.
- The parent builds its own stream descriptors. Their instruction pointer is
  exactly the loaded SC payload plus its eight-byte file header.
- The actual first source read is one halfword at that pointer, from native
  `0202A524`; the initial decoded length is two bytes and the major category
  matches the source word. Both mode values pass through unchanged.
- Every complete source header/body/stored padding, cache metadata and trailing
  guard remains exact. The parent's distant argument canary remains intact.
- All 2,614 clean/current first-word, category and mode pairs match. This checks
  the first instruction of each block, not all later speaker/text preambles.
- Every executed instruction matches its ROM's mapped source; all relevant
  parent/loader/dispatcher ranges are also byte-exact between clean and V712.

The initial verifier incorrectly required the SC declared body length to equal
the entire stored payload. The original storage includes either zero or two
zero alignment bytes. The corrected verifier checks the declared halfword body,
four-byte storage alignment and all padding bytes. No ROM fix followed from that
test-contract correction. The initial successful result was retained before
adding the explicit cross-ROM first-word comparison; the final run includes it.

## Consequence for the village cards

V727 already establishes that the source SC blocks lack the eight village-card
image-command patterns. V732 closes generation/mutation in this specific
original cache-to-first-read path. The parent does not synthesize a card command
during this handoff. Repeating this handoff or the completed file-loader census
is not the next useful investigation.

Mutation during later opcode execution, other stream builders, indirect/direct
filename consumers and the ordinary village-card triggers remain unverified.
This is not a global unused-art claim or a new native village display. Existing
V699 complete controlled card displays remain their separate completed scope.

## Preservation and artifacts

V712 ROM, manifest, patch, registry, canonical baseline, art and saves remain
unchanged. The work ledger adds a closed consumer lead, preserving its 23
completed scopes and six active groups. Original 18 overall plaque objects remain
incomplete and all 22 historical requirement objects remain exact. The graphics
goal stays active; no new ROM, screenshot, guide approval, promotion, commit or
push occurs.

- Verifier: `scripts/verify_script_handoff_v732.py` (targeted Ruff passes).
- Evidence: `work/analysis/script_handoff_v732/proof.json` and `native_cases.json`.
- Checked E archive:
  `Rota Nova translations/Screenshots/Audit comparisons/V732 Script handoff`.

The four low-resolution Online bodies remain excluded, brown marks remain
preserved, and the older-record checks remain a follow-up after goal completion.
