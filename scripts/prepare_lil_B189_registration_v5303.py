"""Prepare cumulative integration and meaningful four-speaker source rejection cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B189_registration_tools_v5303')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/register_lil_B188_v5262b.py');text=source.read_text(encoding='utf-8')
    a=text.index("        description='Complete V5219");b=text.index('        note=',a)
    description="        description='Complete V5263 plus17 B189 whole-scene reviews:10 revisions/7 justified retentions. Guildmaster147/Shopkeeper82 discuss ceramic collecting;Trader104/PortWorker113 privately boast of a recent worthless-ceramics sale and propose approaching the customers. Preserve source-explicit acquisition,expectation,invitation,craze,scarcity,hearsay buying-up,irony and the speaking pair’s short funds. Source ceramics is distinct from unchanged legacy UI China42. Eight names/four voice0 classes bind exact hex93/52/68/71 selectors. All20 source commands,A000,C200,end and original2 tailzeros restore exactly. Seventeen actual panels,67 holds,115 nontext pairs and12 full screens pass. Eight speech timings and unequal final PRNG remain disclosed;returns6937/6937,sampled postscene/final RGB,five native groups and whole actor agree. Keep individual native layout reasons;no font,width,guard or boundary exception.',\n"
    c=text.index("    mutations.extend([\n        ('lost-source-giyaman-glass-distinction'");e=text.index('    for label,path,edit in mutations:',c)
    extras="""    mutations.extend([
        ('lost-reported-buying-up-and-scarcity',doc['actor_terminology_reconciliation'],lambda v:v.update(source_explicit_collecting_craze_good_piece_scarcity_and_hearsay_buying_up_preserved_as_character_claims=False)),
        ('wrong-short-funds-antecedent',doc['actor_terminology_reconciliation'],lambda v:v.update(second_pairs_short_funds_belong_to_Trader_Port_Worker_not_collector_customers=False)),
        ('invented-UI-rename-or-origin',doc['actor_terminology_reconciliation'],lambda v:v.update(ceramics_is_broad_source_term_not_a_new_commodity_UI_rename_or_Chinese_origin_claim=False)),
        ('wrong-hex-decimal-selector-list',doc['actor_terminology_reconciliation'],lambda v:v.update(actual_source_selectors_decimal=[93,52,68,71])),
        ('invented-role-kinship',doc['actor_terminology_reconciliation'],lambda v:v.update(source_role_familiar_forms_do_not_establish_father_brother_master_kinship_or_new_rank=False)),
        ('lost-layout-retention-reason',doc['layout_retention_review_proof'],lambda v:v['retained_layouts'][0].update(reason='')),
    ])
"""
    row=derive(source,'scripts/register_lil_B189_v5303.py',{
        text[a:b]:description,text[c:e]:extras,'B188':'B189','lil_B188_editorial_v2':'lil_B189_editorial_v1','registration_v5262b':'registration_v5303',
        'all-routes-unified-v5263':'all-routes-unified-v5304','combined_v5219':'combined_v5263','all-routes-unified-v5219':'all-routes-unified-v5263','V5219':'V5263',
        'editorial_handoff_verification_v5225':'editorial_handoff_verification_v5269','reference_approval_v5260':'reference_approval_v5301','loader_v5250':'loader_v5291',
        'native_approval_v5245/all11':'native_approval_v5286/all17','actual_v5257/actual_all11':'actual_v5298/actual_all17',
        "len(proof['changed_records'])==11":"len(proof['changed_records'])==17","'{SPEAKER:82}Hello.'":"'{SPEAKER:93}Hello.'",'complete_matching_observations=10':'complete_matching_observations=16',
        'native_four_consumer_cases':'native_eight_consumer_cases','fresh2_actor_names':'fresh4_actor_names',"if r['actor_ID']==130":"if r['actor_ID']==147",
        'wrong-progressive-Daimyo-role':'wrong-progressive-Guildmaster-role','wrong-catalogue-Guildmaster-role':'wrong-catalogue-Trader-role',
        "{'130':'Guildmaster'}":"{'147':'Trader'}","{'150':'Daimyo'}":"{'104':'Guildmaster'}","update(commodity='Paintings')":"update(commodity_UI='Paintings')",
        'lost-source-collection-decision-and-order':'lost-source-recent-acquisition-and-reported-sale',
        'source_explicit_collection_decision_and_order_to_gather_all_giyaman_in_town_preserved':'completed_first_acquisition_and_reported_first_sale_preserved_without_invented_price_quantity_shape_or_origin',
        'build_integrated_release_v5262b.tmp':'build_integrated_release_v5303.tmp','expected_manifest_batches=572':'expected_manifest_batches=573','positive_records=11':'positive_records=17','expected_batches=572':'expected_batches=573',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_registration.json',dict(derivation=row,parent_profile='all-routes-unified-v5263',profile='all-routes-unified-v5304',
        exact_four_speakers_hex_decimal_distinction_eight_names_voices_irony_market_claims_antecedent_and_layout_negatives=True,no_ROM_registry_or_credit_change=True,full_goal_complete=False))
