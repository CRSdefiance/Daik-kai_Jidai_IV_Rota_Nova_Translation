"""Prepare sixteen contextual decisions from the clean-first complete exchange."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B187_author_tools_v5197')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/author_lil_B185_v5096.py','scripts/author_lil_B187_v5197.py',{
        'B185':'B187','all8':'all16','author_v5096':'author_v5197','prose_v5095':'prose_v5196',
        'comparison_v5094':'comparison_v5195',"len(gloss['records'])==8":"len(gloss['records'])==16",
        'voices_v5088':'voices_v5189','dispatches_v5089':'dispatches_v5190','controls_v5091':'controls_v5192','entry_v5090':'entry_v5191','names_v5092':'names_v5193',
        "counts=={'revise':4,'retain-wording':4}":"counts=={'revise':7,'retain-wording':9}",
        """doc.update(records=rows,revised=4,retained=4,two_clean_couple_roles_without_marriage_age_or_kinship_inference=True,
        source_explicit_reported_sales_prices_and_cold_coat_wish_preserved=True,
        FE_prospective_Furs_Stockholm_notice_distinct_from_reported_current_sales_prices=True,source_all11_linear_commands_A000_C200_and_end_preserved=True,full_goal_complete=False)""":
        """doc.update(records=rows,revised=7,retained=9,source_progressive_Sailor155_distinct_from_full_catalogue_Retainer155=True,
        source_Square_Shopkeeper87_and_original_voice0_Sailor_voice4_preserved=True,
        source_reported_unnamed_remedy_effectiveness_and_sales_forgotten_name_memory_trigger_and_search_intentions_preserved=True,
        source_all19_linear_commands_A000_C200_end_and_two_tailzeros_preserved=True,
        FE_prospective_Almonds_Malacca_notice_distinct_from_reported_remedy_claims=True,full_goal_complete=False)""",
        'all4_retentions_individually_justified':'all9_retentions_individually_justified',
        'B185:8 whole-exchange decisions,4 revisions/4 justified retentions':'B187:16 whole-exchange decisions,7 revisions/9 justified retentions',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_bound_author.json',dict(derivation=row,
        complete_exchange_clean_glosses_roles_voices_names_controls_and_terms_precede_comparison=True,
        all_retentions_individually_justified=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared16 contextual decisions:7 revisions/9 justified retentions;native formatting remains pending.')
