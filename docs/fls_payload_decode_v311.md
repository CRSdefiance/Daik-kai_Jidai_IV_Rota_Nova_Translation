# Native FLS palette and pixel decoding V311

Research on unchanged V309, SHA256
`b099a1016d08870adbdbff8693be9b5fba2f0fa611c82358bafcd507199d5289`.
V310 verified metadata parsing. This checkpoint tests actual palette/pixel
file reads and software decompression before GPU upload.

## Original native path

The movie texture consumer020FFD14 prepares original palette queue020FFB7C
and pixel queue020FFC48 requests. Pixel output size comes from padded texture
dimensions and4/8/16-bit format; the stored compressed slot size is different.
Worker020FE218 seeks/reads the actual file and executes incremental LZ routines
020E2D20 and020E2C20. The completed requests are inspected before020FE138's
hardware upload and cleanup.

Every260 compressed texture in all14 generated FLS resources is tested for
both palette and pixels: **520 complete native decoding cases**. All decoded
bytes match independent LZ10 decompression of the current file. Native saved
registers, stack returns and outer guards pass. This includes the translated
genre/subtitle/name art and complete padded texture allocations.

Original020FE71C initializes the movie heap at02233040 with size40000, using
the same arguments as the original loader. The town snapshot's prior movie
heap had been reused; its stale state cannot substitute for initialization.
File SDK open/read/seek/close is the only instruction bridge. Real end-of-file
short reads are modeled; metadata reads remain full-length as in V310.

Inputs are explicitly controlled: the scratch stream object, source-derived
queue parameters, original heap setup and an inert future-upload destination.
Current cold-boot RAM supplies other runtime globals; its hash and ROM identity
match the capture report. Relevant native code bytes match the registered ROM.
The emulator's RAM or gameplay progress is never changed by these CPU tests.

## Large requests overlap

M22 texture0 has131,072 decoded pixel bytes. The native worker emits requests
at offsets0,33,792,67,584 and101,376. Their reported lengths are33,792,
97,280,63,488 and29,696; intermediate requests overlap later output.
The test follows subsequent replacements until both active and pending queue
fields are idle. The final complete bytes then match the independent decoder.

The initial assumption that request lengths could simply be concatenated
stopped prematurely after two calls and falsely rejected the background at
byte68,115. Correcting the harness produces the exact full background. This
was a test error; no ROM code, artwork or palette was changed.

## Raw root limitation

The root `/m02_03.fls` has raw palette/pixel storage. V310 proves the original
generic stream parser accepts its metadata and256x192 movie canvas. Supplying
its raw bytes to this compressed queue does not pass: the palette case exhausts
the bounded CPU run and the pixel case reaches an unmapped read. These failed
controlled inputs receive no decoder, GPU or gameplay credit.

This does not establish that the file is globally unused or that every possible
raw loader is invalid. Its intended caller/raw payload path, projection and
crop remain unknown. Preserve the original coastal artwork and keep this gate
open; do not repeatedly force raw data through a compressed-only test.

## Failed evidence and scope

Retained failed assumptions: stale movie heap, strict full-length EOF reads,
compressed slot size used as output size, and nonoverlapping upload requests.
Their JSON reports remain under `work/analysis/fls_payload_v311/` with explicit
rejected names. The earlier519/520 run is retained; it is superseded by the
complete520/520 run after the native queue semantics correction.

No GPU transfer, palette-bank assignment, alpha blending, projection, screen crop
or physical controller input is credited here. Earlier actual movie captures
continue to provide their separately scoped display evidence. Raw/legacy
consumer discovery, hidden Gallery scenes, occupied weapon/armor, alternate
conditions and all18 plaque/hint entries remain open. Low resolution Online
screenshots remain exempt by the user's instruction.

No new ROM or patch is needed for this checkpoint. V309 stays the registered
combined candidate with its unchanged exact patch. Both audits and progress
documents record the native results. The full graphics goal remains incomplete;
revisit older record-based checks at actual completion.

Evidence and scripts:

- `work/analysis/fls_payload_v311/all_compressed_proof.json`
- `work/analysis/fls_payload_v311/largest_case.json`
- `work/analysis/fls_payload_v311/exploration.json`
- `scripts/research_fls_payload_v311.py --all`
- `scripts/record_fls_payload_v311.py`

Focus next on original texture/view composition and genuine raw/virtual resource
callers. CPU byte equality alone cannot certify every screen's final appearance.
