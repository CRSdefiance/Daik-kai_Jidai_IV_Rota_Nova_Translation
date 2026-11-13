"""Prepare the formal whole-exchange comparison after B186 source and terms."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_comparison_preparation_v5140')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/compare_lil_B185_English_v5094.py','scripts/compare_lil_B186_English_v5140.py',{
        'B185':'B186','comparison_v5094':'comparison_v5140','source_v5087':'source_v5132',
        'all8_clean_current_complete_context':'all12_clean_current_complete_context',
        'terms_v5093/two_couple_roles_Stockholm_Furs_and_reported_sales_prices_reconciliation':'terms_v5139b/Owner_Cook_Alexandria_and_sweet_things_context_reconciliation',
        'voices_v5088':'voices_v5133','dispatches_v5089/all8_source_current':'dispatches_v5135/all12_source_current',
        'names_v5092':'names_v5137',
        'controls_v5091/A000_C200_single_end_and_no_relative_or_predicate_contract':'controls_v5138/one_predicate_three_A000_C200_six_relative_sites_and_single_end',
        'all8_complete_clean_and_predecessor_exchange':'all12_complete_clean_and_predecessor_exchange',
        '        predecessor_is_comparison_material_not_translation_source=True,':
        "        predecessor_is_comparison_material_not_translation_source=True,\n        prior_incidental_closing_FE_exposure_disclosed_in_terms=terms['exposure_disclosure'],\n        first_formal_spoken_exchange_comparison_after_source_roles_controls_and_terms=True,",
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_formal_comparison.json',dict(derivation=row,new_review_credit=0,full_goal_complete=False))
    print('Prepared formal B186 comparison with explicit incidental FE disclosure.')
