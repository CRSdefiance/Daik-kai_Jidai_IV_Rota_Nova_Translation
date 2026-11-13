# V668: actual resource calls and indirect frame source selections

The previous turn made progress through V667's complete actual Karibib Town
screen and retained encounter/missed-return evidence. This checkpoint investigates
the actual indirect resource paths left unknown by earlier static analyses.
V666 remains unchanged; no new ROM, patch, artwork or release profile is made.

## Diagnostic contract and validation

The pinned DeSmuME core has two contiguous4096-entry ARM opcode tables. Complete
8192 executable pointers and the source-declared B/BL families identify one exact
table pair. The original game resource getter020D6558 begins with E92D4070,
index927 under the source instruction-index formula. SFORMAT anchors independently
bind ARM9 instruction, instruction address, next address, all registers and CPSR.

Only the calling diagnostic process temporarily changes that one ARM9 host
opcode-table pointer. A native filter reads the actual getter-entry registers,
records matching entries, restores host registers/flags/stack and tail-jumps to
the unchanged original opcode handler exactly once on every path. It writes
only its private host log. No emulated ROM/RAM/VRAM/register/input is written.
The table pointer and original DLL file are checked restored afterward.

Seven independent native host-only scratch controls cover matching entries,
second log slot, wrong PC, disabled tracing, capacity overflow, wrong instruction
and an invalid stack pointer. Original parameter/return, host registers, flags,
stack and supplied source bytes remain exact. These tests are not gameplay.

Three ordinary24100-frame cold boots use the existing New Game/market schedule:
initial register trace, unmodified-core baseline, and extended stack trace.
There are no saves, savestates or gameplay fixtures. All89 sampled complete
two-screen frames in each observed run match the baseline:178 whole pairs.
Both trace versions contain the same53157 original entry records, in the same
order, with every original register field exact. No overflow or instruction
mismatch occurs. Native reads of eight stack words are bounded to main RAM.

## Original requests and callers

Executing the complete original initializer binds315 owners to their filename
fields. The run requests21 of these owners through seven original source call
sites. Every recorded entry has the expected PC, instruction/host parameter,
ARM state and R15. Direct BL targets and the actual BLX register targets match
020D6558. The source caller instructions remain clean-identical.

The frame atlas receives31698 requests. Of these,11444 use the generic virtual
view getter020D4170: its type4 branch loads the owner from view+12 and calls the
first actual resource virtual method. At the resource entry, LR is020D419C;
the saved parent's LR is at SP+4. Three original native view-getter cases verify
that unwind contract and the nonresource-type path. Only the final cache lookup
is bridged to a supplied loaded header in those isolated cases.

Actual saved returns identify two original copy parents:

| Parent return | Requests |
|---|---:|
|020CFDC0|1032|
|020CFFA0|10412|

Their source-coordinate fields are already copied into stack words4..7 before
resource lookup. The complete original parent/helper code binds those fields to
the subsequent corner-copy source XYWH arguments. Twelve independent native
parent cases cover both parents for each actual geometry; four additional
positive cases select known caption cells. Cache lookup and final pixel call are
bridged in these witnesses, so they validate argument interpretation and ABI,
not new rendered gameplay pixels.

| Selected source XYWH | Requests |
|---|---:|
|104,112,32,16|343|
|104,216,8,8|5301|
|108,29,72,26|1192|
|112,216,8,8|2384|
|128,224,32,32|1192|
|240,240,16,16|1032|

None intersects the five miniature caption cells. The108,29 rectangle overlaps
their Y band but ends at X180, before the first caption at X184; a row-only test
would be misleading. This is evidence for these actual pre-lookup source
selections, not proof that every individual copy completed or every pixel was
painted. Frame requests through the other paths remain separately recorded.

## Limits and next useful work

Confirm has no resource request in this schedule. That is not global non-use.
The generic view getter's other types can return an already stored header
without a resource request. Cached-direct views, other frame/style paths, other
input schedules and the actual six Confirm/Done/Rank/Cancel/Pick Cargo/Pick Ship
contexts remain open. Trace final copy/tile consumers or those other contexts
next; repeating the old literal-owner scans would not resolve this gap.

An early native checker mistakenly compared current LR to the parent's saved
LR. The failure is retained. Original source and independent native execution
resolve the two separate addresses; no ROM change or pixel waiver follows.
The executed initial observer/runner sources are frozen separately. Two later
lint-only source edits preceded the stack extension and occurred after both
initial processes exited. No live runner/helper was modified.

## Evidence and preservation

- Verify: `scripts/verify_resource_dispatch_v668.py` and targeted Ruff checks.
- Source/table proof, native host controls and complete result:
  `work/analysis/resource_dispatch_v668/`.
- Runs/traces: E Generated/work/emulation_v193/resource_dispatch_v668_newgame_*.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V668 Resource dispatch`.
- Current candidate: `out/all_routes_combined_v666_candidate.nds`, SHA256
  `706350a55a058b7a87b67d396333ed397dac664ba36ea378161d18fd085ba121`.

Unmodified screenshots, complete traces, reports, sources and native controls
are retained. There is no new artwork edit, guide promotion, canonical promotion,
commit or push. ROM, patch, registry and release pointers remain unchanged.
All18 original plaque/hint entries remain incomplete; all22 historical scopes
remain exact. Card/legacy/material/equipment/movie contexts, older record checks
and final acceptance retain their scope. The full graphics goal remains active.
