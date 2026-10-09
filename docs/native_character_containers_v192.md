# Native character container classification V192

2026-10-05. Graphics goal active/incomplete. Latest combined ROM remains V189;
V192 here is research, not a new ROM candidate.

## Two previously opaque blocks decoded

The actual IWRAM decoder at `01FF8000`, called by the character loader at
`020097F0`, decodes CHARA blocks 4/5 into 23,756 and 17,618 bytes. Both finish within
their bounded input/output buffers, preserve stack/register ABI and all canaries,
and return complete decoded data with pinned SHA-256 identities. The complete
6,944-byte canonical IWRAM prefix is unchanged in V189; previously added renderer
repair code extends that section to 8,172 bytes and is not mistaken for a decoder
change. The decoder's code and lookup helpers belong to the unchanged prefix.

The same whole-block decoding hypothesis is rejected for CMMNIMG blocks 0/2/3/7:
it attempts a backreference outside the controlled output buffer. Those blocks
remain unresolved. A failed hypothesis does not establish their true encoding or
prove that they contain no text.

## Corrected self-relative record origins

The native selector at `02008A10` resolves a record as:

`header address + table offset + record index × 4 + stored entry offset`

The stored entry offsets therefore use **each entry's own address** as their
origin. The earlier section-relative interpretation cut some record boundaries
incorrectly, despite its byte reconstruction passing. The corrected research
parser preserves stored offsets and applies the native origin before slicing.
The first header word 8 is the first table's offset, not an image/type tag.

All 406 selections across 203 record pairs in 10 containers execute the actual
unchanged native selector. Every pointer and complete selected payload matches
the corrected parser; native return/ABI, untouched source bytes and canaries pass.

| CHARA block | Storage | Record pairs |
| --- | --- | ---: |
| 4 | Native compressed stream | 83 |
| 5 | Native compressed stream | 56 |
| 6 | Original descriptor container | 8 |
| 7 | Original descriptor container | 7 |
| 8 | Original descriptor container | 8 |
| 9 | Original descriptor container | 12 |
| 10 | Original descriptor container | 7 |
| 11 | Original descriptor container | 8 |
| 12 | Original descriptor container | 7 |
| 13 | Original descriptor container | 7 |
| Total | | 203 |

## Numeric rendering metadata classification

The real actor renderer reads four-byte part descriptors from the first sections
and 16-bit controls from the second sections. It masks coordinate/flip fields,
subtracts coordinate bias `30`, and derives source tile coordinates and sizes from
the packed descriptor bits. Its controls select:

- First descriptor: `word & FFF`.
- Descriptor count: `((word >> 12) & 7) + 1`.
- Flip flag: `word & 8000`.

All 8,727 controls select complete bounded ranges of four-byte descriptors. The
native descriptor parsing code ranges are unchanged from canonical and pinned.
All tables and payloads reconstruct their complete containers without leftover
bytes. These 10 blocks are classified as **numeric actor/frame descriptor storage**;
their coordinate/size/flip data is retained. They contain no raster pixels or
written dialogue to localize. Referenced pixel atlases remain separate artwork.

This classification does not prove complete actor construction, actual visible
atlas selection, palette/alpha, GPU composition or gameplay. Those native gates
remain open. The corrected parser is a research tool; the production ROM builder
does not import it, and no ROM artwork or runtime code changed.

## Current embedded storage census

The 57 ILNK blocks now have these storage classifications:

| Classification | Blocks |
| --- | ---: |
| Bounded legacy palette images | 30 |
| Three external palette/pixel pairs | 6 |
| Native character descriptor containers | 10 |
| Unresolved storage format | 11 |

The 11 unresolved blocks are CMMNIMG0/2/3/7 and SLACKIMG13–19. Existing coherent
portrait/comic/thumbnail interpretations of SLACKIMG remain reviewed evidence;
their storage/native semantics are not silently promoted to proved formats.
Historical V151/V190 counts are preserved as historical snapshots. This current
census is source-locked separately and does not imply full visual/runtime clearance.

## Artifacts and remaining work

- `scripts/research_native_compression_v192.py`
- `scripts/verify_self_relative_character_tables_v192.py`
- Corrected `scripts/research_embedded_structures_v190.py`
- `work/analysis/native_compression_v192.json`
- `work/analysis/self_relative_character_tables_v192.json`
- `work/analysis/embedded_storage_census_v192.json`
- `work/qa/native_compression_v192/CHARA_4_decoded.bin`, `CHARA_5_decoded.bin`
- `work/analysis/embedded_structures_v190_before_self_relative_fix.json`

Native decompression, all 406 selectors, all 8,727 descriptor spans and Ruff pass.
Four Online screenshot translations, the 11 unresolved storage blocks, other
graphics formats/source fidelity and actual native visual/input/gameplay/cold-boot
gates remain. No full-goal completion or user acceptance is inferred.
