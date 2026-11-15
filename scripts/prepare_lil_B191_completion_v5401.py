"""Prepare thirteen once-only reviews with a complete six-target historical inverse."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B191_completion_tools_v5401')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/complete_lil_B190_v5351c.py');text=source.read_text(encoding='utf-8')
    a=text.index("        inventory=deepcopy(read(old['unfinished_editorial_scope_v5309'");b=text.index("        for unit in inventory['broader_coverage_units']:",a)
    inventory="""        inventory=deepcopy(read(old['unfinished_editorial_scope_v5351']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B191_completed_v5401']=dict(final_review=str(FINAL),completed_objects=13,registered_candidate=release['candidate'],natural_event191_not_selected=True)
        inventory['historical_Lil_B191_clean_only_before_v5401']=inventory.pop('next_Lil_B191_clean_only_v5355')
        inventory['next_Lil_B192_clean_only_v5405']=dict(path=str(NEXT_SOURCE),sha256=sha(NEXT_SOURCE.read_bytes()),objects=8,uncredited=True,linear11_commands_no_predicates_or_relatives=True)
        inventory['B191_exact_R64_wrap_and_original_no_effect_path']=dict(path=doc['source_bound_wrap_refinement_proof'],sha256=doc['source_bound_wrap_refinement_proof_sha256'],
            only_R64_layout_changed_all13_words_and12_other_targets_preserved=True,actual_two500_draws_skip700_and_apply_no_A000=True,
            four_alternative_effects_offline_structural_only=True)
"""
    row=derive(source,'scripts/complete_lil_B191_v5401.py',{
        text[a:b]:inventory,'B190':'B191','completion_v5351':'completion_v5401','lil_B190_completion_text_v5351':'lil_B191_completion_text_v5401',
        'editorial_handoff_verification_v5352':'editorial_handoff_verification_v5402','editorial_handoff_verification_v5310':'editorial_handoff_verification_v5352',
        'editorial_manuscript_v4':'editorial_manuscript_v5','release_v5347':'release_v5397','startup_v5349':'startup_v5399','registration_v5345':'registration_v5395',
        'actual_v5340b/actual_all17_progressive_FE_RNG_effect':'actual_v5389/actual_all13_progressive_FE_RNG_effect_or_no_effect',
        'actual_review_v5341b/all17_panels_16_fullscreens_conditional_return':'actual_review_v5390/all13_panels_20_fullscreens_no_effect_path_return',
        'lil_B191_clean_context_v5355/all13_clean_exchange':'lil_B192_clean_context_v5405/all8_clean_exchange',
        'Lil-B190-reported-retail-cure-doubt-shopping-and-prospective-Havana17':'Lil-B191-dye-buyout-pitch-repeated-doubt-kinship-free-profit-and-prospective-Calicut13',
        'unfinished_editorial_scope_v5351':'unfinished_editorial_scope_v5401','Lil_B190_v5351':'Lil_B191_v5401',
        'all574_manifest_batches':'all575_manifest_batches','all_current_requested_and_final_framebuffers_equal_V5304':'all_current_requested_and_final_framebuffers_equal_V5346',
        "reg['negative_count']==88":"reg['negative_count']==99","actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==17":"actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==13",
        "for r in actual['actual_panels'])==67":"for r in actual['actual_panels'])==51",'[6934,6937]':'[5977,5975]','dict(total=9,speech=7,control_or_end=2)':'dict(total=12,speech=10,control_or_end=2)',
        "len(transitions['sampled_postscene_whole_RGB_differences_unmasked'])==2":"len(transitions['sampled_postscene_whole_RGB_differences_unmasked'])==4",
        'nine_timing_and_two_original_indicator_shadow_differences_retained_without_masking_or_retiming':'twelve_timing_four_indicator_and_unequal_final_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim',
        '[2467799992,2467799992]':'[759362961,1803218166]',"and transitions['PRNG_equality']":"and not transitions['PRNG_equality']",
        'regressions_v5346':'regressions_v5396',"len(manifest['batches'])==574":"len(manifest['batches'])==575",'retention_v5350':'retention_v5400','[-17:]':'[-13:]',
        "len(source['records'])==13":"len(source['records'])==8","{'revise':10,'retain-wording':7}":"{'revise':5,'retain-wording':8}",'.blocks[190]':'.blocks[191]','block=190':'block=191','blocks=[190]':'blocks=[191]',
        'len(oldkeys)==6071':'len(oldkeys)==6088','len(keys)==17':'len(keys)==13','==6071 and not fresh':'==6088 and not fresh',
        'revised=10':'revised=5','retained=7':'retained=8','revised_count=10':'revised_count=5','retained_count=7':'retained_count=8','fresh_revisions=10':'fresh_revisions=5','fresh_retentions=7':'fresh_retentions=8','new_revisions=10':'new_revisions=5','justified_retentions=7':'justified_retentions=8',
        'credit_added_once=17':'credit_added_once=13','all17_exact_clean':'all13_exact_clean','actual_unique_speeches=17':'actual_unique_speeches=13','actual_matching_holds=67':'actual_matching_holds=51',
        'natural_event190_not_selected':'natural_event191_not_selected','records_editorially_completed=6088':'records_editorially_completed=6101',
        'records_with_source_and_prose_pass=6091':'records_with_source_and_prose_pass=6104','records_with_source_prose_drafts=6091':'records_with_source_prose_drafts=6104','records_revised_and_integrated=3849':'records_revised_and_integrated=3854','retained_wordings_editorially_completed=2239':'retained_wordings_editorially_completed=2247',
        "new[key]['/data/SC2.DK4']==4186;new[key]['/data/SC2.DK4']=4203":"new[key]['/data/SC2.DK4']==4203;new[key]['/data/SC2.DK4']=4216",
        '6088 contextual rereads integrated;source/prose6091':'6101 contextual rereads integrated;source/prose6104','fresh_pass_records_explicitly_reread=6088':'fresh_pass_records_explicitly_reread=6101','fresh_pass_records_integrated=6088':'fresh_pass_records_integrated=6101',
        'records=17':'records=13','new_completed_records=17':'new_completed_records=13','new_source_prose_reviews=17':'new_source_prose_reviews=13',
        'actual_selected_source190_events':'actual_selected_source191_events','actual_B22_content_speeches=17':'actual_B22_content_speeches=13',
        'reviewed_route_records=4489':'reviewed_route_records=4502','completed_route_records=4489':'completed_route_records=4502',
        'completion_credit_added=17':'completion_credit_added=13','actual_source_event190_selected':'actual_source_event191_selected',
        'all17-source-native-reference-actual-registered-release-pass':'all13-source-native-reference-actual-registered-release-pass',
        'no_record_specific_ordinary_boundary_exception_required=True':'no_record_specific_ordinary_boundary_exception_required=False,exact_source_prose_R64_after_be_boundary_reviewed=True',
        'Lil_B190_previously_uncredited_objects_completed=17,Lil_B191_clean_only_uncredited_objects=13':'Lil_B191_previously_uncredited_objects_completed=13,Lil_B192_clean_only_uncredited_objects=8',
        '## V5351: Seventeen Lil B190 reviews integrated once in cumulative V5346':'## V5401: Thirteen Lil B191 reviews integrated once in cumulative V5396','# Current editorial handoff - V5351':'# Current editorial handoff - V5401',
        '(6088,6091,3849,2239)':'(6101,6104,3854,2247)','exactly17_new':'exactly13_new',"len(read(FINAL)['records'])==17":"len(read(FINAL)['records'])==13",'len(allkeys)==6088':'len(allkeys)==6101',
        'completed=6088,source_prose=6091,revised=3849,retained=2239':'completed=6101,source_prose=6104,revised=3854,retained=2247','SC2=4203':'SC2=4216','reviewed_routes=4489':'reviewed_routes=4502','completed_routes=4489':'completed_routes=4502',
        'actual_unique_B190_speeches=17':'actual_unique_B191_speeches=13','match_V5304':'match_V5346','source190_natural':'source191_natural',
        'nine_timing_two_indicator_shadows_and_original_carried_result_preserved':'twelve_timings_four_indicators_unequal_PRNG_and_original_no_effect_path_preserved',
        'new_clean_only_Lil_B191_uncredited_objects=13':'new_clean_only_Lil_B192_uncredited_objects=8',
        'V5346 integration verified;6088 completed/6091 source-prose. Thirteen conditional B191 clean-only glosses pending':'V5396 integration verified;6101 completed/6104 source-prose. Eight linear B192 clean-only glosses pending',
        'Credit seventeen newly integrated reviews once':'Credit thirteen newly integrated reviews once','Six targets staged;seventeen reviews counted once':'Six targets staged;thirteen reviews counted once','Six targets,all historical values and seventeen disjoint new keys audited.':'Six targets,all historical values and thirteen disjoint new keys audited.',
    })
    before,after=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert before-after==Counter({2467799992:2}) and after-before==Counter({759362961:1,1803218166:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_six_target_completion.json',dict(derivation=row,
        thirteen_disjoint_new_keys_and_all_previous_nested_values_required=True,six_target_stage_audit_apply_verify_required=True,
        exact_R64_wrap_and_actual_no_effect_scope_preserved=True,no_shared_mutation_yet=True,full_goal_complete=False))
