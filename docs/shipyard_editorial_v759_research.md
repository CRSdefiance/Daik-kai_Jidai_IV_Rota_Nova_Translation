# V759 research: faithful shipyard dialogue and typed quantities

This is research, not a ROM candidate. V758 remains the latest registered combined
ROM. Completed editorial coverage remains128 entries (92 revised,36 retained).
Source/prose coverage is now152 entries, including24 active drafts: three unmapped
750-752 and21 Shipyard entries784-804. The full editorial goal and the separate
graphics audit remain unfinished.

## Meaning and natural English

The clean source establishes a five-ship fleet limit, exact design-copy purchase,
mast/durability statistics, dock custody, sale selection/price confirmation,
repair eligibility/cost, seven volunteer voices, a qualified-helper repair
discount, a one-day repair wait, and copy preparation/purchase confirmation.
788 and789 are independent selections. Old English incorrectly ended788 with
`Which ship will you` and began789 with `sell?`. Old796-798 contained unrelated
trade/service-price fragments. These defects are restored in the new drafts.

Source792's IC is a first-person pronoun, not a name. Both Japanese alternatives
become I. The source/native proof preserves this distinction and the seven voice
registers without inventing age, family relationships or character assignments.
787,790 and801 retain their natural wording. The remaining18 receive prose or
quantity-grammar revisions.803 now reads:

> A ship just like %s? It'll cost %s and take %s to prepare. Buy it?

The arguments are respectively the literal ship name, the complete typed price,
and the complete preparation duration. `Just like` conveys the same specifications
as the selected ship in the original design-copy context. English is authored as
one logical paragraph, without alignment spaces or manual line breaks.

## Native source context

`native_context.json` binds clean/current original callers, all eight voice-table
slots (including native fallback), eleven copy/discount fragments per build, and
160 abstract preparation-getter contracts per build. Those preparation contracts
span0-16; they do not establish that every abstract combination is an earned or
legal ship design. Original number formatting returns CP932 full-width digits,
not narrow ASCII. Price1 and preparation1 therefore remain required grammar cases
until stronger source bounds prove otherwise.

The original portrait pipeline runs printf before its macro parser. Initialized
V758 company RAM demonstrates FALCON becoming BergstromLCON, FIONA becoming
HodramONA, FORTUNE becoming Bergstrom FleetRTUNE, and FURY expanding the captain's
full name. ICARUS becomes a Japanese first-person pronoun plus ARUS when the actor
property is supplied. This is a native parser contract demonstration, not a claim
that those names were entered or that a full Shipyard scene was activated.

## Prototype and evidence

All new executable code exists only in disposable Unicorn scratch at02460000 and
above. No such address is approved ROM storage. No ROM, registered profile,
release config or patch is produced.

- A typed-number adapter recognizes exactly six original price-call return PCs
  and the copy-preparation return PC. It calls unmodified ABF50, retains every
  full-width digit, and appends `gold coin`/`gold coins` or `day`/`days` inside the
  original128-byte number buffer.105 typed cases and15 unknown-caller fallbacks
  pass.77 paired whole4MiB RAM comparisons prove equality outside that original
  buffer, with unchanged return ABI.24 original copy-argument fragments execute
  the actual numeric calls through the adapter; only the preparation result and
  virtual ship-name getter are explicitly supplied. They prove original argument
  order and zero/positive preparation selection, not a completed purchase.
- Literal copying and bounded balancing are selected only for the reviewed direct
  and Yes/No message IDs, or the two original queued parents with voice table
  02118460. Queued stack+274 holds a saved return address rather than a message ID;
  selection correctly uses the table. All36680 parent/ID/table membership cases
  pass. Other source macros retain their original parser path.
- Balancing tries independent first/continuation widths: first36 down to16 and
  continuation35 down to16, then the existing bounded fallback. The search has at
  most420 width pairs plus one fallback. A scoped first-width adapter preserves
  the existing helper's older width encodings.180 complete inherited native
  outputs and return-ABI controls remain exact; wider release regression remains
  required after actual integration.
- All1124 supplied price/mast/durability/name/preparation cases preserve complete
  words, guarded buffers and return ABI, fit four35-cell rows, and have no weak
  line ending or short final-row finding. Supplied extremes include signed-int
  maximum prices, single/plural quantities and23-byte compact/spaced names.
  These are stress contracts, not proof of every editable-name limit or reachable
  amount. Argument provenance distinguishes the proper name A, including A inside
  a spaced name, from the English article a.
- All68 complete228x64 native font planes equal independent ASCII and KANJI font
  rasters, including every first/final glyph, colour index, shadow, row and blank
  pixel. All six contact sheets were visually reviewed. The independent KANJI
  model initially omitted the original style1 (1,1) colour15 shadow; the corrected
  comparison accounts for it. This was a host-model error, not a ROM font defect.

The previous research attempts remain archived: the first uniform/min24 prototype
had415 findings; min16 and improved natural803 wording left14 findings, including
proper-name false positives. Independent first/continuation widths and provenance
resolve those findings. No failed attempt is counted as final verification.

## Open integration gates

`translations/shipyard_editorial_manuscript_v2.json` carries all21 source/context/
localization/naturalness approvals. Its formatting release gates remain false:
native scratch-code evidence cannot authorize an unowned executable location or
prove real loading/display. Preserve v1 as the earlier pending-grammar draft.

Next establish owned immutable storage for the prototype, with all pointer,
packed-descriptor, branch and runtime-write owners mapped. Preserve the existing
123040-byte late-copy payload, cache/startup/allocator contracts and graphics.
The bounded fixed-record padding scan records23 leads only; zero/space padding
does not prove that any of them is reusable. No padding was overwritten.

Then integrate all21 through the registered builder, verify every native message
copy and all unselected bytes, construct the exact clean-input patch, and exercise
original Yard sale/repair/helper/copy scenes in cold-boot gameplay with protected
saves and disclosed fixtures. Confirm actual editable ship-name limits and the
command-like-name cases there. Update progress after those gates pass.750-752,
wider shared prose, Lil/all routes, remaining player-facing prose, and the original
graphics audit remain open.

Research and native previews are archived under
`E:/Rota Nova translations/Editorial review/V759 Shipyard research`.
They are not gameplay screenshots or finalized guide images. No canonical
promotion, save modification, commit or push occurs at this checkpoint.
