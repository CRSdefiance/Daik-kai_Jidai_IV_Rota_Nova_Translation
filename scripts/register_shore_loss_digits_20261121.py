"""Register the source-bound Search sailor-loss count fix."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_shore_loss_digits_20261121 as live
from scripts import register_sailing_help_20261120 as startup_release
from scripts import register_shore_phrase_wraps_20261121 as parent
from scripts import stage_shore_loss_digits_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = parent.base, parent.batch
PROFILE = 'all-routes-shore-loss-digits-v1-20261121'
ROOT = Path('out/shore_loss_digits_registered_20261121_v1')
ROM = ROOT / 'Translation_DS_Shore_Loss_Digits_20261121_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261121_shore_loss_digits_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_shore_loss_digits_registered_20261121.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'qa.xml'
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
RUNTIME_ID = 'DK4_SEARCH_SAILOR_LOSS_ASCII_DIGITS'
CHECKPOINT = 'The Search sailor-loss notice now uses regular-width digits, with the original crew loss and sailing return verified.'
PENDING = parent.PENDING


def verify(registry, previous, viewed):
    stored, native, actual = map(base.load, (stage.PROOF, live.NATIVE, live.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == native['candidate_sha256'] == actual['candidate_sha256']
    assert stored['parent_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert stored['complete_parent_inverse'] and stored['exact_clean_patch_reconstruction']
    assert stored['patch_sha256'] == base.digest(stage.PATCH)
    assert stage.REBUILT.read_bytes() == stage.ROM.read_bytes()
    assert viewed == {s['path']: s['sha256'] for s in (native['sheet'], actual['sheet'])}
    assert all(base.digest(p) == v for p, v in (viewed | actual['evidence'] | stored['source_evidence']).items())
    assert actual['actual_emulator'] and actual['expected_complete_native_ink'] and actual['unchanged_effect_and_return']
    assert not actual['hardware'] and actual['original_loss'] == 11 and actual['unchanged_other_screen_captures'] > 40
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [17, 0, 0, 0]
    clean, old, image = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(stage.CLEAN) == previous['clean_input_sha256'] == stored['clean_input_sha256']
    before, after = map(batch.files, (old, image))
    assert before.keys() == after.keys()
    assert {key for key in before if before[key] != after[key]} == {stage.ARM}
    arm, common = after[stage.ARM], after[stage.COMMON]
    assert (arm, stored['call']) == stage.patch(before[stage.ARM], clean.read_file(stage.ARM))
    assert batch.digest(arm) == stored['target_ARM9_sha256']
    assert batch.digest(common) == stored['target_COMMON_sha256'] == previous['target_COMMON_sha256']
    image.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    portrait = parent.stage.portrait
    directory = batch.digest(arm[portrait.DIRECTORY_OFFSET:portrait.TABLE_OFFSET])
    installed = portrait.owned_entries(common, arm, directory)
    pending = base.load(PENDING)['records']
    assert len(pending) == 276
    for row in pending:
        now = installed[row['message_ID']]
        assert portrait.reference(now) == row['current_reference'] and now.text.hex() == row['current_hex']
    guards = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guards)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    starter = startup_release.env['startup_check'].startup_proof
    FunctionType(starter.__code__, starter.__globals__ | {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})(
        previous, candidate, arm)

    record, = native['records']
    now = installed[stage.MESSAGE]
    assert record['message_ID'] == stage.MESSAGE and record['current_hex'] == now.text.hex()
    assert portrait.reference(now) == record['current_reference'] and now.text.count(b'%s') == 1
    assert record['decision'] == 'retention' and len(native['numeric_ring_checks']) == 384 and len(record['render_cases']) == 12
    assert all(case['complete_font_bounds_and_buffer_guards'] and case['pages'] == 1 for case in record['render_cases'])
    record['registered_reference'] = record['current_reference'] | {'candidate_sha256': candidate}
    record['gameplay_observed'] = True
    draft = dict(translation_policy=native['translation_policy'], target_locale=native['target_locale'],
                 encoder=native['encoder'], review_gates=native['review_gates'], records=[record],
                 candidate_sha256=candidate, parent_sha256=previous['candidate_sha256'],
                 original_observation=str(stage.LEAD), native_validation=str(VERIFY / live.NATIVE.name),
                 checked_story_format_guard=controls, unchanged_pending_records=276,
                 shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'], binding=stored['call'],
                 focused_replay=actual, visual_review_receipt=viewed, new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.ARM: stored['target_ARM9_sha256']}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
old_ids = template[template.index('    for row in draft["records"]:'):template.index('    manifest["shore_phrase_wraps_pipeline"]')]
program = checked_text(template, {
    'len(manifest["batches"]) == 956 and len(manifest["checks"]) == 291':
        'len(manifest["batches"]) == 957 and len(manifest["checks"]) == 292',
    'stage.PROOF, STARTUP, QA, live.PROOF, args.visual_review,': 'stage.PROOF, STARTUP, QA, live.NATIVE, live.LIVE, args.visual_review,',
    'release_stack_before_shore_phrase_wraps.json': 'release_stack_before_shore_loss_digits.json',
    'release_stack_with_shore_phrase_wraps.json': 'release_stack_with_shore_loss_digits.json',
    'verified_deck_predecessor=predecessor, shore_phrase_wraps_release=str(REVIEW)':
        'verified_shore_predecessor=predecessor, shore_loss_digits_release=str(REVIEW)',
    'registered_shore_phrase_wraps_and_complete_parent_inverse': 'registered_shore_loss_digits_and_complete_parent_inverse',
    'manifest["shore_phrase_wraps_pipeline"]': 'manifest["shore_loss_digits_pipeline"]',
    old_ids: '''    row, = draft["records"]
    assert (row["file_path"], row["id"]) in credited
    assert RUNTIME_ID not in manifest["changed_records"][stage.ARM]
    manifest["changed_records"][stage.ARM].append(RUNTIME_ID)
''',
    'base.digest(live.PROOF)': 'base.digest(live.LIVE)',
    'owned_message_IDs=sorted(stage.EDITS), target_COMMON_sha256=archives[stage.COMMON]':
        'owned_digit_call=stored["call"], target_ARM9_sha256=archives[stage.ARM]',
    'changed_components=1, target_COMMON_sha256=archives[stage.COMMON]':
        'changed_components=1, target_ARM9_sha256=archives[stage.ARM]',
    'previously_localized_records=41, new_contextual_records=0, prose_revisions=9, spacing_revisions=0, wrap_only_revisions=2, justified_retentions=30':
        'previously_localized_records=1, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1',
    'name_label_revisions=0, text_display_revisions=0, pagination_fixes=0':
        'name_label_revisions=0, text_display_revisions=1, pagination_fixes=0',
    'focused_shore_attack=True, normal_sailing_return=True, variant_selector_restored=True':
        'paired_search_crew_loss=True, regular_digits_observed=True, normal_sailing_return=True, variant_selector_restored=True',
    'ledger["shore_phrase_wraps_20261121"]': 'ledger["shore_loss_digits_20261121"]',
    'prior_records_reviewed=41, actual_gameplay_records=1, new_contextual_credit=0,\n        prose_revisions=9, spacing_revisions=0, wrap_only_revisions=2, justified_retentions=30, text_display_revisions=0':
        'prior_records_reviewed=1, actual_gameplay_records=1, new_contextual_credit=0,\n        prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1, text_display_revisions=1',
    'Preserve the shore phrase-wrap candidate or reconstruction': 'Preserve the Search sailor-loss candidate or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Search sailor-loss digit testing candidate

The [testing ROM](../../{ROM.as_posix()}) displays the Search crew-loss count in the regular English font. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Search sailor-loss count

The Search notice **Sailors lost: 11.** now displays the count in the regular English font. The existing English and its single substitution remain intact. All five original Search callers share the same crew-loss routine and notice. The fix redirects its one number-format call. [Exact review and binding](../{REVIEW.as_posix()})

Paired DeSmuME runs used the same copied save, shoreline setup and temporary attack-variant selection. The before and after runs both removed 11 sailors and returned to the same sailing screen. Other Search outcomes and hardware were outside the replay. Offline checks covered 384 number-buffer cases and 12 complete, visually reviewed layouts. [Emulator comparison](../{(VERIFY / live.GAME_SHEET.name).as_posix()})

Six startup holds, 24 protected getters and 17 focused tests passed. The clean-input patch reconstructs the candidate byte for byte. Only the four-byte ARM9 call changes. All 114 accepted layers carry forward. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register-shore-loss-digits', 'exec'), env)


if __name__ == '__main__':
    env['main']()

