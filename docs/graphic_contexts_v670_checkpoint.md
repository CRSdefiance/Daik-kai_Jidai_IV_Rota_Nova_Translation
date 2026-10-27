# V670: ordinary crew and isolated Grand Race image selections

## Scope and result

The unchanged V666 experimental ROM completes four cold boots: observed and
unmodified baseline versions of the existing 17500-frame crew schedule and
5000-frame Grand Race roster schedule. All50 sampled whole two-screen pairs
match their current baselines, and all50 match the retained V657/V661 captures.
No savestate is loaded. These are targeted automated emulator tests, not a
playthrough or hardware/wireless verification.

| Context | Primitive entries | Exact whole Frame | Exact whole Marker | Other headers |
|---|---:|---:|---:|---:|
| Ordinary crew allocation |309852|42569|2530|264753|
| Isolated race roster |27400|5093|0|22307|

The previously verified V669 host observer and source contract remain byte
identical. It records the original scaled, corner and tiled primitive arguments
without modifying emulated state. Complete-file comparisons distinguish Frame
and Marker despite their identical20-byte headers. Every recorded guard passes;
the private opcode slot is restored and the pinned core file stays unchanged.
Entry records establish source selection, not individual call completion or the
survival of every source pixel after clipping and subsequent paints.

## Fixture disclosure

Crew allocation uses the original cartridge-save donor and ordinary inputs with
no live gameplay fixtures. The race case repeats V661's explicitly isolated
four-card receive-ring/readiness fixture. Its201 updates affect only the first
212 bytes of each of four512-byte receive slots and one readiness halfword.
Every update verifies the complete RAM change set. The last update restores all
declared fields; observed and baseline event logs are identical. Original ring
counters are untouched. This verifies local roster UI, not actual wireless peers,
an earned unlock, race readiness between devices, or a race outcome.

## Remaining evidence gap

None of the selected whole-Frame footprints intersects the five miniature
Done/Rank/Cancel/Pick Cargo/Pick Ship cells in these schedules. The separate
Confirm file is not selected through these three primitives. This bounded
negative result does not establish global non-use. Embedded atlas aliases,
other primitives, other game contexts and all six control contexts remain open.
Other headers are retained without assigning filenames from metadata alone.

No graphics, ROM, patch, registry or release pointers change. All18 original
plaque/hint entries remain incomplete and all22 historical requirements remain
exact. The wider graphics goal, source-restoration reviews, legacy consumers,
older record checks and final acceptance are still open.

## Evidence

- Verifier: `scripts/verify_graphic_contexts_v670.py`.
- Proof and frozen inputs: `work/analysis/graphic_contexts_v670/`.
- Captures: E Generated/work/emulation_v193/graphic_contexts_v670_*.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V670 Crew and race image calls`.
- Candidate: `out/all_routes_combined_v666_candidate.nds`.
- Candidate SHA256: `706350a55a058b7a87b67d396333ed397dac664ba36ea378161d18fd085ba121`.
