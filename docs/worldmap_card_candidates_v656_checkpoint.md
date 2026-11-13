# V656: classify the16 remaining WorldMap village-card byte candidates

The previous goal turn made progress through V655's five complete tooltip/banner
compositions and native first/final-letter controls. This checkpoint follows the
remaining positive source-search lead for the eight village-caption cards. It
does not change artwork, ROM, patch, registry or any release pointer.

## Question

V589 searched script/shared/event/test containers at every byte position. The only
remaining16 village-card-like patterns were inside `/data/WORLDMAP.DK4`. That
proof correctly retained them as byte candidates, not decoded script instructions.
This turn maps every candidate to the original typed reader and compressed page.

## Complete source layout

The whole archive is byte-exact between clean and current V653. Its ten ILNK
blocks each begin with250 four-byte terrain-page headers:2500 declared pages.
Each header contains either an offset/length pair for a compressed page or the
original FFFF uniform-page marker.

All1037 compressed streams exactly partition their blocks' payload bytes after
the1000-byte header tables. Only0–3 final alignment bytes remain per block. All16
four-byte candidate patterns lie wholly inside exactly one compressed stream
each. None crosses a stream boundary or belongs to an instruction record/header.
The full ownership table, page coordinates and source bytes are retained.

## Original filename, selector and decompressor

Original0206E578 executes its real archive constructor and stores each supplied
block index. At the original Open boundary it passes `\DATA\WORLDMAP.DK4`.
Twenty clean/current prefix cases cover all ten block indices. They deliberately
stop before Open; filesystem success or actual device loading is not claimed.

Original0206E530 selects the exact header for each declared page coordinate.
Original overlay01FFA10C then decodes a complete50x25-word terrain page. Its
compressed branch calls the original resident ITCM decompressor01FF8000; its
uniform branch constructs the complete1250-word tile-variation pattern.

Twenty-six unique pages are exercised: all16 candidate-owning pages plus one
uniform control per block. Both clean and current execute each complete native
decode:52 calls. Every2500-byte result, input-read event, source byte, coordinate,
descriptor, neighboring guard and saved-register/stack ABI matches. The ten
uniform outputs additionally match an independent complete1250-word model.

All64 candidate bytes are actually read by the compressed-input reader at native
01FF8058,01FF8084,01FF822C or01FF8244. These are flag/literal/bit-input reads.
No script dispatcher, event-still parent or filename loader executes in these
decode paths. Relevant original main, overlay and decompressor instructions
remain exact between clean and current ROMs.

## Result and limits

The16 byte matches do not establish any village-card trigger in the analyzed
WorldMap reader. They are compressed terrain input, not evidence of a script
record. This removes that concrete false lead from the next investigation.

Loaded block buffers and valid page coordinates are explicit isolated native
contracts. There is no new emulator run, ordinary event trigger, screenshot,
GPU/display or guide credit. This is not global unused-art proof: computed or
other filename paths and generated script inputs remain unproven. The eight
caption cards' translated planes, preservation and supplied native display
evidence remain valid, with ordinary reachability still open.

## Evidence and unchanged goal

- Script: `scripts/trace_worldmap_card_candidates_v656.py`; targeted Ruff passes.
- Proof: `work/analysis/worldmap_card_candidates_v656/proof.json`.
- Archive:
  `E:/Rota Nova translations/Screenshots/Test fixtures/V656 Terrain byte candidates`.
- Current ROM remains `out/all_routes_combined_v653_candidate.nds`, SHA256
  `c4e9c4faf18c212e5b6572d61e6b2821493f38bbc1dc89d601b37b16058b3ade`.

No V656 ROM, canonical promotion, commit or push is created. All18 original
plaque/hint entries remain incomplete and all22 historical scope objects remain
exact. The full graphics goal stays active. Other actual control/card/legacy/art,
material/transition/gameplay and final-acceptance gates remain open. User exclusions
for the four low-resolution Online screenshots and preservation of the brown
comic marks remain in force. Older record-based checks remain due at actual
full-goal completion.
