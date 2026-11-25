# V503 current M28 caption and progressive-name coverage

V502 remains the current experimental combined candidate, SHA-256
`f26a930d91f0df2089a080f0945b9f06a3d1f9718f18a39a6e6dca7edc8842bc`.
No production ROM, patch, script, progression or graphics data changed.

## Test and results

A source-locked research ROM substitutes exact current M28 bytes into M20's file
slot. Every other file and component is byte-identical to V502. The DeSmuME run
cold boots without a savestate or unlock modification; ordinary inputs end at2200.
It runs9000 frames, captures every120 frames and every frame3540-3700.

- Main title texture4: all4941 ink/shadow pixels match at the original visible origin.
- Gold Rota Nova texture5: all3437 ink/shadow pixels match.
- Progressive name textures27-46: all19 distinct source-pixel states appear in
  order, with complete leading/internal/trailing ink and shadows at(12,167).
- Textures30 and31 have identical rendered pixels; they form one equivalence class.
- The final Hodram Joakim Bergstrom state matches all3047 pixels from3667 onward.
- All nonzero name pixels remain inside the256x192 visible screen.

| Source texture image | First complete distinct state | Last sampled state |
| --- | --- | --- |
| 27 |3591|3594|
| 28 |3595|3598|
| 29 |3599|3602|
| 30/31 |3603|3610|
| 32 |3611|3614|
| 33 |3615|3618|
| 34 |3619|3622|
| 35 |3623|3626|
| 36 |3627|3630|
| 37 |3631|3634|
| 38 |3635|3638|
| 39 |3639|3642|
| 40 |3643|3646|
| 41 |3647|3650|
| 42 |3651|3654|
| 43 |3655|3658|
| 44 |3659|3662|
| 45 |3663|3666|
| 46 |3667|3700|

## Stronger check than the historical prefix comparison

A completed name includes pixels from all its earlier prefixes. The older V337
comparison could therefore credit a prefix from a later full-name frame. V503
credits only the largest completely matching distinct image at each frame, then
requires all19 distinct states in their original order. This demonstrates the
visible reveal sequence instead of merely finding every prefix inside a final name.

Pixel matches do not identify the native bound texture index where images are
equivalent. Textures30/31 remain indistinguishable by pixels. This is not a direct
GPU binding trace, normal ending invocation, legitimate unlock, full-route test,
complete transition/transparent-background proof or hardware verification.
Those remaining scopes are retained; the graphics goal is not complete.

## Evidence

- Preparation: `scripts/prepare_m28_planes_v503.py`.
- Verifier: `scripts/verify_m28_progressive_v503.py`.
- Fixture manifest: `work/analysis/m28_planes_v503/fixture_manifest.json`.
- Proof: `work/analysis/m28_planes_v503/progressive_proof.json`.
- Report: `work/emulation_v193/m28_planes_v503/capture_report.json`.
- Visual review: `work/analysis/m28_planes_v503/progressive_contact_sheet.png`.
- Selected native frames and the review sheet are saved under
  `E:\Rota Nova translations\Screenshots\Diagnostics\m28-v503`.

ROM/report/PNG hashes, complete dense interval, original input schedule, matching
glyph/shadow colors and chronological state order pass. Both scripts pass Ruff.
All22 historical requirements and all18 incomplete plaques remain in the audit.
At actual goal completion, revisit older record-based checks.
