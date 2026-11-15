"""Prepare eight contextual decisions:five revisions and three justified retentions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B192_author_tools_v5415')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/author_lil_B188_v5241.py');text=source.read_text(encoding='utf-8')
    a=text.index('    doc.update(records=rows,revised=4,retained=7,');b=text.index('    ROOT.mkdir',a)
    updated="""    doc.update(records=rows,revised=5,retained=3,
        source_Port_Worker115_and_Sailor153_catalogue_Retainer_voices0_4_preserved=True,
        opening_question_reversal_lack_of_chance_and_candid_admission_distinct=True,
        popularity_and_probable_only_person_hyperbole_are_character_claims=True,
        nervous_question_personal_wish_offer_follow_me_and_hesitant_assent_preserved=True,
        source_tobacco_smoking_not_sanitized_or_changed_to_equipment_brand_or_instruction=True,
        no_age_rank_kinship_employment_dependence_health_claim_or_completed_smoking_invented=True,
        source_Tobacco33_and_one_Istanbul_alias_preserved=True,
        source11_linear_commands_one_A000_C200_end_two_tailzeros_no_predicates_or_relatives_preserved=True,
        tentative_Tobacco_Istanbul_FE_not_earlier_location_or_earned_fashion=True,full_goal_complete=False)
"""
    row=derive(source,'scripts/author_lil_B192_v5415.py',{
        text[a:b]:updated,'B188':'B192','lil_B188_prose_v5240':'lil_B192_prose_v5414','author_v5241':'author_v5415','comparison_v5239':'comparison_v5413',
        'all11':'all8',"len(gloss['records'])==11":"len(gloss['records'])==8",'voices_v5233':'voices_v5407','dispatches_v5234':'dispatches_v5408','controls_v5236':'controls_v5410','entry_v5235':'entry_v5409','names_v5237':'names_v5411',
        "{'revise':4,'retain-wording':7}":"{'revise':5,'retain-wording':3}",'all7_retentions':'all3_retentions','B188:11 whole-exchange decisions,4 revisions/7 justified retentions.':'B192:8 whole-exchange decisions,5 revisions/3 justified retentions.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_bound_author.json',dict(derivation=row,complete8_record_exchange_reviewed=True,
        five_revisions_three_individual_retentions=True,no_ROM_registry_or_credit_change=True,full_goal_complete=False))
