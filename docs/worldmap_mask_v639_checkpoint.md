# V639: original World Map mask construction and cache lifecycle

## Result

The mask-creation gap retained by V551/V638 is resolved for the observed current
World Map state. Original native code rebuilds every19520 packed byte/39040 index
from the real source painting and captured area-visibility records. An independent
coordinate/rectangle model produces exactly the same bitmap, which already has
complete actual-screen and VRAM evidence from V638.

V638's preceding goal turn made progress by identifying the cursor/marker
producers. V639 adds original bitmap construction, area-state provenance, cache
invalidation/copy checks and two explicitly isolated state controls. No production
art, wording, ROM, patch, registry, battery save or release pointer changes.
V639 is an evidence checkpoint; no V639 release ROM is created.

## Actual captured state and source

- Candidate: `out/all_routes_combined_v636_candidate.nds`.
- SHA256: `c4ff537ddcd4da5eb1743fb28cd0eb160492e9b660af080ddae44e94a9f4d95d`.
- Profile: `all-routes-unified-v636`; complete470-batch/114-layer stack retained.
- Reused actual run: `work/emulation_v193/worldmap_composition_v638`, frame36000.
  This was an ordinary cold boot without a preloaded save, savestate or RAM cheat.
  No new emulator run is claimed for V639's isolated native execution.
- Reused actual RAM SHA256:
  `9a18663f09e318ff1b4b09185fe1426d74330139499e24f9a9c0c1fdfd3b732f`.
- Original blue atlas: `/_pxl/seaarea.pxl`, unchanged from clean. Page7 supplies
  the244x160 whole-world painting with its original palette and dimensions.

Original getter020989E8 resolves the captured map view0218A3B8 to its actual
controller0218A3A8. Original CB118 resolves the area-state store, whose visibility
word is022E1174. All24 bits are clear in this captured state. This is an exact
source-state observation, not a claim about every city's discovery, legitimate
voyages or the full save history.

Original CACAC resolves all24 actual52-byte area records; CADA0 returns each
record's correct index. CAD68/CAC00 select its corresponding visibility bit.
Each record supplies up to two world-coordinate rectangles. There are28 valid
rectangles across the24 captured records.

The original source-map bounds are[0,0,40000,20000], with native target bounds
[0,0,244,160]. The independent model transforms positive endpoints using exact
integer rational truncation: x×244/40000 and y×160/20000. Every resulting rectangle
matches the actual native geometry/eraser operands, in their original order.

## Original rebuild and complete independent comparison

Original0208F334 mode0 uses original020474DC and the actual resident cache to copy
the complete source page into scratch022403C0. It selects the original area bits
and records, transforms their rectangles and erases hidden regions through
original020D5C98. No filesystem, getter, painter, source plane or geometry result
is bridged/replaced. Every executed instruction word matches the clean ROM.

The actual28 rectangle union covers28865 pixels. Outside that union,501 original
source pixels were already0. Thus the actual background has29366 zero pixels,
with9674 nonzero original-source indices retained. The proof distinguishes
source zeros from pixels actively cleared by the game.

All19520 native packed output bytes and all39040 independently modeled indices
match the captured live bitmap. This connects original construction to the
complete map/overlay and physical VRAM comparisons in V638; a retained captured
bitmap is no longer the only evidence for the mask's production.

## Explicit isolated controls and cache checks

These controls operate only in Unicorn copies of the exported RAM. They are
never applied to the emulator, ROM or battery save and are not earned-map or
guide acquisition evidence.

| Case | Source visibility bits enabled | Erasure rectangles | Erased union | Remaining nonzero source indices |
|---|---|---:|---:|---:|
|Actual captured state|None|28|28865|9674|
|Isolated area14 control|14|26|27633|10886|
|Isolated all-area control|0–23|0|0|37228|

Original setter020CAD38 changes each control's bit. Every setter's whole before/
after main-RAM comparison permits changes only in the area visibility word and
the original page-cache invalidation word. All other main RAM remains exact.
The all-area case reproduces every source-page byte, with no erasure call.

The mask-ready word at controller+6C80 is explicitly reset in the isolated copy
to force a rebuild; its original clearing/set instructions and branches remain
unchanged. This is a supplied cache condition, not a newly observed gameplay
transition. Scratch starts with A5 poison, proving a completed rebuild replaced
the old contents. Leaving the ready flag set instead retains the poison; that
negative control confirms that an existing cache hit cannot supply the passing
rebuild result.

Original02047470 invalidates the actual page-cache store022857AC. Mode1 then
copies the rebuilt mask into the poisoned real bitmap destination02279B6C.
Every destination byte matches the independent model; both source and destination
adjacent16-byte guards remain exact. A repeated mode1 call preserves the
destination and the expected native page-cache flags. All native calls return
with their complete stack and saved-register ABI intact.

## Rejected diagnostic and artifact review

The first diagnostic reversed the scratch and page-store addresses. Its scratch
comparison failed, and its apparent destination equality had not proved a copy
because the real cache had remained valid. This is preserved as
`initial_mask_probe.json` and excluded from passing evidence. The corrected
source literals, actual invalidator, poisoned destinations and full-byte checks
above establish the final result.

The derived source/masked/all-area comparison sheet was visually inspected.
Its original/masked shapes agree with the source state and actual V638 screen;
it is clearly labeled a derived native-bitmap review. The all-area panel is an
isolated native control, not a new screenshot or normal player unlock.

## Reproduction, archive and remaining scope

- `scripts/verify_worldmap_mask_v639.py`.
- `work/analysis/worldmap_mask_v639/native_mask_proof.json`.
- `E:/Rota Nova translations/Screenshots/Test fixtures/V639 World Map mask`:
  native proof, tools, original/corrected diagnostics, derived review sheet and a
  clearly labeled reused unmodified V638 screenshot. No additional guide copy.

All18 original plaque/hint entries remain `fully_completed:false`; all22
historical requirements/scopes remain exact. The new evidence is additive and
resolves the observed-state mask gap without rewriting earlier scope records.
Other actual map pages, sepia seamap/legacy storage consumers, raw comics, older
title consumers, village cards, miniature/Confirm contexts, other movie/material
variants and final user acceptance remain open. The canonical and every release
pointer remain unchanged. Full graphics goal active; older record-based checks
remain due at actual completion.
