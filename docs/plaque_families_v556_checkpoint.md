# V556 broader material review and ship plaque prototype

The previous goal turn made progress: integrated V555 restored424 original
plaque margin pixels and passed61 complete native crops,17 font masks,56
unchanged startup frames and exact patch reconstruction. This turn expands the
global texture review to additional active graphics families.

## New affected family

Original/current whole-atlas comparison identifies broad horizontal pale bands
in all11 localized Ships information plaques. They have not received the recent
crew/person fine-grain correction. The earlier statement that Ships V2 retained
complete source plaques is insufficient as a background quality claim: current
label faces visibly differ from the original material. Ships remains in the
global texture audit even though its English text and earlier gameplay layer
were accepted.

The current11 labels are Water, Food, Crew, Holds, Cargo, Fore/Aft, Square,
Marines, Guns, Cannon and Hull. The prototype retains every accepted term and
glyph position; it makes no new terminology decision based only on an atlas.
Marine-quarter and gun-placement labels still deserve contextual consistency
review beside the runtime numbers and the Assign Sailors terminology.

## Source-based full correction prototype

`scripts/review_ship_plaque_texture_v556.py` restores original wallpaper outside
the plaque faces inside all11 historical erase rectangles, then completes every
face with fine source grain and genuine clean native frame edges. All erase
passes precede all face passes because the old rectangles overlap a preceding
plaque's bottom rows. This also removes the extended stale horizontal strips
created by those overlaps. Only then are complete English masks redrawn at
their exact inherited positions.

Grain uses clean towninfo Share strips [2,62,43,74] and [85,62,124,74]. Bevels use
the original Type frame [8,20,48,36]. The source grain is reconstruction for
concealed or resized regions, not exact recovery of each ship plaque's hidden
pixels. Header, palette, dimensions and all unowned pixels remain unchanged.

All11 independent native-font masks, including every first/final letter, match
the current atlas exactly. The actual face bounds are16 pixels tall at historical
box top+7, not the full23/24-pixel erase rectangles. This prevents overwriting
wallpaper above each plaque. Native display and runtime icon overlays remain
unverified for this research artifact.

An initial whole-region black-index check fails on Hull. Exact diagnostics show
that the clean divider at row143 shares the ink index and crosses the blank
first font row. The corrected check verifies every owned divider pixel against
the original source and independently verifies every actual glyph pixel. The
source divider is not excluded from testing or classified as missing letters.

Visual review shows fine material, genuine edges and no Japanese-shaped texture
ghosts in the prototype. Broad bands in V555 are removed. No production ROM,
patch, accepted layer, registered profile or canonical baseline is changed.

## Other materials inspected

All five name-entry labels use dark gradient plaques, not gold wood. All five
fleet rows use patterned brown wallpaper, not gold wood. Current/source whole
atlases are saved, and neither reviewed family shows the ship plaque's broad
gold band artifact. This is a material/style observation, not complete native
or embedded-alias verification. Do not substitute a gold donor into these assets.

## Evidence and next gates

- `work/analysis/plaque_families_v556/ship_source_current.png`.
- `name_source_current.png` and `fleet_source_current.png`.
- `ship_texture_prototype_review.png`.
- `ship_texture_prototype_proof.json`.
- `ship_RESEARCH_ONLY.pxl`, explicitly not a playable release.
- Ruff passes for the new research verifier.

Next: test the complete Ships screen with runtime cargo/cannon/sail sprites and
numeric fields, confirm complete plaque crops and Back/ship selection, then
register the full inherited V555 stack plus the correction and reconstruct its
patch exactly. Keep the name-entry gradients and fleet wallpaper in the wider
audit. All22 historical requirements are retained and all18 original plaque/hint
entries remain incomplete. The graphics goal remains active. Current production
candidate remains experimental V555, SHA256
8d64339a6376e713526b78e1279f88c2db3ecd0648171aaad7a17511f5b50654.
