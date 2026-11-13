# V601: original score clipping and full bitmap-plane verification

The previous V600 turn was progress: it corrected score-resource ownership and
mapped the actual result parent. It retained29 unresolved frame comparisons.
This turn verifies the score-label regions in all29 with live state and the
original drawing code. No production ROM, patch, font or graphics asset changes.

## Reproducible observation

Six fresh research cold boots reuse the exact three V600 research ROMs and the
unchanged source-save/controller schedule. Three runs capture all29 unresolved
frames plus four control frames, with five read-only native-state exports each.
Three additional runs export the seven remaining foreground-difference cases.
All captured screenshots reproduce their earlier V600 images exactly, including
every image acquired alongside a CPU/TCM/VRAM export. There is no savestate load,
frame shift or altered input to make a comparison pass.

At all33 primary frames, both complete200-byte score controllers match across
English, Japanese and blank-label runs. Their real label members retain owner
02313A38, native format4, palette0, source origins160/184 and full24-by24 extents.
Original constructors leave some spare descriptor words nonzero. The first
verifier's zero-field assumption was rejected; documented fields and complete
captured-object equality replace it. No game field was cleared to fit a test.

`headless_desmume_v193.py` now accepts optional `--capture-native-state-at` frames.
It exports the existing bounded read-only native-state format and verifies that
serialization leaves main RAM unchanged. The option is inactive by default.
New reports bind each exact frame, CPU registers, TCM, VRAM, OAM and I/O to hashes.

## The test model's clipping error

V600's position search compared partially clipped digits to a generic host crop.
That lost twelve otherwise usable position anchors. V601 selects a unique pose
using only original unchanged digit cells that are completely on-screen. These
positions come from the earlier93-update original animation replay; neither
Japanese nor English label pixels participate in selection.

The original score parent0200C054 then executes against each captured real object,
graphics context023117C4 and resident named score file. It uses original adapters
020CFDE8/020CFD6C, resource resolver020D4170 and blitter01FF92D8. No renderer, getter,
resource header, file payload, palette or SDK boundary is bridged. Only the
independently observed original animation geometry and the blank framebuffer seed
are supplied to this bounded source replay. The original transparent-pixel rules
and framebuffer/resource guards are checked.

This replaces the incorrect generic host clipping assumption. In particular,
the eight negative-left-coordinate failures now match the original native
output. It does not introduce a new clipping rule into the ROM or make a general
claim about unrelated renderers.

## Results

- All29 previously unresolved cases have exact visible score-label cells in both
  English and Japanese controls. Entry/exit cropping follows the original routine.
  V600's complete centered94-point English masks and first/final letters remain
  separately verified.
- 48 of58 entire native5 frame composites pass. The remaining ten variant cases
  occur in nine unique frames and differ only over the existing crew figure:
 4323,4351,4407,4435,4463,4519,4547,4575,4603.
- In each of those nine frames, both entire captured49152-pixel bitmap planes
  match the original painter's output, byte for byte including bit15. There are
 18 two-plane cases and3,538,944 checked bytes.
- The captured top bitmap plane also remains wholly unchanged. OAM and the full
  non-bitmap VRAM texture/palette banks are identical across all three variants.
  Captured I/O records the bitmap-bank configuration and enabled main BG0/3D.

Consequently, the29 score-label verification gaps are addressed. The nine final
composed-image disagreements are not bitmap-text defects. Their precise
foreground timing/raster cause remains unproven; they are retained as separate
background-rendering evidence gaps. This is not a claim that all final pixels or
all3D rendering states match. No source or captured frame was silently retimed.

The V600 failures remain in their original proof. The new proof supersedes their
interpretation as unresolved label checks and carries the nine foreground cases
forward explicitly. The specific original native result renderer has strong
controlled display evidence; ordinary battle activation, earned outcomes, all
other result states and physical hardware remain outside this fixture.

## Artifacts and scope

- Verifier: `scripts/verify_score_boundaries_v601.py`; Ruff and Python compilation.
- Proof: `work/analysis/score_boundaries_v601/boundary_proof.json`.
- Exact target list: `frames.json` in that directory.
- Six immutable capture reports and their raw snapshots on E under
  `Generated/work/emulation_v193/score_boundaries_v601_*` and `score_BG3_v601_*`.
- Twelve full unmodified research screenshots, reports, verifier and provenance
  under `Screenshots/Test fixtures/V601 Score boundaries`. No ordinary guide or
  earned-result credit; publication is unapproved.

Production remains experimental V599, SHA256
`1c72049ca2eba551825d67de2429b4ac9751179183afc2ddb5749666d398eba5`.
Its patch SHA256 remains
`2aa5a523cfef3165db2eae31643b2d66e3e08a75aa709c025066958a144ffc9f`.
The release registry, canonical baseline and all graphics files remain unchanged.
All18 original plaque entries remain incomplete and all22 historical objects are
retained exactly. Other miniature/Confirm, legacy/village/movie/material and
final acceptance gates remain open. The graphics goal remains active; revisit
older record-based checks at actual full completion.
