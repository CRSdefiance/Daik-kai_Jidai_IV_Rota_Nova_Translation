"""Preserve clean B199 progress and paired-label context without integration credit."""
import argparse
import gzip
import json
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B199_native_checkpoint_v5794')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5795')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5777/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Lil_B199_source_prose_native_approved_uncredited_v5794'
SCOPE='unfinished_editorial_scope_v5794'
PREVIOUS='previous_latest_checkpoint_before_B199_native_v5794'
OLD_SCOPE='unfinished_editorial_scope_v5776'
COUNTERS=dict(records_editorially_completed=6232,records_with_source_and_prose_pass=6235,
              records_revised_and_integrated=3917,retained_wordings_editorially_completed=2315)
PACKET=Path('work/analysis/lil_B199_source_v5767/all31_clean_current_complete_context.json')
GLOSS=Path('work/analysis/lil_B199_clean_context_v5765/all31_clean_portrait_chase_found_book_and_misunderstood_gift_glosses.json')
CONTEXT=Path('work/analysis/couple_context_review_v5775/five_whole_source_contexts_paired_label_draft_and_B199_name_fields.json')
CENSUS=Path('work/analysis/couple_speaker_uses_v5773b/all_four_routes_direct_role_speech_census_and_complete_native_exchanges.json')
GETTERS=Path('work/analysis/couple_name_consumers_v5774/four_current_native_role_getters_and_exact_staged_owners.json')
from scripts.lil_B199_checkpoint_text_v5794 import SUMMARY,NEXT

def inverse(value):
    old=deepcopy(value)
    old['latest_checkpoint']=old.pop(PREVIOUS)
    old.pop(KEY);old.pop(SCOPE)
    return old

def check(plan,applied=False):
    for item in plan['files']:
        assert sha(Path(item['target']).read_bytes())==item['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(item['planned']).read_bytes())==item['planned_sha256']
        assert sha(gzip.decompress(Path(item['before']).read_bytes()))==item['before_sha256']
    for p,digest in plan['evidence'].items():assert sha(Path(p).read_bytes())==digest
    old=json.loads(gzip.decompress(Path(plan['files'][0]['before']).read_bytes()))
    new=read(plan['files'][0]['planned'])
    assert inverse(new)==old
    assert sha(encode_ledger(old))==plan['files'][0]['before_sha256']
    assert new['current_integrated_candidate']==old['current_integrated_candidate']
    assert all(new[k]==old[k]==v for k,v in COUNTERS.items())
    assert new['goal_status']=='active' and not new['full_goal_complete']
    prior=read(PRIOR)
    assert prior['ledger_sha256']==plan['files'][0]['before_sha256']
    for key in ['candidate','patch']:
        assert sha(Path(prior[key]).read_bytes())==prior[key+'_sha256']
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return new

def stage():
    assert not ROOT.exists() and not VERIFY.exists()
    before=LEDGER.read_bytes();old=json.loads(before);prior=read(PRIOR)
    assert sha(before)==prior['ledger_sha256']
    assert not any(k in old for k in [KEY,SCOPE,PREVIOUS])
    packet,gloss,context,census,getters=map(read,[PACKET,GLOSS,CONTEXT,CENSUS,GETTERS])
    rows=packet['blocks'][0]['records']
    assert len(rows)==len(gloss['records'])==31 and gloss['prior_English_speech_unread']
    known={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    assert len(known)==6232 and not known&{historical_key(r) for r in rows}
    assert packet['current_ROM_sha256']==prior['candidate_sha256']
    assert context['manual_review_scope']==dict(complete_representative_exchanges=5,complete_representative_speeches=212,
                                               distinct_role_utterances=27,all581_manually_reread=False)
    assert census['source_blocks_scanned']==1307 and len(census['selected_native_blocks'])==17
    assert len(getters['original_native_cases']['rows'])==4
    old_scope=Path(old[OLD_SCOPE]['path']);assert sha(old_scope.read_bytes())==old[OLD_SCOPE]['sha256']
    scope=deepcopy(read(old_scope));scope['next_focus']=NEXT
    scope['historical_Lil_B199_clean_source_before_v5794']=scope.pop('next_Lil_B199_clean_review_pending')
    scope['next_Lil_B199_native_approved_uncredited_v5794']=dict(
        manuscript='translations/lil_B199_editorial_manuscript_v5.json',
        native_approval='work/analysis/lil_B199_native_approval_v5793/all31_source_prose_current_native_approval.json',
        source_actual='work/analysis/lil_B199_source_paths_v5782/one_actual_source_path_and_complete_command_intervals.json',
        reviewed_objects=31,revisions=11,justified_retentions=20,new_completion_credit=0,
        source_actual_speeches=31,source_actual_frames=13001,source_end_return_frame=10776,
        native_alignment_cases=248,source_consumer_negatives=22,formatter_negatives=28,
        effective_R58_registered_catalog_Camille_and_question_already_integrated=True,
        preserved_one_FI_two_private_thoughts_and_two_attempted_gift_corrections=True,
        English_reference_relocation_actual_atomic_compiler_and_registered_release_pending=True)
    scope['C_drive_space_recovery_v5790']=dict(
        cache_manifest='work/analysis/storage_recovery_v5790/before_manifest.json',
        relocation_receipt='work/analysis/storage_recovery_v5790/relocation_receipt.json',
        compressed_logical_bytes_verification='work/analysis/storage_recovery_v5790/unchanged_document_hashes_and_preserved_failed_layout.json',
        preserved_cache_files=102,preserved_cache_byte_count_bound_in_receipt=True,
        no_ROM_translation_or_proof_deleted=True,resolved_not_blocking=True,
        failed_formatter_v2_zero_byte_preserved=True,approved_formatter='dk4tool/dialogue/lil_B199_layout_v3.py')
    assert 'speaker_names_and_role_labels_localization_review_v5708' in scope
    manuscript=read('translations/lil_B199_editorial_manuscript_v5.json')
    approval=read('work/analysis/lil_B199_native_approval_v5793/all31_source_prose_current_native_approval.json')
    actual=read('work/analysis/lil_B199_source_paths_v5782/one_actual_source_path_and_complete_command_intervals.json')
    terminal=read('work/analysis/lil_B199_source_run_v5781_clean_Japanese/terminal.json')
    assert len(manuscript['records'])==31 and manuscript['revised']==11 and manuscript['retained']==20
    assert all(all(r['review'].values()) for r in manuscript['records'])
    assert manuscript['source_prose_or_completion_credit_added']==0 and not manuscript['formatting_review_pending']
    assert approval['manuscript_sha256']==sha(Path(approval['manuscript']).read_bytes())
    assert approval['all248_current_native_alignment_cases_and_complete_planes_pass']
    assert approval['source_consumer_negatives']==22 and len(approval['formatter_negatives'])==28
    assert actual['selected_source_speech_indices']==[r['source_record_index'] for r in manuscript['records']]
    assert not actual['unvisited_source_indices'] and actual['source_end1162_return_frame']==10776 and actual['total_frames']==13001
    assert len(actual['command_pairs'])==56 and terminal['terminal'] and terminal['observer_host_slots_restored']
    fixture=read('work/analysis/lil_B199_source_fixture_v5780/complete_B199_source_B22_fixture.json')['fixtures'][0]
    assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']==terminal['research_ROM_sha256']
    assert len(fixture['all56_stored_fixture_commands'])==56 and len(fixture['original_text_records'])==31
    assert any(Path(p['path']).resolve()==Path(fixture['research_ROM']).resolve() for p in read('translations/rom_retention_pins.json'))
    ROOT.mkdir(parents=True);scopepath=ROOT/'unfinished_editorial_scope_inventory.json';save(scopepath,scope)
    paths=[PRIOR,PACKET,GLOSS,CONTEXT,CENSUS,GETTERS,old_scope,scopepath,Path(__file__),
        Path('work/analysis/lil_B199_clean_inventory_v5764/all_clean_B199_speeches_before_predecessor_comparison.json'),
        Path('work/analysis/lil_B199_voices_v5768/current207_catalog_eight_voices_and_three_source_selectors.json'),
        Path('work/analysis/lil_B199_dispatches_v5769/all31_source_current_dispatches_one_FI_and16_control_leaves.json'),
        Path('work/analysis/lil_B199_entry_v5770/source_EV2_B199_action_dependency_and_native_getter_binding.json'),
        Path('work/analysis/lil_B199_branches_v5771/original_relative_skip_operand_proof.json'),
        Path('work/analysis/lil_B199_names_v5772/six_original_progressive_and_catalogue_name_consumers.json'),
        Path('work/analysis/couple_label_clean_context_v5766/four_complete_clean_route_exchanges_and_exact_couple_name_fields.json'),
        Path('scripts/census_couple_speaker_uses_v5773.py'),Path('scripts/census_couple_speaker_uses_v5773b.py'),
        Path('translations/lil_B199_editorial_manuscript_v5.json'),
        Path('work/analysis/lil_B199_native_approval_v5793/all31_source_prose_current_native_approval.json'),
        Path('work/analysis/lil_B199_fonts_v5792/all31_progressive_FE_native_planes_and248_alignment_cases.json'),
        Path('work/analysis/lil_B199_controls_v5778/sixteen_exact_leaves_four_resources_two_pictures_two47xx_pause_and_end.json'),
        Path('work/analysis/lil_B199_source_fixture_v5780/complete_B199_source_B22_fixture.json'),
        Path('work/analysis/lil_B199_source_fixture_v5780/pin_receipt.json'),
        Path('work/analysis/lil_B199_source_run_v5781_clean_Japanese/terminal.json'),
        Path('work/analysis/lil_B199_source_paths_v5782/one_actual_source_path_and_complete_command_intervals.json'),
        Path('work/analysis/lil_B199_comparison_v5783b/all31_complete_clean_and_predecessor_exchange.json'),
        Path('work/analysis/lil_B199_comparison_v5783b/complete_clean_context_actual_source_and_project_name_reconciliation.json'),
        Path('work/analysis/lil_B199_comparison_correction_v5783c/correction_receipt.json'),
        Path('work/analysis/lil_B199_macro_markup_v5786/one_exact_runtime_macro_markup_no_prose_change.json'),
        Path('work/analysis/lil_B199_idiom_layout_v5790b/one_complete_idiom_protection_and_justified_three_row_gift_response.json'),
        Path('work/analysis/storage_recovery_v5790/before_manifest.json'),
        Path('work/analysis/storage_recovery_v5790/relocation_receipt.json'),
        Path('work/analysis/storage_recovery_v5790/unchanged_document_hashes_and_preserved_failed_layout.json'),
        Path('dk4tool/dialogue/lil_B199_layout_v2.py'),Path('dk4tool/dialogue/lil_B199_layout_v3.py'),
        Path('dk4tool/dialogue/lil_B199_profile.py'),Path('scripts/lil_B199_checkpoint_text_v5794.py'),
        Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('translations/release_stack.json')]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    new=deepcopy(old);new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY+'\n\n'+NEXT
    new[KEY]=dict(summary=SUMMARY,next=NEXT,evidence=evidence,all31_B199_objects_uncredited=True,
        two_role_label_revisions_proposed_not_integrated=True,one_new_source_research_ROM_one13001_frame_boot_no_completion_credit=True,full_goal_complete=False)
    new[SCOPE]=dict(path=str(scopepath),sha256=sha(scopepath.read_bytes()),Lil_B199_uncredited_objects=31,native_approved_objects=31,
        proposed_role_label_revisions=2,retrospective207_name_queue_preserved=True,full_goal_complete=False)
    assert inverse(new)==old
    targets={LEDGER:encode_ledger(new)}
    assert len(targets[LEDGER])<100*1024*1024
    section='## V5794: B199 complete source scene and31 native-approved contextual reviews\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name
        prefix=('# Current editorial handoff - V5794\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
    files=[]
    for i,(target,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';backup=ROOT/f'{i:02d}.before.gz'
        planned.write_bytes(data);backup.write_bytes(gzip.compress(target.read_bytes(),mtime=0))
        files.append(dict(target=str(target.resolve()),planned=str(planned.resolve()),before=str(backup.resolve()),
            before_sha256=sha(target.read_bytes()),planned_sha256=sha(data)))
    save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True))
    print('Six targets staged;31 native-approved B199 objects remain uncredited pending English reference/actual/release.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);phase=p.parse_args().phase
    if phase=='stage':stage()
    else:
        pp=ROOT/'staged_checkpoint.json';plan=read(pp)
        if phase=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists();check(plan)
            save(ROOT/'independent_preapplication_audit.json',dict(plan_sha256=sha(pp.read_bytes()),
                all_before_planned_evidence_hashes_exact=True,deep_nested_inverse_and_exact_old_ledger_bytes_verified=True))
            print('Six-file preapplication and complete inverse audit pass.')
        elif phase=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'independent_preapplication_audit.json')['plan_sha256']==sha(pp.read_bytes());check(plan)
            for item in plan['files']:
                assert Path(item['target']).is_relative_to(Path.cwd().resolve())
                assert Path(item['planned']).is_relative_to(ROOT.resolve())
            for item in plan['files']:
                with Path(item['target']).open('r+b') as f:
                    f.write(Path(item['planned']).read_bytes());f.truncate();f.flush();os.fsync(f.fileno())
                assert sha(Path(item['target']).read_bytes())==item['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_exact=True,all_original_history_preserved=True))
            print('Six audited checkpoint targets applied with original history intact.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_exact']
            new=check(plan,True);prior=read(PRIOR)
            VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),
                candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],patch=prior['patch'],patch_sha256=prior['patch_sha256'],
                all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,**COUNTERS,
                completed=6232,source_prose=6235,revised=3917,retained=2315,SC2=4347,SC3=96,reviewed_routes=4633,completed_routes=4633,
                B199_uncredited_clean_glosses=31,B199_source_current_dispatches=62,B199_native_name_consumers=6,
                paired_labels_draft_only=True,paired_label_native_current_consumers=4,complete_source_representative_exchanges=5,
                complete_source_representative_speeches=212,distinct_role_utterances=27,all581_context_speeches_not_manually_reread=True,
                catalog_queue=207,new_source_research_ROMs=1,new_source_cold_boots=1,new_source_frames=13001,native_approved_B199_objects=31,native_alignment_cases=248,source_consumer_negatives=22,formatter_negatives=28,no_English_scene_or_registered_release_claim=True,no_promotion_commit_push_or_pruning=True,
                main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5795 verified:31 native-approved uncredited reviews and one complete Japanese source boot saved;V5756/main/counters unchanged. Full goal active.')
