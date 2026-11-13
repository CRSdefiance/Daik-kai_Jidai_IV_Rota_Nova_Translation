# V561 complete shared action-control material and font audit

The previous goal turn established actual Common-wheel OBJ/VRAM/OAM provenance.
This turn reviews the distinct shared frame-control family. Production V558,
its patch, release registry and accepted baseline are unchanged.

## All22 stored controls checked

Every current record in frame_action_buttons_graphics_v7.json is independently
checked against its declared font contract. Fifteen use complete native ASCII
glyphs, including Arrival's reviewed variable ink spacing; seven use the declared
compact seven-pixel faces. All1447 foreground pixels, first/final letters, spaces
and bounds match. The two trimmed native-font top rows are independently confirmed
blank. The entire65536-pixel frame half in CMMNIMG block5 matches the loose atlas.
Header, dimensions and all83 original palette banks remain exact to clean.

The seven miniature controls Done, Rank, Cancel, Pick Cargo, Pick Ship, M and D
contain only background index0 and their declared foreground index9. Every
background pixel is therefore exact solid-zero material, not a wooden texture
that needs restoration. Type, Price % and Arrival retain separate source ornaments;
coloured ornament pixels are not automatically classified as Japanese remnants.

Natural-English source meanings remain: Equip/Advice/Yes/No/Remove/Use;
Set Crew/Balance/Minimum/Done; Flagship as the flagship-priority preset;
Fill Evenly as equal resupply; Type/Price %/Arrival; Done/Rank/Cancel;
Pick Cargo/Pick Ship; and compact month/day initials. Actual parent context is
still needed for broader terminology/crop conclusions; the audit does not infer
every command's behavior merely from its isolated label.

## Textured controls and reconstruction experiment

The first12 controls are diagonal bronze/shaded button faces. Their original
backgrounds are not identical: simple cross-cell consensus has173 disagreement
positions in the smaller control sample and148 in the wider sample. Copying one
whole generic button would therefore change original material.

The historical repair uses nearest-row colors only where original white faces
and dark shadows were erased. Under a conservative mask of original white
lettering plus black points within two pixels, all3239 current visible source
material points outside English ink already match the original. The two-pixel
shadow extent is an explicit review assumption, not a mapped original shadow
producer. This review does not establish a new visible-material loss.

A research alternative preserves source material and reconstructs concealed
points from another same-size original button selected by local visible-neighbour
colour agreement. Three points require same-plate diagonal samples because no
usable contextual donor remains. It changes323 pixels, all in reconstructed
regions, with every English mask and all ten other controls retained. Source
header/palettes/extents and unowned pixels stay exact.

Visual comparison does not establish enough improvement to integrate this
alternative. Concealed texture is unknown and must not be called exact recovery.
The research PXL is retained, clearly labeled RESEARCH_ONLY; no new ROM build is
made for an unsupported claim of improvement. The source-based texture workflow
still applies to any later revised control artwork.

## Native consumer scope

Two actual ordinary V558 snapshots—Common wheel frame12700 and Swap Ships
frame6700—are scanned for12-word frame views using owner02313F60 and each of the
seven exact miniature source origins. No matching views are found under this
specific layout/origin filter. The paths, hashes and results are recorded.
This is not proof of global non-use, absence of broader atlas views, or lack of
other view layouts. Actual consumer, palette, clipping and display checks for
these miniature controls remain open. Stored-font passes do not establish them.

## Evidence

- `scripts/review_action_materials_v561.py`; source-based research generator.
- `scripts/verify_action_materials_v561.py`; complete current-family verifier.
- Ruff passes for both scripts.
- `work/analysis/action_materials_v561/current_material_and_font_proof.json`.
- Full original/current review sheets for all22 controls and original atlas view.
- Local alternative review sheet, source counts and research-only PXL/proof.

The evidence is on E through the existing work/analysis junction. All22 historical
requirements retain exact scope and all18 original plaque/hint entries remain
incomplete. Current candidate remains experimental V558, SHA256
bf62f246f485c7adf9a763c7765bc63476128f73f6cce983717bf297877cff6d.
The full graphics goal remains active; native action-control parents/crops and
other recorded graphics work remain to complete.
