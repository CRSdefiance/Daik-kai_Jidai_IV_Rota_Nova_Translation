"""Independently audit B177 completion, exact integrated references and the full preserved scope."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.complete_lil_B177_v4659 import ROOT as COMPLETION,DOC,FINAL,FAMILY,RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4660')

def unchanged_outside(a,b,allowed):
    assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}

if __name__=='__main__':
    assert not ROOT.exists()
    receipt=read(COMPLETION/'completion_receipt.json');lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    before=read(COMPLETION/(lp.name+'.before'))
    assert sha((COMPLETION/(lp.name+'.before')).read_bytes())==read('work/analysis/editorial_handoff_verification_v4652/verified_handoff.json')['ledger_sha256']
    assert lp.read_bytes()==encode_ledger(ledger) and lp.stat().st_size<100*1024*1024
    allowed={'completed_editorial_families','records_editorially_completed','records_revised_and_integrated',
        'retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','reviewed_but_incomplete_route_record_IDs',
        'active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871','coverage_units','formatting_watchlist',
        'current_integrated_candidate','unfinished_editorial_scope_v4659','lil_B177_completion_v4659','latest_checkpoint'}
    unchanged_outside(before,ledger,allowed)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    family=ledger['completed_editorial_families'][-1];assert family['id']==FAMILY
    final,doc=read(FINAL),read(DOC);rows=family['records'];assert rows==final['records'] and len(rows)==10
    assert (final['revised'],final['retained'])==(5,5) and final['source_prose_credit_already_recorded_in_V4623']
    assert (family['revised_count'],family['retained_count'],family['fresh_revisions'],family['fresh_retentions'])==(5,5,5,5)
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':5,'retain-wording':5}
    all_rows=[r for f in ledger['completed_editorial_families'] for r in f['records']];keys=[historical_key(r) for r in all_rows]
    assert len(keys)==len(set(keys))==5885
    def decision(row):
        value=row.get('historical_editorial_decision') or row.get('decision') or row.get('editorial_decision')
        assert isinstance(value,str) and value.startswith(('revis','retain'))
        return 'revise' if value.startswith('revis') else 'retain'
    assert Counter(decision(r) for r in all_rows)=={'revise':3738,'retain':2147}
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(3738,2147)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'])==(5885,5888,5888)
    assert ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file']
    assert ledger['completed_editorial_record_counts_by_file']=={**before['completed_editorial_record_counts_by_file'],'/data/SC2.DK4':4032}
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==5885
    fresh,old=[l['contextual_story_natural_dialogue_pass_v1871'] for l in [ledger,before]]
    unchanged_outside(old,fresh,{'integrated_record_keys','fresh_pass_records_integrated','fresh_pass_records_pending_native_actual_release',
        'pending_record_keys','pending_contextual_families','latest_pending_contextual_family','latest_contextual_manuscript',
        'latest_completed_family','latest_final_review','coverage_note','reconciled_families'})
    assert fresh['integrated_record_keys']==old['integrated_record_keys']+old['pending_record_keys']
    assert {historical_key(r) for r in fresh['integrated_record_keys']}==set(keys)=={historical_key(r) for r in fresh['record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5885,5885,0)
    assert not fresh['pending_record_keys'] and not fresh['pending_contextual_families'] and fresh['latest_pending_contextual_family'] is None
    assert fresh['reconciled_families'][:-1]==old['reconciled_families']
    assert fresh['reconciled_families'][-1]['historical_decisions_newly_completed']==dict(revised=5,retained=5)
    assert ledger['reviewed_but_incomplete_route_record_IDs']=={**before['reviewed_but_incomplete_route_record_IDs'],'/data/SC2.DK4':[]}
    active,prior=ledger['active_source_prose_drafts'],before['active_source_prose_drafts']
    unchanged_outside(prior,active,{'manuscripts','route_record_subsets_pending','status','note'})
    assert active['manuscripts']==prior['manuscripts'] and active['route_record_subsets_pending']=={**prior['route_record_subsets_pending'],str(DOC):[]}
    assert sum(map(len,active['route_record_subsets_pending'].values()))==0
    for a,b in zip(before['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']=='all-route-scenes':
            unchanged_outside(a,b,{'reviewed_route_records','completed_route_records','next'});assert (b['reviewed_route_records'],b['completed_route_records'])==(4286,4286)
        elif a['id']==FAMILY:
            unchanged_outside(a,b,{'status','pending','completion_credit_added','final_review','new_emulator_runs','new_current_candidate_emulator_runs',
                'new_explicit_source_English_fixture_runs','actual_sampled_B22_display_IDs','offline_only_display_IDs','full_goal_complete'})
            assert b['completion_credit_added']==10 and b['pending'] is None
        else:assert a==b
    unchanged_outside(before['formatting_watchlist'],ledger['formatting_watchlist'],{'lil_B177_v4623','lil_B177_v4659'})
    unchanged_outside(before['formatting_watchlist']['lil_B177_v4623'],ledger['formatting_watchlist']['lil_B177_v4623'],{'status','registered_release_pending','final_review'})
    for p,h in {**receipt['evidence'],**receipt['updated_files']}.items():assert sha(Path(p).read_bytes())==h,p
    release,start,view,actual,transitions,reg=map(read,[RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG])
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all553_manifest_batches_and114_accepted_layers_present']
    assert start['paired_frame_count']==31 and start['all_current_requested_and_final_framebuffers_equal_V4595']
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and view['viewed']
    assert sha(Path(view['sheet']).read_bytes())==view['sha256']==start['review_sheet_sha256']
    assert reg['negative_count']==95 and reg['all_negatives_reject_before_mutation']
    tests=read('work/analysis/lil_B177_release_tools_v4655/regression_test_results.json')
    assert tests['returncode']==0 and '78 passed' in tests['output']
    rom=Path(release['candidate']);assert sha(rom.read_bytes())==release['candidate_sha256']==start['candidate_sha256']==final['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert rom.read_bytes()==Path('out/lil_B177_reference_v4630_RESEARCH_ONLY.nds').read_bytes()
    assert rom.read_bytes()==Path(release['exact_patch_reconstruction']).read_bytes()
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256'] and ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4655'
    assert read('translations/promoted_build.json')['profile']=='all-routes-unified-v4595'
    im=NdsImage.open(rom);target=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[177]
    source=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[177]
    predecessor=IlnkContainer.parse(NdsImage.open(doc['current_ROM']).read_file('/data/SC2.DK4')).blocks[177]
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
        assert row['actual_source_event176_selected'] is False and row['individual_actual_source_event_activation_not_claimed']
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    assert Counter(r['kind'] for r in rows)=={'progressive':9,'system-FE':1}
    assert actual['complete_matching_observations']==10 and not actual['failures'] and not actual['paired_region_differences']
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[5255,5257]
    assert transitions['nontext_equal_samples']==115 and not transitions['nontext_difference_samples']
    assert transitions['source_A0008_C200480_single_end482_actually_executed']
    assert transitions['whole_RGB_town5290_through5950_and_final9001_equal'] and transitions['whole_RGB_final9001_equal']
    assert transitions['postscene9001_whole1A04_actor_models_and_captain2_equal'] and all(transitions['postscene9001_native_component_equality'].values())
    assert not transitions['PRNG_equality'] and transitions['postscene9001_PRNG_seeds']==[463267532,403514907]
    assert len(transitions['actual_timing_differences'])==11
    assert transitions['exact_timing_difference_counts']=={'total':11,'speech':9,'control_or_end':2}
    assert len(transitions['fourteen_following_A_button_indicator_animation_differences_retained_unmasked'])==14
    assert transitions['fourteen_following_indicator_differences_viewed_in_representative_full_screens_and_retained']
    assert transitions['no_new_PRNG_causal_trace'] and transitions['future_world_equivalence_and_full_RAM_equality_not_claimed']
    assert transitions['following_B120_offset606_in_progress_at_end_adds_no_editorial_credit']
    scope=ledger['unfinished_editorial_scope_v4659'];assert scope['incomplete_COMMON']==3 and scope['incomplete_route_source_prose']==0
    assert scope['remaining_B178_B180_physical_speeches']==38 and scope['canonical_Maria32_pending_uncredited'] and scope['Proof_terminology_consistency_open']
    inventory,oldinventory=read(scope['path']),read(before['unfinished_editorial_scope_v4641']['path'])
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    unchanged_outside(oldinventory,inventory,{'incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus','broader_coverage_units','lil_B177_completed_v4659'})
    assert inventory['incomplete_route_source_prose_groups']==[] and inventory['incomplete_route_source_prose_count']==0
    for a,b in zip(oldinventory['broader_coverage_units'],inventory['broader_coverage_units'],strict=True):
        if a['id']!='all-route-scenes':assert a==b
        else:unchanged_outside(a,b,{'reviewed_route_records','completed_route_records','source_prose_pending_records','source_prose_pending_family','next'})
    assert inventory['lil_B177_completed_v4659']['actual_FE_panels']==1
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4659')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4659',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5885,integrated=5885,pending=0,
        source_prose=5888,revised=3738,retained=2147,candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest_batches=553,accepted_layers=114,
        all10_source_predecessor_integrated_references_and5_retentions_verified=True,
        all_earlier_ledger_records_completions_and_full_objective_preserved=True,
        native80_alignment_cases40_stored_cases_single_end_two_decodes_and10_dispatches_bound=True,
        actual10_panels9_progressive1_impersonal_FE_A000_C200_single_end_and_town_return_verified=True,
        all115_upper_portrait_name_samples_equal_11_timing_and14_indicator_RGB_differences_retained=True,
        final_state_actor_captain_town_final_RGB_equal_unequal_PRNG_with_full_RAM_future_world_and_hardware_limits=True,
        current_startup31_whole_frames_and5_models_verified=True,candidate_whole_ROM_equal_reviewed_research_reference=True,
        atomic_compiler_negatives=95,regression_tests_passed=78,main_V4595_unchanged=True,
        remaining_B178_B180_physical_speeches=38,new_source_prose_reviews=0,new_completed_records=10,
        all_jobs_terminal=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4659 independently verified:5885 completed,zero pending,3738 revised/2147 retained. B177 integrated;main V4595/full objective preserved.')
