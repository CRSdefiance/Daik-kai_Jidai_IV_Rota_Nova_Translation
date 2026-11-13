# V588: complete original SLACK portrait caller loop

Production remains experimental V581, unchanged. The previous turn made progress
by binding raw-frame reads/copies and the actual fixed-canvas loader contract.
This batch executes the complete known SLACK caller loop, including the metadata
calls omitted from the earlier per-portrait fragments.

## Source and current parent

The ordinary V581 New Game capture at frame2000 from V582 provides genuine
parent/global RAM. The report and4 MiB snapshot hashes are verified; this source
has no battery save, savestate, inventory or other synthetic state fixture.
The unique indexed8,52-word,136-row descriptor is02192E34, in parent02192500.

Original code0209ED3C-0209EE94 is exact clean source. Execution starts with its
own counter-zero assignment and native synthetic-header setup. It derives width,
height, loop indexes and selected archive blocks itself. The actual parent,
captured globals and a scratch stack are replay inputs. No metadata result,
archive selector, view constructor or virtual method is stubbed.

Only SDK filesystem operations are bridged to exact current ROM files. The
original wrapper, ILNK header/block parser and original portrait-view routines
execute. The replay stops at the loop's original end; it is not a complete UI
constructor, an observed live instruction trace or a new emulator playthrough.

## Complete four-iteration result

The native counter runs0,1,2,3 and exits at4. The sole observed archive request
per iteration is `(14+counter,02233040,offset0,length0)`. As established in V587,
zero length requests the whole selected block. All four14144-byte source blocks
14/15/16/17 load exactly, with all original handles closed.

The real preceding metadata virtual calls execute as well:

| Iteration | Actual character record | Native method | Output |
| --- | --- | --- | --- |
|0|022D5D24|020CD6CC|02192E84|
|1|022D4364|020CD998|02192E84|
|2|022D4384|020CD998|02192E84|
|3|022D43A4|020CD998|02192E84|

This closes a gap in V202's per-index fragment: those tests began after the
metadata call and supplied the index separately. The whole-loop replay retains
the original calls, counter updates, back edge and stopping condition.

Every one of the four44-byte persistent portrait views exactly matches the
actual captured parent. They name `personbustup00.pxl` through
`personbustup03.pxl`, with104x136 extents. The full20-byte synthetic header is
also reproduced exactly. This constructs four views; it supplies no new Maria
visibility/unlock claim, palette interpretation or GPU display credit.

The memory observer covers the entire loop, including all four metadata methods,
archive calls and view construction. It sees zero ARM reads from the14144-byte
raw-buffer span. It also sees no writes to ARM9 DMA setup registers during the
loop. Verifier/SDK-bridge host reads are not miscounted as native ARM reads.
Hardware async activity and consumers after/outside this loop are not simulated.

Thus this known caller reads only portrait blocks14-17, and those raw bytes do
not supply its constructed PXL views in the tested replay. It does not select
comic block19. The claim does not extend to other execution contexts or readers.

## Caller census and limits

All current loaded ARM9 main sections and declared overlays are scanned for:

- Direct aligned ARM B/BL targets, including tail-branch candidates.
- Thumb BL/BLX candidates.
- Stored absolute wrapper pointers at every byte alignment, including odd values.

The only direct candidate for0204704C is original0209EDE8. There are no Thumb or
stored-pointer candidates in this census. This extends the old aligned-call
inventory; it is not whole-program reachability. Computed targets, relative/indexed
tables, numeric file-ID readers, other SDK interfaces and later consumers remain
open. Do not convert the bounded result into a global unused-art assertion.

The next useful investigation is a distinct raw/direct-color descriptor or other
reader path. Repeating the proven portrait loop or forcing raw16 art through the
fixed indexed event-still canvas does not establish comic scene availability.

## Evidence and preservation

- `scripts/trace_slack_caller_loop_v588.py`.
- `work/analysis/slack_caller_loop_v588/original_loop_proof.json`, including the
  complete current executable-unit hashes, exact I/O and virtual targets.
- `scripts/record_slack_caller_loop_v588.py` archives proofs/source provenance
  under `E:/Rota Nova translations/Screenshots/Test fixtures/V588 Original SLACK caller`.

The existing V582 capture is reused as a source; there are no new screenshots,
guide candidates or fresh DeSmuME results in this batch. Its RAM/report are not
modified. Production ROM/patch, artwork, translations, release registry and
canonical base remain unchanged. All18 plaque/hint entries remain incomplete
and all22 historical requirement objects remain deep-identical. The full graphics
goal and actual raw comic/legacy display/restoration gates remain open.
