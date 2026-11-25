# Preserved native neighbors in mixed COMMON owners

V130 integrates every BGM title while keeping promotional native messages
3289-3290 byte-identical to their complete current spans. These two messages
remain untranslated and require presentation classification. Their preservation
does not add translation progress or establish that the messages are unused.

## Complete-owner accounting

The planner requires every native selection in a targeted packed owner to be
either authored or explicitly preserved. There is no automatic partial-owner
exception. Preserved IDs must be distinct from authored IDs, belong to a targeted
owner and match their current native selected spans exactly. Every byte, including
leading spaces, Japanese text, line breaks and terminal padding, must survive the
independent selector/copy emulation unchanged. Missing or unrelated declarations,
overlapping IDs and shifted/dropped bytes are rejected.

Registered preserved declarations also lock the clean source span and the
registered transform parent's current span, supply a written reason and retain
status `untranslated-renderer-classification-pending`. The complete transform
locks its input hashes, all manuscript hashes, final COMMON/ARM9 hashes, directory
hash and whole final native layout. Authored and preserved IDs are reported
separately. The global inventory continues to count the Japanese messages.

V130's source-locked transform reconstructs all inherited 467 authored selections
and adds 38 reviewed BGM titles. All 3,668 saved selections were compared against
V129 independently of the final-layout declarations; exactly 31 visible title
paragraphs change, seven reviewed titles retain their existing text, every other
visible paragraph remains unchanged, and both preserved promotional spans match
exactly. Source/current declarations are in
`translations/common_native_reblocking_v130.json`. Evidence is in
`work/analysis/common_reblock_v130_independent_research.json` and
`work/analysis/common_reblock_v130_saved_comparison.json`.

## Translating a preserved message later

The extender requires an explicit `--translate-preserved-native-message <ID>`
when a new source-locked manuscript replaces an inherited preserved span. It
checks that the inherited lock exists, the new authored ID exists and the old
clean/current locks still match, then retires only the named preservation
declaration. Reviewed registration requires the new manuscript's full editorial
and mapped-renderer gates. Do not delete a preservation lock merely to omit a
neighbor from owner accounting.

## Regression evidence and limits

Five mixed-owner regressions cover every native selected span, exact promotional
bytes, missing neighbors, a dropped first byte, authored/unrelated overlap and
changed/duplicate source declarations. Renderer regressions separately require
the exact scoped BGM patch and reject altered tracking code or font. All 72
combined integration/translation/item/sound/geometry tests pass.

The BGM renderer is a distinct title presentation. Its ASCII geometry is checked
through the source-locked tracking renderer and all 38 clean title meanings,
rather than the four-line shared-dialogue presentation. The shared-dialogue gate
continues to apply to ordinary authored COMMON messages. No long promotional
translation has been approved by relaxing that gate.

The two preserved messages, heading 3291, later COMMON blocks, older English
fidelity, ARM9/UI, graphics and actual cold-boot checks remain goal work.
