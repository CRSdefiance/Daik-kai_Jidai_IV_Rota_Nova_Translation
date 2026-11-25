# Exact raw/PXL copies and complete FLS reader V224

The previous turn verified ocean-init texture reads and startup palettes. This
turn identifies exact embedded pixel copies, fixes a shared-reader omission,
accounts for every PXL/FLS asset, and reproduces V218 exactly. **No playable ROM
bytes change. The full graphics goal remains active.**

## Four exact DSCHR pixel copies

The clean DSCHR bank contains the complete packed pixel payloads of these loose
PXL files, and both representations remain unchanged in V218:

| Loose source | Raw pixel offset | Complete pixel bytes | PXL dimensions |
|---|---:|---:|---|
| chara00.pxl | 0 | 131,072 | 1024x256, four-bit |
| chara01.pxl | 131,072 | 4,096 | 128x64, four-bit |
| chara02.pxl | 135,232 | 4,096 | 128x64, four-bit |
| chara03.pxl | 139,392 | 4,096 | 128x64, four-bit |

Every payload byte is identical. Complete source views show character, equipment,
building/ship-part and animation sprites, without a readable composed Japanese
instruction or caption. Preserve the original art.

Pixel equality does **not** establish palette equality or native parent/crop
selection. The loose palettes do not byte-match the corresponding raw slots;
their displayed colors are separate evidence to map. These matches cover
**143,360 pixel bytes**, not the whole DSCHR file. Another **66,752 bytes**, including
palette gaps and later source data, remain outside the exact-copy comparison.

## OCINIT ship lead is partial

Five nontrivial 128-byte anchors match ship.pxl. Rearranging its two vertical halves
side by side accounts for **7,733 of 8,192 bytes** in the OCINIT region at 20800.
The remaining **459 differences** matter. Do not synchronize this region from the
loose file or borrow its palette as if the match were complete. The native table's
512x32 four-bit texture metadata is a useful lead, not a complete equivalence proof.
No OCINIT payload or palette is changed.

## Previously unsupported raw FLS record

The FLS reader assumed all palette/pixel slots were LZ10 streams. The root
`/m02_03.fls` has raw storage instead: its archive compression bit 80 is clear,
and its declared slots contain a 512-byte palette and 262,144 indexed pixels.
The record's visible-height field is 377; its stored source is 512x512, with
original padding retained. Its complete source view depicts coastal buildings,
harbor, sea and birds, with no readable Japanese caption.

`FlsArchive` now selects raw or LZ10 storage from the **archive header**, not the
per-texture flags. M22 contains the same texture flags with compressed storage,
so treating texture flags as a compression discriminator would be wrong.

Raw reads enforce declared slot bounds. Raw serialization preserves raw storage;
the original file round-trips byte for byte. The existing compressed path and
height behavior remain intact. This is source-reader/storage support, not a claim
that the raw illustration's actual loader, visible crop or projection is verified.

## Complete asset accounting and regression

The saved audit accounts for **all 660 PXL payloads**: 618 indexed assets and 42
direct-color portrait assets. Direct-color portraits are checked from their
declared headers/payload sizes and are not silently dropped by the indexed parser.

All **261 FLS textures** decode with zero exceptions, including the raw harbor
illustration. Together these are the historical 921-entry source inventory; this
count is not a claim that every localization or display gate is complete.

After the shared reader change, the registered builder reproduces the complete
V218 ROM exactly:

`be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f`.

All earlier translations, graphics, routes and release stages are preserved.
The existing V218 and its exact patch remain the current combined candidate.

## Evidence and next work

- `dk4tool/graphics/fls.py`: raw/compressed storage selection and exact raw writing.
- `scripts/audit_raw_matches_v224.py`, focused Ruff passing.
- `work/analysis/raw_pxl_matches_v224/saved_audit.json`: all source rows, exact
  copies, raw round-trip and complete prior-ROM reproduction.
- Four full chara source previews and `raw_harbor_full_reader.png`.
- `ocinit_partial_anchor_matches.json`: partial ship leads only.

Remaining raw palette/parent/crop relationships, unmatched DSCHR/OCINIT data,
other embedded resources, four unreadable Online screenshot bodies/chat,
confirmed-name consistency, contextual/native/gameplay and final whole-scope
verification stay in the goal. Older record-based checks remain to revisit after
full completion.
