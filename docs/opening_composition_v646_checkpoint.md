# V646: ordinary opening source composition and all M28 texture views

The preceding V645 turn made progress with the original duel-name context.
This turn advances the remaining movie/composition work on unchanged V640. No
ROM, patch, artwork, wording, registry, canonical baseline or release pointer is
changed. The full graphics goal remains active.

## Ordinary cold boots and source coverage

Five successful runs use the original startup flow without inputs, battery saves,
savestates, cheats or movie-slot substitution. They reside under
`E:/Rota Nova translations/Generated/work/emulation_v193/opening_composition_v646_`:

| Run suffix | Frames | GPU checkpoints | Purpose |
|---|---:|---:|---|
|actual|7000|192|Initial pending-list/source-binding investigation|
|detail|7400|420|Fill missing texture bands; four additional CPU/VRAM exports|
|committed_v2|7400|25|Pilot committed-list and source-VRAM comparisons|
|committed_full|7400|611|Complete source-view coverage and final RGB verification|
|baseline|7400|0|Independent original run without state exports|

The initial `committed` attempt stops with a protective range rejection at706.
It receives no completed-run credit. The original source allocates render arrays
on the heap; restricting those arrays to DLL image sections was incorrect. Final
reads use source-derived pointers and strict source array limits, with committed
readable allocation checks before copying. No source state is loaded or written.

All170 M28 native source views are represented in169 exact source-equivalence
groups. Textures30/31 have identical pixels and palette; these captures do not
distinguish their runtime IDs. Every complete native-view index cell and palette
byte matches the actual texture VRAM. Every sampled texel lies inside the checked
native extent. Unused power-of-two padding is not assumed uploaded or cleared.

All611 sampled complete upper-screen compositions match every RGB pixel:
30,031,872 comparisons without exclusions.475 cases use M28 and136 use the
separate original logo movie.61 complete black samples are retained, with no
visible-picture negative claim. Source-file transitions can leave a committed
image after its RAM controller has gone; complete VRAM/source matches remain
separate from controller lifetime. This is not a check of every intermediate
video frame, physical hardware or a full campaign.

## Why the former comparison produced false mismatches

The pinned core's `gfx3d_savestate()` serializes the list currently being built.
`gfx3d_doFlush()` separately latches the committed renderer list. At rapid changes,
the current FLS metadata can already select the next image while the display
still shows the preceding committed image. Applying the older two-frame pending
list rule to M28 yields14 mismatches. Those diagnostics remain intact.

The new read-only exporter uses the exact DLL SHA and original SFORMAT table
anchors. Both304-byte state layouts and all21 declared member addresses are
checked against live binary records. Native POLY/VERT sizes are40/64 bytes.
Heap render-array reads are restricted to their source-declared sizes and checked
with VirtualQuery. Main RAM, geometry and source VRAM remain unchanged by reading.
The exact executed exporter source is archived; its maintained version adds a
redundant descriptor assertion independently checked against the same DLL records.

Source MMU bank controls bind A/B to texture slots0/1 and G to texture-palette
slot0. Actual packed source indices and complete palettes select their ROM views
without looking at screenshot colors. The GPU color framebuffer is not used as
expected source data. Four unsafe-range/wrong-core controls are rejected before
native copying. All recorded anchor addresses are independently reconciled with
the pinned PE records.

A fixed one-frame committed-list-to-display relationship passes every final case.
Dense title/name intervals reject alternatives0/2/3 with explicit counterexamples.
One remaining mid-fade discrepancy was the source renderer's automatic translucent
Y sort: original order0,1,2,3,4 becomes0,2,3,4,1. The lower sky layer consequently
blends over part of the gold subtitle. Using the original maxY/minY/stable-index
rule resolves all3260 differing pixels while retaining the recorded alpha8.
An attempted fitted alpha1 still differs at679 pixels and is explicitly rejected.
No alpha fitting or pixel waiver enters the final proof.

## Complete English planes, boundaries and original art

Every ink/shadow texel of all22 edited M28 planes is sampled in an opaque context:
the main title, gold subtitle and20 progressive name cards.44 controls remove
leading/trailing title ink, the first revealed name prefix or the last distinct
name-reveal unit. Every control produces a visible mismatch. The original single
outer-column test could erase only a black shadow matching its backdrop in three
cards; that diagnostic is retained rather than described as a missing letter.
The revised name controls use the original stored progressive sequence, including
the30/31 equivalence, rather than invented glyph positions or widths.

All original M28 palettes, flags and native dimensions remain exact clean source.
The20 inherited name-card records repartition palette padding and compressed pixel
space within unchanged whole slot ends. Assuming all records equal clean was
incorrect; current M28 remains byte-exact V573. Only the same22 source image planes
differ from clean; all other148 decoded image planes remain source art. Logo.fls
has four textures: only its already-localized genre card3 differs, with original
records/palettes retained, and the whole current movie remains V573-exact.

The similarly named loose `/_pxl/logo.pxl` is title/subtitle art; logo.fls texture3
is the separate genre card. Their original/current comparison sheets demonstrate
that they are different images. This does not establish an ordinary consumer for
the standalone loose logo or justify replacing the genre card with title art.

## Baseline, visual review and saved evidence

The separate no-export run repeats the same7400-frame/no-input path. Every shared
complete two-screen frame matches the exported run, including all blank space,
backgrounds and lower-screen controls. Exact counts are recorded in the proof.
This independently checks that the new reading method does not alter those frames.

Twelve actual upper-screen anchors were visually reviewed, including the complete
blue/gold title, intentional fade, progressive/full name and several story scenes.
The complete native825/2001 screenshots were reviewed separately. This is not a
claim of individual visual inspection of every one of the611 comparisons.

- Proof: `work/analysis/opening_composition_v646/opening_composition_proof.json`.
- Native/source verifier: `scripts/verify_opening_composition_v646.py`.
- Export-invariance/anchor finalizer: `scripts/finish_opening_composition_v646.py`.
- Exact source exporter snapshots and failed diagnostics remain in that directory.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V646 Opening source composition`.
- Two unmodified ordinary startup guide candidates: full title825 and full name2001,
  under `Screenshots/Guide candidates/V640 Opening movie`. Publication is not approved.

V640 remains the compiled experimental ROM, SHA256
93868a0b250a3b52897225dac48ab29e0b14d1f097208ca9a418208dd29d0b9e.
This adds no new full921-asset/57-block preservation run. Existing release bytes
and hashes remain unchanged. All18 original plaque/hint objects remain incomplete
and all22 historical requirement objects retain exact scope. Miniature/Confirm
parents, white village-card contexts, raw comics, standalone/legacy title and map
consumers, other movie/material variants, wood-texture acceptance and final release
acceptance remain open. The four low-resolution Online exemptions and brown-mark
retention remain. Older record-based checks remain due at full-goal completion.
