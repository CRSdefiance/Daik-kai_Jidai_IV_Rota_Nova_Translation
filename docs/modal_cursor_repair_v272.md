# Shared modal cursor repair V272

## Actual cause and high-level repair

Rafael's Deck View tutorial, SC0_B43_R45, stores the complete word Deck but displayed
eck. The source FE selector and record bytes are intact. The old inline cursor rule
rewound x6 to x0 after an exact LF/space history. The ASCII renderer buffers pairs:
a pending blank and the first visible D were emitted at x0/x6, then the subsequent
e was emitted at x6 and overwrote D. The fourth row's n was similarly overwritten.
A correct glyph-request sequence therefore did not prove complete displayed letters.

The inherited rule is recorded in `translations/dialogue_pair_phase_arm9.json`,
DK4_DIALOGUE_ZERO_CURSOR_INLINE_BLOCK, and its historical trace in known_issues.
The earlier Janus cursor probe already documented a lost J. V272 narrows the rule:
rewind only while consuming another blank guard, or when the pair buffer is empty.
It excludes the harmful rewind before a visible character paired with a pending
guard. Safe one-guard layouts, two-space guards, larger intended indentation and
tested Japanese layouts retain their original positions. Source controls, macros,
English, all record allocations and fonts are unchanged. No duplicated letters,
record growth or extra string buffers are used.

V271's simpler blank-only predicate fixed the actual tutorial but unnecessarily
changed safe one-guard positioning. It remains reproducible and is superseded.
The final pending-buffer-aware helper preserves those already safe layouts and
compiled Grand Race help. The existing ASCII simulation has an opt-in
buffered_cursor_guard parameter calibrated against native positions; its historical
default and old formatting outputs remain unchanged.

## Native and actual saved-ROM proof

All325 at-risk ASCII FE notices execute the current real font pipeline. Every
visible cell is unique and all independent font pixels match. The old code had25
overwritten visible cells across19 records. Every previously non-overlapping
notice is pixel-, position- and return-identical to V270. Macro tokens in these
raw-input cases are explicitly stored-text inputs, not a complete live macro
expansion/playthrough claim. Japanese two-guard, guard counts0/2/3/4 and nonzero
tracking regressions remain exact. Two compiled phase-safe Grand Race paragraphs
are exact. Input/header/pixel guards, saved registers, stack, boot/cache, ARM7 source
ownership and arena checks pass.

A fresh28400-frame DeSmuME cold boot follows the exact Rafael opening, town,
Guild purchase and Y Equip sequence. The actual Deck View tutorial has all916
ink pixels, including its leading D and n, exact to the independent native raster.
Only frame22000 changes, confined to the dialog text. All73 other comparable whole
captures are byte-identical, including the2080-pixel occupied-book paper composite
and all223 tooltip letter pixels. This is targeted emulator verification, not a
live traversal of all325 notices or a full route/hardware test.

## Complete registered ROM and patch

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v272` |
| Candidate | `out/all_routes_combined_v272_candidate.nds` |
| ROM SHA256 | `e9757bebf055839831512c353fb5e5f934d2b3943fa39cf17333875276d0a8c8` |
| Patch | `out/all_routes_combined_v272_candidate.xdelta` |
| Patch SHA256 | `0b94d551e323fdc0893fa188f9fc548cab61c9e4392cf949053da9dc6cfefc6a` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch input | `work/clean.nds` |
| Clean SHA256 | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Changed internal component versus V270 | ARM9 only |

The earlier complete V270 and V271 profiles reproduce exactly through the shared
builder. All467 inherited accepted/experimental batches, required stages and prior
records remain in the neighboring manifest. Every story/COMMON file, artwork,
ARM7 and overlay is exactV270. Only the source-locked cursor branch, owned helper
and necessary startup/cache extent change. All unrelated code and the complete
inherited pool prefix are preserved. The config and registry hashes are checked;
the exact clean-base patch reconstructs V272. Ruff passes targeted files.
Experimental; explicit user cold-boot acceptance pending and canonical unchanged.
On the user's emulator, check title/New Game, Rafael's established opening/town,
the full Deck View notice and other system notices, Grand Race help and the
preserved occupied item tooltip before acceptance.

## Continuing audit

The325-record guard census is no longer a request to enlarge61 fixed allocations:
the shared cursor repair preserves every allocation. Word splitting in long
dynamic notifications is a separate layout issue. Other native parent contexts,
occupied weapon/armor and additional health/mood states remain open.
All18 plaque/hint entries and Armor/Weapon variants remain incomplete as requested.
Four Online source bodies, raw comics/legacy and other contextual/native displays,
name consistency and final whole-goal verification remain outstanding.

Revisit older record-based checks at actual goal completion. In particular, glyph
order and a bitmap rebuilt from overlapping draw events are insufficient evidence
of readable first letters: require distinct visible cells and independent complete
pixels. The graphics goal remains active and is not achieved or paused.

Native evidence: `work/analysis/modal_cursor_v272/native_proof.json`.
Actual saved-ROM proof: `work/analysis/modal_cursor_v272/saved_live_proof.json`.
Verifier: `scripts/verify_modal_cursor_release_v272.py`.
Release config: `translations/modal_cursor_guard_release_v2.json`.
