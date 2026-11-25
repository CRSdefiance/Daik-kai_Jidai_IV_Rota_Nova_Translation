"""Register the five revised lines in Rafael's ordinary Tavern recruitment lesson."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import check_rafael_tavern_lesson_20261119 as game
from scripts import register_rafael_deck_after_trade_20261119 as parent
from scripts import review_rafael_tavern_lesson_20261119 as staged
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = parent.base, parent.native, parent.workflow
stage = SimpleNamespace(ROOT=staged.STAGED, ROM=staged.ROM, PROOF=staged.PROOF, review=staged, ARM=native.ARM)
PROFILE = 'all-routes-rafael-tavern-lesson-v1-20261119'
ROOT = Path('out/rafael_tavern_lesson_registered_20261119_v2')
ROM = ROOT / 'Translation_DS_Rafael_Tavern_Lesson_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_rafael_tavern_lesson_candidate_v2')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_rafael_tavern_lesson_20261119.md')
STARTUP, QA = game.STARTUP, stage.ROOT / 'registered_qa.xml'
verified = SimpleNamespace(PROOF=game.PROOF, LIVE=game.PROOF)
CHECKPOINT = 'Julio’s Tavern recruitment lesson has five revised lines, with all seven panels and the Flagship assignment verified in ordinary Lisbon gameplay.'
ROW_COUNT_NOTES = {10: 'The advice and its reason each fit one complete line in English.'}

verification = checked_text(getsource(parent.verify), {
    "assert live['ordinary_gameplay_existing_save'] and live['native_lesson_event_after_Trade'] and not live['hardware']":
        "assert live['ordinary_gameplay_existing_save'] and not live['hardware']",
    "assert live['fully_displayed_live_name_and_regular_F'] and live['speakerless_system_page_exact']":
        "assert live['prior_and_current_exact_joined_speaker'] == 'Julio Erneco'",
    "len(live['pairs']) == 12 and live['command_count'] == 16": "len(live['pairs']) == 7 and live['command_count'] == 10",
    'parent.stage.parent.stage.verify_runtime(arm,previous)': 'parent.parent.stage.parent.stage.verify_runtime(arm,previous)',
    '{SC0:[43]}': '{SC0:[138]}',
    'if x != y] == [43]': 'if x != y] == [138]',
    'parent.stage.PENDING': 'parent.parent.stage.PENDING',
    "for row in draft['records']) == 3": "for row in draft['records']) == 5",
    'b[43]': 'b[138]',
    'block=43': 'block=138',
    '''            assert {item['code'] for item in plan['diagnostics']} == {'line-break-count'}
            r['compiled_lines'] = plan['lines']
            r['qa_waivers'] = ['line-break-count']
            r['qa_waiver_reason'] = ROW_COUNT_NOTES[r['source_reference']['record_index']]''':
        '''            warnings = {item['code'] for item in plan['diagnostics']}
            idx = r['source_reference']['record_index']
            assert warnings == ({'line-break-count'} if idx in ROW_COUNT_NOTES else set())
            r['compiled_lines'] = plan['lines']
            if warnings:
                r['qa_waivers'] = ['line-break-count']
                r['qa_waiver_reason'] = ROW_COUNT_NOTES[idx]''',
})

publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 924 and len(manifest["checks"]) == 259':
        'len(manifest["batches"]) == 925 and len(manifest["checks"]) == 260',
    'verified_town_shortage_predecessor': 'verified_deck_after_trade_predecessor',
    'previously_localized_records=12': 'previously_localized_records=7',
    'prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=9':
        'prose_revisions=5, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=2',
    'text_display_revisions=3': 'text_display_revisions=5',
    'ordinary_Rafael_Trade_exit_and_complete_Deck_lesson=True': 'ordinary_Rafael_Tavern_recruitment_and_assignment=True',
    'rafael_deck_after_trade': 'rafael_tavern_lesson',
    'Preserve Deck After Trade ROM or reconstruction': 'Preserve the Rafael Tavern Lesson ROM or reconstruction',
    'glob("staged_v*")': 'glob("staged_tavern_v*")',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael Tavern recruitment test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Tavern lesson and all earlier candidate fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael's Tavern recruitment lesson

All seven Julio turns were reviewed against clean Japanese. Five revisions explain getting underway, treating the room, finding enough sailors, assigning them and the cost of hiring beyond what the fleet needs. The exact Recruit Crew wording and Julio's final invitation are retained with individual reasons. [Source and current references](../{REVIEW.as_posix()})

Two cold boots from the preserved Lisbon save triggered the original Tavern lesson. All seven panels and Julio nameplates matched the native renderer in both builds. The revised replay chose Recruit Crew, applied Flagship in Assign Sailors, accepted the unassigned crew prompt and returned to the Tavern menu. [First three revisions](../{VERIFY.as_posix()}/recruitment_comparison_1.png) · [Last two revisions](../{VERIFY.as_posix()}/recruitment_comparison_2.png)

Only Rafael's Tavern lesson changes. The patch reconstructs the candidate from the clean ROM byte for byte. Six startup holds, 24 protected name getters and 49 focused tests passed. Two historical fixtures skipped. The 276 pending shared records carry forward. Hardware testing remains open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(verification, __file__ + '::verify', 'exec'), env)
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
