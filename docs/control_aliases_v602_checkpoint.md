# V602: decoded control-copy search and current English synchronization

The previous turn made progress by verifying all29 score-label cases with the
original drawing routine and complete bitmap planes. This turn investigates
whether unresolved Confirm/miniature controls have copies in other graphics
resources. Production V599, its patch, graphics and release registry are unchanged.

## Search method and complete declared coverage

Seven original templates cover the full Confirm button, its inner face, and the
five small Pick Cargo/Pick Ship/Done/Rank/Cancel cells. These are source Japanese
templates, not English strings used to search for already translated output.

The search decodes all660 PXL files and261 FLS textures. It checks1313 color
domains, including indexed palette banks and42 direct-color PXL files;879 distinct
indexed textures also receive a palette-independent exact-index-shape search.
Every row is checked at its actual decoded stride. Packed-file contiguity and
equal source/destination image widths are not assumed. BGR555 comparisons retain
bit15; index-only matches explicitly do not establish palette or alpha equivalence.

A synthetic control places the original39-by14 Confirm face at odd pixel x17
inside a128-pixel-wide, two-bank four-bit image. Its palette indices are reversed
and its valid colors occupy bank1. The color search finds that crop exactly;
bank0 is rejected. Changing one Japanese face pixel outside the anchor row keeps
the search anchor intact but correctly rejects the full crop. These are analysis
controls only; no ROM artwork is modified.

All seven original self controls are found. No additional exact color or indexed
copy appears in the declared PXL/FLS domains. This does not exclude resized,
partial or recolored-and-reindexed copies, arbitrary runtime composition or raw
blocks outside a known decoder. It is not proof that Confirm is unused.

## Embedded storage: decoded packets and external palettes

All57 blocks in the existing six-archive storage census are visited. The bounded
legacy decoder recognizes31 type16 image packets, including successive packets
when the preceding extent identifies the next header. Their128 palette domains
are searched. Nondecodable blocks and uninterpreted trailing bytes remain listed;
they receive no automatic graphics or native-use clearance.

The separate established type19-palette/type18-pixel storage pairs add three
packed image interpretations and104 palette domains. Headers, extents, complete
index unpack/repack and current palette retention are checked. These remain
storage interpretations; adjacency does not prove the game uses a specific
palette bank or that a control is displayed through that archive.

Exact full-color and lower15-bit storage comparisons do not identify the five
known common-atlas copies. An explicit index-shape pass does, demonstrating why
palette equivalence must not be inferred from glyph shape. The five matches are
in `/GRP/CMMNIMG.DK4` pixel block5, associated storage palette block4:

| Control | Loose source crop | Embedded index crop |
| --- | --- | --- |
|Pick Cargo|[208,32,256,40]|[464,32,512,40]|
|Pick Ship|[208,40,240,48]|[464,40,496,48]|
|Done|[240,40,256,48]|[496,40,512,48]|
|Rank|[184,48,208,56]|[440,48,464,56]|
|Cancel|[208,48,256,56]|[464,48,512,56]|

These are automatically recovered known aliases, not newly visited native
screens or newly discovered missing translations. The former whole-atlas copy
checks remain valid; this search adds cross-resource template coverage.

## Current text and source compatibility

All five complete current embedded index crops match their loose English crops.
Independent compact-font layout checks include all307 foreground points, every
first/final letter and space, plus the blank remainder of each original source
cell. Confirm's complete86-point English face also matches the original ASCII
font contract. Both entire current control atlases are byte-identical to V573,
preserving the prior controlled native Confirm/miniature evidence; no new native
consumer credit follows merely from that continuity.

The original complete initializer is re-executed: owner023139C0 still initializes
`_pxl/kakutei.pxl`. It has no score-style wrong-owner correction. The separate
Confirm and five miniature ordinary parents remain unresolved. Continue genuine
dynamic selection, external-palette/embedded consumers or runtime-generated
views; repeating the earlier direct-literal census will not establish a screen.

The reviewed comparison sheet shows original and current loose crops plus a
white/black embedded **index mask**. Its third column deliberately does not claim
native embedded colors. This is an analysis sheet, not an emulator screenshot
or guide candidate. No new Japanese-bearing copy requiring a patch was identified
within these declared exact-template domains.

## Artifacts and scope

- `scripts/scan_graphic_template_aliases_v602.py` and
  `decoded_template_alias_proof.json` under `work/analysis/graphics_aliases_v602`.
- `scripts/scan_embedded_control_aliases_v602.py` and
  `embedded_control_alias_proof.json` in that directory.
- `scripts/verify_control_aliases_v602.py` and `current_control_copy_proof.json`.
- Source/current/index review sheet and hashed evidence under
  `E:/Rota Nova translations/Screenshots/Audit comparisons/V602 Control aliases`.
  There are no new native screenshots or guide-publication approvals.

All three scripts pass targeted Ruff and Python compilation. Production remains
experimental V599, SHA256
`1c72049ca2eba551825d67de2429b4ac9751179183afc2ddb5749666d398eba5`;
its patch remains
`2aa5a523cfef3165db2eae31643b2d66e3e08a75aa709c025066958a144ffc9f`.
All18 original plaque entries remain incomplete and all22 historical objects
retain exact scope. Other material, legacy/village/movie and acceptance gates
remain open. This is progress in decoded-copy auditing, not graphics-goal
completion or global proof of nonuse. Revisit older record-based checks at full
completion.
