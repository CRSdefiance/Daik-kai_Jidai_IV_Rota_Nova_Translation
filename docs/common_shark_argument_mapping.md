# Shark damage report argument

Clean COMMON global messages 2331–2336 describe a shark tearing `%s` apart.
The argument refers to a figurehead item. This is static source classification;
actual displayed names and expanded wrapping still require a runtime sample.

Evidence from the source-locked clean ARM9, not a translated candidate:

- The six message IDs are in the voice table at ARM9 file offset `0x116C80`
  (runtime address `0x02116C80`), with one `FFFFFFFF` voice slot.
- The literal at file offset `0x74064` references this table. The shark branch
  calls `0x02055D0C` at `0x02073938`, takes the nonzero returned object in `r5`,
  calls its virtual method at vtable offset `8`, and passes that result in `r2`
  to dialogue formatter `0x02053F0C` at `0x02073970`.
- `0x02055D0C` gets the ship's object through `0x020AB158`, reads byte `0x4B`
  via `0x020A4B60`, then uses `0x0204A624` to map slots 0–9 to item indices
  `0x72`–`0x7B` (114–123). The default is `0xDB`; default and index `0x79`
  return null and suppress this report.
- The returned object is `0x022D322C + 4 + item_index * 0x14`, the item table
  returned by `0x020CB190`. The function applies item operation `6`
  through `0x02049F30` before returning this item object.
- Independently source-locked COMMON item descriptions 114–123 all describe
  figureheads: eagle, three pigs, orca, white whale, dragon, dolphins, maiden,
  devil, king and Virgin Mary. These descriptions corroborate the item range.

The nearby `0x0207403C` virtual name call belongs to a different report and must
not be used as the shark call's argument evidence. Losing cargo or a person's
limb was an unproven inference. New messages 2334/2335 use “torn to pieces,”
retaining the actual item-name substitution and the admiral's alarm where present.
