# Initial glossary

| Japanese | Suggested English | Category |
|---|---|---|
| 出航 | Set Sail | menu |
| 交易 | Trade | menu |
| 港 | Port | location |
| 酒場 | Tavern | location |
| 造船所 | Shipyard | location |

Treat these as working terms until verified in game context.

## Complete commodity labels — V636

Use the full labels in `translations/commodity_fidelity_manuscript_v2.json` for
the17 reviewed shared commodity entries. Iron Ore and Copper Ore preserve the
source's 鉱石 distinction; Raw Silk and the three material-specific Cloth names
preserve raw-material versus finished-product meanings. Use Frankincense,
Lacquerware, Whale Meat and Smoked Salmon for the specific products named in source.
Expand legacy display abbreviations to Shark Fins, Cinnamon, Platinum,
Tortoiseshell, Turmeric and Black Wool.

**ヤシ油 → Coconut Oil:** the proposed Palm Oil expansion from P. Oil was rejected
before handoff. ヤシ油 and the separately indexed ココナッツ油 are source-equivalent
coconut-oil terms;both use Coconut Oil without adding a quality,refining or botanical
difference. Their original IDs and gameplay fields remain separate.
References: [MEXT food-composition explanation](https://www.mext.go.jp/b_menu/shingi/gijyutu/gijyutu3/attach/1299201.htm),
[Japan Oilseed Processors Association](https://www.oil.or.jp/kiso/seisan/seisan01_02.html).

The complete table,reasons and scope are in
[V636 commodity checkpoint](commodity_fidelity_v636_checkpoint.md). Other107 existing
commodity labels are retained;this entry does not newly approve every legacy name.

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

Preserve deliberate source nicknames and vocal effects in dialogue. For example,
Claudio calls Rafael **Rafi** (ラフィ) in clean SC2B133R0056. This is a specific
familiar address, not a replacement for the locked Rafael name. Lil deliberately
draws out Camille's name in SC2B159R0161 after he compares someone else's cooking
with hers; the localization retains that vocal effect. Exact source bytes are in
`translations/character_nickname_evidence_v292.json`.

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

The original story provides further direct support: clean `/data/SC2.DK4`,
block121 record410, explains that the nickname began when someone teasingly used
a girl's name because he looked like a girl as a child. Record403 distinguishes
his true name, Marinus Kuhn, from Overijssel, his mother's surname. Camille thus
preserves an intentional nickname with a feminine association in the source;
this does not change his identity or claim that his nationality requires a French
name. Exact clean bytes and source context are recorded in
`translations/camille_nickname_source_evidence_v291.json`.

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


## Verified compact skills (V464)

Use Vigor for生命力,Swords for剣闘術,Speech for説得力 and Guile for謀略術.
These match complete actual native labels and their Japanese meanings. Physical
Health is the separate condition label. Preserve original stat relationships and
thresholds. V462 Sword/Talk visual readings were disproved by complete pixel masks.
See [V464 source and display evidence](skill_terms_v464_checkpoint.md).


## Minor-character surname correction V518

**Yukihisa Genjo Shiraki** retains the full surname **Shiraki** from the clean
シラキ entry. The former central Shira spelling omitted the final kana despite
the complete seven-letter form fitting the original eight-byte slot with NUL.
Runtime portrait captions use Yukihisa Shiraki,consistent with story naming.
The historical source profile remains for reproduction;V518 applies a late
central correction. All locked primary naming decisions remain unchanged.


## V610 village place-name decisions

Use the 24 spellings in [Village name decisions](village_names_v610_decisions.md). レバキュー is Leveque, correcting the former Lebaque spelling in three active Lil records. コルフ is Korf in the source Bering Sea context. Preserve Forel, Ezo and the game's Wanganui spelling as documented. Character-name locks remain unchanged.


## Refit bow sail (V2284)

Use **Spritsail** for スプリットセイル in clean DS COMMON1268/1280 andthe matching component label. The clean bow-fitting context andfollowing-wind benefit identify the sail under the bowsprit. This is a contextual terminology inference,supported by the [publisher Japanese manual](https://www.gamecity.ne.jp/manual/dk4HeN38/jp/3400.html) and[National Historic Ships Manual of Maritime Curatorship,Fittings,p.97](https://www.nationalhistoricships.org.uk/sites/default/files/2023-02/c_fittings.compressed.pdf). The publisher reference is a later-version Japanese manual,not an official English localization. Earlier Split Sail manuscripts are preserved for reproduction. See [source anddisplay review](refit_context_v2294_checkpoint.md).
