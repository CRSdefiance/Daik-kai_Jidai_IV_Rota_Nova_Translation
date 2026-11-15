# Shared native FLS bind/decode/upload pipeline V334

V326 remains unchanged, SHA256
`fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1`.
No ROM, artwork, patch or release-profile change was needed.

## Combined native execution

All270 source-observed visible binding combinations are now tested through one
shared native object per case. The original constructor/parser and texture loader
allocate and bind the observed poses. Their real queued jobs then execute the
original decoder worker, completed-job upload service and SDK destination selection.
The queues are drained to their original idle state before data is checked.

This connects the formerly separate V332 zero-offset uploads and V333 shared
allocations. Native allocation offsets are used; destinations are not all forced
to zero. Original SDK handling of physical split spans and any small CPU copies
executes alongside the declared immediate DMA model.

Inputs remain explicit: recorded native poses/frame counters/global controls,
captured runtime globals, fresh object and modeled LCDC memory. No source picture,
role dictionary, renderer instruction or production data is changed.

## Full observed-combination results

Current English and clean Japanese files each pass270 cases:540 pipeline fixtures,
covering all260 compressed textures across14 files. Their native bindings and
material commands match. Each version's final data is compared independently
with its own decoded payload, because English artwork intentionally differs.

Every simultaneously visible texture row and its palette matches after all shared
uploads complete. Per version, **18,754,624 bytes** are checked across the270
combinations. This total includes repeated textures in different combinations;
it is not a new unique-file inventory count.

Pixel spans use the original visible height and padded row stride, including
right-row padding. Unused padded bottom rows are not claimed to survive later
shared writes: their separate full-buffer single-texture evidence is V332.
Native logical offsets are correlated with the physical spans selected by the
SDK's actual copies, so crossing a bank boundary is not flattened into an
assumed contiguous address. Every native decode/upload queue finishes idle.

The source decoder, loader, upload and bank-selection code ranges remain exact.
The full process ended normally with exit0. Focused Ruff and the result recorder
pass; no failing combination was omitted or substituted.

## Remaining hardware and playback requirements

The DMA/LCDC setup is an isolated memory model with immediate completion. It does
not model hardware timing, IRQ delivery, GPU-visible bank aliases, texture fetch,
screen/depth clipping, alpha blending or final framebuffer pixels. The results
prove shared CPU-side data coexistence under the captured bank setup; they are
not actual multi-texture GPU composition or ending/Gallery playback.

Movie-lifetime release/recycling and transitions remain open. Each observed
combination starts from a fresh native object, not a claimed continuous movie.
The raw root resource has no observed visible pose in its tested path; its
intended caller/raw loader/usage remains open and no global-unused claim is made.

Both graphics audits, requirements and progress documents record this combined
evidence. All18 plaque/hint entries and Armor/Weapon variants remain incomplete.
Other legacy/gameplay gates remain open. Low resolution Online screenshots remain
exempt. The graphics goal stays active; revisit older record-based checks at
actual completion.

## Reproduction

- `scripts/research_fls_shared_upload_v334.py --all`.
- `scripts/record_fls_shared_upload_v334.py`.
- `work/analysis/fls_shared_upload_v334/all_shared_upload_proof.json`, `summary.json`,
  M22 exploration, progress and run log.

These are controlled native pipeline fixtures, not a whole-route or physical-device
verification.
