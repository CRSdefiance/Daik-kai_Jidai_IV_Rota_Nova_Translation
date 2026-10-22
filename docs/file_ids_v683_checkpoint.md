# V683: numeric file IDs, direct byte ranges and actual ARM9 stack memory

V682 resolved the known Save/Load RAM-stream callers. This checkpoint addresses
a distinct remaining graphics-search gap: numeric file-ID and direct-range SDK
opens can bypass the filename entry. Production V678, its artwork, translation,
patch, registry and release pointers remain unchanged.

## Actual interfaces and source binding

| Original entry | Recorded input |
| --- | --- |
|020DED50|Filename open: file object and filename|
|020DEDA0|Numeric open: file object, archive pointer and file ID|
|020DEE1C|Direct range: file object, archive pointer, begin/end and fifth stack argument|

The complete selected SDK range and every declared direct caller's argument
context match the clean Japanese code. All loaded main sections and declared
overlays are checked for aligned ARM calls, Thumb calls and stored pointers
to these entries. This census is retained as a bounded static result, not a
closed proof about every computed call target.

All 714 ROM FAT records are checked against the actual file bytes. The observed
numeric IDs are resolved through this exact current table and filesystem map.
File 0's synthetic `/__unnamed__/file_00000.bin` label is a tooling name: the
original ARM9 overlay table identifies it as overlay 0's 6,208 bytes of code.
File 2 is `/sound_data.sdat`. The literal archive name in the recorded objects
is `rom`; no alternative filesystem is silently assumed.

## Correct memory mapping before interpreting the trace

The initial diagnostic read all pointers through the main-RAM mirror helper.
Its registers were valid, but its stack reads were wrong when the stack was
in DTCM. In particular, the direct-range fifth argument appeared as an ARM
instruction rather than its actual `FFFFFFFF` value. Both initial terminal
runs, source, controls and logs are retained as rejected stack-field evidence.

The corrected observer binds the pinned core's `DTCM` and `MDTC` SFORMAT
anchors. The exact original MMU source gives configured 16 KiB DTCM priority
over main-RAM mirrors. Ten explicit precedence/boundary controls distinguish
the two byte sources; crossing a mapped boundary is rejected. Fifteen grouped
native prefix/ABI controls and eight main-RAM mirror controls also pass.
The shared host opcode group is tested with both original targets present.

The first verifier then incorrectly assumed every stack stayed in DTCM. That
rejected verifier/log are also retained. Actual execution uses 28 DTCM entries
and 461 main-RAM fiber-stack entries. The current verifier reconstructs all
DTCM stack fields from the complete captured DTCM and checks main-RAM stack
fields against the initial trace's unchanged complete-WRAM hash and identical
bounded reads. It does not reinterpret a main-RAM fiber stack as DTCM. No ROM,
native result or emulator output was altered to satisfy these corrections.

## Completed sequences and bounded result

Two corrected cold boots finish the original V681 schedules. Their original
unmodified-core baselines are reused only after pinning the baseline reports,
ROM/core hashes, full input schedules, save inputs, every screenshot and final
RAM. There is no new baseline run presented as fresh work.

| Sequence | Frames | Full RGB screenshot pairs | Filename entries | Numeric-ID entries | Direct ranges |
| --- | ---: | ---: | ---: | ---: | ---: |
|Ordinary Rafael New Game|4,000|16|39|46|4|
|All four Event Scenes carousels|38,600|177|195|201|4|

All 193 sampled complete two-screen RGB pairs and both terminal 4 MiB RAM
states match the retained unmodified baselines. All 489 callbacks preserve
the complete CPU prefix, 4 MiB WRAM, 16 KiB DTCM and DTCM configuration;
host interpreter pointers are restored and the core DLL remains exact.
The corrected and initial traces repeat all frame/kind/register/LR fields.
All 234 filename entries also repeat the independent V681 trace exactly.

Each filename entry has its matching numeric open in the original wrapper,
with the same file object and exact file ID. The 13 numeric requests beyond
those wrappers are:

- Seven in ordinary New Game: three overlay-0 opens and four sound-data opens.
- Six in Gallery: three overlay-0 opens and three sound-data opens.

All eight direct ranges equal complete ROM header-declared tables: one FNT,
one FAT and two ARM9 overlay-table reads per sequence. They are not unclassified
graphics byte ranges. All eight fifth arguments are `FFFFFFFF`, now verified
against the actual DTCM stack.

Thus numeric-ID/direct-range opens do not explain an additional graphics load
in these two sequences. This closes that specific untraced-interface question.
The trace records entries, not successful-open return values. It neither proves
global non-use of unresolved artwork nor visits its unknown actual contexts.
Other schedules, cached/indirect sources and other interfaces remain possible.

Ordinary New Game has no save, savestate or gameplay fixture. Gallery uses the
unchanged authorized system-unlock donor/manifest; its access is artificial and
not an earned unlock. The four-frame current review sheet was opened and shows
the title, opening, initial logo and final Maria Gallery selection without a
new defect in these selected views. Prior V681 complete Gallery source/caption
checks remain separate; this checkpoint adds interface and baseline evidence.

## Artifacts and preserved goal

- Producer: `scripts/trace_file_ids_v683.py`; corrected controls run with
  `python -m scripts.trace_file_ids_v683 controls`.
- Verifier: `scripts/verify_file_ids_v683.py`.
- Source contracts, controls, failed diagnostic assumptions, proof and review:
  `work/analysis/file_ids_v683/` on E.
- Initial and corrected terminal captures:
  `E:/Rota Nova translations/Generated/work/emulation_v193/file_ids_v683_*`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V683 Numeric file IDs`.
- V678 SHA256: `d1aaf37bcb7dec218d200a5fa72a6c58e0fb50ab85a8bcb7766d4e749903e341`.

All 18 original plaque/hint entries remain incomplete; all 22 historical
requirement objects retain exact scope. Six controls, eight village cards,
actual comic/legacy contexts, material restoration, older checks and final
acceptance remain open. The next useful graphics investigation must go beyond
the specific filename/numeric/range paths and schedules already checked.
No guide promotion, new candidate, canonical promotion, commit or push occurs.
Online exclusions and brown-mark preservation stand. This is progress; the
full graphics goal remains active.
