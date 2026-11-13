# Combined V252: expanded plaque audit and short equipment hints

The preceding turn fixed old Japanese caption fringe in V251. This turn extends
the user's ongoing plaque audit and fixes an observed alternate-state styling gap.
All17 plaques plus the equipment-hint entry remain explicitly incomplete.

## Observed defect and scoped correction

Normal LEFT navigation through Lil's equipment slots exposes **Armor** and
**Weapon**. V251 draws their34×16 and40×16 backgrounds as flat tan rectangles,
while the88×16 Equipped Items heading uses textured, beveled port-paper artwork.
The new source-locked final stage supplies the same donor paper for both measured
short sizes. Fonts, text, positions, item selection and glyph colors are unchanged.

Native coverage verifies all pixels exactly once for34/40/88×16 hints. Six
fallback cases preserve other sizes/heights, another manager and inactive/reset
white defaults. Original saved-register/stack ABI and ARM9/ARM7 startup, copied
pool, cache and arena checks pass. All inherited pool bytes remain exact.
Other occupied-item name dimensions remain to review; no all-size guarantee is
made from the three observed geometries.

## Fresh ordinary gameplay coverage

Three fresh cold boots of the registered candidate use ordinary controller input,
without loaded savestates or RAM injection. Two extended paths visit four male
sailors and Lil; another changes the crew editor through Lo/Hi/decrease states.
The earlier failed crew extension included future B/UP inputs beyond its original
10000-frame stop. That attempt is retained separately and replaced by a trimmed,
explicit schedule; its exited-town images are not crew-state proof.

- Five sailor screens: captain displayed as Raphael Castor, Janus, Claudio, Julio,
  and Lil. All50 full stat/status plaque regions match the saved art exactly.
- Every complete seven-label/three-digit lower skill line matches the native font:
  50 lines, including every blank and numeric digit. Values remain within0..500.
- Three equipment hints: the complete native font, every background texture pixel
  and original beveled donor edges match for Equipped Items, Armor and Weapon.
- Four crew-editor states: all28 complete plaque regions match. Full right-aligned
  Need/Now/Max digits are checked at their observed origins, including zero and
  two-digit values. These are displayed values, not inventory arithmetic proof.
- All415 unaffected sampled framebuffers match V251 byte-for-byte, including
  title/selection/opening/town/navigation and the ordinary sailor/crew displays.
- Thirty-four focused artwork/state-reader tests pass; changed Python files pass
  Ruff. All capture processes are terminal.

The observed captain label still says **Raphael Castor**, differing from the locked
Rafael choice. This confirms remaining runtime-name migration rather than silently
claiming naming consistency. It is documented separately from the plaque artwork.

## Continued audit status

All18 base entries remain **incomplete, pending continued audit and user review**.
Armor/Weapon are recorded as additional incomplete variants of the equipment-hint
entry. These checks add evidence and repair known defects; they do not close the
user's audit. Occupied-item names, additional health/mood conditions, wider routes,
alternate parents/banks and physical-device acceptance remain open. The full
graphics goal, unreadable Online sources and remaining embedded/native/source
requirements remain active. Revisit older record-based checks at eventual full
completion.

## Integration and complete handoff

| Item | Identity |
|---|---|
| Canonical build base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA-256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Profile | `all-routes-unified-v252`, experimental |
| Complete stack |467 prior batches,114 baked accepted layers, every terminal stage retained |
| Candidate | `out\all_routes_combined_v252_candidate.nds` |
| Candidate SHA-256 | `e4e8bd220b7f625c7f03ee9c1de9daaa96f6a3e835cb602821910b5764a793c0` |
| Patch | `out\all_routes_combined_v252_candidate.xdelta` |
| Patch SHA-256 | `e0c6da6e4d019e37fdc7c5335b0edd0535930ebce4bca4af6e2fdc992f545995` |
| Manifest | `out/all_routes_combined_v252_candidate.manifest.json` |
| Changed component vs V251 | `/__arm9__.bin` only |

After the shared helper/default-compatible builder changes, V251 reproduces
exactly. Every ROM file, all route scripts, ARM7, overlay, artwork and the previous
43-pixel fringe repair remain byte-identical. The clean-ROM xdelta reconstruction
is byte-identical to V252. User cold-boot acceptance remains pending; the canonical
baseline is not promoted. Please check title/New Game/story/town, the ongoing
crew/sailor screens and all three equipment headings on the user's setup.
The raw comic's native display is still unproved and is not inferred from these
regression boots.

## Evidence

- `work/analysis/plaque_coverage_v252/saved_live_proof.json` and `native_proof.json`.
- `work/analysis/plaque_coverage_v252/expanded_live_audit.png`.
- `scripts/verify_short_equipment_release_v252.py` and `verify_short_equipment_runtime_v252.py`.
- `dk4tool/patch/short_equipment_paper.py` and its versioned release configuration.
- `work/emulation_v193/short_equipment_v252/{town,lil_items,crew_trimmed}/`.
