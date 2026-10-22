# Build continuity protocol

This is the mandatory procedure for every model and every playable ROM candidate.
Its purpose is to let translation work accumulate without reverting previously
accepted menus, graphics, names, goods, or dialogue.

## Sources of truth

1. `AGENTS.md` contains the non-negotiable repository rules.
2. `translations/release_stack.json` is the machine-readable layer registry.
3. `out/raphael_natural_v2_accepted_base.nds` is the immutable binary baseline. Its
   current SHA-256 is
   `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`;
   the registry and builder enforce it.
4. `docs/known_issues.md` records failed experiments and renderer hazards.

Never infer quality or ancestry from an output filename. A ROM is a valid candidate
only when its neighboring manifest proves its baseline, layer stack, changed files,
and checks.

## Layer states

- **Accepted:** the user cold-boot tested the layer and explicitly approved it. The
  layer is listed in `accepted_layers` and is applied automatically to every playable
  candidate.
- **Experimental:** the layer is incomplete, failed testing, or awaits testing. It
  belongs to a named profile and is never included in unrelated builds.
- **Revoked:** the build is documented in `known_issues.md` and must not be used as a
  parent, release, or source of bytes.

Only an explicit user statement that a candidate is accepted authorizes moving its
batches into `accepted_layers`. A model must never promote a layer merely because its
automated checks pass.

## Procedure for any requested change

1. **Read before editing:** read `AGENTS.md`, this protocol,
   `translations/release_stack.json`, and the relevant section of
   `docs/known_issues.md`.
2. **Classify the work:** use a disposable research probe when mapping an unknown
   format. Use a named profile for anything handed to the user as a playable test.
3. **Preserve source locks:** author batches against the canonical baseline's exact
   internal file. Never extract translation input from a derivative ROM.
4. **Register dependencies:** if a feature requires multiple batches, add one profile
   containing the complete set. Never rely on a long handwritten list of `--batch`
   arguments for a handoff build. The builder rejects batches that are not registered
   in the selected profile.
5. **Build once:** run `scripts/build_integrated_release.py --profile <name>`. The
   builder automatically prepends every accepted layer from the registry.
6. **Audit the manifest:** confirm the baseline hash, registry hash, profile, complete
   batch list, changed internal paths, and changed record IDs. Missing accepted layers
   or unexpected files are release blockers.
7. **Run targeted verification:** run the feature verifier plus syntax/unit tests. A
   byte-level pass proves preservation, not visual correctness.
8. **Cold-boot test:** never use a save state. At minimum test the title menu, New Game
   character selection, one established story scene, town UI, and every changed screen.
9. **Record the result:** update `known_issues.md` and `todo.md`. If a test fails, keep
   the profile experimental and revoke the candidate by name.
10. **Promote only on approval:** after the user explicitly accepts the candidate, add
    its stable batches to `accepted_layers`, mark them `baked_into_baseline`, retain the
    former baseline as a rollback artifact, and update every canonical hash guard. Do
    not replace the canonical baseline casually.

## FLS subtitle viewport authoring

New FLS subtitle/label batches must set `native_viewport_policy: header-size-v2`.
The native visible width is the high16 bits of the selected texture's first
record word; the decompressed power-of-two allocation can be wider. V302 actual
movie evidence shows widths168/176/216 for M20/M22/M24, with42 missing fill/outline
pixels when a176-wide M22 card was authored against256 storage columns.
The native height is the low16 bits of the second texture record word. V304's
genre-card check shows192 native rows inside256 storage rows; centering against
storage had placed the English32 pixels too low. The v2 builder derives both
layout dimensions, rejects conflicting explicit sizes and rejects ink/outline
outside the native view. V303's width-only v1 remains supported with its original
defaults for reproduction; all its subtitle heights already match storage.
Preserve full
wording and fit the existing compressed slot; retain palette/metadata and all
unowned assets. Historical batches without this policy retain their original
behavior for exact earlier-release reproduction. V303 source-locked batches
exercise the policy and four negative storage-width cases.

## Required handoff statement

### Observed V609 late-pool expansion regression

V609's 320-byte expansion beyond V608's 123040-byte late-copy payload reproduces
a black upper screen/Press START stall. A research control retaining that storage
layout while restoring every village-label pointer and original SC2 also fails.
The deeper memory/cache/scheduling mechanism is unresolved. Complete staged-copy
or initialized-name checks alone are not startup evidence for such growth.

V610 preserves the whole staged payload, cache wrapper, startup calls and arena
bounds exactly to V608. It packs the same complete English labels into exclusively
owned source text spans, preserving interleaved RTTI and all other bytes. Future
late-pool growth must receive independent source-bound cold-boot/input regression
evidence before handoff. Do not reuse rejected V609 as a release parent. See
[V610 boot isolation and verification](village_ui_v610_checkpoint.md).

New or revised textured plaque artwork must follow
`docs/plaque_texture_workflow.md`. Compare visible texture and frames to the
original Japanese source; generated-output and glyph matches alone do not
establish faithful background restoration.

Every ROM handoff must state:

- exact candidate filename and SHA-256;
- canonical base filename and SHA-256;
- named profile;
- accepted and experimental batches applied;
- changed internal files;
- automated verifiers run;
- cold-boot areas the user must test;
- whether the candidate is experimental, accepted, or revoked.

If any item is unknown, the ROM is not ready to hand off.

## Current Sound Setup status

The former `sound_selector_en_v5.nds` is superseded. The coordinated 38-title BGM
table, interior pointer map, and 57-title SFX table were accepted with the Extras and
Common V6 candidate on 2026-09-03 and are baked into the canonical parent. Their
source-locked batches remain as reproducibility records and must not be reapplied to
the promoted baseline.

## Original graphics resource identification

Establish resource ownership from the executed original initializer's filename
field (owner+12 for this resource class), then verify the actual resident whole
file where available. Do not infer owner/filename pairs by reading two adjacent
literal words in an initializer pool: their order and grouping are not a public
table contract. V600 found that the old V164 score test paired owner023139FC
with the following filename; that owner actually initializes deckchip15.pxl.
The real deck04.pxl score owner is02313A38. Its native caller and cache evidence
supersede that old selection claim; historical generators remain unchanged for
reproduction. See `docs/score_parent_v600_checkpoint.md`.

For clipped graphics, verify the original drawing path before declaring a lost
letter from a host-side crop model. V601's negative-coordinate score cases match
the original parent/blitter and real bitmap planes; a generic source crop did
not reproduce them. Use unchanged complete digit cells or captured controller
fields as independent position evidence. Do not select positions from the letters
being tested, silently retime captures, or assume every spare word in a native
view was zeroed by its constructor. Retain foreground/3D comparison differences
separately when the complete text bitmap planes pass.

## Shared C-string label boundaries

### Source-bound story percent commands

Every playable build checks final English SC0-SC3 records after all post-batch
stages against the exact clean Japanese source. Syntactically valid conversions
can still be defects: `3% of sales` contains `% o`, and `1% share` contains `% s`.
Neither source Japanese paragraph supplies those arguments. Use the natural word
`percent` for literal story percentages. Preserve real source format commands
and source-leading `25` presentation state. The final guard does not silently
escape bytes or change native code; a failing record requires source/context
review and a registered repair. The gate concerns changed English story records;
COMMON, HELP and ARM9 retain their separate native formatting contracts.

V685's `story_literal_percent_safety` stage follows the complete V678 stack.
Its four reviewed paragraphs preserve allocations, preambles and every other
record. Existing source profiles retain their historical wrapping behavior;
the two new route-specific percent profiles opt into the existing automatic
balanced planner with identical native widths and pair-phase rules.

Profiles derived from V651 retain `captain_prompt_wrap` after the complete V640
stack. The four captain-instruction IDs269..272 use the guarded modal formatter
only at original parent020546E8. Keep the complete prose unchanged. Actual modal
bitmaps use6x12 source cells and16-pixel displayed row spacing; do not infer
their source-row metric from the screenshot spacing.

V640 fixes the inherited Americas/Med. join. For C-string labels, reserve the NUL
inside the actual owned text span; an even glyph/byte count or a fixed-text batch
slot check does not prove termination. An exact-capacity replacement needs a
typed ownership/consumer review. Do not treat adjacent zero bytes as spare text:
the word after this region-name family is an integer array used by area selection.

Profiles derived from V640 retain `region_name_boundaries` after the full V636
stack. It validates all eight complete final strings, independent terminators,
every-byte pointer ownership, adjacent nontext data and unchanged map metadata.
Keep historical generators reproducible. Do not apply a C-string rule blindly
to a proven fixed-width/count-delimited record; record that separate contract.

## Gallery captions and carousel arrows

Profiles derived from V523 must retain `gallery_caption_bounds` after the full
V518 stack. Any later scene-caption change must resolve all164 final pointers
from resident sections and the verified staged-pool copy, preserving original
arrows and requiring complete glyph extents inside[32,224]. A256-pixel bitmap
fit alone is insufficient: original arrows overwrite edge letters. Recheck the
actual Gallery consumer and preserve natural, faithful complete English titles.

## Static Historic Sites paragraphs

Profiles derived from V534 retain `site_descriptions_v3.json` and its complete
V528 dependencies. The static Gallery painter buffers printable ASCII glyphs;
LF is processed separately and does not flush an odd pending glyph. Use the
`static-site-gallery-pending-flush-v3` compiler profile: wrap at41 characters,
generate an empty cell at the end of an odd printable line before LF, and retain
zero next-line indent. Translators author one natural paragraph without padding
or manual line breaks. Raw-byte LF parity was disproved by the V532 pixel test.
Require complete native masks for every paragraph; byte retention alone missed
the V530 misplaced leading letter. Preserve all42 numbered Character labels and
21 site names when repacking their shared owned allocations. Do not move the
allocator start or grow a section to make these strings fit.

For image testing, derive supported IDs from the original Gallery image-owner
table, not its21-slot metadata count alone. Slots1/4 have null image pointers and
placeholder descriptions. `prepare_supported_sites_v529.py` selects19 real
images; declared supported fixtures are checked before emulator frames begin.
Keep historical invalid fixtures as diagnostics without display credit.
