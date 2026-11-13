# V729: remaining image-instruction modes

The active queue continues from the existing graphics goal. Completed scopes
remain outside that queue, with their evidence retained. This checkpoint closes
one additional source-path lead; it does not close the original comic viewer.

## What was verified

`scripts/verify_image_modes_v729.py` executes the original image instruction
dispatcher, descriptor decoder and existing-child cleanup for all 256 indices
in modes 0, 1 and 2, in both four-byte and eight-byte instruction forms:
1,536 cases. Every executed instruction matches the registered current code;
the dispatcher, selector, cleanup and constructor source ranges are also exact
to the clean ROM. Operands, decoded lengths and neighboring guards pass.

- Modes 1 and 2: all 1,024 cases reach the common wait boundary with no child.
- Mode 0, indices 0–217: all 436 cases reach the original constructor at
  `0204A930`, with arguments `(widget+84, index, 101, 0)`.
- Mode 0, indices 218–255: all 76 cases return with no child.

Source calls identify mode 0 as an item-information window: its constructor
calls formatter `0204E3F0`, which uses the item-store getter `020CB190`, plus
item resource helper `020477B8`. The final tests stop before the constructor;
they do not establish its complete loading or display. No loose image loader
or SDK file call executes in the tested selector/cleanup scopes. Mode 3 already
has V538 and current V724 evidence and was not repeated.

## Inputs and limits

The diagnostic instruction streams are supplied inputs. The starting 4 MiB RAM
snapshot comes from frame 3900 of the declared V724 index12 research-command
fixture, not an ordinary event reached through gameplay. Its original capture
report, fixture ROM hash and RAM hash are verified. This is a standalone native
selector test, not a new emulator framebuffer capture, playthrough, full CPU
replay, return-ABI test, or proof of ordinary scene reachability.

An exploratory continuation of the item constructor reached an unmapped fetch
at `E5802000` after its item-store getter in the incomplete standalone model.
That continuation receives no constructor/display credit and establishes no ROM
defect. The report-schema lookup was corrected from the final-RAM object to the
per-frame RAM list before the successful final run.

This closes searching these three selector modes for a hidden comic-image
selector. It does not prove global non-use of raw art or rule out other loading
paths, generated scripts, flags, geometry, palette import or ordinary parents.
Those remaining requirements stay in the active queue.

## Integration and audit

V712 ROM, manifest, patch, release registry and canonical baseline remain
unchanged. The original 18 overall plaque objects remain incomplete, and the
22 historical requirement objects are preserved. Previously completed material,
base displays, source classifications and targeted native checks carry forward.
The four low-resolution Online bodies remain excluded; approved brown marks
remain preserved. The full graphics goal stays active.

Evidence: `work/analysis/image_modes_v729/proof.json`, `cases.json` and
`executed_source.json`. Checked copies are stored on E under
`Rota Nova translations/Screenshots/Audit comparisons/V729 Image instruction modes`.
These are test records, not new guide screenshots or publication-approved art.

After completion of the graphics goal, revisit the older record-based checks
as requested.
