# V695: relocated source planes and two original embedded UI atlases

The previous goal turn made progress through V694's actual second room/gender
display checks. This checkpoint investigates a different remaining path: image
headers whose palette/pixel pointers have been relocated, including RAM, VRAM
and DTCM sources. Whole-file header comparisons alone cannot identify them.
No missing small-control parent is found. This is evidence that changes the next
investigation, not completion of the six unresolved control contexts.

## Retained actual state, explicit native replay

Three original V653 Sailor Info states at frames 6400, 7200 and 8000 supply the
original main RAM, IO/bank mapping, LCDC VRAM, ITCM and DTCM. These are retained
cold-boot captures with ordinary equipment cursor navigation and a copied save;
no new emulator run, current-ROM gameplay or earned item acquisition is claimed.

The unchanged V663 full lower painter is configured only in this diagnostic
process to write its outputs into the new analysis folder and add a read-only
source observer. No producer/helper file is changed while running. The original
lower iterator still performs all drawing. Its one SDK clock input deliberately
selects the off phase; no image, source getter, clipping, allocator or font call
is bridged. All three complete 98,304-byte outputs are exact to the corresponding
retained V663 off-phase native outputs. They write the complete output over
poison, read no unwritten output, and preserve the original ABI/guards.

All executed code also matches the registered current V692 main/ITCM/overlay/
copied-pool instructions. All 660 whole PXL files in V692 remain byte-identical
to V653. This binds current source art and relevant code, without relabeling old
captures as new V692 gameplay. The explicit off-phase outputs differ from the
retained screenshots by 204, 204 and 236 RGB pixels respectively. Those counts are
retained; this checkpoint makes no new same-frame GPU equivalence claim.

## Complete source-plane identities

There are 59 original primitive entries and 14 distinct header/bank selections
per state: 177 selections and 42 whole planes in total. Source addresses are
derived from the actual descriptors, using the original 16-bit word-width unit
and unsigned relative palette/pixel offsets. The source mapper preserves the
captured VRAM aliases and DTCM precedence. No unknown page is zero-filled.

Every complete packed plane and selected palette bank is retained. Whole pixel
bytes and selected palette bytes identify the current Frame, Marker, Person Info
and chip atlases. Other sources include a portrait strip, an equipment icon,
generated caption/stat planes, the DTCM footer, and these two embedded sources:

| Original source | Address | Dimensions | Complete pixel bytes |
|---|---|---|---:|
| Button backdrops | `021279AC` | 24 by 48 | 576 |
| A/B/X/Y/L/R controller icons | `0211B688` | 96 by 28 | 1,344 |

Both complete embedded pixel ranges match clean Japanese, V653 and current V692
ARM9 bytes. They are used as source inputs by the actual lower-screen painter.
The source sheet was opened and reviewed: these are decorative UI backdrops and
existing Latin controller symbols, with no Japanese text to translate. Preserve
them. This is source classification and selected native use, not a claim that
every glyph variant or palette bank has separately been shown on hardware.

## Small-control result and limits

Seven current English and seven original Japanese complete templates are checked
against all 42 whole indexed planes at their actual strides. Only the three
known Frame palette selections per state contain the five miniature captions.
No source crop among all 177 original calls intersects those caption cells.
Confirm's full graphic and inner face have no matching source in these planes.
The independent matcher finds a caption at a deliberately different stride and
rejects a changed ink point outside its anchor row.

This resolves these relocated Sailor Info sources; repeating the same sources
will not establish the six missing control parents. Other states, readers,
rescaled/reindexed copies and actual legacy consumers remain open. No global
unused-art assertion follows from this bounded negative result.

Initial probes incorrectly assumed all PXLs were indexed, then used 32-bit
instead of 16-bit width units, and initially omitted the copied painter's
preflight in its process-local output folder. Their failures changed only the
analysis harness; retained rejected sources and this explanation preserve the
corrections. No game, art or source palette was altered.

## Recording and remaining goal

The experimental ROM remains V692, SHA-256
`0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.
ROM, manifest, patch, registry, canonical baseline and release pointers are exact.
All 18 plaque/hint entries remain incomplete and all 22 historical requirements
remain unchanged. Six controls, cards/comics/legacy/restoration, V694's suffix
comparison, older record checks and final acceptance retain their scope.

- Producer: `scripts/research_relocated_sources_v695.py`.
- Independent source/matcher checks: `scripts/verify_relocated_sources_v695.py`.
- Analysis: `work/analysis/relocated_sources_v695`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V695 Relocated UI sources`.
- No new ROM, guide promotion, commit, push or acceptance. Full goal remains active.
