# Native FLS texture bindings V323

Current combined ROM remains V322, SHA256
`9486a749d9ed15af618adee4f0818ce1e99a7bccd93a7daa4d639cf066db7e03`.
No ROM, artwork or patch changes were made.

## Native loading and submission evidence

The earlier V312 original timelines provide an observed pose for every one of
the 260 compressed textures across 14 FLS files. Each pose is now checked in a
fresh isolated native object against both the current English file and the clean
Japanese file: 520 binding fixtures.

Each fixture executes the original constructor/parser, frame-dependent texture
resolver, texture-slot loader, software VRAM allocators, affine math and complete
quad submission routine. The declared inputs are one observed pose, its original
frame counter and camera/color/alpha controls, and captured V309 runtime globals.
Pointers into parsed source metadata are checked, rather than replaced with
invented headers. The native loader populates the material, texture/palette
addresses and padded size fields; no hard-coded binding is supplied.

Every current/source pair produces identical bindings and 20 native register
writes. Together these are 5,200 commands per version, including full UV and
vertex submissions. Original movie code, allocator code and matrix helpers are
byte-identical in current, clean and captured RAM. Every tested current FLS file
also remains byte-identical to its V312 pose-provenance file.

An independent comparison with each original texture record checks all 260:

- Pixel format: 178 indexed 8-bit textures and 82 indexed 4-bit textures.
- Width/height and padded storage exponents in the submitted material parameter.
- All four UV coordinates, including complete right and bottom boundaries,
  from the source pose offsets and original visible dimensions.
- Normal returns, saved registers and outer stack guards.

This includes M20/27 at 168x32, M22/1 and M22/2 at 176x32, and M24/3 and M24/4
at 216x32. The genre card, logo/3, uses its original 256x192 UV rectangle inside
256x256 storage. These source-defined submissions agree with the viewport
authoring repairs and earlier separately recorded actual opening pixel checks.

## First experiment and correction

The first direct geometry-only experiment produced an uninitialized texture
parameter because it omitted native binding setup. Its evidence is retained as
`geometry_only_uninitialized_texture_rejected.json`; it earns no textured-render
clearance. The original movie update parent was then traced: it calls the actual
slot loader and allocation callbacks. The corrected source-derived fixtures use
that loader, require nonzero texture allocation keys and reject format zero.
Their independent format, exponent and UV checks all pass.

## Explicit remaining scope

The mapped register region is an observed sink, not a GPU emulator. Texture and
palette jobs are queued but not uploaded in these fixtures. No final framebuffer,
palette-bank concurrency/recycling, projection setup, contextual mask clipping,
alpha blending or actual ending/Gallery playback is certified. A fresh independent
binding for each texture does not prove a simultaneous multi-texture scene.

The raw root `/m02_03.fls` has no observed active pose in the tested original
timeline path, so it is not forced into a fabricated binding. Its intended
consumer, raw loading and final rendering remain open; no global-unused claim
is made. All 11 legacy gates, all 18 plaque/hint entries, occupied Armor/Weapon,
alternate conditions and broader gameplay contexts remain open. Low resolution
Online images remain excluded by the user.

The full graphics goal remains active. Revisit older record-based checks at its
actual completion. These are controlled native binding fixtures, not a complete
playthrough or physical-device test.

## Reproducible evidence

- `scripts/research_fls_submission_v323.py`: bounded native update/draw discovery.
- `scripts/verify_fls_bindings_v323.py --all`: all 520 fresh binding fixtures.
- `scripts/record_fls_bindings_v323.py`: independent metadata/UV checks and audit update.
- `work/analysis/fls_submission_v323/all_bindings_proof.json` and `binding_summary.json`.
- Source pose proof: `work/analysis/fls_frames_v312/all_files_proof.json`.

Both graphics audits, the requirements ledger and progress documents record the
new evidence while retaining open final-rendering obligations. Focused Ruff passes.
