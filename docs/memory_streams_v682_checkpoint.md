# V682: Save/Load RAM streams and current Level/Power plaques

This checkpoint closes the specific suspicion that generic stream modes 1 and 2
are additional filename loaders in their known Save/Load callers. It changes no
ROM, artwork, translation, palette, registry, patch or release pointer. V678
remains the latest experimental compiled candidate.

## Source contract and bounded native controls

The original generic open at 020D0398 assigns backing 02249C40 for mode 1 and
02233040 for mode 2. Both ignore the filename argument and initialize the cursor
and high-water size to zero. These modes select a RAM buffer; they are not
read-only versus write-only permissions. Original reads/writes copy bytes and
update cursor/high-water fields. Absolute and relative seeks change the cursor;
the memory path's origin-2 seek leaves it unchanged. Close clears the backing
and size but retains the cursor. These source ranges match the clean ROM.

Twenty native host-prefix controls include the shared opcode group containing
both known caller returns. Eight main-RAM mirror controls pass. Four clean/current
mode-1/mode-2 scenarios execute 40 complete original native operations, checking
unaligned writes, zero reads, seeks, data, canaries, stack and preserved registers.
No SDK filesystem call is reached by these supplied RAM operations.

## Actual Save/Load sequence

Two cold boots finish all 14,200 frames of the established Save/Load input
schedule: one read-only host observer and one unmodified-core baseline. Both
load the same unchanged isolated donor battery save. Neither loads a savestate
or injects live gameplay state. All 32 complete sampled two-screen RGB pairs
and the full terminal RAM match. The sequence previews Save, visits all six
Load slots, cancels/reenters confirmation, and loads the first slot to Stockholm.
It does not confirm an actual cartridge Save write.

The observer records 33 callbacks: nine selected memory-stream records and 24
ignored disk opens/closes. Every callback checks the complete CPU prefix and
4 MiB WRAM unchanged by observation; all host opcode pointers are restored and
the core DLL remains exact. Known caller returns use r4 for the stream owner,
whereas open/close entries use r0.

| Session | Original backing | Complete payload | Source or role |
| --- | --- | ---: | --- |
|Mode 1, frames 2839–2843|02249C40|37,015 bytes|Exact donor slot 6, zero-based 5, offset 204800|
|Mode 2, frames 5811–6204|02233040|37,015 bytes|Current game serialization used by Save preview|
|Mode 1, frames 13842–13846|02249C40|37,015 bytes|Exact donor slot 1, zero-based 0, offset 0|

All three actual buffers additionally pass complete isolated original-native
readback from their captured snapshots, without SDK calls. The mode-2 readback
seeks to zero first. It verifies byte retrieval, not a whole-game save/restore
roundtrip, persistence or actual cartridge writes.

### Cursor and size are separate

Mode 2 closes with cursor 124 and high-water/payload length 37,015. The initial
verifier incorrectly required cursor equal size; its source/log are retained.
Source semantics and complete actual fields resolve this analyzer assumption.
An unnecessary isolated header-refresh probe then incorrectly expected an
idempotent header update on the close snapshot. That rejected verifier/log are
also retained. The current verifier removes that probe and reads the untouched
captured payload after a seek. No production bytes or emulator run were changed
to satisfy either assumption. Header-refresh entry was not traced, so this
checkpoint does not identify the last live operation that set cursor 124.

02233040 is a reusable Save serialization backing in this sequence; its use
does not imply a permanent raw-picture identity. These known mode-1/mode-2
callers do not open additional graphics filenames. Other callers, interfaces,
legacy artwork and unresolved actual graphics consumers remain open.

## Plaque and visual checks

The current whole `/_pxl/saveloadinfo.pxl` equals the V612 translated asset.
All 36 Level/Power crops across 18 active states match 26,568 complete native
five-bit region pixels. Independent native-font masks include every leading
and trailing glyph stroke and blank cell. This is current display evidence;
the earlier V612 getter replay is not presented as a new V682 replay.

The eight-frame current review sheet was opened. Labels, six-slot list,
confirmation and final Stockholm Town display show no new defect in the
selected views. Hidden wood reconstruction remains approximate. All 18 original
plaque/hint audit entries remain incomplete pending broader variants/material
review and acceptance. These captures are test evidence, not guide promotion.

## Evidence and scope

- Scripts: `prepare_memory_streams_v682`, `observe_memory_streams_v682`,
  `check_memory_streams_v682`, `run_memory_streams_v682`,
  `verify_memory_streams_v682`, recorder and archive verifier.
- Source contracts, native controls, preserved failed analyzer assumptions,
  full proof and review sheet: `work/analysis/memory_streams_v682/` on E.
- Both terminal capture reports, screenshots, final RAM and actual observer
  snapshots/payloads: `E:/Rota Nova translations/Generated/work/emulation_v193/memory_streams_v682_*`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V682 Save Load memory streams`.
- V678 SHA256: `d1aaf37bcb7dec218d200a5fa72a6c58e0fb50ab85a8bcb7766d4e749903e341`.

The original 22 historical requirement objects remain exact. Six small controls,
eight cards, actual comic/legacy contexts, material restoration, older checks
and final acceptance remain open. Online exclusions and brown-mark preservation
stand. The preceding status-only user response is classified as no progress;
this recorded checkpoint is progress. The full graphics goal remains active.
