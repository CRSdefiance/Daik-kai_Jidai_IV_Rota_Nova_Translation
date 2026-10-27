"""Apply staged B172 pending metadata and independently audit exact scope and preserved work."""
import argparse
from collections import Counter
import os
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B172_v4379 import ROOT as CHECKPOINT,DOC,FAMILY
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4380')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    assert not ROOT.exists()
    workspace=Path.cwd().resolve();plan=read(CHECKPOINT/'mutation_plan.json');assert len(plan)==6
    if args.apply:
        for item in plan:
            target,staged=Path(item['target']),Path(item['planned'])
            assert target.is_relative_to(workspace) and staged.is_relative_to(CHECKPOINT.resolve())
            assert sha(target.read_bytes())==item['before_sha256'] and sha(staged.read_bytes())==item['planned_sha256']
            assert staged.stat().st_size>=target.stat().st_size
        for item in plan:
            with Path(item['target']).open('r+b') as stream:
                stream.write(Path(item['planned']).read_bytes());stream.flush();os.fsync(stream.fileno())
            assert sha(Path(item['target']).read_bytes())==item['planned_sha256']
    for item in plan:
        assert Path(item['target']).read_bytes()==Path(item['planned']).read_bytes()
        assert sha(Path(item['target']).read_bytes())==item['planned_sha256']
    lp=Path('translations/editorial_review_current_v1.json');ledger,before=read(lp),read(CHECKPOINT/(lp.name+'.before'))
    assert lp.read_bytes()==encode_ledger(ledger) and lp.stat().st_size<100*1024*1024
    allowed={'records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file',
        'reviewed_but_incomplete_route_record_IDs','active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871',
        'coverage_units','formatting_watchlist','unfinished_editorial_scope_v4379','lil_B172_scope_reconciliation_v4379','latest_checkpoint'}
    assert {k:v for k,v in before.items() if k not in allowed}=={k:v for k,v in ledger.items() if k not in allowed}
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    fresh,old=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    assert fresh['integrated_record_keys']==old['integrated_record_keys'] and fresh['record_keys'][:5762]==old['record_keys']
    keys=[historical_key(r) for r in fresh['record_keys']]
    assert len(keys)==len(set(keys))==5789
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5789,5762,27)
    doc=read(DOC);validate_natural_dialogue_batch(doc);rows=doc['records']
    assert len(rows)==27 and Counter(r['editorial_decision'] for r in rows)=={'revise':19,'retain-wording':8}
    expected=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    assert fresh['pending_record_keys']==fresh['record_keys'][5762:]==expected
    assert len(fresh['pending_contextual_families'])==1 and fresh['pending_contextual_families'][0]['id']==FAMILY
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==5792
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3936 and ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']==64
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==5792
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5762,3659,2103)
    for previous,current in zip(before['coverage_units'],ledger['coverage_units'][:-1],strict=True):
        if previous['id']!='all-route-scenes':assert previous==current
        else:
            assert current['reviewed_route_records']==4190 and current['completed_route_records']==4163
            mutable=['reviewed_route_records','completed_route_records','next']
            assert {k:v for k,v in previous.items() if k not in mutable}=={k:v for k,v in current.items() if k not in mutable}
    assert ledger['coverage_units'][-1]['id']==FAMILY and ledger['coverage_units'][-1]['completion_credit_added']==0
    images=[NdsImage.open(p) for p in ['work/clean.nds',doc['current_ROM']]]
    source,current=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[172] for im in images]
    for row in rows:
        assert all(row['review'].values()) and row['full_clean_context_precedes_comparison'] and row['source_meaning']==row['fresh_source_gloss']
        for data,reference,value in [(source,row['source_reference'],row['source_hex']),(current,row['current_reference'],row['current_hex'])]:
            at,raw=reference['offset'],bytes.fromhex(value)
            assert data[at:at+len(raw)]==raw and data[at+len(raw)]==0 and data[at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert row['source_selector'] in [2,26,201] and not any('{MACRO:'+m+'}' in row['english'] for m in ['FI','FA','FO'])
        if row['editorial_decision']=='retain-wording':
            assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    clarified=next(r for r in rows if r['source_record_index']==11)
    assert clarified['historical_clean_first_gloss'] and clarified['clean_gloss_precision_note'] and 'literal again' in clarified['source_meaning']
    approval=read('work/analysis/lil_B172_native_approval_v4378/approval_receipt.json')
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())}
    assert (approval['progressive_planes'],approval['current_macro_alignment_cases'],approval['source_consumer_negatives'],approval['source_macro_negatives'],approval['source_macro_absence_negatives'],approval['formatter_negatives'])==(27,216,15,0,3,14)
    assert approval['narrow_row_count_notes']==13 and len(approval['review_sheets'])==4
    assert all(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['review_sheets'])
    fonts=read(doc['native_font_proof'])
    assert (fonts['new_current_original_macro_alignment_calls'],fonts['reused_original_macro_alignment_calls'])==(216,0)
    assert len(fonts['cases'])==27 and all(c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows'] for c in fonts['cases'])
    assert not fonts['source_macro_preservation_negatives'] and len(fonts['source_macro_absence_negatives'])==3
    assert all(r['rejected'] for r in fonts['source_macro_absence_negatives'])
    controls=read(doc['source_effect_and_predicate_contract'])
    assert len(controls['all11_source_current_nonrelative_nonspeech_leaves'])==11 and len(controls['three_resource_words30_boundary_cases'])==30
    assert len(controls['source_C200_pairs'])==1 and len(controls['source_C200_pairs'][0]['cases'])==2
    assert len(controls['five_presentation_structural_cases'])==5 and len(controls['one_later_A000_structural_case'])==1
    assert controls['source_declared_end_offsets']==[1880] and not controls['source_pause_resume_pairs']
    assert controls['no_source_2000_pause_FE_2100_4100_membership_predicate_or_relative_sites']
    assert controls['source_A000_hex']=='00a0ffff010cc960' and controls['source_A000_raw_hex_words']==['0C01','60C9']
    assert controls['source_C2001868_then_A0001870_then6240_1878_then_end1880_preserved'] and controls['source_A000_packed_semantics_not_inferred']
    names=read(doc['source_nameplate_consumer_proof'])
    assert names['approved_prose_names']=={'2':'Lil','26':'Julian','201':'Mihwa'}
    assert names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','26':'Julian Lopes','201':'Mihwa'}
    cases=names['native_six_consumer_cases']['rows'];assert len(cases)==6
    assert all(r['original_scratch_rings'] and r['original_getter_writes'] for r in cases if r['actor_ID'] in [2,26])
    assert len([r for r in cases if r['actor_ID']==201])==2 and all(r['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring' and not r['original_scratch_rings'] and not r['original_getter_writes'] for r in cases if r['actor_ID']==201)
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in cases)
    terms=read(doc['actor_terminology_reconciliation'])
    assert len(terms['exact_completed_B78_title_bindings'])==4 and terms['chosen_crown_title']=='Silla Gold Crown'
    item=terms['exact_global_item_pointer_binding'];assert item['source_string']['text']=='新羅の金冠' and item['current_string']['text']=='Silla Gold Crown'
    city=terms['exact_Seoul_route_map_string_binding'];assert city['source_Japanese']=='京城' and city['approved_English']=='Seoul'
    for image,key in zip(images,['source_hex','current_hex'],strict=True):
        arm=image.read_file('/__arm9__.bin');value=bytes.fromhex(city[key]);assert arm[city['offset']:city['offset']+len(value)]==value
    assert terms['explicit_conditional_date_request_and_Mihwa_will_think_about_it_are_distinct']
    assert terms['Julian_promise_interpretation_is_his_overeager_response_not_her_confirmed_consent']
    assert terms['initial_offer_to_show_Lil_and_final_request_for_Lil_to_show_Mihwa_preserve_role_reversal']
    assert terms['SourceItems_LocalProduct_broader_review_and_later_older_record_reaudit_stay_open']
    receipt=read(CHECKPOINT/'staged_receipt.json')
    for path,digest in {**receipt['evidence'],**receipt['preserved_release_files']}.items():assert sha(Path(path).read_bytes())==digest,path
    candidate=ledger['current_integrated_candidate']
    assert candidate['profile']=='all-routes-unified-v4353' and sha(Path(candidate['path']).read_bytes())==candidate['sha256']=='964c2da7273773c2db63b53eaf1136981d212c4e6282aee303ad101cc508de4e'
    promoted=read('translations/promoted_build.json')
    assert promoted['profile']=='all-routes-unified-v4303' and sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']
    scope=ledger['unfinished_editorial_scope_v4379']
    assert sha(Path(scope['path']).read_bytes())==scope['sha256'] and scope['remaining_B173_B180_physical_speeches']==134 and scope['incomplete_route_source_prose']==27
    assert scope['canonical_Maria32_pending_uncredited'] and scope['wider_story_shared_town_random_help_prose_open']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4379')
    ROOT.mkdir(parents=True)
    result=dict(checkpoint='V4379',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5789,integrated=5762,pending=27,source_prose=5792,revised=3659,retained=2103,
        new_source_prose_reviews=27,new_completed_records=0,all27_clean_current_references_individual_glosses_eight_retentions_and_native_approval_verified=True,
        all_prior_completions_latest_V4353_promoted_V4303_registry_builder_wider_scope_and_storage_preserved=True,
        native_planes=27,total_processor_alignment_cases=216,fresh_processor_alignment_cases=216,exact_reused_processor_alignment_cases=0,
        source_consumer_negatives=15,source_macro_deletion_negatives=0,source_macro_absence_negatives=3,formatter_negatives=14,all4_complete_native_sheets_viewed=True,
        source_commands=38,nonrelative_leaves=11,source_pause=[],source_A000_count=1,source_A000_hex='00a0ffff010cc960',source_C200_pairs=1,source_end_offsets=[1880],
        Mihwa_two_original_readonly_name_paths_and_four_owned_Lil_Julian_scratch_paths_bound=True,actual_selected_B172_IDs=[],new_emulator_runs=0,
        remaining_B173_B180_physical_speeches=134,current_candidate=candidate['path'],candidate_sha256=candidate['sha256'],
        all_jobs_terminal=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'verified_handoff.json',result)
    save(CHECKPOINT/'checkpoint_receipt.json',{**receipt,'ledger_sha256':result['ledger_sha256'],
        'updated_files':{str(Path(r['target']).relative_to(workspace)):r['planned_sha256'] for r in plan}})
    print('V4379 independently verified:5789/5762/27;5792 source/prose. All27 B172 reviews/native planes andeight retentions bound. V4353 latest/V4303 main unchanged;full goal active.')
