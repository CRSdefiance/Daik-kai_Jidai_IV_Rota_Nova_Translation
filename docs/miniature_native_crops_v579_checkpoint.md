# V579: five complete miniature captions through native rendering

The previous turn added current ending playback and historical credit/pan
verification. This turn completes controlled native loading, crop, palette and
lettering checks for Done, Rank, Cancel, Pick Cargo and Pick Ship. Their ordinary
callers remain unresolved. Production remains experimental V573, SHA256
`f987f1c56ba5641544e5c84698c59351e39465b15001601adddf697698d89a77`.
No playable ROM, patch, source artwork, registered layer or canonical parent changes.

## Four explicit research fixtures

All five cells fit in the original frame-atlas rectangle [184,32,256,56], size 72x24.
The established Cargo Setup crop fixture selects this real resource through owner
02313F60. Ten documented setup/literal words change in each research ARM9, retaining
the original drawing/cache routines. The actual fixtures retain every byte of the
production frame atlas and all other art.

Each of two original palette banks has an actual fixture and a blank control.
In blank controls only, the 307 foreground indices inside the five declared cells
are replaced by index 0 in the loose frame atlas. Its original header, all 83 banks,
extent and every other index remain exact. The embedded archive remains production
data. These explicit negative controls are research artifacts, outside the patch.

The four ROMs have RESEARCH_ONLY filenames and reside on E through work/analysis.
Each cold boots for 4,600 frames with identical ordinary controller inputs and an
isolated copy of the existing Syracuse test save. All four processes finalize
normally. No savestate or additional inventory/location/condition fixture is used.
The original save remains SHA256
`958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb`.

This deliberately changes the source crop in Cargo Setup. It does not identify
the ordinary place or function of any of the five caption graphics.

## Complete native loading and pixels

At frames 4,300 and 4,600 in all four runs, captured RAM contains the expected 72x24
view, original frame owner, selected palette bank and zero flags. The original
getter 020D4170 resolves a whole resident PXL byte-identical to that fixture's named
file. Its registered filename is `_pxl/__frame.pxl`. Eight source/cache/view cases
pass without substituting a fabricated resident header or image.

Independent compact-font masks match the current source cells. Their full first
and final glyphs and word gaps are included. All 20 native appearances pass:

| Caption | Complete ink per appearance | Source meaning |
| --- | --- | --- |
| Done | 43 | 終了, finish/end |
| Rank | 49 | 等級, grade/rank |
| Cancel | 55 | キャンセル, cancel |
| Pick Cargo | 84 | 積み荷選択, select cargo |
| Pick Ship | 76 | 船選択, select a ship |

The existing words remain reasonable general English. Context-dependent choices,
such as Done versus Exit for 終了, await the ordinary consumer; no new semantic
change or final context approval is inferred from this supplied crop.

All 1,228 foreground points and 5,120 full-cell ink/background points pass. The complete
72x24 source region appears at native destination [0,261,72,285]. The rightmost
source cell reaches x256 without losing its final strokes. Both captured states
retain all five words.

Every actual/blank pair differs at exactly the 307 declared glyph positions.
All 393,216 paired full-screen pixel positions match the expected composition,
including all pixels outside the crop. The blank controls reject every complete
caption mask. Both bank appearances were visually reviewed at native resolution.

## Original palette behavior

Bank 0 uses original foreground 0xA16D, RGB5 (13,11,8). Its index 0 is opaque 0x8800,
RGB5 (0,0,2). All blank cell pixels match that source color exactly.

Bank 9 uses original white foreground 0xFFFF, RGB5 (31,31,31). Its index 0 is transparent
0x0000. Non-ink cell pixels match the blank-control background. This preserves the
original material/opacity behavior; a black-background assumption is not imposed.
Across the two banks, all pixels outside the 72x24 native crop remain exact at both
captured frames. The tests establish these two palette uses; they do not claim
native display in every one of the83 stored banks.

## Saved evidence and reproduction

- Generator: `scripts/prepare_miniature_crops_v579.py`.
- Verifier: `scripts/verify_miniature_crops_v579.py`.
- Both pass targeted Ruff.
- `work/analysis/miniature_crops_v579/fixture_manifest.json` records all four ROM
  hashes, exact ten-word changes, the 307 control indices and source-save identity.
- `native_five_caption_proof.json` in the same directory records eight real
  cache/view cases, 20 complete caption appearances, paired/cross-bank comparisons
  and capture hashes. `inputs.json` records the exact shared controller schedule.
- Raw reports/PNGs/RAM: E:/Rota Nova translations/Generated/work/emulation_v193/
  miniature_crops_v579_bank0_actual, bank0_blank, bank9_actual and bank9_blank
  (each directory has the miniature_crops_v579_ prefix).
- Eight full screenshots and four native 72x24 crops, with reports and hashed
  provenance: E:/Rota Nova translations/Screenshots/Test fixtures/V579 Miniature crops.

For each generated research ROM, run `headless_desmume_v193.py` in a fresh output
directory with `--frames 4600 --inputs-json work/analysis/miniature_crops_v579/inputs.json
--capture-every 4600 --capture-at 4300 4600 --dump-capture-ram`, plus the named source
save via `--battery-save`. The verifier deliberately names the recorded directories;
inspect new provenance before changing those bindings.

No fixture is a playable release or an ordinary guide screenshot. No guide
publication is approved. Production V573 and its existing exact patch remain
unchanged. The five normal callers and Confirm parent remain open, alongside the
broader material/artwork audit. All 18 original plaque entries remain incomplete
and all 22 historical objects retain their exact scope. The graphics goal remains
active; revisit older record-based checks at actual full completion.
