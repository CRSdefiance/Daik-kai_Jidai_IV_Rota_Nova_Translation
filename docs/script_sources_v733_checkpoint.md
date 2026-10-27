# V733: actual command execution and resident script sources

The previous turn made progress through V732's complete finite cache-to-first-read
checks. This batch observes the original interpreter during actual Rafael New
Game execution, rather than supplying another isolated command stream.

## Two current, ordinary runs

Two V712 cold boots each complete 4,000 frames with the same normal inputs and
16 requested capture timestamps. Neither loads a battery save or savestate or
uses a gameplay/unlock fixture. One is an unobserved baseline; the other uses a
read-only observer before and after the original command-dispatch call.

The private host interpreter filters select original guest instructions
`02024070` and `02024074`. They preserve host registers/flags and tail-call the
unchanged original handler once. Ten current native prefix/ABI controls cover
the two targets; eight mirror-read and ten DTCM-priority/boundary controls pass.
The exact helper and original emulator MMU/SFORMAT source hashes are pinned.
Configured DTCM takes priority over main-RAM mirrors.

At each callback, the observer verifies that its own work leaves all 128 exported
CPU-prefix bytes, 4 MiB main RAM, 16 KiB DTCM, 32 KiB ITCM and DTCM configuration
unchanged. This is not a full CPU/private-core-state equivalence claim. Both
temporary host slots are restored and the core DLL remains exact. Shared harness,
filter assembler and memory-read helper files are unchanged; the runner uses a
process-local harness proxy.

## Observed command sources

The trace records 41 actual observations: 21 command entries and 20 returns.
Every one resolves to the original SC cache object for route 0, block 44. Its
entire 6,768-byte resident payload matches the registered current ROM at every
observation. There is no unclassified source buffer in this run.

For all 20 returned commands, the source pointer, packet prefix and complete
resident script match at entry and return. The original game changes its world
and display state normally; the test does not require all game RAM to remain
unchanged across command execution. The observed commands include dialogue,
image/display operations and an inline world-state action.

The final command is still awaiting normal in-game input when capture ends. Its
entry source is verified, but it receives no return credit. Both diagnostic
processes are terminal with exit 0; this in-game wait is not a live process or a
reason to restart a run.

These checkpoint observations do not exclude a temporary write followed by
restoration between callbacks, unobserved commands, other script blocks, other
stream builders or ordinary village-card triggers. This is not proof that the
eight cards are unused or that the whole interpreter is read-only. The completed
V727/V732 file/handoff proofs retain their separate scopes.

## Baseline and visual check

All 16 complete 256×384 RGB frame pairs match exactly. Both final 4 MiB RAM
states also match byte for byte. Duplicate final/capture entries at frame 4000
do not increase the unique-frame count. The paired full-screen review was opened;
it shows the same complete opening dialogue and scene in both runs.

One unobserved original frame 4000 is copied to the E drive guide-candidate
folder with its provenance. It has no gameplay fixture and is a candidate for
later guide review, not publication approval. Test records remain separately in
the audit archive.

## Audit and remaining work

The current ordinary-opening source-check scope is complete and carried forward.
Do not replay this same short schedule solely to search for village-card use.
Further consumer work should target other original contexts or trace the actual
image-parent arguments where needed. Original village-card triggers, original
comic playback, small-control/legacy consumers and final overall review remain
open. The full graphics goal stays active.

All 18 original overall plaque/hint objects remain incomplete and all 22
historical requirement objects remain exact. V712 ROM, manifest, patch, release
registry, canonical baseline, art and saves remain unchanged. No rebuild,
promotion, commit or push occurs. Online body exclusions, preserved brown marks
and the older-record follow-up remain in force.

- Runner: `scripts/run_script_sources_v733.py`.
- Observer: `scripts/observe_script_sources_v733.py`.
- Verifier: `scripts/verify_script_sources_v733.py` (all targeted Ruff checks pass).
- Proof/review: `work/analysis/script_sources_v733/` on E through the junction.
- Actual runs: `E:/Rota Nova translations/Generated/work/emulation_v193/script_sources_v733_baseline`
  and `script_sources_v733_observed`.
- Checked archive: `E:/Rota Nova translations/Screenshots/Audit comparisons/V733 Actual script sources`.
- Guide candidate: `E:/Rota Nova translations/Screenshots/Guide candidates/Rafael New Game/V712_frame_004000.png`.
