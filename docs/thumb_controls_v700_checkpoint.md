# V700: bounded Thumb control paths and the first replay I/O failure

The previous goal turn made progress through V698's actual Sailor Info states
and V699's eight complete village-card fixture displays. This turn checks a
previously excluded control-owner path and diagnoses the first V698 replay stop.
No production artwork, ROM, script, patch, manifest, registry or release pointer
changes. There is no new emulator screenshot or ordinary control-display credit.

## Thumb search boundary

V688 covered bounded ARM literal, arithmetic and pointer-table owner aliases.
It explicitly left Thumb paths open. V700 considers every aligned halfword in
the same source-bound main sections and overlay0, including the current verified
startup-copy live POOL view. The analyzer recognizes Thumb literal-load seeds and
up to24 following two-byte constant arithmetic, move, shift or read-only word-load
instructions. No value crosses a call, branch, store, stack operation, unknown
instruction or unsupported state. Every halfword is only a candidate, including
inline data; this is not an executable-code census.

|Version|Halfword positions|Literal seeds|New owner leads|
|---|---:|---:|---:|
|Clean source|761,472|3,996|0|
|Current V692 views|887,198|4,531|0|

The two exact20-byte target objects are Confirm at023139C0 and Frame at02313F60.
Three native Thumb calibration cases execute a computed alias, a read-only pointer
table, and a literal at halfword phase2. All15 non-PC registers,PC,CPSR and the
complete4 MiB RAM match independently declared results. Three negative branch,
store and return boundaries pass. Six owner-boundary cases include offset0/16 and
exclude offset20, avoiding V688's rejected adjacent-resource false lead.

An initial native calibration switched from the machine's SVC mode to system mode
after writing SP/LR, so the selected system bank held zero. Its source and failure
note are retained. Selecting the intended CPSR bank before initializing its
registers fixes the test setup; production code was never changed.

The result adds no new Confirm/Frame parent. It removes this bounded literal/constant
Thumb path from the immediate leads. Variable/runtime pointers, cross-call flows,
other resource readers and dynamic geometry remain outside coverage. All six
small-control context requirements stay open; no global unused-art claim is made.

## Exact first V698 replay failure

The unchanged V698 replayer is rerun against its actual captured state in a separate
diagnostic directory. A Unicorn invalid-memory observer records the access and
returns false, preserving the original failure. It supplies no I/O value or bridge.

The first stop is exactly:

- Original PC020E31E4: `LDRH r0,[r1]`.
- R1/address04000204, size2, unmapped read.
- The original source literal at020E31F4 is04000204 in both clean and current ROMs.
- The retained DeSmuME source names04000204 `REG_EXMEMCNT` in `registers.h`.
- The diagnostic reaches the same two actual checkpoints, `update_entry` and
  `actor_ready`, and reproduces the original `UcError()` without changing it.

The invalid-access callback's value field is not a captured hardware-register
value. No zero-filled I/O page is mapped and no guessed register value is returned.
This establishes the immediate test-model gap, not a production text/graphics
defect or full subsequent execution. Replaying this whole prefix requires a
source-bound model or actual captured inputs for the I/O it encounters. Later
prefix state equivalence and V694's separate suffix RAM/DTCM differences remain
unproven; the successful V698 display comparisons remain valid on their own scope.

## Evidence, release and remaining scope

- `scripts/trace_thumb_controls_v700.py` and `scripts/diagnose_person_prefix_io_v700.py`.
- `work/analysis/thumb_controls_v700/`: source hashes, bounded scan, native controls,
  retained initial calibration, exact failing access and copied replay failure.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V700 Thumb controls and replay IO`.
- V692 SHA256 remains
  `0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.

All18 original plaque/hint entries remain incomplete and all22 historical scope
objects remain exact. Ordinary control/card triggers, comic playback, remaining
legacy/embedded contexts, texture/restoration review, older record-based checks
and final acceptance remain open. No guide promotion, new ROM, commit or push.
The full graphics goal remains active.
