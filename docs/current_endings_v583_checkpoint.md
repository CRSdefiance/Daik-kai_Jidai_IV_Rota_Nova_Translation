# V583: current Hodram, Lil and Maria endings

Production remains experimental V581. Three fresh DeSmuME cold boots now exercise
the original M30/M31/M32 movie paths in that exact ROM. No movie, translation,
playable ROM, release profile, patch or canonical baseline changes.

## Original paths and isolated setup

The ending fixture admits the exact V581 ARM9 only after five ending/captain/
teardown/playback code ranges match clean source. Four further FLS update,
projection, selection and upload ranges also match clean source. All four M29-M32
files remain byte-identical to clean source. Wrong-captain and unverified-version
requests are rejected. The older V534/V573 version guards remain intact.

Each run changes only the original temporary gameplay-state byte022796BC from1
to4. The unmodified selector reads the active captain and chooses29+captain.
Actual movie pixels come from the running production ROM; no movie substitution
or injected drawing code is used. Both original E-drive donors, their historical
test sources and their new disposable copies retain their source hashes.

| Captain | Frames | Fixture frame | Setup |
| --- | --- | --- | --- |
| Hodram |24000|3000|Copied Athens donor; recorded controls also clear pending dialogue. |
| Lil |34000|18000|Fresh New Game with recorded ordinary controls; no existing save. |
| Maria |15000|3000|Copied Maria donor. |

The authorization is for isolated tests, not earned route completion. The lower
gameplay scene can remain visible while the fixture plays an upper-screen movie.
These lower-screen contexts are not presented as normal earned-ending composition.
All three processes finalized normally. No gameplay save acceptance is performed.

## Whole native frames, credits and prompts

Captures every4 frames, with every-frame windows12000-14000 for Hodram and
18000-21000 for Lil, produce these exact source matches:

| Captain | Complete source-template upper frames | Distinct full-screen templates | Complete credit composites | Shared historical/current upper frames |
| --- | --- | --- | --- | --- |
| Hodram |1936|6,7,8,9,11|59|91|
| Lil |2994|4,5,6,7,9|59|130|
| Maria |2117|1,2,3,5,7|59|100|

Each upper-frame comparison includes49,152 pixels. Each credit plane is the
original English `SpecialThanks : BRIDGE Inc.` at(0,90), including all306 white
source strokes,961 dark source points, complete first/final lettering and blank
cells. Each current movie has20 observed uniform five-bit gray levels:
1,3,4,6,7,9,10,12,13,15,17,18,20,21,23,24,26,27,29,31. These are observed output
states, not internal GPU alpha or all possible intermediate shades.

The original complete `Save the ending data?` prompt passes238 ink points plus
all blank cells in each run, at frames20280/26280/11280 respectively. Whole upper
movie frames match historical V534 footage at the recorded shared frame numbers;
underlying lower gameplay is not included in those comparisons.

## Split-image pans

The dense current runs add836 exact Hodram and2,344 exact Lil full upper-frame
source-window compositions. All three source128-row tiles are considered:

- Hodram's unscaled windows establish2/1 adjacency. Both2/1/3 and3/2/1 remain
  consistent with this particular pixel-window model. Unobserved order is not
  chosen from those windows.
- Lil's windows uniquely establish3/2/1. Texture3 now has all rows0-127 observed
  (the old sparse proof missed rows0-2); texture2 has all128 rows observed;
  texture1 has rows0-63. Its remaining64 rows are real source artwork, outside
  this exact unscaled-window proof.

Other zooms, fades and source rows are not silently treated as full opaque matches.
Source M30 texture5 (woman at a window) and M32 texture4 (seated woman with flowers)
were separately viewed at their actual header bounds. No readable Japanese
instruction/caption is observed. Retain the original contextual illustrations.
Neither receives a new complete static native-frame match from this batch.

## Previously unverified M30 shooting star

The original M30 texture4 is a sparse gray streak with46 nonzero points, not a
photographic pan segment. Its native effect is now positively identified:

- Every one of the2,001 dense frames12000-14000 must exist for the search.
- 25 consecutive frames13337-13361 contain all46 source points at their original
  RGB5 values18/22, moving through six distinct positions.
- Four entry frames13333-13336 contain27 visible source points, with19 outside
  the original viewport. Four exit frames13362-13365 contain19 visible points,
  with27 outside. No clipped source point is counted as visible.
- Together these cover33 consecutive native frames and1,334 exact visible
  source-stroke pixel checks. Before/after frames13332/13366 reject the complete
  source pattern as negative controls.
- All observed origins agree within one pixel with original V312 pre-GPU quad
  geometry for source counters327-334. The four current FLS code ranges and source
  movie bind that historical controlled model to unchanged current inputs.

Transparent source points are not assumed black: the star overlays the original
night sky. This proves the visible stroke, its movement and entry/exit clipping;
it is not a full independent background compositor, an instruction trace of the
running core, or an internal GPU-alpha measurement. No correction is required.

## Evidence, reproduction and remaining scope

- Verifiers: `scripts/search_ending_effect_v583.py`, then
  `scripts/verify_current_endings_v583.py`; targeted Ruff passes.
- Guarded fixture: `scripts/native_ending_fixture_v537.py`.
- Proof: `work/analysis/endings_current_v583/current_endings_proof.json`.
- Source/code/save provenance and all three exact input schedules are in the
  same analysis directory. Raw reports, PNGs and read-only pause RAM are under
  E:/Rota Nova translations/Generated/work/emulation_v193/endings_current_v583_
  followed by hodram/lil/maria.
- 32 unmodified full screenshots, the native streak sequence sheet, reports,
  replay schedules and hashed provenance are saved under
  E:/Rota Nova translations/Screenshots/Test fixtures/V583 Current endings.
  None is promoted to guide evidence.

For reproduction, use fresh output directories, V581, each provenance-named copied
save where applicable, the recorded captain-specific input file and frame budget,
`--capture-every 4`, its declared `--capture-window` where applicable,
`--capture-at <fixture frame> --dump-capture-ram --pause-at <fixture frame>
--dump-pause-ram --allow-ending-fixtures`. At the pause request the declared
`ending_captain` and continue until the declared frame budget; stop normally at
the final pause. Do not preload a save for Lil. Inspect new reports before
rebinding the named evidence directories.

Candidate SHA256 remains542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68;
patch SHA256 remainse411c4f24e4669309f262493320b08708c9f376da2b9bd80631a002d2f34e415.
Rafael's prior V573 playback remains separate, bound to unchanged original movie
and code inputs; this is not four new V581 runs. All18 original plaque entries
remain incomplete and all22 historical objects retain their exact scope. Five
miniature callers, Confirm parent, broader materials and other legacy/event/movie
contexts remain open. The graphics goal stays active. Revisit older record-based
checks at actual full completion.
