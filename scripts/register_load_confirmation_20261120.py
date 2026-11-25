"""Register the verified Load confirmation over the cumulative Tavern release."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_amsterdam_tavern_editorial_20261120 as startup_check
from scripts import register_tavern_round_digits_20261120 as parent
from scripts import stage_load_confirmation_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = stage.base, stage.batch
PROFILE = 'all-routes-load-confirmation-v1-20261120'
ROOT = Path('out/load_confirmation_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Load_Confirmation_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_load_confirmation_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_load_confirmation_registered_20261120.md')
STARTUP = stage.ROOT / 'own_startup_verification.json'
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
QA = stage.ROOT / 'qa_supported.xml'
CHECKPOINT = 'Title-screen Continue and in-game Load now ask “Load this save?” in the registered candidate.'


def verify(registry, previous, viewed):
    stored, game = map(base.load, (stage.PROOF, stage.GAME))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == game['candidate_sha256']
    assert base.digest(parent.ROM) == previous['candidate_sha256'] == stored['parent_sha256'] == game['parent_sha256']
    assert base.digest(stage.CLEAN) == previous['clean_input_sha256'] == stored['clean_input_sha256']
    assert stored['whole_parent_inverse'] and stored['clean_input_patch_byte_exact']
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.ROOT / 'translation.xdelta') == stored['clean_input_patch_sha256']
    assert viewed == game['sheets'] and viewed[str(stage.NATIVE_SHEET)] == stored['native_sheet_sha256']
    assert all(base.digest(p) == sha for p, sha in (viewed | game['evidence']).items())
    assert [r['frame'] for r in game['holds']] == list(stage.HOLDS) and game['selected_save_preserved']
    assert game['cancelled_to_slot_list'] == [3000, 6200] and game['accepted_to_same_Lisbon_screen'] == [3800, 7000]
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [17, 0, 0, 0]

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.ARM}
    old_arm, arm = (files[stage.ARM] for files in (before, after))
    assert stage.patch(old_arm, clean.read_file(stage.ARM)) == arm
    assert batch.digest(arm) == stored['target_ARM9_sha256']
    assert batch.digest(after[stage.COMMON]) == previous['target_COMMON_sha256'] == stored['target_COMMON_sha256']
    new.replace_file(stage.ARM, old_arm)
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    assert arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET] == old_arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]
    old_review = base.load(parent.REVIEW)
    assert old_review['unchanged_pending_records'] == 276

    check_startup = FunctionType(startup_check.startup_proof.__code__, startup_check.startup_proof.__globals__ |
                                 {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})
    check_startup(previous, candidate, arm)
    snapshot = base.load(STARTUP)['read_only_snapshot']
    assert base.digest(snapshot['path']) == snapshot['sha256']
    start = stage.OFFSET
    end = start + stage.SPAN
    assert Path(snapshot['path']).read_bytes()[start:end] == arm[start:end]
    record, = stored['records']
    assert old_arm[start:end].hex() == record['current_hex'] and arm[start:end].hex() == record['staged_hex']
    record['registered_reference'] = record['current_reference'] | dict(candidate_sha256=candidate,
        ARM9_sha256=batch.digest(arm), exact_stored_hex=record['staged_hex'])
    draft = dict(candidate_sha256=candidate, parent_sha256=previous['candidate_sha256'],
        translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=batch.GATES, records=[record], checked_story_format_guard=controls,
        unchanged_pending_records=276, shared_storage_scope=old_review['shared_storage_scope'],
        observed_gameplay=game, new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.ARM: batch.digest(arm)}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 947 and len(manifest["checks"]) == 282':
        'len(manifest["batches"]) == 948 and len(manifest["checks"]) == 283',
    'stage.PROOF, STARTUP, QA, game.NATIVE, game.GETTER, game.PROOF, args.visual_review,':
        'stage.PROOF, STARTUP, QA, stage.GAME, args.visual_review,',
    'release_stack_before_tavern_round_digits.json': 'release_stack_before_load_confirmation.json',
    'release_stack_with_tavern_round_digits.json': 'release_stack_with_load_confirmation.json',
    'verified_hamburg_ceramics_predecessor=predecessor, tavern_round_digits_release=str(REVIEW)':
        'verified_tavern_round_digits_predecessor=predecessor, load_confirmation_release=str(REVIEW)',
    'registered_tavern_round_digits_and_complete_parent_inverse': 'registered_load_confirmation_and_complete_parent_inverse',
    'manifest["tavern_round_digits_pipeline"]': 'manifest["load_confirmation_pipeline"]',
    'native_display_sha256=base.digest(game.PROOF)': 'native_and_emulator_evidence_sha256=base.digest(stage.GAME)',
    'owned_number_call=stored["changed_call"], target_ARM9_sha256=archives[stage.ARM], owned_common_slots=stored["COMMON_allocations"]':
        'owned_text_slot=stored["changed_call"], target_ARM9_sha256=archives[stage.ARM]',
    'changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON]':
        'changed_components=1, target_ARM9_sha256=archives[stage.ARM]',
    'MESFILE_sha256=archives[stage.COMMON]': 'MESFILE_sha256=previous["target_COMMON_sha256"]',
    'repository_tests=30, legacy_fixture_tests_skipped=2, reviewed_UI_labels=0, previously_localized_records=11, new_contextual_records=0, prose_revisions=4, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7':
        'repository_tests=17, legacy_fixture_tests_skipped=0, reviewed_UI_labels=1, previously_localized_records=1, new_contextual_records=0, prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0',
    'name_label_revisions=0, text_display_revisions=1, pagination_fixes=0':
        'name_label_revisions=0, text_display_revisions=0, pagination_fixes=0',
    'ordinary_Amsterdam_Tavern_round=True, declined_and_accepted_branches=True,\n                                       six_alternate_price_lines_offline=True':
        'ordinary_title_Continue_and_in_game_Load=True, declined_and_accepted_branches=True',
    '''    ledger["amsterdam_tavern_round_20261120"].update(
        separate_pending_price_glyph=False, registered_correction=str(REVIEW))
    checkpoint = CHECKPOINT''': '    checkpoint = CHECKPOINT',
    'ledger["tavern_round_digits_20261120"]': 'ledger["load_confirmation_20261120"]',
    'prior_records_reviewed=11, actual_paired_states=6, new_contextual_credit=0,\n        prose_revisions=4, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7, text_display_revisions=1':
        'prior_records_reviewed=1, actual_paired_states=4, new_contextual_credit=0,\n        prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0, text_display_revisions=0',
    'Preserve the Tavern round candidate or reconstruction': 'Preserve the Load confirmation candidate or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Load confirmation testing candidate

The [testing ROM](../../{ROM.as_posix()}) uses **Load this save?** in title-screen Continue and in-game Load. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Load confirmation

Title-screen Continue and in-game Load now ask **Load this save?** after the player selects an occupied slot. This matches **Select a save to load** above the list and keeps the original Japanese question and the original Yes/No control. The text remains one line in its existing terminated slot. [Exact source, wording decision and native proof](../{REVIEW.as_posix()})

Paired ordinary emulator replays verified all four prompts and both answers in each menu. No returned to the list, and Yes loaded the same Lisbon screen. Only the changed letters differed across the confirmation frames. Nine control frames and the original cartridge-save donor matched byte for byte. Hardware was outside this pass. [Emulator comparison](../{(VERIFY / stage.GAMEPLAY_SHEET.name).as_posix()}) · [Complete native pages](../{(VERIFY / stage.NATIVE_SHEET.name).as_posix()})

Six startup frames, 24 protected getters and 17 focused tests passed. The clean-input patch recreates the cumulative ROM byte for byte. The ledger remains at 27,700 credited records with 276 stored shared keys open for display-owner review. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
