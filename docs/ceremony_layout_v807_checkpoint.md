# V807: ceremony paragraphs and complete native font review

The 52-entry ceremony draft now has prospective formatting evidence for all
21 site names, all four original protagonist given names, and synthetic custom
names of every length from 1 through 23. All 202 original-native printf/layout
cases preserve complete words within four rows of 35 cells. Their 202 complete
228-by-64 font planes independently match the game font, including blank space
and first/final letters. All 17 contact sheets were visually inspected.

## English refinement

Notice 290 was an unrelated trade-good placeholder in V803. Its first ceremony
draft restored the correct meaning but stranded an article with a long custom
name. The V2 paragraph reads:

> %s and the others were drawn into an unfamiliar spiritual world. It was a remarkable experience.

This retains the source group's experience of being drawn into an unknown
spiritual world. It is one authored paragraph, with no manual alignment or line
breaks. The other 51 draft records, source glosses and decisions are unchanged.
The initial 92-case finding and both superseded drafts remain available.

## Evidence scope

Current manuscript: `translations/ceremony_editorial_manuscript_v2.json`.
Final research: `work/analysis/ceremony_layout_v807_name_bounds/`.
`research_report.json` records exact manuscript, candidate, context, producer and
image hashes. `native_given_names.json` records the original given-name getters;
the saved admiral is Hodram. Synthetic name lengths are formatting stress inputs,
not actual earned states or player names.

Ordinary dialogue and protagonist reactions use the existing LITERAL helper
directly. Modal notices use the existing balanced modal path through an explicit
ID348 proxy. This establishes the prospective native formatting and font output;
it does **not** enable the ceremony IDs in production or prove their actual
dispatcher, portraits, pagination, effects, dismissal or scene transitions.
Shared refusal 64 remains byte-for-byte unchanged in the ROM; its other consumers
still need an audit before any presentation change. Every draft formatting gate
remains false pending production verification.

## Bounded runtime work next

The exact proposed ordinary, yes/no and four-protagonist memberships require a
174-byte table under the existing encoding. Together with the existing 24-byte
phrase index array and alignment, this needs 200 bytes; the proven private data
allocation is 168 bytes. The existing modal wrapper occupies 124 of its 128
bytes. These are measurements, not permission to extend either allocation.
`runtime_size_measurement.json` records the seven parent contracts and exact added
IDs/tables. The next step is a source-owned placement or encoding design, with
preservation tests for all existing parents, phrases and modal selections.
No generic zero run is assumed free and no pool, section, cache or arena grows.

V803 and its exact reconstructable patch remain current and unchanged. No new
ROM was built and no new ceremony gameplay was run. The ledger remains at 550
completed COMMON entries, 605 source/prose reviewed and 55 pending, including the
three older 750-752 contexts. Registered integration, complete native copies and
representative actual ceremony scenes remain required. The full editorial goal
and separate graphics/18-plaque audit stay unfinished.
