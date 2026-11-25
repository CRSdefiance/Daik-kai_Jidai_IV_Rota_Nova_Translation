# Raw sea-art records and classification V219

The previous goal turn localized the no-target notice and verified V218. This turn
executes the complete raw creature/ocean record readers and upload argument paths,
inspects full source artwork, and records nine decisions to retain original art.
**No ROM bytes change. V218 remains current; the full goal is active.**

## Complete native file partitions

All 14 cases execute the unchanged native queued reader at `020CDE20` and upload
dispatcher at `020CE238`, returning with the original saved-register/stack ABI.
SDK filesystem and hardware transfers are explicit bridges to the exact source.
Every read byte, offset, file handle and buffer guard is checked. The cases cover
all **178,176 bytes**, without gaps, overlap or ignored source tails.

| Family | Native kind | Records | Complete file bytes |
|---|---:|---:|---:|
| GMONS | 1 | 6 | 94,208 |
| OCETC | 2 | 8 | 83,968 |

The two metadata tables are verified from actual file-selection branches, not
their proximity in memory. GMONS uses the six-entry table at `02125908`; OCETC
uses the eight-entry table at `02125938`. Each record includes a 512-byte palette.
Native pixel uploads select texture offset `2F000`; palette uploads select `1000`.
GMONS uploads all 512 palette bytes. OCETC uploads the first 384; the remaining
128 bytes are still preserved and inspected, not silently dropped from the file.

All source files and the reader/upload code remain identical to the clean ROM.

## Native texture format

The original register fragment `0206C064..0206C074` writes `6ED05E00` to
`040004A8`: a 256x256 texture in the 16-color indexed format at `2F000`. A separate
original fragment `0206B6B8..0206B6CC` adds its preceding stack width parameter;
six explicit inputs verify widths 8,16,32,64,128,256 with 256 rows. The format is
four bits per pixel, with color zero marked transparent. Field interpretation is
supported by the primary [libnds header](https://github.com/devkitPro/libnds/blob/master/include/nds/arm9/videoGL.h).

These are complete register-fragment executions, not GPU rendering or proof that
an arbitrary width belongs to a particular record. The different source views do
not replace that missing parent-selection evidence. RGB previews also do not claim
physical alpha composition.

## Source-art decisions

Original low/high nibbles and complete palettes produce full source views. All
sixteen palette variants for each entry below were inspected at full resolution.
They show coherent creature, weather and water animation artwork, with no readable
Japanese instruction or caption. Keep their exact pixels, borders and palettes.
The descriptions below are visual categories, not official creature identities.

| File | Records retained | Observed source forms |
|---|---|---|
| GMONS | 0,1,3,5 | Spiny/tentacled/rounded creatures, shark and splash animations |
| OCETC | 0,1,3,4,7 | Dolphin/water figures, vortex, whirlpool and lightning animations |

Decisions and exact source/reviewed-sheet hashes are in
`translations/raw_sea_art_decisions_v219.json`. This settles source-art localization
for these **nine entries**, while actual scene palette selection, UV crops and
alpha remain separately scoped native-display work.

Five small records remain open: **GMONS 2/4 and OCETC 2/5/6**. Some reconstructed
layouts are striped; other candidate widths reveal water/splash-like shapes.
Those observations are useful evidence, but exact native source layout/parent
selection is not yet established. No whole-file text-free clearance is claimed
for either family, and none of these five is edited or prematurely retained.

## Other resource leads

The actual TITLEMAP filename begins at `0213E2CC`, referenced by `0204BC70`.
Its reader/bitmap construction is now located near `0204BAE0..0204BC6C`; source
interpretation remains open. OCINIT has readers in the initial sailing loader,
queued dispatcher and race code. DSCHR has multiple queued source branches plus
generated-text alternatives. These are located leads, not additional asset clearances.

The prior V212 generated-help queue investigation remains separate from the live
English panels integrated in V217/V218. A preserved string or a parameterized
queue fixture is not proof that its old alternative is currently displayed.

## Evidence and remaining scope

- `scripts/research_raw_art_v219.py`: all 14 native reads/uploads and complete
  indexed/palette-preserving views.
- `scripts/verify_raw_texture_formats_v219.py`: seven original texture register cases.
- `work/analysis/raw_resource_v219/native_record_proof.json`,
  `texture_format_proof.json`, source views, complete overview and geometry candidates.
- `translations/raw_sea_art_decisions_v219.json`: nine scoped retain decisions.

Focused Ruff passes. No candidate, patch or release-stack change is needed for
unchanged art; existing V218 and its exact patch are preserved. Five small layouts,
TITLEMAP/OCINIT/DSCHR and other embedded/raw consumers, four Online screenshot
bodies/chat, confirmed-name consistency, contextual/native/gameplay and the final
whole-scope audit remain in the goal. Older record-based checks remain scheduled
for revisiting when the full goal is complete.
