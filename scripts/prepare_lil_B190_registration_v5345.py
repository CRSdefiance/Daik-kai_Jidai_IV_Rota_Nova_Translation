"""Prepare guarded B190 cumulative registration and meaningful rejection cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B190_registration_tools_v5345')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/register_lil_B186_v5176.py');text=source.read_text(encoding='utf-8')
    a=text.index("        ('lost-wrap-proof'");b=text.index("        ('wrong-timing-disclosure'",a)
    extra="""        ('lost-layout-reason',doc['layout_retention_review_proof'],lambda v:v['retained_layouts'][0].update(reason='')),
        ('wrong-source-voice',doc['actor_voice_contract'],lambda v:next(r for r in v['fresh2_actor_names']['rows'] if r['actor_ID']==159).update(original_voice_class=0)),
        ('wrong-progressive-role',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'159':'Retainer'})),
        ('wrong-catalogue-role',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'159':'Sailor'})),
        ('wrong-city',doc['actor_terminology_reconciliation'],lambda v:v['one_source_current_city_alias'].update(text='Amsterdam')),
        ('lost-reported-cure',doc['actor_terminology_reconciliation'],lambda v:v.update(source_explicit_publicly_sold_medicine_one_go_cure_and_panacea_reputation_preserved_as_hearsay=False)),
        ('lost-skepticism',doc['actor_terminology_reconciliation'],lambda v:v.update(surprise_then_explicit_truth_question_then_reported_apparent_truth_kept_distinct=False)),
        ('invented-medical-fact',doc['actor_terminology_reconciliation'],lambda v:v.update(no_verified_efficacy_guaranteed_mechanic_medical_role_recipe_dose_ingredient_brand_or_price_invented=False)),
        ('wrong-category-as-commodity',doc['actor_terminology_reconciliation'],lambda v:v.update(category_index=42)),
        ('wrong-category-consumer',doc['actor_terminology_reconciliation'],lambda v:v['current_category_binding']['rows'][-1].update(text='Med')),
        ('lost-clean-first-disclosure',doc['actor_terminology_reconciliation'],lambda v:v.update(no_predecessor_English_exposed=False)),
        ('missing-carried-result-case',doc['carried_result_proof'],lambda v:v['cases'].pop()),
        ('wrong-native-end-prior-result',doc['carried_result_proof'],lambda v:v['cases'][2].update(end_native_result=[0,0,0,0,0,0])),
        ('lost-carried-result-flag',doc['carried_result_proof'],lambda v:v.update(original_interpreter_preserves_caller_second_result_word=False)),
        ('wrong-actual-end-result',actual_proof,lambda v:v['versions'][0]['selected_B22_command_pairs'][-1].update(result_words=[0,0])),
"""
    c=text.index("        description='Complete V5122");e=text.index('        note=',c)
    description="        description='Complete V5304 plus17 B190 whole-exchange reviews:10 revisions/7 individually justified retentions. Sailor159/PortWorker119 rumor about the mansion owner,unexplained illness,reported retail one-go cure,explicit skepticism,panacea reputation,personal wish and proposed shopping. Preserve source claims as hearsay and the tentative Medicine/Havana notice. Medicine is category13,not a single commodity. Four source names distinguish Sailor/Retainer;voices4/0 remain. All29 commands,one500 predicate,six branches,three alternative effects,C200,end and2 tailzeros restore exactly. Two9001-frame fixtures show17 panels,67 holds,115 nontext pairs and16 fullscreens. Original roll875/result2/effect52 and carried C2003,2/end0,2 agree. Returns6934/6937,nine timings/two later indicator-shadow differences disclosed;final measured PRNG,RGB,five native groups and actor agree within measured scope. No natural-event or future-world claim.',\n"
    row=derive(source,'scripts/register_lil_B190_v5345.py',{
        text[a:b]:extra,text[c:e]:description,'B186':'B190','lil_B186_layout_v4':'lil_B190_layout_v1','registration_v5176':'registration_v5345',
        'all-routes-unified-v5177':'all-routes-unified-v5346','combined_v5122':'combined_v5304','all-routes-unified-v5122':'all-routes-unified-v5304','V5122':'V5304',
        'editorial_manuscript_v6':'editorial_manuscript_v4','editorial_handoff_verification_v5174':'editorial_handoff_verification_v5310',
        'reference_approval_v5172':'reference_approval_v5343','loader_v5162':'loader_v5333',
        "'source_bound_wrap_refinement_proof'":"'layout_retention_review_proof','carried_result_proof'",
        'native_approval_v5156/all12':'native_approval_v5327/all17','actual_v5169/actual_all12':'actual_v5340b/actual_all17',
        'predicate700_v5159/all12_aligned_and_unaligned_original700':'predicate500_v5330/all12_aligned_original500',
        "len(proof['changed_records'])==12":"len(proof['changed_records'])==17",'complete_matching_observations=11':'complete_matching_observations=16',
        "'{SPEAKER:AE}Hello.'":"'{SPEAKER:9F}Hello.'",'concealed-RNG-inequality':'invented-final-RNG-inequality','lambda v:v.update(PRNG_equality=True)':'lambda v:v.update(PRNG_equality=False)',
        "next(r for r in v['cases'] if r['operand_pointer_unaligned'])":"next(r for r in v['cases'] if r['version']=='current')",
        'wrong-scratch-address':'wrong-native-RNG-write-address','wrong-scratch-value':'wrong-native-RNG-write-value','update(value=701)':'update(value=501)',
        'build_integrated_release_v5176.tmp':'build_integrated_release_v5345.tmp','expected_manifest_batches=570':'expected_manifest_batches=574',
        'positive_records=12':'positive_records=17','expected_batches=570':'expected_batches=574',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_guarded_registration.json',dict(derivation=row,profile='all-routes-unified-v5346',parent='all-routes-unified-v5304',
        source_terms_names_voices_native_layout_and_original_carried_result_rejection_cases=True,
        no_ROM_registry_or_credit_mutation=True,full_goal_complete=False))
