"""Prepare seventeen once-only credits with exact full-ledger historical inverse."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B190_completion_tools_v5351')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/complete_lil_B189_v5309.py');text=source.read_text(encoding='utf-8')
    a=text.index("        inventory=deepcopy(read(old['unfinished_editorial_scope_v5268'");b=text.index("        for unit in inventory['broader_coverage_units']:",a)
    inventory="""        inventory=deepcopy(read(old['unfinished_editorial_scope_v5309']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B190_completed_v5351']=dict(final_review=str(FINAL),completed_objects=17,registered_candidate=release['candidate'],natural_event190_not_selected=True)
        inventory['historical_Lil_B190_clean_only_before_v5351']=inventory.pop('next_Lil_B190_clean_only_v5313')
        inventory['next_Lil_B191_clean_only_v5355']=dict(path=str(NEXT_SOURCE),sha256=sha(NEXT_SOURCE.read_bytes()),objects=13,uncredited=True,
            conditional38_commands_three_predicates16_relatives_four_alternatives=True)
        inventory['B190_carried_result_and_stopped_audit_preserved']=dict(path=doc['carried_result_proof'],sha256=doc['carried_result_proof_sha256'],
            original_result2_C200_3_2_end_0_2_preserved=True,no_emulator_rerun=True)
"""
    row=derive(source,'scripts/complete_lil_B190_v5351.py',{
        text[a:b]:inventory,'B189':'B190','completion_v5309':'completion_v5351','lil_B189_completion_text_v5309':'lil_B190_completion_text_v5351',
        'editorial_handoff_verification_v5310':'editorial_handoff_verification_v5352','editorial_handoff_verification_v5269':'editorial_handoff_verification_v5310',
        'release_v5305':'release_v5347','startup_v5307':'startup_v5349','registration_v5303':'registration_v5345',
        'actual_v5298/actual_all17_progressive_FE_A000':'actual_v5340b/actual_all17_progressive_FE_RNG',
        'actual_review_v5299/all17_panels12_fullscreens_two_pair_return':'actual_review_v5341b/all17_panels_16_fullscreens_conditional_return',
        'lil_B190_clean_context_v5313/all17_clean_exchange':'lil_B191_clean_context_v5355/all13_clean_exchange',
        'Lil-B189-two-pair-ceramics-collection-ironic-sale-and-prospective-Hamburg17':'Lil-B190-reported-retail-cure-doubt-shopping-and-prospective-Havana17',
        'unfinished_editorial_scope_v5309':'unfinished_editorial_scope_v5351','Lil_B189_v5309':'Lil_B190_v5351',
        'all573_manifest_batches':'all574_manifest_batches','all_current_requested_and_final_framebuffers_equal_V5263':'all_current_requested_and_final_framebuffers_equal_V5304',
        "reg['negative_count']==74":"reg['negative_count']==88",'[6937,6937]':'[6934,6937]','dict(total=8,speech=8,control_or_end=0)':'dict(total=9,speech=7,control_or_end=2)',
        "not transitions['sampled_postscene_whole_RGB_differences_unmasked'] and transitions['all_sampled_postscene_whole_RGB_equal'] and transitions['eight_speech_timing_and_unequal_final_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim'] and transitions['four_original_speakers_and_two_pair_portrait_transition_observed']":
        "len(transitions['sampled_postscene_whole_RGB_differences_unmasked'])==2 and not transitions['all_sampled_postscene_whole_RGB_equal'] and transitions['nine_timing_and_two_original_indicator_shadow_differences_retained_without_masking_or_retiming'] and transitions['original_carried_result2_C200_3_2_and_end_0_2_preserved']",
        '[463267532,3723009301]':'[2467799992,2467799992]',"and not transitions['PRNG_equality']":"and transitions['PRNG_equality']",'regressions_v5304':'regressions_v5346',
        "len(manifest['batches'])==573":"len(manifest['batches'])==574",'retention_v5308':'retention_v5350','.blocks[189]':'.blocks[190]','block=189':'block=190','blocks=[189]':'blocks=[190]',
        'len(oldkeys)==6054':'len(oldkeys)==6071','==6054 and not fresh':'==6071 and not fresh',
        'natural_event189_not_selected':'natural_event190_not_selected','records_editorially_completed=6071':'records_editorially_completed=6088',
        'records_with_source_and_prose_pass=6074':'records_with_source_and_prose_pass=6091','records_with_source_prose_drafts=6074':'records_with_source_prose_drafts=6091',
        'records_revised_and_integrated=3839':'records_revised_and_integrated=3849','retained_wordings_editorially_completed=2232':'retained_wordings_editorially_completed=2239',
        "new[key]['/data/SC2.DK4']==4169;new[key]['/data/SC2.DK4']=4186":"new[key]['/data/SC2.DK4']==4186;new[key]['/data/SC2.DK4']=4203",
        '6071 contextual rereads integrated;source/prose6074':'6088 contextual rereads integrated;source/prose6091',
        'fresh_pass_records_explicitly_reread=6071':'fresh_pass_records_explicitly_reread=6088','fresh_pass_records_integrated=6071':'fresh_pass_records_integrated=6088',
        'actual_selected_source189_events':'actual_selected_source190_events','reviewed_route_records=4472':'reviewed_route_records=4489','completed_route_records=4472':'completed_route_records=4489',
        'actual_source_event189_selected':'actual_source_event190_selected','Lil_B189_previously_uncredited_objects_completed=17,Lil_B190_clean_only_uncredited_objects=17':'Lil_B190_previously_uncredited_objects_completed=17,Lil_B191_clean_only_uncredited_objects=13',
        '## V5309: Seventeen Lil B189 reviews integrated once in cumulative V5304':'## V5351: Seventeen Lil B190 reviews integrated once in cumulative V5346',
        '# Current editorial handoff - V5309':'# Current editorial handoff - V5351','(6071,6074,3839,2232)':'(6088,6091,3849,2239)',
        'len(allkeys)==6071':'len(allkeys)==6088','completed=6071,source_prose=6074,revised=3839,retained=2232':'completed=6088,source_prose=6091,revised=3849,retained=2239',
        'SC2=4186':'SC2=4203','reviewed_routes=4472':'reviewed_routes=4489','completed_routes=4472':'completed_routes=4489','match_V5263':'match_V5304','source189_natural':'source190_natural',
        'eight_speech_timing_and_unequal_final_PRNG_differences_preserved':'nine_timing_two_indicator_shadows_and_original_carried_result_preserved',
        'new_clean_only_Lil_B190_uncredited_objects=17':'new_clean_only_Lil_B191_uncredited_objects=13',
        'V5304 integration verified;6071 completed/6074 source-prose. Seventeen conditional B190 clean-only glosses pending':'V5346 integration verified;6088 completed/6091 source-prose. Thirteen conditional B191 clean-only glosses pending',
    })
    before,after=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert before-after==Counter({463267532:1,3723009301:1}) and after-before==Counter({2467799992:2})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_six_target_completion.json',dict(derivation=row,
        seventeen_disjoint_new_keys_and_all_previous_nested_values_required=True,six_target_stage_audit_apply_verify_required=True,
        native_constants_preserved_except_measured_PRNG_data=True,no_shared_mutation_yet=True,full_goal_complete=False))
