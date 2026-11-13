# Latin-name migration research and native card verification

## V203: Maria's native fields and default name macros verified

The missing Maria widget test now passes through a documented selection fixture:
four fields, 246 exact font pixels and a complete 14,144-pixel portrait. Her actual
player object expands FI/FA/FO/FU to Maria/Li/Li Clan/Maria Huamei Li, with byte
lengths 5/2/7/15. The prepared Maria FI/FA/FO profiles agree. This closes the missing
native field/default-name evidence; full text/artwork migration remains pending,
and the test-only selector is not a legitimate unlock or release layer. See
[V203 evidence](maria_native_widgets_v203.md).

## V201: all 25 remaining name capacities have research solutions

The catalog passes exact canonical/clean locks and a complete four-route scope
audit: 128,492 segments, only the 25 intended records, no conflicting matches.
528 lookup cases, 105 actual-player native copies, 62 negative checks and startup
ownership pass. All 25 previews were reviewed, four source/context wording issues
corrected, and a cold-boot long-message smoke matches 817 complete native ink pixels.
Together with V199's two B44 cases, all 27 capacity failures have research solutions.
Original-scene checks, broader reviews and registered integration remain unfinished.
V190 remains the latest candidate. [Current evidence and full scope](confirmed_name_catalog_v201.md).

## V199: two B44 allocations verified through native continuation

The previous goal turn made progress on the five-field implementation, native
widgets and complete source preparation. This turn revalidates the historical
Lisbon relocation constraints against the immutable current source and verifies
the two blocked B44 records through actual cold boots.

The exact pre-Lisbon rollback matches the old map's SC0/block hashes. Both old and
current blocks have **500 logical segments** and identical per-record parity.
Outside the 106 historically movable segments, only the length header and the two
same-size choices differ; their 8/14-byte allocations remain unchanged. The
research probe updates all 15 selected-name records in B44. R0210 and R0327 each
gain two bytes, with original parity retained, for a **four-byte block growth**.
Every other SC0 block, other resource and ARM7 component remains exact to V190;
ARM9 carries only the previously guarded name-field changes.

Actual captures show the complete resized dialogue:

- R0210: Rafael is asked whether he has asked his father for help.
- R0327: Rafael Castor is assigned leadership of Castor Co., the ship and fleet.

All **five lines / 1,237 ink pixels** and their blank cells match the native font
exactly, including first and last glyphs. The observed speakers are Janus Pasar
and Julio Erneco. Default FI/FA/FO expansion is visible as Rafael/Castor/Castor Co.

Both protected tutorial branches execute: **Ask him** enters the trading-post
tutorial; **Prepare alone** returns directly to Lisbon. Both later reach sailing.
The same longer-input V190 control also reaches sailing. The brief frame-scheduled
input run stopped earlier than either resized record; a names-only probe reproduces
that wait without B44 resizing. A later longer press and a one-frame shift of the
brief pulses both resume progression. This is responsive, timing-sensitive test
input; its exact polling mechanism is not established and no permanent VM halt is
inferred from that trajectory.

Evidence: `work/analysis/confirmed_names_v199/b44_revalidation_report.json`,
`b44_current_source_inherited_map.json`, `resized_record_native_pixels.json` and
`b44_cold_boot_proof.json` in the same folder. Implementation:
`scripts/revalidate_confirmed_name_b44_v199.py`; focused Ruff passes. All runs are
explicit research-only, with no savestates or callback errors. The two allocation
solutions are now verified for research; **25 allocation cases remain unresolved**.
No new registered candidate, patch or baseline promotion was made.

### Remaining allocation strategy investigation

The native expander at 02053914 supports FI, FA, FO, FU and its existing pronoun
handling; it does not provide a ready-made short NPC-name token. No new macro or
glyph abbreviation was introduced. Native message-dispatch call sites 020242C8,
02024310 and 02024330 pass text through this expander using a 1,024-byte stack
buffer. A scoped full-string lookup at this copy stage is an option to investigate
for the remaining short utterances while preserving script instruction boundaries.
This is source evidence and an implementation lead, not an executed or approved
runtime change. Required source guards, actor/control preservation, cache/startup
ownership, exact output and native tests remain mandatory.

The full graphics scope remains: all pending names/text/artwork consistency,
preview/editorial and Maria checks, unfinished Online source text, unresolved
graphics storage/context/native/gameplay work, and one registered combined ROM
with an exact patch. V190 remains the latest registered candidate; goal active.

## V198 confirmed-name implementation and current preparation

The naming choices are now user-confirmed; see `docs/glossary.md`. The previous
goal turn made progress by settling Camille and recording all rationales. This
turn implements a source-locked five-field transform in
`dk4tool/patch/confirmed_character_names.py`: Rafael, Camille, Joakim, Maria's Li
surname and Huamei middle name. Exact clean Japanese slots and sole table references
are guarded. Pointers, instructions, auxiliary/staged sections and unrelated bytes
remain exact. The original complete V190 is the required input.

`scripts/verify_confirmed_name_fields_v198.py` executes real native startup/pool
copying and all three ordinary name accessors for 207 indices. **621 selections**
pass: five intended fields change and **616 other outputs remain exact**. Evidence:
`work/analysis/confirmed_names_v198/native_fields_report.json`. This is native
fixture evidence, not a standalone integrated release.

`scripts/prepare_confirmed_name_text_v198.py` prepares **448 source-locked records**:
183 literal-name changes and 265 default-name macro cases, including **59 baked
canonical records**. Clean Japanese and neighboring context are attached. The
current Rafael FI/FU and Maria FA lengths are modeled without changing historical
profiles or disabling guards. Logical-paragraph formatting and the existing
balanced formatter resolve **34 full-first-row/phase-wrap cases**.

**27 byte-allocation failures remain**, including very short Camille utterances.
They are saved in `work/analysis/confirmed_names_v198/allocation_backlog.json`.
Two B44 records have historical mapped movable segments, but that map still needs
revalidation against the current source. Five native COMMON/help records need their
own consumer/reblocking review. Do not shorten the confirmed names or bypass gates.

An overly narrow fallback initially misdecoded the baked B141 R0107 speaker byte
97 with the first A of Admiral. Its clean and canonical leading bytes agree; an
existing registered Raphael route calibration already supports that state. The
preparation now reuses that calibration and preserves 97 as a speaker token.
No new global byte rule or game rendering defect is claimed from this decoder
observation. Its complete updated preview is readable; native scene checks remain.

Clean B125 source and following dialogue also revealed an older name-only greeting
that omitted Admiral and introduced leading whitespace. The unregistered editorial
override now reads `Admiral {MACRO:FA}!`, naturally preserving the source title and
recognition greeting. Source/context/localization/naturalness are reviewed;
formatting/native integration approval is still pending. The corrected preview
shows complete `Admiral Li!` within bounds.

There are **416 offline previews on 35 sheets**. Two current individual previews
were inspected after regeneration; the remaining visual/editorial work stays open.
Macro text in previews represents declared defaults, not proof of live expansion.
Reports/drafts/previews are under `work/analysis/confirmed_names_v198/` and
`work/qa/confirmed_names_v198/`. Drafts are unregistered and their unreviewed gates
remain false. Focused Ruff checks pass for the five new implementation scripts/modules.

### Actual changed-name widget captures

An explicitly research-only NDS carries the five name-field changes on the complete
V190 stack. Every filesystem resource, ARM7 and other non-ARM9 component is exact.
It is **not registered for handoff or normal gameplay**, because the text/macro
migration is incomplete. Four isolated cold-boot runs finish without callback
errors or savestates. Three intended widgets are visually inspected and match the
entire native font mask, including all blank cells and first/last letters:

| Widget | Exact ink pixels | Bounds, exclusive right/bottom |
|---|---|---|
| Rafael, captain confirmation | 80 | [89, 220, 125, 231] |
| Joakim, captain middle-name field | 78 | [89, 242, 125, 253] |
| Camille Overijssel, opening nameplate | 196 | [16, 276, 124, 287] |

The attempted Maria navigation returned to Rafael; it does **not** verify her
middle/surname widgets or prove she is unavailable under all conditions. Determine
the legitimate selection/input/unlock path or use a documented native widget
fixture. Evidence: `work/analysis/confirmed_names_v198/widget_pixels_report.json`;
captures: `work/emulation_v193/confirmed_name_widgets_v198/`.

The latest registered candidate remains **V190**. No new integrated ROM/patch or
acceptance was claimed. Full naming/text/artwork consistency, structural allocation
work, complete reviews, Maria verification and all other graphics-goal work remain.

## Historical V197 three-name proposal

**Policy update, 2026-10-06:** retain Hodram. The Hoodlum substitution and SC1
macro-length change evaluated below are superseded. The 450-record/42-failure
figures describe the historical three-name proposal, not the currently required
migration. Source ownership and native original-card evidence remain valid.
Follow `translations/character_name_localization_policy_v1.json` for current choices.

## Progress classification

The preceding goal turn made progress: it resolved the user's naming preference,
verified original cards and changed the authoritative glossary. This turn adds
native name ownership/getter proof, source-locked migration drafts, formatting
failure evidence and complete real-emulator lettering comparisons. The goal
remains active and incomplete. No playable ROM or accepted layer changed.

## Shared names and affected text

`scripts/research_latin_name_migration_v197.py` verifies clean Japanese owners:
ordinary table index 0, Rafael (12-byte slot); index 1, Hoodlum (12-byte slot);
index 9, Camille (8-byte slot). The exact terminated names fit; each has its one
expected static ARM9 table reference. An isolated ARM9 research result preserves
all pointers, code and auxiliary sections/staged payload.

The actual native startup/pool copier and ordinary getter execute for all 207
entries. Three complete outputs change as intended and 204 remain exact. This is
scoped native machine execution, not a playable spelling-migration release.

The saved research report is
`work/analysis/latin_name_migration_v197/report.json`. Its 450 source-locked draft
records cover 187 literal-name changes and 263 default-name macro cases. All 445
progressive fixed records pass their original encoding checks; proposed changes
produce **30 byte-overflow and 12 pair-phase/auto-wrap failures**. Five native
COMMON/help records need their own consumer/reblocking review. Draft review gates
are false and drafts are explicitly unregistered; generated substitutions do not
inherit an editorial approval.

Do not ship shortened names or disable guards to make these records fit. Resolve
the complete names through reviewed logical prose, safe formatting and relocation
where necessary. Terminal scene-caption/Gallery data, baked canonical records,
actual macro expansion proof, previews and integrated-build checks also remain.

## Original name-card native evidence

Two fresh V190 cold boots used the workspace-local DeSmuME core, no savestates,
no injected memory and no scripted input. Captures are in
`work/emulation_v193/v190_latin_opening/` (14,000 frames) and
`work/emulation_v193/v190_latin_opening_fine/` (2,900 frames, capture every 10).
Both finish with no callback errors and the exact V190 ROM hash.

`scripts/verify_original_latin_cards_native_v197.py` compares all nonblack original
glyph and outline pixels with native five-bit framebuffer colors:

| Source texture | Complete names | Frame | Exact pixels | Lettering bounds, exclusive right/bottom |
|---|---|---|---|---|
| 22 | Rafael Castor | 1520 | 1,613/1,613 | [7, 98, 126, 117] |
| 46 | Hoodlum Joakim Bergstrom | 2080 | 2,599/2,599 | [14, 168, 246, 186] |
| 71 | Camille Overijssel; Lil Argot | 2680 | 2,920/2,920 | [8, 104, 210, 153] |

All complete leading/trailing source lettering is included and lies within the
256×192 top display. Transparent/black backing and unowned scene pixels are not
asserted to match. Later frame 2720 changes ten dim pixels at the surname's right
edge while bright lettering remains exact; the temporal cause is unclassified
and saved explicitly, not excluded from the complete-frame comparison.

The proof is `work/analysis/original_latin_cards_native_v197.json`. Selected-frame
source fidelity does not prove every animated crop/alpha or physical hardware.

## National naming plausibility

The user's follow-up asks whether the names fit their nationalities. Original
Latin artwork establishes fictional-character spelling; it does not establish
that every spelling is a typical real-world national name.

- Rafael appears in Portugal's official [given-name list](https://irn.justica.gov.pt/Portals/33/Regras%20Nome%20Proprio/Lista%20Nomes%20Pr%C3%B3prios.pdf?ver=WNDmmwiSO3uacofjmNoxEQ%3D%3D).
- Camille is a real name borne by men and women in France, documented by
  [INSEE](https://www.insee.fr/fr/statistiques/9040114). The Dutch form Camiel is
  documented in [Meertens material republished by Ensie](https://www.ensie.nl/betekenis/camiel).
- Joakim and Bergström occur in [Swedish name statistics](https://www.namntips.se/fornamn/Joakim/).
  Hoodlum is also an English word for a violent criminal, documented by
  [Cambridge](https://dictionary.cambridge.org/dictionary/english/hoodlum). Treating
  it as an invented/atypical character name is an inference; no proof that the
  publisher made a spelling mistake was found.

The [original publisher's character introduction](https://www.gamecity.ne.jp/products/products/ee/new/dai4/dai4_02.htm)
confirms Rafael's Portuguese background, Hoodlum's Swedish naval role and Lil's
Dutch/Amsterdam setting with Camille. This research does not authorize inventing
replacement character identities. Existing original-Latin naming decisions remain.
