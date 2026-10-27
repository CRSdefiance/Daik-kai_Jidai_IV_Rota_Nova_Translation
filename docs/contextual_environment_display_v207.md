# Retained facility signs: native display V207

2026-10-07. V205 remains the registered combined candidate. This work adds
display evidence for retained contextual artwork; it does not change release bytes.

## Evidence

A fresh cold boot renders the unchanged Tavern lantern (`/_pxl/kbj04.pxl`,
40×44) and Inn plaque (`/_pxl/kbj08.pxl`, 50×44) through the original native
views, cache and GPU. All 923 and 1,248 source pixels outside transparent index
255 match native five-bit color, including painted signs and opaque edges.
All visible pixels lie within the bottom 256×192 viewport. Transparent backdrop
pixels are excluded explicitly, rather than claimed to be opaque source matches.

A second fresh cold boot reaches the same town and uses ordinary D-pad input
to select both facilities. Complete original-font masks match every foreground
and blank cell, including first and last letters:

| Caption | Captured frame | Mask bounds, exclusive right/bottom | Exact ink pixels |
|---|---:|---|---:|
| Tavern | 15400 | (64,244)–(100,255) | 72 |
| Inn | 15550 | (64,264)–(82,275) | 35 |

Both labels and the entire native town fixture were visually reviewed. The
contact sheet records navigation through several other facilities as context;
only the two masks above receive complete glyph assertions here.

## Fixture scope

`work/analysis/environment_live_fixture_v207/fixture_manifest.json` pins V205
as source and a research ROM SHA-256 of
`31becdf4873a422beb23f93da8e45f70357710163d43c379ae0afeccd225b891`.
Only ARM9 words at B7CA8 and B7D6C force the alternate image/hit-bound selection.
All files, ARM7 and other ARM9 bytes remain exact. No savestate or emulator-memory
injection is used. This ROM is research only and must not be handed off.

Lisbon is the host for this fixture, not a claimed ordinary city for these icons.
The separate caption-anchor selector at B8020 still uses the original Lisbon
field. These captures prove complete displayed sprites and English label bounds
in this fixture; normal alternate-city caption anchor positions and city assignment
remain unproved. Four retained town backgrounds still require display evidence.

Keep both physical signs unchanged, supported by independent English facility
labels and the V206 source/consumer review. Do not invent a proper inn name from
the indistinct plaque. Full graphics completion remains open, including four
Online screenshot bodies, archive classification, naming consistency, remaining
native/gameplay checks and the final registered combined ROM/patch.

Verifier: `scripts/verify_environment_live_fixture_v207.py`.
Proof: `work/analysis/environment_live_fixture_v207/native_sign_pixel_proof.json`.
Capture reports and input schedules are saved beside the research artifacts.
