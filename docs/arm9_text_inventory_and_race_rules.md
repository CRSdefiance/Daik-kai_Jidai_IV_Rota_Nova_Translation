# ARM9 text inventory and Grand Race instructions

## Actual CP932 numeric and player-name glyph pixels verified

The optional Kanji-font mode in `execute_scene_caption_raster.py` now loads the
actual 6,944-byte ARM9 auto-load section at 01FF8000 and executes the native
CP932 painter at 01FF83AC. D198C/D19BC execute the actual 3,340-entry font-map
lookup. The exact 73,480-byte clean `/GRP/KANJI.FNT` asset initializes its native
runtime address; V139's asset is byte-identical. Palette, map, lookup/shadow code
and exact painter span remain identical to clean. Older translated strings in
other ITCM-section data are preserved; the whole section is not claimed clean.

Independent decoding reads eleven rows of two packed MSB-first bytes per glyph,
paints the real foreground and lower-right shadow, and compares the entire
bitmap buffer in both direct-color and paletted formats. All ten full-width
digits, zero, 255 and 65535 pass with odd/even names and the eighteen-byte ASCII
name limit: 66 mixed native numeric pixel cases. Another 68 CP932 player-name
cases cover complete pairs through eighteen bytes and mixed ASCII/CP932 parity
with Monster Fish and Giant Squid class labels. Native printf, ordered full
glyph sequence, first class letter at x6, full-buffer pixels and bounds pass.

The six-panel native-ink preview was reviewed: complete numbers, maximum ASCII
and CP932 names, Armament and class leading characters are intact. Ink/shadow
colors are normalized for inspection; this does not establish physical palette.
Evidence: `work/analysis/map_creature_complete_v139/native_cp932_pixel_proof.json`
and `native_cp932_ink_preview_review.json`. Mutation tests reject changed ITCM
pixel masks, changed/truncated font data; original request-only mode retains its
explicit painter contract. Inherited caption and Golden Route rendering tests
also pass with the optional painter extension.

The CP932 pixel-painter contract is closed for these tested tooltip paths.
Font disk loading, bitmap origin/clear, physical composition/palette and gameplay
remain explicit contracts/checks. Strict tooltip release preparation remains;
V139 and the research ARM9 text proposal are unchanged.

## Player faction-name capacity and serialized extent verified

The actual player faction name is special-owner+55: the special object starts
at shared-state+19E4, so its name is shared-state+1A39. Native default producer
46F50:46F78 resolves the route-specific faction table and copies its complete
name into temporary record+3B. CD704:CD710 then copies record+3B into owner+55.
Four actual native defaults pass: Castor Co., Bergstrom Fleet, Argot Co. and
Li Clan.

Faction-name edit dispatch 9DF54 passes an explicit eighteen-byte limit at
9DF74 to AEB98. Native dispatch, strlen and accepted-name copy execute for all
ASCII lengths 1-18 and complete CP932 pairs 1-9. The keyboard UI remains an
explicit contract. The inherited whole-character append repair also passes
at this actual capacity for lengths 16, 17 and 18 with one/two-byte inserts.

Both serialization loops are inclusive: CMP #12 followed by BLE visits byte
indices 0 through 18, copying nineteen bytes including a valid name's NUL.
Native loops 83050 and 83148 and actual byte helpers 469DC/46BE0 execute for all
27 fields, preserving every byte, counter, stack and adjacent-field guard.
Physical I/O is the explicit backend contract. Load does not synthesize or
validate a NUL in malformed saved fields; a negative fixture records that fact.

All 39 classes render with seventeen- and eighteen-byte ASCII player names in
both pixel formats: 156 complete native printf/glyph/row/buffer checks pass.
Combined faction/player-name regressions pass. Evidence:
`work/analysis/map_creature_complete_v139/native_player_faction_name_proof.json`.
Full-width numeric/name CP932 pixels, physical palette/composition/gameplay and
strict release preparation remain. V139 and all proposed text are unchanged.

## Fixed faction names traced through native lookup and tooltip rendering

The native faction constructor CD488 selects 68-byte source records at 11BC70,
then writes the complete name pointer into runtime owner+4. Runtime owners use
76 bytes at the CB160 base plus four. Vtable 137240 slot+8 calls 3CF9C: other
factions return that fixed pointer; the current player faction returns the
CB184 shared-state base plus 1A39. Native route lookup 397D8 maps the four routes
to faction indices 0, 2, 1 and 3. The ordinary faction bound at 24748 is twenty.

`probe_map_tooltip_faction_names.py` executes the actual constructor, index
arithmetic, route lookup, comparison and name getter for all twenty ordinary
factions under all four routes: eighty selections pass. Stack/return and adjacent
76-byte owner guards survive. All twenty inherited fixed pointers and full
text/NUL are unchanged. Each fixed name then passes through native printf and
the actual tooltip renderer with all 39 classes in both pixel formats: 1,560
full glyph/row/buffer comparisons pass, including intact leading characters.
Thirty-one targeted regressions and Ruff pass; changed route mapping, virtual
getter and name accessor field reject.

Evidence: `work/analysis/map_creature_complete_v139/native_faction_name_proof.json`.
The player-name fixture proves selection, not its input capacity. The editor,
writer and save/load bounds for shared-state+1A39 remain unresolved; no 16- or
32-byte limit is inferred from the generic name editor. Older faction/class
English fidelity, numeric CP932 pixels and physical presentation checks also
remain. V139 is unchanged; this research is not yet approved for integration.

## Tooltip numeric sources bounded; mixed full-width digits verified

Actual map armament formatting receives CP932 full-width digits from ABF50, not
ASCII placeholder numbers. B4AA8 matches one of three faction/percentage byte
pairs and returns an unsigned byte (0-255), or zero for no match. B3FD4 with the
caller's constant index one returns the unsigned halfword at object+18 (0-65535).
ABF50 converts the native values to complete full-width decimal bytes through the
32-slot, 128-byte AC000 ring. These getter/converter/allocator bodies execute.

`probe_map_tooltip_numeric_values.py` verifies all 768 percentage value/entry
combinations, twenty decimal/ring boundary cases, and forty mixed ASCII/CP932
cases in both pixel formats. Two successive numeric allocations retain distinct
live pointers across slot31-to-slot0 wrap, complete leading/last bytes and NUL,
unchanged earlier bytes in each slot, every other slot and the exact final ring
index. Native stack/return state is intact. Decimal boundaries include zero,
9/10, 99/100, 999/1000, 9999/10000 and 65535.

Actual native printf uses those full-width digit bytes, then the native tooltip
renderer receives the complete copied text. Every visible ASCII name/percent/
Armament glyph and every CP932 numeric glyph request has the expected code,
style, row and coordinate; leading Armament stays at x6/y12 for odd/even names.
Native measured width remains within256; the tested maximum second row is126px.
Forty-six combined numeric/allocation/tooltip regression tests and Ruff pass,
including changed digit arithmetic, out-of-range input and buffer wrap/lifetime.

Evidence: `work/analysis/map_creature_complete_v139/native_numeric_proof.json`.
CP932 number pixel painting is still the explicit ITCM painter contract; this
proof covers the actual requests and positions, not those pixels. Exhaustive
dynamic faction/user-name bounds, physical palette/routing/gameplay and strict
release preparation remain. Earlier ASCII-number fixtures are representative
renderer checks and are not the actual numeric source proof. Complete English
wording, allocation and existing proofs are unchanged; V139 remains current.

## Full creature names allocated; all static class tooltips verified

All four complete creature names now fit with the five full map tooltip labels/
formats and all six inherited Golden Route labels. Exact source-owned packing
uses 151 of 172 string bytes and retains 21 spare. Complete existing Monster,
Whale, Shark, Next and Switch strings are shared under full text/NUL/source checks;
their storage is unchanged. No label is shortened.

The two-entry Golden Route heading table moves from 16A1B0 to the former creature
slot 15B7E8. Its sole byte-position literal consumer F2D04 is verified in clean,
canonical and V139 sources and updated; both native title lookup instructions
use that same literal. This joins the already owned neighboring text spans into
one 68-byte pool. All source/padding, all declared literal/interior consumers and
all changes outside the complete owned pools/pointer fields are checked. Native
instructions, fonts, tracking and geometry are unchanged. The source pointer scan
now sorts declared spans and rejects overlapping source owners before scanning;
regressions prevent silently skipping spans supplied out of address order.

Research ARM9 SHA-256: `d937be33b97b654038d03f1aed57ae30a2a49e0afce7d96ae1e2c972c1b758b3`. No ROM is written.
Tool: `compile_map_creature_allocation.py`; report and proposed ARM9 are in
`work/analysis/map_creature_complete_v139/`.

Actual native construction/name lookup passes for all 39 classes, now including
Monster Fish, Giant Squid, Shark and Whale. All 39 class strings flow through native
printf into the actual tooltip renderer with four odd/even category/name variants
and both pixel formats: 312 complete glyph/row/full-buffer comparisons pass.
`probe_map_creature_complete.py` also replays eight title, six footer and two modal
rasters against V139, preserving text/centering/geometry/metadata/pixels exactly.
Zero/nonzero dispatch at 0/1/2/255 passes. All 164 inherited caption pointers and
complete text/NUL are unchanged. Four native entity-selection branches also pass.
Seventy-one targeted allocation/class/tooltip/Golden Route/ownership regressions
and Ruff pass.

Evidence: `native_complete_proof.json` in the same directory. Formatting approval
and release integration remain pending dynamic faction/user-name/numeric bounds,
remaining presentation contracts and physical routing/gameplay. These tests cover
all static classes; they do not establish full dynamic-name coverage. Previous
creature storage-shortfall notes below are superseded by the complete allocation.
V139 remains the latest candidate, and the full translation goal remains active.

## All 39 native tooltip classes mapped; four creature names localized

Clean source bounds the class table at 39 entries. Table 11C7A8 has 56-byte source
records; runtime class objects use 64 bytes at the CB154 base plus four. Actual
CD3D0 construction, ABEC0 native index arithmetic, CD474 source selection, the
complete class vtable and 1FD74 name getter execute for every index 0-38. All
constructed name pointers/NUL text match the saved V139 table, and every stack/
adjacent-object guard survives. No entity/name lookup was substituted in this proof.

The audit found four still-Japanese names at indices 34-37. The new
`translations/map_creature_class_manuscript_v2.json` localizes them fully as
Monster Fish (化魚), Giant Squid (大イカ), Shark (サメ), and Whale (鯨). Source,
context, localization and naturalness reviews pass; formatting remains false.
The monster and giant qualifiers are retained. Older class abbreviations still
belong to the broader fidelity review.

Their four verified source slots own 28 bytes; full English plus NUL needs 37.
The longest complete string needs 13 bytes, exceeding each original slot. Existing
complete Whale at 15BB90 and Shark at 15CB59 were found in V139; any later sharing
must lock their full bytes/NUL and retain their current storage. Remaining slot
geometry requires relocation, not shortened wording or unverified padding.

Evidence: `work/analysis/map_entity_tooltips_v139/all_class_initializer_proof.json`.
Tool: `inventory_map_tooltip_classes.py`. Twenty-nine combined inventory/tooltip
regressions and Ruff pass, including source count boundaries, wrong vtable access
and native writes into an adjacent class object.

Next: allocate all four full creature names, extend native formatting to all 39
classes, and finish dynamic faction/user-name and numeric bounds plus parent
geometry/routing. Existing tooltip guard and pixel proof remain intact. No ROM or
COMMON translation count changed; V139 is current and the goal remains active.

## Native map tooltip newline repair and pixel proof

The first raster execution disproved copy-only formatting approval: an odd-length
first row drew the next row's first glyph on the preceding row. A single LF-space
guard fixed that case but caused the first two second-row letters to overlap for
an even-length preceding row. Both failures are recorded in
`work/analysis/map_entity_tooltips_v139/newline_defect_evidence.json`.

`formatted_text` now generates two blanks after each native tooltip newline.
Editorial English stays unchanged. Actual renderer execution places every second-
row character correctly with a consistent six-pixel continuation indent for both
parities. Native font, tracking, renderer code and tooltip geometry remain unchanged.
Full allocation shares the exact existing Monster string at 17223D under the full
V139 input hash and complete text/NUL check. Its storage is retained. The two source-
owned pools use 51/56 bytes, with five spare; all five full labels/formats survive.
Research ARM9 SHA-256: `9c7be5ee8cdbd8c8e15998733d4cb62fbf78b4aca01094036332546a0212dff8`.

Actual 763C tooltip measurement (77FC/CF220/CF348), font/context initialization,
D5404/D16B4 pixels and D5140 cleanup execute. Thirty-four full-buffer comparisons
cover odd/even names, all new category labels, representative faction/ship-class
names, percentages and over-width printf values in both native pixel formats.
Separate native printf copies retain complete arguments, first/last bytes, NUL,
stack and output guards. Sixty combined map/caption/footer/modal tests and Ruff
pass, including regressions for the original dropped-leading-glyph and single-
guard overlap defects. Existing helper defaults retain passing compatibility.

Evidence: `native_raster_proof.json` and `native_copy_proof.json` in the same
research directory. `probe_map_entity_tooltip_raster.py` independently computes
full glyph order/positions and exact-font pixels; the proposal hash is locked.

Remaining: exhaustive dynamic faction/name/ship-class/percentage bounds and mixed
CP932 presentation, parent placement/construction and physical routing. Parent UI
state update, bitmap validity/clear/composition, origin and eleven-byte glyph copy
remain explicit contracts. Formatting reviews remain false and no ROM is built;
V139 remains the latest candidate. Earlier tooltip sizing/copy-only notes below
are superseded by this guarded allocation and full representative pixel evidence.

## Map entity tooltip localization research on V139

Five additional source strings are fully localized: Pirates, Monster, ???,
`%s\n%s class`, and `%s  %6s%%\nArmament %8s`. All entity/name/class/percentage/
armament meaning and printf substitutions survive; the original two tooltip rows
are retained. Native ASCII percent requires %% in the format string.

Exact source/padding checks against clean, canonical and V139 lock all five fields
and every byte-position literal into both pools. Lossless packing uses 55 of 56
owned bytes across 1190EC:119104 and 1478B8:1478D8. Only those bytes and five literal
fields change. Consumer and native printf code remain unchanged.

Actual 70424:70470 selection executes all four branches: special monster type,
missing faction/pirates, unidentified faction and dynamically named faction.
Entity resolver and virtual-name lookup remain explicit external contracts.
D7720/D7754/D7950 execute six complete native format copies with original stack
arguments. First/last bytes, NUL, stack and bounded output guards pass. Twelve
regressions additionally cover CP932 class bytes, over-width printf substitutions,
leading-character mutation, extra interior consumers and source-padding mutation.
Ruff passes.

Scripts: `prepare_map_entity_tooltips.py`, `execute_map_entity_tooltip_copy.py`.
Manuscript: `translations/map_entity_tooltip_manuscript_v2.json`.
Evidence: `work/analysis/map_entity_tooltips_v139/report.json` and
`native_copy_proof.json`. Research ARM9 SHA-256: `e7a389994589969f95a3782c918f04ac02298bb4088c24a8523f02b7f89743c1`.

All five formatting reviews remain false pending actual tooltip renderer/pixels,
dynamic maximum names/classes/values, geometry and physical routing. No ROM or
COMMON count changed; V139 remains the latest candidate. This is progress toward
remaining ARM9/UI localization, not release approval.

## Current Golden Route status: V139

All six viewer labels are integrated with approved native formatting in V139.
Saved-ROM/native heading/footer/empty-message consumers and patch roundtrip pass;
all V138 components except the owned ARM9 labels/pointers remain byte-exact.
Full glyph/leading-character proofs cover both pixel formats. Parent geometry,
constructed bitmap/origin contracts, physical routing and gameplay remain pending.
See `translation_progress.md` for hashes and `golden_route_viewer_release_v1.json`
for strict source/evidence gates. Earlier pending/research notes below are historical.

## Golden Route viewer localization research on V138

Six clean-source fields remain Japanese in V138:

| Source offset | Japanese | Complete English | Literal consumer |
| --- | --- | --- | --- |
| 16A1A0 | 前へ | Previous | 12EC28 |
| 16A1A8 | 次へ | Next | 12EC2C |
| 16A1B8 | 切り替え | Switch | 12EC4C |
| 16A1C4 | 黄金航路発見！ | Golden Route Found! | 16A1B0 |
| 16A1D4 | 黄金航路の記録 | Golden Route Records | 16A1B4 |
| 16AF7C | 黄金航路の記録は有りません | No Golden Route records. | F14D8 |

`prepare_golden_route_viewer.py` verifies all original text/NUL/padding against
clean, canonical and V138 ARM9. Owned spans exclude the intervening title pointer
array and following RTTI strings. Every byte-position literal into the spans is
exactly one of these six consumers. The complete canonical Next at 11B53C and
Switch at 14C114 are reused under exact byte/NUL checks; their slots are retained.
Four allocated labels use seventy-five of eighty-eight owned bytes; thirteen are
spare. All changed bytes belong to source spans or the six pointer fields.

F2BFC:F2C40 selects the two headings via table16A1B0, measures actual full bytes
with CED28, centers at `128 - strlen * 3`, and calls D5200. Actual CE898 formatting
copies full text/NUL to its native buffer; D5404 consumes the result. Native
execution gives X71 for Found and X68 for Records. Eight separately connected
native glyph/pixel cases (two headings, Y0/Y12, two pixel formats) preserve complete
glyphs and ordinary paired flush behavior. Parent Y is a parameterized contract;
physical screen routing is not yet proven.

Footer labels enter CA890 through descriptor tables, then CA780. CA780 computes
width `floor(strlen / 2) * 12`; the English lengths 8/4/6 are even and therefore
match six-pixel widths 48/24/36. It draws through a local D5160/D5404 context.
Full footer transfer/placement/raster remains pending. The empty message follows
F0B70 DB4F4(type3); if the record count is zero, F0B80 loads F14D8 and F0B84 calls
5473C, whose actual format-copy routine is 54774. It needs a separate modal-dialog
layout/leading-character proof. It is not the heading consumer.

All six editorial source/context/localization/naturalness gates pass in
`translations/golden_route_viewer_manuscript_v2.json`; native formatting remains
false. Nine mutation/native tests and Ruff pass. Research proposal/proof:
`work/analysis/golden_route_viewer_complete_v138/` and
`work/analysis/golden_route_heading_v138_proof.json`; proposal SHA-256
`9a4b950d452631a6cc60721177e1f8e2b1ad778d854b6e42b11df04fdb2828a5`.
No ROM, release acceptance or integrated count changed.

## Broader inventory on V133

The old scan began at `0x110000`, required two Japanese characters, searched
only 64 bytes for NUL, and rejected multiline text. It reports 920 candidates,
many of which are binary/font data. Its count is not a remaining UI count.

`inventory_arm9_text.py` scans the entire ARM9 and its one overlay, retaining
NUL-bounded text and control-bounded printable CP932 islands. It also reports
single-character and halfwidth-kana candidates, long strings, unterminated
tails, source/current span bytes, profile ownership and aligned address words
pointing to starts or interiors. Known ASCII glyph data is classified only
when its exact font hash matches; it remains visible in the inventory.

| V133 inventory measure | Count |
| --- | ---: |
| Candidates, including binary decodes | 81,411 |
| ARM9 / overlay candidates | 81,094 / 317 |
| Candidates with aligned address references | 1,694 |
| Single Japanese-character candidates | 66,277 |
| Strings longer than 64 bytes | 9 |
| Candidates before the old scan's start | 64,680 |
| Verified native ASCII font-data candidates | 36 |
| Referenced NUL-bounded pool candidates queued for review | 834 |

These are classification queues, **not untranslated UI counts**. Instruction
bytes and other binary values can decode as Japanese; a pointer-like word
also does not prove display use. Fixed fields, control grammars, generated
strings and compressed text still need separate coverage. Raster graphics
are outside this scanner. No broad completion or unused-text claim is made.

Independent coverage checks retain all 920 old candidates and verify the
nine newly recovered race-help bodies against unchanged clean-source bytes.
Six tests cover early/single-character strings, long/multiline text,
halfwidth kana, binary-prefixed islands, invalid/ASCII input and interior
pointer references. All six tests and new-tool Ruff checks pass.

Evidence: `work/analysis/arm9_text_inventory_v133.json`,
`arm9_text_inventory_v133_coverage_proof.json`, and
`arm9_text_inventory_v133_reference_priority.json`.

## Nine complete Grand Race source translations

Each help descriptor pairs a title pointer with a body pointer. Their bytes
and all nine original bodies are locked to the clean ROM and unchanged V133.
The manuscript preserves all instructions as natural English paragraphs:

| Topic | Body offset | Original bytes including NUL | Draft English bytes including NUL |
| --- | --- | ---: | ---: |
| Time limit | `0x137F74` | 207 | 174 |
| Your ship | `0x137EAC` | 200 | 205 |
| Supplies | `0x137C90` | 165 | 212 |
| Map | `0x138168` | 300 | 293 |
| About Grand Race | `0x137DF0` | 188 | 146 |
| Race area | `0x137BF4` | 153 | 140 |
| Basic rules | `0x138044` | 292 | 267 |
| Prizes | `0x137B90` | 100 | 124 |
| Stopping a race | `0x137D38` | 182 | 168 |

The source mechanics retained include four sea regions, up to four players,
host/join roles, Touch Screen control rather than the D-pad, all seven
checkpoints in any order, finishing first, continuation until everyone
finishes, food and barrel indicator location, slowdown at zero food, supply
points, player colors in join order, G/red/light-blue map markers, passed
checkpoint removal, flagship selection from save data, basic performance
without equipment/crew/item effects, placing-based prizes added to save money,
disqualification without a prize, void races if no one finishes in time,
and one powered-off system stopping the race for everyone.

`translations/grand_race_rules_manuscript_v2.json` now has all five review gates
complete for all nine pages. The V134 profile integrates its complete formatted
bodies and eight English headings. The earlier research sections below describe
the mapping and allocation that preceded integration; the current release status
is recorded at the end of this document. No source mechanics were shortened.

## Allocation research, not presentation approval

The nine complete original strings occupy `0x137B90–0x138294` with only zero
padding between them. A research plan repacks all nine complete English
paragraphs in this same 1,796-byte region, updates their nine body pointers,
preserves ARM9 size and every unrelated byte, and independently reads all nine
new selections through those pointers. Paragraphs/alignment use 1,737 bytes,
leaving 59 bytes **before actual safe formatting is applied**.

This initial allocation removes the individual-slot shortfall without
shortening meaning. It is an unformatted research component, not a playable
ROM. The subsequent formatted allocation is documented below.

Evidence: `work/analysis/grand_race_rules_repack/plan.json`.

## Native help consumer mapping

The initial draw (`0x3F190`), direct page selection (`0x3E8E8`) and previous/next
navigation (`0x3F51C`) use the same group table at `0x115334`. Its four
pointer/count pairs select all nine descriptors exactly:

| Group | Pointer list | Count | Descriptor order |
| --- | --- | ---: | --- |
| 0 | `0x1152A8` | 1 | `0x1152CC` |
| 1 | `0x11530C` | 4 | `0x1152DC`, `0x1152B4`, `0x1152D4`, `0x1152EC` |
| 2 | `0x1152E4` | 2 | `0x1152C4`, `0x1152BC` |
| 3 | `0x115304` | 2 | `0x1152AC`, `0x1152FC` |

Each path creates a context with `0x020D5160`, draws the title through the
descriptor's first pointer, sets the body cursor to `(0, 12)`, draws the
descriptor's second pointer through `0x020D5404`, then destroys the context.
All aligned ARM9 address words into the original body region are exactly
the nine descriptor body fields. This covers aligned pointer words, not
every possible generated, unaligned, overlay or indirect reference grammar.

`verify_grand_race_help_consumers.py` verifies the groups, selections, bodies,
18 branch targets and 18 code/context spans against V133 and the exact
canonical accepted baseline. These checks pass. The shared renderer differs
from clean Japanese because it already contains the accepted newline/cursor
repair; its V133 bytes match the canonical baseline. A clean-only renderer
lock would incorrectly reject that inherited repair.

The ASCII path in `0x020D5404` processes one byte at a time, but the context
glyph backend at `0x020D4DA8` queues the first ASCII byte and flushes a pair
on the next call. `0x020D596C` moves the cursor without flushing that queue.
The inherited repair handles the guarded newline cursor. An English formatter
must preserve safe pair phase as well as width; bare word-wrapped ASCII is
not formatting approval. The existing protected-break codec is used in the
research page formatter, with an independent pair-buffer/cursor model.

Evidence: `work/analysis/grand_race_help_consumer_proof.json`,
`grand_race_help_consumers.txt`, `grand_race_help_renderer.txt`, and
`grand_race_help_context_and_glyph.txt`. At this mapping checkpoint no ROM/profile
was created; formatting and integration followed as documented below.

## Complete formatted pages and allocation proof

Native startup at `0x5CA8–0x5CC8` sets the shared font metrics to 6 pixels
per ASCII character and 12 pixels per line. `0x10E12C` constructs that same
font object at runtime address `0x02312098`. The help setup passes width 252
and height 108 through `0x3EA38`, the widget's virtual method `0xD43B0`, and
dimension assignment `0xD3A1C`. `0xD4A7C–0xD4B84` obtains the local bounds
from those dimensions. These code spans are source-locked to the accepted
baseline and V133. With the body starting at y=12, eight body rows fit.

`format_grand_race_help.py` uses automatic balanced wrapping and the established
protected-break codec. It independently models ASCII buffering, guarded LF
cursor reset and the final pair flush. It checks every non-space character's
exact position against each complete line. All nine full paragraphs fit;
the largest page uses eight lines. All nine exact-font panels were viewed
as a complete contact sheet. No dropped start, clipped final row, shortened
paragraph or invented alignment was found. Draft headings are shown for review;
they have not yet been inserted.

The four-byte-aligned research allocation fails after safe formatting:
it needs 1,812 bytes, exceeding the 1,796-byte region. Byte-packed strings
use 1,794 bytes, leaving two bytes. This preserves every complete formatted
body, all nine NULs and the region's original bounds. The descriptor pointer
fields remain aligned; `0xD5404` reads body characters using byte loads, so
the character strings themselves do not require word alignment. The saved
research component independently selects all nine exact formatted bodies,
keeps ARM9 size, and changes only the region and nine pointer fields.

Six targeted tests pass. They check complete prose and safe break phase,
demonstrate the character loss/overwriting from bare or unsafe-phase guards,
verify the protected continuation start, and reject overflow and authored
line breaks. Changed tools pass Ruff. This is static and exact-font research;
this research checkpoint preceded the playable build enforcement, title-slot
locks and saved-ROM verification documented below. Live page/navigation checks
remain pending.

Evidence: `work/qa/grand_race_help/report.json`, `sheet.png`,
`work/analysis/grand_race_rules_formatted_repack/plan.json`,
`grand_race_help_widget_setup.txt`, `grand_race_help_window_bounds.txt`,
and `grand_race_help_font_initialization.txt`.

## Integrated experimental V134

`all-routes-unified-v134` now includes `grand_race_help_arm9_v2.json` on the
complete V133 stack (430 batches). Candidate
`out/all_routes_combined_v134_candidate.nds` has SHA-256
`6af0f04f94538daa6cab58062c62e9dff578041da1f0b9ccf84b0b2fedcada9f`.
All nine body pages and eight headings are translated; the inherited Map heading
is byte-exact. Longer headings use verified original zero padding: Time Limit,
Basic Rules and Stopping a Race fit 12/12/16-byte slots. About the Race fits its
16-byte padded slot and retains the original heading's meaning.

The builder regenerates all 18 patch spans from the reviewed manuscript,
rejecting missing gates/pages, stale formatted bytes, altered body pointers,
incorrect source ownership and unrelated heading data. It locks 18 mapped
consumer/font/geometry spans. The complete COMMON transform is inherited
using a reconstructed V119 input containing both V133 captions and the help
layer; no existing route/shared/UI/graphics layer is lost.

Independent saved proof verifies all nine title/body selections, full prose,
every visible character position and all region boundaries. Every V133 file
and component remains byte-exact except the 18 declared ARM9 data spans;
all 3,668 COMMON selections, executable code, fonts and page-group tables
are unchanged. All 97 release/targeted tests, changed-tool Ruff and
map/item/sound/integrity/baseline/manifest verifiers pass. No cold-boot
acceptance or baseline promotion. Check all four help groups and previous/next
navigation, particularly the eight-line Map page and first/last characters.

Saved proof: `work/analysis/grand_race_help_v134_saved_proof.json`.
See `docs/remaining_translation_checkpoint.md` for the full handoff evidence
and remaining project goal.

## Other concrete review leads

- Japanese Golden Route headings at `0x16A1C4` and `0x16A1D4` are selected
  through the table at `0x16A1B0`, referenced by `0xF2D04`. The routine near
  `0xF2C00` centers by byte length times six and calls `0x020D5200`.
  `0x020D5200` formats through `0x020D5234`, then calls `0x020D5404`.
  This wrapper identity alone does not establish the local context's layout.
- The Japanese empty-record text at `0x16AF7C` has an aligned address word at
  `0xF14D8`; its precise consumer still needs tracing. Do not treat nearby
  disassembly as proof that a particular PC-relative load uses that word.
- Scene/artwork names recur in the ARM9 pool beginning around `0x13894C`.
  Some references point into a candidate span rather than its beginning.
  For example, the pointer at `0x115CAC` targets `0x13898C`, inside the
  candidate span beginning `0x138984` (`Ironclad港町１`). Fixed-field boundaries
  and actual consumers must be resolved before interpreting such spans as
  complete displayed strings or replacing them.

Research disassembly: `work/analysis/golden_route_ui_consumer_candidates.txt`
and `golden_route_ui_fixed_renderer.txt`. These files contain candidate code
and data; executable-looking data words are not caller evidence.

## Remaining race menus and wireless widgets: V134 research

V134 remains unchanged. Six remaining Japanese main/category labels have exact
aligned text references in the 16-byte menu entries at `0x115354` onward.
The main menu caller at `0x3E468` supplies the first two entries to `0x51F4C`;
the rules menu caller at `0x3E568` supplies four entries starting at `0x1153A4`.
The wrapper creates a selector with vtable `0x14062C`. Its string accessor
`0x51E0C` fetches the selected entry's first word through `0x51DF8`.

The selector at `0x52078` measures each enabled string through `0xCF348`.
This routine counts one unit for an ASCII byte and two for a CP932 pair;
it stops at NUL or LF. Selector geometry multiplies the maximum count by the
six-pixel metric at `0x116440`. Per-button geometry uses margins `(0, 4)` from
`0x116438`, twelve-pixel text height and the centered parent rectangle.
The button constructor `0xACBEC` copies text through `0xACC64`: at most 48
bytes, followed by NUL, into the field at object offset `0x68`. All proposed
complete English labels are shorter than this limit. The final button draw
path and inherited UI overlap/padding locks still need verification before
release. These are consumer findings, not a visual acceptance claim.

Wireless widget drawing is separate. `0xFB494` invokes `0xD1604`, which reads
the first source byte before entering its draw loop. ASCII is drawn immediately
through `0xD16B4`, advancing six pixels; CP932 pairs advance twelve pixels.
This routine does not process LF as a layout break and does not use the story
renderer’s deferred two-ASCII buffer. Full wireless instructions are split
across line widgets; their order, coordinates and complete source meaning must
be reconstructed before generating English layout. Do not reuse the story
protected-break encoding for this renderer.

Evidence in `work/analysis/`:
`grand_race_remaining_ui_v134_source.json`,
`grand_race_remaining_ui_widget_followup.txt`,
`grand_race_remaining_ui_widget_draw.txt`,
`grand_race_remaining_ui_menu_text.txt`, and
`grand_race_remaining_ui_ascii_draw.txt`.

Some disassembly spans include literal pools and vtable metadata. Only traced
instructions and resolved loads support the findings above; data words that
decode as ARM instructions do not establish additional consumers.

### Complete wireless manuscript and error-return layout

`translations/grand_race_remaining_ui_manuscript_v2.json` now covers all 46
source parts in this remaining referenced race queue as 38 complete logical
messages. Multiple source fragments are joined in reading order before
localization. Full meanings retain one host only, all-player confirmation,
host area selection, four exact prizes/player numbers, capacity failure,
registration closure and both touch/A Button controls. Host/Join describe
wireless roles; no family relationship is invented. Prose is independently
reviewed for source, localization and naturalness. General context/formatting
gates remain open until each caller and screen is mapped. No release count or
candidate was changed. The preparer pins clean, canonical and V134 hashes and
checks all original text, NULs, alignment padding and aligned pointer fields.

The error-return sentence has a completed narrower static proof through its
actual derived text-widget table `0x16B290`. The initial abstract table at
`0x16BADC` is overwritten; it is not the callable table. Constructor `0xFB004`
copies x/y, text pointer and style into the object. Draw method `0xF37D8` calls
`0xD1604` directly at `0xF3818`. Three resolved PC-relative text loads select
the original starts `0x16B93C`, `0x16B954`, `0x16B968`; their geometry pointers
select `(16,16)`, `(16,32)`, `(16,48)`. Eight code/context spans are byte-exact
between clean Japanese, canonical and V134. The only aligned references into
the contiguous 68-byte source region are those three literal fields.

`scripts/probe_grand_race_wireless_return.py` automatically balances the full
paragraph into three NUL-terminated strings. The formatted English uses all
68 bytes of the shared region and moves its three pointers within that region.
Every selected byte and six-pixel glyph position is checked. The exact-font
preview was reviewed: all three lines are natural, with intact first/last
characters and ample display width. No LF or story pair guard is used. This is
a research allocation/preview proof; integration enforcement, saved-ROM proof
and runtime still remain. Evidence: `work/qa/grand_race_wireless_return/report.json`
and `preview.png`, plus `grand_race_wireless_text_widget_v134.txt`.

### Expanded race source queue and four-line role instructions

Further caller tracing found eleven additional source strings: four finishing
positions, four short player identifiers, the host area-selection heading,
role-selection heading and unoccupied-player status. The manuscript now covers
57 source parts as 49 complete logical messages. The earlier 46-part queue was
incomplete; it must not be reused as the complete race UI source set.

The broad scanner's `isprintable()` filter rejected the ideographic space in
`親機　ステージ選択` at `0x16B9E0`, hiding a valid referenced heading. It also
excluded full-width player labels containing no kana/kanji. Both omissions are
fixed: U+3000 is retained as display whitespace, and full-width Latin/digits/
symbols are separately counted as candidates without claiming they are Japanese
words. Full-width-only labels are not mislabeled as half-width-kana-only.
Three new real coverage regression tests pass; all nine inventory tests pass.

The refreshed V134 ARM9/overlay inventory reports 81,507 candidates, including
164 with full-width characters and 48 with ideographic spaces. There are 1,782
candidates with aligned address references and 26 longer than 64 bytes. These
counts include binary decodes, remain unclassified, and are not a UI backlog
or translation percentage. The scoped reconciliation verifies every one of the
57 manuscript source parts and its exact start reference in this inventory.
Evidence: `work/analysis/arm9_text_inventory_v134_expanded.json` and
`grand_race_ui_v134_expanded_coverage.json`.

The role-instruction table at `0x12EDFC` is now traced through the loop at
`0xFA274`: four calls to constructor `0xFB004`, style 1, x=16 and y=64/80/96/112.
The geometry comes from `0x12ED14`; the caller advances each row by 16 pixels.
Nine accepted/source/current code-context spans are exact. The complete paragraph
is automatically balanced into four independently positioned ASCII strings,
respecting source-owned alignment padding and native six-pixel glyph width.
Every word, first/last character and line bound is checked; the exact-font
preview has been reviewed. Original text pointers can stay unchanged for this
paragraph. It remains research, with release enforcement and runtime pending.
Evidence: `scripts/probe_grand_race_wireless_roles.py` and
`work/qa/grand_race_wireless_roles/report.json` / `preview.png`.

Across all 49 logical drafts, the unformatted English currently totals 1,123
bytes including NULs, while reviewed original strings plus four-byte alignment
padding total 1,112 bytes. Individual fitting prompts do not prove a complete
pool allocation; final allocation/relocation must retain all meanings rather
than shorten drafts simply to satisfy these old slots. Remaining screen geometry,
selection grammar and pool ownership must still be resolved. V134 is unchanged.

### Whole referenced-pool reconciliation and additional screens

The refreshed scanner also finds two further headings containing ideographic
spaces: `子機　ステージ決定` at `0x16B990` and `親機　ゲームに移行します` at
`0x16BA08`. Both have fresh full-meaning English; the manuscript now has 51
logical messages / 59 source parts. The reusable verifier
`scripts/verify_grand_race_ui_source_coverage.py` reconciles all 59 parts and
exact aligned start references. It also audits the entire referenced NUL-bounded
wireless range, retaining three explicit other leads at `0x16AFD0`, `0x16B482`
and `0x16B688` for consumer classification. They are not declared unused.
An independent clean-Japanese scan finds the same three other leads, so existing
English did not hide another referenced Japanese entry in this scoped range.
Fixed fields, interior references and other reference grammars remain limits.

`scripts/probe_grand_race_wireless_screens.py` traces four actual source-table
and geometry loads, constructor loops, row counts/strides and title selections.
All corresponding code/context spans are exact in clean, canonical and V134.
The title constructor `0xFAED4` centers by byte length times six, starts at y=2
and constructs the derived native text widget. Body widgets start at x=16/y=64
and advance by 16 pixels. The exact-font search, host waiting-room and host
area-choice text previews have been reviewed; complete leading/trailing text
and all lower-screen/A Button/Confirm conditions survive.

The joining-device waiting-for-area screen uses exactly two body widgets via
table `0x12ECEC`, constructor call `0xF85AC`. Its complete English paragraph
cannot be split into two word-boundary lines of at most 40 cells. This is an
explicit presentation blocker: gain a third line or provide another independently
proven display method. The complete prose is retained. The preview omits the
blocked body and marks the screen as blocked; it must not be counted as reviewed
or integrated. Eight new formatter regressions verify this real overflow,
complete return-prompt controls and fail-closed authored spacing/controls.
All 17 inventory/layout tests and changed-tool Ruff pass.

Current source-owned strings plus alignment padding total 1,160 bytes; the full
51 English messages need 1,175 bytes including NULs before final storage planning.
Exact existing `Grand Race`, `Basic Rules` and `About the Race` strings were found
as potential sharing leads. Their ownership/profile dependencies must be locked
before sharing; title sharing is not yet an allocation or release proof.
Evidence: `work/qa/grand_race_wireless_screens/report.json` and `sheet.png`,
`work/analysis/grand_race_wireless_remaining_layout_v134.txt`,
`grand_race_ui_existing_title_aliases.json` and the refreshed expanded coverage
report. Return/role proofs were refreshed against the 59-part manuscript with
unchanged reviewed English. V134 remains unchanged.
