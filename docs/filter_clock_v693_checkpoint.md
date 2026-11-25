# V693: original cursor clocks and exact same-frame DMA composition

The previous goal turn made progress with V692's shared Captain caption repair.
This checkpoint closes the two specific cursor-timing observations retained by
that release. No ROM, patch, artwork, palette, script or release profile changes.
The current experimental candidate remains V692, SHA-256
`0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.

## Why the first captures were insufficient

V692 retained 87 changed highlight pixels at frame 9600 and 1446 non-caption
pixels at frame 10800. Both appearances occurred in original source captures,
but that did not explain their exact same-frame timing.

The first V693 observation records the original lower iterator at `020D32B8`,
its return at `020D3314` and actual SDK clock returns at `02000FA8`. All four
initial paints reproduce complete output, registers and CPSR. Each paint spans
about six emulated frames and starts at VCOUNT 198, after visible scanlines.
The screenshot can therefore still show the preceding completed paint.
Those initial captures and proofs are retained. A second capture range includes
the predecessor chain, using process-local configuration of the frozen runner
and observers; no shared producer source is edited.

## Exact clocks and complete original paints

There are eight recorded lower paints per ROM: V685 source and V692 current.
Every complete 98,304-byte output matches the actual function return. All bytes
are written, none are read before being written, and original return registers
and CPSR match. Across 16 cases this verifies 1,572,864 output bytes.

Every executed ARM/ITCM/overlay/copied-pool instruction matches its registered
ROM. The full clock helper and iterator remain clean-ROM identical. No graphics,
actor getter, crop, font, allocator or game logic call is bridged. The only
external inputs supplied to native replay are the 40 exact SDK tick returns
already observed during those same game calls.

The original clock helper uses unsigned `(tick-origin) % 0x88FA4 < 0x77DAF`.
All 40 complete native helper returns and ABI checks agree with that formula.
For the relevant completed paint before frame 9600, V685's two highlight
decisions are visible, whereas V692's are hidden. For the relevant paint before
10800, both versions compute visible highlights, but finish on different frames.
These are the original game's clock decisions, not a new localization effect.

## Switch rows derived from original DMA command state

The exact original DMA setup routine writes its control word at `01FF98D0`.
At its following PC `01FF98D4`, the observed arguments identify:

- DMA channel 3.
- Control `8000C000`: immediate 16-bit transfer of 49,152 words.
- Source `022E1794`, the complete original lower bitmap.
- Destination `06000000`, mapped to the lower display's bitmap bank.

The pinned core's `MMU.cpp` performs the complete immediate transfer before
scheduling the bus-stall duration. The source ROM's first observed issued lower
transfer is row 55 at frame 9600 and row 97 at frame 10800. These switch rows
come from the original PC and full arguments, independently of changed pixels.
V692's corresponding completed paints return in the preceding frame; neither
questioned visible frame contains a new lower transfer.

For each source frame, take rows before the independently observed switch from
the previous completed native paint, and later rows from the same-frame completed
native paint. For each current frame, use the already completed native paint.
All four predicted 98,304-byte bitmaps match all 192 actual before-RenderLine
rows exactly. Original display mode, bitmap bank, affine identity, row origin,
zero blend and zero brightness are checked per row. Conversion predicts every
one of the 196,608 same-frame lower-screen RGB pixels exactly.

No pixels are excluded, no screenshot is delayed or substituted, and no switch
row is fitted to lettering or disagreement. Four explicit wrong-phase controls
produce different output, demonstrating why a single final-paint comparison
would be insufficient. The original before/after caption text remains different
where expected; the source control still displays Japanese 艦長.

## Observer integrity and actual visual review

Four complete 15,200-frame cold boots retain the V692 input/donor contracts.
All 152 comparable whole screenshots and four complete terminal RAM states match
their respective unobserved same-ROM baselines exactly. No savestate, code/RAM/
location fixture or original donor modification is used. Clock observers only
copy game state. Native host slot/prologue detours are restored; the core DLL
file remains exact. Fifteen host-prefix controls, eight bounded mirror controls
and twelve scanline-prologue controls pass. The three host RenderLine entries
are bound to the original VCOUNT-driven HBlank calls.

The source/current actual-and-predicted lower-screen sheet was opened and
reviewed. Complete portrait borders, sprites, popup lettering and highlight
changes match. The 87/1446 observations are explained by original clocks and
bitmap-transfer timing; no graphics repair is warranted for those two cases.
This closes that specific V692 timing gap, not all animation/device timing.

## Remaining scope and storage

The second gender-icon consumer, its embedded copy, six small control contexts,
eight white village-card contexts, comic/legacy/standalone artwork, approximate
restoration review, older record-based checks and final acceptance remain open.
All 18 original plaque/hint entries remain incomplete. All 22 historical
requirement objects and every prior audit key remain exact. The user’s Online
exclusions and brown-mark preservation decision remain in force.

Analysis: `work/analysis/filter_clock_v693`, including `predecessors`.
Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V693 Original
cursor clocks and DMA`. Large capture files already on E have individually
checked references in the archive. These observer/duty-test pictures are not
guide-approved. Current V692 ROM/manifest/patch/registry/canonical/historical
pointers remain unchanged. No commit, push or canonical promotion is made.
The full graphics goal remains active; this checkpoint is progress.
