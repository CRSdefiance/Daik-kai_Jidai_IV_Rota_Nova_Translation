"""Prepare actual-changing B231 production challenges, including the exact scoped warning."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B231_challenge_tools_v7512')
if __name__=='__main__':
    assert not ROOT.exists();src=Path('scripts/challenge_lil_B230_atomic_v7464.py').read_text('utf8')
    a=src.index("    root('Samwell-catalogue-global-approval-invented'");b=src.index("    add('effect-consumer-native-rows-lost'",a);oldnames=src[a:b].rstrip()
    names="""    for k in ['both_null_middle_fields_andsame_text_full_getters_preserved','legacy_item99_title_ambiguity_unapproved','legacy_item99_Medicine_title_ambiguity_unapproved_andnot_changed','progressive_header_display_only_not_full_catalogue_UI_approval']:root('names-scope-'+k,paths['speaker_name_review'],k,False)
    for i in range(2):
        add('name-catalogue-changed-'+str(i),paths['speaker_name_review'],lambda v,i=i:v['records'][i].update(catalogue_current='Invented Name'))
        add('name-source-null-lost-'+str(i),paths['speaker_name_review'],lambda v,i=i:v['records'][i]['source_fields'][2].update(source_null=False))
        add('name-current-null-lost-'+str(i),paths['speaker_name_review'],lambda v,i=i:v['records'][i]['source_fields'][2].update(current_null=False))
    getters=Path(d['current_consumer_proof']);add('Carlo-full-getter-invented',getters,lambda v:v['native_four_distinct_name_consumers']['rows'][3].update(text='King Carlo'))
    item=Path(d['source_named_item_binding'])
    for k in ['source_physician_spelling_Herophilus_supported_by_exact_item_name_andlegacy_designation','no_new_physician_nationality_gender_biography_or_modern_history_fact_inferred','source_medical_book_not_drug_or_runtime_FI_substitution','legacy_Herophilus_Medicine_title_is_exact_current_asset_not_new_editorial_approval','broader_item99_title_consumer_review_lead_medical_book_vs_medicine_ambiguity','reported_sailor_fatigue_management_not_cure_orconfirmed_mechanic','no_item_or_actor_asset_change_or_duplicate_credit','no_inventory_card_orcomplete_item_mechanic_orother_consumer_approval','full207_name_role_alias_andearlier_consumer_review_remains_open']:root('item-scope-'+k,item,k,False)
    for k,x in [('record_ID','DK4_ITEM_POINTER_051'),('Japanese','アルマジロの皮'),('English','Armadillo Steel Hide'),('source_terminated_hex','834100'),('current_terminated_hex','41726d6f7200'),('pointer_field',0),('current_storage_offset',0),('source_storage_offset',0)]:add('item-field-'+k,item,lambda v,k=k,x=x:v['source_named_item'].update({k:x}))
    add('item-other-consumers-falsely-approved',item,lambda v:v['source_named_item'].update(current_native_item_getter_card_bounds_mechanics_and_all_other_consumers_not_reviewed_here=False))"""
    a=src.index("    entry=Path(d['source_entry_proof'])");b=src.index("    add('actual-command-comparison-erased'",a);oldscope=src[a:b].rstrip()
    scope="""    entry=Path(d['source_entry_proof']);namefont=Path(d['native_name_proof'])
    add('source231-prerequisite-invented',entry,lambda v:v['selected_B231_source_events'][0].update(must_be_completed=[230]))
    add('source231-exclusion-invented',entry,lambda v:v['selected_B231_source_events'][0].update(must_not_be_completed=[230]))
    add('source231-wrong-action',entry,lambda v:v['selected_B231_source_events'][0].update(action_index=229))
    root('entry-source-identity-lost',entry,'original_source_EV2_and_action_table_exact',False)
    root('entry-hash-changed',doc,'source_entry_proof_sha256','0'*64)
    root('name-font-count-lost',namefont,'name_literal_alignment_count',0)
    root('name-font-plane-count-lost',namefont,'complete_name_component_plane_count',7)
    for k in ['source_personal_fields_Lil_Argot_Carlo_Sinat_match_both_original_getters','no_surname_nationality_occupation_or_scene_location_inferred_from_secondary_field','all_first_internal_final_name_glyphs_and_zero_ink_flushes_complete','no_name_asset_or_duplicate_credit']:root('name-font-scope-'+k,namefont,k,False)
    add('name-font-missing-case',namefont,lambda v:v['name_planes'][0]['native_alignment']['cases'].pop())
    add('name-font-wrong-text',namefont,lambda v:v['name_planes'][0].update(text='King Carlo'))
    special=next(i for i,r in enumerate(d['records']) if r['source_record_index']==35)
    row('R35-warning-erased','exact_reviewed_base_warnings',[],special)
    row('R35-waiver-erased','qa_waivers',[],special)
    row('R35-reason-erased','qa_waiver_reason','',special)
    row('R35-different-row-approved','formatted_markup',d['records'][special]['formatted_markup'].replace('seen in the','seen in a'),special)
    row('R35-warning-changed','exact_reviewed_base_warnings',[dict(severity='warning',code='weak-line-ending',message='line 2 ends with weak wrap word in')],special)
    row('R35-blanket-waiver','qa_waivers',['weak-line-ending','encoding'],special)"""
    changes={oldnames:names,oldscope:scope,'B230':'B231','atomic_v7464':'atomic_v7512','atomic_v7463':'atomic_v7511',"('actual_objects',16),('actual_pages',16),('actual_complete_body_holds',66),('actual_complete_name_holds',66)":"('actual_objects',0),('actual_pages',0),('actual_complete_body_holds',0),('actual_complete_name_holds',0)",'source_middle_field_not_invented_surname_rank_or_nationality':'no_surname_nationality_occupation_kinship_or_rank_inferred','King Samwell':'King Carlo',"('false-revision','editorial_decision','revise',0)":"('false-revision','editorial_decision','revise',retain)","('lost-boundaries','reviewed_ordinary_boundaries',[],2)":"('lost-boundaries','reviewed_ordinary_boundaries',[],next(i for i,r in enumerate(d['records']) if r['reviewed_ordinary_boundaries']))",'target_offset=976':'target_offset=748','all17':'all16','selectors2_22':'selectors2_19',"'negative_count',75":"'negative_count',0",'all_base_QA_diagnostics_preserved_zero_warning_waivers':'all_base_QA_diagnostics_preserved_one_exact_R35_article_classification','event230':'event231','original_normal_end974_four_bytes_andtarget_two_byte_tail_preserved':'original_normal_end746_four_bytes_andtarget_two_byte_tail_preserved','all19_commands':'all18_commands',"row('wrong-source-voice','source_voice_class',7,0)":"row('wrong-source-voice','source_voice_class',0,0)",'item52-':'item99-','positive_records=17':'positive_records=16','all17_actual17_pages67_body67_headers_bound':'all16_actual16_pages63_body63_headers_bound'}
    row=derive('scripts/challenge_lil_B230_atomic_v7464.py','scripts/challenge_lil_B231_atomic_v7512.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_B231_semantic_challenges.json',dict(tool=row,all_cases_fresh_actual_changing_andmust_reject_before_mutation=True,dependency_digests_bypassed_approved_records_mirrored=True,no_schema_exceptions_count_as_rejections=True,sole_R35_warning_null_middles_fresh_names_item99_andall_measurements_challenged=True,new_credit=0,full_goal_complete=False))
