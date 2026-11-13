# Native FLS CPU upload service V332

Current ROM remains V326, SHA256
`fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1`.
No ROM, artwork, patch or release-profile changes.

## Original decoder and upload execution

Every compressed texture is tested separately through the original constructor/
stream parser, queue insertion, decoder worker and completed-job upload service.
The original service at020FE138 selects pixel/palette SDK upload functions,
temporarily configures banks, flushes the source buffer, transfers data and
clears completed jobs. Original game/SDK instructions execute; SDK filesystem
operations remain the explicit stream bridge.

The SDK's original ITCM helper at01FF990C programs DMA channel3 in these cases.
Its complete routine, bank/upload functions and interrupt wrappers are source-
exact. An initial whole-ITCM equality assertion was too broad: 23 established
arena-related bytes differ outside the tested DMA helper. That overclaim is
withdrawn; the actual transfer routines are independently checked. No production
code was changed to make the comparison pass.

## Explicit hardware contracts

The isolated fixture maps LCDC memory and DMA registers. Each native request
must be aligned, incrementing, immediate32-bit DMA with a bounded positive
count. The model copies the requested words and clears enable at the next CPU
instruction. Other DMA modes and zero-count/unbounded requests are rejected.

This is an immediate DMA model, not a physical transfer. Hardware cycle timing,
IRQ delivery, GPU-visible VRAM aliases and final rendering are not modeled.
The declared logical destination is offset0 in the captured bank configuration;
each texture/palette starts in a fresh isolated object and sentinel-filled memory.
It does not establish simultaneous allocation, bank recycling or every setup.

## Complete results

All **520 palette/pixel cases** across260 compressed textures pass. At the final
native SDK-selected physical destination, all **9,821,984 payload bytes** equal
independent decompression and the original metadata's declared/padded sizes.
The whole modeled LCDC memory outside requested DMA spans remains unchanged.
Native decoder/upload routines return and completed queues clear normally.

The largest131,072-byte M22 background is tested explicitly. Its four native
requests overlap future output; later transfers overwrite provisional bytes.
Final destination data matches every byte. Requests are not concatenated or
treated as finished merely because their lengths sum to the output size.

The palette/pixel sources include the translated cards and artwork. Complete
decoded byte transfer is stronger than the earlier inert-destination decoder
check. It is still not final GPU pixel, palette-bank concurrency or playback proof.
Raw root/m02_03 remains outside the compressed queue test, with its intended
caller/raw loading/usage gate open.

## Continuing goal

Both graphics audits, requirements ledger and progress documents record the
new CPU-side evidence. GPU bank aliases, concurrent/recycled palettes, screen/
depth clipping, blending and actual ending/Gallery playback remain open.
All18 plaque/hint entries and Armor/Weapon variants remain incomplete. Other
legacy/gameplay gates remain open. Low resolution Online screenshots remain
exempt. The full graphics goal stays active; revisit older record-based checks
at actual completion.

Evidence: `work/analysis/fls_upload_v332/all_upload_proof.json`, `largest.json`,
`summary.json`, progress and run log.
Reproduce with `scripts/research_fls_upload_v332.py --all` and
`scripts/record_fls_upload_v332.py`; focused Ruff passes. The process is terminal
with exit0. These are controlled native upload fixtures, not a route playthrough
or physical-device verification.
