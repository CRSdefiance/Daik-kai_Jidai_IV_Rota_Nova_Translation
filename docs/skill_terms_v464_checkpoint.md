# V464 Help terminology matches verified live skills

Experimental; graphics goal active. All22 historical requirements and all18
incomplete plaque entries remain. Previous turn: normally rested/prepared fleet.
This turn corrects Help terminology from complete live pixel evidence.

## Observation correction and glossary

The tiny V462 screenshot was misread as Sword and Talk. Full native masks prove
Swords (77 ink pixels,including10 final-s pixels),Speech80,Vigor57 and Guile62.
Talk has no matching mask. The runtime ten-entry dictionary is Vigor,Command,
Sailing,Survey,Finance,Swords,Aim,Speech,Guile,Observe. Evidence:
`work/analysis/skill_terms_v463/UI_term_proof.json`. This supersedes the V462
visual-reading note. No live missing-letter or label inconsistency is claimed.

| Source | Compact skill name | Reason |
| --- | --- | --- |
| 生命力 | Vigor | Vitality,maxHP and resilience;distinct from physical Health condition. |
| 剣闘術 | Swords | Swordsmanship proficiency;preserve the complete established label. |
| 説得力 | Speech | Persuasive/diplomatic ability,not generic sociability. |
| 謀略術 | Guile | Cunning and schemes,not only battle tactics. |

Thirteen Help articles use these names instead of Health,Combat,Social,Tactics.
Physical Health160 remains exact;Sailor Info158 retains its Health link and names
HP and Vigor168 distinctly. Source meaning,roles,attribute relationships,links
and all16 numeric requirements remain. Runtime labels/artwork are unchanged.
Manuscript: `translations/skill_terms_help_manuscript_v1.json`.

## Presentation and verification

Existing HP208 and requirements209 continuations are reused with exact parent
source locks. All211 IDs,sentinel203,crew210 and196 unselected articles remain.
All15 native previews were reviewed;all211 native archive loads pass. All15
actual full-glyph pages and39 original link widgets pass. Both continuation
returns and L/R history restore whole pages exactly. All56 earlier title/New
Game/story/town/Help-entry frames match V461. Only HELP differs;all470 inherited
batches/stages,ARM9,artwork,COMMON,routes and prepared battery stay exact.
The clean-ROM patch reconstructs the candidate byte for byte.

Tests are targeted DeSmuME evidence,not hardware or full gameplay. Older Help
links,legacy/environment/Gallery/endings,equipment and plaque audits remain open.

## Handoff

ROM: `all_routes_combined_v464_candidate.nds`

SHA-256: `fe4b6a4ec6081bfb39bb22aa6d88c5047d5983248f343b91c6939a721d028f2b`

Patch SHA-256: `e86cfbcd3fd26dea84f9203c0faf7c04d108e7b226d366b027afc45b43148c32`

Profile: `all-routes-unified-v464`, all470 prior batches/every V461 stage plus
`translations/skill_terms_help_release_v1.json`. Delta: `/COMMON/HELP.DK4`.
Canonical: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
No promotion. User cold-boot areas: title/New Game,town,HP/Vigor and skill Help,
requirements and continuation/history controls.

Verifiers: `verify_skill_terms_release_v464.py`,`verify_skill_terms_live_v464.py`,
211 native archive loads,live UI term masks and targeted Ruff.
Proof: `work/analysis/skill_terms_release_v464/release_proof.json`.
Actual report: `work/emulation_v193/skill_terms_v464/capture_report.json`.
ROM,patch,manifest and two guide captures are on E. Revisit older record-based
checks at true full-goal completion.
