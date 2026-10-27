# Registered graphics pixel ownership V226

V225 checked formats, dimensions, flags, palettes and extents for all 921 entries.
This turn checks pixel ownership against registered batches and the accepted
canonical baseline. **V218 remains unchanged; the full goal remains active.**

## Native image-index comparison

The audit covers **81 registered graphic entries**. All **48 PXL/FLS entries
changed after the canonical baseline** have registered ownership, including normal
label boxes, indexed-art regions and whole subtitle slots owned by the full-slot
FLS label writer.

Every changed index outside those declared regions matches the accepted baseline.
There are **zero new out-of-scope pixel changes** in these entries.

An initial clean-ROM comparison flagged 4,998 pixels across six images: marker,
regional fleet, Golden Route discovery/logs and character selection. All 4,998
are existing accepted canonical artwork and remain unchanged in V218. They are
not new defects or a reason to restore Japanese source pixels.

| Comparison | Result |
|---|---|
| Canonical to V218, outside registered regions | No pixel changes |
| Clean to V218, inherited pixels outside those regions | 4,998 canonical pixels preserved |
| Changed-after-canonical entries lacking ownership | None of 48 |

## Scope limits

An owned box can contain translated text and background recovery. This audit does
not prove that every inside-box pixel is correct, that a border crossing a box is
undamaged, that letters fit their native crop, or that alpha/readability/gameplay
is complete. Those requirements retain separate evidence and open items.

Whole-slot ownership is used only for the registered FLS label format whose writer
clears/replaces that subtitle texture. It is not inferred for other formats.
Embedded raw banks and their explicit transfer/consumer proofs remain separate.

## Reproducible evidence

- `scripts/audit_graphics_ownership_v226.py`, focused Ruff passing.
- `work/analysis/graphics_ownership_v226/ownership_proof.json`: source hashes,
  every registered owner/box and per-entry counts.
- The V225 whole-inventory preservation proof remains valid.

No artwork is altered and no new ROM or patch is produced for the audit. Current
V218 and its exact patch remain intact. Four screenshot body/chat translations,
confirmed-name consistency, remaining embedded/contextual/native display and
final whole-scope gameplay verification remain open. Readable screenshot source
material has been requested. Older record-based checks remain to revisit after
full completion.
