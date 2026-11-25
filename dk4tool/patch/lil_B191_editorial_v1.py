"""Atomic B191 whole-exchange localization with distinct progressive and FE contracts."""
import json
import re
import struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B191_layout_v3 as codec
from dk4tool.dialogue.lil_B191_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B191_editorial_release_v1.json'
SELECTORS={86,154,254}
FLAGS=['all38_structural_commands_verified', 'all13_active_speech_targets_preserved', 'all9_nonrelative_leaves_three_mixed_predicates_four_A000_C200_end_exact', 'all16_relative_sites_and80_native_skip_cases_preserved', 'all125_mapped_structural_paths_preserve_all13_speeches_and_no_effect_paths', 'progressive12_impersonal_FE1_and_FI0_FA0_FO0_preserved', 'single_end730_target676_preserved', 'no_source2000_pause_2100_4100_resources_or_presentations', 'original_mixed_RNG_semantics_and_packed_effect_bytes_preserved', 'source_and_target_prefix6_to128_byte_exact', 'exact_R64_source_prose_wrap_preserved', 'representative_actual_display_controls_and_parent_return_approved']

def load(path):
    return json.loads(Path(path).read_bytes())

def require(value,message):
    if not value:raise ValueError('Lil B191 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path)
    require(conf.get('format')=='dk4-lil-B191-editorial-release-v1','unknown release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical script differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean input differs')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean script differs')
    doc,mapping=load(conf['manuscript']),load(conf['reference_map']);validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1'
        and doc['formatting_review_pending'] is False and all(all(r['review'].values()) for r in doc['records']),'five-gate manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(doc['reference_map']).read_bytes()),'approved map differs')
    require(mapping['format']=='dk4-lil-B191-source-relocation-map-v1' and mapping['external_references_complete']
        and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete source map required')
    for flag in FLAGS:require(mapping.get(flag) is True,'missing map approval:'+flag)
    proof_keys=['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof',
        'source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof','layout_retention_review_proof','carried_result_proof','source_bound_wrap_refinement_proof']
    for key in proof_keys:require(sha(Path(doc[key]).read_bytes())==doc[key+'_sha256'],'proof differs:'+key)
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B191_layout_v3.py')
        and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B191_profile.py'),'scoped formatter/profile required')
    native,stored,controls,sample,ends,names=[load(doc[k]) for k in proof_keys[:6]]
    observed=load(doc['postscene_native_state_proof'])
    require(len(native['cases'])==13 and native['current_original_macro_alignment_calls']==104
        and native['complete_progressive_planes']==12 and native['complete_FE_logical_and_physical_planes']==1,'complete native consumers required')
    require(len(native['negative_controls'])==18 and all(r['rejected'] for r in native['negative_controls']),'source-consumer negatives required')
    approval=load(conf['native_approval'])
    require(len(approval['formatter_negatives'])==len(set(approval['formatter_negatives']))==28
        and all(isinstance(r,str) and r for r in approval['formatter_negatives']),'formatter negatives required')
    require(len(stored['final_target_parity_cases'])==13 and stored['current_final_stored_macro_alignment_cases']==52
        and stored['new_parity_macro_alignment_cases']==12 and stored['exact_byte_identical_reused_macro_alignment_cases']==40
        and stored['all13_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored proof required')
    require(len(controls['relocated_dispatch_cases'])==13 and len(controls['all9_exact_nonrelative_leaves'])==9
        and len(controls['predicate_pairs'])==3 and len(controls['C200_pairs'])==1 and len(controls['A000_structural_pairs'])==4
        and len(controls['all125_source_and_relocated_structural_paths_identical'])==125,'complete relocated controls required')
    require([(p['old_offset'],p['new_offset']) for p in controls['predicate_pairs']]==[(8,8),(28,28),(76,76)],'exact predicate sites required')
    for pair in controls['predicate_pairs']:
        require(len(pair['cases'])==2 and pair['old_offset']%4==0 and pair['new_offset']%4==0,'source predicate alignment differs')
        threshold={8:500,28:700,76:500}[pair['old_offset']]
        require(all(r['threshold']==threshold for r in pair['cases']),'source raw threshold differs')
        a,b=pair['cases'];require(a['native_result']==b['native_result'] and a['after_seed']==b['after_seed'],'predicate pair differs')
        require(all(r['unforced_current_snapshot'] and r['full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch'] for r in pair['cases']),'original RNG and operand ownership required')
        require(not a['operand_pointer_unaligned'] and not b['operand_pointer_unaligned']
            and not a['unaligned_operand_scratch_writes']
            and b['unaligned_operand_scratch_writes']==([dict(PC=0x0202A5D8,address=0x02279600,size=4,value=threshold)] if b['operand_pointer_unaligned'] else []),'original operand scratch differs')
    ownership=load(conf['operand_ownership_proof'])
    require(len(ownership['cases'])==36 and ownership['unforced_cases']==9 and ownership['CPU_only_boundary_fixture_cases']==27
        and ownership['actual_emulator_seed_writes']==0,'complete operand alignment proof required')
    require(Counter(r['version'] for r in ownership['cases'])=={'clean':12,'current':12,'relocated':12}
        and sum(r['operand_pointer_unaligned'] for r in ownership['cases'])==0,'aligned source/current/target coverage required')
    require(len({(r['version'],r['offset'],r['supplied_CPU_only_seed_fixture']) for r in ownership['cases']})==36
        and Counter((r['version'],r['offset']) for r in ownership['cases'])=={(v,at):4 for v in ['clean','current','relocated'] for at in [8,28,76]},'exact mixed-predicate coverage keys required')
    for r in ownership['cases']:
        require((r['supplied_CPU_only_seed_fixture'] is None)==r['unforced_current_snapshot']
            and (r['unforced_current_snapshot'] or r['before_seed']==r['supplied_CPU_only_seed_fixture']),'CPU fixture provenance differs')
    for r in ownership['cases']:
        threshold={8:500,28:700,76:500}[r['offset']]
        expected_seed=(r['before_seed']*0x41C64E6D+0x3039)&0xFFFFFFFF
        roll=((expected_seed>>16)&0x7FFF)%1000;result=0 if roll<threshold else 1 if roll==threshold else 2
        writes=([dict(PC=0x0202A5D8,address=0x02279600,size=4,value=threshold)] if r['operand_pointer_unaligned'] else [])
        writes.append(dict(PC=0x020D984C,address=0x02168EB8,size=4,value=expected_seed))
        require(r['after_seed']==expected_seed and r['roll']==roll and r['native_result']==[2,result,0,0,0,0]
            and r['bound']==1000 and r['threshold']==threshold and r['all_original_native_writes']==writes
            and r['full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch']
            and r['cleanup_restores_only_owned_seed_and_optional_scratch_and_recovers_all4MiB'],'exact native ownership differs')
    for version in ['clean','current','relocated']:
        for at,threshold in [(8,500),(28,700),(76,500)]:
            group=[r for r in ownership['cases'] if r['version']==version and r['offset']==at]
            require(len(group)==4 and sum(r['unforced_current_snapshot'] for r in group)==1
                and {r['roll'] for r in group if not r['unforced_current_snapshot']}=={threshold-1,threshold,threshold+1},'three native threshold boundary classes per site required')
    ui=controls['C200_pairs'][0]['cases']
    require(len(ui)==2 and all(r['source_owned_UI_request_words']==[1,2,13,0,0,0,1] for r in ui)
        and ui[0]['source_owned_UI_writes']==ui[1]['source_owned_UI_writes'],'isolated C200 source ownership differs')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',730),('research',676)],'guarded end decodes required')
    require(names['progressive_nameplate_values']=={'86':'Square Shopkeeper','154':'Sailor'}
        and names['full_catalogue_values']=={'86':'Square Shopkeeper','154':'Retainer'},'distinct source names required')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
        ('progressive-nameplate',86):'Square Shopkeeper',('full-catalogue',86):'Square Shopkeeper',
        ('progressive-nameplate',154):'Sailor',('full-catalogue',154):'Retainer'}
        and all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in names['native_four_consumer_cases']['rows']),'four original name consumers required')
    voice=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voice['fresh2_actor_names']['rows']}=={86:0,154:4},'original Shopkeeper/Sailor voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['approved_prose_names']=={'86':'Square Shopkeeper','154':'Sailor'}
        and terms['full_catalogue_names']=={'86':'Square Shopkeeper','154':'Retainer'} and terms['city']=='Calicut'
        and [(r['source_text'],r['text']) for r in terms['two_source_current_city_aliases']]==[('カリカット','Calicut')]*2
        and terms['category_index']==14 and terms['source_category']=='染料' and terms['approved_full_category']==terms['compact_UI_category']=='Dyes'
        and [r['text'] for r in terms['current_category_binding']['rows']]==['Dyes']*6 and len(terms['all12_category14_native_bindings'])==12,'source category14 and two city aliases required')
    for flag in ['source_dyes_category14_not_single_named_pigment_garment_recipe_or_UI_rename', 'Sailor154_catalogue_Retainer_does_not_prove_player_employment_master_rank_or_kinship', 'familiar_oyajisan_does_not_prove_fatherhood_age_or_employment_relation', 'exclusive_color_competitor_buyout_popularity_imminent_sellout_and_conditional_profit_are_source_explicit_character_claims', 'no_narrator_verified_shortage_stock_price_rise_guaranteed_profit_or_earned_game_mechanic', 'admired_color_hesitation_urgency_doubt_reluctant_delegation_and_final_repeated_doubt_insistence_progression_preserved', 'two_identical_soukanaa_doubts_and_distinct_soudesu_soudesutte_replies_preserved', 'delegation_and_sulking_request_not_completed_purchase_delivery_recovery_or_new_relationship', 'no_named_pigment_ingredient_recipe_garment_quantity_price_or_new_source_town_invented', 'tentative_Dyes_Calicut_FE_distinct_from_character_pitch_prior_location_and_earned_state', 'source_three_predicates16_branches_four_effects_and_no_effect_paths_not_flattened', 'all13_clean_first_glosses_precede_predecessor_English', 'no_predecessor_English_exposed', 'no_new_name_category_city_widget_fidelity_credit']:require(terms.get(flag) is True,'whole-exchange source context required:'+flag)
    require(doc['exact_source_prose_R64_after_be_boundary_reviewed'] and not doc['no_record_specific_ordinary_boundary_exception_required'],'exact R64 boundary approval required')
    wrap=load(doc['source_bound_wrap_refinement_proof'])
    require(wrap['only_changed_record_IDs']==['DK4_MES_B191_R0064'] and wrap['all13_words_controls_and_prose_unchanged']
        and wrap['twelve_other_compiled_targets_exact'] and wrap['twelve_other_native_planes_exact']
        and len(wrap['exact_source_and_prose_mutation_controls'])==6
        and all(r.get('rejected') or r.get('exact_reviewed_boundary_not_inherited') for r in wrap['exact_source_and_prose_mutation_controls']),'exact source/prose wrap proof required')
    layout=load(doc['layout_retention_review_proof'])
    require(layout['all13_panels_on_two_native_sheets_viewed_after_image_return'] and {r['id'] for r in layout['retained_layouts']}=={
        'DK4_MES_B191_R0056','DK4_MES_B191_R0064','DK4_MES_B191_R0068','DK4_MES_B191_R0072','DK4_MES_B191_R0088'}
        and all(r['reason'] for r in layout['retained_layouts']),'individual native layout reasons required')
    carry=load(doc['carried_result_proof'])
    require(carry['original_interpreter_preserves_caller_second_result_word'] and len(carry['cases'])==15
        and {(r['version'],r['prior_result']) for r in carry['cases']}=={(v,p) for v in ['clean','current','relocated'] for p in [0,1,2,3,0xFFFFFFFF]}
        and all(r['C200']['native_result']==[3,r['prior_result'],0,0,0,0] and r['end_native_result']==[0,r['prior_result'],0,0,0,0]
            and r['all4MiB_owner_payload_and_guards_exact'] for r in carry['cases']),'original caller-owned result propagation required')
    require(sample['all13_panels_twelve_progressive_one_FE_original_no_effect_path_C200_end_and_parent_return_pass']
        and sample['source_all38_commands_16_branches_three_mixed_predicates_four_alternative_effects_and_no_effect_paths_preserved']
        and sample['actual_conditional_paths_verified_without_forcing_same_outcome']
        and sample['original_scene_two_unforced500_draws_skip700_and_no_A000_preserved']
        and sample['no_open_translation_specific_display_or_control_finding'] and not sample['offline_only_display_IDs'],'representative scope required')
    require(observed['all13_complete_held_planes_and_source_paired_regions_match']
        and observed['all13_speeches12_progressive1_impersonal_FE_actually_observed']
        and observed['nontext_equal_samples']==len(observed['all115_sampled_nontext_region_checks'])==115
        and not observed['nontext_difference_samples'] and observed['whole_RGB_final9001_equal'],'all actual panels/regions required')
    require(observed['exact_timing_difference_counts']==dict(total=12,speech=10,control_or_end=2)
        and len(observed['actual_timing_differences'])==12
        and observed['postscene9001_native_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True)
        and observed['postscene9001_whole1A04_actor_models_and_captain2_equal'],'measured state/timing limits required')
    require(observed['PRNG_equality'] is False and observed['postscene9001_PRNG_seeds']==[759362961,1803218166]
        and observed['future_world_equivalence_and_full_RAM_equality_not_claimed'],'measured unequal final RNG and limits required')
    require([(r['frame'],r['whole_frame_difference_bbox']) for r in observed['sampled_postscene_whole_RGB_differences_unmasked']]==[
        (6730,[225,371,239,376]),(6910,[225,371,239,376]),(7690,[224,360,240,376]),(7870,[224,360,240,376])]
        and observed['twelve_timing_four_indicator_and_unequal_final_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim']
        and observed['original_carried_result2_C200_3_2_and_end_0_2_preserved']
        and observed['both_actual_rolls875_988_at8_76_return2_skip700_at28_and_apply_no_source_A000']
        and observed['four_source_effect_alternatives_native_structural_only_not_actually_executed'],'all measured no-effect/timing/state scope required')
    require(len(observed['all_actual_consumer_sheets_viewed'])==3 and len(observed['paired_full_screen_views'])==5
        and all(s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002,'viewed current evidence required')
    actual=load(conf['actual_proof'])
    require(actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==13
        and not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs'],'all13 actual panels required')
    require(len(actual['versions'])==2 and [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[34,34]
        and [v['fixture_exit_frame'] for v in actual['versions']]==[5977,5975]
        and actual['observed_random_path_difference']['original_effects_by_case']==dict(clean_Japanese=[],reviewed_English=[]),'original no-effect paths required')
    for version in actual['versions']:
        require(len(version['selected_intervals'])==13 and version['single_source_end730_actually_reached']
            and version['selected_B22_command_pairs'][-1]['result_words']==[0,2]
            and version['selected_B22_command_pairs'][-1]['original_source_offset']==730
            and not version['source_A000'] and len(version['source_C200'])==1
            and version['source_C200'][0]['word']==0xC200 and version['source_C200'][0]['original_source_offset']==728
            and version['source_C200'][0]['result_words']==[3,2] and version['source_C200'][0]['UI_request_after']==[1,2,13,0,2,0,1],'actual no-effect/UI/end controls differ')
        require([(r['source_offset'],r['roll'],r['result'],r['threshold']) for r in version['actual_predicate_transitions']]==[(8,875,2,500),(76,988,2,500)]
            and all(r['actual_unforced_original_LCG_transition'] for r in version['actual_predicate_transitions']),'two original actual draws and skipped700 site required')
    require([{k:s[k] for k in ['path','sha256']} for s in approval['reviewed_sheets']]==native['review_sheets'],'native sheet approval binding differs')
    for sheet in approval['reviewed_sheets']:
        require(sheet['viewed_in_full_current_turn'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'native sheet view differs')
    for sheet in sample['viewed_actual_sheets']:
        require(sheet['viewed_after_image_return'] and sheet['review'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'actual sheet view differs')
    rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==13 and {r['source_selector'] for r in rows}==SELECTORS,'thirteen exact records required')
    require(Counter(r['kind'] for r in rows)=={'progressive':12,'system-FE':1}
        and Counter(r['editorial_decision'] for r in rows)=={'revise':5,'retain-wording':8},'consumer/decision scope differs')
    require(sample['actual_sampled_display_IDs']==sample['represented_reviewed_display_IDs']==ids
        and all([r['id'] for r in v['selected_intervals']]==ids for v in actual['versions']),'actual display keys differ')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==191,'one exact block required')
    spec=mapping['blocks'][0];old_blocks=list(IlnkContainer.parse(source).blocks)
    block,original=old_blocks[191],IlnkContainer.parse(japanese).blocks[191]
    require(len(old_blocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
    require(spec['source_bytes']==len(block)==736 and spec['source_logical_end']==734
        and spec['research_bytes']==680 and spec['research_logical_end']==680,'source/target extent metadata differs')
    require([{k:r[k] for k in ['word','old_offset','new_offset']}|{'old_extent':r['old_native_extent'],'new_extent':r['new_native_extent']} for r in spec['mapped_native_commands']]==spec['command_map'],'both complete command maps must agree')
    fonts={c['id']:c for c in native['cases']};refs={r['id']:r for r in spec['text_records']}
    require(set(fonts)==set(refs)==set(ids),'native/reference coverage differs')
    require({c['id'] for c in controls['relocated_dispatch_cases']}==set(ids)
        and all(c['resolved_actor_ID']==(None if c['source_selector']==254 else c['source_selector']) and c['registered_catalog_match'] is None
            for c in controls['relocated_dispatch_cases']),'individual dispatch scope differs')
    patches=[];changes=[];macros=Counter()
    for row in rows:
        ident=row['id'];case,ref=fonts[ident],refs[ident];fe=row['kind']=='system-FE'
        require(row['actual_B22_display_fixture_observed'] and not row['offline_only_native_display_checked']
            and not row['current_native_UI_body_explicit_unexecuted_boundary'],'individual actual scope differs')
        require(case['complete_native_independent228x48_plane_equal' if fe else 'complete_native_independent216x64_plane_equal']
            and case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and case['all_visible_origins_zero_and_within_four_rows']
            and case['one_native_page_consumes_complete_target'] and sum(len(p['cases']) for p in case['current_native_macro_pipelines'])==8,'complete native plane differs:'+ident)
        if fe:require(all(c['null_source_actor'] for p in case['current_native_macro_pipelines'] for c in p['cases']),'FE null actor differs')
        at,sa=row['current_reference']['offset'],row['source_reference']['offset'];old,raw=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex'])
        require(row['source_reference']['header_offset']==sa-5 and row['current_reference']['header_offset']==at-5
            and row['source_reference']['bytes']==len(raw) and row['current_reference']['bytes']==len(old),'complete source/current reference metadata differs:'+ident)
        require(row['source_reference']['block']==191 and row['source_reference']['record_index']==row['source_record_index']==original[:sa].count(b'\0')
            and row['current_record_index']==block[:at].count(b'\0'),'complete source/current record identity differs:'+ident)
        require(row['block']==191 and row['file_path']==PATH and row['source_selector']==raw[0]==old[0]
            and row['english'].startswith('{SPEAKER:'+format(raw[0],'02X')+'}') and (raw[0]==254)==fe,'source selector differs:'+ident)
        require(block[at:at+len(old)]==old and original[sa:sa+len(raw)]==raw and block[at+len(old)]==original[sa+len(raw)]==0
            and row['current_text_hex']==old.hex(),'source/current text differs:'+ident)
        require(block[at-5:at+1]==original[sa-5:sa+1]==b'\0\x40\xff\xff\0'+raw[:1]
            and row['source_complete_preamble_hex']==block[at-5:at+1].hex(),'complete preamble differs:'+ident)
        require(block[:at].count(b'\0')==row['record_index']==ref['record_index'] and ref['old_offset']==at and ref['old_length']==len(old)
            and row['native_display_consumer']==('original_null_actor_FE_24310_then5473C' if fe else 'original_progressive_54020'),'current reference differs:'+ident)
        sm=re.findall(rb'FI|FA|FO',raw[1:]);tm=[m.encode('ascii') for m in re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])]
        require(sm==tm,'source substitution/order differs:'+ident);macros.update(sm)
        profile=profile_for(arm,block,'FE-paper' if fe else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'],'compiled English differs:'+ident)
        qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning'
            and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved QA:'+ident)
        if row['source_record_index']==64:
            require(len(qa.get('reviewed_ordinary_boundaries',[]))==1 and row.get('reviewed_ordinary_boundaries')==qa['reviewed_ordinary_boundaries']
                and qa['reviewed_ordinary_boundaries'][0]['after_word']=='be'
                and qa['visible_lines']==["What are you waiting for? It'll be","too late once it's sold out."],'exact source/prose R64 soft wrap reason required')
        else:require(not row.get('reviewed_ordinary_boundaries') and not qa.get('reviewed_ordinary_boundaries'),'unreviewed ordinary boundary on another record')
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added'],'stored target differs:'+ident)
        if row['editorial_decision']=='retain-wording':require(row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification'],'unjustified retention')
        patches.append(dict(start=at,end=at+len(old),value=value,old=old))
        changes.append(dict(id=ident,block=191,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(not macros, 'complete macro scope differs')
    require(not spec['choice_commands'] and not spec['actor_style_commands'] and not spec['original2000_pause_and_resume_maps'], 'invented typed object or pause')
    patches.sort(key=lambda patch: patch['start'])
    require(all(a['end'] <= b['start'] for a, b in zip(patches, patches[1:])), 'overlapping objects')
    def mapped(offset):
        delta = 0
        for patch in patches:
            if offset < patch['start']:
                break
            require(not patch['start'] < offset < patch['end'], 'interior reference into complete text')
            if offset == patch['start']:
                return offset + delta
            delta += len(patch['value']) - (patch['end'] - patch['start'])
        return offset + delta
    end = 8 + struct.unpack_from('<H', block, 4)[0]
    require(end == 734 and len(block)==736 and block[end:]==bytes(2), 'nonzero source padding')
    pieces, last = [], 0
    for patch in patches:
        pieces.extend([block[last:patch['start']], patch['value']])
        last = patch['end']
    pieces.append(block[last:end])
    logical = bytearray(b''.join(pieces))
    edges = spec['relative_skip_fixups']
    require(len(edges)==16 and [e['offset'] for e in edges]==[16,20,24,36,40,44,56,68,72,84,88,92,104,116,120,124]
        and len(spec['target_native_skip_cases'])==80 and len(logical)==mapped(end)==680<0x2400,'complete relative scope required')
    for edge in edges:
        cases=[c for c in spec['target_native_skip_cases'] if c['new_offset']==edge['new_offset']]
        require(len(cases)==5 and {c['last_result'] for c in cases}=={0,1,2,3,0xFFFFFFFF},'five original results per relative site required')
        for case in cases:
            last=case['last_result'];taken=edge['word']==0x100 or (edge['word']==0x200 and last==0) or (edge['word']==0x300 and last==1) or (edge['word']==0x400 and last==2)
            destination=edge['new_matched_skip_target'] if taken else edge['new_unmatched_next']
            require(edge['new_offset']+case['native_extent']==destination and case['source_target_preserved_at_mapped_native_boundary']
                and case['ABI_all4MiB_owner_stream_result_length_and_guards_exact'],'source-bound relative operand case differs')
    for edge in edges:
        at, target = mapped(edge['offset']), mapped(edge['matched_skip_target'])
        span = target - at - 4
        require(at == edge['new_offset'] and target == edge['new_matched_skip_target'] and span == edge['target_span']
                and struct.unpack_from('<H', block, edge['span_field_offset'])[0] == edge['source_span']
                and 0 <= span <= 65535 and span % 2 == 0, 'relative target differs')
        struct.pack_into('<H', logical, at + 2, span)
    struct.pack_into('<H', logical, 4, len(logical) - 8)
    target = bytes(logical) + bytes(-len(logical) % 4)
    require(len(target)==680 and target[680:]==bytes() and target[6:128]==block[6:128] and sha(target) == spec['target_block_sha256'], 'target block differs')
    for change in changes:
        ref=refs[change['id']];at=mapped(change['old_offset'])
        require(at==change['new_offset']==ref['new_offset'] and target[:at].count(b'\0')==ref['new_record_index'],'relocated record offset/index differs:'+change['id'])
    commands = spec['mapped_native_commands']
    require(len(commands) == 38 and sum(command['word'] == 0x4000 for command in commands) == 13, 'native command scope differs')
    boundaries = {command['new_offset'] for command in commands}
    require(all(edge['new_matched_skip_target'] in boundaries and edge['new_unmatched_next'] in boundaries for edge in edges), 'relative destination leaves commands')
    for command in commands:
        a, b = command['old_offset'], command['new_offset']
        require(command['word'] == struct.unpack_from('<H', block, a)[0] == struct.unpack_from('<H', target, b)[0], 'mapped opcode differs')
        require(mapped(a) == b and mapped(a + command['old_native_extent']) - b == command['new_native_extent'], 'mapped boundary differs')
        if command['word'] == 0x4000:
            require(block[a:a + 6] == target[b:b + 6], 'speech preamble differs')
        elif command['word'] in [0x100, 0x200, 0x300, 0x400]:
            require(block[a:a + 2] == target[b:b + 2], 'relative opcode differs')
        else:
            require(block[a:a + command['old_native_extent']] == target[b:b + command['new_native_extent']], 'opaque numeric leaf differs')
    stops=[c for c in commands if c['word']==0]
    require([c['old_offset'] for c in stops]==[730] and len(stops)==1 and stops[0]['new_offset']==676
        and stops[0]['new_offset']+4==len(logical) and target[676:680]==bytes(4),'single source end differs')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]
        ==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[c for c in commands if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]]
    exact=[(8,'0080fffff4010000'),(28,'0080ffffbc020000'),(48,'00a0ffff01512aa1'),(60,'00a0ffff01522aa1'),
        (76,'0080fffff4010000'),(96,'00a0ffff01542aa1'),(108,'00a0ffff01552aa1'),(728,'00c2'),(730,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'nine complete source leaves differ')
    require([c['word'] for c in leaves]==[0x8000,0x8000,0xA000,0xA000,0x8000,0xA000,0xA000,0xC200,0]
        and all(c['word'] not in [0x2000,0x2100,0x4100] for c in commands),'source predicate/effect/C200 scope differs')
    restored = bytearray(logical)
    struct.pack_into('<H', restored, 4, end - 8)
    for edge in edges:
        struct.pack_into('<H', restored, edge['new_offset'] + 2, edge['source_span'])
    for patch in reversed(patches):
        at = mapped(patch['start'])
        restored[at:at + len(patch['value'])] = patch['old']
    require(bytes(restored) == block[:end] and bytes(restored)+block[end:]==block, 'inverse does not restore every predecessor byte')
    new_blocks = list(old_blocks)
    new_blocks[191] = target
    result = IlnkContainer(new_blocks).to_bytes()
    require(sha(result) == conf['target_SC2_sha256']
            and [index for index, (a, b) in enumerate(zip(old_blocks, new_blocks, strict=True)) if a != b] == [191], 'whole SC2 target differs')
    image.replace_file(PATH, result)
    return dict(source_SC2_sha256=sha(source), target_SC2_sha256=sha(result), required_runtime_ARM9_sha256=sha(arm),
        manuscript=conf['manuscript'], reference_map=conf['reference_map'], changed_records=changes,
        blocks=[dict(block=191, source_sha256=sha(block), target_sha256=sha(target), source_bytes=len(block), target_bytes=len(target),
                     relative_operands=16, source_commands=38, inverse_restores_every_original_logical_byte=True)],
        all335_other_SC2_blocks_unchanged=True, all13_progressive_FE_speeches_three_mixed_predicates_four_A000_C200_16_relative_sites9_leaves_and_no_effect_paths_preserved=True,
        actual_two_retained_B22_fixtures_and_postscene_exported_state_not_natural_source_activation=True,
        native_code_and123040_staged_payload_unchanged=True)
