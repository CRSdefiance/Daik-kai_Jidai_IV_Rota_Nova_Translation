"""Register the revised Auto Move and at-sea Help on the Tavern Help release."""

from pathlib import Path

from scripts import register_tavern_help_20261120 as parent
from scripts import replay_sailing_help_20261120 as replay
from scripts import stage_sailing_help_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = parent.base, parent.batch
PROFILE = 'all-routes-sailing-help-v1-20261120'
ROOT = Path('out/sailing_help_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Sailing_Help_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_sailing_help_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_sailing_help_registered_20261120.md')
STARTUP, QA = (stage.ROOT / n for n in ('own_startup_verification.json', 'qa.xml'))
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
CHECKPOINT = 'Auto Move and at-sea Help now explain the route requirements, target controls, and mode shortcuts.'
GLOSSES = {
    73: 'Replenish water and food before sailing. Accept an equal fill to capacity or decline and set the proportions yourself.',
    74: 'Depart offers manual sailing, Auto Move and Deck View.',
    75: 'Sail with the player controlling the ship.',
    76: 'Travel automatically to a chosen town. Requires a captain and surveyor. The Route Map must connect the towns, '
        'and your faction needs share at both ends and each stop. Valid routes are red.',
    77: 'Open the same Deck View provided by Shared Commands.',
    82: 'Lists the nine original Help links for actions, encounters and information at sea and shared commands.',
    83: 'Use the D-pad to steer and shoulder buttons to adjust sail angles. Touchscreen steering is available. '
        'Open or close the sails to adjust speed. Leave port half open, with automatic angles when all masts are staffed.',
    84: 'Follow the route automatically. Cancel with the DS back-and-confirm action and resume manual sailing. Auto Move '
        'cannot restart at sea. With the Eagle Figurehead, time advances faster and A restores normal time.',
    85: 'Pause sailing to view town and ship information. Use Info as the entry to Search and Declare War.',
    86: 'From Info, use Y or R to enter Search and A to search the surroundings. Finds include water, food or items. '
        'An unsuccessful search adds 3 fatigue to the sailors. They may desert or be attacked by animals.',
    87: 'From Info, press Y twice or L and pick a town or fleet to start a battle. The faction relationship becomes war '
        'and Friendship falls sharply. Available town commands are limited when you declare war there. Allied fleets are excluded.',
}

source = checked_text(parent.source, {
    'len(original_pages) == 9': 'len(original_pages) == 4',
    '== {15, 16}': '== {76, 85}',
    'assert len(records) == 12': 'assert len(records) == 11',
    'stage.earlier.reference(after[stage.HELP], final[n], n)':
        'stage.original.reference(after[stage.HELP], final[n], n)',
})
template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 951 and len(manifest["checks"]) == 286':
        'len(manifest["batches"]) == 952 and len(manifest["checks"]) == 287',
    'release_stack_before_tavern_help.json': 'release_stack_before_sailing_help.json',
    'release_stack_with_tavern_help.json': 'release_stack_with_sailing_help.json',
    'verified_recruit_crew_predecessor=predecessor, tavern_help_release=str(REVIEW)':
        'verified_tavern_help_predecessor=predecessor, sailing_help_release=str(REVIEW)',
    'registered_tavern_help_and_complete_parent_inverse': 'registered_sailing_help_and_complete_parent_inverse',
    'manifest["tavern_help_pipeline"]': 'manifest["sailing_help_pipeline"]',
    'reviewed_UI_labels=9, previously_localized_records=12, new_contextual_records=0, prose_revisions=9, '
    'spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3':
        'reviewed_UI_labels=3, previously_localized_records=11, new_contextual_records=0, prose_revisions=4, '
        'spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7',
    'ordinary_tavern_help_9_pages=True, command_links_and_history=True':
        'ordinary_sailing_help_4_pages=True, command_links_and_history=True',
    'ledger["tavern_help_20261120"]': 'ledger["sailing_help_20261120"]',
    'prior_records_reviewed=12, actual_help_pages=9, new_contextual_credit=0,\n        prose_revisions=9, '
    'spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3':
        'prior_records_reviewed=11, actual_help_pages=4, new_contextual_credit=0,\n        prose_revisions=4, '
        'spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7',
    'Preserve the Tavern Help candidate or reconstruction': 'Preserve the Sailing Help candidate or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Sailing Help testing candidate

The [testing ROM](../../{ROM.as_posix()}) updates four Help pages for Auto Move, Info, Search and Declare War. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Auto Move and at-sea Help

Auto Move now describes the town and market-share requirements along the whole route. Info and Search explain the targeting and confirmation controls verified in Rafael's tutorial. Declare War keeps both shortcuts and explains what changes when you attack a town or another faction. Seven related articles retain their exact wording. [Clean Japanese, current references and individual decisions](../{REVIEW.as_posix()})

All four revised pages passed original parsing, glyph, wrap, bounds and link checks. A cold-boot emulator run opened all four through the original Help UI. Auto Move returned from Route Map through history, and both Search and Declare War linked back to Info. This replay covers Help navigation. The earlier sailing and tutorial evidence verifies the controls cited by the articles. [Emulator and native pages](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters and 17 focused tests passed. The clean-input patch reconstructs the cumulative candidate exactly. It retains all 114 accepted layers and the ASCII right-bound correction. The ledger still records 27,700 credited reviews and 276 open stored shared entries. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(source, __file__ + '::verify-sailing-help', 'exec'), env)
exec(compile(program, __file__ + '::register-sailing-help', 'exec'), env)


if __name__ == '__main__':
    env['main']()
