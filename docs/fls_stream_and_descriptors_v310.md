# Native FLS stream and cached descriptors V310

Research on unchanged V309, SHA256
`b099a1016d08870adbdbff8693be9b5fba2f0fa611c82358bafcd507199d5289`.
The previous turn fixed26 shared sailing-condition names. This checkpoint
follows two dynamic file-opening paths left unresolved by V301.

## Complete FLS stream parsing

Original constructor020FE050 initializes an isolated1B18-byte movie object.
Original parent020FDED0 calls02100310's stream open and02100050's chunk parser.

Both constructor and parent execute through native return for every15 actual
FLS resource. Filesystem SDK open/read/seek/close is the only instruction bridge.
Allocation, file-prefix interpretation, chunk dispatch and object initialization
execute original ARM9 code using the current captured runtime globals.

The read-only snapshot comes from the V30930,000-frame ordinary cold boot; its
ROM and RAM hashes match the saved capture report. It is copied into an isolated
Unicorn machine. Scratch object, caller-supplied filename and captured global
state are explicit input contracts. No emulator progress is altered or loaded.

Every declared metadata prefix is exact in native allocated memory. Native
file/table/command/FINF pointers match the original header, the source FINF
canvas matches the parsed object, all saved registers and stack returns match,
and object/outer-stack canaries remain intact. This includes metadata for all
261 texture records; it does not claim the texture payloads were decompressed.

| File | Texture records | Native movie canvas |
|---|---:|---|
| logo |4|256x192|
| M20 |28|256x192|
| m21 |1|256x192|
| M22 |3|256x192|
| M23 |5|256x192|
| M24 |5|256x192|
| M25 |3|256x192|
| M26 |2|256x192|
| M27 |1|256x192|
| M28 |170|256x192|
| M29 |8|256x192|
| M30 |12|256x192|
| M31 |10|256x192|
| M32 |8|256x192|
| root m02_03 |1|256x192|

The root file's texture storage remains512x512 with the377-row source image
extent documented previously. Its256x192 **movie canvas** is a different field.
The native parser accepting the root file does not establish its gameplay trigger,
scaling, viewport crop or GPU output. The coastal artwork remains source-exact.

Actual direct callers of parent020FDED0 are020D2C00 (generated movie loader) and
020FD4A0 (movie-state continuation). V301 already proves the generated filename
family logo/M20–M32. Supplying the root filename in this research is a declared
controlled input, not discovery of an original root-file caller.

## Cached graphics descriptor path

Cached-resource helper020D6558 obtains a filename from descriptor+0C.
The current complete main/overlay scan finds21 direct ARM calls, no direct Thumb
calls and one method-pointer literal. Each direct site's literal descriptor is
resolved through actual captured RAM. Native instructions from that descriptor
load to the call site reproduce the same argument; descriptor bytes remain intact.

The21 direct sites select nine actual resources:

- `/_pxl/seaarea.pxl`
- `/_pxl/title/title05.pxl`
- `/_pxl/title/title02.pxl`
- `/_pxl/tumini.pxl`
- `/_pxl/plate4016.pxl`
- `/_pxl/frmMessage.pxl`
- `/_pxl/__frame.pxl`
- `/_pxl/wl_icons.pxl`
- `/_pxl/mysterymap/point.pxl`

This supplies named resource contexts instead of treating every descriptor as
a possible unidentified raw-comic reader. It does not prove full parent/cache/
GPU display or rule out computed/virtual filenames. The remaining method-pointer
context and all11 legacy layout gates stay open.

One isolated segment,020BD0E8–020BD0F8, also reads preceding parent metadata
through R1/R5. A zero-filled scratch input is explicitly provided for that
unrelated metadata; its R0 filename descriptor still comes from the actual
literal and captured descriptor. This case does not claim captured parent
registers, complete widget construction or physical input.

## Failed assumptions retained

An initial verifier masked bit80 from the header's command offset. Original
native parsing uses the complete first word, so that assertion incorrectly
rejected compressed files. The failed proof remains in
`rejected_command_offset_assumption.json`; the corrected proof follows native
pointer arithmetic and passes all15 resources. No ROM change was made.

The first cached-argument attempt omitted BD0EC's R1/R5 parent metadata and
stopped with an unmapped read. That failed call receives no parent/display
credit. The successful case explicitly records its scratch-input contract.

## Current scope and next work

No new ROM or patch is needed for this checkpoint; V309 remains the registered
combined candidate and its exact reconstructable patch remains unchanged.
Both authoritative audits and progress documents record these results. All18
plaque/hint entries and Armor/Weapon variants remain incomplete. Low resolution
Online screenshots remain exempt.

Continue original texture payload reads/decompression, movie texture/view
composition and the virtual descriptor context. Actual legacy/Gallery display,
occupied weapon/armor and alternate condition checks remain open. This does not
complete the graphics goal or imply hardware verification. Revisit older
record-based checks at actual goal completion.

Evidence: `work/analysis/fls_stream_v310/proof.json`,
`cached_descriptor_callers.json`, `native_run.log`;
scripts `research_fls_stream_v310.py`, `research_cached_descriptors_v310.py`,
and `record_fls_stream_v310.py`. Focused Ruff passes.
