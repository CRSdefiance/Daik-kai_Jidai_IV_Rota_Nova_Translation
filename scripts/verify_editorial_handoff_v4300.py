"""Independent V4299 ledger/reference/gameplay preservation audit."""
from collections import Counter
import gzip
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_handoff_verification_v4300')
CHECKPOINT = Path('work/analysis/lil_B170_reference_checkpoint_v4299')
DOC = Path('translations/lil_B170_editorial_manuscript_v6.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    receipt = read(CHECKPOINT / 'checkpoint_receipt.json')
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert sha(ledger_path.read_bytes()) == receipt['ledger_sha256']
    before = json.loads(gzip.decompress((CHECKPOINT / 'ledger.before.json.gz').read_bytes()))
    allowed = {'contextual_story_natural_dialogue_pass_v1871', 'active_source_prose_drafts', 'coverage_units',
               'unfinished_editorial_scope_v4299', 'lil_B170_reference_reconciliation_v4299', 'latest_checkpoint'}
    assert {k: v for k, v in before.items() if k not in allowed} == {k: v for k, v in ledger.items() if k not in allowed}
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    old = before['contextual_story_natural_dialogue_pass_v1871']
    mutable = {'latest_contextual_manuscript', 'latest_pending_contextual_family', 'pending_contextual_families', 'coverage_note'}
    assert {k: v for k, v in old.items() if k not in mutable} == {k: v for k, v in fresh.items() if k not in mutable}
    assert (fresh['fresh_pass_records_explicitly_reread'], fresh['fresh_pass_records_integrated'], fresh['fresh_pass_records_pending_native_actual_release']) == (5725, 5692, 33)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'], ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (5692, 5728, 3614, 2078)
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert receipt['new_source_prose_reviews'] == receipt['new_completed_records'] == 0
    doc, prior = read(DOC), read('translations/lil_B170_editorial_manuscript_v5.json')
    validate_natural_dialogue_batch(doc)
    assert len(doc['records']) == 33
    assert [(r['id'], r['source_hex'], r['current_hex'], r['english'], r['editorial_decision']) for r in doc['records']] == [(r['id'], r['source_hex'], r['current_hex'], r['english'], r['editorial_decision']) for r in prior['records']]
    decisions = Counter(r['editorial_decision'] for r in doc['records'])
    assert decisions == Counter({'revise': 21, 'retain-wording': 12}), decisions
    assert all(r['fresh_retained_wording_justification'] for r in doc['records'] if r['editorial_decision'] == 'retain-wording')
    family = 'Lil-B170-Yifa-collision-apology-Taoist-training-resolve-joining33'
    assert len(fresh['pending_contextual_families']) == 1
    pending = fresh['pending_contextual_families'][0]
    assert pending['id'] == family and pending['manuscript'] == str(DOC) and pending['manuscript_sha256'] == sha(DOC.read_bytes())
    assert len(pending['actual_sampled_display_IDs']) == 33 and not pending['offline_only_display_IDs']
    units = {r['id']: r for r in ledger['coverage_units']}
    assert all(units[row['id']] == row for row in before['coverage_units'] if row['id'] not in [family, 'all-route-scenes'])
    assert units[family]['registered_release_pending'] and units[family]['actual_complete_native_panels'] == 33
    active = ledger['active_source_prose_drafts']
    assert active['route_record_subsets_pending'][str(DOC)] == [r['id'] for r in doc['records']]
    assert active['route_record_subsets_pending'][str(Path('translations/lil_B170_editorial_manuscript_v5.json'))] == []
    for path, digest in receipt['evidence'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    for path, digest in receipt['preserved_release_files'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    for path, digest in receipt['updated_files'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    approval = read(pending['reference_approval'])
    assert approval['manuscripts'] == {str(DOC): sha(DOC.read_bytes())}
    assert approval['new_emulator_runs'] == 4
    mapping = read(doc['reference_map'])
    block = mapping['blocks'][0]
    assert block['block'] == 170 and len(block['command_map']) == 45 and len(block['text_records']) == 33
    assert not block['relative_skip_fixups'] and not block['target_native_skip_cases']
    assert [e['source_offset'] for e in block['original_declared_end_word_maps']] == [1852, 1856]
    assert [e['target_offset'] for e in block['original_declared_end_word_maps']] == [1742, 1746]
    actual = read('work/analysis/lil_B170_actual_v4293/actual_all33_pause_resources_A000_C200_and_first_end.json')
    assert actual['fresh_actual_unique_speech_panels'] == actual['complete_matching_observations'] == 33
    assert not actual['failures'] and not actual['paired_region_differences']
    visual = read('work/analysis/lil_B170_transition_review_v4297/all6_sheets_figure_pause_effect_C200_and_paired_return_review.json')
    assert len(visual['all6_actual_sheets_viewed']) == 6 and len(visual['later67_SeaView_RGB_differences']) == 67
    for row in visual['all6_actual_sheets_viewed']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    repeat = read(doc['focused_repeat_proof'])
    assert repeat['paired_post_B170_town11290_whole1A04_actor_models_and_captain2_equal']
    assert len(repeat['cross_language_speech_timing_differences']) == 22
    assert not any(repeat['same_ROM_later_differing_frames'].values())
    assert all(all(r['component_equality'].values()) for r in repeat['paired_native_persistent_state_and_PRNG_samples'] if r['frame'] <= 16090)
    assert repeat['paired_native_persistent_state_and_PRNG_samples'][0]['source_seed'] == repeat['paired_native_persistent_state_and_PRNG_samples'][0]['English_seed']
    for version in actual['versions']:
        assert version['fixture_exit_frame'] == 11257 and len(version['selected_B22_command_pairs']) == 53
    for case in ['clean_Japanese', 'reviewed_English']:
        for prefix, number in [('display', 4292), ('repeat', 4295)]:
            terminal = read(Path(f'work/analysis/lil_B170_{prefix}_run_v{number}_{case}') / 'terminal.json')
            assert terminal['terminal'] and terminal['observer_host_slots_restored']
    promotion = read('translations/promoted_build.json')
    assert promotion['profile'] == 'all-routes-unified-v4251'
    assert sha(Path(promotion['rom']).read_bytes()) == promotion['rom_sha256'] == 'ff9917225f4e8812ac890973c454a352b5416bee27a7263a5b3258efe9b91b12'
    scope = ledger['unfinished_editorial_scope_v4299']
    assert sha(Path(scope['path']).read_bytes()) == scope['sha256']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4299')
    assert len(ledger_path.read_bytes()) < 100 * 1024 * 1024
    ROOT.mkdir(parents=True)
    save(ROOT / 'verified_handoff.json', dict(checkpoint='V4299', ledger_sha256=sha(ledger_path.read_bytes()),
        fresh_reread=5725, integrated=5692, pending=33, source_prose=5728, revised=3614, retained=2078,
        new_source_prose_reviews=0, new_completed_records=0,
        all33_source_English_decisions_prior_completions_pending_credit_and_wider_scope_preserved=True,
        all33_native_reference_and_actual_display_approved=True, actual_panels=33, actual_new_cold_boot_runs=4,
        both_pause_and_town_whole_RGB_controls_pass=True, first_end1852_actual_second1856_offline_only=True,
        later67_sailing_differences_and22_speech_timing_differences_retained_with_state_PRNG_scope=True,
        original_strict_failures_and_failed_producers_preserved=True,
        promoted_main_V4251_registry_builder_canonical_inputs_and_all_ROMs_preserved=True,
        current_candidate=promotion['rom'], candidate_sha256=promotion['rom_sha256'], remaining_B171_B180_physical_speeches=198,
        registered_B170_compiler_integration_patch_and_startup_pending=True,
        all_jobs_terminal=True, full_goal_active=True, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('Independent V4300 audit passes:V4299,5725 rereads/5692 integrated/33 pending;33 actual panels,four boots;V4251 main preserved. Full goal active.')
