# Environmental retain decisions: native consumers V206

2026-10-07. The previous goal turn localized the clear Online Julien label and
expanded primary-source research. This turn verifies native consumers for the six
previously retained environmental resources. **No ROM, artwork, patch or runtime
code changes. V205 remains the latest registered candidate; goal active.**

## Tavern lantern and Inn plaque

The unchanged native selector at `020B7F68–020B7F84` chooses one of two facility
sprite tables, then indexes a 28-byte record using the supplied facility ID. The
actual resource initializer creates the owner objects; filenames are read from
their real initialized fields, not inferred from adjacent literal-pool words.

| Retained resource | Facility ID | Actual alternate-table owner | Declared image extent | Parent local origin |
|---|---:|---|---|---|
| `/_pxl/kbj04.pxl` | 4 | `02313D6C` | 40×44 | (50,0) |
| `/_pxl/kbj08.pxl` | 8 | `02313D30` | 50×44 | (0,48) |

The exact native caption getter at `020B8220` indexes its independent text table
with the same facility ID. Actual clean/current execution returns:

- ID 4: **酒場 → Tavern**.
- ID 8: **宿屋 → Inn**.

All 12 clean Japanese and 12 initialized English caption selections return
completely with the saved-register/stack ABI preserved. This confirms that the
retained wine/alcohol lantern is a Tavern icon and the tiny plaque is an Inn icon.
The plaque does not justify inventing a readable inn name. Both facility captions
already have English text, independently of the painted sign.

Both selector branches execute for IDs 4/8. Their four actual selected owners
(`kbe04`, `kbj04`, `kbe08`, `kbj08`) resolve through real native view construction
and the image cache/loader. Every complete header, palette and pixel payload equals
its ROM file; source extents match table metadata, view canaries remain intact and
all SDK handles close. A full town UI constructor is not substituted or claimed.

## Four town backgrounds

The native reader at `020B7260` receives an image target and numeric index. It calls
the original formatter with `/towngrp/towngrp%02u.pxl`, opens that actual filename,
reads the exact file into its real shared scratch literal `02233040`, and copies
the complete native palette and packed pixels into a matching target image header.

Indices **32, 33, 35 and 37** all execute that complete formatter/reader/copy path.
Every resulting file/header/palette/pixel byte is exact to clean and V205; all target
and scratch canaries and saved-register/stack checks pass. The native code matches
clean. This supplies filename/geometry/loading/copy evidence for the retained
town paintings, rather than a guessed city assignment from architectural style.

## Scope and retain conclusions

Only SDK filesystem open/read/close operations are bridged to the exact ROM's
resources. Caption selection, icon-table selection, resource registry, native view
and cache loading, dynamic filename formatting and whole palette/pixel copies
execute unchanged ARM instructions. Four town-copy inputs and preceding icon
selector arguments/target buffers are explicit fixtures.

Keep all six original resources. The Tavern's 酒 and the Inn's indistinct plaque
are physical architectural/icon decoration with separate English facility captions.
Town32/33/35/37 retain their previously reviewed painted architectural marks; exact
readings/shop names are not invented. All source bytes, palettes and dimensions
remain untouched. This does not establish every actual city assignment, alternate
palette/alpha state, parent UI composition, GPU crop, input or gameplay usage.
Those gates remain open; the boolean native-consumer follow-up is scoped accordingly.

Evidence: `work/analysis/contextual_environment_v206/native_environment_proof.json`.
Implementation: `scripts/verify_contextual_environment_native_v206.py`, focused
Ruff passing. The existing full-source/enlargement reviews remain recorded in
`translations/contextual_graphics_decisions_v177.json`.

The full objective still includes four unfinished Online screenshot bodies/chat,
remaining names/text/caption/biography integration, legacy/archive relationships,
broader native/gameplay checks and one complete combined release/patch. No goal
completion or user acceptance is implied. Revisit older record-based checks at
eventual completion as requested.
