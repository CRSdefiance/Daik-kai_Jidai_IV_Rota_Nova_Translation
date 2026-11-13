# V492 compact allocation controls

Status: research only. V484 remains the current registered candidate, SHA-256
`f2036bafc3736a353cb0a2de8f40bd5eee8bed3cd16e779f68e3ebb1914b875c`.
No playable candidate, patch, canonical promotion or graphics completion credit.

## Matched movie results

Five cold-boot DeSmuME tests use the same core, options, input schedule and
6000-frame range. Each substitutes exact M28 bytes into the M20 resource slot.
The original town numeric bitmap binding is retained. The only added behavior
is one persistent allocation through the original SDK allocator, guarded by a
pointer slot. This does not establish normal ending invocation or route unlocks.

| Added allocation | Matching name pixels at frame 3700 | Result |
| --- | --- | --- |
| 0 bytes | 3047 of 3047 | Complete |
| 16 bytes | 3047 of 3047 | Complete |
| 128 bytes | 3047 of 3047 | Complete |
| 608 bytes | 553 of 3047 | Incomplete |
| 2912 bytes | 553 of 3047 | Incomplete |

608 bytes represents a proposed 96x12 four-bit line bitmap plus header and
alignment. 2912 bytes represents five such rows in a 96x60 bitmap. Neither
persistent allocation restores the name artwork in this matched fixture.
The exact allocator capacity, fragmentation or movie failure mechanism is still
unproven. These observations do not prove that every allocation above 128 bytes
fails, or that the real ending uses the same loading conditions.

The helper occupies fixed padding at `01FFC504`; the pointer slot is `01FFC5FC`.
All helper instruction and literal bytes remain exact in the terminal ITCM export.
Each allocated pointer is `023A9780`. This experiment does not rely on the
runtime-written `01FFC828` region used by older controls. No new free operation
or shared numeric-header mutation is introduced.

## Copy-path investigation

The original town updater at `020B5FC8` constructs its text context over the
composed view at town-object offset `+14`. The stock-name painter runs at
`020B63D4`; the function ends after context destruction at `020B63E8`.
The separate composed-view draw function `020D437C` passes its descriptor table
and count to `020D470C`, then invokes the destination's virtual composition
method. The captured Istanbul object contains the 21-entry table `0211A65C`.
This distinguishes text updates from later descriptor composition; rendering
directly after the stock painter is not yet proven to target the final screen.

An isolated synthetic destination using the ordinary image-view class has no
composition method and stops at PC zero. That probe is not valid destination
evidence and does not establish a direct drawing fix. Next work must establish
the real destination contract before replacing the shared bitmap expansion.

## Evidence

- Preparation: `scripts/prepare_town_allocation_sizes_v492.py`.
- Verification: `scripts/verify_town_allocation_sizes_v492.py`.
- Manifests, assembly and proof: `work/analysis/town_allocation_sizes_v492`.
- Actual capture reports: `work/emulation_v193/town_allocation_sizes_v492_*`.
- The verifier checks source/ROM/report hashes, every capture hash, complete
  name pixels, matched options/inputs and terminal helper integrity.
- Both scripts pass Ruff. No production bytes were changed.

All22 historical requirements and all18 incomplete plaque entries remain in
the audit. Synthetic inventory fixtures remain authorized for equipment testing;
they do not prove normal acquisition or unlocks. At actual graphics-goal
completion, revisit older record-based checks.
