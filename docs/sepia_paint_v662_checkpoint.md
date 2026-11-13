# V662: complete controlled native sepia-map painting

## Result

All64 page/palette combinations of the original `/_pxl/seamap.pxl` pass the
complete native loader, cache, view and software-painting test on current V653.
All3,145,728 destination words match an independent source-index/palette model,
including every edge and the surrounding screen. There are56 unique paintings
because the eight stored palette banks include duplicate colors.

This advances V256's loading/view proof to complete native painting. Page, bank,
destination and screen selector are explicit controlled inputs. It does not
identify a gameplay caller, display this atlas in an emulator, establish GPU or
physical-device behavior, or display the separate legacy CMMNIMG maps.

## Original loading and painting

Original resource registration `0210E190` initializes owner `02313B8C` with its
actual sepia filename. Original cache setup and image resolution load all156,436
file bytes through an explicitly disclosed SDK filesystem bridge. The bridge
supplies only open/read/seek/close against the exact current ROM file; no getter,
image header or painter is substituted. The completed test needs one file open,
one full read and one close. Every later view resolves through the hot cache.

All64 guarded native views preserve owner, source origin, 244x160 extent and the
supplied palette-bank ID. Native software painter `01FF92D8` receives original
source headers and normal source/destination operands. Screen selector0 targets
the original 256x192 software plane `022E1794`, placing each complete page at6,16.
All stack/saved-register return checks and adjacent canaries pass. Every executed
instruction is exact to the original ARM9/overlay code.

All2,498,560 source pixels are opaque under their actual palette words. Writes
are confined to the declared rectangle, all expected destination bytes are
written, and the painter never reads completed output as source. All647,168
surrounding background pixels remain exact across64 cases.

## Palette alpha and rejected contracts

The actual source flags word is4. Original instructions `01FF948C` and
`01FF9498` test palette bit15 before storing complete16-bit palette words. They
do not discard color index0. Source index0 occurs in five of the eight pages:
40 page/bank cases contain30,200 opaque index0 pixels altogether. A generic
index-zero transparency model loses these pixels and is explicitly rejected.
The other24 cases have no source index0 and get no credit for that negative.

One separate isolated control clears only bit15 of copied palette0, paints the
selected page and verifies that those source cells retain the known background.
All49,152 words and native write coverage pass, then the loaded source file is
restored byte-exact. This temporary analysis-memory change is not shipped art.

The first experiment incorrectly supplied a destination header where the
original dispatcher accepts a screen selector. Its first mismatch report is
retained. Source disassembly establishes the original destination calculation;
the corrected test never redirects the native painter. The initial assumption
that every page contains index0 was also rejected using the full source counts.

## Source review and unresolved use

All eight bank0 outputs were inspected at native size. They retain the original
unlabeled cartographic paintings, with no newly identified Japanese caption to
translate. Existing source-content retention decisions remain unchanged.

The ordinary map pages previously tested in V641 use the separate blue
`seaarea.pxl`. A bounded aligned-literal search finds the sepia owner in resource
registration, not a newly established screen. It does not exclude computed,
indirect or other file-ID consumers. The nearby resource table is not evidence
that the ordinary map viewer selects the sepia atlas. Actual sepia and legacy
map consumers remain open; no global unused-data claim follows.

## Evidence and remaining goal

- Verify: `python scripts/verify_sepia_paint_v662.py`.
- Native proof: `work/analysis/sepia_consumers_v662/native_paint_proof.json`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V662 Sepia native painting`.
- Eight PNGs are controlled native-render outputs, not gameplay screenshots or
  guide candidates.

V653, patch, manifest, registry, canonical parent and release pointers stay
unchanged. All18 original plaque/hint entries remain incomplete and all22
historical scope objects remain exact. Other control/card/legacy/material,
equipment, gameplay, older record checks and final acceptance gates remain open.
The complete graphics goal remains active. No new ROM, commit or push is made.
