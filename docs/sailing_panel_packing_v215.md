# Sailing packed-bank screen mapping V215

2026-10-07. Previous goal turn executed the native producer and reviewed complete
English layouts. This turn matches original packed output to the actual Search
Mode capture, including the heading and differing source row regions. **No ROM
changes; V211 remains current and the full goal is active.**

## Verified bank geometry

The original word-placement function `01FFB6A4` is consistent with consecutive
32×16 four-bit banks, each containing four-by-two 8×8 tiles. Native sample calls
confirm offsets 0,2,32,34,98,256,1856,1994 and 3968 for the inspected coordinate
pairs. A whole linear screenshot buffer is not interchangeable with this stream.

Foreground-mask comparisons independently use the actual captured Search panel.
Every foreground bit and blank cell matches in the eight regions below:

| Region | Source virtual X | Width×height | Native origin |
|---|---:|---|---|
| Heading | 0 | 192×16 | (56,2) |
| Body 0 | 192 | 192×16 | (8,32) |
| Body 1 | 384 | 240×16 | (8,48) |
| Body 2 | 672 | 192×16 | (8,64) |
| Body 3 | 864 | 240×16 | (8,80) |
| Body 4 | 1152 | 240×16 | (8,96) |
| Body 5 | 1440 | 240×16 | (8,112) |
| Body 6 | 1728 | 64×16 | (8,128) |

Total: **25,600 exact foreground/blank pixels**. The heading's Y offset is 2,
rather than 0. Treating the first and third body regions as 240 pixels instead
of their verified 192 introduces pixels from the next packed source region.
Those failed assumptions were corrected before encoding replacement graphics.

The last width covers the complete known source region, not the entire blank
viewport. This is an exact foreground/blank comparison; palette/shadow colors,
unmapped blank regions and every other mode are not silently included in its claim.

## Consequence for English production

The complete V214 English layouts remain reviewed prose/font previews. Their
uniform proposed canvas must be encoded through the actual sprite arrangement,
or a fully verified scoped replacement producer. Blindly copying the linear
bitmap or plain ASCII into the original producer would use the wrong contract.

Next work: confirm/reconstruct the Info and Declare War arrangement, produce
complete English under the original caller's buffer/ABI and display bounds,
then compile and cold-boot all three modes in a registered combined candidate.
No native-English or formatting gate is marked complete yet. All remaining
Online/name/raw/context/native/gameplay and final ROM/patch scope is preserved.

Verifier: `scripts/verify_sailing_panel_packing_v215.py` (Ruff passing).
Evidence: `work/analysis/sailing_panel_packing_v215/screen_mapping.json` and eight
complete matched mask PNGs. Native Japanese source capture and V214 producer
buffers are hash-pinned in that proof. No candidate promotion is implied.
