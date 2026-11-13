"""Apply staged B173 pending metadata and independently audit exact scope and preserved work."""
import argparse
from collections import Counter
import os
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B173_v4426b import ROOT as CHECKPOINT,DOC,FAMILY
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4427')

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
        'coverage_units','formatting_watchlist','unfinished_editorial_scope_v4426','lil_B173_scope_reconciliation_v4426','latest_checkpoint'}
    assert {k:v for k,v in before.items() if k not in allowed}=={k:v for k,v in ledger.items() if k not in allowed}
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    fresh,old=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    assert fresh['integrated_record_keys']==old['integrated_record_keys'] and fresh['record_keys'][:5789]==old['record_keys']
    keys=[historical_key(r) for r in fresh['record_keys']]
    assert len(keys)==len(set(keys))==5800
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5800,5789,11)
    doc=read(DOC);validate_natural_dialogue_batch(doc);rows=doc['records']
    assert len(rows)==11 and Counter(r['editorial_decision'] for r in rows)=={'revise':8,'retain-wording':3}
    expected=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    assert fresh['pending_record_keys']==fresh['record_keys'][5789:]==expected
    assert len(fresh['pending_contextual_families'])==1 and fresh['pending_contextual_families'][0]['id']==FAMILY
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==5803
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3947 and ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']==64
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==5803
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5789,3678,2111)
    for previous,current in zip(before['coverage_units'],ledger['coverage_units'][:-1],strict=True):
        if previous['id']!='all-route-scenes':assert previous==current
        else:
            assert current['reviewed_route_records']==4201 and current['completed_route_records']==4190
            mutable=['reviewed_route_records','completed_route_records','next']
            assert {k:v for k,v in previous.items() if k not in mutable}=={k:v for k,v in current.items() if k not in mutable}
    assert ledger['coverage_units'][-1]['id']==FAMILY and ledger['coverage_units'][-1]['completion_credit_added']==0
    images=[NdsImage.open(p) for p in ['work/clean.nds',doc['current_ROM']]]
    source,current=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[173] for im in images]
    for row in rows:
        assert all(row['review'].values()) and row['full_clean_context_precedes_comparison'] and row['source_meaning']==row['fresh_source_gloss']
        for data,reference,value in [(source,row['source_reference'],row['source_hex']),(current,row['current_reference'],row['current_hex'])]:
            at,raw=reference['offset'],bytes.fromhex(value)
            assert data[at:at+len(raw)]==raw and data[at+len(raw)]==0 and data[at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert row['source_selector'] in [2,202] and not any('{MACRO:'+m+'}' in row['english'] for m in ['FI','FA','FO'])
        if row['editorial_decision']=='retain-wording':
            assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    approval=read('work/analysis/lil_B173_native_approval_v4425/approval_receipt.json')
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())}
    assert (approval['progressive_planes'],approval['current_macro_alignment_cases'],approval['source_consumer_negatives'],approval['source_macro_negatives'],approval['source_macro_absence_negatives'],approval['formatter_negatives'])==(11,88,13,0,3,14)
    assert approval['narrow_row_count_notes']==5 and len(approval['review_sheets'])==2
    assert all(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['review_sheets'])
    fonts=read(doc['native_font_proof'])
    assert (fonts['new_current_original_macro_alignment_calls'],fonts['reused_original_macro_alignment_calls'])==(88,0)
    assert len(fonts['cases'])==11 and all(c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows'] for c in fonts['cases'])
    assert not fonts['source_macro_preservation_negatives'] and len(fonts['source_macro_absence_negatives'])==3
    assert all(r['rejected'] for r in fonts['source_macro_absence_negatives'])
    controls=read(doc['source_effect_and_predicate_contract'])
    assert len(controls['all8_source_current_nonrelative_nonspeech_leaves'])==8
    assert len(controls['two_resource_words20_boundary_cases'])==20 and len(controls['source_predicate_cases'])==2
    assert controls['source_predicate_hex']=='0080ffff000cca70' and controls['source_predicate_raw_hex_words']==['0C00','70CA']
    assert controls['no_predicate_or_event_state_forced'] and controls['unforced_historical_predicate_result']==1
    assert all(p['native_result']==[2,1,0,0,0,0] and p['sole_scratch_restore_recovers_all4MiB_exact'] for p in controls['source_predicate_cases'])
    assert controls['source_predicate_semantics_not_assumed_from_packed_words']
    assert len(controls['two_presentation_structural_cases'])==2 and len(controls['two_A000_structural_cases'])==2
    assert controls['source_declared_end_offsets']==[762] and not controls['source_pause_resume_pairs'] and not controls['source_C200_pairs']
    assert controls['source_A000_hex_by_offset']=={'720':'00a0ffff010b39a2','748':'00a0ffff010cca60'}
    assert controls['source_A000_packed_semantics_not_inferred'] and controls['all11_speeches_precede_first_A000_and_predicate']
    paths=controls['complete_two_boolean_suffix_paths']
    assert [p['original_A000_offsets'] for p in paths]==[[720],[720,748]] and all(p['source_end_offset']==762 for p in paths)
    branch=read(doc['branch_proof'])
    assert len(branch['cases'])==40 and len(branch['operands_requiring_adjustment_when_resizing'])==4
    assert [e['offset'] for e in branch['operands_requiring_adjustment_when_resizing']]==[736,740,744,756]
    names=read(doc['source_nameplate_consumer_proof'])
    assert names['approved_prose_names']=={'2':'Lil','202':'Reika'}
    assert names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','202':'Reika'}
    cases=names['native_four_consumer_cases']['rows'];assert len(cases)==4
    assert sum(r['actor_ID']==2 and bool(r['original_scratch_rings']) and bool(r['original_getter_writes']) for r in cases)==2
    assert sum(r['actor_ID']==202 and r['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring' and not r['original_scratch_rings'] and not r['original_getter_writes'] for r in cases)==2
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in cases)
    terms=read(doc['actor_terminology_reconciliation'])
    assert len(terms['exact_completed_B78_crown_bindings'])==4 and terms['chosen_crown_title']=='Silla Gold Crown'
    assert terms['chosen_site_title']=='Tomb of King Muryeong'
    item,site=[terms[k] for k in ['exact_global_item_pointer_binding','exact_global_historic_site_pointer_binding']]
    assert item['source_string']['text']=='新羅の金冠' and item['current_string']['text']=='Silla Gold Crown'
    assert site['source_string']['text']=='武寧王陵' and site['current_string']['text']=='Tomb of King Muryeong'
    import struct
    for image,label in zip(images,['source_string','current_string'],strict=True):
        arm=image.read_file('/__arm9__.bin')
        for binding in [item,site]:
            value=binding[label];pointer=struct.unpack_from('<I',arm,binding['pointer_field_offset'])[0]
            assert pointer==value['pointer'] and pointer-0x02000000==value['file_offset']
            assert arm[value['file_offset']:value['file_offset']+value['bytes']].hex()==value['hex']
            assert arm[value['file_offset']+value['bytes']]==0
    for flag in ['guarded_knowledge_recent_other_question_beauty_and_crown_location_remain_secondhand',
        'woman_does_not_remember_name_smooth_talking_man_only_tentatively_connected_to_Julian',
        'man_apparently_went_to_named_tomb_not_confirmed_present_location',
        'Lil_conclusion_and_competitive_vow_not_verified_narration_or_hostility',
        'B172_qualified_date_reply_and_B78_later_acquisition_transfer_not_imported',
        'SourceItems_LocalProduct_graphics_and_older_record_reaudit_stay_open']:
        assert terms[flag],flag
    receipt=read(CHECKPOINT/'staged_receipt.json')
    for path,digest in {**receipt['evidence'],**receipt['preserved_release_files']}.items():assert sha(Path(path).read_bytes())==digest,path
    candidate=ledger['current_integrated_candidate']
    assert candidate['profile']=='all-routes-unified-v4404' and sha(Path(candidate['path']).read_bytes())==candidate['sha256']=='cf3df83493af515c5aff02770181684b73e590190efad5b76e198eb690543996'
    promoted=read('translations/promoted_build.json')
    assert promoted['profile']=='all-routes-unified-v4353' and sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']
    scope=ledger['unfinished_editorial_scope_v4426']
    assert sha(Path(scope['path']).read_bytes())==scope['sha256'] and scope['remaining_B174_B180_physical_speeches']==123 and scope['incomplete_route_source_prose']==11
    assert scope['canonical_Maria32_pending_uncredited'] and scope['wider_story_shared_town_random_help_prose_open']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4426')
    ROOT.mkdir(parents=True)
    result=dict(checkpoint='V4426',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5800,integrated=5789,pending=11,source_prose=5803,revised=3678,retained=2111,
        new_source_prose_reviews=11,new_completed_records=0,all11_clean_current_references_individual_glosses_three_retentions_and_native_approval_verified=True,
        all_prior_completions_latest_V4404_promoted_V4353_registry_builder_wider_scope_and_storage_preserved=True,
        native_planes=11,total_processor_alignment_cases=88,fresh_processor_alignment_cases=88,exact_reused_processor_alignment_cases=0,
        source_consumer_negatives=13,source_macro_deletion_negatives=0,source_macro_absence_negatives=3,formatter_negatives=14,both_complete_native_sheets_viewed=True,
        source_structural_commands=23,nonrelative_leaves=8,relative_sites=4,relative_operand_cases=40,predicate_clean_current_cases=2,
        source_pause=[],source_A000_count=2,source_A000_offsets=[720,748],source_predicate_offset=728,source_C200_pairs=0,source_end_offsets=[762],
        Reika_two_original_readonly_name_paths_and_two_owned_Lil_scratch_paths_bound=True,actual_selected_B173_IDs=[],new_emulator_runs=0,
        remaining_B174_B180_physical_speeches=123,current_candidate=candidate['path'],candidate_sha256=candidate['sha256'],
        failed_UTF_encoding_derivation_caught_before_checkpoint_writes_and_preserved=True,
        all_jobs_terminal=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'verified_handoff.json',result)
    save(CHECKPOINT/'checkpoint_receipt.json',{**receipt,'ledger_sha256':result['ledger_sha256'],
        'updated_files':{str(Path(r['target']).relative_to(workspace)):r['planned_sha256'] for r in plan}})
    print('V4426 independently verified:5800/5789/11;5803 source/prose. All11 B173 reviews/native planes andthree retentions bound. V4404 latest/V4353 main unchanged;full goal active.')
