# V690: initialization return and a live final-raw-buffer control

## Result

V689 stopped at the chooser's four-portrait loop boundary. The remaining original
initialization code also returns without reading or writing the final raw portrait
payload. A live isolated replacement of that payload leaves all 21 sampled
ordinary Rafael New Game screens and the complete 4000-frame terminal main RAM
identical to the control. This extends the evidence for this chooser path;
it does not prove raw artwork globally unused.

## Two terminal cold boots

Both tests use the unchanged V685 ROM and the same established ordinary input
schedule. Each reaches 4000 frames and terminates with exit 0. Neither loads a
battery save or savestate. The control observes only. The second test makes one
explicit, version-guarded 14144-byte in-process WRAM write at the actual last raw
read return, PC 0209EDEC, captain-loop index 3, parent 02192500.

The source bytes at 02233040 must match the exact original SLACKIMG block17
before replacement. The deterministic diagnostic pattern has its own hash in
`isolated_raw_buffer_fixture.json`. Full before/after RAM snapshots prove the
change is restricted to that input region. CPU, DTCM, mapping configuration,
native code, ROM and other RAM remain unchanged by the fixture operation.
The synthetic case is explicitly declared in its capture report and run contract.
Its images are test fixtures and receive no guide promotion.

Each run captures the four raw entries, four returns, loop boundary and actual
initialization return: 10 callbacks per run. The observer restores all private
host dispatch pointers and preserves the emulator DLL. Twenty native prefix
cases and eight memory-mirror controls pass. The old generic checker's console
label still says 15; the authoritative stored list contains 20 verified cases.

All 21 complete two-screen fixture/control pairs match. The 21 complete control
frames and terminal main RAM also match the retained V689 ordinary run. All 20
observed CPU prefixes match between cases. At loop completion and initialization
return, full case-to-case RAM differs only by the declared diagnostic input,
and all DTCM is exact. By frame 4000 the complete main RAM states are identical.
The exact later overwrite point or all possible buffer readers is not inferred.

## Complete remaining initialization

The actual stack frame supplies the saved return PC 0209DC90. Starting at the
captured loop boundary 0209EE94, 873 distinct original instruction words execute
without call, SDK, input or native-return bridges. Both actual cases reproduce
every next general register, CPSR, saved register, stack pointer, complete 4 MiB
main RAM and complete 16 KiB DTCM exactly at the captured real return.

Neither replay accesses the raw payload, including the classifier's main-RAM
mirror/DTCM-precedence rule. Original instruction words remain byte-identical
to the Japanese ROM. This is the whole remaining initialization segment; the
earlier V689 tails retain their separate evidence.

The paired actual title, biography and confirmation images were opened and
visually reviewed. This does not compare every intermediate console frame.
It verifies the sampled initial Rafael displays, not every captain update,
the comic viewer, another raw consumer or native legacy palette semantics.

## Consequence and next work

Do not identify raw SLACK14–17 with the chooser's separate personbustup00–03
PXL views merely because both have plausible portrait dimensions. The raw reads
are not consumed by the measured view-building/remaining initialization code.
All-captain selection updates, later/different consumers and legacy/comic
display relationships remain separate questions. The next useful chooser test
is actual cycling through the other captains, rather than repeating the same
four archive-read assertions.

## Evidence and unchanged scope

- Producer: `scripts/trace_chooser_raw_independence_v690.py`, frozen before both runs.
- Verifier: `scripts/verify_chooser_raw_independence_v690.py`.
- Native helper: unchanged `scripts/replay_raw_portrait_tail_v689.py`.
- Analysis: `work/analysis/chooser_raw_independence_v690`.
- Runs: E Generated/work/emulation_v193/chooser_raw_independence_v690_control/poison.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V690 Chooser raw independence`.

Current ROM remains experimental V685, SHA256
`83e7bdc7c4926ad69eb04704e8327aba50d0fe29b00cce7f5f59d4be8c203150`.
Production ROM, manifest, patch, registry, canonical baseline and release pointers
remain unchanged. All 18 plaque/hint entries remain incomplete and all 22 original
requirements remain exact. Other raw/legacy/control/card/material/older-record
and final acceptance gates remain open. Full graphics goal remains active.
No new ROM, guide promotion, commit or push.
