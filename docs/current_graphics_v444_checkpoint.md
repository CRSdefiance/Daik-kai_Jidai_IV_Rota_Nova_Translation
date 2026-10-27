# Current graphics inventory and consumer leads V444

Previous goal turn: progress (V443 whole Guild repair, actual capture, exact patch
and E-drive publication). This turn: source/current inventory and consumer evidence.
No ROM or translated artwork changed; V443 remains experimental.

## Current inventory

The complete clean/current comparison covers 660 PXL files and 261 FLS textures,
including 42 direct-colour PXL images. All921 original format/flags, palettes,
dimensions and pixel-payload extents pass. All84 previously changed graphics
entries remain. The audit's candidate and preservation references now name V443
and `work/analysis/current_graphics_v444/preservation_proof.json`.

This verifies source preservation, not text accuracy, borders, final crops, alpha
or every gameplay display. No full completion claim is made.

## Three file-open leads

- SDK call `020B7178` belongs to PXL staging entry `020B7158`; its two direct
  parents construct event and town filenames. All300 current files match the
  original native loading evidence from V385.
- SDK call `020D0474` is disk mode0 in general wrapper `020D0398`. The caller's
  filename is preserved in r4 and passed to SDK open. Eleven direct main-code
  callers are recorded, including resource cache, CMMN archive, TITLEMAP and font
  readers. Deeper argument paths and indirect consumers remain to trace.
- SDK call `02100348` belongs to FLS reader `02100310`, reached through FDED0.
  All15 original full-stream native traces execute this exact call. Current movie
  files and reader code match that evidence byte for byte.

Selected code ranges also match clean source. These are current bindings to
bounded prior native tests, not new gameplay captures or proof that raw archives
are unused. Evidence: `work/analysis/legacy_review_v444/consumer_leads_proof.json`;
script: `scripts/audit_graphics_consumer_leads_v444.py`.

## Comic and remaining displays

SLACK block19 frame6 was extracted directly and visually inspected, including a
magnified analysis crop. Its brown marks resemble handwritten marks but do not
provide a confirmed reading. They remain original; neither their interpretation
nor the actual comic display gate is cleared. The analysis crop is not a finalized
guide screenshot.

All22 historical requirements and all18 incomplete plaque entries remain under
audit. No low-resolution Online translation is requested. Normal battery saves
near endings, Japan/Korea or occupied Weapon/Armor would permit stronger actual
display evidence; an optional user request is pending. Independent consumer work
can continue without those saves. Revisit older record-based checks at actual
full-goal completion.
