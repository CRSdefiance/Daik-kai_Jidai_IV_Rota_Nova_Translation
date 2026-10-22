# Ordinary Market transactions and heading graphics V598

Evidence checkpoint on unchanged experimental V593. This run uses ordinary
controls from a fresh New Game, with no battery save, savestate, research ROM,
unlock, inventory change or live RAM fixture. It ends normally at24100 frames.

## Actual transaction path

The successful older Market input prefix is replayed on the current ROM. It
arrives in Deal with two ordinary Salt purchases already staged: funds30000,
spent1144, net28856. Further A presses on the selected Local goods do not add
another hold in that observed state; they are not counted as extra purchases.

UP selects a Cargo hold. A removes one staged purchase, reducing spent to572
and restoring Local Salt stock from3 to4. X Finish opens the Sailor's confirmation;
A accepts, and the Trader acknowledges. Returning to Market and reopening Trade
shows funds29428 with income/spent both zero: one572 purchase has committed.

A on the owned Salt stages its sale. It moves to Sold and shows income288,
spent0, net29716. X then B No returns the entire98,304-pixel Deal framebuffer
exactly to its preceding state. A later X/A confirmation commits the sale.
After the normal Trader/Market return and reentry, funds29716 are shown with
income/spent reset to zero. The Sold section retains that Salt entry. This is
observed purchase/sale and return behavior, not an exhaustive trading-system test.

## Source meaning and actual graphics

The original captions are 売却品, 特産品 and 積み荷. Current **Sold**, **Local**
and **Cargo** are retained. Sold denotes goods sold to the port, Local its
specialty-goods section, and Cargo the ship's goods. It is not an inferred
Sold Out message. The source images and actual post-sale context support these
compact section labels.

All three headings use the original marker helper's sourceX112, rows0/16/32,
size32x16, palette0 and flags0. Nine actual Deal states verify27 complete crops:
all13,824 pixels match the current source atlas. Original getter020D4170 resolves
that entire resident PXL byte for byte from each real view, without supplied
resource/file binding. Original text layout independently verifies all188 English
ink points, including full first/final letters inside the native32-pixel width.

All72 complete HUD word/number masks pass, including foreground and blank cells.
Original native stock getters read the actual CTradingView/model link; the five
goods IDs and quantities agree with the observed stock changes. Those queries
leave the complete model unchanged. The read-only type metadata and relative
view fields distinguish the real object from a vtable value stored in code/data.

## Material review and retained limits

Native and enlarged nearest-neighbor original/current crops were reviewed. Both
use the original dark, horizontally banded wood and framing. This comparison
does not recover material hidden by Japanese strokes or close the global texture
audit. A tentative shared-background reconstruction across these three source
cells has17 visible conflicts under its provisional masks; they are not treated
as identical unlettered donors and no artwork is rebuilt from that assumption.

The separate32x12 Sell/Buy atlas cells at rows48/60 are not these three headings.
No literal marker view in the earlier88-reference census explains their ordinary
parent, and the original dynamic-row helper's three direct callers select
rows32/16/0. This is bounded caller evidence, not global nonuse or permission to
remove those graphics. Their ordinary parents remain open. All18 original
plaque/hint entries and all22 historical requirement objects retain exact scope.

## Evidence and preservation

- `scripts/verify_market_transactions_v598.py`.
- `work/analysis/trade_consumers_v598/ordinary_trade_proof.json`.
- `final_recorded_inputs.json` in that directory reproduces this ordinary path.
- Native report, screenshots and read-only pause RAM are on E under
  Generated/work/emulation_v193/trade_consumers_v598.
- Ten unmodified fullscreens and provenance are under Screenshots/Guide candidates/
  V598 Market transactions. They are candidates only; publication is not approved.
- Source/current material comparison and proofs are under Screenshots/
  Audit comparisons/V598 Market headings.

No ROM, patch, graphics, source asset or canonical baseline changed. V593 SHA256
remains `d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642`.
The graphics goal remains active; this is not a full route or physical-device test.
