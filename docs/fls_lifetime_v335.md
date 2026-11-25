# Continuous native FLS resource lifetimes V335

V326 remains unchanged, SHA256
`fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1`.
No ROM, graphics, patch or release-profile change.

## Original continuous execution

Each parsed movie object now advances continuously through its original update
parent020FD478. The native timeline, per-frame cache aging, loader, allocators,
decoder worker and completed-job upload service run in their original order.
This replaces the previous fresh-object-per-combination lifetime assumption.

The original outer loop tests terminal state3 before further drawing/services.
The fixture follows that stop condition, then calls its original resource cleanup
at020FDF00. Inspection establishes that cleanup frees texture/palette keys and
cancels matching queued jobs; it does not queue new loads. General object
destruction, filesystem teardown and the caller's remaining UI reset are outside
the tested resource cleanup segment.

Geometry drawing and VBlank wait are deliberately excluded. LCDC memory and
aligned immediate32-bit DMA follow the prior explicit model. Hardware timing,
GPU aliases/fetch and framebuffer processing are not modeled. Captured globals
and native heap initialization remain supplied runtime contracts.

## Complete lifecycle results

All15 current-English and clean-Japanese lifetimes reach original terminal
state3. Per version they execute **45,058 native updates**, with **528 allocations
and matched frees**. **354 previously freed keys** are reallocated. Up to13 texture
allocations coexist; their live intervals never overlap.

Current/source allocation/free event sequences, intervals, reuse decisions,
terminal states and pending-job cleanup match exactly. Every original update,
service and cleanup returns with saved registers/stack preserved. Original
lifecycle, loader, allocator and cancellation code ranges are source-exact.
After cleanup, no tracked live texture/palette keys or pending jobs remain.

This verifies native CPU resource release/reuse and job cleanup under the declared
model. It does not prove GPU-visible data during transitions, timing/races or
complete rendered-frame correctness. Different compressed bytes may require
different transfer counts; these counts are not incorrectly required to match.

The raw root's generic timeline also ends with no allocations in this path.
Its intended real caller/raw loading/usage remains unknown; no global-unused
or actual root-playback claim is made.

## Remaining goal and evidence

Both graphics audits, requirements ledger and progress documents record the
result. Continuous GPU data fetch, bank aliases, timing, viewport/depth clipping,
alpha blending, final pixels and actual ending/Gallery playback remain open.
All18 plaque/hint entries and Armor/Weapon variants remain incomplete. Other
legacy/gameplay requirements stay open; low resolution Online images remain
exempt. The graphics goal continues; revisit older record-based checks at actual
completion.

Evidence: `work/analysis/fls_lifetime_v335/all_lifetimes_proof.json`, `summary.json`,
M22 exploration, progress and run log. Reproduce with
`scripts/research_fls_lifetime_v335.py --all` and `scripts/record_fls_lifetime_v335.py`.
Focused Ruff passes. The process ended normally with exit0.

These are controlled continuous CPU lifecycle tests, not movie playback,
a complete route or physical-device verification.
