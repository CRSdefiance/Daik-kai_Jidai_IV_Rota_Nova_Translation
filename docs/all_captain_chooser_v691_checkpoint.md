# V691: all four actual captain chooser updates and complete name fields

## Current result

Two fresh 5200-frame V685 cold boots cycle Rafael → Hodram → Lil → Maria → Lil →
Hodram → Rafael with normal controller inputs. Both finish normally with exit 0.
The previously authorized byte-exact system-unlock donor makes Maria available;
this is fixture access, not earned route completion. No story, inventory or
location state is injected. The second case retains V690's explicitly declared
single raw17 scratch-buffer replacement.

All seven selected states per case have complete source-photo and name-field
verification. The original four 104×136 PXL photos remain byte-exact to the
Japanese ROM. All 14 displayed photo planes match every source native-five-bit
pixel at bounds [76,28,180,164]: 198016 pixels including edges and backgrounds.

| Captain | First | Middle | Last | Existing company/fleet field |
|---|---|---|---|---|
|Rafael|Rafael|empty|Castor|Castor Co.|
|Hodram|Hodram|Joakim|Bergstrom|Bergstrom Fleet|
|Lil|Lil|empty|Argot|Argot Co.|
|Maria|Maria|Huamei|Li|Li Clan|

These are existing integrated names, not new spelling/localization changes.
All 56 full 113×11 name/middle/surname/company fields match independent original
ASCII-font masks. First and final letters, spaces and all trailing blank cells
are checked. Empty middle-name fields are checked as empty whole fields. This
includes returning from longer fields to shorter ones without stale letters.

## Original ownership and cached files

Actual parent 02192500 points to the selected record through field +54; original
setter 02046F00 stores the selected index at record+4. Name fields are independently
read from their observed fixed offsets. Each selected view at parent+5AC+i*30h
is type4, source origin (0,0), size (104,136), with its real initialized owner.
Owner filename+12 binds `personbustup00.pxl` through `personbustup03.pxl`.

Fourteen complete original native resource-cache getter calls on copies of the
captured states return every byte of the corresponding original ROM file. All
calls return with their stack/saved-register ABI intact, and all executed code
words match Japanese source. No SDK I/O, loader, getter return or pixel result
is bridged. These are isolated cache-hit proofs, separately supported by actual
whole-photo pixel comparisons; they are not additional live filesystem traces.
Reserved view words are retained rather than invented as zero.

## Persistent live input control

The read-only control and declared-input case have 14 complete two-screen RGB
pairs, all exact. Every post-entry captured state through frame5200 retains the
diagnostic 14144-byte pattern in raw scratch, including all four captain views
and the reverse cycle. Complete captured/terminal main RAM is otherwise exact
between cases; this is checked by constructing the complete expected RAM with
the single declared region replaced, not by tolerating unrelated differences.

All 20 initialization-event CPU prefixes also match between cases. The source
raw17 contents, replacement extent and complete before/after fixture snapshots
are independently verified. The observer restores private host slots and leaves
the core file unchanged. V690's identical 20 host-prefix/eight mirror controls
are reused with hashes, exact targets and frozen observer source checked. The
runner changes only process-local observer configuration before loading the core;
no live producer or shared helper file is edited.

The all-four source/current-case screenshot sheet was opened and reviewed.
No missing leading/trailing name letters, stale field text, portrait cropping or
new visible defect was identified in these selected views. Biography prose is
observed without being rewritten or granted a full editorial review here.

## Consequence and remaining scope

This supplies current actual display and complete source binding for all four
loose captain portraits and their default name fields, including Maria and
reverse selection. It strengthens the distinction between these loose PXL views
and the legacy raw SLACK14–17 payloads. It does not identify a different raw
consumer, clear every intermediate frame, establish legacy palette semantics,
or prove global unused art or full route/hardware coverage.

All 18 original plaque/hint entries remain incomplete. All 22 historical
requirement objects remain exact; prior narrower evidence is retained as history.
Six control contexts, eight village cards, other legacy/comic/standalone art,
material review, older record-based checks and final acceptance remain open.

## Files and unchanged release

- Runner: `scripts/run_all_captain_chooser_v691.py`.
- Verifier: `scripts/verify_all_captain_chooser_v691.py`.
- Frozen reused observer: `scripts/trace_chooser_raw_independence_v690.py`.
- Analysis: `work/analysis/all_captain_chooser_v691`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V691 All captain chooser`.
- No fixture screenshot is promoted to guide approval.

Current experimental ROM remains V685, SHA256
`83e7bdc7c4926ad69eb04704e8327aba50d0fe29b00cce7f5f59d4be8c203150`.
ROM, manifest, patch, registry, canonical baseline, donor saves and release
pointers remain unchanged. Full graphics goal remains active. No commit/push.
