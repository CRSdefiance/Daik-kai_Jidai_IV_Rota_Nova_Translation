# Original confusion event and party dispatch V389

Evidence checkpoint on unchanged V388. No ROM, patch, sprite or emulator progress
was changed. The graphics goal and all 18 plaque/hint audit entries remain open.

## Original event context

The original hazard branch `02072ED4..02072F38` selects the descriptor at
`02116FA0`, containing messages2404–2408 about a ship caught in a tornado. For the
flagship it loads callback `02065830` from literal `02073120` and passes it to
the original whole-party dispatcher `02065B08`. Other ship cases call the same
effect directly after the original actor eligibility check.

The effect changes Health0 (Healthy) to Health1 (Tired), preserving an existing
nonzero health condition. Mood0–4 changes to Mood5, whose Japanese source is 混乱
and whose reviewed V388 label is Confused. This confirms the mental-condition
context and supplies a concrete event to pursue in normal gameplay. A generic
Tavern action is not credited as a way to obtain this particular effect.

## Native integration proof

`scripts/verify_tornado_condition_dispatch_v389.py` runs the original dispatcher
and callback against genuine read-only actor/global data from the V379 cold-boot
voyage export. In an isolated Unicorn machine, current V388 code/data is loaded,
the captured main RAM is imported, and only the three reviewed current condition
lookup pointers are adopted. This explicit contract reconciles old captured globals
with the current labels; it is not injected into the running emulator or a save.

Five callback invocations cover four distinct captured actors. One started with
Healthy/Upset; the other three with Healthy/Normal. All finish with Tired/Confused.
Every actor byte outside the original two condition fields remains exact. Native
Health/Mood getters return the complete current strings. Original dispatcher,
effect code, stack and saved-register checks pass; targeted Ruff passes.

Proof: `work/analysis/condition_events_v389/party_dispatch_proof.json`.
The direct-call investigation remains in `source_callers.json`; that initial scan
alone missed the flagship's indirect callback and is not treated as a complete
call graph. A separate message descriptor also mentions lightning, but its full
calling context has not been mapped here and receives no event-dispatch credit.

## Scope and next work

This resolves the original source association and full party-effect execution in
the supplied captured context. It does not prove a genuine tornado encounter,
new condition display through the whole emulator/GPU, all hazard eligibility,
occupied equipment, unlocked Gallery/endings or other pending graphics consumers.
Those requirements stay in the ledger. No simulated image is added to the guide.

V388 remains the registered experimental candidate, SHA-256
`1629f2823aa953507c0ec3029556701509fd28d364824aefb6ce2aa61109abcc`.
Its exact patch and full handoff remain in `docs/condition_labels_v388_checkpoint.md`.
Generated artifacts reside on E through the verified storage junctions. Low-resolution
Online screenshot translation remains user-exempt. Revisit older record-based checks
when the full graphics goal is complete.
