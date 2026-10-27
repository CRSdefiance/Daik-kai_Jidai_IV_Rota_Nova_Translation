# Native movie projection prefix V331

V326 remains unchanged, SHA256
`fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1`.
No ROM, graphics asset, patch or release profile changes.

## Original projection setup

The original movie draw parent at020FD178 executes through020FD28C, immediately
before slot selection. Its SDK orthographic/look-at/rotation routines execute
without instruction bridges. Original projection, timeline, mask/quad and SDK
code ranges are byte-identical in current, clean and the captured runtime RAM.
The native constructor/parser and supplied filename/global-state contracts remain
the previously documented stream fixture.

The CPU reads division and square-root hardware registers. Their arithmetic
results follow the [pinned DeSmuME implementation](https://github.com/libretro/desmume/blob/95b4d798731caa809125b6c3c11d17cc332ff6ef/desmume/src/MMU.cpp#L1049).
The fetched Git blob is verified against the commit tree. Hardware completion is
instantaneous in this isolated model: cycle latency, races and GPU processing
are not modeled. The unused C++ signed64 minimum/-1 overflow case is explicitly
rejected rather than assigned an invented result.

All15 FLS current/clean pairs produce identical native commands and serviced
arithmetic reads. Each prefix writes74 GPU registers and services19 math-register
reads, including repeated reads of a result. Totals are **1,110 register writes**
and **285 serviced reads per version**, not285 distinct division operations.

An independent exact-rational reference uses the original inputs: top/left0,
bottom/right1, near1, far400 and scale1. Native FX12 projection axis scales are
2/-2, translations-1/+1, and depth terms-2/399 and-401/399 at native precision.
The emitted16-word projection and12-word camera matrices match every reference
value in all15 cases. The camera matrix is identity with a negative-one z
translation in this declared setup.

A negative control leaves the mapped math registers unmodeled/zero. It emits
an all-zero projection apart from the final4096 word and fails the reference.
Simply mapping hardware addresses is therefore not accepted as projection proof.

## Contextual mask scope

The original parent resets the object's mask count to zero before selecting
slots. Its unchanged draw loop calls the mask producer only for active slots
with a nonzero draw kind. The complete recorded15 timelines contain none.

The mask audit covers45,058 native update calls and all recorded distinct states,
including global controls. Every tested current FLS file is byte-identical to
the proven timeline's source-provenance file. This establishes absence of active
mask slots in these particular constructor/timeline paths. It is not a claim
that the engine's mask feature is globally unused, that every possible caller
was tested, or that GPU viewport/depth clipping is complete.

The raw root file retains its separate unknown caller/usage obligation. Running
the generic prefix with its parsed object does not establish actual root playback.

## Remaining rendering and goal requirements

This checkpoint stops before drawing slots and before the complete parent return.
It verifies original CPU projection preparation, matrix words and mask reset;
the recorded writes are observed register commands, not final GPU framebuffer
pixels. Full texture transfer, concurrent/recycled palette banks, viewport/depth
clipping, alpha blending and actual ending/Gallery playback remain open.

Both graphics audits, the requirements ledger and progress documents record the
result. All18 plaque/hint entries and Armor/Weapon variants remain incomplete.
Other legacy/native/gameplay gates stay open. Low resolution Online screenshots
remain exempt. The graphics goal stays active; revisit older record-based checks
at actual completion.

Evidence: `work/analysis/fls_projection_v331/all_projection_proof.json`, `source.json`
and pinned `MMU.cpp`; source mask states in
`work/analysis/fls_frames_v312/all_files_proof.json`.
Reproduce with `scripts/research_fls_projection_v331.py --all`; focused Ruff passes.
