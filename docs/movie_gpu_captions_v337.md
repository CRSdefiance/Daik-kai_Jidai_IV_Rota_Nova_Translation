# Complete edited M28 caption pixels V337

## Results

Every one of the **22 edited M28 textures** has at least one exact match for all
nontransparent ink and shadow pixels in actual DeSmuME GPU captures. Comparisons
use native 5-bit channel precision.

The opening main title matches all 4,941 pixels; gold Rota Nova matches all 3,437.
Twenty progressive Hodram name textures (27-46) match their complete nonzero planes.
The final **Hodram Joakim Bergstrom** matches all 3,047 pixels from frame 3667.
Leading, internal and trailing lettering and source shadows are included.

## Capture and scope

The original capture spacing of 30 frames missed brief reveal steps. A new cold
boot captures all **161 consecutive frames, 3540-3700**, without changing inputs.
The run terminates normally at frame 4000. ROM/report/PNG hashes, input identity,
absence of savestates and callback errors, and the full frame interval pass.
The optional runner `--capture-window FIRST LAST` records its interval in the
report; omitted arguments preserve existing capture behavior.

The same research-only M28-through-M20 file substitution is used as V336.
The production V326 ROM remains unchanged, SHA256
`fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1`.

A prefix's pixels can also match a later longer name. These comparisons establish
complete visible ink, not which texture was bound at every frame. Transparent
background pixels and every transition are outside this comparison. Intended
normal caller, legitimate unlocks, route ending gameplay and physical hardware
remain unverified. This does not close legacy raw-art or other movie requirements.

## Audit status

Both audits and requirements 5/6 record the result. All 18 plaques and Weapon/Armor
variants remain incomplete. User-exempt low-resolution Online images remain
excluded. The full graphics goal remains open. Revisit older record-based checks
at actual completion.

Evidence: `work/analysis/movie_gpu_caption_v337/proof.json`,
`work/emulation_v193/movie_gpu_caption_v337/capture_report.json`, and V336 captures.
Reproduce pixel checks with `scripts/verify_movie_gpu_captions_v337.py`.
Focused Ruff passes for the verifier and capture runner.
