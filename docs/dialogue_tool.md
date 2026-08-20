# Standard-dialogue tool

The dialogue tool provides offline inspection, formatting, linting, preview, and an
opt-in fixed-size encoder for the game's standard `ILNK` dialogue containers:

- `/COMMON/MESFILE.DK4`
- `/COMMON/HELP.DK4`
- `/data/SC0.DK4` through `/data/SC3.DK4`

The encoder does not write a ROM directly. The guarded release builder remains the
only approved path for producing a playable candidate.

For profiles with `pair_phase_safe_breaks`, encoding also models the progressive
renderer's two-single-byte draw batches. Protected breaks are emitted as `LF+SPACE`;
when the tracked ASCII phase is unsafe, an additional pre-LF space is inserted in the
encoded bytes only. It counts against the fixed record allocation but never appears in
editable dialogue markup. Macro expansion parity must be declared by the route profile
or encoding stops with `pair-phase-unsafe`.

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

For delegated natural-dialogue batches, use the batch audit rather than previewing
records one at a time:

```text
python scripts/audit_dialogue_batch.py --rom out/raphael_natural_v2_accepted_base.nds --japanese-rom work/clean.nds --batch translations/<batch>.json --out work/qa/<batch>
```

It validates the source lock and policy, formats and fixed-encodes every record,
reports widths/padding/manual-break debt, and creates one exact-font PNG per record.
The command fails on every unwaived warning or error. See
`dialogue_delegation_protocol.md` for the v2 work-packet rules.

Audit the expected font tables and renderer instructions without changing a ROM:

```text
dk4tool audit-dialogue-font work/clean.nds --out work/phase2/standard_font_audit.json
```

## Profiles and present limitation

The `raphael-story-live`, `story`, `shared`, and `help` profiles use traced renderer metrics: fixed 6-pixel
ASCII advances, fixed 12-pixel Shift-JIS advances, 11-pixel glyphs, and a 16-pixel line
pitch. Cold-boot probes established both story and shared-message boxes at exactly 216
pixels (36 ASCII cells). The help-window width remains provisional pending its probe.

`raphael-story-live` is required for new Raphael dialogue. It emits protected `0A 20`
breaks and models the default Raphael/Castor/Castor Co. macro widths. The bare-newline
profile is retained as `story-clean-revoked` solely to reproduce the failed probe and
must never appear in a release profile.

Runtime `FI`, `FA`, and `FO` substitutions use normal glyph advances and vary with the
current given name, family name, and company name. The Raphael defaults measured 42,
36, and 60 pixels. Standalone `I` produces a 12-pixel full-width Japanese first-person
pronoun (`僕` for Raphael), not a literal English capital I. Profile fallback widths
remain conservative when the actual runtime values are unknown.

With `--arm9`, the PNG preview draws the game's exact 6-by-11 ASCII bitmaps. It exposes
wraps, macros, raw bytes, and the right-edge boundary, but it is not an emulator
replacement for runtime substitutions, page transitions, or portrait/name controls.

## Fixed-size encoding

Translation batches may opt in with `"encoder": "dialogue-fixed-v1"` and a
`dialogue_profile`. This encoder formats the editable markup, preserves the exact
source command multiset and order, rejects unknown controls and unsafe literal macro
bytes, enforces the calibrated pixel/page limits, and pads back to the exact source
record length. `{PAD}` is mandatory so padding is always intentional.

This mode never relocates a record. `allow_expand`, raw replacement bytes, and `{END}`
are rejected. Existing legacy batches are not reinterpreted and retain their previous
behavior.

The first registered live profile is `natural-dialogue-probe`, containing the
contiguous opening conversation of Raphael's route and one tutorial record. Its
verifier proves that `/data/SC0.DK4`, every ILNK block, and every record except the
declared targets retain their original size and bytes.

## Promotion rule

Only explicitly registered `dialogue-fixed-v1` batches may enter a playable probe.
They still require the source lock, release-stack checks, structural verifier, cold
boot, and user acceptance before promotion. Record relocation remains disabled until
the relevant block's interior entry points and mixed binary payload are fully mapped.
