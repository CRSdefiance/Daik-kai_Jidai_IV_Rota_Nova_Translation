"""Prepare cumulative integration and meaningful mixed-threshold/no-effect negatives."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B191_registration_tools_v5395')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/register_lil_B190_v5345.py');text=source.read_text(encoding='utf-8')
    a=text.index("        ('lost-layout-reason'");b=text.index("        ('wrong-timing-disclosure'",a)
    extra="""        ('lost-layout-reason',doc['layout_retention_review_proof'],lambda v:v['retained_layouts'][0].update(reason='')),
        ('wrong-source-voice',doc['actor_voice_contract'],lambda v:next(r for r in v['fresh2_actor_names']['rows'] if r['actor_ID']==154).update(original_voice_class=0)),
        ('wrong-progressive-role',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'154':'Retainer'})),
        ('wrong-catalogue-role',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'154':'Sailor'})),
        ('wrong-city-alias',doc['actor_terminology_reconciliation'],lambda v:v['two_source_current_city_aliases'][0].update(text='Amsterdam')),
        ('invented-kinship',doc['actor_terminology_reconciliation'],lambda v:v.update(familiar_oyajisan_does_not_prove_fatherhood_age_or_employment_relation=False)),
        ('lost-buyout-urgency-and-profit-claims',doc['actor_terminology_reconciliation'],lambda v:v.update(exclusive_color_competitor_buyout_popularity_imminent_sellout_and_conditional_profit_are_source_explicit_character_claims=False)),
        ('lost-repeated-doubt',doc['actor_terminology_reconciliation'],lambda v:v.update(two_identical_soukanaa_doubts_and_distinct_soudesu_soudesutte_replies_preserved=False)),
        ('invented-verified-profit',doc['actor_terminology_reconciliation'],lambda v:v.update(no_narrator_verified_shortage_stock_price_rise_guaranteed_profit_or_earned_game_mechanic=False)),
        ('wrong-category-as-commodity',doc['actor_terminology_reconciliation'],lambda v:v.update(category_index=42)),
        ('wrong-category-consumer',doc['actor_terminology_reconciliation'],lambda v:v['current_category_binding']['rows'][-1].update(text='Med')),
        ('lost-clean-first-disclosure',doc['actor_terminology_reconciliation'],lambda v:v.update(no_predecessor_English_exposed=False)),
        ('missing-carried-result-case',doc['carried_result_proof'],lambda v:v['cases'].pop()),
        ('wrong-native-end-prior-result',doc['carried_result_proof'],lambda v:v['cases'][2].update(end_native_result=[0,0,0,0,0,0])),
        ('lost-carried-result-flag',doc['carried_result_proof'],lambda v:v.update(original_interpreter_preserves_caller_second_result_word=False)),
        ('wrong-actual-end-result',actual_proof,lambda v:v['versions'][0]['selected_B22_command_pairs'][-1].update(result_words=[0,0])),
        ('wrong-second700-threshold',doc['relocated_control_proof'],lambda v:v['predicate_pairs'][1]['cases'][0].update(threshold=500)),
        ('wrong-owned700-threshold',operand,lambda v:next(r for r in v['cases'] if r['offset']==28).update(threshold=500)),
        ('duplicate-owned-site',operand,lambda v:v['cases'][0].update(offset=28)),
        ('invented-actual-effect',actual_proof,lambda v:v['versions'][0]['source_A000'].append({'word':40960})),
        ('wrong-second-actual-draw',actual_proof,lambda v:v['versions'][0]['actual_predicate_transitions'][1].update(source_offset=28)),
        ('lost-R64-wrap-proof',doc['source_bound_wrap_refinement_proof'],lambda v:v.update(all13_words_controls_and_prose_unchanged=False)),
        ('concealed-other-wrap-changes',doc['source_bound_wrap_refinement_proof'],lambda v:v.update(twelve_other_compiled_targets_exact=False)),
        ('lost-R64-boundary-reason',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==64).pop('reviewed_ordinary_boundaries')),
        ('lost-wrap-mutation-control',doc['source_bound_wrap_refinement_proof'],lambda v:v['exact_source_and_prose_mutation_controls'].pop()),
        ('unreviewed-other-boundary',str(DOC),lambda v:v['records'][0].update(reviewed_ordinary_boundaries=[{'after_word':'dye'}])),
    """
    c=text.index("        description='Complete V5304");e=text.index('        note=',c)
    description="        description='Complete V5346 plus13 B191 whole-exchange reviews:5 revisions/8 justified retentions. Shopkeeper86/Sailor154 discuss a dye color. Restore buyout warning,urgency,rapid depletion,delegation and kinship-free familiar profit reassurance;retain repeated doubts/answers and the tentative Dyes/Calicut notice. Profit/shortage are speaker claims. Four source names,voices0/4,category14 and two city aliases bind. Exact R64 source/prose soft wrap uses2 safe rows with every word unchanged. All38 commands,three500/700/500 predicates,16branches,four effects and no-effect paths,C200,end and source2 tailzeros restore exactly. Source736/734 becomes680/680. Two9001-frame content boots show13 panels,51holds,115nontext pairs,20fullscreens and normal return. Both unforced875/988 draws select the original no-effect path. Returns5977/5975,twelve timings,four original indicators and unequal final PRNG are disclosed;final RGB,five native groups and whole actor agree. No natural activation,earned state or actual execution of the four alternative effects is claimed.',\n"
    row=derive(source,'scripts/register_lil_B191_v5395.py',{
        text[a:b]:extra,text[c:e]:description,'B190':'B191','lil_B190_layout_v1':'lil_B191_layout_v3','registration_v5345':'registration_v5395',
        'all-routes-unified-v5346':'all-routes-unified-v5396','combined_v5304':'combined_v5346','all-routes-unified-v5304':'all-routes-unified-v5346','V5304':'V5346',
        'editorial_manuscript_v4':'editorial_manuscript_v5','editorial_handoff_verification_v5310':'editorial_handoff_verification_v5352','reference_approval_v5343':'reference_approval_v5393','loader_v5333':'loader_v5382',
        "'layout_retention_review_proof','carried_result_proof']":"'layout_retention_review_proof','carried_result_proof','source_bound_wrap_refinement_proof']",
        'native_approval_v5327/all17':'native_approval_v5376/all13','actual_v5340b/actual_all17_progressive_FE_RNG_effect':'actual_v5389/actual_all13_progressive_FE_RNG_effect_or_no_effect',
        'predicate500_v5330/all12_aligned_original500_ownership_cases':'predicates_v5379/all36_original_mixed_predicate_ownership_cases',
        "len(proof['changed_records'])==17":"len(proof['changed_records'])==13",'complete_matching_observations=16':'complete_matching_observations=12',"'{SPEAKER:9F}Hello.'":"'{SPEAKER:56}Hello.'",
        'all5_source_and_relocated_structural_paths_identical':'all125_source_and_relocated_structural_paths_identical',
        'invented-final-RNG-inequality':'concealed-final-RNG-inequality','lambda v:v.update(PRNG_equality=False)':'lambda v:v.update(PRNG_equality=True)',
        'build_integrated_release_v5345.tmp':'build_integrated_release_v5395.tmp','expected_manifest_batches=574':'expected_manifest_batches=575','positive_records=17':'positive_records=13','expected_batches=574':'expected_batches=575',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_guarded_registration.json',dict(derivation=row,profile='all-routes-unified-v5396',parent='all-routes-unified-v5346',
        mixed_thresholds_no_effect_actual_path_source_terms_and_exact_R64_wrap_rejections=True,no_shared_mutation_yet=True,full_goal_complete=False))
