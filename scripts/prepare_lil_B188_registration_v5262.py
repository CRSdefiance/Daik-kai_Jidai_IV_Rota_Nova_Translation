"""Prepare complete cumulative registration and scene-specific rejection controls."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B188_registration_tools_v5262')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/register_lil_B187_v5218.py');text=source.read_text(encoding='utf-8')
    a=text.index("        description='Complete V5177");b=text.index('        note=',a)
    description="        description='Complete V5219 plus11 B188 whole-exchange reviews:4 revisions/7 justified retentions. Preserve Daimyo130/Guildmaster150 roles and original voice0,source giyaman/glass,conjecture about a famous craftsman,the collector’s personal discovery,first-person collection decision,sweeping gathering order and formal compliance. The supported my lord address does not invent an additional rank. The Glass/Osaka notice stays tentative. All14 source commands,A000,C200,end and original2 tailzeros restore exactly;target424 bytes is logically complete. Eleven actual panels,43 holds,115 nontext pairs and36 full screens pass. Eleven timings,twelve later original A-indicator differences and unequal final PRNG remain disclosed;final RGB,five native groups and whole actor agree. Retain R22/R38 natural two-row layouts with individual reasons;no font,width,guard or boundary exception.',\n"
    extras="""    mutations.extend([
        ('lost-source-giyaman-glass-distinction',doc['actor_terminology_reconciliation'],lambda v:v.update(source_explicit_giyaman_parenthetical_glass_and_new_name_echo_preserved=False)),
        ('invented-purchase-context',doc['actor_terminology_reconciliation'],lambda v:v.update(gather_not_explicit_buy_no_price_payment_museum_donation_shortage_item_shape_or_completed_collection_invented=False)),
        ('lost-layout-retention-reason',doc['layout_retention_review_proof'],lambda v:v['retained_layouts'][0].update(reason='')),
        ('unbound-my-lord-address',str(DOC),lambda v:v.update(my_lord_supported_by_clean_Daimyo_role_and_marked_deference_not_inferred_kinship_or_new_title=False)),
        ('lost-conjecture-boundary',doc['actor_terminology_reconciliation'],lambda v:v.update(praise_and_famous_craftsman_attribution_are_character_judgment_and_conjecture_not_named_maker_or_proven_origin=False)),
    ])
"""
    row=derive(source,'scripts/register_lil_B188_v5262.py',{
        text[a:b]:description,'B187':'B188','registration_v5218':'registration_v5262','all-routes-unified-v5219':'all-routes-unified-v5263',
        'combined_v5177':'combined_v5219','all-routes-unified-v5177':'all-routes-unified-v5219','V5177':'V5219',
        'editorial_handoff_verification_v5183':'editorial_handoff_verification_v5225','reference_approval_v5216':'reference_approval_v5260','loader_v5206':'loader_v5250',
        'native_approval_v5201/all16':'native_approval_v5245/all11','actual_v5213/actual_all16':'actual_v5257/actual_all11',
        "'postscene_native_state_proof','current_C200_source_ownership_proof'":"'postscene_native_state_proof','current_C200_source_ownership_proof','layout_retention_review_proof'",
        "len(proof['changed_records'])==16":"len(proof['changed_records'])==11","'{SPEAKER:9B}Hello.'":"'{SPEAKER:82}Hello.'",'complete_matching_observations=15':'complete_matching_observations=10',
        "('false-final-RNG-inequality',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_equality=False))":"('concealed-final-RNG-inequality',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_equality=True))",
        "if r['actor_ID']==155":"if r['actor_ID']==130",'wrong-progressive-Sailor-role':'wrong-progressive-Daimyo-role','wrong-catalogue-Retainer-role':'wrong-catalogue-Guildmaster-role',
        "{'155':'Retainer'}":"{'130':'Guildmaster'}","{'155':'Sailor'}":"{'150':'Daimyo'}",
        'lost-source-reported-efficacy-sales-fact':'lost-source-collection-decision-and-order',
        'source_explicit_reported_remedy_effectiveness_and_strong_sales_both_must_be_preserved':'source_explicit_collection_decision_and_order_to_gather_all_giyaman_in_town_preserved',
        '    for label,path,edit in mutations:reject(label,path,edit)':extras+'    for label,path,edit in mutations:reject(label,path,edit)',
        'build_integrated_release_v5218.tmp':'build_integrated_release_v5262.tmp','expected_manifest_batches=571':'expected_manifest_batches=572','positive_records=16':'positive_records=11','expected_batches=571':'expected_batches=572',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_registration.json',dict(derivation=row,parent_profile='all-routes-unified-v5219',profile='all-routes-unified-v5263',
        source_metadata_names_voices_giyaman_collection_and_layout_retention_negatives_required=True,no_ROM_registry_or_credit_change=True,full_goal_complete=False))
