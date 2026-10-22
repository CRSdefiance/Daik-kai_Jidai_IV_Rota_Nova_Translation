# V681: actual Gallery file requests and complete live raw portrait returns

V680 made progress through controlled raw16 scaling and caption-edge checks.
This checkpoint observes actual file activity in the complete Event Scenes
sequence and an ordinary New Game. It changes no ROM, graphics, translation,
palette, registry, patch, save donor or release pointer. V678 remains current.

## Original native targets and read-only observation

| Location | Actual recorded operation |
| --- | --- |
|020DED50|SDK filename-open entry; complete CPU prefix, original filename and file-object prefix|
|0204704C|Original SLACK archive wrapper entry; block, destination, offset and length|
|0209EDEC|Known original caller immediately after raw read; complete loaded payload|

All relevant original code ranges match the clean Japanese ROM. Three private
host interpreter slots preserve registers/flags/stack, call a bounded diagnostic
callback, and tail-jump to their unchanged original handlers. They are restored
before freeing the filters. The DLL file remains pinned and unchanged.

Every callback verifies the complete CPU prefix and4MiB WRAM unchanged by
observation. No game instruction, file read result, source buffer, portrait,
quest state or graphics is substituted. Filename reads account for the original
DS main-RAM mirrors using the pinned MMU source mask003FFFFF; cross-edge reads
are rejected. Fifteen native host controls exercise all three target selectors,
disabled/wrong-PC/word/argument behavior and full original return/ABI preservation.
Eight independent bounded-read controls check accepted mirrors and rejections.

These are actual **entry requests**, not observed successful-open return values
or a trace of every possible SDK/file-ID interface.

## Four completed cold boots

| Case | Frames per run | Whole two-screen observed/baseline pairs |
| --- | ---: | ---: |
|Ordinary Rafael New Game|4000|16|
|Complete four-route Event Scenes Gallery|38600|177|

Both observed runs and both unmodified-core baselines finish normally. Each
pair has identical complete sampled RGB screens and identical full terminal RAM.
No savestate is loaded. Ordinary New Game uses no battery save or gameplay
fixture. Gallery uses the previously authorized byte-exact checksum-valid system
unlock save; its artificial access is disclosed and no earned unlock is claimed.
The original donor and fixture remain unchanged.

## Positive raw-reader result

Ordinary New Game produces47 recorded events:39 filename requests, four original
raw-wrapper entries and four original caller returns. The actual block order is
14,15,16,17; destination02233040, offset0, whole14144-byte blocks. All four complete
returned payloads match the exact source archive. The first three return during
frame1219; the fourth returns during1220. This is actual original runtime loading,
with no SDK bridge or forced selector. It complements the earlier isolated loop
replays. It does not show raw comic block19 being read or identify those portrait
bytes as the subsequently displayed loose-PXL portraits.

## Event Scenes loading and complete current displays

Gallery records195 actual filename requests,178 distinct paths. The159 distinct
event-photo paths exactly equal the current original Gallery tables' visible
photo set, and every selected photo has a matching preceding filename request.
All four original carousels traverse164 positions and four wrap returns.

The established source-linked Gallery verifier runs unchanged on V678 and the
new captures. It validates every complete photo at its declared five-bit color
comparison (8,060,928 pixel comparisons), every complete caption/heading/route
description, runtime caption pointers in all164 selected RAM snapshots, popup
labels, arrow-safe title bounds and the four wraps. Current observed/baseline
RGB equality is full precision and covers177 sampled two-screen frames.

The12-frame review sheet covers first/middle/last selections across all four
routes and was opened. No new cut caption, lost edge letter or damaged photo
was identified. These are targeted automated emulator tests, not route completion
or hardware/wireless verification.

Actual early requests distinguish `/FLS/logo.fls` and `/FLS/M28.fls` from the
unresolved loose `/_pxl/logo.pxl`. Ordinary New Game additionally requests M20.
The Frame and Marker PXLs are requested; this file trace does not identify which
miniature cells a renderer selects from Frame.

The Gallery sequence makes no raw-SLACK-wrapper entry and requests no SLACKIMG
archive through this filename interface. Neither sequence requests legacy
CMMNIMG.DK4, copyright.pxl, the loose logo.pxl, ship_eurL.pxl, startmenu0.pxl or
kakutei.pxl through this interface. This is a bounded runtime result, **not global
non-use**. Other modes, generated/file-ID interfaces and indirect readers remain
possible. No unresolved legacy/card/control requirement is retired on that basis.

## Evidence and preserved scope

- Scripts: `prepare_file_requests_v681`, `observe_file_requests_v681`,
  `check_file_requests_v681`, `run_file_requests_v681`, `verify_file_requests_v681`.
- Original complete Gallery verifier: `scripts/verify_gallery_carousels_v522.py`.
- Proofs/source contracts/frozen fixture bindings:
  `work/analysis/file_requests_v681/` on E through the analysis junction.
- Four terminal reports, native request logs,177 Gallery screenshots per run,
  selected capture RAM, four actual raw returns and ordinary controls:
  `E:/Rota Nova translations/Generated/work/emulation_v193/file_requests_v681_*`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V681 Actual file requests`.
- Focused Ruff, original Gallery verifier, request/source/baseline verifier and
  final archive checks pass.
- V678 SHA256 remains
  `d1aaf37bcb7dec218d200a5fa72a6c58e0fb50ab85a8bcb7766d4e749903e341`.

All18 plaque/hint entries remain incomplete; all22 historical requirement objects
remain exact. Six small controls, eight village cards, legacy/comic consumers,
source-restoration/material review, older record checks and final acceptance
remain in the active full graphics goal. Online exclusions and brown-mark
preservation stand. No new ROM, guide publication, canonical promotion, commit
or push is performed by this checkpoint.
