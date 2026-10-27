# V589: village-card dispatch and omitted container coverage

Production remains experimental V581. This checkpoint changes no ROM, patch,
artwork, translation, save or release profile. It extends V427's route-only
reference search and distinguishes two original image command paths. It supplies
no new emulator screenshot, ordinary village trigger or guide evidence.

## Correct asset identities

The eight localized village-card files are **evstill168, 169, 170, 171, 206, 207,
208 and 209**. They are not a consecutive 200-207 group. V549 already verifies
their complete translated planes and native GPU display in supplied scene
fixtures. Ordinary event context remains open.

## Exhaustive original operand decoder

The complete original dispatcher at0202A510 executes to its actual parent call
for every16-bit operand of instruction4620, separately on clean and V581 code:
131,072 native cases. The relevant dispatch/parent/loader code ranges are exact
between the ROMs; the argument digests match.

- Bit15 set:32,768 operands select02028AA8. The event-still index is the low8
  bits. Higher operand bits do not make that index a variable lookup. This parent
  calls02028B74, which formats `/evstill/evstill%03u.pxl`.
- Bit15 clear:32,768 operands select02028BAC, with arguments `(operand>>8)&127`
  and `operand&255`. Its original020B7128 path resolves a town image through
  020B7294 and020B7260. The actual filename format is
  `/towngrp/towngrp%02u.pxl`; this is not a second village-card selector.
- All cases retain instruction length4, original global parent02276F88 and
  options `(2,0,0)`. Input streams and owner/result neighbor guards remain exact.

These supplied-input replays stop at the real parent call before file loading,
transitions or drawing. They do not add GPU or ordinary event reachability
credit. V427's separate auxiliary-flag checks and V549's scene captures remain
their own evidence.

## Original caller census

All loaded ARM9 main sections and declared overlays are checked for aligned ARM
B/BL, Thumb BL/BLX and stored absolute/odd pointers at every byte position:

| Target | Direct ARM calls |
| --- | --- |
|02028B74 event-still formatter/loader |02028AF8,02028B0C,02042F6C |
|02028AA8 event-still parent |02029FB4 |
|02028BAC town-image parent |02021BB8,02029FD0 |

Clean and V581 yield the same targets, all unconditional linked calls. No Thumb
or stored-pointer candidate occurs for these three targets. The extra02021BB8
town-parent call consumes fields from its supplied state record; it does not
call the event-still formatter. The Gallery tables already exclude these eight
cards under V426.

Computed/relative/indexed call targets, numeric file-ID readers, generated
instruction streams and other filename construction remain unproven. This
census cannot establish global unused art.

## Expanded source search

Twenty containers per ROM,40 total, are searched at every byte position,
including odd offsets. This includes both `/COMMON` archives, both sets of
four SC archives under `/data` and `/testdata`, both sets of four VE event files,
DECKCHIP and WORLDMAP. ILNK blocks are searched whole; VE files are searched
whole including their headers. VE files are not treated as ILNK.

There are no village-card event-still byte patterns in any shared, route, event,
test-data or DECKCHIP container. Sixteen matches occur in WORLDMAP in each ROM;
that entire file is source-exact. Those are byte candidates within map data,
not decoded script instructions or proven event triggers. The proof retains
all locations rather than treating positive pattern matches as execution.
All eight test-data SC/EV containers also remain exact to clean source.

This closes the omitted-container gap in V427 and rules out the alternate
town-image command as an event-still selector. Repeating that alternate-form
search is not the next useful step. Normal village-card usage still needs a
computed/generated or separate-reader path; it is not closed by this result.

## Evidence and preservation

- `scripts/trace_village_dispatch_v589.py`.
- `work/analysis/village_dispatch_v589/dispatch_proof.json`, with ROM/script/code
  hashes, complete caller census, decoder digests and all container hashes/counts.
- `scripts/record_village_dispatch_v589.py` archives the proof and scripts under
  `E:/Rota Nova translations/Screenshots/Test fixtures/V589 Village dispatch`.

The current patch and ROM are hash-checked unchanged. All18 original plaque/hint
entries remain incomplete; all22 historical requirement objects retain their
exact scope. No source fragment is reinterpreted or erased. The graphics goal
remains active and incomplete, including the broader material, legacy, comic
and movie-context gates. Older record-based checks remain a follow-up at full
completion.
