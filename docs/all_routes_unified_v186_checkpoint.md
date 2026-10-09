# Combined V186: smoother English title and duplicate-caption omission

2026-10-05. Focused user-requested correction: **Uncharted Waters IV**
now has smooth blue beveled lettering with shaded edges, replacing the prior
binary-alpha, thick white outline. The small **ロッタ ノヴァ** label is a phonetic
rendering of Rota Nova; its redundant English duplicate is omitted from all four
Rota Nova title copies. Original gold-logo pixels, copyright, palettes, native
headers/records/dimensions and unowned scenery remain preserved.

**15 focused tests**, whole byte-identical V185 reproduction, all **463 registered
batches** and inherited terminal stages, exact saved artwork/manifest identity,
and clean-ROM patch reconstruction pass. Only M28 and the three Rota Nova PXL
title resources change versus V185. V186 is experimental; native display and
cold-boot acceptance remain pending. The broader graphics goal **stays paused**.
See [V186 title checkpoint](all_routes_unified_v186_checkpoint.md).

## Design correction

The user screenshot showed a real styling defect: the earlier authoring scripts
thresholded antialiased letter coverage at 128, drew thick solid white outlines,
and used flat per-row blue shading. This introduced visibly stepped edges and
made the English wordmark differ from the source's dimensional gold logo.

The replacement uses a new blue beveled serif wordmark generated with the built-in
**image_gen** tool, retaining exact **UNCHARTED / WATERS IV** text. The tool's
full prompt, reference and asset identity are saved in
`work/qa/title_restyle_v186/generation.json`. The complete transparent source
asset is saved in `translations/assets/blue_title_wordmark_v2.png`.

The bitmap is fitted to 42 native pixels high with Lanczos projection; only
virtually transparent generation dust outside the visible wordmark is excluded.
Soft edge coverage is blended against the original donor scene before mapping
to each unchanged game palette. There is no binary-alpha letter-edge threshold,
new runtime font, changed texture dimension or widened native crop. Native-size
and integer-enlarged comparisons were reviewed for every changed copy.

The original small Japanese **ロッタ ノヴァ** label says Rota Nova phonetically.
It duplicated the existing gold Latin logo after translation. Following the
user's permission to restore or omit it, this version omits it. Source-backed
scene restoration fills the caption area on the two title screens; the
standalone/opening logo backgrounds are cleared in the caption area while
protecting adjoining gold artwork. The standalone caption's lower white fringe
was caught during review and included in the new bounded removal region.

Restoration via source donor/palette mapping is not a claim of exact recovery
of the hidden original sky/water. The original gold-logo pixels, copyright and
unowned scenery are preserved; all source headers, palettes, texture sizes,
native records and unrelated movie bytes are exact. Actual game display,
composition, palette alpha and cold-boot readability still require feedback.

## Integration and verification

Profile **all-routes-unified-v186** contains the full **463 experimental batches**
and all inherited terminal repair stages. All accepted layers remain baked into
the canonical baseline; zero additional accepted batches applied. Four versioned
title batches replace only their v1 predecessors:

- `translations/opening_m28_title_art_v2.json`
- `translations/rota_title_logo_art_v2.json`
- `translations/rota_title_title03_art_v2.json`
- `translations/rota_title_title05_art_v2.json`

All earlier IDs, other batches, relocations and repair stages are retained. The
builder and shared renderers are unchanged; the complete prior V185 ROM was
reproduced byte for byte before compiling the registered V186 candidate.

Only these internal files differ versus V185:

- `/FLS/M28.fls`
- `/_pxl/logo.pxl`
- `/_pxl/title/title03.pxl`
- `/_pxl/title/title05.pxl`

The same 34 changed paths versus canonical remain in the adjacent manifest and
saved proof; ARM9 and all route/text/other graphics files are byte exact versus V185.

**15 focused tests pass**: soft native-size coverage, complete bounded lines,
source gold/headers/palettes/records/unowned pixels, caption-fringe removal,
source hash guards, and leading/final wordmark deletions with fresh hashes.
Eight deletion cases are rejected by the complete-art verifier. Saved ROM
identity, full stack, golden menus, unchanged IDs/relocations/manifest checks and
clean-ROM xdelta reconstruction pass. Authoring script/tests pass Ruff.

## Exact handoff

| Artifact | SHA-256 |
| --- | --- |
| Candidate out\all_routes_combined_v186_candidate.nds | `b2e7ea716a761836f00516d7d7a71a8f6d4762e5406fff65601b5e443fceac0a` |
| Canonical out\raphael_natural_v2_accepted_base.nds | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Previous V185 / full reproduction | `f81509cdd809b40f654347b4b21be9a2229c80ff76204d9f2b51a60f9e0c613c` |
| Clean patch base work/clean.nds | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| ARM9, unchanged | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Builder, unchanged | `d58a3d5816f6cadea3982aeac86647057f3a724d3f99c7d3e8e7a925d6891e29` |
| Registry | `266ba20556b39532b2cb1139cb89ac81ae163660c704eca5b0f41d181cd1f75f` |
| Generated wordmark | `e357836b83dc8c527a16954d4fd5a007a102d59a33a5e7663903f9f950822d28` |
| out\all_routes_combined_v186_candidate.xdelta, 874309 bytes | `d41b57f51f2423ec771756f1bfaf2a506b17360968732889c069dce8c127588e` |

Adjacent manifest: `out/all_routes_combined_v186_candidate.manifest.json`.
Saved proof: `work/analysis/title_restyle_v186_saved_proof.json`.
Tests: `work/analysis/v186_title_tests.log`.
Reference, prompt and comparisons: `work/qa/title_restyle_v186/`.
Native-size title preview: `work/qa/title_restyle_v186/title03_native.png`.

Cold-boot without savestates: opening movie, both Rota Nova title scenes,
title menu, New Game character selection, one established story scene and town UI.
Check smooth complete lettering, absence of the duplicate caption, gold-logo
edges and the transitions into/out of the title. V186 remains **experimental**;
no acceptance or canonical promotion is assumed.

The broader graphics goal remains **paused**. This focused correction does not
clear Online/unclassified/contextual/native/gameplay gates or resume translation.
The requested follow-up on older record-based checks remains for eventual full
goal completion.
