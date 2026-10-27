# Complete remaining COMMON manuscripts and packing research

## V154 refresh with ARM946 copy behavior

`probe_remaining_common_layout.py --current-v154` now prepares the same 245
drafts against the complete repaired V154 ARM9. All 3,668 selections are
compared, and all 798 warm/cold authored/neighbor copies preserve their text,
terminators, guards and stack with ARM946 unaligned accesses modeled explicitly.
Current copy, boot and name changes are retained in the research ARM9. Artifacts
use the separate `remaining_common_v154_*` prefix under `work/analysis/`.
The old V150 evidence remains historical and is not substituted for the new
CPU behavior. Actual draw/resource consumers and formatting approval remain
pending; V154's playable COMMON content is unchanged.

## Current status

The saved V150 inventory still has 245 Japanese native selections across 133
physical records. Every selection now has source-reviewed English prose:
31 promotional entries in `common_online_promotional_manuscript_v2.json` and
214 scene/artwork/name labels in `common_scene_labels_manuscript_v1.json`.
These are drafts with unresolved COMMON consumer/presentation gates. V150,
its patch and the canonical baseline are unchanged; there is no integration
credit from this work yet.

## Scene/artwork/name prose

The complete 3393–3606 range is covered exactly once. Of 214 labels, 123 match
clean Japanese in the already reviewed inline-caption manuscript; those names
retain their existing English. The other 91 are translated from clean COMMON
source, retaining scene details, locations, character spellings, numbered/lettered
variants, large-artwork markers and exploration directions/obstacles.

Every row has exact clean bytes and previous/next source labels. All English is
one paragraph with the fixed-encoder PAD marker; there are no authored wrapping
spaces or breaks. The 214 prose records pass structural/editorial validation in
an isolated in-memory formatting assumption. Their actual formatting flags stay
false, and the strict insertion validator rejects the saved manuscript.
Inline caption correspondence does not establish the separate COMMON consumer.

Two source anomalies remain explicit:

- COMMON 3497 says 総見算のマリアたち; the corresponding ARM9 scene says
  総見式のマリアたち. Matching preceding/following labels establish Maria route
  indices 34–36 and COMMON 3496–3498. **Maria and Her Companions at the Grand
  Review** follows that scene context, with the variant documented.
- COMMON 3537 has an unexplained terminal full-width t in 森03右折ｔ. The label
  retains it as ASCII t, pending resource/consumer context; it is not silently
  removed or treated as a layout command.

## Whole-owner packing and actual native copies

`probe_remaining_common_layout.py` combines both manuscripts in disposable
research against exact V150. It preserves every nonauthored packed neighbor
and reblocks complete physical owners into the original five final cache blocks
36–40. Their sizes are 3,957, 4,041, 4,025, 4,095 and 1,641 bytes, each below
the native 4,096-byte cache limit. No owner is split or text shortened.

All 3,668 selections are compared independently by the planner. Every unrelated
selection, executable loader/selector byte and ARM9 byte outside the message
directory/offset tables is preserved. The largest selected copy is 376 bytes,
below the 512-byte output buffer including its terminator.

All 245 authored messages and all 154 unchanged messages sharing that pool
execute actual native selector/copy bodies in both warm and cold cache cases:
798 guarded copies total. Complete text, leading/final bytes, NUL, output guards
and stack are verified. Cold cases execute the native ILNK header/block path
with bounded successful host open/read contracts, not physical file I/O.
Header reads use their actual bounded stack scratch. A deliberately shifted
3393 start offset drops its leading character and is rejected by the native
copy verifier.

Research artifacts: `work/analysis/remaining_common_research_common.bin`,
`remaining_common_research_arm9.bin`, `remaining_common_layout_proof.json` and
fresh saved inventory `common_remaining_v150.json`. New scripts pass lint.

## Required next work

Classify actual COMMON consumers, distinguish resource identifiers from visible
labels, and map draw geometry, wrapping and glyph rendering before formatting
approval and registered combined integration. Keep all complete source meaning;
do not fit long prose into an assumed dialogue box or infer unused text solely
from inline duplicates. Native copy correctness does not prove readable display
or intact rendered glyphs. Preserve all inherited translation stages when this
research becomes a registered terminal COMMON release.

The full goal also retains ARM9/UI/graphics work, older-English fidelity and
runtime/gameplay checks where available. After completion, revisit older
record-based checks as requested.
