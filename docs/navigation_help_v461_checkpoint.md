# V461 complete linked navigation Help

Experimental; graphics goal active. All22 historical requirements and all18
incomplete plaque entries remain. Previous turn: fifteen interface/ship articles.
This turn: four navigation articles and their original linked paths.

## Source corrections

Route Map104 restores the current sea/faction display, City-level-only display in
regions with unvisited cities, city/fleet data selection, route lines, red-route
Auto Move and world-map zoom/region selection. Touchscreen Sailing101 restores
the normal-sailing context, direction, touch-distance speed and touching the ship
to stop. Both previously had a generic This Topic heading.

Their older inbound articles had lost original hyperlinks. Auto Move76 now
preserves Captain/Surveyor requirements and every endpoint/intermediate-city
market-share condition, with four original links. Manual Movement83 preserves
D-pad/L/R steering, touchscreen link101, sail opening/closing speed effects,
Half Open departure and Full Open action. Automatic Half Open adjustment needs
assigned Sail Handlers at every mast, not ordinary sailors; link125 is restored.
Source-platform square/circle/cross symbols are localized as the corresponding
actions without inventing DS button mappings.

Manuscript: `translations/navigation_help_manuscript_v2.json`, with complete
source locks, neighbors, gloss/context/notes and five reviews per article.

## Evidence

- Four complete native pages and original links compile without prose shortening.
- Every preview was visually reviewed and all211 native archive loads pass.
- Actual normal Help navigation uses Shared Commands→Route Map and
  Deck→Workrooms→Captain/Masts to reach Auto Move and touchscreen sailing.
- All four actual full-glyph pages and seven original link widgets pass.
- Original L/R history restores the whole Manual Movement page pixel exactly.
- All56 title/New Game/story/town/Help-entry frames match V457.
- All207 unselected articles,211 existing IDs, sentinel203 and continuations
  208/209/210 remain exact. Only HELP differs; ARM9, artwork, COMMON and routes
  remain exact with all470 prior batches and stages.
- The clean-ROM patch reconstructs the complete candidate byte for byte.

The known generic marker phrases and This Topic headings are now absent. This
does not establish complete older Help fidelity: source inspection also finds
lost links in74/82/84/89, retained for follow-up. V459 is a superseded unpublished
two-article research version; V461 retains the full V457 parent stack.
These are targeted automated DeSmuME tests, not hardware, a full playthrough or
independent proof of every sailing mechanic. Broader graphics/legacy contexts,
occupied equipment, Gallery/endings and all plaque audits remain open.

## Handoff

ROM: `all_routes_combined_v461_candidate.nds`

SHA-256: `e437cb89df1bcad464d4488aa66ac1e472e3573f540e4ecc10f74cd5aad53073`

Patch SHA-256: `4493d7d7a99a2ce771c9e6f6bad62a834f5f4d4b1565bce6d23ae5af2cddb01e`

Profile: `all-routes-unified-v461`, all470 inherited batches and every V457 stage,
plus `translations/navigation_help_release_v2.json`. Delta from V457:
`/COMMON/HELP.DK4`. Canonical base remains
`out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
No canonical promotion is made.

Verifiers: `verify_navigation_help_release_v461.py`,
`verify_navigation_help_live_v461.py`,211 native archive loads and targeted Ruff.
Proof: `work/analysis/navigation_help_release_v461/release_proof.json`.
Actual report: `work/emulation_v193/navigation_help_v461/capture_report.json`.
User cold-boot areas: title/New Game, town and Help Route Map, Captain→Auto Move,
Masts→Manual Movement→Touchscreen Sailing, including history controls.

ROM, exact patch, manifest and three verified guide captures are on
`E:\Rota Nova translations`. Revisit older record-based checks at true completion.
