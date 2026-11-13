# V638: original World Map overlay producers and complete actual composition

## Result

The281 unexplained overlay pixels retained by V551 are now bound to the original
cursor and marker painters, their actual cached source files, selected palette
banks and native destination points. The complete39040-pixel current map crop
matches the independently composed bitmap and both original overlays, without
excluding either region. All39040 corresponding physical VRAM pixels also match.

This is progress on the environmental/native-composition audit. No Japanese text
was found in these retained map paintings, and no art or wording changes are
needed. Raw comic/Porto Estado/standalone consumers remain unresolved; repeating
the earlier generic loader compatibility tests does not establish their parents.

## Actual current run

- Current experimental candidate: `out/all_routes_combined_v636_candidate.nds`.
- SHA256: `c4ff537ddcd4da5eb1743fb28cd0eb160492e9b660af080ddae44e94a9f4d95d`.
- Profile: `all-routes-unified-v636`; full470-batch/114-layer integration retained.
- Run: `work/emulation_v193/worldmap_composition_v638`,36000 frames, fresh cold
 boot with no preloaded battery save, savestate, cheat, location or RAM fixture.
- Ordinary inputs: the exact established
 `work/analysis/town_force_texture_v544/map_inputs.json` schedule.
- Read-only RAM at34800,35200,35600,36000 and native serialization at36000.
 The export is verified not to alter main RAM or load a state.

All four selected complete two-screen captures match V551's historical V546
screens pixel-for-pixel with the same input schedule:393216 regression pixels.
That comparison is separate from the new original producer/source proof.

V638 is an evidence checkpoint, not a new ROM. The ROM, patch, registry, canonical
and all release pointers remain unchanged. The canonical remains the user's
accepted `out/raphael_natural_v2_accepted_base.nds`; no promotion is inferred.

## Original source and native placement

| Component | Actual source | Source crop | Bank | Native destination |
|---|---|---|---:|---|
| Cursor | `/_pxl/__frame.pxl` |80,32,24,24|56|128,96|
| Marker | `/_pxl/__marker.pxl` |176,96,16,16|29|124,40|
| Dynamic map |Actual header02279B38|0,0,244,160|0|6,16|

The original initialized owners are02313F60(frame) and02313F74(marker). Actual
owner+12 filename fields, captured view source origins/extents/bank words and
complete resident file bytes match the current ROM. Every index in the selected
source crops and their complete selected palette banks remain exact to clean.
Other translated regions in those shared atlases remain intact.

The cursor's sprite is0218BD0C, with its registered callback0200CAF8. The marker's
sprite is0218C07C, with callback02099304. The direct map sprite is02190E80, with
callback0200CAF8. Their actual renderer context is023117C4. Each complete original
callback executes independently on a copy of the new captured RAM, using actual
cached resources and original getter020D4170. No file, getter, source pixel,
destination point or draw helper is replaced. All three return with full stack
and saved-register ABI intact; every executed instruction word matches clean.

The actual original01FF92D8 operands record the source headers, banks, source
positions/sizes and destination points above. Thus placement is independently
obtained by original execution, rather than selected to fit the screenshot.
Initial pattern matching supplies leads only; the final proof does not depend
on guessed source origins or a supplied destination rectangle.

## Complete display comparison

The original dynamic244x160 bitmap remains source page7 with the observed mask:
9674 nonzero indices match the original blue seaarea atlas; the remaining indices
are0. The map painter's actual origin is6,16. Applying the two original overlay
crops at their executed relative positions predicts every39040 lower-screen
pixel, including all176 cursor differences and105 marker differences.

The corresponding full crop in physical VRAM offset60000 also matches every
pixel at native BGR555 precision. Original software screen selector0 is not
assumed to mean the upper screen: the actual visible lower crop and physical
VRAM are positively compared. No overlay masks, fitted positions, tolerances or
retiming are used in the final composition comparison.

A diagnostic attempt walked the entire registered sprite chain. The first five
callbacks returned, but a later background callback reached an unmapped address
in isolated execution. `registered_sprite_probe.json` preserves that failure;
it is not credited as a full-chain pass. The three independently tested callbacks
above are the completed proof. The first optional source-matcher draft requested
NumPy, which is unavailable in this runtime; the final standard-library/Pillow
matcher and complete verifier require no new dependency.

## Artifacts and storage

- `scripts/probe_worldmap_overlays_v638.py`: complete-pattern source leads.
- `scripts/verify_worldmap_composition_v638.py`: actual original callbacks,
 source/crop/palette/placement, complete map/VRAM and four full-screen regressions.
- `scripts/record_worldmap_composition_v638.py`: archive and additive audit entry.
- `work/analysis/worldmap_composition_v638/native_composition_proof.json`.
- `E:/Rota Nova translations/Screenshots/Test fixtures/V638 World Map composition`:
 four unmodified current screens, reports, tools, source-bound proofs and diagnostics.
- One ordinary World Map screenshot is retained as a guide candidate, without
 publication approval or a completed route claim.

The complete V637 and V638 emulator run directories now physically reside under
`E:/Rota Nova translations/Generated/work/emulation_v193/`. Their former workspace
paths are junctions, preserving every earlier recorded evidence path. Both moves
verified every file hash and overwrote no existing archive.

The final World Map screenshot was visually inspected. Its retained blue map,
cursor/marker, complete World Map/Fleets-Villages headings and lower controls are
readable in the observed state. No new translation is authored in this checkpoint.

## Remaining scope

The original mask-creation lifecycle, other actual map pages, sepia seamap/legacy
CMMN storage use and other states remain open. This proof resolves V551's281
overlay-producer gap for the observed state; it does not establish every map state
or a complete playthrough. Raw comics, older title consumers, village cards,
miniature/Confirm ordinary contexts, other movie/material variants and final user
review remain open.

All18 original plaque/hint entries remain `fully_completed:false`; all22 historical
requirements/scopes remain exact. The preceding V637 turn made progress through
84 actual condition views. The full graphics goal remains active and incomplete.
Older record-based checks remain due at eventual full-goal completion.
