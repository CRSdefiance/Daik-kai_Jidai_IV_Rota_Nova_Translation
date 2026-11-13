# V549 native village-caption cards

The previous turn completed the connected native item-cache transfer proof.
This turn closes the village cards' supplied-input native display gap. V546 is
unchanged; no new production candidate, patch or release layer is needed.

## Original native display, isolated inputs

Eight research-only copies of V546 change only the image operand byte in the
existing original SC0 block44 offset30 event-still instruction20460180. The
opcode/control bytes remain2046 and80; the operand selects168-171 or206-209.
All other route bytes, blocks, file/component bytes, English prose, artwork and
instruction offsets remain exact to the current production parent. Each research
ROM is explicitly named RESEARCH_ONLY and has a fixture provenance manifest.
These copies are not registered playable releases and are not distributed as such.

Each capture cold-boots the real DeSmuME core with normal opening button inputs,
without a preloaded save, savestate, RAM injection or cheat. The game loads and
draws the selected event-still through its original event widget. This makes the
image appear in Rafael's opening for diagnosis; it does not recreate a legitimate
village-development event or demonstrate normal route reachability.

## Verified whole screens and English

| Image | Complete current caption |
|---|---|
|168|Arab Village 1|
|169|New World Village|
|170|Chinese Village|
|171|North Sea Village|
|206|Arab Village (Developed)|
|207|New World Village (Developed)|
|208|Chinese Island (Developed)|
|209|North Sea Village (Developed)|

All49152 pixels of each256x192 native upper screen match the current asset's
palette-derived native5 colours at3600,4000 and4200 frames. White backgrounds,
all text, blank cells and the preserved fragment are included; none are masked
out of the comparison. Each final frame has both a normal capture and final
capture entry; duplicate timestamps do not count as separate verified states.

Independent original-font reconstruction verifies all171 character cells and
1972 ink pixels in the stored planes. Sixteen first/final-character deletion
negative cases are rejected. Original source headers, palettes, flags and image
extents remain exact. Numeral1 and image208's Island distinction remain present.
The source/localization review in V330 is retained; no new wording was required.

Image207's complete279-pixel top-edge fragment and all top20 source rows remain
source-exact and now display pixel-exact in this original consumer. Native display
does not resolve the fragment's identity or permit inventing an additional word.
This is supplied-input evidence; ordinary event context and other transition/
alpha states remain open.

## Saved evidence and audit

Eight complete screenshots and a visually inspected native-upper-screen sheet
are saved under:
`E:/Rota Nova translations/Screenshots/Test fixtures/village_card_gpu_v549`.
They are labeled synthetic test scenes and are not approved guide screenshots.
Hash-verified copy receipts are in the proof. All emulator handles exited0.

- Preparation:`scripts/prepare_village_card_gpu_v549.py`.
- Verification:`scripts/verify_village_card_gpu_v549.py`; Ruff passes.
- Proof:`work/analysis/village_card_gpu_v549/native_GPU_proof.json`.
- Captures:`E:/Rota Nova translations/Generated/work/emulation_v193/village_card_gpu_v549_*`.

All22 original requirement records remain exact; all18 plaque/hint entries and
the global plaque-texture review remain incomplete. The full graphics goal stays
active. Raw comic/legacy consumers and broader ordinary gameplay contexts still
need evidence. V546 SHA256 remains
499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3.
