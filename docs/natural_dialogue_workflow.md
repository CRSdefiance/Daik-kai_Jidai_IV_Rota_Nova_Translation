# Natural-dialogue workflow

This is the required process for every story or shared-dialogue translation, whether
it is written by Luna, Terra, Sol, or a human contributor.

New work uses `natural-dialogue-v2` and the exhaustive process in
`dialogue_delegation_protocol.md`. `natural-dialogue-v1` remains valid only while
existing reviewed batches are migrated.

## Source and context

1. Translate from the clean Japanese record, never from an older English draft.
2. Review the previous and next spoken records, speaker control, portrait, scene,
   and runtime name/faction macros before writing the line.
3. Translate the intent and character voice. Do not shorten merely to imitate an old
   fixed-width draft. If the allocation is genuinely too small, flag the record for
   relocation instead of shipping broken English.

## US localization

The target is idiomatic American English (`en-US`), not a word-for-word Japanese
transcript. Preserve story facts, intent, tone, characterization, and necessary
cultural information, then express them the way an American localization would.

1. Do not copy Japanese syntax, sentence fragments, repeated subjects, honorifics,
   or forms of address when they sound unnatural in American English.
2. Never invent a relationship, title, rank, gender, or factual implication merely
   because a Japanese form of address can be translated literally. For example,
   `じいさん` can be a familiar way to address an older man; translating it as
   “Grandpa” is forbidden unless the surrounding story proves actual kinship.
3. Prefer the character's established name when “old man,” “big brother,” “master,”
   or a similar literal address would mislead an American player. Retain such wording
   only when it conveys important characterization without creating a false fact.
4. Localize idioms and jokes by effect rather than vocabulary. Preserve deliberate
   formality, rudeness, hesitation, or affection in natural English dialogue.
5. Use the project glossary for names, places, factions, ships, and nautical terms.
   Do not improvise a new spelling or relationship label to make one line fit.
6. Read every line aloud and review it with the preceding and following lines. A line
   that is technically accurate but sounds translated fails the localization gate.

## Formatting

1. Write prose as one logical paragraph. Do not insert `{LB@...}` or `{ALIGN@...}`.
2. Let `dialogue-fixed-v1` wrap Raphael dialogue using the calibrated
   `raphael-story-live` profile. Other routes require their own route-aware profile.
3. An explicit `{LB}` is allowed only for a deliberate dramatic pause or paragraph
   boundary and requires a `manual_break_reason` on that record.
4. Preserve speaker controls and `{MACRO:FI}`, `{MACRO:FA}`, and `{MACRO:FO}` exactly.
5. Keep `{PAD}` for `dialogue-fixed-v1` until relocation is available. A
   `dialogue-relocatable-v1` batch must omit `{PAD}` and is allowed only when its
   exact source block has a complete, independently reviewed relocation map. Review
   the padding report for fixed records: large trailing padding after a full page can
   create a blank page in the native renderer.
6. Cold-boot testing proves that a bare `0A` is unsafe in progressive story dialogue:
   the next glyph can appear before the line transition. The encoder—not the translator—
   must emit the protective space. Never author one manually.
7. The first line has 36 visible cells. A guarded continuation conservatively budgets
   35 until a zero-width guard or runtime fix is live-tested. Raphael macros use their
   default 7/6/10-cell values; every other route needs a route-aware macro profile.
8. Do not preserve leading Japanese line breaks merely for vertical staging. English
   dialogue begins on the first line unless a scene-specific review demonstrates that
   a deliberate pause is essential.
9. `raphael-story-live` also models the live progressive renderer's two-ASCII-byte
   draw batches. At a protected break whose current phase would batch the guard with
   the first continuation glyph, the encoder inserts an internal pre-LF phase space.
   This byte never appears in editable markup and translators must not author it.
   It consumes fixed allocation; a record that no longer fits must be rewritten
   naturally or moved to the relocation backlog.
10. Runtime macro width does not prove expansion-byte parity. A pair-phase-aware
    profile must declare the exact ASCII expansion length for every macro before a
    protected break. The encoder fails closed when that parity is unknown.
11. Raphael SC0 uses printable leading state bytes for two B48 speakers: `0x4B`
    for Hans Retzel and `0x71` for the dock worker. They are mapped only by
    `raphael-story-live` and must be authored as `{SPEAKER:4B}` and
    `{SPEAKER:71}`. Do not generalize printable ASCII into speaker controls;
    other leading values remain blocked until independently mapped.

## Editorial gates

Every batch using `translation_policy: natural-dialogue-v1` must declare
`target_locale: en-US` and all five review gates: `source`, `context`, `localization`,
`naturalness`, and `formatting`. Each record must name its speaker and explain its
scene context. The integrated builder rejects positioned breaks, diagnostic strings,
missing context, and unreviewed batches.

Version 2 additionally requires the five review gates on every individual record,
plus a faithful `source_meaning` gloss and a `localization_note`. This prevents a
new record from inheriting a batch-level approval that was granted before it existed.

Natural dialogue should read aloud cleanly. Prefer contractions where they suit the
speaker, complete idiomatic sentences, and consistent names. Avoid telegraphic phrases
such as “Sorry to ask so much” when “I'm sorry to ask so much of you” fits and better
matches the Japanese.

## Required verification

Before accepting a rewritten scene, review every generated line boundary and the
transition to the following record. An isolated final letter, an unexpected empty
box, or a blank line at the top of the next record is evidence of a width/padding
failure and blocks release.

Before handoff, validate the batch, build through its registered release profile, and
cold-boot the title, New Game, the complete changed scene, and the transition into the
next scene. Never use a save state. Capture any unexpected portrait, blank box, lost
first letter, extra page, or unnatural wrap as a release blocker.
