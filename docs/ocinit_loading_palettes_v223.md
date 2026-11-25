# OCINIT native reads and startup palettes V223

This turn traces the ocean-init source bank and its shared startup palette inputs.
**No ROM bytes change. V218 remains current; the full graphics goal stays active.**

## Verified native texture reads

The original table at `02119194` supplies seven size/offset/destination triples.
The normal sailing initializer actually loops through the first six. All seven
entries are exercised through the unchanged original seek/read/texture-transfer
span with explicit table inputs; the seventh is not silently claimed as part of
the normal six-entry loop.

| Entry | File offset | Bytes | Texture destination |
|---|---:|---:|---|
| 0 | 0 | 65,536 | 00000 |
| 1 | 65,536 | 2,048 | 0E800 |
| 2 | 67,584 | 65,536 | 19000 |
| 3 | 133,120 | 8,192 | 29000 |
| 4 | 141,312 | 16,384 | 2B000 |
| 5 | 157,696 | 16,384 | 13000 |
| 6 | 174,080 | 2,048 | 2F000 |

Every byte, SDK file offset, count, texture destination and surrounding buffer
guard matches. Native stream open/close and the transfer argument spans execute;
filesystem/hardware operations are explicit bridges. All handles close.

The table covers **176,128 bytes** of the **194,560-byte** file. Its remaining
**18,432 bytes** at 2B000..2F800 are unclassified. Do not call this a complete-file
partition or discard the tail.

## Shared startup palette evidence

The original startup argument sequence at `02000E10..02000EE0` executes all thirteen
palette transfers. Each source pointer, size, destination and full byte hash is
recorded. The sources are immutable ARM9 palette arrays, rather than an assumed
palette at the end of OCINIT. Their relationship to individual texture consumers
still needs classification; matching a destination alone does not establish an
artwork's full native presentation.

## Diagnostics remain unadopted

Direct RGB555 rendering is visibly incoherent. File-tail palette assumptions are
not supported. A 128x512 indexed presentation and a four-bit alternative are source
diagnostics; they are not sufficient for artwork clearance without the corresponding
native texture/palette/parent relationship. No Japanese text is fabricated from
these noisy views, and no source pixels or colors are changed to make them clearer.

TITLEMAP's earlier complete record/source decisions and native queue bounds remain
separate valid evidence. The unresolved map scene rendering is not closed here.

## Artifacts and remaining work

- `scripts/verify_ocinit_io_v223.py`, focused Ruff passing.
- `work/analysis/raw_banks_v223/native_ocinit_proof.json`: seven source/transfer
  cases, thirteen palette argument cases and explicit coverage/tail limits.
- Source-only color diagnostics in the same directory, not release assets.

OCINIT texture formats and palette/parent relationships, its unclassified tail,
DSCHR and other embedded/raw resources, four Online screenshot bodies/chat,
confirmed-name consistency and final contextual/native/gameplay verification remain
in the full goal. V218 and its exact patch remain unchanged. Older record-based
checks remain to revisit after full goal completion.
