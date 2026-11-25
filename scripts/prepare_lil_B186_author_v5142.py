"""Prepare the twelve-object author record with B186-specific conditional scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_author_preparation_v5142')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/author_lil_B185_v5096.py','scripts/author_lil_B186_v5142.py',{
        'B185':'B186','all8':'all12','author_v5096':'author_v5142','prose_v5095':'prose_v5141',
        'comparison_v5094':'comparison_v5140','len(gloss[\'records\'])==8':'len(gloss[\'records\'])==12',
        'voices_v5088':'voices_v5133','dispatches_v5089':'dispatches_v5135','names_v5092':'names_v5137',
        'controls_v5091/A000_C200_single_end_and_no_relative_or_predicate_contract':'controls_v5138/one_predicate_three_A000_C200_six_relative_sites_and_single_end',
        'entry_v5090':'entry_v5136',
        "branch_proof='work/analysis/lil_B185_controls_v5091/A000_C200_single_end_and_no_relative_or_predicate_contract.json'":
        "branch_proof='work/analysis/lil_B186_branches_v5134/original_relative_skip_operand_proof.json'",
        "counts=={'revise':4,'retain-wording':4}":"counts=={'revise':7,'retain-wording':5}",
        "doc.update(records=rows,revised=4,retained=4,two_clean_couple_roles_without_marriage_age_or_kinship_inference=True,\n        source_explicit_reported_sales_prices_and_cold_coat_wish_preserved=True,\n        FE_prospective_Furs_Stockholm_notice_distinct_from_reported_current_sales_prices=True,source_all11_linear_commands_A000_C200_and_end_preserved=True,full_goal_complete=False)":
        "doc.update(records=rows,revised=7,retained=5,two_clean_Owner_Cook_roles_without_rank_kinship_or_nobility_inference=True,\n        comic_sweet_emphasis_self_authority_and_two_perfunctory_replies_preserved=True,\n        source_all24_commands_one700_predicate_six_relatives_three_alternative_effects_C200_end_and_two_tailzeros_preserved=True,\n        FE_prospective_Sweets_Alexandria_notice_distinct_from_Owners_confident_prediction=True,\n        untranslated_Alexandria_alias_is_separate_unreviewed_caller_lead=True,\n        incidental_closing_FE_exposure_disclosed_in_terms=True,full_goal_complete=False)",
        'all4_retentions_individually_justified':'all5_retentions_individually_justified',
        'B185:8 whole-exchange decisions,4 revisions/4 justified retentions':'B186:12 whole-exchange decisions,7 revisions/5 justified retentions',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_bound_author.json',dict(derivation=row,new_review_credit=0,full_goal_complete=False))
    print('Prepared B186 author:12 decisions with exact source/current references and individual retention reasons.')
