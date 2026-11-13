# V560 live Common wheel OBJ provenance and material review

The previous goal turn verified the fleet wallpaper and its ordinary Swap Ships
consumer. This turn separates the stored bronze marker strips from the live
Common wheel and positively binds the latter to its actual emulator OBJ state.
No ROM, patch, translation, artwork or release registry changes are made.

## Two distinct artwork paths

The six live Common captions use precompiled sprites in `/GRP/DSOBJ.DK4`, as
documented in `docs/release_build.md`. Stored `/_pxl/__marker.pxl` captions and
their `/GRP/CMMNIMG.DK4` copy remain separate audit assets. Repeating a loose
marker check alone would not prove the live wheel's lettering source.

All six DSOBJ banks independently match the full native font at five-pixel
advance. Original nonwhite material, frame and padding pixels outside the new
English ink remain exact. The754-position text region has753 agreeing visible
background references across the six original sprites. The one fully concealed
point23,11 is index6 inferred from13 original diagonal samples, not recovered
information. No disagreement between visible source references is found.

The entire current16384-byte DSOBJ file is exact to the accepted baseline. An
initial comparison to clean beyond the first6144 bytes differs because other
accepted sprite translations already exist. That result is retained in the
diagnostic source_scope.json; it is not classified as a new regression or a claim
that only these six banks have ever been localized.

## Ordinary current captions

A V558 cold boot replays the established Lil opening and Common-menu navigation
without a preloaded battery save, savestate, cheat or synthetic fixture. Six
selected states at11200/11500/11800/12100/12400/12700 verify Crew Setup, Deck View,
Route Map, Info, Items and Functions. Every ink and blank font-cell pixel matches,
including all first/final letters and spaces. The run completes12700 frames exit0.

## Actual emulated VRAM, OAM and palette binding

The read-only native export now records the actual serialized VMEM palette field
in addition to existing OAM, VRAM, I/O and CPU exports. It is2048 bytes. Serialization
matches the same-frame direct RAM export and does not change main RAM; no state
is loaded. Existing exports remain intact. The decoder exposes field extents so
unknown regions are not selected by guessed memory layout.

All6144 bytes of the six32-tile,64x32 sprite banks occur byte-exact at physical
LCDM offset80000, VRAM bankE. E control82 maps it to main OBJ at offset0. Main
DISPCNT1191B selects1D OBJ mapping with32-byte tile units and standard palettes;
BLDCNT is0. Main OAM entries74..79 are normal, non-affine, unflipped64x32 sprites
with priority0. Tile indices0/32/64/96/128/160 bind exactly to the six file banks.
Palette banks0 and1 are read from the exported standard main OBJ palette at VMEM
offset200; colours are not borrowed from a default PXL preview.

Each actual marker view's64x24 position agrees with its corresponding OAM sprite.
The OBJ image has eight extra transparent padding rows. In hardware OAM priority
order, all8150 visible composite pixels from the six sprites match the final
Functions-state screenshot. This includes overlapping cards and the complete
selected sprite; it is emulator register/framebuffer evidence, not physical DS
device verification. Whole-file OBJ VRAM residency or all animation states are
not inferred from the6144-byte binding.

## Why V245's stored marker repair did not change the live captions

The current marker's first six cells differ from the accepted baseline at1044
caption positions. Every one lies beneath a nonzero pixel of its corresponding
actual OBJ sprite, at matching positions, with normal sprite mode and no blend.
The opaque OBJ composite therefore covers those marker edits in the observed
state. This positively explains the stored-versus-live distinction at this state;
it does not globally classify other marker consumers as unused. The current
embedded marker copy's entire left-half indices also match the loose marker.

Two intermediate hypotheses are rejected: marker palette10 entry15 is opaque
white, so transparency of that entry is not the explanation. The0211B608 table
contains keyboard cues L/R/X/Y/Back/Select, not Common caption strings. Method
020161C8 is unchanged across clean, baseline and current ROMs and reaches an
original initializer; no caption renderer shim is inferred from that slot.

## Artifacts and remaining work

- `scripts/verify_radial_obj_v560.py`; complete verifier and Ruff pass.
- `work/analysis/radial_obj_v560/source_and_hardware_proof.json` (emulated state).
- Source diagnostic scope record and complete navigation schedule.
- `E:/Rota Nova translations/Generated/work/emulation_v193/radial_obj_v560`.
- Its `native_state` folder includes OAM, physical VRAM, standard palettes and
  provenance. Pinned GPU.cpp/MMU.cpp sources in the V551 evidence define the
  palette/addressing conventions used by the verifier.

The six source-based material/font checks and actual selected-caption states pass.
Remaining action controls, other atlas consumers and unobserved menu animation
states remain in the wider audit. All22 historical requirements retain exact
scope and all18 original plaque/hint entries remain incomplete. Current candidate
stays experimental V558, SHA256
bf62f246f485c7adf9a763c7765bc63476128f73f6cce983717bf297877cff6d.
The full graphics goal remains active.
