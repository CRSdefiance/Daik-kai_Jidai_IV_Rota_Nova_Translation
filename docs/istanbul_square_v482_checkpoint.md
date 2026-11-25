# V482 genuine Istanbul Square coverage

V474 remains unchanged, SHA-256
`1d513b81762499f0fd6a2edeeabb182a69c334756fc9261f70c07a0110984b9e`.
The genuine Istanbul battery save is copied into a fresh emulator folder and
loaded through normal controls. No inventory fixture, savestate, unlock or ROM
modification is used. The original donor hash remains intact.

## Actual city/category verification

The Square has four signs, rather than Amsterdam's three:

| Original category | Current visible sign | Interpretation |
| --- | --- | --- |
| 珍味 | Delic. Shop | Delicacies; current label is abbreviated. |
| 酒類 | Liquor Shop | Alcoholic beverages. |
| 宝石 | Gems Shop | Gemstones. |
| 繊維 | Fiber Shop | Fibers and textiles. |

Original native category getters confirm all four Japanese terms. Actual
frames4500/4600/4700/4800 select each corresponding sign. Every foreground glyph
and blank cell in all four captions matches, including first/final characters.
The original focus padding, complete right-side fill and neighboring frame edge
match. Whole-screen differences between the four captures occur only within the
shop selection area. All four shops activate normally, at frames4900/5200/5600/5900.

Frames5200/5600/5900 show complete COMMON658 dialogue. Both lines start at x22,
y296/312; the complete sentence and blank cells match the native font. Existing
wording remains subject to the requested later record/prose review.

The initial Trends choice temporarily covers the third row. A dismisses that
choice and restores all four visible signs. This is ordinary contextual overlay
behavior, not evidence of missing caption glyphs.

## Full-wording layout investigation

The abbreviation Delic. is not treated as final wording approval. A trial with
Delicacy Shop in the 64-pixel unwrapped caption canvas loses final-letter ink,
despite its visible ink nominally fitting. Full-word lettering therefore needs
a source-backed layout change and actual capture before integration. No failed
trial wording is shipped. The 16-pixel dialogue wrapper is not the Square's
12-pixel unwrapped caption contract; comparing those contexts gave an unrelated
wrap result and is not evidence of a current Square defect.

Reproducible trial: `scripts/probe_square_wording_v482.py`, proof
`work/analysis/istanbul_square_v482/wording_trial.json`. It executes the current
Square paint hook, confirms existing captions, and records exactly eleven missing
ink pixels for the proposed Delicacy Shop expansion. Textile Shop fits that
contract, but no replacement wording is integrated or credited as a GPU capture.

## Artifacts and remaining work

Verifier: `scripts/verify_istanbul_square_v482.py`.
Proof: `work/analysis/istanbul_square_v482/square_proof.json`.
Capture: `work/emulation_v193/istanbul_square_v482/capture_report.json`.
Verified sign and dialogue images are archived in the guide and copied to E.

This extends actual city/category coverage; other categories/cities, full-wording
layout, older prose, regional/legacy/Gallery/ending contexts remain open. All22
historical requirements and all18 incomplete plaque entries are retained.
No canonical promotion, full-playthrough or hardware claim. The graphics goal is
still active. Revisit older record-based checks at actual goal completion.
