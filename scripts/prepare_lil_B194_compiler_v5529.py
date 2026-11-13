"""Prepare source-locked atomic integration for conditional B194 with one original FI."""
import re
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.seal_lil_B194_references_v5526 import FLAGS
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B194_compiler_tools_v5529')
CONTRACT = '''    require(len(controls['relocated_dispatch_cases'])==11 and len(controls['all6_source_current_target_nonrelative_nonspeech_leaves'])==6,'complete relocated controls required')
    require(controls['changed_unaligned_operand_scratch_owned_and_restored'] and len(controls['unforced_relocated_predicate_cases'])==1,'relocated predicate proof required')
    pred=controls['unforced_relocated_predicate_cases'][0]
    require((pred['source_offset'],pred['target_offset'])==(312,274) and pred['case']['native_result']==[2,0,0,0,0,0]
        and len(pred['case']['original_unaligned_operand_read_scratch_writes'])==1
        and pred['case']['sole_scratch_restore_recovers_all4MiB_exact'],'unaligned availability scratch differs')
    priors=[0,1,2,3,0xFFFFFFFF]
    ui=controls['relocated_C200_prior_result_cases'];resources=controls['relocated_resource42_prior_result_cases'];end_prior=controls['relocated_end_prior_result_cases']
    require(len(ui)==10 and {(r['source_offset'],r['target_offset'],r['prior_result']) for r in ui}=={
        (a,b,p) for a,b in [(494,464),(534,508)] for p in priors},'both UI sites/all priors required')
    require(all(r['case']['native_result']==[3,r['prior_result'],0,0,0,0]
        and r['case']['source_owned_UI_request_words']==[1,2,13,0,0,0,1] for r in ui),'C200 ownership/carried result differs')
    require(len(resources)==10 and all((r['source_offset'],r['target_offset'])==(406,376) for r in resources)
        and {(r['case']['previous_result'],r['case']['incidental_boundary_return']) for r in resources}=={(p,v) for p in priors for v in [0,priors[-1]]}
        and all(r['case']['native_result']==[3,r['case']['previous_result'],0,0,0,0] for r in resources),'resource42 boundary/all priors differ')
    require(len(end_prior)==5 and {r['prior_result'] for r in end_prior}==set(priors)
        and all(r['target_offset']==510 and r['native_result']==[0,r['prior_result'],0,0,0,0] for r in end_prior),'end carried result differs')
    require([len(p['speech_record_indices']) for p in controls['relocated_structural_predicate0_1_paths']]==[9,11],'conditional path scope differs')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',536),('research',510)],'guarded end decodes required')
    progressive={'6':'Julio Erneco','117':'Port Worker','156':'Sailor'}
    full={'6':'Julio Erneco','117':'Port Worker','156':'Retainer'}
    require(names['progressive_nameplate_values']==progressive and names['full_catalogue_values']==full,'exact original names/roles required')
    name_rows=names['native_six_consumer_cases']['rows']
    require(len(name_rows)==6 and {(r['consumer'],r['actor_ID']):r['text'] for r in name_rows}=={
        **{('progressive-nameplate',int(i)):v for i,v in progressive.items()},**{('full-catalogue',int(i)):v for i,v in full.items()}},'six original name consumers required')
    require(sum(r['ownership_mode']=='original-owned-name-scratch-ring' for r in name_rows)==2
        and all(r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] and r['all_actor_models_and_unowned4MiB_exact'] for r in name_rows)
        and all((r['actor_ID']==6)==bool(r['original_scratch_rings']) for r in name_rows),'mixed name ownership differs')
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh3_actor_names']['rows']}=={6:5,117:0,156:4},'three original voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['approved_prose_names']==progressive and terms['full_catalogue_names']==full
        and terms['commodity_index']==37 and terms['source_commodity']=='清酒' and terms['commodity']=='Sake'
        and terms['city']=='Hangzhou' and terms['one_source_current_city_alias']['text']=='Hangzhou'
        and terms['commodity_binding']['text']=='Sake' and terms['original_commodity_metadata_hex']=='d00705db84030100'
        and terms['FI_default_expansion']=='Lil' and terms['FI_default_ASCII_bytes']==3
        and terms['source_title']=='提督' and terms['source_supported_English_title']=='Admiral','exact names/commodity/FI title required')
    for flag in ['two_owned_Julio_scratch_consumers_and_four_original_readonly_role_consumers_preserve_unowned4MiB',
        'source_recent_experiences_casual_taste_rice_hearsay_surprise_thirst_invitation_acceptance_and_urgency_preserved',
        'rice_ingredient_remains_reported_not_recipe_technical_process_origin_or_narrator_fact',
        'legendary_liquor_is_Julios_excited_inference_not_certified_identity_award_or_earned_item',
        'conditional_Julio5_voice_and_source_explicit_FI_Admiral_address_not_invented_kinship_or_new_rank',
        'no_invented_brotherhood_player_employment_shared_drinking_history_or_new_personal_name',
        'source_now_drink_invitation_and_later_urgent_purchase_are_intentions_not_completed_actions',
        'no_price_amount_measured_serving_venue_recipe_origin_health_effect_intoxication_or_reward_invented',
        'Sake37_individual_commodity_and_one_Hangzhou_alias_not_category_or_new_UI_fidelity_credit',
        'Sake37_older_UI_fidelity_review_remains_open_separate_from_dialogue',
        'tentative_Sake_Hangzhou_FE_not_earlier_location_or_earned_fashion',
        'source21_commands_one_predicate_four_relatives_resource42_two_C200_one_FI_and_single_end_preserved',
        'all11_clean_first_glosses_precede_predecessor_English_prose_comparison',
        'raw_current_dispatch_hex_is_structural_evidence_not_translation_source']:
        require(terms.get(flag) is True,'source context required:'+flag)
    layout=load(doc['layout_QA_proof'])
    require(not layout['failures'] and len(layout['records'])==11 and len(layout['row_count_notes'])==3
        and doc['all11_current_native_previews_viewed_on_two_sheets'] and doc['viewed_phrases_use_full_verified_width_and_complete_clauses']
        and doc['no_record_specific_ordinary_boundary_exception_required'] and doc['no_shared_metric_guard_or_manual_break_change'],'viewed layout/reasons differ')
    require(sample['all11_panels10_progressive1_FE_one_FI_and_normal_returns_pass'] and sample['original21_commands_four_relative_sites_and_one_declared_end_preserved']
        and sample['default_source_availability0_and_original_recruitment_setup_availability1_observed_without_forcing']
        and sample['source_resource42_and_two_C200_paths_observed_in_conditional_setup']
        and sample['extra_original_B165_recruitment_initializer_is_disclosed_test_setup_not_earned_progress']
        and sample['no_open_translation_specific_display_or_control_finding'] and not sample['offline_only_display_IDs'],'representative scope required')
    require(observed['unique_actual_display_objects']==11 and observed['actual_panel_observations_across_setups']==20
        and observed['sampled_nontext_pairs']==230 and observed['total_paired_fullscreen_views']==24
        and observed['all_content_jobs_terminal_and_reaped'] and observed['actual_new_cold_boot_runs']==4 and observed['total_frames']==36004
        and not observed['visual_review_pending'] and observed['default_name_Lil_actual_FI_display_verified_all_custom_name_lengths_not_claimed']
        and observed['no_PRNG_causal_future_world_full_RAM_or_hardware_equivalence_claim'],'complete viewed actual scope required')
    require(len(observed['versions'])==2 and observed['offline_only_display_IDs']==[],'two distinct actual setups required')
    actuals=[]
    for index,v in enumerate(observed['versions']):
        expected,selected,stored_count,outcome,exit_frame=[(9,24,30,0,5017),(11,30,31,1,5737)][index]
        require(v['predicate_result']==outcome and v['actual_selected_fixture_commands']==selected and v['stored_fixture_commands']==stored_count
            and v['return_frames']==[exit_frame,exit_frame] and v['complete_native_holds']==[35,44][index]
            and v['timing_differences']==dict(total=0,speech=0,control_or_end=0) and v['sampled_nontext_pairs']==115
            and v['sampled_postscene_and_final_RGB_equal'] and v['all_five_native_groups_and_whole1A04_actor_and_captain2_equal']
            and v['final_PRNG_seeds']==[3723009301,3723009301],'measured per-setup timing/state differs')
        require(sha(Path(v['actual_proof']).read_bytes())==v['actual_proof_sha256']
            and sha(Path(v['visual_analysis']).read_bytes())==v['visual_analysis_sha256'],'actual evidence differs')
        actual=load(v['actual_proof']);analysis=load(v['visual_analysis']);actuals.append(actual)
        require(actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==expected
            and not actual['failures'] and not actual['paired_region_differences'],'actual native planes differ')
        require(analysis['postscene9001_native_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True)
            and not analysis['actual_timing_differences'] and not analysis['nontext_difference_samples'],'measured raw state/timing differs')
        require(len(v['viewed_sheets'])==5 and all(s['viewed_after_image_return'] and not s['visual_review_pending']
            and sha(Path(s['path']).read_bytes())==s['sha256'] for s in v['viewed_sheets']),'actual views differ')
        for version in actual['versions']:
            require(len(version['selected_B22_command_pairs'])==selected and len(version['selected_intervals'])==expected
                and version['fixture_exit_frame']==exit_frame and version['single_source_end536_actually_reached']
                and version['selected_B22_command_pairs'][-1]['result_words']==[0,outcome]
                and version['selected_B22_command_pairs'][-1]['original_source_offset']==536,'actual source path/end differs')
            require(len(version['actual_predicate_transitions'])==1 and version['actual_predicate_transitions'][0]['source_offset']==312
                and version['actual_predicate_transitions'][0]['result']==outcome,'actual original availability differs')
            ui=version['source_C200']
            require([r['original_source_offset'] for r in ui]==([534] if index==0 else [494,534])
                and all(r['word']==0xC200 and r['extent']==2 and r['result_words']==[3,outcome] for r in ui),'actual UI path differs')
            require(len(version['source_A000'])==1 and version['source_A000'][0]['original_source_offset']==8,'source A000 differs')
            if index==1:
                require(sum(r.get('disclosed_original_recruitment_initializer',False) for r in version['selected_B22_command_pairs'])==1
                    and sum(r['word']==0x632A for r in version['selected_B22_command_pairs'])==1,'original recruitment/resource42 setup differs')
    require(load(conf['actual_proof'])==observed,'combined actual proof differs')
    require([{k:s[k] for k in ['path','sha256']} for s in approval['reviewed_sheets']]==native['review_sheets'],'native sheet approval differs')
    for s in approval['reviewed_sheets']:require(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256'],'native view differs')
'''

if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('dk4tool/patch/lil_B193_editorial_v1.py');text=source.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index('\ndef load',a)
    c=text.index("    require(len(controls['relocated_dispatch_cases'])");e=text.index("    rows=doc['records']",c)
    changes={text[a:b]:'FLAGS='+repr(FLAGS)+'\n',text[c:e]:CONTRACT,
        'B193':'B194','SELECTORS={166,167,168,254}':'SELECTORS={6,117,156,254}',
        "'layout_retention_review_proof'":"'layout_QA_proof'",
        "len(native['cases'])==15":"len(native['cases'])==11","native['current_original_macro_alignment_calls']==120":"native['current_original_macro_alignment_calls']==88",
        "native['complete_progressive_planes']==14":"native['complete_progressive_planes']==10","len(native['negative_controls'])==20":"len(native['negative_controls'])==24",
        "len(stored['final_target_parity_cases'])==15":"len(stored['final_target_parity_cases'])==11","stored['current_final_stored_macro_alignment_cases']==60":"stored['current_final_stored_macro_alignment_cases']==44",
        "stored['new_parity_macro_alignment_cases']==32":"stored['new_parity_macro_alignment_cases']==20","stored['exact_byte_identical_reused_macro_alignment_cases']==28":"stored['exact_byte_identical_reused_macro_alignment_cases']==24",
        'all15_final_targets':'all11_final_targets','len(rows)==len(set(ids))==15':'len(rows)==len(set(ids))==11','fifteen exact records':'eleven exact records',
        "{'progressive':14,'system-FE':1}":"{'progressive':10,'system-FE':1}","{'revise':8,'retain-wording':7}":"{'revise':4,'retain-wording':7}",
        "and all([r['id'] for r in v['selected_intervals']]==ids for v in actual['versions'])":"and observed['actual_sampled_display_IDs']==ids and all([r['id'] for r in v['selected_intervals']]==ids for v in actuals[1]['versions'])",
        "mapping['blocks'][0]['block']==193":"mapping['blocks'][0]['block']==194",'old_blocks[193]':'old_blocks[194]','blocks[193]':'blocks[194]',
        "row['source_reference']['block']==193":"row['source_reference']['block']==194","row['block']==193":"row['block']==194",'block=193':'block=194',
        "spec['source_bytes']==len(block)==668 and spec['source_logical_end']==666 and spec['research_bytes']==spec['research_logical_end']==676":
        "spec['source_bytes']==len(block)==540 and spec['source_logical_end']==540 and spec['research_bytes']==516 and spec['research_logical_end']==514",
        "require(not macros,'source has no FI/FA/FO substitutions')":"require(macros==Counter({b'FI':1}),'one original FI required')",
        "and not spec['relative_skip_fixups'] and not spec['target_native_skip_cases']":"and len(spec['relative_skip_fixups'])==4 and len(spec['target_native_skip_cases'])==20",
        'end==666 and len(block)==668 and block[end:]==bytes(2)':'end==540 and len(block)==540 and block[end:]==bytes()',
        'mapped(end)==676':'mapped(end)==514',
        "    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)":
        """    expected_edges=[(320,0x200,4,328),(324,0x300,4,332),(328,0x100,168,500),(496,0x100,0,500)]
    fixups=spec['relative_skip_fixups']
    require([(r['offset'],r['word'],r['source_span'],r['matched_skip_target']) for r in fixups]==expected_edges,'source relative sites differ')
    for edge in fixups:
        a,b=edge['offset'],edge['new_offset'];finish=mapped(edge['matched_skip_target']);span=finish-b-4
        require(b==mapped(a) and edge['span_field_offset']==a+2 and edge['unmatched_next_offset']==a+4
            and edge['new_unmatched_next']==b+4 and edge['new_matched_skip_target']==finish and edge['target_span']==span
            and struct.unpack_from('<H',block,a+2)[0]==edge['source_span'] and 0<=span<=0xFFFF and span%2==0,'relative map differs')
        struct.pack_into('<H',logical,b+2,span)
    cases=spec['target_native_skip_cases']
    require({(r['new_offset'],r['last_result']) for r in cases}=={(r['new_offset'],p) for r in fixups for p in priors},'all target skip inputs required')
    for case in cases:
        edge=next(e for e in fixups if e['new_offset']==case['new_offset']);p=case['last_result'];word=edge['word']
        take=word==0x100 or (word==0x200 and p==0) or (word==0x300 and p==1)
        require(case['native_extent']==4+(edge['target_span'] if take else 0)
            and case['ABI_all4MiB_owner_stream_result_length_and_guards_exact'],'target skip extent/ownership differs')
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)""",
        'len(target)==676 and target[676:]==bytes()':'len(target)==516 and target[514:]==bytes(2)',
        'len(commands)==18':'len(commands)==21',"sum(c['word']==0x4000 for c in commands)==15":"sum(c['word']==0x4000 for c in commands)==11",
        "require(not c['source_0100_ancestors'] and not c['target_0100_ancestors'],'invented ancestor')":
        "require(c['target_0100_ancestors']==[mapped(a) for a in c['source_0100_ancestors']],'relative ancestry differs')",
        "        else:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque leaf differs')":
        "        elif c['word'] not in [0x100,0x200,0x300]:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque leaf differs')",
        '==[(662,672)]':'==[(536,510)]',"leaves=[c for c in commands if c['word']!=0x4000]":"leaves=[c for c in commands if c['word'] not in [0x4000,0x100,0x200,0x300]]",
        "[(8,'00a0ffff011d39a1'),(660,'00c2'),(662,'00000000')]":"[(8,'00a0ffff012536a1'),(312,'0080ffff06fe0030'),(406,'2a63'),(494,'00c2'),(534,'00c2'),(536,'00000000')]",
        'three exact leaves required':'six exact leaves required','==[0xA000,0xC200,0]':'==[0xA000,0x8000,0x632A,0xC200,0xC200,0]',
        "    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']":
        "    for edge in fixups:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])\n    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']",
        'new_blocks[193]':'new_blocks[194]','==[193]':'==[194]','relative_operands=0':'relative_operands=4','source_commands=18':'source_commands=21',
        'all15_progressive_FE_speeches_no_macros_A000_C200_and_single_end_preserved':'all11_progressive_FE_speeches_one_FI_A000_availability_resource42_two_C200_and_single_end_preserved',
        'actual_two_complete_B22_fixtures_three_portraits_115_regions_59_holds_10_speech_timings_equal_postscene_RGB_and_measured_PRNG_not_natural_activation':
        'actual_four_B22_fixtures_two_unforced_paths_original_recruitment_setup_230_regions79_holds_equal_measured_postscene_state_not_natural_activation',
    }
    assert all(k in text for k in changes)
    planned=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)
    compile(planned,'dk4tool/patch/lil_B194_editorial_v1.py','exec')
    old,new=native_numbers(text),native_numbers(planned)
    assert old-new==Counter({463267532:2}) and new-old==Counter({3723009301:2,4294967295:1})
    row=derive(source,'dk4tool/patch/lil_B194_editorial_v1.py',changes)
    assert Path(row['successor']).read_text(encoding='utf-8')==planned
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_atomic_compiler.json',dict(derivation=row,
        only_high_constant_changes_are_measured_PRNG_and_one_explicit_prior_mask=True,
        all21_commands4_spans1_FI_both_UI_resource_predicate_alignment_full_metadata_and_inverse_guarded=True,
        mixed_Julio_name_ownership_roles_voices_source_reportedness_intentions_title_and_two_actual_setups_guarded=True,
        every_check_precedes_single_replace_file=True,new_review_credit=0,full_goal_complete=False))
