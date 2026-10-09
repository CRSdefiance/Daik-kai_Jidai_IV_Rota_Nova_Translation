# Initial glossary

| Japanese | Suggested English | Category |
|---|---|---|
| 出航 | Set Sail | menu |
| 交易 | Trade | menu |
| 港 | Port | location |
| 酒場 | Tavern | location |
| 造船所 | Shipyard | location |

Treat these as working terms until verified in game context.

## Character names

### Faithful, sensible English naming

On 2026-10-06 the user confirmed the naming choices below and refined the policy:
use original Latin names when appropriate, but prefer a faithful, more sensible
English localization when one exists. Original artwork is evidence of the game's
chosen spelling; it does not automatically override a better adaptation.

Preserve character identity and the Japanese source's name/sound. Consider English
readability, unintended meanings and national naming conventions without inventing
an unrelated identity or claiming that a fictional name is a real national name.
Make decisions individually and keep dialogue, nameplates, biographies and artwork
consistent. Do not bulk-rename characters solely to match original Latin artwork.

| Previous project spelling | Confirmed spelling | Decision and basis |
|---|---|---|
| Raphael | Rafael | `Rafael Castor`, clean `/FLS/M28.fls` texture 22. |
| Hodram | Hodram | User-confirmed phonetic adaptation of ホドラム. Original `Hoodlum` has an unintended English meaning; reconcile opening art with Hodram. |
| Joachim | Joakim | User explicitly confirmed Joakim; original `Hoodlum Joakim Bergstrom` card, texture 46. |
| Kamil | Camille | User explicitly confirmed Camille; original `Camille Overijssel` card, texture 71, supplies a valid Latin name. |
| Maria Hoamei Lee / Hoa-mei Lee | Maria Huamei Li | User explicitly confirmed the source-reviewed Maria Huamei Li spelling on 2026-10-06. |
| Lil | Lil | `Lil Argot`, also visible in texture 71; retain this spelling. |

The user has explicitly confirmed **Rafael**, **Hodram**, **Joakim**,
**Camille** and **Maria Huamei Li**. **Lil Argot** retains its established spelling.
The reviewed choices are settled. The Hodram-to-Hoodlum proposal is superseded;
Kamil is a historical project spelling to migrate, not an open preference.

On 2026-10-07 the user reaffirmed **Camille** as final and requested a written
rationale for all settled names. The explanations below are the decision record
for future translation and graphics work. Reuse these spellings consistently;
do not reopen the choices based only on an older manuscript spelling.

Maria's confirmed spelling is **Maria Huamei Li**. The Japanese publisher uses
マリア・ホアメイ・リー; an official Chinese series announcement uses
瑪莉亞・華梅・李. Huamei/Li is the proposed Mandarin romanization of 華梅/李,
preserving Maria from the source. This does not establish a birth/baptism story.
See `docs/maria_name_source_review_2026_10_06.md`; implementation remains pending,
including the untranslated stored middle-name field.

### Why we chose these names

**Rafael Castor:** the original Latin card explicitly gives Rafael. It is also a
valid Portuguese given-name form, fitting the character's established background.
Raphael was a defensible earlier adaptation, but the clear source spelling gives
us a stronger basis for Rafael. Castor already agrees with the source and stays.
Sources: clean `/FLS/M28.fls` texture 22; the publisher's
[character introduction](https://www.gamecity.ne.jp/products/products/ee/new/dai4/dai4_02.htm);
Portugal's [official given-name list](https://irn.justica.gov.pt/Portals/33/Regras%20Nome%20Proprio/Lista%20Nomes%20Pr%C3%B3prios.pdf).

**Hodram Joakim Bergstrom:** Hodram is our deliberate exception to the original
Latin first name Hoodlum. It follows the Japanese ホドラム closely and avoids
an English word carrying a thug/criminal meaning. It preserves the fictional
character's identity without inventing an unrelated Swedish name. We do not claim
Hodram is a conventional Swedish given name. Joakim matches the original Latin
middle name and Swedish naming; it supersedes the earlier Joachim spelling.
Bergstrom retains the original game's surname spelling. Sources: clean M28
texture 46; [Cambridge's Hoodlum definition](https://dictionary.cambridge.org/dictionary/english/hoodlum);
[Swedish name statistics](https://www.namntips.se/fornamn/Joakim/).

**Camille Overijssel:** the original artwork explicitly establishes Camille, and
Camille is a genuine name used by men as well as women. We preserve this valid
source name because no concrete unwanted English meaning or readability problem
has been established that warrants replacing it. Kamil was a reasonable phonetic
adaptation of カミル, but phonetic reconstruction is weaker evidence once the game
supplies a usable Latin spelling. The earlier preference for Kamil placed too much
weight on phonetic closeness; that reasoning was reconsidered and the user then
confirmed Camille. A French-form name does not invalidate a fictional Dutch
character or require us to invent a more stereotypically Dutch identity. Overijssel
already agrees with the original card and remains unchanged. Sources: clean M28
texture 71; [INSEE on names used by both sexes](https://www.insee.fr/fr/statistiques/9040114).

**Maria Huamei Li:** preserve Maria, which is explicit in the Japanese publisher's
full name, and use a consistent Mandarin romanization for 華梅 and 李, as supplied
in the official Chinese series rendering. Huamei is one given name, so we use it
without an inserted space or hyphen. Li replaces the inconsistent Lee surname
spelling; Lee is a legitimate alternative, but mixing romanization schemes across
the same character and family creates inconsistency. This is our source-supported
localization, not a claim that an official English edition uses this exact spelling.
Do not infer a birth/baptism story from Maria. See the
[source review](maria_name_source_review_2026_10_06.md), which records the publisher
and licensed-operator sources and their scope.

**Lil Argot:** keep the established spelling, which matches the original Latin
artwork and current translation. No reviewed problem calls for a replacement.
Treat Argot as her proper surname; do not translate its dictionary meaning into
another surname. Source: clean M28 texture 71, which includes both Lil and Camille.

These choices preserve character identity and use national naming conventions as
supporting context. They do not assert historical authenticity for every name.
An explicit usable Latin name normally carries more weight than a reconstructed
spelling; a concrete target-language problem can justify a faithful adaptation,
as with Hodram. Name length or implementation convenience must not decide spelling.

### Implementation status

V204 reconciles the opening **Hodram Joakim Bergstrom** artwork using original
native glyphs. All 22 reveal states, palettes, dimensions, first/last letters and
black shadows pass native checks. See `docs/all_routes_unified_v204_checkpoint.md`.
Other confirmed-name field/text/caption migrations remain pending; this is partial
consistency work, not a completed naming migration.

These are naming decisions, not a claim that the current ROM has been migrated.
The original palette, dimensions, and complete texture indices match between clean,
canonical, and V190 for all three reviewed cards. The active-manuscript inventory
is saved in `work/analysis/original_latin_names_v196.json`.

Regenerate affected dialogue through its route formatter and verify shared-name
allocations and runtime macro lengths. Raphael-to-Rafael changes ASCII pair parity;
Camille increases length while retaining odd parity. Existing formatting and
dropped-leading-character guards remain mandatory. Keeping Hodram preserves its
existing six-byte first-name expansion. Historical V196/V197 Hoodlum research
drafts are not current release instructions. The authoritative policy is
`translations/character_name_localization_policy_v1.json`.
Maria's Lee-to-Li surname change also requires macro-length/parity checks, and
Joachim-to-Joakim requires full-name field/consumer review. Apply the chosen names
consistently to dialogue, shared names, biographies, Gallery captions and artwork.
Only the Hodram opening-artwork correction is integrated so far; the other selected
field/text changes have not yet been compiled into a new playable ROM.

### Other reviewed names

| Japanese | English | Basis |
|---|---|---|
| ヴェルス | Vels | Established Raphael dialogue spelling, including `raphael_deep_route_v89.json`, SC0 block 24 record 8; clean ordinary-name table index 61. |
| アカブー | Akaboo | Phonetic project localization of the clean ordinary-name table index 77. The long final vowel is represented by `oo`; no official Latin spelling is claimed. |

The clean ROM is the primary source for both labels. Supplemental Japanese
[town-event notes](https://w.atwiki.jp/offlinedaikoukai/pages/19.html) identify
アカブー as a town-square character; they do not establish an English spelling.
These choices retain the character names without adding titles or relationships.
