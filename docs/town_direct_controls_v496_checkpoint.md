# V493-V496 stack rendering and draw-path controls

Status: rejected research prototypes; no production change. V484 remains current,
SHA-256 `f2036bafc3736a353cb0a2de8f40bd5eee8bed3cd16e779f68e3ebb1914b875c`.
No new playable candidate, reconstructable release patch or canonical promotion.

## Stack bitmap design

The five stock-name pointers are captured from the original town loop using SL,
its compact displayed-row index. The count is reset before each stock update.
The original numeric bitmap binding and72-row view are restored; the inherited
124 full English names and all other graphics/script payloads are preserved.
A temporary96x12 four-bit bitmap renders each complete name at five-pixel advance.
The prototypes attempt to compose each row through the game's native interfaces.
No persistent allocation or free is added.

- V493 hooks the primary composed-view virtual table entry. V494 instead hooks
  the composed-view function entry with a trampoline for the original instruction.
- V495 hooks the lower descriptor composition API at020D470C, forwarding its
  original register and stack arguments. Its source view has explicit bounded
  secondary-view metadata;832 stack bytes contain the bitmap, view, context,
  descriptor and minimal virtual table.
- Code uses fixed SDK padding plus the now-unreachable lazy allocator's owned
  commodity-name tails. The compact helper's first32 bytes remain for price UI.
  All autoload section extents and all non-ARM9 ROM components remain exact.

The native verifiers pass all124 independent font masks, complete first/final
letters, source-view canaries, stock count/capture bounds and register/stack ABI.
The isolated virtual composition destination is a bounded stub. Its passing
arguments and masks do not prove that the actual game uses that interface to
draw the visible town labels.

## Actual rejection gates

All three variants have the same observed outcome under matched cold boots:

| Test | Result |
| --- | --- |
| M28 substituted into M20;6000 frames | All3047 Hodram name-card pixels match at3700 |
| Genuine Istanbul battery save;5900 frames | Stock labels missing;31 of62 sampled whole frames differ |
| Fresh New Game/title/story/town/help;21200 frames | No terminal crash;55 of56 whole-frame hashes match |

The different fresh frame15200 loses town stock labels in the stock column.
The town differences begin at2900 and continue through5900; not every difference
is confined to the final stock-column rectangle during transitions. The complete
per-frame pixel counts and bounds are retained in the proof. None of these
variants is a release fix. Positive movie masks do not compensate for lost labels.
The M28 substitution is research evidence, not normal ending/unlock verification.

## Dispatcher diagnostic V496

A bounded hook records96x12 rectangles passed to the established framebuffer
dispatcher at the call02006BDC. It restores every original input before delegating
to the original dispatcher. Native matching/fallback probes preserve all command
bytes, inputs and stack. Actual Istanbul captures match all62 V484 frames exactly.
The executable helper remains exact in the terminal ITCM export, but no matching
rectangle is recorded. This does not prove that the dispatcher was never called;
the command's address or dimensions may differ from the filter assumptions.

Next work must establish the actual visible stock-label consumer and its command
layout, including stack-resident commands and any deferred composition, before
replacing the shared numeric atlas expansion. V497 is a separately preserved
broader address/command trace, retaining the original rendering behavior.
Its address window includes RAM mirrors and stack locations through027FFFC0,
without a width/height filter. It also records zero commands and preserves all62
town frames; its helper remains exact in the terminal ITCM export. These results
leave the live consumer unresolved. The trace proof is
`work/analysis/town_dispatch_trace_v497/control_proof.json`.

## Reproducibility and retained scope

- Preparation/native verifiers: `scripts/prepare_town_direct_labels_v493.py`
  through`v495.py` and `scripts/verify_town_direct_native_v493.py` through`v495.py`.
- Matched reports/manifests: `work/analysis/town_direct_labels_v493` through`v495`
  and their corresponding`work/emulation_v193` folders.
- Dispatcher trace: `scripts/prepare_town_dispatch_trace_v496.py`,
  `work/analysis/town_dispatch_trace_v496`.
- Combined verifier: `scripts/verify_town_direct_controls_v496.py`.
- Combined proof: `work/analysis/town_dispatch_trace_v496/control_proof.json`.
- All eight preparation/verification scripts pass Ruff.

All22 historical requirements and all18 incomplete plaque entries remain in the
audit. No requirement or hidden context is cleared by these controls. The full
graphics goal remains active. At actual completion, revisit older record-based checks.
