"""Bind reviewed B234 scope, including distinct physical and deployed regional-name offsets."""
from collections import Counter
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL

def audit_sealed_scope(doc,mapping,seal,load,require):
    def yes(value,keys,label):require(all(value[k] is True for k in keys),label)
    for k,n in dict(actual_objects=18,actual_pages=18,actual_complete_body_holds=71,actual_complete_name_holds=71,offline_only_objects=0).items():require(doc[k]==n,'manuscript coverage:'+k)
    require(doc['offline_only_object_IDs']==[] and not doc['full_goal_complete'],'remaining goal')
    yes(doc,['full207_name_role_alias_andearlier_review_open','no_surname_nationality_occupation_kinship_or_rank_inferred','familiar_banter_unspecified_recovery_ship_companionship_greatgrandfather_papal_trade_donations_reported_blessing_andconditional_discovery_preserved','exact_source_item106_unchanged_no_title_card_mechanic_orother_consumer_approval','complete_R5_original_three_CP932_ellipsis_glyphs_retained','no_modern_date_new_rank_relationship_gender_biography_orconfirmed_item_outcome_invented'],'whole-exchange fidelity andscope')
    for r in doc['records']:
        require(r['speaker']=={19:'Carlo Sinat',104:'Trader'}[r['source_selector']],'source identity')
        require(all(isinstance(r[k],str) and r[k].strip() for k in ['context','source_meaning','localization_note','editorial_finding']),'individual contextual reasoning')
        require(r['no_manual_line_break_padding_or_alignment_authored'] and r['original_physical_native_rows_per_page']==r['native_profile_maximum_total_rows']==4 and r['native_page_count']==1,'authored prose andnative geometry')
    approval=load(doc['native_approval'])
    for k,n in dict(revision_count=14,retention_count=4,native_pages=18,logical_compiled_alignments=144,stored_alignments=72,zero_ink_parity_tails=7,name_alignments=20,layout_rejections=83,actual_objects=18,complete_body_holds=71,complete_name_holds=71,offline_only_objects=0).items():require(approval[k]==n,'native approval:'+k)
    f,s,q=[load(doc[k]) for k in ['native_font_proof','native_stored_proof','native_policy_validation']]
    require(f['complete_native_pages']==18 and f['logical_compiled_input_alignment_cases']==144,'native page counts')
    yes(f,['all18_single_original_four_row_pages','all18_complete_prose_paragraphs','all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds','each216x64_plane_exact_independent_current_font_and_all_canaries','all_original_current_font_renderer_instructions_verified','original_pair_phase_and_guards_bound_without_new_substitutions','zero_source_and_compiled_FI_FA_FO_no_substitutions_added','only_original_static_selectors19_104'],'complete font proof')
    require((s['stored_alignment_cases'],s['fresh_alignment_cases'],s['exact_reused_alignment_cases'],s['zero_ink_parity_tail_count'],s['complete_native_pages'])==(72,28,44,7,18) and s['all_final_stored_targets_equal_reviewed_complete_native_ink'] and s['all_bounds_canaries_pair_phase_and_zero_macros_pass'],'stored proof')
    require(q['positive_paragraph_count']==18 and q['negative_count']==len(q['negative_cases'])==83 and all(c['rejected'] for c in q['negative_cases']) and len(q['row_count_reasons'])==8 and q['all_base_QA_diagnostics_preserved_one_exact_R33_line1_article_classification'],'policy obligations')
    warning=dict(severity='warning',code='weak-line-ending',message="line 1 ends with weak wrap word 'the'")
    require(sum(bool(r['row_count_reason']) for r in doc['records'])==8,'eight row reasons')
    for r in doc['records']:
        expected=[warning] if r['source_record_index']==33 else []
        require(r['exact_reviewed_base_warnings']==expected and r['qa_waivers']==(['weak-line-ending'] if expected else []) and bool(r['qa_waiver_reason'])==bool(expected),'only exact R33 warning')
    names=load(doc['speaker_name_review'])
    yes(names,['both_actual_final_English_personal_androle_headers_complete','two_contextual_progressive_names_retained_no_assets_or_duplicate_credit','both_null_middle_fields_andsame_text_full_getters_preserved','no_surname_nationality_occupation_kinship_or_rank_inferred','regional_literal_excluded_from_both_returned_names_not_surname_or_nationality','full_catalogue_UI_unvisited','full207_name_role_alias_andearlier_name_review_open','source_item106_no_asset_card_mechanic_orother_consumer_approval','progressive_header_display_only_not_full_catalogue_UI_approval','no_new_name_or_dialogue_credit'],'name consumers andscope')
    alias=names['spoken_alias'];require((alias['Japanese'],alias['English'],alias['source_record_indices'])==('フィリポ','Filippo',[9,16]) and alias['other_route_English_bodies_unread'],'spoken alias scope')
    source=NdsImage.open(doc['source_ROM']).read_file('/__arm9__.bin');current=NdsImage.open(doc['current_ROM']).read_file('/__arm9__.bin')
    require(sha(source)=='0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731' and sha(current)==doc['current_ARM9_sha256']=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a','source/current runtime')
    payload=bytes(MainCodeFile(current,BASE).sections[3].data[:-48]);require(len(payload)==123264 and current.find(payload)==1517964,'deployed payload andphysical base')
    item=load(doc['source_named_item_binding']);region=item['actor104_regional_secondary_storage_contract']
    require((region['actor_ID'],region['column'],region['pointer_field'],region['source_storage_offset'],region['source_Japanese'],region['current_pointer'],region['current_literal'],region['current_terminated_hex'],region['deployed_pool_base'],region['current_deployed_payload_offset'],region['current_physical_ARM9_storage_offset'])==(104,4,1185924,1429952,'ヨーロッパ',37256672,'European','4575726f7065616e00',37255712,960,1518924),'independent regional storage binding')
    yes(region,['current_consumer_reported_storage_offset_is_absolute_ARM9','original_consumer_record_preserved','both_returned_name_strings_exclude_regional_literal','no_global_unused_field_or_nationality_or_surname_claim'],'regional offset andidentity scope')
    def fields(row):
        p=row['pointer_field']
        if row.get('source_null'):
            require(row['current_null'] and source[p:p+4]==current[p:p+4]==bytes(4),'null middle');return
        require(int.from_bytes(source[p:p+4],'little')==row['source_pointer'] and int.from_bytes(current[p:p+4],'little')==row['current_pointer'],'name/item pointers')
        for arm,which in [(source,'source'),(current,'current')]:
            at=row[which+'_storage_offset'];raw=bytes.fromhex(row[which+'_terminated_hex']);require(raw[-1]==0 and 0 not in raw[:-1],'independent terminator')
            if which=='current' and row['current_storage_kind']=='verified-current-staged-payload':
                require(p==1185924 and at==region['current_physical_ARM9_storage_offset']==1518924 and raw==b'European\0','sole source-bound regional absolute storage')
                relative=region['current_deployed_payload_offset']
                require(row['current_pointer']==POOL+relative==37256672 and at==1517964+relative and payload[relative:relative+len(raw)]==arm[at:at+len(raw)]==raw,'regional physical bytes anddeployed relative bytes independently exact')
            else:require(row[which+'_pointer']==BASE+at and arm[at:at+len(raw)]==raw,'static name/item bytes')
    require(len(names['records'])==2,'two name/role records')
    for n in names['records']:
        actor=n['actor_ID'];require(n['english']=={19:'Carlo Sinat',104:'Trader'}[actor] and [r['Japanese'] for r in n['source_fields'] if r.get('Japanese')]=={19:['カルロ','シナート'],104:['交易所の親父','ヨーロッパ']}[actor],'exact source identity fields')
        require(n['catalogue_current']==n['english'] and n['catalogue_wording_editorially_approved'] and n['actual_final_English_header_observed'] and n['full_catalogue_UI_unvisited'] and n['no_name_asset_or_duplicate_credit'] and n['source_fields'][2]['source_null'] and n['source_fields'][2]['current_null'],'same getter wording;catalogue UI unvisited')
        for r in n['source_fields']:fields(r)
    getters=load(doc['current_consumer_proof'])['native_four_distinct_name_consumers']['rows']
    require({(r['actor_ID'],r['consumer']):r['text'] for r in getters}=={(19,'progressive-nameplate'):'Carlo Sinat',(19,'full-catalogue'):'Carlo Sinat',(104,'progressive-nameplate'):'Trader',(104,'full-catalogue'):'Trader'},'four exact original getters')
    yes(item,['legacy_Filippo_spelling_is_consistency_lead_not_other_route_fresh_approval','actor104_source_oyaji_role_not_Carlo_father_or_automatic_personal_name','regional_European_literal_not_part_of_either_returned_name_no_nationality_surname_orbiography_inferred','reported_papal_association_blessing_andconditional_find_not_confirmed_mechanic','no_specific_pope_Gregory_biography_ordinal_or_item_title_invented_in_dialogue','no_item_or_actor_asset_change_or_duplicate_credit','no_inventory_card_orcomplete_item_mechanic_orother_consumer_approval','full207_name_role_alias_andearlier_consumer_review_remains_open'],'item/alias reported scope')
    require(item['source_dialogue_alias_Japanese']=='フィリポ','clean alias')
    r=item['source_named_item'];require((r['record_ID'],r['Japanese'],r['English'],r['source_terminated_hex'],r['current_terminated_hex'])==('DK4_ITEM_POINTER_106','グレゴリウスの冠',"Gregory's Crown",'834f838c8353838a8345835882cc8aa500','477265676f727927732043726f776e00'),'exact item106')
    require((r['pointer_field'],r['source_storage_offset'],r['current_storage_kind'],r['current_storage_offset'])==(1174528,1434712,'static-current-ARM9',1435852) and r['current_native_item_getter_card_bounds_mechanics_and_all_other_consumers_not_reviewed_here'],'item106 static storage andbroader consumer limit');fields(r)
    np=load(doc['native_name_proof'])
    require((np['name_literal_alignment_count'],np['fresh_native_name_font_alignment_cases'],np['exact_reused_native_name_font_alignment_cases'],np['complete_name_component_plane_count'])==(20,8,12,5) and len(np['name_planes'])==5 and sum(len(r['native_alignment']['cases']) for r in np['name_planes'])==20 and {r['text'] for r in np['name_planes']}=={'Carlo Sinat','Trader','Carlo','Sinat','European'},'five planes20 alignments8 fresh12 reused')
    yes(np,['source_personal_Carlo_andshared_Trader_role_match_both_original_getters','regional_European_literal_render_is_technical_only_not_returned_name_or_nationality','all_first_internal_final_name_glyphs_and_zero_ink_flushes_complete','no_name_asset_or_duplicate_credit'],'name-font exact scope')
    entry=load(doc['source_entry_proof'])
    require(sha(Path(doc['source_entry_proof']).read_bytes())==doc['source_entry_proof_sha256'] and entry['original_source_EV2_and_action_table_exact'] and [(r['event_ID'],r['script_block'],r['action_index'],r['must_be_completed'],r['must_not_be_completed']) for r in entry['selected_B234_source_events']]==[(234,234,235,[],[])],'source234 no explicit prerequisites orexclusions;not natural activation')
    a,l=load(doc['actual_English_proof']),load(doc['later_scope_proof']);o=mapping['observed_comparison_contract']
    measured=dict(source_exit=a['source_exit_frame'],English_exit=a['exit_frame'],normal_port=a['normal_port_sample_frame'],body_holds=a['actual_complete_body_holds'],name_holds=a['actual_complete_name_holds'],command_difference_rows=len(a['command_comparison_differences']),duration_changes=len(a['command_duration_changes']),later_samples=len(a['later_sampled_whole_frame_comparisons']),later_RGB_differences=len(l['later_sampled_RGB_differences']),component_equality=l['five_native_component_equality'],captains=l['captain_IDs'],PRNG_seeds=l['final_PRNG_seeds'],following_B120_ends=[r['B120_end_frames'] for r in l['following_B120']])
    require(measured==o==seal['observed_comparison_contract'],'actual comparison agreement')
    require(o==dict(source_exit=7174,English_exit=7173,normal_port=7270,body_holds=71,name_holds=71,command_difference_rows=18,duration_changes=8,later_samples=147,later_RGB_differences=0,component_equality=dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True),captains=[2,2],PRNG_seeds=[1202927797,1202927797],following_B120_ends=[[11976],[11976]]),'approved measured comparison')
    require(Counter(k for r in a['command_comparison_differences'] for k in r['different_fields'])==dict(returned=18,start=17,before_RNG=6,after_RNG=6),'all command fields')
    require([(r['source_offset'],r['source_duration'],r['English_duration']) for r in a['command_duration_changes']]==[(68,237,240),(144,241,237),(436,237,241),(558,241,237),(826,237,241),(922,241,237),(1218,237,241),(1350,241,237)],'all eight measured durations')
    require(a['actual_native_pages']==len(a['actual_page_panels'])==18 and not a['incomplete_sampled_body_holds'] and len(a['semantic_upper_portrait_pairs'])==18 and not a['page_transitions'],'complete actual page set')
    yes(a,['all18_single_original_native_pages_verified','initialized_B22_not_natural_event234_original_location_earned_progress_full_effects_route_orhardware','no_roles_roster_funds_conditions_RNG_results_RAM_code_battery_or_savestate_forced','no_full_RAM_every_intermediate_frame_future_sequence_broad_simulation_orcausal_claim','full207_name_role_alias_andearlier_editorial_scope_open','source_Carlo_andshared_Trader_role_headers_preserved','all_following_resident_payloads_verified_against_actual_SC0_to_SC3_bank','full_catalogue_UI_unvisited','source_item106_card_getter_mechanics_other_consumers_unapproved','progressive_header_approval_only_no_name_asset_change','ASCII_dark_gray_andexact_R5_CP932_light_gray_complete_masks_andall_name_masks_verified'],'actual coverage andpalette scope')
    plan=load(next(p for p in a['evidence'] if Path(p).name=='run_plan.json'));fixture=load(a['fixture'])
    require(plan['source_event234_not_naturally_selected'] and plan['displayed_original_source_block']==234 and fixture['fixtures'][0]['source_block']==234 and fixture['initialized_Amsterdam_B22_not_natural_event234_location_or_earned_progress'],'actual B234 entry scope')
    for p in a['actual_page_panels']:require(p['complete_body_holds'] and all(h['complete_independent_native_body_black_gray_all_glyphs_equal'] for h in p['complete_body_holds']),'every page complete')
    for p in a['actual_panels']:require(p['native_pages']==1 and {h['native_page'] for h in p['complete_body_holds']}=={1} and {h['native_page'] for h in p['complete_name_holds']}=={1},'every body andname page held')
    pal=load(doc['source_ellipsis_palette_proof']);silence=next(r for r in doc['records'] if r['source_record_index']==5);panel=next(r for r in a['actual_panels'] if r['id']==silence['id'])
    require(silence['source_hex']==silence['compiled_hex']=='68816381638163' and silence['english']=='{SPEAKER:68}………' and silence['editorial_decision']=='retain-wording','exact meaningful source silence')
    require(pal['source_body_hex']=='816381638163' and pal['black_pixels']==pal['shadow_pixels']==18 and pal['retained_CP932_shadow_RGB']==[197,198,197] and pal['English_ASCII_shadow_RGB']==[98,97,98] and len(pal['source_actual_cases'])==len(panel['complete_body_holds'])==3 and panel['body_shadow_RGB']==[197,198,197] and all(h['body_shadow_RGB']==[197,198,197] for h in panel['complete_body_holds']),'sole CP932 light-gray source andEnglish holds')
    for p in a['actual_panels']:
        if p['id']!=silence['id']:require(p['body_shadow_RGB']==[98,97,98] and all(h['body_shadow_RGB']==[98,97,98] for h in p['complete_body_holds']),'other ASCII dark-gray holds')
    c=load(doc['relocated_control_proof'])
    yes(c,['all18_complete_preambles_voices_andzero_macro_bodies_bound','zero_original_orinvented_FI_FA_FO','normal_state0_retains_existing_value_word_in_all25_cases','original_normal_end1528_four_bytes_andtarget_zero_storage_tail_preserved','all20_commands_no_predicate_relative_typed_style_orpicture_assumptions','opaque_A000_effects_bridged_not_fully_explained'],'control boundary scope')
    require(c['source_A000']['source_command_hex']=='00a0ffff6a000110' and c['source_A000']['rows']==c['relocated_A000']['rows'] and c['source_A000']['opaque_effect_bridges']==c['relocated_A000']['opaque_effect_bridges'],'effect structural consumer')
