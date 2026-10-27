# Village promised words: V154 research checkpoint

**Historical research checkpoint, superseded by
[combined V155](all_routes_unified_v155_checkpoint.md).** The actual keyboard,
capacity alias, title/input native rasters and inherited-state verification
described below as pending are now completed and integrated. Physical cold boot,
full widget composition and gameplay usability remain pending. The final ITCM
is 7,900 bytes with arena low 01FF9EE0; the extra village-only keyboard helpers
account for the increase from the 7,704-byte early research version.

The translation goal is active on 2026-10-02. No new playable ROM has been
built or promoted in this checkpoint. Combined V154 remains the latest candidate;
retain the confirmed V153 system-panel and V152 shared-copy repairs.

## Clean-source localization and ownership

`translations/village_promised_words_manuscript_v1.json` contains 54 fresh
natural-dialogue-v2, en-US records: 24 accepted answers, 24 quoted descriptions,
four dialogue templates, the input prompt and editor title. The source is the
exact clean ARM9, SHA-256
`0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731`.

The answer table at `0201192A8` and clue table at `0201191E8` each have 24
entries, copied by the real `020788C0` village routine. The upstream village
selector explicitly iterates indices 0–23 and uses 25 as its no-village sentinel.
The native answer comparison at `02078B00` is case sensitive. Correct input
leads to the clue and permission to use facilities **on the next visit**;
incorrect input leads to the village chief's departure. Preserve that timing.

All byte positions in the four actual loaded ARM9 sections and decompressed
overlay were searched for owner/interior pointers. There are 54 actual references.
The sole extra pointer-like sequence crosses `MOV r1,r6` / `BL 020B4DD8` at
`0202FBDF`; both complete instructions are locked, not broadly exempted.

Proper names are checked against the clean phonetics and clues. References are
saved in the manuscript for Sugarloaf Mountain, Erik, Svartisen, Purnululu and
Tawantinsuyu. Geographic identification remains an inference from that source.
Sugarloaf Mountain is 18 ASCII bytes; the source answer's trailing space is
deliberately omitted. Every drafted ASCII answer fits the parent input limit.

## New native macro hazard, researched repair

The old macro expander `02053914` interprets bare capital `I` and `F` as commands.
It corrupts `Easter Island`, `Frenchman` and `Inca Empire` even after the shared
copy alignment repair. This is distinct from the FE selector and copy defects.
The exact formatter test first caught `Easter Island` becoming invalid CP932.

Research adds a 108-byte resident wrapper at `01FF9DAC`. It treats the **four
exact newly relocated village dialogue template pointers** as literal English.
Every other pointer chains to the inherited monthly wrapper. No Japanese macro
syntax, existing helper body, source string, font or DTCM bytes change. This is
not a universal authorization to bypass macros on other callers: classify and
verify each additional literal-English caller before extending its scope.

The staged payload expands from 1,568 to 3,008 bytes, preserving its complete
inherited prefix. It remains at `023A7200` for startup, then the actual late-copy
stub copies it to the reserved pool beginning `02387A20`. The resident section
is 7,704 bytes, below the overlay boundary `01FFA000`; both heaps are reserved.
Native ARM7 source and loaded sections remain exact after ARM9 autoload, BSS
clear and late copy. Full cross-CPU scheduling/cold boot remain unproven.

## Verification completed

- 96 actual table/strcmp/success-failure branch cases for all 24 answers.
- 24 complete incremental answer entry cases and 38 ASCII/CP932 boundary cases
  through the real append body/frame/return, with cursor/drawing contracts.
- 54 actual village dialogue calls across two supplied crew lists. Native table
  copies, captain selector, actor wrapper, sprintf and scoped literal copy execute.
- The actual `020AE960` input-prompt caller reaches the native modal formatter
  and preserves `Enter the promised words.` in both buffers.
- 56 native raster cases for 28 unique portrait/modal texts, both pixel modes:
  complete glyph order, leading letters, whole words, bounds and independently
  decoded full pixels match. Every generated panel was visually inspected.
- Nine monthly/unrelated preparation cases are identical before and after the
  wrapper, including maximum amount digits and mismatched caller/table scope.
- 32 existing focused renderer, monthly-wrapper and input tests pass; ruff passes.

Proofs and plans have prefix `work/analysis/village_promised_words_`.
Native previews are under `work/qa/village_promised_words_native/`.
Research binary: `work/analysis/village_promised_words_research_arm9.bin`.

## Must finish before integration

1. Trace the **actual keyboard output encoding**, including the Latin page
   selected with the functional `英` resource identifier. Its native page draws
   fixed two-byte cells; synthetic ASCII append tests do not prove keyboard entry
   can produce those ASCII passwords. Do not translate the functional `英`/`記`
   keys blindly: earlier caption substitutions broke page lookup.
2. Complete the real editor capacity path. `020AE960` passes limit 18 to its
   parent; `020AFE58` stores it at parent+`D8`. Child initialization `020B0F38`
   begins with capacity 32, so the append boundary fixtures explicitly supply 18.
   Trace event dispatch, whole-character conversion and the 19-byte destination
   before claiming the real input screen is safe. No observed overflow is claimed.
3. Verify `Promised Words` through the actual title context/printf renderer at
   `020B02B8`, whose bitmap setup specifies 108×12. Complete physical/modal/editor
   composition and usability, including case-sensitive answer spelling.
4. Verify all inherited name owners/getters and the shared ARM946 matrix against
   the final research output. Register a source-locked terminal layer after V154
   name fidelity, build the complete canonical 435-batch stack, and check saved
   ROM/components/manifest, baseline and exact patch reconstruction.

Formatting approvals cover the 24 clues, four dialogue templates and prompt.
The 24 answers and editor title remain pending. No playable candidate or global
rendering guarantee is claimed. The full COMMON/ARM9/graphics goal remains active;
retain the requested after-goal revisit of older record-based checks.
