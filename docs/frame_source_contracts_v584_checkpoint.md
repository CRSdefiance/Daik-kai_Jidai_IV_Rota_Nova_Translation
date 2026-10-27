# V584: original frame-atlas source contracts and caller census

Production remains experimental V581. This batch makes no ROM, patch, artwork,
profile or canonical changes. It replaces coarse source-coordinate searches with
source-bound argument analysis and original native helper execution.

## Correct software drawing contracts

The corner-copy routine is in the original low-memory main-code section; the
tiled helper is in declared ARM9 overlay0 at01FFA000. The overlay's entire
6,208-byte data is exact clean source. Do not interpret their coordinates as
interchangeable source/destination rectangles. V587 corrects the earlier prose
that incorrectly placed both routines in that overlay:

| Routine | Registers | Stack arguments |
| --- | --- | --- |
|01FFAE70 tiled copy|r0 screen; r1 PXL header; r2 palette bank; r3 source XYWH descriptor|0: destination LTRB pointer|
|01FF92D8 corner copy|r0 screen; r1 PXL header; r2 palette bank; r3 source XY pointer|0: source size pointer;4: destination XY pointer|

Eighteen tiled and four corner-copy controlled executions match an independent
model across the complete196,608-byte two-screen software framebuffer, its guards,
resource guards and saved-register/stack ABI. The source is the exact current
`/_pxl/__frame.pxl`; resource binding is an explicit input in these probes.
The cases include all five miniature cells, original palette banks0/9, repeated
decorative tiles, both screens, viewport-origin offsets and clipping.

The original tiled routine restarts its tile phase at the clipped destination
edge. Its zero-width/height descriptor can repeat a single source pixel across
the destination; it must not automatically be classified as unused. Both opaque
and transparent zero-descriptor cases pass. No behavior of this original routine
is changed, and no general sprite-clipping guarantee is inferred.

## Literal owner paths

An aligned PC-load census covers every mapped main section and the declared
overlay. All48 literal references to owner02313F60 are reconciled:

-38 view-setting/constructing sites. Twenty-nine have complete source XYWH
  constants within their basic block. Three more have source rows136/120/208
  known locally. Six remaining row definitions resolve to224 or216 in earlier
  stack setup. These are outside the miniature-caption band32-55.
- Eight shared resource-getter sites: four generic frame/strip/tile helpers and
  four fixed drawing families. Their remaining fixed sources use rows56/104/224.
- Two sites belong to original startup initialization. Executing that initializer
  confirms the owner filename is `_pxl/__frame.pxl` at owner+12.

For the six earlier stack definitions, checked original control flow establishes
that the source-row store dominates the constructor. The source row slot has no
other direct store. Normal callee stack ABI and absence of an aliased write to
that slot remain explicit assumptions; this is not a live parent-context proof.
Five complete function regions are clean-identical. The sixth differs only at
three nonexecuted literal words for existing Fleet/Village, Shortage and %s Admiral
translations. All reachable instructions and row definitions remain exact clean.
Those literal differences are individually bound, not broadly exempted.

## Every tile of the fixed styles

The shared wrappers have84 fixed-style call sites. All84 source pointers resolve:
the two direct-border calls take their style array in r1, while the other wrapper
families use r2 or their fixed default. A runtime destination pointer must not be
reported as an unresolved source pointer.

Original styles contain nine-part frames, three-part strips or single tiles.
Checking only the first tile is insufficient. Original wrapper/helper execution
with two declared center flags produces168 cases and852 tile calls. Every
nonempty declared tile is exercised; zero-dimension records are recorded according
to whether the original path calls them. All selected source footprints lie
outside the five miniature cells. Source helper code and complete style arrays
remain exact clean source.

The resource getter is bridged to the exact supplied production header and pixel
calls are argument-traced in these wrapper cases. Their actual pixel contracts
are verified separately above. These are not84 newly visited gameplay screens,
852 framebuffer captures, or proof of ordinary caption availability.

## Consequence and limits

The literal view and fixed-style paths do not explain ordinary use of Done,
Rank, Cancel, Pick Cargo or Pick Ship. The next investigation should target
computed/aliased owners, indirect calls or embedded-copy readers. Repeating the
same literal rectangle search or persistent-view scan cannot establish a parent.
This census does not prove global non-use. Prior V579 complete controlled native
caption rendering remains valid; the actual five parents and Confirm parent stay
open. No new Japanese instruction requiring translation is found in this batch.

One wording lead is retained for contextual review: source literal0208E56C maps
`%s提督` to inherited `%s Admiral`. Verify its actual heading context and word
order before revising it; this geometry batch does not silently rewrite prose.

## Evidence and reproduction

Run in order with the project dependency path:

1. `scripts/trace_frame_crop_arguments_v584.py`.
2. `scripts/resolve_frame_rows_v584.py`.
3. `scripts/trace_frame_styles_v584.py`.
4. `scripts/verify_frame_blitter_contract_v584.py`.
5. `scripts/verify_frame_style_tiles_v584.py`.
6. `scripts/verify_frame_caller_census_v584.py`.

All six pass targeted Ruff. The final `frame_caller_reconciliation.json` in
`work/analysis/frame_callers_v584` binds subordinate proofs, current ROM/atlas,
source code, style records, assumptions and limits. Original/current atlas
projections and disassembly diagnostics are stored alongside it on E through
the analysis junction. They are source projections, not gameplay screenshots.
Final proof copies/projections and hashed provenance are under
E:/Rota Nova translations/Screenshots/Test fixtures/V584 Frame source contracts.
No new DeSmuME run or guide-candidate promotion occurs in this batch.

While developing the probes, checks rejected four incorrect assumptions: the
stack source row always being local, the whole large function matching clean
despite three localized literals, a style having only its first tile, and a
zero-size descriptor always being unused. These failures changed the analysis
model, not the ROM. Missing/unknown values remain explicit instead of fabricated.

V581 ROM/patch remain unchanged. All18 original plaque entries remain incomplete
and all22 historical requirement objects remain deep-identical. The graphics
goal stays active; other materials, legacy/event/movie contexts and after-goal
older record-based checks retain their scope.
