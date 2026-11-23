"""Register the reviewed Tavern Help articles and their original links."""

from inspect import getsource
from pathlib import Path

from scripts import register_palace_help_20261120 as earlier
from scripts import register_recruit_crew_20261120 as parent
from scripts import replay_tavern_help_20261120 as replay
from scripts import stage_tavern_help_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = parent.base, parent.batch
PROFILE = 'all-routes-tavern-help-v1-20261120'
ROOT = Path('out/tavern_help_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Tavern_Help_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_tavern_help_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_tavern_help_registered_20261120.md')
STARTUP, QA = (stage.ROOT / n for n in ('own_startup_verification.json', 'qa.xml'))
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
CHECKPOINT = 'Tavern Help now uses Recruit Crew, Schemes and the live scheme names in all nine revised pages.'
GLOSSES = {
    11: 'Use buildings’ signs for town commands. City-only commands require City status. The original links list the main buildings and other town options, including ruins.',
    12: 'Recruit sailors and gather information at the Tavern. Religious restrictions leave many towns in Arab cultural regions without a tavern, so replacement sailors are harder to find and battles are risky.',
    13: 'Order a drink for 5 to 10 gold to learn about nearby towns and other factions. Women at city taverns are knowledgeable and may reveal an item’s whereabouts.',
    14: 'Buy drinks for the room. Hear about towns and other factions and sometimes items. Treating everyone before recruiting improves turnout.',
    15: 'Recruit sailors for your ships. More developed towns attract more at once and cost more to recruit in. Dismiss extras on the spot. Treating the room helps turnout. Assign recruits to individual ships afterward.',
    16: 'A Strategist’s idea enables a scheme against another faction. It costs 1,000 gold and can fail. Another faction is required locally. Except for forged documents, you must have visited a town where a rival holds market share.',
    17: 'Lure another faction’s fleet toward a chosen town in the current sea region.',
    18: 'When there are multiple other factions, choose two and create forged documents to turn them hostile toward each other.',
    19: 'Choose one town in the region and spread damaging rumors there. It reduces the target faction’s local share. A Strategist with insufficient ability will not come up with the plan.',
    20: 'Choose a town in the current sea region where a rival holds share. Bribe a local broker to take some of that faction’s share. The Strategist needs sufficient ability to think of this plan.',
    118: 'The Tactics Room houses a Strategist with Guile of at least 120. An idea unlocks Tavern schemes. The officer can foil enemy plans and obtains information about other factions when the crew stays at an Inn.',
    139: 'Assign sailors to ships. Need, Now and Max are displayed. Left and Right change the current count, and Auto offers priority to the flagship, equal ratios or minimum staffing. Ships short of required crew sail more slowly.',
}

source = checked_text(getsource(earlier.verify), {
    "== {35, 37}": "== {15, 16}",
    "assert len(records) == 9": "assert len(records) == 12",
    "stage.reference(after[stage.HELP], final[n], n)": "stage.earlier.reference(after[stage.HELP], final[n], n)",
})
template = earlier.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 949 and len(manifest["checks"]) == 284':
        'len(manifest["batches"]) == 951 and len(manifest["checks"]) == 286',
    'release_stack_before_palace_help.json': 'release_stack_before_tavern_help.json',
    'release_stack_with_palace_help.json': 'release_stack_with_tavern_help.json',
    'verified_load_confirmation_predecessor=predecessor, palace_help_release=str(REVIEW)':
        'verified_recruit_crew_predecessor=predecessor, tavern_help_release=str(REVIEW)',
    'registered_palace_help_and_complete_parent_inverse': 'registered_tavern_help_and_complete_parent_inverse',
    'manifest["palace_help_pipeline"]': 'manifest["tavern_help_pipeline"]',
    'reviewed_UI_labels=6, previously_localized_records=9, new_contextual_records=0, prose_revisions=6':
        'reviewed_UI_labels=9, previously_localized_records=12, new_contextual_records=0, prose_revisions=9',
    'ordinary_palace_help_9_pages=True, continuation_backlinks_and_history=True':
        'ordinary_tavern_help_9_pages=True, command_links_and_history=True',
    'ledger["palace_help_20261120"]': 'ledger["tavern_help_20261120"]',
    'prior_records_reviewed=9, actual_help_pages=9, new_contextual_credit=0,\n        prose_revisions=6':
        'prior_records_reviewed=12, actual_help_pages=9, new_contextual_credit=0,\n        prose_revisions=9',
    'Preserve the Palace Help candidate or reconstruction': 'Preserve the Tavern Help candidate or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Tavern Help testing candidate

The [testing ROM](../../{ROM.as_posix()}) updates nine Tavern and Tactics Room Help pages to match the live commands. The [clean-input patch](translation.xdelta) recreates ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Tavern Help and its menu labels

Tavern Help now uses **Recruit Crew**, **Schemes**, **Lure Fleet**, **Forge Papers**, **Bad Rumors**, and **Bribe** just as they appear in the game. **Treat Everyone** connects buying a round to recruiting, **Recruit Crew** links to **Assign Sailors**, and the **Tactics Room** links back to **Schemes**. The revisions preserve the town conditions, the 1,000-gold cost and the Forge Papers exception. Three related articles retain their wording. [Exact source and individual decisions](../{REVIEW.as_posix()})

All nine revised pages passed native glyph, wrapping and bounds checks and were opened in one ordinary emulator replay. Both the Assign Sailors history return and the Tactics Room backlink returned to the expected complete page. This pass covered Help navigation. Hardware and Tavern transactions were outside the replay. [Native and emulator evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters and 17 focused tests passed. The clean-input patch reconstructs the cumulative candidate byte for byte. The ledger retains 27,700 credited reviews and 276 stored shared keys open for display-owner review. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = earlier.env | globals()
exec(compile(source, __file__ + '::verify-tavern-help', 'exec'), env)
exec(compile(program, __file__ + '::register-tavern-help', 'exec'), env)


if __name__ == '__main__':
    env['main']()
