"""Prepare cumulative registration with meaningful cooking/three-portrait negatives."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B193_registration_tools_v5477')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/register_lil_B192_v5436.py');text=source.read_text(encoding='utf-8')
    a=text.index("        description='Complete V5396");b=text.index('        note=',a)
    description="        description='Complete V5437 plus15 B193 whole-exchange reviews:8 revisions/7 justified retentions. Preserve three source Ladies,meal praise,reported spice classification,local ingredient compatibility,cost concern,relative reassurance,personal tentative dinner plan,immediate cooking-teaching offer,delight and explicit friendship. Keep Chili29/Seoul names and older compact-label fidelity scope. All18 source commands,A000,C200,end and2 source tailzeros restore exactly. Fifteen actual panels,59 holds,115 nontext pairs and12 full screens pass. Ten speech timings differ;returns6457/6457,sampled postscene/final RGB,five native groups,whole actor and measured final PRNG agree within scope. Keep corrected111-character four-row explanation and other individual layout reasons;no font,width,guard or boundary exception.',\n"
    c=text.index("    mutations.extend([\n        ('lost-popularity-hyperbole-boundary'");e=text.index('    for label,path,edit in mutations:',c)
    extras="""    mutations.extend([
        ('lost-cooking-and-immediate-teaching-context',doc['actor_terminology_reconciliation'],lambda v:v.update(source_cooking_preparation_question_and_immediate_teaching_offer_not_trade_advice=False)),
        ('lost-reported-spice-classification',doc['actor_terminology_reconciliation'],lambda v:v.update(first_time_meal_praise_stimulating_flavor_reported_spice_classification_and_local_ingredient_compatibility_preserved=False)),
        ('erased-source-friendship-or-invented-kinship',doc['actor_terminology_reconciliation'],lambda v:v.update(friendship_explicit_in_otomodachi_preserved_without_invented_kinship_romance_marriage_employment_or_prior_history=False)),
        ('invented-price-profit-or-scarcity',doc['actor_terminology_reconciliation'],lambda v:v.update(source_price_question_and_relative_reassurance_preserved_as_character_claims_without_amount_scarcity_or_profit=False)),
        ('invented-completed-cooking-or-lesson',doc['actor_terminology_reconciliation'],lambda v:v.update(tonight_tentative_household_use_and_now_teaching_offer_not_completed_purchase_cooking_or_lesson=False)),
        ('invented-stew-powder-or-quantity',doc['actor_terminology_reconciliation'],lambda v:v.update(Chili29_individual_commodity_not_category_or_chili_stew_powder_recipe_origin_or_specific_quantity=False)),
        ('lost-layout-retention-reason',doc['layout_retention_review_proof'],lambda v:v['retained_layouts'][0].update(reason='')),
        ('wrong-explanation-character-count',doc['layout_retention_review_proof'],lambda v:v.update(exact_paragraph_ASCII_characters=109)),
    ])
"""
    row=derive(source,'scripts/register_lil_B193_v5477.py',{
        text[a:b]:description,text[c:e]:extras,'B192':'B193','registration_v5436':'registration_v5477','all-routes-unified-v5437':'all-routes-unified-v5478',
        'combined_v5396':'combined_v5437','all-routes-unified-v5396':'all-routes-unified-v5437','V5396':'V5437','verification_v5402':'verification_v5443',
        'reference_approval_v5434':'reference_approval_v5475','loader_v5424':'loader_v5465','native_approval_v5419/all8':'native_approval_v5460/all15','actual_v5431/actual_all8':'actual_v5472/actual_all15',
        "len(proof['changed_records'])==8":"len(proof['changed_records'])==15","'{SPEAKER:99}Hello.'":"'{SPEAKER:A6}Hello.'",'complete_matching_observations=7':'complete_matching_observations=14',
        'native_four_consumer_cases':'native_six_consumer_cases','fresh2_actor_names':'fresh3_actor_names',"if r['actor_ID']==153":"if r['actor_ID']==166",
        'wrong-progressive-Sailor-role':'wrong-progressive-Lady-role','wrong-catalogue-Retainer-role':'wrong-catalogue-Lady-role',"{'153':'Retainer'}":"{'166':'Sailor'}","{'153':'Sailor'}":"{'166':'Retainer'}",
        "v['one_source_current_city_alias']":"v['two_source_current_city_aliases'][0]",'concealed-final-RNG-inequality':'invented-final-RNG-inequality','lambda v:v.update(PRNG_equality=True)':'lambda v:v.update(PRNG_equality=False)',
        'tentative_Tobacco_Istanbul_FE_distinct_from_character_popularity_claim_prior_location_or_earned_fashion':'tentative_Chili_Seoul_FE_does_not_establish_earlier_location_or_earned_fashion',
        'build_integrated_release_v5436.tmp':'build_integrated_release_v5477.tmp','expected_manifest_batches=576':'expected_manifest_batches=577','positive_records=8':'positive_records=15','expected_batches=576':'expected_batches=577'} )
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_registration.json',dict(derivation=row,parent_profile='all-routes-unified-v5437',profile='all-routes-unified-v5478',
        exact_three_actors_six_names_voices_source_cooking_friendship_reportedness_price_intentions_layout_and_measured_actual_negatives=True,no_ROM_registry_or_credit_change=True,full_goal_complete=False))
