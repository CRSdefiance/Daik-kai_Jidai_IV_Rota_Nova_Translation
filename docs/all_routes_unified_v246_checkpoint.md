# Combined V246: Assign Sailors and Sailor Info layout corrections

This experimental candidate addresses the two screens reported by the user on
2026-10-09. The broader graphics goal remains active; this checkpoint does not
declare complete localization or promote the canonical baseline.

## Assign Sailors

The Marines/Guns and Lateen/Square labels were positioned above their actual paper
plaques. Their lettering areas now restore the complete former text, including
lower rows, and use measured baselines inside the original plaques. Marines/Guns
have native glyph origins at y110; Lateen/Square at y132. The three top captions
retain their established layout. Complete native-font caption regions match the
actual cold-boot frame. Ship names, crew counts, supply values and sailing data
are not changed by this art repair.

The restored small text regions use the existing reviewed background data and
same-row paper restoration for the expanded lower rows. Palette, dimensions and
encoded file extent remain unchanged. Original plaque borders are retained.

## Sailor Info

All six stat names remain complete English: Stamina, Agility, Charm, Wits, Spirit
and Luck. Wider gold paper plaques match the existing Health/Mood/Level/HP style.
They end at x170. Bars begin at x174 and occupy at most50 pixels, ending at x224.
The numeric front origin remains x227. Labels, bars and numeric values therefore
have separate horizontal areas. The native stat values are preserved; only their
displayed bar width is scaled to half the former range and bounded to0–50 pixels.
Negative or over100 input is visually clamped, while underlying values/getters and
numeric formatting remain unchanged. The numeric baseline moves down two pixels
to align with the new plaque lettering.

The older white rectangle is the equipment tooltip, not a missing image. Its fill
now uses tan paper RGB(205,190,141) only for the Sailor Info equipment tooltip
manager. The original constructor, item eligibility and selected item naming
remain intact. A scoped manager marker resets on the next generic tooltip bitmap
clear, preventing the style from leaking to other tooltip contexts. The native
foreground, glyphs and positioning remain intact. All169 font ink pixels and the
full blank cells of **Equipped Items** match within`[138,210,222,221]`.

## Verification

- The complete V245 ROM reproduces byte for byte after the builder addition.
- All467 inherited batches, previous record IDs, required layers and terminal
  stages remain. Two art batches are explicitly superseded; the new runtime
  layout stage is appended after the existing complete runtime stack.
- Source locks require the canonical ARM9 and exact complete V245 ARM9. Only
  scoped instructions, bar geometry records, owned helper data and normal
  startup/cache metadata change. All52,576 inherited pool bytes are preserved.
- Native tests cover twelve bar-boundary inputs, all four original stacked
  tooltip arguments, saved-register/stack ABI, same-manager versus other-manager
  styling and reset behavior. Constructor/rectangle rendering interceptions are
  explicit CPU contracts; live framebuffer evidence supplies the display check.
- Native boot, arena, late copy/cache model and ARM7-source checks pass.
- Fresh ordinary Lil-route cold boots reach both requested screens, without
  savestates, RAM injection or fixture ROMs. All17 complete plaque/caption regions
  match their saved PXL pixels. Six initialized bar rows stay within the new
  width bound. The actual tooltip contains1,239 tan background pixels and complete
  native-font text. Both full screens were visually reviewed.
- Twenty-nine focused graphics preservation tests pass; all changed Python files
  pass Ruff. Both emulator/build processes are terminal.
- The xdelta patch reconstructs the candidate exactly from the pinned clean ROM.

## Candidate handoff

| Artifact | Identity |
|---|---|
| Canonical build base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA-256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Candidate | `out/all_routes_combined_v246_candidate.nds` |
| Candidate SHA-256 | `bb6b9e747bee91471e876b43d8acc0abb5be9ee72cb9dbd7b51f1a8a7cfe2cd7` |
| Patch | `out/all_routes_combined_v246_candidate.xdelta` |
| Patch SHA-256 | `d6e33148a5e59708763a38c15f0117d5d7348ba5c1906beb48863b882121d05b` |
| Manifest | `out/all_routes_combined_v246_candidate.manifest.json` |
| Profile | `all-routes-unified-v246`, experimental,467 complete batches |

Only `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl` and `/_pxl/personinfo.pxl` change
relative to V245. All route scripts, other graphics, ARM7 and original overlay
remain unchanged. User cold-boot acceptance is pending. Check Assign Sailors,
all six Sailor Info stat rows and equipment tooltips with the user's own saved
game; verify other tooltip contexts return to their original style. The automated
screens use a fresh new game, so numeric state can differ from the user's images.

## Evidence

- `scripts/prepare_two_screen_art_v246.py` and the two versioned art batches.
- `dk4tool/patch/two_screen_layout.py` and`translations/two_screen_layout_release_v1.json`.
- `scripts/verify_two_screen_runtime_v246.py`, `verify_two_screen_release_v246.py`
  and`verify_two_screen_live_v246.py`.
- `work/analysis/two_screen_layout_v246/{runtime_plan,native_proof,saved_proof,live_proof}.json`.
- `work/emulation_v193/two_screen_v246/crew/frame_010000_final.png`.
- `work/emulation_v193/two_screen_v246/person/frame_010500_final.png`.

Four exact Online screenshot transcripts, remaining native/embedded/environmental
coverage, name consistency and final whole-scope gameplay work remain open. Keep
the full goal active and revisit older record-based checks at eventual completion.
