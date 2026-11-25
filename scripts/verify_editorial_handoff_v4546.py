"""Independently audit B175 completion, exact integrated references and the full preserved scope."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.complete_lil_B175_v4545 import ROOT as COMPLETION,DOC,FINAL,FAMILY,RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4546')

def unchanged_outside(a,b,allowed):
    assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}

if __name__=='__main__':
    assert not ROOT.exists()
    receipt=read(COMPLETION/'completion_receipt.json');lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    before=read(COMPLETION/(lp.name+'.before'))
    assert sha((COMPLETION/(lp.name+'.before')).read_bytes())==read('work/analysis/editorial_handoff_verification_v4538/verified_handoff.json')['ledger_sha256']
    assert lp.read_bytes()==encode_ledger(ledger) and lp.stat().st_size<100*1024*1024
    allowed={'completed_editorial_families','records_editorially_completed','records_revised_and_integrated',
        'retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','reviewed_but_incomplete_route_record_IDs',
        'active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871','coverage_units','formatting_watchlist',
        'current_integrated_candidate','unfinished_editorial_scope_v4545','lil_B175_completion_v4545','latest_checkpoint'}
    unchanged_outside(before,ledger,allowed)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    family=ledger['completed_editorial_families'][-1];assert family['id']==FAMILY
    final,doc=read(FINAL),read(DOC);rows=family['records'];assert rows==final['records'] and len(rows)==32
    assert (final['revised'],final['retained'])==(19,13) and final['source_prose_credit_already_recorded_in_V4519']
    assert (family['revised_count'],family['retained_count'],family['fresh_revisions'],family['fresh_retentions'])==(19,13,19,13)
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':19,'retain-wording':13}
    all_rows=[r for f in ledger['completed_editorial_families'] for r in f['records']];keys=[historical_key(r) for r in all_rows]
    assert len(keys)==len(set(keys))==5865
    def decision(row):
        value=row.get('historical_editorial_decision') or row.get('decision') or row.get('editorial_decision')
        assert isinstance(value,str) and value.startswith(('revis','retain'))
        return 'revise' if value.startswith('revis') else 'retain'
    assert Counter(decision(r) for r in all_rows)=={'revise':3728,'retain':2137}
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(3728,2137)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'])==(5865,5868,5868)
    assert ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file']
    assert ledger['completed_editorial_record_counts_by_file']=={**before['completed_editorial_record_counts_by_file'],'/data/SC2.DK4':4012}
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==5865
    fresh,old=[l['contextual_story_natural_dialogue_pass_v1871'] for l in [ledger,before]]
    unchanged_outside(old,fresh,{'integrated_record_keys','fresh_pass_records_integrated','fresh_pass_records_pending_native_actual_release',
        'pending_record_keys','pending_contextual_families','latest_pending_contextual_family','latest_contextual_manuscript',
        'latest_completed_family','latest_final_review','coverage_note','reconciled_families'})
    assert fresh['integrated_record_keys']==old['integrated_record_keys']+old['pending_record_keys']
    assert {historical_key(r) for r in fresh['integrated_record_keys']}==set(keys)=={historical_key(r) for r in fresh['record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5865,5865,0)
    assert not fresh['pending_record_keys'] and not fresh['pending_contextual_families'] and fresh['latest_pending_contextual_family'] is None
    assert fresh['reconciled_families'][:-1]==old['reconciled_families']
    assert fresh['reconciled_families'][-1]['historical_decisions_newly_completed']==dict(revised=19,retained=13)
    assert ledger['reviewed_but_incomplete_route_record_IDs']=={**before['reviewed_but_incomplete_route_record_IDs'],'/data/SC2.DK4':[]}
    active,prior=ledger['active_source_prose_drafts'],before['active_source_prose_drafts']
    unchanged_outside(prior,active,{'manuscripts','route_record_subsets_pending','status','note'})
    assert active['manuscripts']==prior['manuscripts'] and active['route_record_subsets_pending']=={**prior['route_record_subsets_pending'],str(DOC):[]}
    assert sum(map(len,active['route_record_subsets_pending'].values()))==0
    for a,b in zip(before['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']=='all-route-scenes':
            unchanged_outside(a,b,{'reviewed_route_records','completed_route_records','next'});assert (b['reviewed_route_records'],b['completed_route_records'])==(4266,4266)
        elif a['id']==FAMILY:
            unchanged_outside(a,b,{'status','pending','completion_credit_added','final_review','new_emulator_runs','new_current_candidate_emulator_runs',
                'new_explicit_source_English_fixture_runs','actual_sampled_B22_display_IDs','offline_only_display_IDs','full_goal_complete'})
            assert b['completion_credit_added']==32 and b['pending'] is None
        else:assert a==b
    unchanged_outside(before['formatting_watchlist'],ledger['formatting_watchlist'],{'lil_B175_v4519','lil_B175_v4545'})
    unchanged_outside(before['formatting_watchlist']['lil_B175_v4519'],ledger['formatting_watchlist']['lil_B175_v4519'],{'status','registered_release_pending','final_review'})
    for p,h in {**receipt['evidence'],**receipt['updated_files']}.items():assert sha(Path(p).read_bytes())==h,p
    release,start,view,actual,transitions,reg=map(read,[RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG])
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all551_manifest_batches_and114_accepted_layers_present']
    assert start['paired_frame_count']==31 and start['all_current_requested_and_final_framebuffers_equal_V4496']
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and view['viewed']
    assert sha(Path(view['sheet']).read_bytes())==view['sha256']==start['review_sheet_sha256']
    assert reg['negative_count']==82 and reg['all_negatives_reject_before_mutation']
    tests=read('work/analysis/lil_B175_release_tools_v4541/regression_test_results.json')
    assert tests['returncode']==0 and '78 passed' in tests['output']
    rom=Path(release['candidate']);assert sha(rom.read_bytes())==release['candidate_sha256']==start['candidate_sha256']==final['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert rom.read_bytes()==Path('out/lil_B175_reference_v4526_RESEARCH_ONLY.nds').read_bytes()
    assert rom.read_bytes()==Path(release['exact_patch_reconstruction']).read_bytes()
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256'] and ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4541'
    assert read('translations/promoted_build.json')['profile']=='all-routes-unified-v4496'
    im=NdsImage.open(rom);target=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[175]
    source=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[175]
    predecessor=IlnkContainer.parse(NdsImage.open(doc['current_ROM']).read_file('/data/SC2.DK4')).blocks[175]
    byid={r['id']:r for r in doc['records']};mapping=read(doc['reference_map']);refs={r['id']:r for r in mapping['blocks'][0]['text_records']}
    for row in rows:
        old=byid[row['id']];ref=refs[row['id']]
        assert row['english']==old['english'] and all(row['review'].values()) and row['source_meaning']==row['fresh_source_gloss']
        for data,loc,value in [(source,row['source_reference'],row['source_hex']),
            (predecessor,row['historical_source_prose_predecessor_fields']['current_reference'],row['historical_source_prose_predecessor_fields']['current_hex']),
            (target,row['integrated_reference'],row['integrated_hex'])]:
            at=loc['offset'];raw=bytes.fromhex(value);assert data[at:at+len(raw)]==raw and data[at+len(raw)]==0
            assert data[at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert row['integrated_reference']['offset']==ref['new_offset'] and row['integrated_reference']['record_index']==target[:ref['new_offset']].count(b'\0')
        assert row['actual_B22_display_fixture_observed'] and not row['offline_only_complete_native_display_verified']
        assert row['actual_source_event175_selected'] is False and row['individual_actual_source_event_activation_not_claimed']
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    assert Counter(r['kind'] for r in rows)=={'progressive':23,'system-FE':9}
    assert actual['complete_matching_observations']==32 and not actual['failures'] and not actual['paired_region_differences']
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[10534,10535]
    assert transitions['nontext_equal_samples']==218 and len(transitions['nontext_difference_samples'])==14
    assert transitions['source_C2001700_and_first_end1702_actually_reached'] and transitions['second_declared_end1706_offline_native_only']
    assert transitions['whole_RGB_town10570_through10870_equal'] and transitions['final16001_whole_RGB_equality_not_claimed']
    assert transitions['postscene16001_whole1A04_actor_models_and_captain2_equal'] and all(transitions['postscene16001_native_component_equality'].values())
    assert transitions['PRNG_equality_causal_trace_and_future_world_equivalence_not_claimed']
    scope=ledger['unfinished_editorial_scope_v4545'];assert scope['incomplete_COMMON']==3 and scope['incomplete_route_source_prose']==0
    assert scope['remaining_B176_B180_physical_speeches']==58 and scope['canonical_Maria32_pending_uncredited'] and scope['Proof_terminology_consistency_open']
    inventory,oldinventory=read(scope['path']),read(before['unfinished_editorial_scope_v4537']['path'])
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    unchanged_outside(oldinventory,inventory,{'incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus','broader_coverage_units','lil_B175_completed_v4545'})
    assert inventory['incomplete_route_source_prose_groups']==[] and inventory['incomplete_route_source_prose_count']==0
    for a,b in zip(oldinventory['broader_coverage_units'],inventory['broader_coverage_units'],strict=True):
        if a['id']!='all-route-scenes':assert a==b
        else:unchanged_outside(a,b,{'reviewed_route_records','completed_route_records','source_prose_pending_records','source_prose_pending_family','next'})
    assert inventory['lil_B175_completed_v4545']['actual_FE_panels']==9
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4545')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4545',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5865,integrated=5865,pending=0,
        source_prose=5868,revised=3728,retained=2137,candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest_batches=551,accepted_layers=114,
        all32_source_predecessor_integrated_references_and13_retentions_verified=True,all_earlier_ledger_records_completions_and_full_objective_preserved=True,
        native256_alignment_cases128_stored_cases_two_ends_four_decodes_and32_dispatches_bound=True,
        actual32_panels23_progressive9_FE_C200_first_end_and_town_return_verified=True,second_end_offline_scope_and14_visual_differences_retained=True,
        final_state_actor_equality_with_PRNG_full_RGB_and_future_world_limits=True,current_startup31_whole_frames_and5_models_verified=True,
        candidate_whole_ROM_equal_reviewed_research_reference=True,atomic_compiler_negatives=82,regression_tests_passed=78,
        main_V4496_unchanged=True,remaining_B176_B180_physical_speeches=58,new_source_prose_reviews=0,new_completed_records=32,
        all_jobs_terminal=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4545 independently verified:5865 completed,zero pending,3728 revised/2137 retained. B175 integrated;main V4496/full objective preserved.')
