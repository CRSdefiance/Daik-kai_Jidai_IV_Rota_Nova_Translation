# V603: bounded native drawing-call trace

The previous turn answered a status question and made no implementation progress.
This batch implements and runs a new runtime investigation of the unresolved
Confirm and five miniature controls. Production V599, its patch, artwork, layer
registry and canonical baseline are unchanged.

## Research instrumentation and safeguards

A clearly named `current_blitter_trace_RESEARCH_ONLY.nds` derives from the exact
V599 hash. Its only changed components are ARM9 and the original 6,208-byte
overlay0 file. The overlay table is unchanged. Every existing autoload payload
is preserved except one branch at the corner-copy entry; the added research
section occupies 01FFD000..01FFF000. One branch also instruments the tiled-copy
entry in overlay0. Both wrappers preserve registers and flags and execute the
original displaced push before resuming at the exact original next instruction.
No resource, owner, source rectangle, palette, getter or drawing output is supplied
in place of an original input. Instrumentation can affect execution timing.

| Entry | Captured input contract |
| --- | --- |
|01FF92D8 corner copy|r0 screen, r1 PXL header, r2 bank, r3 source XY; stack source size and destination XY|
|01FFAE70 tiled copy|r0 screen, r1 PXL header, r2 bank, r3 source XYWH; stack destination LTRB|

The 852-byte helper counts every entry. It records selected complete input
rectangles, caller LR, header fields, a first-pixel sample and, only for the two
known generic adapters, an owner read from the real view. It does not assume r5
is a view for other callers. Negative coordinates retain their signed meaning.

Selection includes four-bit 48x20 Confirm-shaped images; 16/24/32/48x8 independent
canvases; and four-bit 256x256/512x256 atlas rectangles intersecting the complete
miniature band. Conservative one-pixel bounds include original zero-size tiled
descriptors. One otherwise unrelated atlas sample from each routine is recorded
as a positive control. These samples do not count every use of their source cells.
The fixed 84-record buffer deduplicates full records and explicitly counts
overflow, rather than silently dropping new records.

Twenty Unicorn cases verify all input/saved registers, CPSR flags, the exact
displaced stack contents, source preservation and both calling contracts, including
zero dimensions. Separate checks cover duplicate counts, capacity/overflow,
wrong-depth/size rejection and both positive controls. These stop after the
displaced prologue; they are not full gameplay tests. An initial assembler
`.space` directive caused incorrect absolute resume branches and was rejected by
these checks before any emulator run. The final helper uses explicit NOPs and
all exact resume-address checks pass.

## Actual cold boots and scope

All runs use the pinned DeSmuME core, original controller/stylus schedules and no
savestate. The Deck run cold-boots a byte-identical isolated battery-save copy;
the other two begin through New Game. No new inventory, outcome, location or
unlock fixture is applied. The ROM instrumentation makes these research runs,
not normal guide or earned-outcome evidence.

| Input path | Frames | Drawing calls | Exact unique screenshot comparisons to V599 |
| --- | ---: | ---: | ---: |
|Name editor, Latin/Symbol pages and returns|7,900|73,024|17|
|Saved-game Continue, town and Deck|4,650|48,530|12|
|New Game and Market purchase/sale sequence|24,100|283,213|19|
|Total|36,650|404,767|48|

There are 51 exact capture-file comparisons, including duplicate final captures,
covering 48 distinct run/frame pairs and 4,718,592 whole-frame pixel positions.
One additional keyboard capture at frame6900 has no historical counterpart and
gets no exact-comparison credit. The Deck baseline is a separate fresh run of
unmodified V599 with the same save and inputs. Keyboard and Market comparisons
use their existing V599 captures. This does not establish identical behavior
between sampled frames, across every path or on hardware.

Both drawing routines produce positive control records in each run. All six
records are the known source-row208 atlas decorations, outside the target band;
there are zero selected target records and zero overflows. The observer body,
both hook branches and unused log tail remain exact in final read-only native
ITCM exports. Native serialization neither changes main RAM nor loads a state.

## Cache-lifetime evidence and consequence

The logged positive address0232D330 still contains the entire exact current
`__frame.pxl` in the final keyboard snapshot. It has been reused for unrelated
data in the final Deck and Market snapshots; the exact current atlas is resident
elsewhere in each. The proof records this distinction instead of assigning a
later resource identity to an earlier pointer. Header shape/first-pixel samples
are not a whole-file checksum at the time of a call.

No target use is observed through these two routines in the three sampled input
paths. This is new runtime evidence, including computed callers, but is not
proof that the controls are unused globally. Other gameplay paths, GPU consumers,
direct-color/resized/partial/composed copies and raw graphics remain outside the
trace. Confirm and all five miniature ordinary parents remain open. The next
investigation should expand to actual GPU/embedded consumers or genuinely
different input paths, rather than repeat these same three schedules or the
earlier literal-reference census.

## Reproduction and retained work

1. `scripts/prepare_blitter_trace_v603.py`.
2. `scripts/verify_blitter_trace_abi_v603.py`.
3. Run the original schedules saved under `work/analysis/blitter_trace_v603`
   against the research ROM with `headless_desmume_v193.py`, using the report
   arguments and read-only native exports. Never use this ROM as a release parent.
4. `scripts/verify_blitter_trace_v603.py`.
5. `scripts/record_blitter_trace_v603.py`.

Proofs, seven unmodified research screenshots and provenance are archived on E
under `Screenshots/Test fixtures/V603 Runtime drawing trace`. Publication and
ordinary guide credit are not granted. All18 original plaque/hint entries remain
incomplete and all22 historical requirement objects retain their exact scope.
Other material, rare-event, legacy, ending and human acceptance gates remain
open. The graphics goal is active; older record-based checks remain due at full
completion.
