# Controlled movie GPU checks V336

Production V326 remains unchanged, SHA256
`fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1`.

## Test scope

Five disposable research ROMs replace only `/FLS/M20.fls` with the exact current
bytes of M28, M29, M30, M31 or M32. Each manifest records file and ROM hashes.
These fixtures use the Rafael opening path to exercise the original movie engine
and DeSmuME GPU. They do not establish normal ending triggers, legitimate unlocks,
route completion or the intended caller. They are not playable release candidates.

All five runs cold boot without savestates. Inputs end at frame 2200. M28 runs
11,000 frames; the other four run 12,500, capturing every 30 frames. All emulator
processes terminate normally. Captured PNG and report hashes are verified.

## Exact captured pixel results

The verifier compares colors at native 5-bit precision. M28 texture 46 matches
all 3,047 nontransparent name and shadow pixels at six frames, 3690 through 3840,
origin (12, 167). This includes the full **Hodram Joakim Bergstrom** lettering.

| Movie | Exact complete upper-screen matches | Pixels per match |
| --- | ---: | ---: |
| M29 | 234 | 49,152 |
| M30 | 167 | 49,152 |
| M31 | 142 | 49,152 |
| M32 | 155 | 49,152 |

These are selected opaque scene matches within frames 2400 through 10500.
The sampled M30 frame 6000 is not exact; other held frames match, starting at 4530.
This result does not assert that every frame, transition, alpha effect or viewport
is correct. Real ending navigation, Gallery unlocks, physical hardware and legacy
raw-art callers remain open.

## Audit status

Both graphics audits and requirement 6 retain the controlled-substitution scope.
All 18 plaque/hint entries, including Weapon and Armor variants, remain incomplete.
The user-exempt low-resolution Online24/27/31/33 graphics require no further
translation. Existing partial edits are retained. The full graphics goal remains
incomplete; revisit older record-based checks at actual completion.

Evidence: `work/analysis/movie_gpu_fixture_v336/GPU_pixel_proof.json`, the five
fixture manifests and `work/emulation_v193/movie_gpu_fixture_v336_m*/capture_report.json`.
Reproduce with `scripts/prepare_movie_gpu_fixture_v336.py`, the documented opening
input schedule and `scripts/verify_movie_gpu_fixtures_v336.py`.
