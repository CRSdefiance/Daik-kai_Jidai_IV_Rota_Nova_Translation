# English text rendering and formatting roadmap

## Implementation status

Phase 2 began on 2026-08-05. The repository now has a lossless standard-dialogue token
model, ILNK control inventory, explicit macro markup, profile-driven pixel wrapping,
deterministic lint reports, and diagnostic PNG previews. See
[dialogue_tool.md](dialogue_tool.md).

Phase 3's conservative fixed-size encoder is now implemented as an explicit per-batch
opt-in. The base 6/12-pixel advances and 6-by-11 ASCII glyphs are
verified from ARM9. Cold-boot probes established the story and shared-message boxes at
216 pixels (36 ASCII cells), and confirmed that name/company macros use normal glyph
advances. The help-window bound still needs its own probe. Relocation remains disabled;
one fixed-allocation Raphael record is registered as a live experimental profile.

Phase 4 groundwork now includes a read-only block-layout inventory command and a
fail-closed relocation planner. The planner calculates shifted record and entry-point
offsets but rejects every size change while a block's external/interior reference map
is incomplete. No playable build currently enables record expansion.

## Goal

Build a profile-driven English text system that makes translations predictable without
changing unrelated game state. The first target is standard dialogue in
`/COMMON/MESFILE.DK4`, `/COMMON/HELP.DK4`, and `/data/SC0.DK4` through
`/data/SC3.DK4`. Later adapters will cover ARM9 menus, compact HUD fields, packed name
tables, and graphical text.

This work has two layers:

1. An **offline dialogue compiler** that understands the original bytecode, lays out
   English safely, validates it, and rebuilds only declared records.
2. An optional **runtime renderer patch** that removes limitations which cannot be
   solved cleanly offline, such as macro collisions, proportional Latin text, and
   constrained record storage and safe zero-indent progressive-story newlines.

The offline compiler is the first deliverable. A runtime patch must not become a
prerequisite for continuing ordinary translation work.

## Renderer families

| Family | Examples | Planned handling |
|---|---|---|
| Standard dialogue | `MESFILE`, `HELP`, `SC0`–`SC3` | Shared dialogue profile and compiler; highest priority |
| ARM9 dialogs and menus | Options confirmations, character editor, shipyard formatters | Small renderer-specific profiles; runtime adapter where ASCII is not supported correctly |
| Compact live fields | Dates, coordinates, prices, names, HUD labels | Width-aware formatter profiles with strict slot limits |
| Packed or substring tables | BGM/SFX titles, some names and labels | Map every interior pointer before relocation or replacement |
| Graphical text | PXL atlases, cutscene subtitle cards | Existing image decode/redraw/repack pipeline; tracked separately |

## Standard-dialogue architecture

### 1. Lossless record parser

Replace the current assumption that a record is simply CP932 prose with a lossless
token stream. Every byte must be represented as one of:

- visible Japanese or Latin text;
- line, page, wait, portrait, speaker, or layout control;
- runtime substitution such as protagonist names;
- leading/trailing layout padding;
- unknown bytes retained verbatim; or
- record terminator and internal entry-point boundaries.

No-edit parsing and serialization must remain byte-identical for every standard
dialogue container. Unknown controls block translation of that record instead of being
guessed.

### 2. Explicit intermediate representation

Use one structured representation for translators and builders. Suggested tokens are
`{LB}`, `{PAGE}`, `{WAIT:n}`, `{SPEAKER:n}`, `{PORTRAIT:n}`, `{NAME:given}`, and
`{RAW:hex}`. Literal English must never be confused with runtime commands; in
particular, uppercase `F` and `I` must cease to be implicit macro syntax in editable
text.

Each record should retain:

- source file, block, record, and byte offsets;
- exact source bytes and source-file hash;
- renderer profile and control schema;
- all known entry points into the record;
- byte budget and expansion policy;
- speaker, portrait, scene, and route metadata; and
- formatting and emulator-test status.

### 3. Font metrics and layout engine

Measure the actual in-game Latin glyph widths and define dimensions per window type.
Wrapping must use pixel widths rather than a universal character count. The engine
should support:

- word wrapping without splitting ordinary words;
- explicit translator-selected breaks;
- maximum lines per page;
- punctuation and indentation rules;
- worst-case widths for runtime names and numbers;
- overflow diagnostics with the widest offending line; and
- renderer-family-specific newline modes. Progressive story dialogue requires guarded
  `0A 20`; the bare-`0A` experiment is revoked after live glyph-loss failures.

The formatter should produce a layout report before it produces replacement bytes.

### 4. Safe encoder

Encoding should be selected by renderer profile, not by a global setting. For the
initial standard-dialogue profile it must:

- preserve all control tokens and their order;
- protect the first visible glyph after a line break;
- preserve required leading layout bytes;
- encode runtime substitutions explicitly;
- reject unknown macros and unencodable characters;
- enforce exact-size records until entry points are mapped; and
- pad only through a declared padding policy.

### 5. Entry-point and relocation map

Some records contain several messages or are entered at interior byte offsets. Before
allowing expansion, build a reference map for every ILNK block:

- discover all pointers to block starts and record interiors;
- identify shared suffixes and substring records;
- record pointer base, width, endian order, and owning table;
- rewrite every affected pointer when a record moves; and
- prove that untouched pointers and blocks remain identical.

Expansion stays disabled for a block until its reference map is complete and covered
by tests.

### 6. Preview and diagnostics

Provide a desktop preview that draws text with extracted game font metrics and the
selected window profile. It does not replace emulator testing, but it should expose
overflow, bad breaks, leading-glyph hazards, substitutions, and page boundaries before
a ROM is built.

Proposed commands:

```text
dk4tool inspect-dialogue <rom> --file-path <path> --out <report>
dk4tool format-dialogue <translation> --profile story --out <formatted>
dk4tool preview-dialogue <formatted> --record <id> --out <image>
dk4tool lint-dialogue <translation> --profile story
```

## Optional runtime renderer patch

After the offline compiler is stable, trace the standard dialogue draw routine and its
callers. Determine whether `MESFILE`, `HELP`, and all four story containers converge on
one glyph loop. If they do, a single carefully scoped hook should:

- distinguish literal ASCII from game commands;
- apply newline before the following glyph;
- accept explicit substitution/control opcodes;
- use measured Latin advances, ideally variable width;
- preserve Japanese rendering for untranslated records; and
- remain compatible with existing saves and control scripts.

If callers set materially different modes, keep one shared core with small adapters.
Do not duplicate a complete renderer for each screen. The patch must have a signature
check against the exact ARM9 revision and a feature flag so an unpatched build remains
possible.

## Later adapters

### ARM9 menus and prompts

Catalog each draw function and assign a profile: ASCII-capable, fixed-width CP932,
formatted string, or graphical. Options Reports/Sailing Help is the first fixed-width
test case. An adapter may redirect it to the shared Latin glyph routine or supply a
profile-specific encoder; full-width Latin is only a diagnostic fallback, not release
quality.

### Compact HUD and formatted values

Model placeholders and maximum rendered values, then measure the complete result in
pixels. Date, money, percentage, coordinate, and ship-name formatters need separate
golden cases because their available widths differ.

### Packed tables

Map interior pointers before translating BGM/SFX titles or any concatenated name table.
The tool should expose each pointed-to substring as a stable logical row while retaining
the shared backing range and rejecting overlapping edits that cannot coexist.

### Graphical text

Continue using atlas-specific redraw scripts. Add a registry connecting each visible
caption to its ROM resource, bounding box, palette, English text, preview, and test
status so graphical coverage can be audited alongside live text.

## Verification gates

The following gates are required before the standard-dialogue compiler can be used for
release candidates:

1. Byte-exact no-edit roundtrip for `MESFILE`, `HELP`, and `SC0`–`SC3`.
2. Golden tokenization tests for every known control and macro.
3. Tests proving that line breaks do not consume the first English glyph.
4. Tests for literal uppercase `F` and `I`, names, punctuation, and multibyte text.
5. Pixel-width tests using short, exact-fit, and overflow examples.
6. Pointer-preservation tests for fixed records and relocation tests for mapped blocks.
7. Integrated-release verification against `out/raphael_natural_v2_accepted_base.nds`.
8. Cold-boot emulator checks for each modified renderer family and previously accepted
   screens.

No new renderer family is considered supported until it has at least one live-tested
golden screen and a documented rollback path.

## Delivery phases

| Phase | Deliverable | Completion criterion |
|---|---|---|
| 0 | Renderer inventory and golden corpus | Representative good/bad records and screenshots classified by renderer family |
| 1 | Standard-dialogue tokenizer and linter | Unknown controls are blocked; known records roundtrip byte-exactly |
| 2 | Width-aware formatter and preview | Standard dialogue can be wrapped and previewed with deterministic diagnostics |
| 3 | Fixed-size standard-dialogue encoder | New translations build without dropped glyphs, macro collisions, or undeclared changes |
| 4 | ILNK entry-point mapper and safe relocation | Mapped blocks can expand while all interior pointers remain valid |
| 5 | Optional shared runtime renderer hook | Proportional Latin, explicit macros, and zero-indent protected newlines pass cold-boot tests across standard dialogue |
| 6 | Menu, HUD, packed-table, and graphics adapters | Each remaining renderer family has its own profile, tests, and coverage registry |

## Initial implementation slice

Start with a small golden corpus from Raphael dialogue, Lil dialogue, tavern/shared
messages, tutorial/help text, and the known broken Options prompt. Phase 1 should change
no ROM bytes: it only parses, tokenizes, roundtrips, and reports hazards. Once those
tests pass, format and rebuild a disposable standard-dialogue probe from the protected
baseline and cold-boot test it before translating larger blocks.
