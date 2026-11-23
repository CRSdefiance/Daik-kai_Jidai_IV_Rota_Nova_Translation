"""Register the complete Palace Help review over the current cumulative candidate."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_amsterdam_tavern_editorial_20261120 as startup_check
from scripts import register_load_confirmation_20261120 as parent
from scripts import replay_palace_help_20261120 as replay
from scripts import stage_palace_help_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = parent.base, parent.batch
PROFILE = 'all-routes-palace-help-v1-20261120'
ROOT = Path('out/palace_help_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Palace_Help_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_palace_help_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_palace_help_registered_20261120.md')
STARTUP, QA = (stage.ROOT / n for n in ('own_startup_verification.json', 'qa.xml'))
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
CHECKPOINT = 'Palace Help matches all six menu commands and keeps the revised contract rules and headings on their original linked pages.'
GLOSSES = {
    25: 'Trends increase prices. They arise naturally or a Missionary can start one. Large sales may earn share or, under an exclusive contract, a letter that can open otherwise unavailable contracts.',
    35: 'The Palace or Governor’s Office provides contracts and military investment. The six original links identify these and the two letter, lending and reclaim commands.',
    36: 'Buy 1 to 20 units. The number of units determines the share that allows trade. A town cannot sign with you when it has three contracts or the other factions hold all shares.',
    37: 'Buy 1 to 20 units of military investment at half the Arms rating in gold per unit, or 40 percent for Rafael. It increases Arms and can raise share when there is space or an enemy owns share. High Arms reduces surrender and unlocks better ships and guns.',
    38: 'Present a Letter of Introduction from the Market to the ruler or governor in a Port. Gain five points with a contract, or make a contract by taking one point if all share is held. Three factions already contracted or your own 100 percent share prevents use.',
    39: 'Present a Market Letter of Recommendation to the ruler or governor in a town of any size. Gain ten points with a contract, or make a contract by taking one point if all share is held. The three-faction and own 100 percent restrictions still apply.',
    40: 'Lend an item to the ruler or governor at your home port. Monthly rent depends on item value. Proofs of Conquest, Proof Maps and Ancient Maps cannot be lent.',
    41: 'Reclaim a loaned item at the palace or governor’s office in your home port.',
    149: 'Arms measures how heavily a town is armed. Military investment at the Palace or Governor’s Office raises it. A higher rating makes surrender less likely when the town is attacked.',
}


def verify(registry, previous, viewed):
    stored, game, plan = map(base.load, (stage.PROOF, replay.LIVE, stage.PLAN))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == game['research_ROM_sha256']
    assert base.digest(parent.ROM) == previous['candidate_sha256'] == stored['parent_sha256']
    assert base.digest(stage.CLEAN) == previous['clean_input_sha256'] == stored['clean_input_sha256']
    assert stored['complete_parent_inverse']
    assert stored['clean_input_patch_byte_exact'] and base.digest(stage.ROOT / 'translation.xdelta') == stored['clean_input_patch_sha256']
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    assert all(base.digest(path) == sha for doc in (stored, game) for path, sha in doc['evidence'].items())
    assert viewed == {r['path']: r['sha256'] for r in stored['sheets'] + game['readable_actual_sheets']}
    assert all(base.digest(path) == sha for path, sha in viewed.items())
    assert game['actual_ordinary_controls_no_state_injection'] and not game['hardware'] and not game['offline_only_pages']
    original_pages = stage.ARTICLES.keys() | stage.CHILDREN.values()
    assert game['actual_pages'] == len(original_pages) == 9
    assert {r['topic_id'] for r in game['actual_HELP_cases']} == original_pages
    assert {p['topic'] for p in game['original_forward_back_andL_R_history_returns']} == {35, 37}
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [17, 0, 0, 0]

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.HELP}
    arm = after[stage.ARM]
    assert batch.digest(arm) == previous['target_ARM9_sha256'] == stored['target_ARM9_sha256']
    assert batch.digest(after[stage.HELP]) == plan['target_HELP_sha256'] == stored['target_HELP_sha256']
    prior, final = (IlnkContainer.parse(files[stage.HELP]).blocks for files in (before, after))
    assert len(prior) == len(final) == 217 and prior[203] == final[203] == b'\0'
    assert {i for i, (was, now) in enumerate(zip(prior, final, strict=True)) if was != now} == original_pages
    assert plan['owned_topic_ids'] == sorted(original_pages) and plan['all_original_links_andcomplete_logical_prose_exact']
    new.replace_file(stage.HELP, before[stage.HELP])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    earlier = base.load(parent.REVIEW)
    assert earlier['unchanged_pending_records'] == 276
    check_startup = FunctionType(startup_check.startup_proof.__code__, startup_check.startup_proof.__globals__ |
                                 {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})
    check_startup(previous, candidate, arm)

    records = stored['records']
    assert len(records) == 9 and [r['topic_id'] for r in records if r['decision'] == 'revision'] == sorted(stage.ARTICLES)
    for r in records:
        n = r['topic_id']
        assert prior[n].hex() == r['current_source_hex']
        assert all(final[p['topic_id']].hex() == p['encoded_hex'] and p['native_display']['all_executed_current_instruction_bytes_exact']
                   for p in r.get('native_pages', []))
        r['registered_reference'] = stage.reference(after[stage.HELP], final[n], n) | {'candidate_sha256': candidate}
        r['source_meaning'] = GLOSSES[n]
        r['review']['formatting'] = True
    draft = dict(candidate_sha256=candidate, parent_sha256=previous['candidate_sha256'], records=records,
        translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=list(stage.GATES), checked_story_format_guard=controls, preserved_217_topics_and_original_link_targets=True,
        exact_menu_terms=stored['exact_menu_terms'], unchanged_pending_records=276,
        shared_storage_scope=earlier['shared_storage_scope'], observed_gameplay=game, new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.HELP: batch.digest(after[stage.HELP])}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 948 and len(manifest["checks"]) == 283':
        'len(manifest["batches"]) == 949 and len(manifest["checks"]) == 284',
    'stage.PROOF, STARTUP, QA, stage.GAME, args.visual_review,':
        'stage.PROOF, stage.PLAN, STARTUP, QA, replay.LIVE, replay.NAV, args.visual_review,',
    'release_stack_before_load_confirmation.json': 'release_stack_before_palace_help.json',
    'release_stack_with_load_confirmation.json': 'release_stack_with_palace_help.json',
    'verified_tavern_round_digits_predecessor=predecessor, load_confirmation_release=str(REVIEW)':
        'verified_load_confirmation_predecessor=predecessor, palace_help_release=str(REVIEW)',
    'registered_load_confirmation_and_complete_parent_inverse': 'registered_palace_help_and_complete_parent_inverse',
    'manifest["load_confirmation_pipeline"]': 'manifest["palace_help_pipeline"]',
    'if file == stage.COMMON:': 'if file == stage.HELP:',
    'native_and_emulator_evidence_sha256=base.digest(stage.GAME)': 'native_and_emulator_evidence_sha256=base.digest(replay.LIVE)',
    'owned_text_slot=stored["changed_call"], target_ARM9_sha256=archives[stage.ARM]':
        'owned_help_pages=base.load(stage.PLAN)["owned_topic_ids"], target_HELP_sha256=archives[stage.HELP]',
    'changed_components=1, target_ARM9_sha256=archives[stage.ARM]': 'changed_components=1, target_HELP_sha256=archives[stage.HELP]',
    'ARM9_sha256=archives[stage.ARM]': 'ARM9_sha256=previous["target_ARM9_sha256"]',
    'reviewed_UI_labels=1, previously_localized_records=1, new_contextual_records=0, prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0':
        'reviewed_UI_labels=6, previously_localized_records=9, new_contextual_records=0, prose_revisions=6, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3',
    'ordinary_title_Continue_and_in_game_Load=True, declined_and_accepted_branches=True':
        'ordinary_palace_help_9_pages=True, continuation_backlinks_and_history=True',
    'ledger["load_confirmation_20261120"]': 'ledger["palace_help_20261120"]',
    'prior_records_reviewed=1, actual_paired_states=4, new_contextual_credit=0,\n        prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0, text_display_revisions=0':
        'prior_records_reviewed=9, actual_help_pages=9, new_contextual_credit=0,\n        prose_revisions=6, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3, text_display_revisions=0',
    'Preserve the Load confirmation candidate or reconstruction': 'Preserve the Palace Help candidate or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Palace Help testing candidate

The [testing ROM](../../{ROM.as_posix()}) revises six Palace Help articles on nine pages. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Palace Help and its menu labels

Six Palace Help articles now use the menu's action names, including **Introduction**, **Recommendation** and **Reclaim**. The two letter articles explain when you can sign a contract and how many percentage points you gain. **Military Investment** fits on one heading line and keeps its cost, effects and Rafael's rate. The loan article restores the governor as a possible recipient. Three surrounding articles retain their wording. [Exact Japanese, references and individual decisions](../{REVIEW.as_posix()})

All nine revised pages passed original parser, glyph, word-wrap, bounds and pagination checks. An ordinary emulator run reached all nine through the original widgets. The Military Investment backlink and Help history returned to the expected full pages. The test covers the Help screens. Hardware and new transaction tests were outside this pass. [Emulator and native pages](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters and 17 focused tests passed. The clean-input patch reconstructs the cumulative candidate exactly. The ledger retains 27,700 credited reviews and 276 stored shared records to classify. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
