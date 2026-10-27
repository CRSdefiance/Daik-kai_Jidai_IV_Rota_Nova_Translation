# Native and compact label glyph review V227

This turn verifies complete glyphs in the actual V218 image pixels, rather than
inferring text correctness from a successful build. **V218 is unchanged; the full
graphics goal remains active.**

## All 57 graphic labels checked

The scope is the seventeen registered native-PXL-label batches:

- 48 labels use the original ROM ASCII font, including two labels with reviewed
  ink-based spacing.
- Nine use the source-locked compact bitmap faces: controls, date markers and
  male/female symbols.
- Health/mood/level/HP, crew assignment, name-entry fields, treasure/fleet headings,
  village captions, score labels and action buttons are included.

Every source glyph's complete foreground mask is checked against the actual
candidate pixels. Blank cells in the complete text extent are checked too, detecting
old Japanese remnants or overlapping foreground. All **24,864 foreground/blank
pixels** pass. Every leading/trailing letter, symbol and punctuation mark is present.
Every glyph's ink remains within the declared draw box.

Native top-row trimming is checked to remove no source ink. Fixed-width and compact
layouts preserve complete source glyphs; ink-based spacing removes only blank
bearings. The source font comes from the current candidate and is hash-pinned.

## Visual and English review

All 57 tight text previews were inspected at their source bitmap scale. The controls
and headings read as normal English UI labels; village names and developed variants
are complete. Press-a-button wording, date M/D and gender symbols remain intact.
No clipped first/last glyph or extra old-label foreground was found in the checked
text extents.

The first contact sheet included large source background boxes, causing previews
to overlap. The sheet is corrected to show tight text extents; that display issue
was in the review artifact, not in the ROM. It is not counted as a game fix.

## Limits

This verifies stored bitmap glyphs and label extents. It does not establish every
native consumer's crop, physical alpha/color composition, input or gameplay display.
Those gates remain separately scoped. Indexed title artwork, compressed subtitle
art, promotional screenshot bodies and embedded raw copies have their own evidence;
none is silently included in the 57-label claim.

## Evidence

- `scripts/audit_label_glyphs_v227.py`, focused Ruff passing.
- `work/analysis/label_glyphs_v227/glyph_proof.json`: every label, glyph origin/ink,
  source font hash, full bitmap comparison and reviewed-preview hash.
- `all57_labels.png` and 57 tight source-size crops.

No image or ROM changes. The registered V218 and its exact patch remain current.
Four screenshot body/chat translations still require readable source; remaining
embedded/contextual/native display, confirmed-name consistency and final whole-
scope gameplay verification remain open. Older record-based checks remain to
revisit after full goal completion.
