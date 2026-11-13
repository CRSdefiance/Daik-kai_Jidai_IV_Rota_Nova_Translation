# Complete item labels and whole-word paragraphs

This records the preserved item payload before the cache wrapper. The current
research target, promotional render/provider evidence and 69-test checkpoint
are documented in [item startup and providers](item_cache_promotional_research.md).
The payload below is exact in that newer target; its 2090 rasters are inherited
byte evidence, not fresh target executions.

The full goal remains active. **V158 is still the latest combined candidate.**
This is an ARM9 research image, without playable integration credit.
The current exhaustive local native sweep passes 2090 raster cases; release
integration remains pending.

## Changes and source review

35 logical records cover six headings, thirteen categories and sixteen crew
roles. Each label has a clean Japanese source, English meaning gloss, en-US
wording, localization note and per-record gates. Advice is a separate menu
command; Use is not visible in its mapped branch. Their formatting stays pending.

Short fixtures hid a category/role overlap after the first Effect/owner repair.
Complete labels now use category x0, role x88, Effect x180 and number x218,
with tracking -1. Owner names/prices start at x88 on y24. Navigation Gear and
Boarding Leader fit in full. Items remains centered with five-pixel advance.
Counter geometry/tracking and global category/role tables remain exact.
Private item getters preserve the source pointer/entry-address ABI.

Real advice exposed character wrapping that split words and placed a six-pixel
glyph one pixel outside the view. Narrow D5404 renders only one line per call;
an LF paragraph therefore loses its continuation. The item-only compiler now
preserves existing words, removes legacy machine alignment/padding, wraps whole
words within 47 characters and compiles separate NUL-terminated lines. A private
helper draws each line through the native painter, resets x and advances y by 12.
All 198 paragraphs fit three lines. Six legacy full-width uppercase I/F display
escapes become ordinary English only in this post-copy presentation.

COMMON bytes/global selectors remain unchanged. The private advice getter calls
the original loader before choosing the formatted item presentation. IDs outside
2815–3012 retain its original pointer. Original clips use absolute limits,
main [0,36,240,72] and standalone [0,24,240,60]; only the right limit moves to 239.
An experimental height/absolute-bottom mistake was rejected by missing-glyph
checks and corrected before integration.

## Exact identity and evidence

- V158 source ARM9: `cf2af4679fb30135b62d0388bbdcc5781d27114d79d47758dc901d9ba4da28a5`.
- Current research ARM9: `c55a2530af7816a5f612494c42c16af5911e58791d571d92ad9297b7e87980ee`.
- Unchanged COMMON: `ea978f466496f8593f13fb97f17b9bac174beea5665c57f1f5e358b2808776c9`.
- Pool 19520 bytes at 02387A20–0238C660; inherited 3584-byte prefix exact.
- Staging 023A7200–023ABE70; late-copy entry 023ABE40. ITCM stays 8172 bytes,
  ending 01FF9FEC with aligned low 01FFA000. Five helpers use reserved main RAM.
- 62 focused tests pass: inherited Gallery/movement/captions/duel and fourteen item
  tests for overlap, shifted pointers, full real paragraphs, missing continuations
  and invalid indices. 237 private lookup ABI cases pass.
- All 13 categories/16 roles were visually reviewed in sixteen uniformly scaled
  native panels across four grids. Ownership/artwork remain fixture contracts.

The completed current-hash proof contains 1338 synthetic and 752 actual
static-item cases in both callers/formats, complete glyph vectors, independent
pixels, nonoverlap, bounds, constructor/clear, shared source dispatch, SDK/ARM7
loading and arena reservation. All 29 representative/category-role panels were
visually reviewed. 33 local label formatting gates pass; Advice and skipped Use
stay pending. The same-hash synthetic phase was retained during startup-test
repair; its whole expected field vectors and immutable source ROM were checked.
Actual resource and loading gates were rerun and saved. Both phase proofs now
persist before later gates, so failures cannot discard local evidence.
`item_interface_native_proof_before_word_wrap.json` preserves the preceding
category-only proof; its different hash does not approve the new paragraph code.

The first resource sweep caught a verifier error for a relocated item name.
The oracle now resolves both resident text and the copied pool. All 188 static
name pointers are classified; the error did not change ROM bytes.

Both boot and canvas setup had a fixed 10000-instruction late-copy limit. The
expanded pool needs 19584 allowed steps; the old cap stopped before the POP and
misreported register/stack damage. Both helpers now derive the limit from the
complete aligned payload and explicitly require caller return and exact copied
bytes. Native full copy, source construction/clear/shared draw and arena probes
pass independently. No ROM startup code was changed by this test repair.

## Native providers and required next work

Static records are at 0211E210. Native CB190 returns 022D322C; the item vtable
is 0213C38C and name virtual 0204A53C. Native CDAFC/property/index getters and
COMMON copies execute. Description IDs are item index+2815. Runtime item-object
and warm-cache initialization remain contracts. All 188 static indices pass both
native draw functions and formats with complete name and continuation glyphs.

Promotional indices 188–197 use CDAFC→02102BB0 and dynamic owner 023800C8,
whose 24-byte metadata array starts at owner+3E4. Actual native initialization
segment 02102C24–02102C7C copies all ten default names and metadata with bounded
writes and intact canaries. The segment stops before random additions; its full
return, downloaded states and promotional screen rendering remain pending.
Proof: `work/analysis/promotional_item_default_initialization_proof.json`.

Before integration, finish actual Advice menu consumers, promotional data,
real crew/ship names and owner searches, counter source initialization and
complete parent crops/artwork. Refresh inherited consumers, lock exact-hash
evidence, register/build the full profile, and verify saved ROM/manifest/lineage/
patch. Physical cold boot and explicit full-candidate acceptance remain required
for promotion. Global role/category consumers still need their own translation
and layout audit.

Cache visibility for the newly executable main-pool helpers is a separate release
gate. The original late copy was designed for data. Its native SDK loader uses
CP15 maintenance at 02000A34/02000A38/02000A3C, but the emulator skips these
instructions and does not model instruction/data caches. Map and preserve the
required startup maintenance before placing executable helpers in a playable
candidate; local instruction execution does not prove physical cache visibility.

Files: `work/analysis/item_interface_plan.json`,
`work/analysis/item_interface_research_arm9.bin`,
`translations/item_interface_manuscript_v1.json`,
`work/analysis/item_interface_native_proof.json`,
`work/analysis/item_label_grid_proof.json`, and
`work/qa/item_interface_native/label_grid_0.png` through `label_grid_3.png`.

Canonical baseline, V158 ROM/patch and registry are unchanged. No promotion,
commit or push is claimed. Revisit older record-based checks after goal completion.
