# V449 faithful crew jobs and whole-entry requirements

Experimental; full graphics goal active. The previous turn was progress on28
sea/sailor data articles. This turn restores27 Deck/crew articles106–133
(excluding the already reviewed Holds127) and corrects seven related Sailor Info
articles to use the established native role glossary.

## Source fidelity and terminology

The old room pages included placeholders and unrelated item/trading text. The
replacement preserves each room's job, minimum skill, benefit, restriction and
original link. Examples: Surgeon needs Observe150; Chief Cook needs Aim70;
Captain accepts only the main character; every mast must have a Sail Handler for
automatic sail adjustment at Half Open; Cargo Holds have a five-room maximum.
Purser buying/selling conditions, belief-based Chapel refusal, lookout sniping,
Deckhand fatigue and all other source qualifications are retained.

Seven V447 articles now consistently name Surgeon, Chief Cook, First Mate,
Purser, Sail Handler and Boarding Leader, matching the16-entry native role table
verified in V326. The existing runtime role strings and artwork are unchanged.
The source platform triangle instruction is localized to the existing Auto
action, without asserting a different hardware button binding.

`translations/crew_help_manuscript_v1.json` contains clean/canonical/current source
locks, source neighbors, gloss, context, localization notes and five review gates
for every article. Prose remains one paragraph without authored line breaks.

## Requirements formatting

All16 minimum values match the Japanese table in original order. An opt-in
`semicolon-entries-v1` formatter keeps each job, skill and number on one row.
Eight entries appear on each of two pages, with continuation209 and a return link.
This prevents Animal Keeper from being split across pages. Oversized entries,
single-entry lists and unknown layout policies fail closed. Ordinary paragraph
formatting remains unchanged; the full inherited build still reproduces every
earlier stage's pinned output.

## Actual evidence and limits

- All34 reviewed articles produce35 native pages; every preview was reviewed.
- All210 archive topics load completely with original guards/history behavior.
- All35 actual pages have complete first/interior/final glyph pixels.
- All45 actual link widgets, including16 on Workrooms, match original destinations.
- List continuation/return and L/R history restore whole pages pixel exactly.
- All56 title/New Game/story/town/Help-entry frames match V447.
- All175 unselected articles, existing209 IDs, sentinel203 and HP continuation208
  remain exact. Only HELP differs from V447; all artwork and ARM9 remain exact.
- The clean-ROM patch reconstructs the complete candidate byte for byte.

These are targeted automated DeSmuME tests, not hardware or full gameplay testing
of every job benefit. Ten remaining legacy Help marker matches need source review.
The actual footer still displays Japanese 前/次/最初; source/consumer tracing and
localization of those labels remain pending. The guide captures document verified
article content, not a claim that every footer caption is already English.
All22 historical requirements and all18 incomplete plaque entries remain.

## Handoff

Candidate: `all_routes_combined_v449_candidate.nds`

SHA-256: `6fe86cb220af43b903f7764e3d5cd859853d92ab6eac0211e9a34ff06f91b870`

Patch SHA-256: `ff275cd6c9a116d8527c0d008c88a380e3e8b425a65b21a8e8aa0d82169351c4`

Profile `all-routes-unified-v449` retains all470 inherited batches and every V447
stage, plus `translations/crew_help_release_v1.json`. Changed internal file from
V447: `/COMMON/HELP.DK4`. Canonical base remains
`out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
No canonical promotion is made.

Verifiers: `verify_crew_help_release_v449.py`, `verify_crew_help_live_v449.py`,
210 native loads through `verify_help_archive_v281.py`, and targeted Ruff.
Proof: `work/analysis/crew_help_release_v449/release_proof.json`.
Actual report: `work/emulation_v193/crew_help_v449/capture_report.json`.
User cold-boot areas: title, New Game/opening, town and Help→Shared Commands→Deck,
Personnel, Workrooms, Holds, Ability Requirements and related Sailor Info articles.

ROM, exact patch, manifest and three verified article screenshots are saved to
`E:\Rota Nova translations`. Revisit older record-based checks at true completion.
