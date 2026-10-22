# V704: original portrait palette import and framebuffer half blend

## Result

The previous goal turn answered a status question and made no implementation or
verification progress. This checkpoint resumes the outstanding V704 investigation
and adds complete native routine evidence on unchanged production V692.

The palette initializer at `02047B18` reads the actual flat portrait atlas
`/GRP/CMMNIMG.000`. It does not request legacy `CMMNIMG.DK4` or raw comic
`SLACKIMG.DK4`. Its opacity loop is therefore not a discovered comic importer.

The overlay routine at `01FFAB74` is an in-place half blend. It reads existing
destination colours and averages them with a supplied solid colour before setting
opacity. It changes RGB and cannot substitute for a colour-preserving import.

## Complete original portrait initializer

The original routine executes from entry through its normal return in Unicorn,
using the retained V703 production-baseline RAM at frame6080. A guarded output
object is supplied outside main RAM. Only the four SDK filesystem operations are
bridged to actual ROM files; constructor, reader, seek, palette loop, copy,
descriptor construction, close and destructor execute original instructions.

The actual requests are:

|Resource|Read offset|Read bytes|Purpose established by output|
|---|---:|---:|---|
|`/GRP/CMMNIMG.000`|0|512|256 portrait palette words|
|`/_pxl/item.pxl`|20|512|Item palette copied into the supplied object|

All256 portrait palette words retain their low15 RGB bits and have bit15 set.
Exactly227 stored words acquire that bit; the other29 already have it. All512
runtime palette bytes match independently reconstructed source words at the
scratch buffer and original face-strip palette target. The source files remain
clean-ROM exact. No filename fallback, invented file or decoded pixel injection
is used, and every handle closes.

All16 constructed item descriptors have the original format, dimensions, relative
palette and pixel pointers. The output object's unrelated bytes and both outer
guards remain exact. Whole4MiB main-RAM differences are confined to the declared
palettes and original filesystem globals. All239 distinct executed native words
match clean original code. Stack and saved-register ABI pass.

This explains V547's earlier227-word normalization observation with a complete
connected original initializer. It adds no ordinary gameplay or GPU display claim.

## Complete half-blend contracts

Five complete original overlay calls cover both screens, an interior rectangle,
negative-coordinate clipping, right/bottom clipping, an empty off-screen rectangle,
and a whole screen. Both entire software framebuffers are compared for every case:
983,040 total output bytes, including untouched pixels. Point/size inputs, outer
guards and all main RAM outside the framebuffer remain exact. Native returns,
stack and saved registers pass; executed instructions match original code.

The independent expected output is:

`(((destination & 0x7BDE) + (fill & 0x7BDE)) >> 1) | 0x8000`

The five clipped areas contain77,40,28,0 and49,152 pixels. Of the49,297 affected
pixels,49,296 differ from an opacity-only import model. No external source-image
pointer is an argument to this routine. Its normal callers and GPU use are not
newly observed here.

## Bounded lead search and existing evidence

The retained scanner finds71 clean and74 current aligned ARM immediate-mask leads,
including possible inline data. Eleven in each version have nearby halfword
loads/stores. These are candidate windows, not eleven proven image importers.

The second palette loop, `0204BB3C`, belongs to the already source-bound TITLEMAP
reader: V221 previously executed all56 record reads and palette conversions. Its
existing proof and source classification are referenced, not counted as new tests.

A supplementary aligned ARM literal-load census across the same main/overlay/pool
sections finds one load of `80008000`, at `020F412C`. Its surrounding function is
retained as a structured-record writer lead, not established as a raw image import.
The original disassembly shows field packing and stride8 record writes; a complete
normal-caller interpretation is still open.

An ARM immediate `ORR #80` search finds16 leads, none with `STRB` in its bounded
nearby window. This does not exclude Thumb/register-mask code, generated masks,
other arithmetic, indirect conversion, longer dataflow or unobserved consumers.
Do not turn negative bounded searches into a global unused-art claim.

## Remaining scope and release

The original comic viewer, descriptor/import contract, normal scene selection,
page geometry, complete readability and concealed-background restoration remain
open. No global opacity correction or production artwork change follows from
these experiments. No new screenshot or guide claim is made.

The next useful consumer investigation must follow the original raw-image
descriptor/reader callers or source-corresponding modern artwork, rather than
repeat these portrait/TITLEMAP palette tests or apply the half blend to comics.

All18 original plaque/hint entries remain incomplete, all22 historical requirement
objects remain exact, and the full graphics goal remains active. The user-excluded
low-resolution Online screenshot translation remains excluded.

Production V692 stays SHA256
`0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.
ROM, patch, manifest, registry, canonical parent and release pointers are unchanged.
No commit or push.

Evidence: `work/analysis/opacity_paths_v704/`. Archive:
`E:/Rota Nova translations/Screenshots/Test fixtures/V704 Original opacity paths`.
