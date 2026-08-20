# DeSmuME runtime dialogue tracing

This workflow identifies the live ARM9 code that consumes standard-dialogue
bytes. It is specifically meant to replace speculative static patches for the
newline, indentation, and dropped-first-glyph problems.

## Known-good trace fixture

- ROM: `out/dialogue_live_safe_v3.nds`
- Savestate: `dialogue_live_save_v3.dst`
- Emulator: DeSmuME 0.9.13 x64
- Lua script: `scripts/desmume_dialogue_renderer_trace.lua`
- Output: `work/dialogue_renderer_trace.log`

The savestate was verified offline. Its ARM9 RAM contains:

| Text marker | ARM9 address |
|---|---:|
| `Prince Henry and Duke Leon` | `0x0218F362` |
| `Behold, the Carteira` | `0x0218F4DF` |

## Running the trace

1. Open `out/dialogue_live_safe_v3.nds` in DeSmuME.
2. Use **File > Load State From...** and select
   `C:\Users\chris.r.francis\Downloads\desmume-0.9.13-win64\dialogue_live_save_v3.dst`.
3. Open **Tools > Lua Scripting > New Lua Script Window**.
4. Load `scripts/desmume_dialogue_renderer_trace.lua`.
5. Confirm the Lua window prints `TRACE READY` and the emulator overlay says
   `Dialogue trace ACTIVE`.
6. Advance through the `Prince Henry...` line and the later
   `Behold, the Carteira!` line.
7. Pause emulation and stop/close the Lua script.

The script is read-only with respect to emulated memory. It records memory-read
addresses, ARM9 program counters, and registers around newline/control bytes.

## Why this is the required next step

The rejected static renderer probes modified an address that did not control
the live progressive text path. DeSmuME's Lua hooks expose the instruction that
actually reads each byte, including the LF byte and the first byte after it.
The resulting trace provides a concrete execution address for disassembly and
a later minimal ARM9 patch.

Do not create another renderer ROM probe until this trace has identified and
documented the live reader instruction(s).

## Follow-up: newline resume trace

After the failed renderer experiments, use
`scripts/desmume_dialogue_resume_trace.lua` with the same safe ROM and savestate.
This read-only trace records entry, LF detection, native post-LF advance, exit,
the returned r9 pointer, and the next invocation of `0x020D5404`. Its purpose is
to prove which caller resumes on the guard byte and where the continuation-line
horizontal position is established.

## Cave-safety result

The apparent ARM9 zero padding at `0x02171E48` through `0x02172463` is runtime
data, not a code cave. The cold-boot New Game trace proved live structures at
`0x021723FC` through `0x02172463`. Independent inspection of the known-good
Raphael savestate also proved live structures at `0x02172300` through
`0x0217231F`. No address in the entire file-zeroed tail may be patched.

A future stateless `0x020D550C` experiment is blocked until its helper location
is proven executable and unused with both static and runtime evidence. Merely
finding zero bytes in the ARM9 file does not satisfy that requirement.

## Guard-space cursor trace after the failed inline skip

Cold-boot screenshots proved that consuming the protected space moves the first
continuation glyph to the preceding line. Automatic wrapping remains intact and
flush left. The next read-only trace must therefore measure the guard space's
cursor advance without removing it.

Use `out/dialogue_live_safe_v3.nds`, the known-good Raphael savestate, and
`scripts/desmume_guard_space_cursor_trace.lua`. Advance through `Prince Henry`,
`Surprised?`, and `Not right away`, then stop the script. The output
`work/guard_space_cursor_trace.log` records the cursor at the LF byte, the stored
guard space, and the first following glyph. A later probe may compensate the
six-pixel guard advance only after this trace proves the exact transition.

## Missing `J` draw trace

Both cursor-compensation probes preserved wrapping but dropped the uppercase `J`
from the protected `LF+SPACE+Janus` continuation. The first run of
`scripts/desmume_guard_j_draw_trace.lua` was inconclusive: its broad space/`J`/`a`
filter reached the 200-event limit on unrelated text before the target line. Its
only captured `J` had source context `00 00 4A 75`, not the required
`0A 20 4A 61 6E` sequence.

The trace now hooks both the byte loop at `0x020D54F0` and the draw call at
`0x020D5774`, but records events only when that exact protected `Janus` sequence
is within six bytes of `r9`. Run it against the revoked one-pixel probe solely
for diagnosis, cold-loaded without a savestate. Do not build another renderer
probe until the log proves whether the `J` reaches the draw call and records its
cursor value.

The narrowed run proved that `J` reaches `0x020D5774` as glyph `0x4A` with
cursor `1`; the following `a` reaches the same call with cursor `7`. The source
stream and cursor hook therefore behave as designed, and the `J` disappears in
the virtual draw callback or its clipping path. The trace now also records `r3`
at `blx r3` and dynamically hooks that callback when the protected `J` is seen,
so the next run can identify and disassemble the actual draw implementation.

That callback run identified `r3=0x020D4DA8`; the embedded uppercase `J` bitmap
is nonblank and valid. A first static vtable match suggested inner renderer
`0x020D4FC8`, but the absence of its hooks in the next live run disproved that
class-instance assumption. The ASCII pending-pair dispatch is actually at
`0x020D4FA4`. The trace now reads the live object's vtable, records its
`[vtable+0x20]` target, and dynamically hooks that exact function to capture the
`Ja` rectangle. Do not substitute a same-method static vtable match for the live
object's complete vtable identity.

The live-vtable run confirmed object vtable `0x021603E4` and inner target
`0x020D4FC8`, but the inner-event filter still assumed that `J` was the first
byte of its two-character batch. The trace now accepts `J` in either byte of the
exact target pair, including the likely `[space, J]` case.

The corrected trace captured `[space, J, NUL]` at rectangle `(x=0, y=12)`.
Therefore `J` is rasterized as the pair's second six-pixel cell at `x=6`. The
zero/one-pixel cursor compensation then places `a` at `x=6`/`x=7`, and the
following cell clears or overwrites the `J` bitmap. This is pair-phase overlap,
not missing font data, source consumption, or a failed draw dispatch.

`out/dialogue_guard_pair_phase_probe.nds` tests a record-local phase repair. It
adds an invisible trailing space before this protected LF so the guard completes
the old pair and `J` begins the new pair at cursor zero. Because record 71 has no
padding, `rebuild` becomes the natural one-byte-shorter `repair`; allocation and
ILNK offsets remain unchanged.
