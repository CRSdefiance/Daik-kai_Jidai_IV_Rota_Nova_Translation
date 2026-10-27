# Actual player-name expansion and complete glyphs: V278 research

V277 compiled and scope-checked all76 short-slot name-migration translations.
This turn verifies their remaining macro expansions from actual current player
state and checks every complete expanded body against the real font painter.
The latest playable candidate remains V275; the fixtures here are research-only.

## Actual current player state

A6000-frame ordinary DeSmuME cold boot starts from the complete V275 parent,
changing only the research ARM9 name fields/catalog. All script files, artwork,
other resources and ARM7 remain exact. No savestate is loaded. The test reaches
Rafael's actual opening and exports4MiB of RAM read-only. Native execution uses
this captured state and the exact startup-loaded catalog bytes; no getter or
macro-function bridge provides any name.

Sixteen independent macro/alignment cases confirm the actual defaults:

| Macro | Actual output | ASCII bytes |
|---|---|---:|
| FI | Rafael |6|
| FA | Castor |6|
| FO | Castor Co. |10|
| FU | Rafael Castor |13|

All131 catalog keys, including the98 macro-bearing keys, then execute through
the native lookup and original expander at four alignments and three scoped
callers: **1572 complete copies**. The expected expanded strings, terminating
NUL,512-byte output region, input guards, saved registers, stack and complete
catalog payload match. The caller actor-context argument is0, using the captured
default Rafael player state. This does not prove custom-name layout or every
other runtime context/route scene.

## Complete visible glyphs and pixels

All76 compiled bodies are expanded using the verified native outputs, with only
their mapped leading actor/FE selector removed before the font test. The real
ASCII painter and original ITCM Shift-JIS painter execute on a controlled216×64
native bitmap. Independent ASCII font and KANJI.FNT decoding verifies every
foreground/shadow pixel, every blank region, semantic glyph order, distinct
nonoverlapping visible cells, first/final letters and complete line bounds.
Input/header/pixel/register/stack guards pass. Each body uses at most four
consecutive16-pixel rows with no missing row.

One checker initially rejected a blank ASCII draw at x216 in SC0 B136 R0168.
Inspection confirms that all visible glyphs are in bounds, every character
survives and the native painter clips that empty request without writes outside
the bitmap. The independent checker now clips empty-cell clearing to the view
while retaining strict full-cell bounds for every visible glyph. No game code,
wording or panel limit changes to accommodate this harmless blank request.

All10 native-text review sheets were viewed. Nine corrected final sheets are
byte-identical to the viewed first pass; the changed final sheet was viewed again.
This visual review establishes readable complete native text; full source/context
editorial gates and original progressive scene behavior remain separate checks.

## Source-faithful punctuation correction

The review found a genuine punctuation defect in SC0 B147 R0012. The default
company macro already ends in **Co.**, and the earlier authored sentence appended
another period, producing **Co..**. The Japanese has Uddin courteously change his
address to the company leader: `FO総帥`.

The revised logical sentence reads:

> Forgive me for startling you, {MACRO:FI}... or perhaps I should call you {MACRO:FO}'s leader.

The default display now ends **Castor Co.'s leader.** The business leadership
meaning remains; no military rank or new story fact is added. Custom company
names also receive a proper sentence-ending period. The new versioned override
locks the exact canonical Japanese source and the exact older reviewed wording
it supersedes. Translators author no line breaks or alignment spaces.

After this correction, the route/COMMON scope census, native startup/cache/arena/
ARM7 checks,2096 lookup cases,1179 near-miss cases,396 literal copies, fresh cold
boot,1572 real-state expanded copies and all76 native glyph checks pass again.
Targeted Ruff passes. The first-pass fixture/evidence is retained separately.

## Final research identities

| Artifact | SHA256 |
|---|---|
| Corrected research ARM9 | `6cdc1ab1cbc74d5836ca8bd67d911a6ff9519a6c49845bc9a428c24702202a89` |
| Corrected research-only ROM | `30af96ed94dd45660650026a76caeeb6892e88d2bc20ec8d2ef7144141b28488` |

The final fixture manifest is `work/analysis/name_macro_v278/final/fixture_manifest.json`.
It explicitly forbids normal-gameplay release or handoff. The original scene and
script text are not fully migrated yet; do not present this fixture as the next
combined release. The actual RAM/ROM/ARM9 and glyph proof identities agree.

## Remaining gates and next action

The98-key default-player expansion gate and76-body native glyph gate are now
verified. The catalog still has26 compiler line-break-count warnings needing
record-specific formatting review; ordinary generated English wrapping must not
inherit Japanese manual line positions. Complete the other368 fixed route
records' review/previews, the six native COMMON final expansion/display checks,
the two structured HELP article allocations/consumers and remaining name/art
consistency. Then integrate all changes through one registered full inherited
profile, reproduce the preceding ROM and verify an exact clean-ROM patch plus
ordinary scene/transition cold-boot samples.

All18 plaque/hint entries and their variants remain incomplete. Alternate
status/equipment contexts, other native/art consumers and final whole-goal audit
remain open. Low-resolution Online images stay excluded by the user's direction.
The goal remains active and incomplete. Revisit older record-based checks at
actual completion.

## Evidence

- `translations/confirmed_name_editorial_v278.json`
- `work/analysis/name_macro_v278/final/actual_player_macro_proof.json`
- `work/analysis/name_macro_v278/final/native_glyph_proof.json`
- `work/emulation_v193/name_macro_v278_final/capture_report.json`
- `scripts/verify_name_macro_real_state_v278.py`
- `scripts/verify_name_catalog_glyphs_v278.py`

The font surface is controlled native input, and the actual player RAM comes from
the cold boot. Neither test is a full route playthrough or hardware verification.
