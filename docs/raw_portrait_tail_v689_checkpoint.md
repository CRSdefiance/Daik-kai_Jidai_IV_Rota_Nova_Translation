# V689: what the chooser does after reading legacy raw portraits

## Result

The original captain chooser reads SLACKIMG blocks 14–17, but its following
view-construction loop does not consume those raw pixels. It constructs separate
104×136 type-4 views owned by `personbustup00.pxl` through `personbustup03.pxl`.
This resolves a specific consumer-association question; it does not prove that
the raw portraits are globally unused or that their display/palette is verified.

The original 22-item ledger was reviewed to choose this follow-up. Its legacy
storage and actual-consumer requirements remain intact. Eleven historical legacy
gates are not eleven newly discovered untranslated pictures.

## Actual cold-boot evidence

A new V685 ordinary 4000-frame cold boot uses the established 203-action schedule
with no battery save, savestate, unlock, inventory, location or other live fixture.
A read-only host observer records four actual raw-call entries, four returns and
the following loop boundary. All 9 callbacks preserve the CPU prefix, complete
4 MiB main RAM, 16 KiB DTCM and its mapping configuration. Private host dispatch
slots restore, and the emulator DLL remains exact. Fifteen host-prefix and eight
mirror-read controls pass. The process ends normally with exit 0.

All four requests are `(14+i,02233040,0,0)`. Every complete 14144-byte returned
payload matches both current and Japanese-source blocks. Entries/returns occur
at frames 1219–1220, in actual parent 02192500. This is stronger than merely
observing a filename or finding a payload in a later scratch snapshot.

Twenty-one complete two-screen frames match the retained V685 ordinary baseline.
Full terminal main RAM matches the version-bound retained 4000-frame V678 control;
that control's ROM/report identities remain disclosed. The selected actual title,
biography and confirmation screens were opened and visually reviewed.

## Connected native tails and independent controls

Each actual return state is replayed through the following original chooser code
until the next raw call entry, or the loop boundary for the fourth case. These
replays use captured registers, CPSR, full main RAM and actual DTCM. No function,
SDK read, native return or drawing operation is bridged.

| Raw block | Distinct original instructions | Next boundary |
|---|---|---|
|14|401|Next raw read entry|
|15|401|Next raw read entry|
|16|413|Next raw read entry|
|17|117|Loop completion at 0209EE94|

All executed instruction words match clean Japanese code. In all four cases,
every following general register, CPSR, all main RAM and all DTCM match the actual
next captured boundary exactly. There are no raw-buffer reads or writes in these
segments, including the main-RAM mirror classification with DTCM precedence.

Four isolated counterfactual controls replace each raw payload with a known
14144-byte pattern. Native registers, CPSR, views and other RAM/DTCM remain exact;
the complete resulting RAM equals the expected real snapshot with only that
explicit input region replaced. No altered ROM or emulator screenshot is made.
An original native two-instruction word getter calibrates the read detector with
one actual four-byte read and its expected 12345678 return.

The complete actual 48-byte constructed views bind their initialized resource
filenames independently. Reserved words are retained, including a nonzero word
in one view, rather than assumed zero. Dimensions alone do not identify the raw
payload with these PXL resources or prove an old palette is interchangeable.

## Consequence and limits

Do not grant raw SLACK14–17 display credit from this chooser loop, or substitute
their pixels/palette for the separate PXL views. The first three payloads are
unread by these segments before the next load. The final block17 remains in
scratch at loop completion; subsequent code/other readers are outside this
specific result. No global unused-art or complete native-format claim follows.
Future raw-art work needs a later/different actual consumer, rather than another
test that only confirms these four archive reads.

During the source-art review, `うみうし → Sea cow.` was rechecked. V183 explicitly
documents it as a comic adaptation linking the previous bullfighter line and
the depicted cow-like horns. The standard referent is a sea slug; the comic
wording is an editorial inference, not an official species/name claim. Existing
wording is retained after reading that context. No new translation defect is
recorded from the isolated dictionary reading. Original creator credits and
the user's preserved brown marks remain unchanged.

## Storage and remaining scope

- Producer: `scripts/trace_raw_portrait_tail_v689.py` (frozen before the live run).
- Replay: `scripts/replay_raw_portrait_tail_v689.py`.
- Independent verification: `scripts/verify_raw_portrait_tail_v689.py`.
- Analysis: `work/analysis/raw_portrait_tail_v689`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V689 Raw portrait tails`.
- Three unmodified ordinary screenshots: `E:/Rota Nova translations/Screenshots/Guide candidates/V685 New Game`.
  These are guide candidates; publication approval is not inferred.

Current ROM remains experimental V685, SHA256
`83e7bdc7c4926ad69eb04704e8327aba50d0fe29b00cce7f5f59d4be8c203150`.
No ROM, manifest, patch, registry, canonical baseline, release pointer or art changes.
All 18 original plaque/hint entries remain incomplete and all 22 historical
requirements remain exact. Raw comics, legacy/standalone art, six control
contexts, eight cards, source-material review, older wording checks and final
acceptance remain open. This is progress from actual new evidence, not goal
completion or a full route/hardware claim.
