# V552 complete ordinary map overlay composite

The previous turn identified the actual masked page7 blue map and its VRAM output.
This turn resolves the remaining281 overlay pixels in ordinary V546 frame36000.
No ROM, patch, source artwork, translation, registry or save is changed.

## Exact source and actual native bindings

| Graphic | Source rectangle | Palette bank | Native view | Native origin | Opaque pixels |
|---|---|---:|---|---|---:|
|24x24 indicator|`/_pxl/__frame.pxl`80,32 to104,56|56|0218BCAC|128,288|176|
|16x16 marker|`/_pxl/__marker.pxl`176,96 to192,112|29|0218BD3C|124,232|105|

The latter's visible12x12 component has2 transparent pixels of padding on each
edge. Its16x16 source crop is used in full. Searching only default palette colours
would miss both sources: each of these files contains83 stored16-colour banks.
Exact colour filtering plus all recorded foreground pixels yields unique crops
in the appropriate atlas, not an assumed ship image or a guessed nearby literal.

Captured original view fields identify the real owners02313F60 and02313F74,
source origins, extents and exact banks56/29. Complete original resource resolution
020D4170 executes on isolated captured RAM without a file bridge or substituted
resource pointer. It returns the actual resident whole files byte-exact, preserving
its stack/saved-register ABI. Source cells and their palette banks are exact to
clean despite other localized regions in the surrounding atlases.

## Full composition

All176 and105 source foreground pixels match independently. All400 and151
transparent source pixels are included by retaining the underlying map pixels.
The complete244x160 masked base bitmap plus both source rectangles reconstructs
all39040 framebuffer pixels at6,208, without exclusions. The281-point gap recorded
in V551 is resolved for this exact observed ordinary gameplay view.

Earlier-frame tests deliberately tried the same fixed overlay composition at
35400/35600/35800; they differ by875/875/176 pixels respectively. Those frames
are not credited as full-composition passes. Category/animation/visibility state
cannot be assumed constant merely because stored source view fields are equal.
Frame36000 is the verified case; the other state producers remain to trace.

The custom24x24 view's class pointer also traces to original constructor code
02094904. This is a constructor lead, not a new full producer/animation proof.
No graphic identity, speaker or item name is invented from silhouette alone.
These icons have no newly identified Japanese caption requiring translation.

## Artifacts and remaining scope

- `scripts/verify_map_overlays_v552.py`; Ruff and complete verifier pass.
- `work/analysis/map_overlays_v552/overlay_composite_proof.json`.
- `source_candidates.json` and integer-scale native/source crops.
- Ordinary source capture:
  `E:/Rota Nova translations/Generated/work/emulation_v193/worldmap_source_v551`.
- Saved native screenshot:
  `E:/Rota Nova translations/Screenshots/Test fixtures/worldmap_source_v551/ordinary_world_map_v546.png`.

The full observed composite passes. Other marker banks/crops, animation/category
states, the creation of the page7 mask, original sepia seamap and legacy CMMN
contexts remain open. This test does not establish a complete route or hardware
verification. All22 historical requirements remain exact; all18 plaque/hint
entries remain incomplete. The graphics goal stays active. V546 remains SHA256
499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3.
