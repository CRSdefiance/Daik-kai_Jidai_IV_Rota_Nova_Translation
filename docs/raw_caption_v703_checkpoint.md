# V703: accepted raw16 caption and matched opacity control

## Question and result

The previous goal turn made progress through V702's complete standalone-art tile
coverage. V587's event-still experiment rejected raw16 metadata before drawing.
It therefore could not establish a display-alpha requirement. V703 uses the
compatible generic cache/image widget instead,with matching source and opacity
controls that both actually load and draw.

The original English caption RGB data are intact. With their stored high bits
clear,the supplied raw16 widget produces a black rectangle. Setting only bit15 in
a research control makes the same RGB data display correctly,including the complete
“Huh?!” caption. This is a verified contract for this supplied widget and display
mode,**not** a discovered defect in the comic's normal scene or authority to change
the production archive's alpha bits.

## Exact diagnostic inputs

The preparer extracts frame6 rectangle `[40,96,112,128]` from current SLACKIMG block19.
It contains72x32 =2,304 BGR555 words. All stored high bits are clear. The research
descriptor `[16,72,32,20,20]` is supplied metadata,not an original comic descriptor.

Two research-only ROMs put this descriptor/crop into the existing kakutei file slot:

- `source`: all crop bytes preserved exactly.
- `opaque_CONTROL`: each word ORed with8000; every low15 RGB bit remains exact.

Only that borrowed slot's data change. ARM9,ARM7,all other file data and IDs,overlay
tables and banner stay exact to production. Both copies retain the entire original
current GRP archive. The crop excludes the ambiguous brown marks; neither research
copy changes them. Their4,320 source bytes retain SHA256
`3b0111f01e8f7a0857a723f28138d130e29caad046aa5d15f7367831ac1d6943`.

These are private research ROMs on E:,explicitly labelled not playable releases.
The game reads `_pxl/kakutei.pxl` through its real SDK/cache path. This test does
not make the game call the original GRP archive wrapper or discover a comic trigger.

## Actual loading,copy and GPU evidence

Three terminal6,800-frame cold boots use the same unchanged prepared donor and
inputs:raw source,opacity control and normal production baseline. Four48x28-or-
smaller source tiles cover every caption pixel exactly once without resizing.

Both research owners begin uncached. Their original SDK Open requests and complete
4,628-byte loaded files are recorded. All eight original copy entries carry the
correct raw16 header,source rectangles and destination. No format rejection,
palette conversion,SDK bridge or decoded-pixel injection occurs in the game.

Every held tile's actual software bitmap word equals its exact source/control
word. At6080,read-only native exports independently bind the same data to physical
VRAM bankC. The complete671,744-byte LCDM regions differ between source/control
only at the1,344 first-tile high-byte positions,and each difference is exactly80.
All low15 RGB bits remain equal.

The two native states have byte-identical I/O,palettes and OAM. Captured registers
bind an identity-transformed BG3 direct bitmap,bankC mapping,no colour blend or
master brightness,and a black backdrop. Sub-engine sprites are off the tested
rectangle. The retained exact-core source `GPU.cpp`'s `rot_BMP_map` computes its
pixel index from `outColor & 8000`:clear means transparent,set means visible.

Thus the black source result follows from accepted/copied data and this bitmap's
alpha gate. It is not evidence of a failed read,missing leading letters or an
English-font corruption. The opaque control reconstructs all2,304 original RGB
pixels exactly at native five-bit precision. Eight complete upper-screen models
(393,216 pixels) match the captured backdrop/source semantics;lower screens match
complete version-bound native cursor states,and all four source/control lower
pairs are whole-RGB exact.

## Fixture and state safeguards

Only the declared source-view words and temporary CPU R3 argument change. Full
before/after4 MiB RAM guards verify every install,tile change and restore;CPU/TCM
remain unchanged at each view-data write. Original inputs restore before normal
exit. All30 pre-fixture and six restored whole-RGB pairs match the production
baseline. Fifteen native host-prefix/ABI and eight bounded-read controls pass.
All hooks restore and the core file remains exact.

Native state exports are read-only and never loaded. Their exporter validates
serialized WRAM against its same-frame direct main-RAM read. The initial verifier
mistook WRAX,which the exporter labels extra RAM,for WRAM. That rejected verifier
and failure note are retained. The final verifier respects the documented regions
and exporter guards;no main-RAM divergence or production defect was inferred.

## Visual review and next work

Both the raw/control/baseline full-screen sheet and the RGB/control tile-composite
sheet were opened. The control's first/final caption characters,bubble edge and
adjacent crop pixels remain complete. The composite is labelled a research opacity
control,not a production fix or one ordinary game frame. No guide promotion.

This establishes why simply handing these legacy RGB555 words to this native
direct-bitmap widget is unsuitable without an opacity/import contract. The next
consumer investigation must bind the original raw viewer/descriptor/import stage,
including any RGB555-to-display conversion. Do not repeat the rejected indexed8
event-canvas test or globally set high bits from this experiment.

The original comic parent,normal geometry,full-page composition,all other caption
scene displays and concealed-background restoration review remain open. V680's
complete connected native archive/scaling results remain separate valid evidence.

## Evidence and unchanged release

- Analysis: `work/analysis/raw_caption_v703/`.
- Captures: `E:/Rota Nova translations/Generated/work/emulation_v193/raw_caption_v703_*`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V703 Raw caption display contract`.
- Scripts: prepare/run/verify/record/archive verification with suffix `v703`.

Production V692 remains SHA256
`0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.
Production ROM,art,archive,patch,manifest,registry,donor,canonical baseline and
release pointers stay unchanged. No new production candidate,commit or push.
All18 original plaque/hint entries stay incomplete,all22 historical requirement
objects stay exact,and the full graphics goal remains active.
