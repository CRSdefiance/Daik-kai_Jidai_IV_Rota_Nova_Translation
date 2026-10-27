"""Prepare B173's exact pending-credit audit without rewriting numeric text literals."""
from pathlib import Path
import io
import re
import tokenize
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_handoff_audit_tools_v4427')
SOURCE=Path('scripts/verify_editorial_handoff_v4380.py')
TARGET=Path('scripts/verify_editorial_handoff_v4427.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    a=text.index('    clarified=next(');b=text.index('    approval=read(',a)
    text=text[:a]+text[b:]
    a=text.index("    controls=read(doc['source_effect_and_predicate_contract'])");b=text.index("    receipt=read(CHECKPOINT/'staged_receipt.json')",a)
    text=text[:a]+'''    controls=read(doc['source_effect_and_predicate_contract'])
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
''' + text[b:]
    a=text.index('    result=dict(')
    text=text[:a]
    changes={
        'scripts.checkpoint_lil_B172_v4379':'scripts.checkpoint_lil_B173_v4426b',
        'editorial_handoff_verification_v4380':'editorial_handoff_verification_v4427',
        'B172':'B173','v4379':'v4426','V4379':'V4426','native_approval_v4378':'native_approval_v4425',
        "{'revise':19,'retain-wording':8}":"{'revise':8,'retain-wording':3}",
        '[2,26,201]':'[2,202]',"approval['narrow_row_count_notes']==13":"approval['narrow_row_count_notes']==5",
        "len(approval['review_sheets'])==4":"len(approval['review_sheets'])==2",
        'all-routes-unified-v4353':'all-routes-unified-v4404','all-routes-unified-v4303':'all-routes-unified-v4353',
        '964c2da7273773c2db63b53eaf1136981d212c4e6282aee303ad101cc508de4e':'cf3df83493af515c5aff02770181684b73e590190efad5b76e198eb690543996',
        'remaining_B173_B180':'remaining_B174_B180',
        'B172_qualified_date_reply_and_B78_later_acquisition_transfer_not_imported':'B172_qualified_date_reply_and_B78_later_acquisition_transfer_not_imported',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    numbers={'5762':'5789','5789':'5800','5792':'5803','3659':'3678','2103':'2111','3936':'3947',
        '4163':'4190','4190':'4201','27':'11','216':'88','15':'13','172':'173','134':'123'}
    tokens=[]
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type==tokenize.NUMBER and token.string in numbers:token=token._replace(string=numbers[token.string])
        tokens.append(token)
    text=tokenize.untokenize(tokens)
    text=text.replace('all27','all11')
    text+='''    result=dict(checkpoint='V4426',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5800,integrated=5789,pending=11,source_prose=5803,revised=3678,retained=2111,
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
'''
    assert 'utf-8' in text and 'utf-3' not in text
    assert 'blocks[173]' in text and 'source_predicate_cases' in text and 'B173_qualified_date' not in text
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),target=str(TARGET),
        target_sha256=sha(TARGET.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),numeric_tokens_only_no_string_literal_count_remap=True,
        pending_credit_once=11,completion_credit=0,full_goal_complete=False))
    print('Prepared exact B173 pending-credit audit;UTF-8 string and all history preserved.')
