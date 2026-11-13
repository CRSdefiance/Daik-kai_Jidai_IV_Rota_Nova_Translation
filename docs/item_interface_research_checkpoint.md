# Item interface: natural English and native column research

**Historical six-label fixture phase.** Superseded by the
[complete labels and paragraph research](item_interface_complete_labels_research.md).
The counts, allocation, target hash and local proof below describe the earlier
research image and do not approve the current paragraph helpers or real resources.

The full translation goal is active. **V158 remains the latest experimental
combined ROM.** This item work is a disposable ARM9 research image, not a
registered playable candidate or an integrated translation count.

## Source review and confirmed layout defects

Six logical records cover eight clean-source pointer fields:

| Logical English | Native fields | Current evidence |
| --- | --- | --- |
| Items Acquired %d/%d | 451E0 | Native counter, every count 0–198 |
| Advice | 45664, 4D254 | Conditional menu descriptors; actual command consumer pending |
| Effect | 4D864, 4E530 | Both native item-detail draw functions |
| Equipped By | 4D86C | Native equipped-person branch, provider fixtures |
| Use | 4D874 | Mapped branch leaves name null and skips heading; no visible-use credit |
| Equipped Ship | 4D884 | Native equipped-ship branch, provider fixtures |

English is faithful, natural en-US and unpositioned. The counter compiler retains
the native three-character numeric fields; the caller supplies total 198.
Ordinary compiled labels receive a final machine space only when their native
ASCII pair length is odd. Both original Japanese storage and every pointer owner
are source-locked; scans include complete/interior owners in loaded sections and
overlay 0.

Complete English reveals two real spacing hazards. **Effect** spans x104–140,
overlapping original value columns x134/x132. Research moves both values to x144.
Equipped-person/ship headings and names share y24, rather than separate rows.
**Equipped Ship** spans x0–84, overlapping the original name at x48. Research
moves the common name/value column to x88. That also moves the separate price
value, leaving its label unchanged. Negative native tests restore the original
columns and reject actual overlapping glyph cells.

An initial concern about a lost Price placeholder was disproved: source 価格 is
only a label. The value uses its own `%6d` template at 4D880 and actual rotating
formatter 020ABFCC → 020CE898. Both label and six-digit fixture price survive.
The centered native detail title is the existing **Items** at 4D260, not Advice.
Advice is a separate conditional menu command; its consumer must still be traced.

## Native rendering and allocation evidence

506 paired 4/16-bit cases cover every acquired count, six effect values
(0,1,9,99,100,255), seven owner kinds, both standalone advice flags, and the
person/ship/price branches. Native unsigned-byte property getters, index division,
printf, context setup, glyph painting and cleanup execute. Whole code vectors,
independently decoded ASCII/CP932 pixels, synthetic final space cells, nonoverlap,
144×36/240×96 view bounds, registers, stack and pixel guards pass. Eleven
representative previews cover count boundaries and complete headings/values.
All eleven were visually inspected at uniform scale. Four visible logical
records have local formatting review; the separate Advice and nonvisible Use
records retain failed/pending formatting gates. The local review does not
approve resource providers, full parent composition or playable integration.

The separate native constructor proof executes 020D3D80 and 0204D8A0. It creates
a 240×96 4-bit source with header owner+2D70 and backing pixels owner+70–2D70
(11520 bytes). Actual 020D393C and overlay 01FFB2DC clear an A5-seeded canvas;
object canaries survive. Shared native draw method 020CFDE8 → 020D4170 emits
the complete 240×96 source at GPU boundary 01FF92D8. Layer 1 and destination
(0,0) are supplied dispatch fixtures. **This does not prove the upstream parent
draw, clipping, artwork or hardware GPU output.** Widget registration is a
success contract. Initial probe failures exposed a missing bitmap constructor
and incorrect shared-draw argument order; both were corrected without mocking
clear or draw output. No playable ROM was affected.

The research image preserves the complete V158 3584-byte pool prefix. Text
extends it to 3680 bytes (3654 used), staged at 023A7200 and copied to 02387A20.
Copy entry is 023A8060, staging ends at 023A8090 and main arena low is 02388880.
ITCM remains 8172 bytes, ending 01FF9FEC; aligned low 01FFA000 stays at the overlay
boundary. No new helper is added. Native SDK autoload/BSS, ARM7 source/loaded
sections, late copy, stack/registers and arena ownership pass. All other source
code/data and inherited helpers/pool bytes are preserved by the transform.

The 61-test focused suite passes: five new native overlap/first-letter tests
plus 56 inherited Gallery, duel, movement and caption regressions. The five new
tests pass again with the corrected Items title. Changed-tool lint passes.

## Required before integration

- Trace the actual Advice command consumers and both registered menu descriptors.
- Classify the nonvisible Use branch; do not count referenced storage as visible text.
- Execute real item/crew/ship/name/description/advice providers and measure every
  real owner name at x88. Current providers and ownership selections are fixtures.
- Prove the Gallery counter source image initialization and complete parent
  views, clipping and artwork. Direct shared dispatch alone is insufficient.
- Refresh inherited consumers/pixels against the final research image, lock
  reviewed prose/previews/evidence, register a complete release profile, build
  once from the canonical stack, and verify manifest/components/baseline/patch.
- Physical cold boot/gameplay remain pending.

Research files: `work/analysis/item_interface_research_arm9.bin`,
`work/analysis/item_interface_plan.json`,
`work/analysis/item_interface_native_proof.json`, and
`work/qa/item_interface_native/native_sheet.png`.
Manuscript: `translations/item_interface_manuscript_v1.json`.

Source V158 ARM9 SHA-256:
`cf2af4679fb30135b62d0388bbdcc5781d27114d79d47758dc901d9ba4da28a5`.
Research ARM9 SHA-256:
`8bcc6000b0a2356c2e43fb7de871647e89bed693e464e62d93069ed4f3de44df`.
The canonical baseline, V158 ROM/patch and release registry remain unchanged.
No promotion, commit or push is claimed.
