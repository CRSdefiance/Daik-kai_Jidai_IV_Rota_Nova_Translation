# V633: complete Ship Info and centered Refit headings

## Defect and source

Ordinary Info > Ships navigation in experimental V627 exposed a clipped header:
**Ship In** appeared where the stored string is **Ship Info**. The native
168x84 bitmap contains all98 title ink pixels, but its original48-pixel source
rectangle displays only74. The final f/o lose24 pixels. This is a genuine
destination-view defect, not a missing stored translation or a font failure.

The clean ROM's two original title literals are ` 船情報 ` and `装備変更`.
Ship Info faithfully names the information view. Refit is a natural compact
label for the actual Shipyard > Remodel room/equipment view. Neither meaning
is shortened or changed in this correction.

## Exact correction

The original seven-word descriptor at02114D3C changes from
`(-1,104,2,0,36,48,12)` to `(-1,95,2,0,36,66,12)`. The complete11-cell
Ship Info heading now fits and is centered. The shared Refit title becomes
`   Refit   ` to center its five visible letters in that same66-pixel view.
These are UI centering cells, not manually formatted dialogue.

The31-owner Deck pool remains exactly540 bytes. Refit's extra aligned storage
uses exactly four existing terminal padding bytes. All31 start references are
remapped; the every-byte ARM9 pointer census and the sole ARM9 overlay's
every-byte alias census find no additional references into the owned pool.
All other30 strings remain byte-exact. Five invalid-source/owner/reference
controls are rejected. Every other ARM9 byte and every other ROM file/component
remain exact to V627. No font, painter, palette, bitmap allocation, startup code,
staged payload, section size or arena boundary changes.

The registered integrated builder adds `ship_info_title_crop` after the complete
V627 stack. Earlier profiles remain reproducible without this optional stage.

## Actual tests

All successful runs cold boot the actual ROM without savestates. No synthetic
location, inventory, condition, code or framebuffer fixture is used.

1. **Ship Info:** a5600-frame copied-save run replays the original ten inputs.
   The complete98-pixel original-font mask passes. V627's74-pixel clipped mask
   is independently confirmed. Every pixel outside old/new title ink and all
   other captured selection screens match V627 exactly.
2. **Refit:** ordinary Syracuse lower-ship-icon > Remodel navigation reaches
   the real original view. A7200-frame V627 control and exact V633 replay show
   two room selections at6800/7200. Both65-pixel complete title masks pass;
   only old/new title lettering changes. Every other shared capture is exact.
   No completed/paid remodel or acquired equipment is claimed.
3. **Ordinary regression:** all19 captured screens in the24100-frame fresh,
   no-save New Game/story/town/Market schedule match V627 byte-for-byte.
4. **Release:** all470 batch entries remain exact to V627 and all114 accepted
   layers remain registered. All manifest checks pass. Fresh921 PXL/FLS format,
   palette and extent checks and57 embedded block extent checks pass. The
   clean-ROM patch reconstructs every byte of the saved candidate exactly.

Native previews execute the original title-selection/painter fragment in the
captured real bitmap object. Complete masks come independently from the original
font. Missing first/final columns fail the actual-screen comparator. These are
targeted emulator checks, not a complete route playthrough or hardware test.

Earlier navigation diagnostics are preserved separately: one noninteractive run
terminated with EOF at3200, a short menu discovery stopped normally at4800, and
a Lisbon tutorial/Guild discovery stopped normally at29700. They earn no Refit
display credit. The initial assumption that Syracuse lacked a shipyard was
incorrect: the lower ship icon at native bottom-screen230,80 opens it.

## Candidate and reproducibility

- Experimental ROM: `out/all_routes_combined_v633_candidate.nds`.
- SHA256: `eea7c88cd8c6082cf56a8779421018913f2ef9b40ca3cc77fe1d1b13b74ec05f`.
- Profile: `all-routes-unified-v633`; neighboring manifest and `.xdelta` required.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Patch input: `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- Physical output: `E:/Rota Nova translations/Generated/out/`.
- Proofs/config/previews: `work/analysis/ship_title_v633/` and
  `translations/ship_info_title_crop_v1.json`.
- Verifiers: `scripts/verify_ship_title_v633.py` and
  `scripts/audit_graphics_preservation_v574.py`.
- Targeted Ruff and integrated-builder syntax checks pass.

Runs are under `E:/Rota Nova translations/Generated/work/emulation_v193/`:
`ship_title_v633_selection_actual`, `ship_title_v633_shipyard_control`,
`ship_title_v633_refit_actual`, and `ship_title_v633_market`.
The unmodified copied Syracuse save remains SHA256
`958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb`.
Input schedules, frame anchors, reports and read-only RAM exports are retained.

## Scope and next work

All18 original plaque/hint objects stay `fully_completed:false`, and all22
historical requirement objects/scopes remain exact. Existing verified V610 and
canonical pointers stay unchanged; only the latest compiled experimental pointer
advances. No human acceptance, canonical promotion, commit or push is inferred.

Discovery identifies a real live CSelectShipView through ordinary Info > Ships
navigation, but does not prove that Done/Rank/Cancel/Pick Cargo/Pick Ship or the
separate Confirm graphic is displayed there. Those ordinary parents, eight
village cards, legacy/material/environment/movie variants and the broader final
graphics acceptance remain open. The full graphics goal remains active.

Unmodified before/after screenshots and a separately labeled enlarged comparison
are archived under `E:/Rota Nova translations/Screenshots/Audit comparisons/V633 Ship headings`.
Current whole Ship Info/Refit captures are saved as guide candidates with provenance.
