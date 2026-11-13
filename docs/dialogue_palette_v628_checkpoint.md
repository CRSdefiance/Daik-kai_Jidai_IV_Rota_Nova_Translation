# V628: source palette resolves the capital-I comparison discrepancy

## Result

The four CP932 capital-I comparison findings retained in V626/V627 are resolved.
Every foreground and shadow pixel in all fourteen source-bound Tavern dialogue
planes matches the existing emulator captures. The 45 previously differing
pixels are the original gray shadows, not missing black letter strokes.

**This checkpoint changes verification and documentation only.** No ROM, patch,
translation, original artwork, release profile or historical verifier is changed.
The latest compiled candidate remains experimental V627:

- `E:/Rota Nova translations/Generated/out/all_routes_combined_v627_candidate.nds`
- SHA256 `0a03862a0a0a75c748e2f806016d2316f881eb9799907590715c41d251bf2a09`
- Profile `all-routes-unified-v627`

## Cause and source evidence

The historical V257 controlled raster creates a text context with foreground
index1. For CP932 glyphs, the original shadow selector020D1964 returns index15.
The V626 comparison treated every nonzero raster index as black foreground.

The original dialog setup020548A8 instead overwrites its context color with15:
020548C8 is `mov r2,#15`, and020548D4 stores it atcontext+0x30
(`sp+0x34`, with contextat`sp+4`). The same original shadow selector returns14
forforeground15. At source palette02125A20, index15 is0x8020 (black-green
RGB0,8,0 in these captures), while index14 is0xE318 (grayRGB197,198,197).
The native CP932 painter therefore produces a gray shadow beside the black I.

The new verifier checks the dialog color setup, ASCII/shadow routines, CP932
painter and palette against the clean ROM, V626 and V627 byte for byte. Each
selected frame's resident RAM palette and complete KANJI.FNT also match the
source and current ROM. The fourteen dialogue templates and their native
formatted paragraphs are unchanged between V626 and V627.

## Complete checks

`scripts/verify_dialogue_palette_v628.py` calls the existing native formatters and
painters with sourceforeground15 and compares both complete228x80 ink planes
against fourteen existing GPU captures. It checks every blank cell for either
ink color and every painted pixel for its exact RGB565-expanded capture color.
There is no excluded-I column, tolerated pixel difference or replacement glyph.

The old foreground1 replay maps exactly to the corrected index15/14 replay.
Reapplying its old all-nonzero-is-black comparison reproduces precisely:

| Captured frame | Message | Gray shadow pixels falsely classified as missing black |
|---|---:|---:|
| 9600 | 979 | 18 |
| 10000 | 965 | 9 |
| 13600 | 921 | 9 |
| 14400 | 941 | 9 |

The other ten panels have zero such differences. First/final visible-glyph
erasure controls fail the complete masks in every panel. Erasing the CP932
shadow or painting it black also fails in each affected panel. Native return
pointers, source strings, PXL/view guards and saved-register/stack checks pass.
Targeted Ruff checks pass.

## Provenance and limits

Primary proof: `work/analysis/dialogue_palette_v628/palette_proof.json`.
Evidence archive:
`E:/Rota Nova translations/Screenshots/Test fixtures/V628 Source dialogue palette`.
The archive includes fourteen unmodified full screenshots, separately labeled
actual crops, source-palette replay previews, the original capture report and
hash-bound verifier/proof files. Replay previews use a plain background and are
not screenshots or replacements for the original artwork.

These are rechecked V626 cold-boot captures from the24801-frame Tavern scheme
test, not a new emulator run. That run used the previously disclosed Strategist
room/XP/calendar fixture atframe3200; it is not an ordinary earned progression
claim. The replay retains the earlier controlled16px line pitch, now checked
against all fourteen actual text planes. It does not claim that a live text
context was exported during each draw. Background artwork and button pixels
are not compared by these text-ink checks.

The V627 ROM, patch and canonical baseline hashes remain unchanged. The V627
921-asset/57-embedded-region preservation and exact patch reconstruction proofs
are retained, not relabeled as newly executed tests.

All18 original plaque audit entries remain incomplete, and all22 historical
requirement objects retain their original scope. Confirm, five miniatures,
eight village cards, legacy/comic/logo/movie/material and broader gameplay
requirements remain open. The four low-resolution Online image exemptions and
preserved brown marks remain in force. No canonical promotion, full playthrough,
hardware verification or graphics-goal completion is claimed.

## Reproduce

From the repository with the bundled dependencies available:

```powershell
$env:PYTHONPATH='.;.deps'
$env:PYTHONIOENCODING='utf-8'
C:/Python314/python.exe scripts/verify_dialogue_palette_v628.py
.deps/bin/ruff.exe check scripts/verify_dialogue_palette_v628.py scripts/record_dialogue_palette_v628.py
```
