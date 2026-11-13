# Purchase reference review

Recorded 2026-10-12. [Dekuno purchase article](https://dekunobou-rotanova.seesaa.net/article/29158147.html), retrieved that date. The first 24 selected entries use the project's existing English item names. Prices independently match the read-only static item export's base-value field.

`build_purchase_reference.py` rejects unknown item names and price mismatches, exports `ds-purchase-reference.json`, and builds section 12.4. Agreement establishes the listed/base price, not live shop stock, a tested transaction, or every protagonist's event-dependent availability. The source names towns rather than exact menu facilities; no unseen purchase interaction is certified.

Remaining coverage includes other listed purchases, dynamic quest stock, gift-recipient/event prerequisites, all discovery conditions, event-only acquisitions, and 10 additional DS treasures. This is progress toward the full acquisition requirement, not its completion. ROM/save/screenshot files are unchanged.

## Complete source-table coverage, 2026-10-12

Rechecked the [DS shop article](https://dekunobou-rotanova.seesaa.net/article/29158147.html). All 48 item rows are now represented with existing English catalog names. Each listed price matches the native base-value export. This verifies source transcription and catalog agreement, not live stock or every event gate. The generator now preserves sections 12.5 onward when rebuilding purchases.
