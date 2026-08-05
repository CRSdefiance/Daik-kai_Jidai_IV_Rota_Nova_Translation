# Standard-dialogue tool

The Phase 2 dialogue tool is an offline inspection, formatting, linting, and preview
layer for the game's standard `ILNK` dialogue containers:

- `/COMMON/MESFILE.DK4`
- `/COMMON/HELP.DK4`
- `/data/SC0.DK4` through `/data/SC3.DK4`

It does **not** write a ROM. The existing guarded release builder remains the only
approved path for producing a playable candidate.

## Safety model

Every source byte is represented by the tokenizer. Known prose becomes text, `0A`
becomes `{LB}`, verified name substitutions become explicit macro tokens, and every
unmapped byte is retained as `{HEX:NN}`. A record containing an unmapped control is
reported as unsafe to format. Tokenization followed by serialization is byte-exact.

Scenario containers also hold non-dialogue script/binary segments. `inspect-dialogue`
therefore inventories every non-empty segment and labels only whether its controls are
currently mapped. Its raw record count is **not** a translation-progress total and
`control_safe` is not proof that a segment is prose. The existing format-specific text
index remains authoritative for coverage reporting.

Editable text uses explicit tokens:

| Token | Meaning |
|---|---|
| `{LB}` | Line break using the native renderer's compatibility rule |
| `{LB@n}` | Existing byte-aligned line-break directive |
| `{ALIGN@n}` | Existing byte-alignment directive |
| `{SPEAKER:NN}` | Verified leading speaker/portrait slot byte |
| `{MACRO:FI}`, `{MACRO:FA}`, `{MACRO:FO}` | Verified runtime name substitutions |
| `{MACRO:I}` | The renderer's standalone `I` substitution byte |
| `{HEX:NN}` | Preserved raw byte; untranslated records with these are blocked |
| `{END}` | Explicit zero terminator where a schema requires one |
| `{PAD}` | Existing fixed-record padding request |

Literal uppercase `F` and `I` remain unsafe in this renderer and are rejected. This is
intentional: the game interprets them as command bytes. Removing that limitation needs
the optional runtime renderer work planned for Phase 5.

## Commands

Inventory every record and retain unknown bytes:

```text
dk4tool inspect-dialogue baseline.nds --file-path /COMMON/MESFILE.DK4 --out work/phase2/mesfile.json
```

Check translated rows for unmapped controls, missing/reordered macros, unsafe literal
macro letters, line/page overflow, and fixed byte-budget overflow:

```text
dk4tool lint-dialogue translations/mesfile.csv --profile shared --out work/phase2/mesfile_lint.json
```

Create a separately formatted CSV. The command is transactional: it does not write the
output if a translated record has a blocking error.

```text
dk4tool format-dialogue translations/mesfile.csv --profile shared --out work/phase2/mesfile_formatted.csv
```

Render one record to a diagnostic PNG. Supplying a clean extracted ARM9 draws the
game's own ASCII glyphs:

```text
dk4tool preview-dialogue work/phase2/mesfile_formatted.csv --record DK4_MES_B00_R0001 --profile shared --arm9 work/clean_arm9.bin --out work/phase2/preview.png
```

Add `--format` to preview the formatter's proposed wrapping without changing the CSV.

Audit the expected font tables and renderer instructions without changing a ROM:

```text
dk4tool audit-dialogue-font work/clean.nds --out work/phase2/standard_font_audit.json
```

## Profiles and present limitation

The `story`, `shared`, and `help` profiles use traced renderer metrics: fixed 6-pixel
ASCII advances, fixed 12-pixel Shift-JIS advances, 11-pixel glyphs, and a 16-pixel line
pitch. Cold-boot probes established both story and shared-message boxes at exactly 216
pixels (36 ASCII cells). The help-window width remains provisional pending its probe.

Runtime `FI`, `FA`, and `FO` substitutions use normal glyph advances and vary with the
current given name, family name, and company name. The Raphael defaults measured 42,
36, and 60 pixels. Standalone `I` produces a 12-pixel full-width Japanese first-person
pronoun (`僕` for Raphael), not a literal English capital I. Profile fallback widths
remain conservative when the actual runtime values are unknown.

With `--arm9`, the PNG preview draws the game's exact 6-by-11 ASCII bitmaps. It exposes
wraps, macros, raw bytes, and the right-edge boundary, but it is not an emulator
replacement for runtime substitutions, page transitions, or portrait/name controls.

## Promotion rule

Formatted CSV output is review material only during Phase 2. It must not be fed into a
release build until Phase 3's fixed-size encoder, source-lock checks, protected-baseline
comparison, and cold-boot regression gates are implemented and passed.

As a hard guard, the current ILNK rebuilder rejects the Phase 2 `{SPEAKER:NN}` and
`{MACRO:name}` syntax. Existing release batches continue to use their legacy encoding;
Phase 2 output cannot accidentally become a playable build.
