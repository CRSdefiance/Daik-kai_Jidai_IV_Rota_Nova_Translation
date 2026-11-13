"""Expose the full predecessor exchange only after clean glosses and native terms."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B187_comparison_tools_v5195')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/compare_lil_B185_English_v5094.py','scripts/compare_lil_B187_English_v5195.py',{
        'B185':'B187','comparison_v5094':'comparison_v5195','source_v5087/all8':'source_v5188/all16',
        'terms_v5093/two_couple_roles_Stockholm_Furs_and_reported_sales_prices_reconciliation':
        'terms_v5194/Sailor_Square_Shopkeeper_Malacca_Almond_and_reported_remedy_reconciliation',
        'voices_v5088':'voices_v5189','dispatches_v5089/all8':'dispatches_v5190/all16','names_v5092':'names_v5193',
        'controls_v5091':'controls_v5192','all8_complete_clean_and_predecessor_exchange':'all16_complete_clean_and_predecessor_exchange',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_exchange_comparison.json',dict(derivation=row,
        clean_glosses_roles_voices_names_controls_and_terms_already_bound=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared complete sixteen-object comparison;prior English remains comparison material.')
