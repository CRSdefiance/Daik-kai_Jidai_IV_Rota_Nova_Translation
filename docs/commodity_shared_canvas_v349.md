# Commodity shared canvas V347–V349

Status: town specialty layout verified in research fixtures. Market/cargo layouts
and registered integration remain incomplete. V342 is still the registered ROM.

## Actual cause of V346 corruption

The town numeric bitmap is shared with other widgets. Its original header is
022BD774,4-bit,228x72,pitch57 words. The original native initializer at02010DCB0
binds pixels at0601BFC8. Observed VRAM bank D maps main BG memory, so same-frame
read-only LCDC exports identify the physical pixel span at offset07BFC8.

Decoded pixels show date digits in the supposedly free source cells around
x60,y12 and other numbers atx204,y36. Descriptor non-overlap had not accounted
for these additional owners. Moving percentages there corrupted both widgets.
The exporter now retains the671744-byte LCDC region for direct inspection.

## Corrected research design

V347 allocating in the static image initializer failed actual startup (white
screens, observed ARM9 instruction02003A58). This is a failed research build;
the exact underlying allocator failure is not claimed as proven.

V348 moved allocation to the original town bitmap binding call020B59AC. The
wrapper preserves its arguments, allocates15104 bytes through the original native
allocator, clears them, copies all8208 original bitmap bytes through the native
copy routine, and changes the backing image to228x132. A height guard reuses the
allocation on subsequent calls. Native execution against the captured real heap
verified allocation/copy, zero padding, and unchanged heap on the second call.
V348 still clipped the specialties because the town has a separate source-view
size of228x72 atARM9+11A64C.

V349 also changes that source-view height at11A650 to132. The visible240x192
parent is unchanged. Specialties occupy five new96x12 source rows beginning at
y72; their visible positions stay unchanged. The specialty-only text call uses
five-pixel ASCII advance and restores tracking afterward. All original percentage
and date source coordinates remain unchanged. All ROM graphics files, dimensions,
palettes, route scripts, heap bounds, arena/bootstrap/cache code, and original
static image initializer remain unchanged. Only the runtime backing view grows.

The wrapper occupies unused, source-owned commodity-name tails and the compact
helper's unreachable final8 bytes. Byte restoration guards recover the exact
repacked parent. No ROM padding is treated as an executable cave.

## Verification

- Preparation: `scripts/prepare_commodity_lazy_canvas_v348.py` currently emits
  V349 fixtures and the source/target hashes plus owned instruction addresses.
- Verifier: `scripts/verify_commodity_lazy_canvas_v349.py`.
- Evidence: `work/analysis/commodity_lazy_canvas_v349/proof.json`.
- All124 full native name getters and98 complete rasters pass.
- Actual China, Silk Cloth, Jade, Black Glacier Sword, North Sea Ambergris,
  and Fire and Ice Rubies masks match872 ink pixels, including first/final letters
  and blank cells. Every final-screen pixel outside the specialty column matches
  the V344 no-growth parent, including date and percentage fields.
- Earlier sampled specialty-column differences are intended spacing changes.
  The opening wipe atframe11400 matches the parent's complete frame11402 exactly.
  Dense captures match10/11 target frames to another captured parent phase;
  V393 resolves intermediate frame11399: all89 differing pixels are exact original
  scenery, and all11 frames use only correct scene/paper pixels or black reveal.
  Native timing and other scene contexts remain unproven. See
  `town_transition_v393_checkpoint.md`.

Maria visibility remains a one-byte research fixture, not a legitimate unlock.
Three commodity pointers supply long labels for the actual painter. Their stock
availability is not being claimed. These are targeted emulator tests, not a whole
playthrough or hardware verification. No candidate/patch handoff is authorized
by these research results alone.

## Newly observed market requirement

Ordinary market navigation and Buy selection reached the real Deal screen at
frame17600. The supplied Black Glacier Sword label wraps inside a word in both
Goods Info and the Local list. The town correction is therefore insufficient for
all commodity consumers. Those labels need compact native spacing and appropriate
word wrapping with complete letters, followed by the other market/cargo/price
contexts. Capture:`work/emulation_v193/commodity_v349_market_buy/`.

The prior pause-at17100 run ended atEOF without a final report; it is partial
research evidence only. The subsequent17600-frame run terminated normally with
a capture report. Do not use the partial run as an audited completed test.

## Outstanding

Finish market/cargo/price layouts, allocation lifetime across repeated visits and
other routes, the remaining transition frame, and registered combined ROM/patch
integration. All18 plaques remain incomplete. Online low-resolution images remain
exempt. The graphics goal remains active. At actual completion, revisit older
record-based checks.
