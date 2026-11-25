# Current comic artwork review

Previous goal turn: progress, recording the user's approved preservation of the
brown marks. This turn reviews the actual V502 raw comic bytes and searches for
possible display copies. V502 is unchanged and the graphics goal remains active.

## Source and English review

All 21 source/current frames in SLACKIMG block 19 were decoded and reviewed at
their inspected 320×240 storage dimensions. All 18 current caption records
reproduce exactly from the source-locked batch. Checks cover 331 visible English
characters, with 36 first/final-letter erasure cases. Every frame preserves all
unowned source words and all original high color bits; all 11 untouched frames
are byte-identical to source.

The chase dialogue, reaction, reveal, creature dialogue, recruitment credits,
Maria headings and speech, closing thanks and game title retain their reviewed
English. No additional dialogue was found in this full-frame inspection.
Original attribution marks remain under the V179/V180 retention decisions.
The two brown marks remain unchanged under the user's V505 preservation decision.
Source restoration underneath removed lettering is still approximate where
declared; these checks do not prove recovery of hidden original scenery.

## Display-copy search

All 921 original PXL/FLS images were ranked against all 21 raw frames using
32×24 BOX-filtered whole-image RGB distance. The search generated the four
closest leads per frame. The inspected recruitment, Maria speech and closing
portrait leads are unrelated images, not identified comic counterparts.
This method has not identified a display copy. It cannot exclude atlas crops,
composition, alpha variants or other formats and is not proof that the raw
comic is unused. No consumer or viewport was substituted for a gameplay test.

## Evidence and remaining work

- `work/analysis/comic_current_v506/proof.json`: current saved caption pixels.
- `work/analysis/comic_current_v506/all_frames_manifest.json`: complete frames,
  hashes, unowned words and color flags.
- Six labelled source/current sheets in the same folder.
- `work/analysis/comic_current_v506/copy_leads.json`: original-image search scope.
- `scripts/review_comic_frames_v506.py` and
  `scripts/find_comic_display_copies_v506.py`: reproducible source review/search.

Both new scripts pass Ruff. No production graphics, ROM or patch changed.
Actual comic loading, consumer geometry, crops, native readability/gameplay and
declared source-restoration gates remain open. All 22 historical requirements
and all 18 incomplete plaque entries remain in the audit. These decoded images
are diagnostic previews, not finalized guide screenshots.
