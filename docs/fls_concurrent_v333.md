# Concurrent native FLS bindings V333

V326 remains unchanged, SHA256
`fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1`.
No ROM, artwork, patch or release-profile changes.

## Source-observed combinations

The complete V312 timeline states contain270 distinct visible slot/texture
combinations across14 compressed movie files. Visibility follows the original
local and global alpha guards; merely active but invisible slots are excluded.
The largest combination has13 visible slots, rather than27 active slots.

Every combination is tested in one fresh native object against both current
English and clean Japanese files:540 shared-object fixtures. Original constructor,
parser, loader, allocator and complete quad-submission code execute. Inputs are
the recorded native poses, frame counters, global controls and captured runtime
globals. Source metadata pointers and dimensions are checked before binding.

The scope covers all260 compressed texture entries. Per version,644 material
instances use643 distinct allocations across the cases; one combination shares
a texture between slots. Testing every combination also covers fewer, larger
textures whose memory demand might exceed the maximum-slot-count scene.

## Native allocation and reuse results

All live texture and palette intervals in each fixture are nonoverlapping.
Native allocation keys are nonzero and belong to the parsed texture records.
Current and clean files produce identical shared bindings and native material/
draw commands. Loader, allocator and quad code ranges are source-exact.

Binding the same visible poses a second time reuses the same cache keys and
queues no additional palette/pixel jobs. This verifies same-state cache reuse,
not complete movie-lifetime freeing/recycling or a safe asynchronous transition.

No production code or graphics changes were needed. Focused Ruff passes, and
the full combination process ended normally with exit0.

## Explicit remaining scope

These are source-derived native binding fixtures. Pending upload jobs are not
drained or composed in this test. V332's separate zero-offset upload fixtures
retain their own scope; neither result is promoted into proof that these shared
bank layouts upload and render correctly together.

Concurrent GPU-visible bank aliases, completed shared uploads, lifetime release/
recycling, viewport/depth clipping, alpha blending and final framebuffer pixels
remain open. Actual ending/Gallery playback and raw/legacy consumers remain open.
The raw root file has no observed visible pose in its tested timeline and receives
no fabricated binding or global-unused designation.

Both graphics audits, requirements ledger and progress documents record the
results. All18 plaque/hint entries and Armor/Weapon variants remain incomplete.
Low resolution Online screenshots remain exempt. The graphics goal stays active;
revisit older record-based checks at actual completion.

Evidence: `work/analysis/fls_concurrent_v333/all_combinations_proof.json`,
`summary.json`, maximum-slot `proof.json`, progress and run log.
Reproduce with `scripts/research_fls_concurrent_v333.py --all`.
