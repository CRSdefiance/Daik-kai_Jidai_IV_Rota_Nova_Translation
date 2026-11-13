# V578: omitted ending-credit planes and native composition checks

The preceding turn made progress by completing the calibrated existing-capture
search. It yielded no positive miniature-caption consumer. This turn verifies
previously omitted ending-credit planes, adds current Rafael playback and checks
split-image pans. Production remains registered experimental V573, SHA256
`f987f1c56ba5641544e5c84698c59351e39465b15001601adddf697698d89a77`.
No artwork, playable ROM, patch, registry or canonical baseline changes.

## Control-binding follow-up

Executing the original resource initializer confirms that owner 023139C0 really
registers `_pxl/kakutei.pxl`. Its initialized filename pointer is field +12.
Neighboring initializer literals must not be interpreted as a simple alternating
owner/filename array: that would incorrectly assign this owner to the next file.
The earlier Confirm mapping was correct; no corrective ROM patch is needed.
The five tiny-caption consumers and Confirm's ordinary parent remain unresolved.

Additional bounded pixel/tile-unit rectangle queries in the static code and six
existing RAM snapshots yield no leads. They exclude neither computed/indirect
paths nor other states. Diagnostics are retained under
`work/analysis/miniature_consumers_v578/`, including
`Confirm_registration_proof.json` and `runtime_rectangle_leads.json`.
These negatives do not create native-display completion credit.

## Four original-English credit planes

The V537 ending verifier checked large full-screen scenes but omitted the
256x16 credit planes: M29 texture 6, M30 texture 10, M31 texture 8 and M32 texture 6.
They contain the original English `SpecialThanks : BRIDGE Inc.`. The original
credit art is retained, including its typography; no new Japanese translation
is required for this plane.

Each is now found completely in its actual historical V534 ending capture at
native origin (0,90). All 306 white source points and 961 dark source points match.
At full intensity, all 4,096 tile pixels and all 49,152 upper-screen composite pixels
match the expected original credit-on-black image. Leading/trailing strokes and
blank cells are included. The four complete credit displays were visually reviewed.

All four ending FLS files remain byte-exact to clean source in both historical
V534 and current V573. The five relevant ending/captain/teardown/playback code
ranges also remain exact source. Historical evidence remains labeled V534; it is
not described as four new current-build playback runs. Identical credit bitmaps
alone do not distinguish their separate GPU texture instances.

## Current V573 Rafael run

The original one-byte ending-state fixture now also accepts the exact verified
V573 ARM9 hash, retaining its original V534 hash and all captain/state guards.
Its five source code ranges are checked before using the new version. Replaying
all four historical fixture-selection contracts still produces their recorded
metadata. Wrong-captain and unverified-ARM9 negative controls are rejected.

A new V573 cold boot uses an isolated copy of the existing Rafael save. At
frame 3000 the fixture changes only temporary gameplay state 022796BC from 1 to 4.
Original code selects M29; no movie-file substitution or ROM instruction change
is used. The run reaches frame 11600 and finalizes normally. The original donor
and fixture source remain byte exact. This is authorized synthetic testing,
not earned route completion or a whole-game playthrough.

Captures every four frames verify:

- 1,858 full upper-screen source-template matches covering textures 1,2,3,4,5,7,
  including the original ending panels and publisher logo.
- 60 complete credit composites at 30 observed gray levels: 1..29 and 31. Every
  white source stroke remains present, with all 49,152 upper-screen pixels equal
  to the corresponding uniform credit state. Level 30 is not claimed observed.
- 71 entire upper-screen captures equal their same-frame historical V534 captures.
- The complete `Save the ending data?` prompt, including first/final letters.

The uniform gray states describe observed pixels. They are not internal GPU-alpha
measurements or proof of the three intervening frames between samples. Full,
mid-fade and ending-save screenshots were visually inspected. No credit clipping
or missing-letter defect is found in these observed states.

## Split-image pans and source effect art

The historical Hodram and Lil movies contain 256x128 photo segments which the old
full-screen-only comparison could not identify. The new comparison assembles
candidate source orders and compares complete 256x192 displayed windows:

- M30: six exact full-frame composites. Observed windows establish the 2/1
  adjacency; both orders 2/1/3 and 3/2/1 remain consistent. Unseen order is not chosen.
- M31: 24 exact full-frame composites establish the 3/2/1 source order across the
  observed pan. Source texture 3 rows 3..127, texture 2 rows 0..127 and texture 1
  rows 0..63 are covered. The other rows contain source art, not empty padding;
  they are explicitly outside this exact opaque-window evidence.

M30 texture 4 is a separate sparse gray streak consistent with a shooting star,
with 46 nonzero source points. It is visually reviewed and retained as contextual
art; no Japanese text is observed. It must not be forced into the photographic
pan model. An exact source-color search of the old sparse captures provides no
positive effect match; its actual transform/fade/display remains unverified.
No unexplained pixels are erased or silently masked to make a comparison pass.

These pan results add historical native composition evidence bound to unchanged
current source files. Fresh current Hodram/Lil/Maria playback is not claimed.
Other transformations, fades and unobserved portions remain outside their scope.

## Saved artifacts and scope

- `scripts/verify_ending_credits_v578.py`; `--historical-only` is available for
  the historical source-plane checks. Targeted Ruff passes.
- `scripts/native_ending_fixture_v537.py`; exact V534/V573 version guards.
- `work/analysis/ending_native_v578/native_ending_credit_proof.json` contains all
  source/capture hashes, fixtures, matched frames, masks, pan candidates and limits.
- `current_fixture_provenance.json` and `rafael_inputs.json` record the new run.
- Current raw frames/RAM/report: E:/Rota Nova translations/Generated/work/
  emulation_v193/ending_native_v578_rafael.
- Fifteen unmodified full screenshots, reports and hashed provenance:
  E:/Rota Nova translations/Screenshots/Test fixtures/V578 Ending credits.
  Current V573 and historical V534 images have explicit separate filename labels.

Reproduce with the recorded input file, V573, the provenance-named copied Rafael
save, `--frames 11600 --capture-every 4 --capture-at 3000 10800 11280`,
`--dump-capture-ram --pause-at 3000 --dump-pause-ram --allow-ending-fixtures`.
At 3000 send `{"ending_captain":0,"until":11600}`, then `{"stop":true}` at 11600.
Use a fresh output directory. The verifier intentionally names the recorded
evidence directory; inspect a new run's provenance before rebinding it.

No images are promoted to ordinary guide evidence, and publication is unapproved.
All 18 original plaque entries remain incomplete; all 22 historical requirement
objects remain exact. The broader material audit, unresolved controls and other
graphics gates remain open. Revisit older record-based checks at actual full
goal completion. The full graphics goal remains active.
