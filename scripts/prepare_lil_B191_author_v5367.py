"""Prepare complete contextual manuscript with five revisions/eight justified retentions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B191_author_tools_v5367')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/author_lil_B190_v5323b.py');text=source.read_text(encoding='utf-8')
    a=text.index('    doc.update(records=rows,revised=10,retained=7,');b=text.index('    ROOT.mkdir',a)
    updated="""    doc.update(records=rows,revised=5,retained=8,
        source_Square_Shopkeeper86_and_Sailor154_catalogue_Retainer_voices0_4_preserved=True,
        source_urgency_competitor_buyout_popularity_speed_conditional_profit_and_explicit_doubt_preserved=True,
        familiar_oyajisan_not_fatherhood_rank_employment_or_joint_profit_partnership=True,
        two_identical_doubts_and_distinct_enthusiastic_insistent_replies_preserved=True,
        delegation_and_sulking_request_not_completed_purchase_or_delivery=True,
        source_category14_Dyes_two_Calicut_aliases_and_tentative_FE_preserved=True,
        source38_commands_three500_700_500_predicates16_relatives_four_A000s_no_effect_paths_C200_end_two_tailzeros_preserved=True,
        no_earlier_location_earned_state_stock_price_or_profit_guarantee_invented=True,full_goal_complete=False)
"""
    row=derive(source,'scripts/author_lil_B191_v5367.py',{
        text[a:b]:updated,'B190':'B191','lil_B190_prose_v5322b':'lil_B191_prose_v5366','author_v5323b':'author_v5367','comparison_v5321':'comparison_v5365',
        'editorial_manuscript_v1b':'editorial_manuscript_v1','all17':'all13',"len(gloss['records'])==17":"len(gloss['records'])==13",
        'voices_v5315':'voices_v5357','dispatches_v5316':'dispatches_v5358','and6_control_leaves':'and9_control_leaves','branches_v5318':'branches_v5360','entry_v5317':'entry_v5359',
        'controls_v5318/one_predicate_three_A000_C200_six_relative_sites_and_single_end':'controls_v5363/three_predicates_four_A000_C200_sixteen_relative_sites_and_single_end',
        'names_v5319':'names_v5361',"{'revise':10,'retain-wording':7}":"{'revise':5,'retain-wording':8}",
        'all7_retentions':'all8_retentions','B190:17 whole-exchange decisions,10 revisions/7 justified retentions.':'B191:13 whole-exchange decisions,5 revisions/8 justified retentions.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_bound_author.json',dict(derivation=row,
        full13_record_exchange_and_five_gates_per_record_required=True,source_kinship_invention_removed_urgency_and_buyout_restored=True,
        existing_natural_words_retained_with_individual_reasons=True,no_ROM_registry_or_credit_change=True,full_goal_complete=False))
