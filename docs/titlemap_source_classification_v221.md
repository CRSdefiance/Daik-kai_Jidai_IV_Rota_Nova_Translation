# TITLEMAP native records and source-art review V221

The previous goal turn completed five additional sea-effect source reviews. This
turn resolves TITLEMAP's actual record layout, executes every native read/palette
preparation/bitmap constructor, and records full source-art preservation decisions.
**V218 remains unchanged and the full graphics goal is active.**

## Actual native layout

The literal at `0204BC74` is **4940**, or **18,752 bytes** per record. It is not
4000. Each record has 18,240 indexed pixel bytes followed by 512 palette bytes.
The exact file length is 56 records: **1,050,112 bytes**, without an extra tail.

| Field | Native value |
|---|---|
| Pixel buffer | `02233040` |
| Palette buffer | `02237780`, exactly 18,240 bytes after the pixel buffer |
| Indexed bitmap flags | `108` |
| Row pitch | 76 words, or 152 bytes |
| Image/view dimensions | 152x120 |
| Selection formula | `(variant + region * 8) * 4940` |

Seven region and eight variant inputs cover the whole file. Those inputs are
explicit preceding-getter fixtures; they do not claim legitimate scene selection.

## Native verification

All 56 cases run the original stream constructor/open, parent read path,
256-entry palette preparation, stream close and bitmap construction. Only SDK
open/read/absolute-seek/close are bridged to the exact unchanged ROM file.

Every source byte, offset, count, file handle and surrounding buffer guard passes.
The only runtime palette transformation is the original OR with 8000, setting
the opacity bit; original stored palettes remain unchanged. Native bitmap headers
and relative pixel/palette pointers are checked with 32-bit wrapping. Every view
returns exactly 152x120. The complete source contains **1,021,440 indexed pixels**
and **28,672 palette bytes**.

The initial 128-wide/16-KiB diagnostic used incorrect boundaries and an incorrect
palette assumption. It is rejected. Correct source views come directly from the
native 4940-byte record and palette offsets, not a visual guess.

## Source-art decision

All 56 complete images were reviewed. They contain geographic clue-map art,
decorative borders/motifs and red location markers, with no readable Japanese
caption or instruction. Preserve all original pixels, palette entries and borders.
Do not replace decorative motifs with invented text or alter red markers.

Exact per-record source and reviewed-preview hashes are recorded in
`translations/titlemap_art_decisions_v221.json`. This completes source-art
classification for TITLEMAP, not every native scene/display gate.

## Final presentation remains separate

The real caller adjusts the bitmap object through its copy-interface subobject
before calling `020D4988`. That call queues a drawable in the active scene list;
it is not an immediate pixel blit. V222 corrects the argument order and establishes
all native bounds; C9904 processes the UI hierarchy rather than performing a pixel render. A correctly initialized active-list fixture
queues successfully, but the subsequent `020C9904` scene render still requires
additional scene binding. The attempted destination fixture is not a verified
full copy/crop or framebuffer result.

Do not treat that failed final-render probe, or the complete source views, as proof
of actual GPU composition, input behavior or gameplay selection. Those remain open.
No source bytes are changed to work around an incomplete fixture.

## Artifacts and remaining goal

- `scripts/verify_titlemap_v221.py`: all native reads, palette/header construction
  and exact buffer/pointer checks; focused Ruff passes.
- `work/analysis/titlemap_v221/native_proof.json` and 56 hash-pinned native previews.
- `all56_native_source.png`: complete original source overview.
- `translations/titlemap_art_decisions_v221.json`: original-art decisions.

No new ROM or patch is needed for unchanged artwork; the combined V218 and its
exact patch are preserved. Native final scene copy/crops, OCINIT/DSCHR and remaining
embedded/raw consumers, four Online screenshot bodies/chat, confirmed-name
consistency, contextual/native/gameplay and final whole-scope verification remain
in the goal. Older record-based checks remain to revisit after full completion.
