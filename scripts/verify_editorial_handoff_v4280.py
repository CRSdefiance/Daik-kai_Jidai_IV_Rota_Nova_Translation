"""Apply validated B170 pending-credit metadata and independently verify all33 reviews."""
import os
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B170_v4279 import ROOT as CHECKPOINT,DOC,FAMILY
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4280')
if __name__=='__main__':
    assert not ROOT.exists()
    workspace=Path.cwd().resolve()
    plan=read(CHECKPOINT/'mutation_plan.json')
    assert len(plan)==6
    for item in plan:
        target,staged=Path(item['target']),Path(item['planned'])
        assert target.is_relative_to(workspace) and staged.is_relative_to(CHECKPOINT.resolve())
        assert sha(target.read_bytes())==item['before_sha256'] and sha(staged.read_bytes())==item['planned_sha256']
        assert staged.stat().st_size>=target.stat().st_size
    for item in plan:
        with Path(item['target']).open('r+b') as stream:
            stream.write(Path(item['planned']).read_bytes())
            stream.flush()
            os.fsync(stream.fileno())
        assert sha(Path(item['target']).read_bytes())==item['planned_sha256']
    lp=Path('translations/editorial_review_current_v1.json')
    ledger,before=read(lp),read(CHECKPOINT/(lp.name+'.before'))
    allowed={'records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file',
        'reviewed_but_incomplete_route_record_IDs','active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871',
        'coverage_units','formatting_watchlist','unfinished_editorial_scope_v4279','lil_B170_scope_reconciliation_v4279','latest_checkpoint'}
    assert {k:v for k,v in before.items() if k not in allowed}=={k:v for k,v in ledger.items() if k not in allowed}
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    fresh,old=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    assert fresh['integrated_record_keys']==old['integrated_record_keys']
    assert fresh['record_keys'][:5692]==old['record_keys']
    keys=[historical_key(r) for r in fresh['record_keys']]
    assert len(keys)==len(set(keys))==5725
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5725,5692,33)
    doc=read(DOC)
    rows=doc['records']
    assert len(rows)==33 and Counter(r['editorial_decision'] for r in rows)=={'revise':21,'retain-wording':12}
    expected=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    assert fresh['pending_record_keys']==fresh['record_keys'][5692:]==expected
    assert len(fresh['pending_contextual_families'])==1 and fresh['pending_contextual_families'][0]['id']==FAMILY
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==5728
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3872 and ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']==64
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==5728
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5692,3614,2078)
    for previous,current in zip(before['coverage_units'],ledger['coverage_units'][:-1],strict=True):
        if previous['id']!='all-route-scenes':
            assert previous==current
        else:
            assert current['reviewed_route_records']==4126 and current['completed_route_records']==4093
            assert {k:v for k,v in previous.items() if k not in ['reviewed_route_records','completed_route_records','next']}=={k:v for k,v in current.items() if k not in ['reviewed_route_records','completed_route_records','next']}
    assert ledger['coverage_units'][-1]['id']==FAMILY and ledger['coverage_units'][-1]['completion_credit_added']==0
    source,current=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[170] for p in ['work/clean.nds',doc['current_ROM']]]
    for row in rows:
        assert all(row['review'].values()) and row['full_clean_context_precedes_comparison'] and row['source_meaning']==row['fresh_source_gloss']
        for data,reference,value in [(source,row['source_reference'],row['source_hex']),(current,row['current_reference'],row['current_hex'])]:
            at,raw=reference['offset'],bytes.fromhex(value)
            assert data[at:at+len(raw)]==raw and data[at+len(raw)]==0
            assert data[at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert row['source_selector'] in [2,25]
        if row['editorial_decision']=='retain-wording':
            assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    approval=read('work/analysis/lil_B170_native_approval_v4278/approval_receipt.json')
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())}
    assert (approval['progressive_planes'],approval['current_macro_alignment_cases'],approval['source_consumer_negatives'],approval['source_macro_negatives'],approval['formatter_negatives'])==(33,264,13,2,14)
    assert len(approval['review_sheets'])==5 and all(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['review_sheets'])
    fonts=read(doc['native_progressive_proof'])
    assert (fonts['new_current_original_macro_alignment_calls'],fonts['reused_original_macro_alignment_calls'])==(16,248)
    assert set(fonts['fresh_record_IDs'])=={'DK4_MES_B170_R0037','DK4_MES_B170_R0104'}
    assert len(fonts['cases'])==33 and all(c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows'] for c in fonts['cases'])
    controls=read(doc['source_effect_and_predicate_contract'])
    assert len(controls['all12_source_current_nonrelative_nonspeech_leaves'])==12 and len(controls['two_resource_words20_boundary_cases'])==20
    assert len(controls['source_C200_pairs'])==1 and len(controls['source_C200_pairs'][0]['cases'])==2
    assert controls['source_declared_end_offsets']==[1852,1856] and controls['A000_source_command_hex']=='00a0ffff19100120'
    assert controls['source_pause_resume_pairs'][0]['source_resume']==38 and controls['source_pause_resume_pairs'][0]['source_offset']==36
    names=read(doc['source_nameplate_consumer_proof'])
    assert names['approved_prose_names']=={'2':'Lil','25':'Yifa'} and names['progressive_nameplate_values']=={'2':'Lil Argot','25':'Yifa Sol'}
    assert len(names['native_four_consumer_cases']['rows'])==4
    terms=read(doc['actor_terminology_reconciliation'])
    assert terms['chosen_Daoist_discipline_term']=='Taoist arts' and len(terms['exact_completed_COMMON_Taoist_arts_bindings'])==2
    assert terms['teacher_gender_name_school_country_rank_and_degree_not_given'] and terms['source_onesan_address_is_familiar_stranger_appeal_not_established_kinship']
    receipt=read(CHECKPOINT/'staged_receipt.json')
    for path,digest in {**receipt['evidence'],**receipt['preserved_release_files']}.items():
        assert sha(Path(path).read_bytes())==digest,path
    assert ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4251'
    promoted=read('translations/promoted_build.json')
    assert promoted['profile']=='all-routes-unified-v4204'
    assert sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']
    scope=ledger['unfinished_editorial_scope_v4279']
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    assert scope['remaining_B171_B180_physical_speeches']==198 and scope['incomplete_route_source_prose']==33
    assert scope['canonical_Maria32_pending_uncredited'] and scope['wider_story_shared_town_random_help_prose_open']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4279')
    ROOT.mkdir(parents=True)
    result=dict(checkpoint='V4279',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5725,integrated=5692,pending=33,source_prose=5728,revised=3614,retained=2078,
        new_source_prose_reviews=33,new_completed_records=0,all33_clean_current_references_individual_glosses_retentions_and_native_approval_verified=True,
        all_prior_completions_latest_V4251_promoted_V4204_registry_builder_and_wider_scope_preserved=True,
        native_planes=33,total_macro_cases=264,fresh_macro_cases=16,exact_reused_macro_cases=248,
        source_consumer_negatives=13,macro_negatives=2,formatter_negatives=14,all5_complete_native_sheets_viewed=True,
        source_commands=45,nonrelative_leaves=12,source_pause=[36,38],source_C200_pairs=1,source_end_offsets=[1852,1856],
        actual_selected_B170_IDs=[],new_emulator_runs=0,remaining_B171_B180_physical_speeches=198,
        current_candidate=ledger['current_integrated_candidate']['path'],candidate_sha256=ledger['current_integrated_candidate']['sha256'],
        all_jobs_terminal=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'verified_handoff.json',result)
    save(CHECKPOINT/'checkpoint_receipt.json',{**receipt,'ledger_sha256':result['ledger_sha256'],
        'updated_files':{str(Path(r['target']).relative_to(workspace)):r['planned_sha256'] for r in plan}})
    print('V4279 independently verified:5725/5692/33;5728 source/prose. All33 B170 reviews/native planes and12 retentions bound. V4251/latest and V4204/main unchanged;full goal active.')
