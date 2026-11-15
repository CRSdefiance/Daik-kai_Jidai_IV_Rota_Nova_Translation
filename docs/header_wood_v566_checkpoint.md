# V565–V566: Distributed Goods and Spoils wood restoration

## Source review and correction

The original headers read 配布品 (“Distributed Goods”) and 戦利品 (“Spoils”).
Both existing English headings are faithful and remain unchanged. The source
comparison found the same white-only erasure failure as Temporary Storage:
Japanese shadows and dark replacement samples remained behind the English.

| Header | Source white points | Reviewed shadow points | Uncovered retained shadows | Changed pixels | English ink retained | Visible source material retained |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Distributed Goods | 149 | 124 | 97 | 211 | 243 | 3,623 |
| Spoils | 144 | 125 | 106 | 201 | 98 | 3,770 |

Distributed Goods uses shadow indices0/1/4; Spoils uses0/1. Shadows are mapped
within two pixels of original white strokes, inside the lettering region and
away from the outer frame. This conservative proximity mask is a review rule,
not proof of the original font producer's complete shadow algorithm. Blank source
donors contain none of those shadow indices. Each connected component receives a
coherent source patch selected against visible neighbouring grain. Hidden grain
is inferred, not recovered exactly. Original visible material outside that mask,
complete English masks, palettes, dimensions and borders remain exact.

Visual review removes the conspicuous black Japanese shapes behind both English
headings. The previous V564 Temporary Storage result remains byte-reproducible
after extending the helper. The separate blue Confirm button was inspected as
source/current artwork; its own material and native-consumer review remain open.
Marker controls remain in the broader audit.

Each original packed header payload occurs once in the clean ROM. This rules out
an additional exact raw payload copy under that search; it does not prove absence
of differently encoded or compressed copies.

## Original source ownership and crops

Original resource initialization maps Distributed Goods to owner023139E8 and
Spoils to owner02313A4C. The original header selector at0208529C reads
object+0x10: mode2 constructs Distributed Goods at02085314, mode3 constructs
Spoils at02085344. Both use source [0,0,256,16], preserving the complete lettering.
This selector/crop code is byte-identical from clean ROM to V566. Actual reward
or battle event reachability is not proved by those static constructors.

The existing ordinary V564 Cargo Setup capture also resolves original Temporary
Storage view021914B8/owner02313C7C through routine020D4170 to resident0236CDB0,
which is byte-identical to V564's corrected `tempcargo.pxl`. These original-owner
and code leads are saved in `resource_reference_evidence.json` for follow-up.

## Combined candidate and verification

- Profile: `all-routes-unified-v566`, experimental, with all 470 inherited batches
  and 114 accepted layers; canonical parent unchanged.
- Base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Candidate: `out/all_routes_combined_v566_candidate.nds`, SHA256
  `5203bd6717a5898cfdcdc200748733a5b677568bfb001614da965b99a312afb3`.
- Clean-ROM patch: `out/all_routes_combined_v566_candidate.xdelta`, SHA256
  `6c0cb070df1b0cb2c5013f2487b80184a19d39db0a5a2f453f493f0af6fb3c31`.
- Patch source: `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

Only `/_pxl/haifuhin.pxl` and `/_pxl/senrihin.pxl` change from V564. Every code
component and other internal file is byte-identical. The manifest registers the
two source-locked repairs. Applying the patch to the exact clean ROM reconstructs
V566 byte-for-byte.

Four research ROMs substitute each control/corrected header into the actual
Temporary Storage renderer. Each fixture changes only `tempcargo.pxl` from its
parent. Complete paired frame comparisons at4300/4600 pass 393,216 screen pixels
and all 16,384 banner pixels, including both complete English masks and original
palette colors. This demonstrates full-width rendering compatibility; it is not
credited as native loading/display in the original reward or battle events.
The copied source save remains unchanged; no savestate is used.

A separate ordinary V566 New Game cold boot passes all 56 unique startup captures
against V564, including the established title, selection, opening story and town
schedule. Ruff passes. This is targeted emulator evidence, not a full playthrough
or physical-device verification.

## Evidence and remaining scope

Implementation: `dk4tool/patch/cargo_banner_texture.py`,
`translations/header_wood_textures_v1.json`, registered integrated builder stage.
Verifier/fixture preparation: `scripts/verify_header_wood_v566.py`.
Proof/review: `work/analysis/header_materials_v565/v566_release_proof.json` and
`wood_header_repair_review.png`.

Captures are on E under `Generated/work/emulation_v193/header_wood_v566_*`.
Four copied screenshots and provenance are under
`Screenshots/Test fixtures/V566 Wooden headers`, explicitly labeled source
substitutions rather than guide candidates. No synthetic image is approved for
guide publication.

Original event contexts, other control families and all 18 original plaque/hint
entries remain open. All 22 historical requirements retain their full scope.
The graphics goal remains active; this checkpoint does not close the global
texture audit or promote the experimental ROM.

## V567: original wooden-header consumers

Original Distributed Goods/Spoils resource owners and full crops now pass eight
actual emulator cases under a one-word header-choice test cheat. Every resident
PXL matches its named ROM file, and all 32,768 banner pixels plus 786,432 complete
screen pixels match independent controls. No resource-file substitution occurs.
Ordinary reward/battle event coverage remains unverified; the underlying test
scene stays Cargo Setup. Production V566 is unchanged. All 18 plaques remain
incomplete and all 22 historical requirements retain full scope. See
[V567 native-consumer evidence](header_consumers_v567_checkpoint.md).
