# Eight connected HELP articles V434

Experimental candidate:out/all_routes_combined_v434_candidate.nds.
SHA256:6bca9b67d985dfa5effadddaa636388f9d4d4a867c9cc67507a7c2e967fa183c.
Patch SHA256:0d64968cf6187718d4cf14613b1f7e9472b34c89d75f5b1b051844214cc389a0.
Profile:all-routes-unified-v434. Canonical baseline remains
out/raphael_natural_v2_accepted_base.nds, SHA256
3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
All470 inherited batches, accepted dependencies and all V430 stages remain.

## Complete source-faithful prose

The seven remaining Japanese HELP topics21/23/103/105/127/134/144 now cover Market,
Commercial Investment, Shared Commands, Deck, Holds, Info and City Info. Town
Commands11 is also restored from its generic placeholder so Market is reachable.
Commercial Investment retains1–20 units, cost equal to half Growth, both market-share
conditions and the possibility of additional specialties. Deck retains eligibility
requirements and greater effectiveness with higher abilities. X/Menu localization
uses ordinary city input and V328's observed normal sea-menu sequence.

All eight manuscripts have clean/canonical/current source locks, neighboring
context, faithful glosses, localization notes and five per-record review gates.
Compiler-owned wrapping fits every article in ten rows without shortening prose.
Eight original native parser/font previews pass and were reviewed.

## Source-link extraction correction

The Japanese map glyph contains Shift-JIS trail byte7D, which resembles an ASCII
closing brace. A plain byte-pattern parser missed Route Map104 and Ancient Maps142.
New help_source_links walks whole Shift-JIS units before recognizing delimiters;
all202 original topics parse and both exact original destinations survive. The old
six-article V430 and seven-article V432 compiler bytes remain reproducible.
V432 was superseded before handoff because it lacked the Town Commands prerequisite.

## Registered release and actual checks

Only COMMON/HELP.DK4 differs from V430. All non-HELP components/artwork/routes are
exact; all198 unselected HELP topics,206 IDs and203 sentinel are exact. The clean
patch reconstructs the whole ROM. A fresh ordinary-input boot follows Help Index
through Town Commands/Market/Investment, Shared Commands/Deck/Holds/Info and City
Info. All actual first/interior/final glyphs and47 constructed link destinations
pass. L/R history returns the complete City Info framebuffer pixel-exact.
No fixture ROM, savestate, unlock change or live RAM injection. Targeted Ruff passes.

The character-aware current census finds no remaining Japanese HELP topic text.
It still finds76 entries exactly matching the historical generic inventory. This
is not full source-fidelity clearance or full HELP completion. Linked destinations
outside the eight reviewed articles and the broader graphics/legacy/environment/
movie/Gallery/equipment gates remain open. All18 plaques stay fully_completed:false.
No canonical promotion. Revisit older record-based checks at actual goal completion.

ROM, patch, manifest and finalized Town Commands/Investment captures are copied to
E and hash-verified. Suggested user test: cold boot/New Game; open Help and follow
Town Commands -> Market -> Commercial Investment, then Shared Commands -> Deck/
Holds/Info; exercise L/R history and City Info. Candidate remains experimental.

Evidence:work/analysis/help_navigation_v433/page_proposal.json and
work/analysis/general_help_release_v434/release_proof.json. Preparation:
scripts/prepare_help_navigation_v433.py. Actual verifier:
scripts/verify_general_help_live_v434.py. Production:general_help_release.py v2.
