# Combined V158: natural English Gallery descriptions

V158 is the latest **experimental** combined candidate. It rebuilds the complete
435-batch registered stack from the immutable canonical baseline, preserves all
V157 stages, and adds eight source-reviewed logical Gallery translations through
ten native pointer fields. Physical cold boot and gameplay remain pending.

## Source and natural English

The headings are **Event Scenes** and **Historic Sites**. Their descriptions are
**Relive memorable scenes from each captain's story.** and **View the ruins and
churches you've discovered.** Four selected-captain descriptions read
**Memorable scenes from Raphael's/Hodram's/Lil's/Maria's story.**, with the actual
captain's name selected by the native table at 02115678. All-byte loaded-section
and overlay scans prove the ten pointer owners. Original Japanese storage is
preserved. The four table entries were discovered by tracing the consumer;
the older code-address queue did not include them.

Logical prose has no authored positioning spaces or line breaks. The formatter
balances complete words across the two native description rows and avoids weak
row endings such as "and". This Gallery renderer draws ASCII in pairs. An odd
length can produce a synthetic final space cell; compiled rows now explicitly
include a machine-generated trailing space when necessary. Each expected glyph
and cell is verified, including first and last letters.

## Actual callers, allocation and parent presentation

Native event constants at 02042C2C–02042CE4 and draw instructions at
02042D20–02042D98 establish the initial title and description positions.
Selected-captain draws at 02042F70–02042FD0 execute the actual array lookup.
The complete Historic Sites function at 02044158 is exercised with and without
a selected site-name fixture. Native 020456A0, byte-length centering, context
setup, string rendering and cleanup all execute. Seven page variants produce
14 paired 4/16-bit raster cases. Complete glyph vectors, independent font
pixels, native coordinates/tracking, bounds, caller state and stack pass.
All seven unique preview panels were visually inspected.

The actual bitmap constructor 02045C84 creates a 256×192 4-bit canvas at
owner+14, with its inline image header at owner+6014. Native overlay 0 code at
01FFB2DC clears an A5-seeded canvas completely; surrounding canaries survive.
Primary dispatch 02045710 → 020CFDE8 → 020D4170 reaches native GPU boundary
01FF92D8 with the complete 256×192 image at destination (0,0), layer 1, flags 0.
No Gallery text is cropped by this primary view. Resource/GPU registration,
surrounding artwork, upstream menu input and actual hardware output are explicit
remaining contracts. Selected site-name provision is a fixture.

The inherited 3296-byte staged pool prefix stays exact. V158 adds text only,
growing the pool to 3584 bytes (3574 used), staged at 023A7200 and late-copied to
02387A20. Copy entry is 023A8000; staging ends at 023A8030. Main arena low is
02388820. ITCM remains 8172 bytes, ending at 01FF9FEC with aligned arena low
01FFA000. No new resident helper is added. Native SDK autoload/BSS, ARM7 source,
loaded sections, late copy, all arena bounds, registers and stack pass.

## Integration and regression evidence

All 64 inherited duel rasters and both sailing-status rasters remain identical.
24 movement callers, 54 village callers, nine monthly/unrelated scope cases,
207 names, 239 shared owners, all 3668 COMMON selections and 704 ARM946 copy
alignment cases pass. Fifty-six focused tests and changed-tool lint pass.
Negative checks reject a lost first letter, wrong captain pointer, missing
captain evidence, absent visual review, cropped primary view and stale proof.

The saved manifest retains all 435 batches and inherited terminal stages.
Canonical menus/graphics and exact clean-ROM patch reconstruction pass. **Only
ARM9 differs from V157**; COMMON, all four routes, fonts, graphics and every
other component remain exact. The inherited 1061 FE panel proof is preserved
through unchanged relevant bytes; those cases were not rerun. No canonical
promotion, commit or push is claimed at this checkpoint.

| Artifact | SHA-256 |
| --- | --- |
| Canonical baseline | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V158 ROM | `9a197373ba448718f3c0d887fdd27f01ce19b75dae11bb22515fed36981a7f5f` |
| V158 ARM9 | `cf2af4679fb30135b62d0388bbdcc5781d27114d79d47758dc901d9ba4da28a5` |
| COMMON | `ea978f466496f8593f13fb97f17b9bac174beea5665c57f1f5e358b2808776c9` |
| V158 patch, 751795 bytes | `42cd951f72695e3b2fee71ed02d9905c9cec6bbb9b577803425fd47648972984` |
| Registry at build | `fff023b1df4856684397f0be0b49c8f5435697db1539b4f25b00a896d8c8d8ea` |

ROM: `out/all_routes_combined_v158_candidate.nds`; adjacent manifest and xdelta
patch share its stem. Saved verification: `work/analysis/gallery_v158_saved_proof.json`.
Reviewed previews: `work/qa/gallery_descriptions_native/native_sheet.png`.
Registered profile: `all-routes-unified-v158`, experimental. All accepted layers
are already baked into the canonical baseline; the manifest requires zero
additional accepted batches and retains all 435 profile batches and inherited
terminal stages. Compared with the canonical baseline, the nine changed paths
are `/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
`/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and `/data/SC0.DK4` through
`/data/SC3.DK4`. Compared with V157, ARM9 is the only changed component.
Physical title/New Game/established story/town and changed Gallery screens still
require cold-boot testing before full candidate acceptance.

## Full goal remaining

The refreshed loaded inventory has 81314 byte/font candidates and 1449 aligned
address-word leads, **not untranslated counts**. Rough report:
`work/analysis/translation_coverage_v158.md`. The exploratory
`work/analysis/arm9_ui_reference_queue_v158.json` contains 654 unclassified,
unchanged code-address leads. Its broader filter differs from the older
237-entry queue, so these counts are not comparable; indirect table consumers
also remain in the complete inventory.

245 COMMON selections/133 owners still need actual consumer/layout integration.
Further ARM9/UI, older-name semantics, Japanese graphics, complete composition
and physical help/BGM/gameplay checks remain. The full goal stays active. Revisit
older record-based checks after goal completion, as requested.
