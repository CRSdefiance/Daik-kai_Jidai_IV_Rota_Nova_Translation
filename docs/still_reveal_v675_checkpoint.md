# V675: Maria court reveal from original paints and actual scanline sources

## Outcome and limits

The specific V674 incomplete comparison at Maria's court reveal is resolved.
The actual picture is `/evstill/evstill084.pxl`, byte-identical to the Japanese
ROM. The original horizontal-blinds routine and its actual pre-paint inputs
reproduce all nine thickness states. Complete pre-render source compositions
match all 22 sampled upper screens, including two mixed-phase frames. No ROM,
artwork, palette, text, patch, registry or release-pointer change was needed.

This is targeted automated emulator evidence. It does not establish a full
Maria opening/route playthrough, every transition or physical-device behavior.
M26's two wedding illustrations still have unresolved story ownership. The six
small-control parents, eight village-card contexts, legacy/comic/restoration
gates, plaque material acceptance and older record checks remain open. All 18
plaque/hint entries remain incomplete and all 22 historical objects remain exact.

## Actual inputs and independent painting

The original upper iterator starts at `020D32B8`, instruction `E5955004`, with
R4=`023117C4` and the first-list sentinel R5=`023117D0`. A private host interpreter
filter copies actual CPU, WRAM, ITCM, DTCM, I/O and LCDM state immediately before
that instruction. It does not write emulated state or load savestates. Twenty
actual entries occur in the selected 54-frame set; selected frames without a
redraw do not receive invented entry snapshots. Nine native filter controls
verify host ABI, flags, stack, original-handler invocation and selection guards.
The pointer is restored and the pinned core file remains exact.

The actual effect thunk is `02029150`; its original painter is
`020280CC..02028288`, and its blocking update loop begins `0202828C`.
The actual rectangle is 0,0,256,192, orientation 0 and duration 64.
The painter draws successive eight-pixel bands with thickness
`floor(progress * 8 / 64)`. These complete bodies, the thunk and iterator spans
match the Japanese ROM.

Twenty replays use the exact before-entry RAM, TCM and original overlay0 with
source-bound memory mapping. Every executed instruction matches the registered
candidate. All 983,040 output words match an independent ROM palette/index model;
all output bytes are assigned before reading them. All nine phases 0 through 8
are covered. Eight wrong-thickness controls each detect over 5,000 differing
pixels. Complete resident court palette/indices match the ROM in all 20 inputs.

The trailing output guard remains intact. The preceding 16 bytes are the end of
the separately owned lower canvas, also painted by this traversal: all eight
writes bind to original tiled painter `01FFAF98`, exact addresses, widths and
source-state values. They are not incorrectly treated as an unowned guard.

## Display timing and source-bound RGB

Three V675 4,000-frame cold boots use the same authorized isolated system-unlock
save and original New Game inputs as V674. No new gameplay fixtures are applied.
Twenty-five complete screen pairs match the entry-capture run for each of the
two scanline runs, and 14 pairs match V674's unmodified-core baseline: 64 exact
two-screen comparisons. All four terminal 4 MiB RAM states are exact.

The first unchanged V659 observer captures bank D/main-engine rows. In this
post-movie scene they reproduce the lower screen, not the upper screen. Its
result and exact superseded runner are retained. A private extension adds only
read-only bank C/sub-engine rows to the same original RenderLine observation.
Both source rows, complete I/O and CPU registers are retained before rendering.
Original HBlank/VCount call sites and twelve relocated-prefix controls pass;
all detours are restored. Bank C register `84`, sub BG3 settings, identity affine
mapping and disabled blend/brightness bind the actual upper source.

All 4,224 sampled source rows and 1,081,344 upper RGB pixels match. Twenty frames
are whole original band states, selected from actual pre-render source words,
not fitted to a PNG or later buffer. Two frames contain different phases above
and below a transfer boundary:

| Frame | Native new phase | Previous phase | First observed upper DMA row |
| --- | --- | --- | --- |
| 3762 | 1 | 0 | 68 |
| 3786 | 4 | 3 | 143 |

The mixed-frame boundary comes from CPU state before RenderLine, not from pixel
fitting: original `01FF98D4` follows the channel 3 trigger; R6=`022F9794`,
R5=`06200000`, R4=`8000C000`, R7=3 identify the upper bitmap transfer. Before
that transfer the old phase applies; afterward the new phase applies. These
inputs predict all 98,304 source words and every displayed RGB pixel across the
two mixed frames. Every sampled CPU instruction in those frames matches clean.
This is not an independent simulation of every CPU/DMA clock cycle.

At V674's frame 3800 the display reads phase 5 while the next native paint uses
progress 50 / phase 6. Comparing that next paint directly with end-of-frame
state had compared different stages. No frame delay is fitted and no pixel is
excluded. All sampled lower source rows also reproduce their separate screen
as a diagnostic; they are not used to prove upper composition.

## Rejected assumptions retained

- Bare post-frame replay omitted original overlay0 and stopped in unmapped code;
  the successful replay supplies actual TCM plus the original overlay.
- The guessed entry instruction and shared cache for two `9REG` shapes were
  rejected before their failed capture attempts could run the hooked core.
- An immutable preceding guard was inappropriate because it belongs to the
  lower canvas; exact original ownership and writes replace that assumption.
- One whole reveal phase per displayed frame was contradicted by two mixed
  frames. Actual CPU transfer inputs resolve them without waiving pixels.
- The earlier main-only scanline observation describes the lower display here.
  It receives no upper-display credit.

Failure logs and failed-attempt artifacts remain in the analysis/archive.

## Evidence

- Analysis: `work/analysis/still_reveal_v675`.
- Proof: `proof.json`; paired review sheet: `actual_reveal_states.png`.
- Run folders: `still_reveal_v675_before_iterator_v3`,
  `still_reveal_v675_scanlines` and `still_reveal_v675_scanlines_both` under
  `E:/Rota Nova translations/Generated/work/emulation_v193`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V675 Maria still reveal`.
- Latest compiled experimental ROM: `out/all_routes_combined_v666_candidate.nds`.
- SHA256: `706350a55a058b7a87b67d396333ed397dac664ba36ea378161d18fd085ba121`.

The preceding status-only turn was no progress. This continuation verifies the
original paints/display and updates the authoritative evidence: progress.
No guide promotion, user acceptance, canonical promotion or goal completion.
