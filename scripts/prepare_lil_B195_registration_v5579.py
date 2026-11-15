"""Prepare cumulative B195 registration and its source/display rejection checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B195_registration_tools_v5579')

if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/register_lil_B193_v5477.py');text=source.read_text(encoding='utf-8')
    a=text.index("        description='Complete V5437");b=text.index('        note=',a)
    description="        description='Complete V5531 plus20 B195 whole-exchange reviews:3 revisions/17 justified retentions. Preserve three original voice0 roles,six readonly names,the unnamed cheese-rich specialty,skepticism,one shared order,prompt service,wry coaxing,two chewing beats,taste claims,personal future tell-everyone intention and Patron popularity prediction. Both Veracruz aliases and Cheese8 metadata remain exact;older UI fidelity stays open. All23 commands and two source tailzeros restore exactly. Twenty actual panels/79 holds/115 nontext pairs/20 full screens pass;returns7655/7657,15 timing differences,four lower A-indicator differences and unequal final PRNG remain disclosed. Keep original v1 formatter and the complete68-character three-row R17 under unchanged native guards.',\n"
    c=text.index("    mutations.extend([\n        ('lost-cooking-and-immediate-teaching-context'");e=text.index('    for label,path,edit in mutations:',c)
    extras="""    mutations.extend([
        ('invented-named-dish-recipe-origin-or-price',doc['actor_terminology_reconciliation'],lambda v:v.update(source_unnamed_house_specialty_has_plenty_of_cheese_no_invented_pizza_recipe_cuisine_origin_price_or_health_effect=False)),
        ('invented-kinship-from-oyaji-or-aniki',doc['actor_terminology_reconciliation'],lambda v:v.update(source_familiar_oyaji_and_aniki_role_wording_does_not_establish_fatherhood_brotherhood_or_new_kinship=False)),
        ('invented-two-servings-or-purchase-mechanic',doc['actor_terminology_reconciliation'],lambda v:v.update(one_shared_order_not_two_servings_payment_or_purchase_mechanic=False)),
        ('coaxing-changed-to-fraud-or-danger',doc['actor_terminology_reconciliation'],lambda v:v.update(source_damasareta_idiom_coaxes_a_trial_without_actual_deception_fraud_or_danger=False)),
        ('lost-two-chewing-beats',doc['actor_terminology_reconciliation'],lambda v:v.update(two_separate_chewing_beats_and_two_enthusiastic_taste_reactions_preserved=False)),
        ('character-taste-or-popularity-claim-made-narrator-fact',doc['actor_terminology_reconciliation'],lambda v:v.update(source_taste_praise_and_dish_popularity_certainty_remain_character_claims_not_narrator_guarantees=False)),
        ('future-intention-changed-to-advertising-or-profit',doc['actor_terminology_reconciliation'],lambda v:v.update(tell_everyone_is_future_social_intention_not_completed_advertising_trade_demand_profit_or_reward=False)),
        ('lost-older-Cheese8-UI-fidelity-scope',doc['actor_terminology_reconciliation'],lambda v:v.update(Cheese8_older_UI_fidelity_review_stays_open_separate_from_dialogue=False)),
        ('wrong-Cheese8-metadata',doc['actor_terminology_reconciliation'],lambda v:v.update(original_commodity_metadata_hex='0000000000000000')),
        ('lost-R17-layout-retention-reason',doc['source_bound_wrap_retention_proof'],lambda v:v.update(retention_reason='')),
        ('wrong-specialty-character-count',doc['source_bound_wrap_retention_proof'],lambda v:v.update(paragraph_ASCII_characters=67)),
        ('false-two-row-lint-approval',doc['source_bound_wrap_retention_proof'],lambda v:v.update(all11_two_row_splits_fail_unchanged_native_lint=False)),
        ('missing-two-row-split',doc['source_bound_wrap_retention_proof'],lambda v:v['all_complete_word_two_row_splits'].pop()),
        ('invented-boundary-exception',doc['source_bound_wrap_retention_proof'],lambda v:v.update(no_ordinary_boundary_exception_adopted=False)),
        ('changed-formatter-after-retention',doc['source_bound_wrap_retention_proof'],lambda v:v.update(selected_formatter_unchanged=False)),
        ('lost-individual-R17-retention-reason',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==17).update(native_layout_retention_reason='')),
        ('concealed-all-postscene-RGB-differences',doc['postscene_native_state_proof'],lambda v:v['sampled_postscene_whole_RGB_differences_unmasked'].clear()),
    ])
"""
    row=derive(source,'scripts/register_lil_B195_v5579.py',{
        text[a:b]:description,text[c:e]:extras,'B193':'B195','registration_v5477':'registration_v5579',
        'all-routes-unified-v5478':'all-routes-unified-v5580','combined_v5437':'combined_v5531',
        'all-routes-unified-v5437':'all-routes-unified-v5531','V5437':'V5531','verification_v5443':'verification_v5577',
        'reference_approval_v5475':'reference_approval_v5575','loader_v5465':'loader_v5565',
        'native_approval_v5460/all15':'native_approval_v5557/all20','actual_v5472/actual_all15':'actual_v5572/actual_all20',
        "'layout_retention_review_proof'":"'source_bound_wrap_retention_proof'",
        "len(proof['changed_records'])==15":"len(proof['changed_records'])==20", "'{SPEAKER:A6}Hello.'":"'{SPEAKER:77}Hello.'",
        'complete_matching_observations=14':'complete_matching_observations=19',"if r['actor_ID']==166":"if r['actor_ID']==92",
        'wrong-progressive-Lady-role':'wrong-progressive-Barkeep-role','wrong-catalogue-Lady-role':'wrong-catalogue-Barkeep-role',
        "{'166':'Sailor'}":"{'92':'Sailor'}","{'166':'Retainer'}":"{'92':'Retainer'}",
        'invented-final-RNG-inequality':'concealed-final-RNG-inequality','lambda v:v.update(PRNG_equality=False)':'lambda v:v.update(PRNG_equality=True)',
        'tentative_Chili_Seoul_FE_does_not_establish_earlier_location_or_earned_fashion':'tentative_Cheese_Veracruz_FE_not_earlier_location_or_earned_fashion',
        'build_integrated_release_v5477.tmp':'build_integrated_release_v5579.tmp',
        'expected_manifest_batches=577':'expected_manifest_batches=579','positive_records=15':'positive_records=20','expected_batches=577':'expected_batches=579'})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_registration.json',dict(derivation=row,
        parent_profile='all-routes-unified-v5531',profile='all-routes-unified-v5580',
        full_source_context_native_bounds_both_maps_R17_retention_and_actual_difference_negatives=True,
        no_ROM_registry_or_credit_change=True,full_goal_complete=False))
