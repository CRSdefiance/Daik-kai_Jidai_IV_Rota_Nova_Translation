# V787: shared scheme-name width and complete native rows

## Status

This is native research for the pending item/diplomacy batch, not a new playable
ROM or production prose approval. V783 remains current. Editorial coverage stays
417 completed,496 source/prose reviewed and79 drafts. All76 pending paragraphs,
wider shared/route/prose review and the separate graphics audit remain unfinished.

## Shared formatting defect and repair

The original CScheme name-width method at0209145C returns10 cells. Its sole
reference is CScheme's vtable field0214C624. The generic selector calls this
method at0204F10C and multiplies its result by6 to size the text area. Original
Japanese scheme labels used an even byte-width bound. The current English
Forge Papers already has12 ASCII cells; the proposed full nominal names reach23.

The research repair changes one existing ARM instruction from `mov r0,#10` to
`mov r0,#24`. It keeps the return instruction and every other byte unchanged.
The24-cell bound includes the23-character maximum and its paired blank cell;
it does not shorten,scale or change the names. The four-bit SDK clears a spare
terminal halfcell for odd text,as documented in the earlier V340 source/font work.
Putting that cell inside the declared field avoids relying on undeclared backing padding.

Parent research ARM9:
`44f4e07420034aad87d837bf9b5be4066ac5bdeec5f2dea2b8141d8e5be4f6c8`.
Corrected research ARM9:
`23fb7c8ffb3055b71c1d41b41756ad1b0b0903c25e3854ca27306cdfe218d6f7`.
No section,BSS,pool,cache,startup,arena or123040-byte staged payload grows.
The getter is not shared by another class; other object types are byte-exact.

## Original native paths tested

- The source object resolver020211E4 handles encoded scheme IDs through its
  original CB130 pool. The CPU fixture changes only a source slot's type byte;
  no real letter,quest or save is created.
- The original4F500 constructor initializes the outer widget and its child.
  The tested row callback uses the correct child at outer+10 and its original
  vtable8C entry4F8D4. The default4FB38 path calls the original name getter and
  D5404 font renderer. No invented vtable or replacement glyph renderer is used.
- Six original sizing-prefix cases cover old/new widths and counts1,10,11.
  The original ten-row cap remains. Corrected outer rectangles stay within
  256×192;content width is144. The original inner-rectangle arithmetic fragment
  uses that same width. SDK window allocation is deliberately outside this proof.
- Forty complete native bitmap cases cover all ten names at heights12 and16.
  Every corrected row matches the independent font,including first/last letters
  and the empty terminal cell. Bitmap/header/view guards pass. The old60-pixel
  field truncates the six proposed names and earlier Forge Papers in these CPU tests.
- Ten width-getter cases preserve the complete8MiB memory and callee-saved ABI.

This does not establish actual GUI allocation,palette/compositing,full menu
playback,earned letters or every possible runtime control flow.

## Mode and backing-surface diagnostics

The first probe reused a dialogue test's wrap flag1. Source4FC70 creates the
list context through D5160,which initializes wrap0,and then invokes virtual8C
without changing that flag. The final tests use that exact single-line setup.
The wrong-mode result is retained separately;it is not a shipped23-cell game defect.

Separately,a controlled23-cell view backed by a tightly sized140-pixel bitmap
consumes all23 bytes but loses13 ink pixels from the first `p` of the next
bitmap row. The paired terminal clear crosses the tight pitch. The corrected
24-cell/144-pixel field preserves the entire plane. This is a native backing-
surface sensitivity test,not a claim about a captured GPU menu's allocator.
It demonstrates why byte counts alone do not prove complete leading letters.

The final comparison sheet shows proposed English in the old-width CPU field
beside the corrected native rows. Its left column is not a set of historical
ROM screenshots. All ten corrected rows are visually reviewed.

## Constructor entry scope

The clean/current census finds six original constructor edges and no additional
absolute,ARM/ADR or Thumb reference lead to these three selector entrypoints.
Four external caller fragments explicitly set width override0;two original
wrappers forward it unchanged. Thus the ordinary discovered static entries use
automatic class width. Native source fragments and stack parameters are recorded,
not merely inferred from a call graph. This is ordinary static-entry closure,
not a proof against every imaginable indirect jump or corrupted program state.

## Preservation and remaining work

Restoring the one instruction reproduces the complete V786 research ARM9.
All3668 current COMMON maps,texts and copy extents stay exact. The user's
repaired676/677 reproduce their exact native wrapping;V747 remains their actual
shop-scene reference. Existing V783 ROM/patch,canonical,clean input,donors and
frozen release dependencies remain exact. No new guide screenshot,commit or push.

Full SDK window construction and actual selector/GPU crops remain to verify in
the registered candidate. The full native initializer reached an unmodeled
allocation/copy dependency;no heap or GPU stub was introduced to claim success.
The live CPU test preserves captured storage and applies only declared guarded
deltas,instead of reloading staging data over the live snapshot.

Continue other name consumers and Guild diplomacy eligibility/argument mapping,
then production routing,COMMON reblocking/copies,registered full-stack integration,
exact clean-input patch and actual revised buy/sell/bargain/diplomacy scenes plus
startup. Then1146 onward,750–752,all routes and remaining prose. The original18
plaques,Online-body exclusion,preserved brown marks,locked character names and
older-record follow-up remain unchanged in the separate unfinished graphics audit.

## Evidence

`work/analysis/scheme_name_width_v787/native_width_verification.json` and
`selector_entry_closure.json` carry the source/code/input contracts.
`odd_pitch_diagnostic.json` records every missing ink coordinate.
`old_and_corrected_name_rows_3x.png` is the reviewed native CPU comparison.
Reproduce with research_scheme_name_width_v787.py,
verify_scheme_selector_entries_v787.py and record_scheme_name_width_v787.py.
Current evidence and producers are archived with SHA-256 receipts at
`E:/Rota Nova translations/Editorial review/V787 Shared letter-name width research`.
