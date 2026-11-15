"""Prepare exact-parent cumulative B192 registration and meaningful rejection cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B192_registration_tools_v5436')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/register_lil_B188_v5262b.py');text=source.read_text(encoding='utf-8')
    a=text.index("        description='Complete V5219");b=text.index('        note=',a)
    description="        description='Complete V5396 plus8 B192 whole-exchange reviews:5 revisions/3 justified retentions. Preserve the smoking-experience question reversal,lack of opportunity,popularity hyperbole,stammered curiosity,offer,follow-me invitation and hesitant assent. Popularity remains character speech;Tobacco33/Istanbul forecast stays tentative. All11 source commands,A000,C200,end and2 source tailzeros restore exactly. Eight actual panels,31 holds,115 nontext pairs and26 full screens pass. Nine timings,seven later original A-indicator differences and unequal final PRNG remain disclosed;returns4775/4777,final RGB,five native groups and whole actor agree. Keep individual R16/R23 layout reasons;no font,width,guard or boundary exception.',\n"
    c=text.index("    mutations.extend([\n        ('lost-source-giyaman-glass-distinction'");e=text.index('    for label,path,edit in mutations:',c)
    extras="""    mutations.extend([
        ('lost-popularity-hyperbole-boundary',doc['actor_terminology_reconciliation'],lambda v:v.update(probably_only_person_in_this_town_is_character_hyperbole_not_narrator_statistics_or_named_location=False)),
        ('lost-source-hesitation-and-question-reversal',doc['actor_terminology_reconciliation'],lambda v:v.update(question_reversal_lack_of_opportunity_popularity_hyperbole_stammered_curiosity_offer_and_hesitant_assent_preserved=False)),
        ('invented-completed-smoking-or-gift',doc['actor_terminology_reconciliation'],lambda v:v.update(offer_and_follow_me_assent_not_completed_smoking_purchase_gift_or_specific_destination=False)),
        ('invented-age-health-or-coercion',doc['actor_terminology_reconciliation'],lambda v:v.update(no_invented_age_rank_employment_smoking_history_dependence_coercion_or_health_claim=False)),
        ('invented-smoke-equipment',doc['actor_terminology_reconciliation'],lambda v:v.update(source_tobacco_and_smoking_not_sanitized_or_changed_to_pipe_cigar_cigarette_or_brand=False)),
        ('invented-kinship-or-rank',doc['actor_terminology_reconciliation'],lambda v:v.update(Port_Worker115_familiar_aniki_role_does_not_prove_brotherhood_or_kinship=False)),
        ('lost-layout-retention-reason',doc['layout_retention_review_proof'],lambda v:v['retained_layouts'][0].update(reason='')),
    ])
"""
    row=derive(source,'scripts/register_lil_B192_v5436.py',{
        text[a:b]:description,text[c:e]:extras,'B188':'B192','lil_B188_editorial_v2':'lil_B192_editorial_v1','registration_v5262b':'registration_v5436',
        'all-routes-unified-v5263':'all-routes-unified-v5437','combined_v5219':'combined_v5396','all-routes-unified-v5219':'all-routes-unified-v5396','V5219':'V5396',
        'editorial_handoff_verification_v5225':'editorial_handoff_verification_v5402','reference_approval_v5260':'reference_approval_v5434','loader_v5250':'loader_v5424',
        'native_approval_v5245/all11':'native_approval_v5419/all8','actual_v5257/actual_all11':'actual_v5431/actual_all8',
        "len(proof['changed_records'])==11":"len(proof['changed_records'])==8","'{SPEAKER:82}Hello.'":"'{SPEAKER:99}Hello.'",'complete_matching_observations=10':'complete_matching_observations=7',
        "if r['actor_ID']==130":"if r['actor_ID']==153",'wrong-progressive-Daimyo-role':'wrong-progressive-Sailor-role','wrong-catalogue-Guildmaster-role':'wrong-catalogue-Retainer-role',
        "{'130':'Guildmaster'}":"{'153':'Retainer'}","{'150':'Daimyo'}":"{'153':'Sailor'}",
        "v['two_source_current_city_aliases'][0]":"v['one_source_current_city_alias']",
        'lost-source-collection-decision-and-order':'lost-source-intent-and-tentative-forecast',
        'source_explicit_collection_decision_and_order_to_gather_all_giyaman_in_town_preserved':'tentative_Tobacco_Istanbul_FE_distinct_from_character_popularity_claim_prior_location_or_earned_fashion',
        'build_integrated_release_v5262b.tmp':'build_integrated_release_v5436.tmp','expected_manifest_batches=572':'expected_manifest_batches=576','positive_records=11':'positive_records=8','expected_batches=572':'expected_batches=576',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_registration.json',dict(derivation=row,parent_profile='all-routes-unified-v5396',profile='all-routes-unified-v5437',
        source_popularity_hyperbole_hesitation_intentions_names_voices_full_metadata_and_layout_negatives=True,no_ROM_registry_or_credit_change=True,full_goal_complete=False))
