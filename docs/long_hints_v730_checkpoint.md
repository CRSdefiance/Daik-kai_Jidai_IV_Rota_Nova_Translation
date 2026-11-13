# V730: current combined-ROM long equipment hints

The previous turn made progress through V729's original image-mode selector
proof and audit update. This batch adds a targeted current V712 integration
check. Earlier V536 and V581 five-long-hint results remain historical evidence;
this is not presented as the first verification of these names.

## Actual current run

One terminal 15,600-frame DeSmuME cold boot uses V712 and a byte-verified test
copy of the Maria Nagasaki save. The original save, test-copy source, ROM,
manifest, patch, release registry and canonical baseline remain unchanged.
No savestate is loaded.

At frame 3000, the original inventory-transfer helper adds five declared test
items. Its exact-current-ARM allowlist is extended only within this process,
after checking the transfer/getter/history code against an already supported
build. The shared helper, harness and core files remain unchanged. The native
transfer replays exactly and changes only 11 validated inventory/history bytes.
Normal UI controls then equip all five items on Maria. This establishes display
testing, not normal item acquisition or eligibility.

## Verified output

| Item | Frame | Complete hint bounds, native pixels |
|---|---:|---|
| Red-Haired Pirate Sword | 15600 | (16,208)–(158,224) |
| Saladin's Silver Armor | 15400 | (64,208)–(200,224) |
| Alexander's Campaigns | 15200 | (94,208)–(224,224) |
| Self-Sharpening Plane | 15000 | (94,208)–(224,224) |
| Aristarchus Telescope | 14800 | (94,208)–(224,224) |

The current native getters classify all 218 item records and return the same
103 equipment names/widths as the V581 catalogue: 28 weapons, 26 armor items and
49 accessories. The five selected names still attain their category maxima.
This is catalogue evidence, not 103 new emulator displays.

All five complete occupied hints and three complete empty hints pass independent
font-cell and whole-paper comparisons, including first/final letters, blanks,
wood grain, bevels and borders. Their entire backing uses the exact 1,408-byte
current tile, independently reconstructed from the original donor coordinates
with the established V581 join. All hints fit within their original bounds.

The five 32×32 item icons pass all 5,120 pixels. Native owner getters confirm
all five belong to captain Maria, type 2/actor 3. Fifty whole current static
Sailor Info plaques pass across the five captured screens. Fifty complete
skill-label/observed-number rows and ten Healthy/Relaxed label masks also pass.
Observed numbers are not a new mechanics oracle. Natural condition changes,
every other actor/state, and normal acquisition are not established.

The actual telescope screen and the sheet containing one full current screen
plus all five enlarged actual hint crops were opened. No missing letter,
cropped paper edge, icon mismatch or new plaque defect was found in this scope.

## Audit and artifacts

The current composition scope leaves the active queue and carries forward as
verified evidence. Other original comic/control/village/legacy contexts and
final overall review remain open. The original 18 overall plaque/hint objects
stay incomplete under the user's audit instruction; their accepted material and
completed base/stat/long-hint subscopes are retained. The 22 historical
requirement objects remain exact. The full graphics goal stays active.

- Runner: `scripts/run_long_hints_v730.py`.
- Verifier: `scripts/verify_long_hints_v730.py`.
- Proof and review: `work/analysis/long_hints_v730/` on E via the analysis junction.
- Actual captures: `E:/Rota Nova translations/Generated/work/emulation_v193/long_hints_v730`.
- Checked archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V730 Current long equipment hints`.

These screenshots use a declared inventory fixture and are not guide or
publication-approved captures. No ROM rebuild, canonical promotion, commit or
push occurs. The four excluded low-resolution Online bodies and preserved brown
marks remain unchanged. Revisit older record-based checks after the graphics
goal is complete.
