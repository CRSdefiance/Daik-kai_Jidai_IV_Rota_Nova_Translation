# Combined V247: native plaque styling and source-reviewed labels

The requested Assign Sailors and Sailor Info redesign is complete. Both screens
use the established port-information paper texture, native palette, original game
font and intact beveled corners. All17 plaques are centered within their borders.
The dynamic Equipped Items heading now uses the same textured paper.

## Translation and formatting

Every plaque, all10 lower abilities and14 other headings/conditions/controls are
reviewed in [the source and localization rationale](crew_sailor_ui_translation_v247.md).
The reviewed crew labels include Fleet Crew, Unassigned, Endurance, Quarters,
Cannon, Fore/Aft and Square. Upper stats remain Stamina, Agility, Charm, Wits,
Spirit and Luck. Lower source-specific skills use Vigor, Speech, Swords and Guile.

Live checks caught a Cannon-border/count overlap and corrected its right edge.
Research labels Vitality/Persuade/Intrigue and Dueling displaced or lost numbers;
final natural labels retain every letter and digit. The shared lower-skill format
also changes from `%6s%4d` to `%7s%3d`, preserving total width while reserving
all three digits even for existing seven-letter names. Fifty native formatter
cases (every label at0/9/97/107/500) pass exact output and memory guards.
The final full-row pixel checks reveal103 Command,91 Sailing,104 Finance,
101 Observe and97 Guile; older screenshots clipped some of those final digits.
The native numeric getter/code remains byte-identical. Min/Max research
controls clipped their third letter; final Lo/Hi preserve the native two-letter
control space and still mean minimum/maximum. Failed research displays are not
release evidence. Only the final candidate SHA below is the handoff.

## Verification

- Exact complete V246 reproduction after the builder change.
- All467 inherited batches, every required accepted layer, prior changed record,
  route script, other graphics, ARM7 and original overlay retained.
- Both PXL headers, palettes, dimensions and packed extents unchanged.
- Native paper helper:487 bounded runs, all1408 pixels covered exactly once,
  preserved saved registers/stack, generic-manager/reset fallback unchanged.
- Original native skill getter returns all10 reviewed labels; numeric getters
  and game-state values are unchanged.
- ARM9/ARM7 startup, main-pool copy, cache and arena checks pass.
- Two final fresh New Game cold boots via normal Lil navigation, without
  savestates or RAM injection. All17 entire plaques match saved pixels, all169
  equipment-heading ink pixels and1239 paper pixels match. All10 complete
  skill rows match their entire seven-label/three-digit format, including blank cells; six stat bar views remain bounded.
- Twenty-nine focused graphics tests pass; all changed Python files pass Ruff.
- Clean-ROM xdelta reconstruction is byte-identical to the candidate.

These are targeted automated emulator checks, not a complete playthrough or
physical-device acceptance. Final captures are under
`work/emulation_v193/plaque_style_v247_final_format/`.

## Full handoff identity

| Item | Identity |
|---|---|
| Canonical build base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA-256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Profile | `all-routes-unified-v247`, experimental |
| Batches |467 complete inherited batches; all required accepted layers included |
| Candidate | `out\all_routes_combined_v247_candidate.nds` |
| Candidate SHA-256 | `01d75da29b6d22fd0bd7bd7281546babfec6c199250a141774f8dc4f30cda9cd` |
| Patch | `out\all_routes_combined_v247_candidate.xdelta` |
| Patch SHA-256 | `302794f93a1d5e1c3ddc476f9ddc419755017106cc1814043569404be532c753` |
| Manifest | `out/all_routes_combined_v247_candidate.manifest.json` |

Only `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl` and `/_pxl/personinfo.pxl`
change relative to V246. The versioned art batches supersede V246 while preserving
its historic hashes. The new final runtime stage is source-locked to full V246.

User cold-boot acceptance remains pending. Please check Assign Sailors, Sailor
Info, all displayed labels/values and equipment hints with the user's own game,
and confirm other tooltip contexts retain their normal style. The canonical
baseline is not promoted. The wider graphics goal remains active and incomplete;
older record-based checks remain a follow-up at its eventual completion.

## Evidence

- `work/analysis/plaque_style_v247/saved_live_proof.json`
- `work/analysis/plaque_style_v247/native_proof.json`
- `work/analysis/plaque_style_v247/translation_review.json`
- `work/analysis/plaque_style_v247/live_preview.png`
- `translations/assign_sailors_graphics_v5.json`
- `translations/person_info_graphics_v3.json`
- `translations/plaque_style_release_v1.json`

## User-required ongoing plaque audit

On2026-10-09 the user explicitly requested that all17 plaques and the Equipped
Items hint remain in the graphics audit and are not marked fully completed.
Their state is **pending continued audit and user review**. Existing source,
native and two cold-boot proofs remain scoped evidence. They do not close the
plaque audit or establish all alternate states, contexts, characters or devices.
