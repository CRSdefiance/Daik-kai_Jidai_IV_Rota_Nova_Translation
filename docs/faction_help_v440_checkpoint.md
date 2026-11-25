# Complete faction HELP and corrected data navigation V440

Experimental candidate:out/all_routes_combined_v440_candidate.nds.
SHA256:1f125b17907fb26b16d6b147795d93c5770c1d9100bd513ae8b1b53b5e590926.
Patch SHA256:23fbf53cb8a55c2e21a3c093103841c1e31771ee966889d504db8693247ecf81.
Profile:all-routes-unified-v440. Canonical baseline remains
out/raphael_natural_v2_accepted_base.nds, SHA256
3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
All470 inherited batches, accepted dependencies and V438 stages are retained.

## Source fidelity

Ten faction articles181–190 replace generic text:overview,home port,home-port
points,Influence,Relations,Allied,At War,Neutral,Subordinate andFriendship. Data
Guide143 now calls destination181 Faction Info, distinguishing it from individual
Fleet Info137. Original Japanese source, neighbors, glosses and individual review
gates accompany natural-dialogue-v2 en-US paragraphs. All eleven native parser/
font previews fit ten rows and were visually reviewed without shortened prose.

Home Port retains the zero-share relocation trigger. Home Port Points retains
one point per flag,the fleet-count bonus and battle/scheme-only capture. Allied
retains possible assistance,not guaranteed assistance. At War retains automatic
engagement,enemy monopoly-city attacks and both investment/combat share methods.
Relations preserves the stated three basic levels and all four referenced pages,
including additional subordination. Subordinate retains successful Threaten and
the established Proof of Conquest term,including both original Threaten links.
Friendship preserves the higher-is-better scale without inventing thresholds.

## Preservation and actual checks

Only COMMON/HELP.DK4 differs from V438. All197 unselected topics,208 identities,
203 sentinel and non-HELP components remain exact. All208 full original archive
loads/guards pass;the clean patch reconstructs the whole candidate exactly.
A fresh ordinary-input boot reaches all eleven pages through Data Guide/Faction
Info and their links. Every first/interior/final glyph and26 constructed original
link widgets passes,including repeated destination33. L/R restores the entire
Subordinate framebuffer pixel-exact. No fixture ROM,savestate,unlock changes or
live RAM injection. Targeted Ruff passes.

## Remaining scope and handoff

Current HELP has no Japanese text,but61 entries exactly match the historical
generic inventory. Other source-fidelity defects remain under audit. Status-provider
native checks remain valid;genuine non-Normal displays/full notices remain open.
All18 plaques and broader legacy/environment/movie/Gallery/equipment requirements
remain incomplete. No canonical promotion. Revisit older record-based checks at
actual full-goal completion.

ROM,patch,manifest and finalized Faction Info/Subordinate captures are copied to E
and hash-verified. User checks:cold boot/New Game;Help -> Data Guide -> Faction Info,
then Influence/Home Port/Friendship/Relations and each relation-state article.
Use L/R history. Candidate is experimental.

Evidence:work/analysis/faction_help_v439/page_proposal.json,
native_archive_history_proof.json and
work/analysis/faction_help_release_v440/release_proof.json. Preparation:
prepare_faction_help_v439.py. Production:faction_help_release.py. Actual verifier:
verify_faction_help_live_v440.py.
