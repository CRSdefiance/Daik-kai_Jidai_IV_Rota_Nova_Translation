"""Prepare an invertible six-target completion after all current gates pass."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B187_completion_tools_v5224')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/complete_lil_B186_v5182.py');text=source.read_text(encoding='utf-8')
    a=text.index("        inventory=deepcopy(read(old['unfinished_editorial_scope_v5127'");b=text.index("        for unit in inventory['broader_coverage_units']:",a)
    inventory="""        inventory=deepcopy(read(old['unfinished_editorial_scope_v5182']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B187_completed_v5224']=dict(final_review=str(FINAL),completed_objects=16,registered_candidate=release['candidate'],natural_event187_not_selected=True)
        inventory['historical_Lil_B187_clean_only_before_v5224']=inventory.pop('next_Lil_B187_clean_only_v5187')
        inventory['next_Lil_B188_clean_only_v5231']=dict(path=str(NEXT_SOURCE),sha256=sha(NEXT_SOURCE.read_bytes()),objects=11,uncredited=True)
"""
    changes={
        text[a:b]:inventory,
        'from scripts.checkpoint_lil_B186_v5173 import WIDER\n':'',
        'B186':'B187','completion_v5182':'completion_v5224','editorial_handoff_verification_v5183':'editorial_handoff_verification_v5225',
        'lil_B186_completion_text_v5182':'lil_B187_completion_text_v5224',
        'editorial_handoff_verification_v5174':'editorial_handoff_verification_v5183','editorial_manuscript_v6':'editorial_manuscript_v4',
        'release_v5178':'release_v5220','startup_v5180':'startup_v5222','registration_v5176':'registration_v5218',
        'actual_v5169/actual_all12_progressive_FE_RNG_effect_C200':'actual_v5213/actual_all16_progressive_FE_A000_C200',
        'actual_review_v5170/all12_panels_20_fullscreens_conditional_return_and_measured_differences':
        'actual_review_v5214/all16_panels12_fullscreens_linear_return_and_measured_differences',
        'lil_B187_clean_context_v5187/all16_clean_exchange':'lil_B188_clean_context_v5231/all11_clean_exchange',
        'Lil-B186-Owner-Cook-sweet-emphasis-self-authority-and-prospective-Alexandria12':'Lil-B187-cough-unnamed-almond-remedy-reported-sales-and-prospective-Malacca16',
        'unfinished_editorial_scope_v5182':'unfinished_editorial_scope_v5224','Lil_B186_v5182':'Lil_B187_v5224',
        'all570_manifest_batches':'all571_manifest_batches','all_current_requested_and_final_framebuffers_equal_V5122':'all_current_requested_and_final_framebuffers_equal_V5177',
        "reg['negative_count']==84":"reg['negative_count']==68",
        "actual['complete_matching_observations']==12":"actual['complete_matching_observations']==16",
        "for r in actual['actual_panels'])==47":"for r in actual['actual_panels'])==63",
        '[5735,5737]':'[6694,6695]','dict(total=10,speech=4,control_or_end=6)':'dict(total=16,speech=14,control_or_end=2)',
        "len(transitions['sampled_postscene_whole_RGB_differences_unmasked'])==4 and transitions['ten_timing_and_four_original_indicator_differences_retained_without_masking_or_retiming']":
        "not transitions['sampled_postscene_whole_RGB_differences_unmasked'] and transitions['all_sampled_postscene_whole_RGB_equal'] and transitions['sixteen_timing_differences_retained_without_masking_retiming_or_future_equivalence_claim']",
        "[1803218166,2467799992] and not transitions['PRNG_equality']":"[2467799992,2467799992] and transitions['PRNG_equality']",
        'regressions_v5177b':'regressions_v5219',"len(manifest['batches'])==570":"len(manifest['batches'])==571",'retention_v5181':'retention_v5223',
        "len(source['records'])==16":"len(source['records'])==11",'[-12:]':'[-16:]',
        "{'revise':7,'retain-wording':5}":"{'revise':7,'retain-wording':9}",
        "(doc['source_prose_or_completion_credit_added']==0 and old['lil_B186_contextual_reference_v5173']['approved_uncredited_objects']==12 and old['lil_B186_contextual_reference_v5173']['source_prose_or_completion_credit_added']==0)":"doc['source_prose_or_completion_credit_added']==0",
        '.blocks[186]':'.blocks[187]','block=186':'block=187','blocks=[186]':'blocks=[187]',
        'len(oldkeys)==6015':'len(oldkeys)==6027','len(keys)==12':'len(keys)==16','==6015 and not fresh':'==6027 and not fresh',
        'retained=5':'retained=9','retained_count=5':'retained_count=9','fresh_retentions=5':'fresh_retentions=9','justified_retentions=5':'justified_retentions=9',
        'credit_added_once=12':'credit_added_once=16','all12_exact_clean':'all16_exact_clean','actual_unique_speeches=12':'actual_unique_speeches=16','actual_matching_holds=47':'actual_matching_holds=63',
        'natural_event186_not_selected':'natural_event187_not_selected','records_editorially_completed=6027':'records_editorially_completed=6043',
        'records_with_source_and_prose_pass=6030':'records_with_source_and_prose_pass=6046','records_with_source_prose_drafts=6030':'records_with_source_prose_drafts=6046',
        'records_revised_and_integrated=3818':'records_revised_and_integrated=3825','retained_wordings_editorially_completed=2209':'retained_wordings_editorially_completed=2218',
        "new[key]['/data/SC2.DK4']==4130;new[key]['/data/SC2.DK4']=4142":"new[key]['/data/SC2.DK4']==4142;new[key]['/data/SC2.DK4']=4158",
        '6027 contextual rereads integrated;source/prose6030':'6043 contextual rereads integrated;source/prose6046',
        'fresh_pass_records_explicitly_reread=6027':'fresh_pass_records_explicitly_reread=6043','fresh_pass_records_integrated=6027':'fresh_pass_records_integrated=6043',
        'records=12':'records=16','new_completed_records=12':'new_completed_records=16','new_source_prose_reviews=12':'new_source_prose_reviews=16',
        'actual_selected_source186_events':'actual_selected_source187_events','actual_B22_content_speeches=12':'actual_B22_content_speeches=16',
        'goal_turn_new_frames=21402':'goal_turn_new_frames=39404','goal_turn_new_emulator_runs=2':'goal_turn_new_emulator_runs=4',
        'reviewed_route_records=4428':'reviewed_route_records=4444','completed_route_records=4428':'completed_route_records=4444',
        'completion_credit_added=12':'completion_credit_added=16','actual_source_event186_selected':'actual_source_event187_selected',
        'all12-source-native-reference-actual-registered-release-pass':'all16-source-native-reference-actual-registered-release-pass',
        'exact_R13_two_ordinary_boundaries_reviewed_without_word_change=True':'no_record_specific_ordinary_boundary_exception_required=True',
        'Lil_B186_previously_uncredited_objects_completed=12,Lil_B187_clean_only_uncredited_objects=16':
        'Lil_B187_previously_uncredited_objects_completed=16,Lil_B188_clean_only_uncredited_objects=11',
        '## V5182: Twelve Lil B186 reviews integrated once in cumulative V5177':'## V5224: Sixteen Lil B187 reviews integrated once in cumulative V5219',
        '# Current editorial handoff - V5182':'# Current editorial handoff - V5224',
        '(6027,6030,3818,2209)':'(6043,6046,3825,2218)','exactly12_new':'exactly16_new',"len(read(FINAL)['records'])==12":"len(read(FINAL)['records'])==16",
        'len(allkeys)==6027':'len(allkeys)==6043','completed=6027,source_prose=6030,revised=3818,retained=2209':'completed=6043,source_prose=6046,revised=3825,retained=2218',
        'SC2=4142':'SC2=4158','reviewed_routes=4428':'reviewed_routes=4444','completed_routes=4428':'completed_routes=4444',
        'actual_unique_B186_speeches=12':'actual_unique_B187_speeches=16','match_V5122':'match_V5177','source186_natural':'source187_natural',
        'ten_timing_four_later_indicator_and_unequal_PRNG_differences_preserved':'sixteen_timing_differences_and_measured_equal_RGB_PRNG_scope_preserved',
        'new_clean_only_Lil_B187_uncredited_objects=16':'new_clean_only_Lil_B188_uncredited_objects=11',
        'V5177 integration verified;6027 completed/6030 source-prose. Sixteen B187 clean-only glosses pending':'V5219 integration verified;6043 completed/6046 source-prose. Eleven B188 clean-only glosses pending',
    }
    row=derive(source,'scripts/complete_lil_B187_v5224.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'prepared_six_target_completion.json',dict(derivation=row,
        sixteen_disjoint_new_keys_required=True,all_prior_root_and_nested_values_preserved_by_exact_inverse=True,
        six_target_stage_audit_apply_verify_required=True,no_shared_mutation_yet=True,full_goal_complete=False))
