"""Independently verify B173 reference approval and all unchanged ledger history."""
from copy import deepcopy
import gzip
import json
from pathlib import Path
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.lil_B173_reference_checkpoint_text_v4441 import SUMMARY,NEXT
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/editorial_handoff_verification_v4442b')
CHECK=Path('work/analysis/lil_B173_reference_checkpoint_v4441')
DOC=Path('translations/lil_B173_editorial_manuscript_v4.json')
OLD=Path('translations/lil_B173_editorial_manuscript_v3.json')
APPROVAL=Path('work/analysis/lil_B173_reference_approval_v4440/approval_receipt.json')
FAMILY='Lil-B173-Reika-crown-inquiry-uncertain-Julian-tomb-lead-competitive-search11'

if __name__=='__main__':
    assert not ROOT.exists()
    receipt=read(CHECK/'checkpoint_receipt.json')
    lp=Path('translations/editorial_review_current_v1.json');raw=lp.read_bytes();ledger=json.loads(raw)
    before=json.loads(gzip.decompress((CHECK/'ledger.before.json.gz').read_bytes()))
    assert sha(raw)==receipt['ledger_sha256'] and encode_ledger(ledger)==raw and len(raw)<100*1024*1024
    for row in read(CHECK/'mutation_plan.json'):
        assert sha(Path(row['target']).read_bytes())==row['planned_sha256']
        assert Path(row['planned']).read_bytes()==Path(row['target']).read_bytes()
    for group in ['evidence','preserved_release_files']:
        for path,digest in receipt[group].items():assert sha(Path(path).read_bytes())==digest,path
    allowed={'contextual_story_natural_dialogue_pass_v1871','active_source_prose_drafts','coverage_units',
        'unfinished_editorial_scope_v4441','lil_B173_reference_reconciliation_v4441','latest_checkpoint'}
    assert {k:v for k,v in before.items() if k not in allowed}=={k:v for k,v in ledger.items() if k not in allowed}
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];oldfresh=before['contextual_story_natural_dialogue_pass_v1871']
    changed={'latest_contextual_manuscript','latest_pending_contextual_family','coverage_note','pending_contextual_families'}
    assert {k:v for k,v in fresh.items() if k not in changed}=={k:v for k,v in oldfresh.items() if k not in changed}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5800,5789,11)
    assert len(fresh['pending_contextual_families'])==len(oldfresh['pending_contextual_families'])==1
    pending=fresh['pending_contextual_families'][0];prior=oldfresh['pending_contextual_families'][0]
    assert pending['id']==prior['id']==FAMILY and pending['manuscript']==str(DOC) and prior['manuscript']==str(OLD)
    pending_fields={'manuscript','manuscript_sha256','manuscripts','pending','actual_sampled_display_IDs',
        'offline_only_display_IDs','new_emulator_runs','reference_approval','reference_approval_sha256'}
    assert {k:v for k,v in pending.items() if k not in pending_fields}=={k:v for k,v in prior.items() if k not in pending_fields}
    assert pending['pending']==NEXT and pending['new_emulator_runs']==2 and not pending['offline_only_display_IDs']
    assert sha(DOC.read_bytes())==pending['manuscript_sha256']
    approval,doc,old=map(read,[APPROVAL,DOC,OLD])
    assert approval['manuscripts']==pending['manuscripts']=={str(DOC):sha(DOC.read_bytes())}
    assert len(approval['actual_sampled_display_IDs'])==11 and approval['all11_source_native_reference_and_representative_rules_approved']
    for path,digest in approval['evidence'].items():assert sha(Path(path).read_bytes())==digest,path
    assert [r['english'] for r in doc['records']]==[r['english'] for r in old['records']]
    assert len(doc['records'])==11 and sum(r['editorial_decision']=='revise' for r in doc['records'])==8
    assert all(all(r['review'].values()) for r in doc['records'])
    for key in ['reference_map','representative_proof','final_padding_proof','relocated_control_proof','termination_decode_proof','postscene_native_state_proof']:
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    active=ledger['active_source_prose_drafts'];prioractive=before['active_source_prose_drafts']
    ignore={'manuscripts','route_record_subsets_pending','status','note'}
    assert {k:v for k,v in active.items() if k not in ignore}=={k:v for k,v in prioractive.items() if k not in ignore}
    assert active['manuscripts']==prioractive['manuscripts']+[str(DOC)]
    subsets=deepcopy(prioractive['route_record_subsets_pending']);ids=subsets[str(OLD)]
    subsets[str(OLD)]=[];subsets[str(DOC)]=ids
    assert active['route_record_subsets_pending']==subsets and ids==[r['id'] for r in doc['records']]
    assert len(ledger['coverage_units'])==len(before['coverage_units'])
    for a,b in zip(before['coverage_units'],ledger['coverage_units'],strict=True):
        assert a['id']==b['id']
        if a['id']==FAMILY:
            expected={**a,**pending,'status':doc['status'],'actual_new_cold_boot_runs':2,
                'actual_complete_native_panels':11,'registered_release_pending':True}
            assert b==expected
        elif a['id']=='all-route-scenes':assert b=={**a,'next':NEXT}
        else:assert a==b,a['id']
    assert ledger['latest_checkpoint']==SUMMARY and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass',
        'records_revised_and_integrated','retained_wordings_editorially_completed'])==(5789,5803,3678,2111)
    scope=ledger['unfinished_editorial_scope_v4441'];assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    assert read(scope['path'])['next_focus']==NEXT
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        text=Path('docs',name).read_text(encoding='utf-8');assert SUMMARY in text and NEXT in text
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4441')
    promotion=read('translations/promoted_build.json');assert promotion['profile']=='all-routes-unified-v4353'
    assert sha(Path(promotion['rom']).read_bytes())==promotion['rom_sha256']
    for case in ['clean_Japanese','reviewed_English']:
        for stage in ['display_run_v4437']:
            assert read(Path('work/analysis')/('lil_B173_'+stage+'_'+case)/'terminal.json')['terminal']
    ROOT.mkdir(parents=True)
    candidate=ledger['current_integrated_candidate']
    assert candidate['profile']=='all-routes-unified-v4404'
    assert candidate['sha256']==doc['current_ROM_sha256']==sha(Path(candidate['path']).read_bytes())
    sample=read(doc['representative_proof']);stateproof=read(doc['postscene_native_state_proof'])
    assert sample['new_emulator_runs']==2 and sample['all11_progressive_panels_unforced_predicate_both_effects_single_end_and_normal_town_return_pass']
    assert sample['actual_VM_descriptor_last_result1_preserved_through_type3_and_end']
    assert len(stateproof['all2_actual_sheets_viewed'])==2 and len(stateproof['paired_full_screen_views'])==6
    assert len(stateproof['all115_sampled_nontext_region_checks'])==115 and stateproof['all115_sampled_nontext_regions_equal']
    assert stateproof['whole_RGB_town5530_and_final9001_equal'] and all(stateproof['postscene9001_native_component_equality'].values())
    assert stateproof['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert stateproof['source_relative_sites736740756_actual_744_offline_native_only']
    assert stateproof['PRNG_equality_or_future_world_equivalence_not_claimed']
    stored=read(doc['final_padding_proof']);mapping=read(doc['reference_map'])
    assert stored['current_final_stored_macro_alignment_cases']==44
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(24,20)
    assert len(mapping['blocks'][0]['relative_skip_fixups'])==4 and len(mapping['blocks'][0]['target_native_skip_cases'])==20
    assert mapping['blocks'][0]['original_declared_end_word_maps']==[dict(source_offset=762,target_offset=794,extent=4,source_four_zero_bytes_exact=True)]
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4441',ledger_sha256=sha(raw),fresh_reread=5800,
        integrated=5789,pending=11,source_prose=5803,revised=3678,retained=2111,new_source_prose_reviews=0,new_completed_records=0,
        all_prior_ledger_values_and_completed_records_preserved=True,all11_source_prose_native_reference_and_actual_display_approved=True,
        actual_panels=11,actual_sheets=2,viewed_source_English_full_screens=6,content_cold_boots=2,frames_each=9001,all_jobs_terminal=True,
        source_structural_commands=23,stored_fixture_commands=32,actual_selected_fixture_commands=31,
        four_relative_sites40_source_current_and20_target_native_cases=True,
        source_predicate1_both_A000s_single_end762_and_normal_return_actual=True,
        actual_VM_last_result1_preserved_through_type3_and_end=True,
        unvisited_source_jump744_has_explicit_offline_native_coverage=True,all115_nontext_regions_equal=True,
        current_candidate=candidate['path'],candidate_sha256=candidate['sha256'],promoted_main_V4353_unchanged=True,
        no_registry_builder_baseline_or_graphics_scope_change=True,one_space_complete_ledger_preserved=True,
        full_goal_active=True,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,APPROVAL,CHECK/'checkpoint_receipt.json',Path(__file__)]}))
    print('V4441 independently verified:11 reference-approved pending;all earlier records/counters,latestV4404,mainV4353 and wider scope preserved.')
