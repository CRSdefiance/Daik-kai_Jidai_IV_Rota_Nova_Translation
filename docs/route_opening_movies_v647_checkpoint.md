# V647: ordinary route opening movies and complete caption boundaries

Evidence checkpoint for the existing V640 combined candidate, SHA256
`93868a0b250a3b52897225dac48ab29e0b14d1f097208ca9a418208dd29d0b9e`.
No ROM, patch, registry, canonical or release-pointer changes.

## Verified scope

Normal New Game/captain selection plays original Rafael M20, Lil M22 and Hodram
M24 without later skip inputs, saves, savestates, cheats, substitution or RAM writes.
Three export runs and three independent no-export baselines terminate normally.
Original captain getters and live movie controllers identify the expected route.

All 36 native source views (28/3/5) bind complete original palettes and native
indices to captured texture VRAM. Pinned-source committed geometry and native Y
ordering reconstruct 94 complete upper-screen RGB frames exactly: 4,620,288 pixels,
without excluded differences. The established fixed committed-to-display delay
is one frame; each route supplies counterexamples to zero delay. All 185 distinct
complete two-screen baseline captures match, totaling 18,186,240 RGB pixels.

All three whole FLS files remain exact V303. Original clean records, flags,
palettes and dimensions are preserved; only the expected five caption planes
differ from clean. Their 8,559 complete letter/outline texels are inside the
actual sampled native view. All ten leading/trailing white-fill-column deletion
controls visibly fail the whole-RGB comparison. The five-caption native/enlarged
sheet was visually inspected for complete wording, punctuation and outlines.
No new wording was authored; faithful translation review remains V303.

The old V299 Lil card1 has exactly 42 nonzero texels outside the actual sampled
native view: 12 white fill and 30 black outline. This reproduces its original
source clipping mechanism without changing the ROM or substituting played art.

## Three post-movie boundaries explicitly remain open

All 97 planned checkpoints are accounted for. Rafael3140, Lil2860 and Hodram3120
have ended their expected live movie controller and are not counted among the
94 independent movie compositions. Software BG3 bitmap overlays now participate.
Adding captured bankD bitmap pixels gives zero next-frame differences for Rafael
and Hodram, but 1,801 for Lil. Lil's same-frame comparison is exact; Rafael's
same-frame comparison differs by 1,344 pixels. These diagnostics are retained.
A per-case lag fit is not accepted. Captured finished bitmap overlays do not
independently prove original software painting. Their timing/paint verification
remains open; these comparisons alone do not establish a translated-art defect.

A separate diagnostic compares the ROM-derived 3D backdrop with the core's
serialized 3D framebuffer at each boundary. All three match completely. This
narrows the outstanding discrepancy to software-overlay composition/timing;
the renderer framebuffer is used only as a diagnostic, not expected source art.

## Evidence and remaining scope

Proof: `work/analysis/route_opening_movies_v647/route_opening_movie_proof.json`.
Full captures/native exports remain under the corresponding `route_opening_movies_v647_*`
folders in `E:/Rota Nova translations/Generated/work/emulation_v193`.
Review archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V647 Route opening movies`.
Five ordinary unmodified guide candidates: `E:/Rota Nova translations/Screenshots/Guide candidates/V640 Route opening movies`.
Guide candidates are not publication approved.

All 18 plaque/hint entries remain incomplete and all 22 historical scopes remain
exact. Online screenshot-body exceptions and brown-mark retention remain effective.
Unsampled movie frames, other graphics/legacy consumers, maps, material review,
whole campaigns, hardware and final acceptance are not inferred. Full goal active;
older record-based checks remain due at actual completion.
