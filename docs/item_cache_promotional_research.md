# Item startup cache maintenance and promotional providers

Advice consumers and actual crew-owner bounds are now verified separately in
[the next checkpoint](item_advice_owners_research.md). This document preserves
the preceding startup/promotional evidence and its narrower limitations.

The full translation goal is active. V158 remains the latest combined ROM.
This checkpoint advances the item research without playable integration credit.

## Exact target and changes

- Previous item research ARM9: `c55a2530af7816a5f612494c42c16af5911e58791d571d92ad9297b7e87980ee`.
- Current cache-maintained ARM9: `edb1032dd92bfbe0c73f18ffdcae71f3b78108bab4ed7546f8b8d3fada739663`.
- The complete preceding 19520-byte item payload is preserved. Main code is
  unchanged except the arena boundary and serialized autoload settings; both
  other autoload sections are exact. The startup BL target is unchanged.
- A 64-byte wrapper occupies the former copy entry, 023ABE40. It calls the
  relocated original copy stub at 023ABE80, then executes the game's SDK drain,
  instruction-line invalidate and data-line clean/flush sequence for each copied
  32-byte line, followed by a final drain. R0–R3, caller SP and return are intact.
- Pool: 19584 bytes, 02387A20–0238C6A0. Staging: 023A7200–023ABEB0.
  The native main arena reserves the entire pool; ITCM remains 8172 bytes with
  aligned arena low 01FFA000. No text, item pointer or helper body changed.

The CP15 encodings are locked to the original SDK instructions at 02000A34,
02000A38 and 02000A3C. Their cache-line operations match the
[ARM946E-S reference manual](https://documentation-service.arm.com/static/5e8e3ee588295d1e18d3aa82).
Unicorn skips these exact operations and applies their checked effects to an
explicit cache model. This is not physical cache or cold-boot acceptance.

## Native execution and independent model

Actual ARM9/ARM7 loading, BSS clearing and startup call execute. ARM7 source and
its relocated sections remain exact. The full payload copies and the caller
returns with preserved registers/stack. The native SDK selects all 614 staged
cache lines, including the wrapper and moved stub. The late wrapper selects
all 612 pool lines in order: 1837 modeled maintenance operations including the
final drain. Each operand, alignment, bound and operation order is checked.

The model starts backing RAM and instruction cache stale, with copied stores
held in dirty data. Clean/flush stages a complete line; drain commits it;
instruction invalidation clears its stale line. The complete expected payload
becomes visible in the model. The preceding data-only copy completes, but its
backing RAM and instruction lines remain stale under these same conditions.
Removing instruction invalidation, data clean/flush or final drain is rejected.
Actual CPU scheduling, physical caches and full cold boot remain unverified.

Both boot and canvas test instruction limits now include the complete copy plus
six loop instructions per 32-byte cache line and bounded overhead. The native
240×96 constructor, actual overlay clear, shared primary dispatch and arena
initialization still pass on the new target.

## Actual item providers

All 198 known item metadata initializers now execute native 020CDAC4,
0204A55C, 020CB190 and 020CDAFC. Complete object metadata, bounded writes,
callee registers, SP and return are checked against their actual resources.
The containing table and object vtable seeds remain explicit contracts.

Promotional defaults 188–197 first execute the real initialization segment
02102C24–02102C7C, including native memcpy and complete name copies. Their
runtime metadata uses owner 023800C8+3E4 and actual provider 02102BB0. CPU
state is restored explicitly after this paused segment for the separate draw;
this does not prove the full random-item initializer returns.

52 fresh target raster cases cover all ten promotional defaults plus static
indices 5, 22 and 151, both complete draw functions and both pixel formats.
They execute actual name virtual, unsigned properties and original warm-cache
COMMON copying. All paragraph words, first/interior/final glyphs, independent
font pixels, bounds and nonoverlap pass. All ten promotional panels were
visually reviewed. 237 private lookup ABI cases pass. 69 focused tests pass;
changed scripts pass Ruff.

The preceding 2090 raster cases are inherited evidence for exactly preserved
item code/data, not fresh executions on the new ARM9 hash. Their proof identity
and complete prefix preservation are checked separately. New target evidence
does not approve a different ROM, bootstrap or consumer.

## Remaining release work

Map full promotional random/download states, actual crew/ship names and owner
searches, Advice menu consumers, Gallery counter allocation, and complete parent
crops/artwork/composition. Refresh inherited paths, register/build a full profile,
then verify saved ROM, lineage, patch reconstruction and physical cold boot.
Canonical promotion requires explicit full-candidate acceptance. Global
category/role consumers and the rest of the full translation inventory remain.

Evidence:

- `work/analysis/item_interface_cache_plan.json`
- `work/analysis/item_interface_cache_native_proof.json`
- `work/analysis/item_native_initialization_proof.json`
- `work/analysis/item_cache_promotional_native_proof.json`
- `work/qa/item_cache_promotional_native/native_sheet.png`

Canonical baseline, V158 ROM/patch and registry are unchanged. No commit or push
is claimed. Revisit older record-based checks after completing the full goal.
