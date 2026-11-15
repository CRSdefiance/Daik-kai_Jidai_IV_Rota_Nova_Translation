"""Independently prove B174 completion, exact references and preservation of full scope."""
from collections import Counter
from pathlib import Path
import re
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.complete_lil_B174_v4500b import ROOT as COMPLETION,DOC,FINAL,FAMILY,RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4501')

def unchanged_outside(a,b,allowed):
    assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}

if __name__=='__main__':
    assert not ROOT.exists()
    receipt=read(COMPLETION/'completion_receipt.json')
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    before=read(COMPLETION/(lp.name+'.before'))
    assert sha((COMPLETION/(lp.name+'.before')).read_bytes())==read('work/analysis/editorial_handoff_verification_v4493/verified_handoff.json')['ledger_sha256']
    assert lp.read_bytes()==encode_ledger(ledger) and lp.stat().st_size<100*1024*1024
    allowed={'completed_editorial_families','records_editorially_completed','records_revised_and_integrated',
        'retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','reviewed_but_incomplete_route_record_IDs',
        'active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871','coverage_units','formatting_watchlist',
        'current_integrated_candidate','unfinished_editorial_scope_v4500','lil_B174_completion_v4500','latest_checkpoint'}
    unchanged_outside(before,ledger,allowed)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    family=ledger['completed_editorial_families'][-1];assert family['id']==FAMILY
    final,doc=read(FINAL),read(DOC);rows=family['records']
    assert rows==final['records'] and len(rows)==33
    assert (final['revised'],final['retained'])==(23,10) and final['source_prose_credit_already_recorded_in_V4475']
    assert (family['revised_count'],family['retained_count'],family['fresh_revisions'],family['fresh_retentions'])==(23,10,23,10)
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':23,'retain-wording':10}
    keys=[historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']]
    assert len(keys)==len(set(keys))==5833
    assert sum(f['revised_count'] for f in ledger['completed_editorial_families'])==ledger['records_revised_and_integrated']==3709
    assert sum(f['retained_count'] for f in ledger['completed_editorial_families'])==ledger['retained_wordings_editorially_completed']==2124
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'])==(5833,5836,5836)
    assert ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file']
    assert ledger['completed_editorial_record_counts_by_file']=={**before['completed_editorial_record_counts_by_file'],'/data/SC2.DK4':3980}
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==5833
    fresh,old=[p['contextual_story_natural_dialogue_pass_v1871'] for p in [ledger,before]]
    fresh_allowed={'integrated_record_keys','fresh_pass_records_integrated','fresh_pass_records_pending_native_actual_release',
        'pending_record_keys','pending_contextual_families','latest_pending_contextual_family','latest_contextual_manuscript',
        'latest_completed_family','latest_final_review','coverage_note','reconciled_families'}
    unchanged_outside(old,fresh,fresh_allowed)
    assert fresh['integrated_record_keys']==old['integrated_record_keys']+old['pending_record_keys']
    assert {historical_key(r) for r in fresh['integrated_record_keys']}==set(keys)=={historical_key(r) for r in fresh['record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5833,5833,0)
    assert not fresh['pending_record_keys'] and not fresh['pending_contextual_families'] and fresh['latest_pending_contextual_family'] is None
    assert fresh['reconciled_families'][:-1]==old['reconciled_families']
    assert fresh['reconciled_families'][-1]['historical_decisions_newly_completed']==dict(revised=23,retained=10)
    assert ledger['reviewed_but_incomplete_route_record_IDs']=={**before['reviewed_but_incomplete_route_record_IDs'],'/data/SC2.DK4':[]}
    active,previous=ledger['active_source_prose_drafts'],before['active_source_prose_drafts']
    unchanged_outside(previous,active,{'manuscripts','route_record_subsets_pending','status','note'})
    assert active['manuscripts']==previous['manuscripts'] and sum(map(len,active['route_record_subsets_pending'].values()))==0
    assert active['route_record_subsets_pending']=={**previous['route_record_subsets_pending'],str(DOC):[]}
    assert len(before['coverage_units'])==len(ledger['coverage_units'])
    for a,b in zip(before['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']=='all-route-scenes':
            unchanged_outside(a,b,{'reviewed_route_records','completed_route_records','next'})
            assert (b['reviewed_route_records'],b['completed_route_records'])==(4234,4234)
        elif a['id']==FAMILY:
            unchanged_outside(a,b,{'status','pending','completion_credit_added','final_review','new_emulator_runs',
                'new_current_candidate_emulator_runs','new_explicit_source_English_fixture_runs','actual_sampled_B22_display_IDs','offline_only_display_IDs','full_goal_complete'})
            assert b['completion_credit_added']==33 and b['pending'] is None
        else:assert a==b
    old_watch=before['formatting_watchlist'];watch=ledger['formatting_watchlist']
    unchanged_outside(old_watch,watch,{'lil_B174_v4475','lil_B174_v4500'})
    unchanged_outside(old_watch['lil_B174_v4475'],watch['lil_B174_v4475'],{'status','registered_release_pending','final_review'})
    for path,digest in {**receipt['evidence'],**receipt['updated_files']}.items():assert sha(Path(path).read_bytes())==digest,path
    assert receipt['new_source_prose_reviews']==0 and receipt['new_completed_records']==33
    assert receipt['actual_unique_speech_panels']==32 and receipt['offline_only_display_IDs']==['DK4_MES_B174_R0069']
    assert receipt['manifest_batches']==550 and receipt['accepted_layers']==114 and receipt['all_jobs_terminal']
    release,start,view,actual,observed,reg=map(read,[RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG])
    candidate=Path(release['candidate']);digest=sha(candidate.read_bytes())
    assert digest==receipt['candidate_sha256']==start['candidate_sha256']
    assert digest==sha(Path('out/lil_B174_reference_v4482_RESEARCH_ONLY.nds').read_bytes())
    assert candidate.read_bytes()==Path(release['exact_patch_reconstruction']).read_bytes()
    assert sha(Path(release['patch']).read_bytes())==receipt['patch_sha256']==release['patch_sha256']
    manifest=read(release['manifest']);registry=read('translations/release_stack.json')
    assert manifest['candidate_sha256']==digest and len(manifest['batches'])==550 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4445'
    assert release['whole_ROM_reconstruction_byte_exact'] and release['file_changes']==['/data/SC2.DK4'] and release['component_changes']==[]
    assert reg['negative_count']==92 and reg['all_negatives_reject_before_mutation']
    negatives=read(reg['negative_cases']);assert len(negatives['cases'])==92 and all(c['rejected'] for c in negatives['cases'])
    tests=read('work/analysis/lil_B174_release_tools_v4496/regression_test_results.json')
    assert tests['returncode']==0 and re.search(r'\b78 passed\b',tests['output'])
    assert start['paired_frame_count']==31 and start['all_current_requested_and_final_framebuffers_equal_V4445']
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and view['viewed'] and view['no_new_display_finding']
    assert sha(Path(view['sheet']).read_bytes())==view['sha256']==start['review_sheet_sha256']
    mapping=read(doc['reference_map']);spec=mapping['blocks'][0];refs={r['id']:r for r in spec['text_records']}
    image=NdsImage.open(candidate);clean=NdsImage.open('work/clean.nds');parent=NdsImage.open(doc['current_ROM'])
    target,jp,old=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[174] for im in [image,clean,parent]]
    assert (len(old),len(target))==(2092,2208) and sha(target)==spec['target_block_sha256']
    assert len(spec['command_map'])==45 and len(spec['relative_skip_fixups'])==4 and len(spec['target_native_skip_cases'])==20
    assert spec['original_declared_end_word_maps']==[dict(source_offset=2086,target_offset=2204,extent=4,source_four_zero_bytes_exact=True)]
    actual_ids={r['id'] for r in actual['actual_panels']};offline={'DK4_MES_B174_R0069'}
    source_rows={r['id']:r for r in doc['records']}
    for row in rows:
        ident=row['id'];origin=source_rows[ident];r=refs[ident];at=r['new_offset'];value=bytes.fromhex(r['target_hex'])
        assert all(row['review'].values()) and row['source_meaning']==origin['source_meaning'] and row['english']==origin['english']
        assert row['source_hex']==origin['source_hex'] and row['source_complete_preamble_hex']==origin['source_complete_preamble_hex']
        source_at=row['source_reference']['offset'];source_value=bytes.fromhex(row['source_hex'])
        assert jp[source_at:source_at+len(source_value)]==source_value and jp[source_at+len(source_value)]==0
        assert target[at:at+len(value)]==value and target[at+len(value)]==0
        assert row['integrated_reference']==row['current_reference'] and row['current_reference']['offset']==at and row['current_reference']['bytes']==len(value)
        assert row['integrated_hex']==row['current_hex']==value.hex() and target[at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert row['historical_source_prose_predecessor_fields']['current_hex']==origin['current_hex']
        assert row['completed_candidate_sha256']==digest and not row['registered_integration_pending']
        assert row['actual_B22_display_fixture_observed']==(ident in actual_ids) and row['offline_only_complete_native_display_verified']==(ident in offline)
        assert not row['actual_source_event174_selected']
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    assert len(actual_ids)==32 and actual_ids|offline==set(refs) and not actual_ids&offline
    assert actual['complete_matching_observations']==32 and not actual['failures'] and not actual['paired_region_differences']
    assert observed['exact_timing_difference_counts']==dict(total=28,speech=20,control_or_end=8)
    assert len(observed['all6_actual_sheets_viewed'])==6 and len(observed['paired_full_screen_views'])==6
    assert len(observed['all232_sampled_nontext_region_checks'])==232 and observed['all232_sampled_nontext_regions_equal']
    assert observed['whole_RGB_town10810_and_final16001_equal'] and all(observed['postscene16001_native_component_equality'].values())
    assert observed['postscene16001_whole1A04_actor_models_and_captain2_equal'] and observed['PRNG_equality_or_future_world_equivalence_not_claimed']
    assert observed['join_notice10570_complete_shared_text_plane_equal'] and observed['join_notice_leading_J_full_Julian_Lopes_and_trailing_exclamation_viewed']
    assert observed['join_notice_full_RGB_difference_is_original_A_button_indicator']==[224,360,240,376]
    for version in actual['versions']:
        assert version['unforced_predicate_result']==0 and len(version['selected_B22_command_pairs'])==51
        assert [r['original_source_offset'] for r in version['actual_source_A000s']]==[2068,2076]
        assert version['actual_source_C200'][0]['original_source_offset']==2084 and version['single_source_end_offset']==2086
        assert [r['source_offset'] for r in version['unvisited_declared_source_objects']]==[886,894,938]
    assert [v['actual_source_relative_commands'][1]['extent'] for v in actual['versions']]==[52,62]
    scope=ledger['unfinished_editorial_scope_v4500'];assert scope['incomplete_route_source_prose']==0 and scope['incomplete_COMMON']==3
    assert scope['remaining_B175_B180_physical_speeches']==90 and scope['canonical_Maria32_pending_uncredited']
    inventory=read(scope['path']);previous_inventory=read(before['unfinished_editorial_scope_v4492']['path'])
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    unchanged_outside(previous_inventory,inventory,{'incomplete_route_source_prose_groups','incomplete_route_source_prose_count',
        'next_focus','broader_coverage_units','lil_B174_completed_v4500'})
    assert inventory['incomplete_route_source_prose_groups']==[] and inventory['incomplete_route_source_prose_count']==0
    for a,b in zip(previous_inventory['broader_coverage_units'],inventory['broader_coverage_units'],strict=True):
        if a['id']=='all-route-scenes':unchanged_outside(a,b,{'reviewed_route_records','completed_route_records','source_prose_pending_records','source_prose_pending_family','next'})
        else:assert a==b
    assert ledger['promoted_main_build_v4452']==before['promoted_main_build_v4452']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4500')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4500',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5833,
        integrated=5833,pending=0,source_prose=5836,revised=3709,retained=2124,
        candidate=str(candidate),candidate_sha256=digest,patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest_batches=550,accepted_layers=114,all33_clean_predecessor_integrated_references_and10_retentions_verified=True,
        all45_commands_four_relative_sites20_target_cases132_stored_cases_C200_two_effects_and_single_end_bound=True,
        actual32_panels_unforced_result0_two_effects_C200_normal_return_verified=True,optional_Emilio69_offline_native_only=True,
        source_and_English_skip_extents52_and62_and_join_notice_first_J_verified=True,
        all232_nontext_regions_and_postscene_component_actor_scope_verified=True,
        current_registered_startup31_whole_frames_and5_models_verified=True,atomic_compiler_negatives=92,regression_tests_passed=78,
        V4445_promoted_main_unchanged=True,every_prior_ledger_record_completion_and_full_objective_preserved=True,
        remaining_B175_B180_physical_speeches=90,new_source_prose_reviews=0,new_completed_records=33,
        full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4500 independently audited:5833 completed,33 B174 completions once;source/prose5836 unchanged. Full scope and main V4445 preserved.')
