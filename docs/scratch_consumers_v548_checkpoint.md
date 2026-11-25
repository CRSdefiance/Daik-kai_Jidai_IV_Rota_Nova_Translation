# V548 connected scratch-buffer item consumer

V546 remains the current combined candidate. No ROM, patch, graphic or release
layer changes in this checkpoint. The previous turn only confirmed an existing
plaque defect record and is classified as no progress. This turn adds a missing
connected native cache-transfer proof rather than repeating the older file-read
or TITLEMAP source tests.

## New evidence

The original item-cache owner at `022857AC` and all 16 native descriptors come
from V547's ordinary V546 cold-boot RAM capture. The descriptors have format8,
word width16 and height32, producing32x32 indexed cells. Their pixel pointers
resolve into native slots at owner+2CC, with a2048-byte stride. The actual image
uses1024 bytes in each slot. The other half is not treated as extra image data.

All218 items in every16 slots execute the complete original routine02047704:

1. Original tag update and file reader02047864.
2. Original file constructor/open/seek/read/close, with only SDK filesystem
   operations bridged to the exact unchanged `/_pxl/item.pxl` in V546.
3. Exact1024-byte source read at532+index*1024 into02233040.
4. Original020E2974 copies that data into the descriptor's cache pixels.

All3488 cases return with the stack and saved registers intact. Complete source
pixels, destination pixels, surrounding guards, all16 headers, every other cache
pixel and the selected slot tag pass. All3488 repeated calls pass with no file
operation or scratch-buffer read. Item/slot selections and cache-miss tag resets
are explicitly controlled inputs in isolated RAM, not natural acquisition.

The original copy routine has r0=source and r1=destination. At the three cache
copy sites02047648,02047764 and02047818,02233040 supplies the source. The tested
connected routine is02047704; this does not credit complete execution of the
other two callers. Assuming the opposite argument order would misclassify these
as scratch writes.

## Reference census and limits

The declared main sections have20 aligned literal words equal to02233040;
ARM9 overlays have none. This is an aligned literal inventory, not a complete
pointer-flow or indirect-call closure. Generic stream routines also use this
address as a comparison threshold/default storage. A literal reference is not
by itself a graphics or palette binding.

The newly verified item transfer reads item pixels, not raw SLACK portraits or
comic planes. TITLEMAP's source/reader/layout and basic item file reads were
already covered by V221/V222 and V210; their rediscovery is not credited as new
verification. V547's synthetic descriptor still points to separate workspace.
Raw SLACK colour binding/comic consumers, generated filenames and actual scene
composition remain open. This checkpoint has no GPU display or normal earned
item-acquisition credit and does not declare any legacy archive globally unused.

## Audit state

All22 original requirements are preserved exactly. All18 plaque/hint entries and
the global source-texture issue remain incomplete. The full graphics goal remains
active; candidate promotion requires the established human acceptance gate.

Proof: `work/analysis/scratch_consumers_v548/transfer_proof.json`.
Verifier: `scripts/trace_scratch_consumers_v548.py`.
Candidate SHA256:499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3.
