"""Extend the exact clean SC3 census with310 registered reviews without replaying native inventory."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/reconcile_maria301_coverage_v1.py').read_text(encoding='utf-8'),{
    'work/story_source_coverage_20261109_SC3_v2':'work/story_source_coverage_20261109_SC3_v5',
    'work/story_source_coverage_20261109_SC3_v1':'work/story_source_coverage_20261109_SC3_v4',
    'maria301_integrated_final_review_v1.json':'maria310_integrated_final_review_v1.json',
    'work/maria301_release_v1':'work/maria310_release_v1',
    "len(prior['missing']) == 4932":"len(prior['missing']) == 4345",
    "doc['all301_individual_five_gates_pass']":"doc['all310_individual_five_gates_pass']",
    'Maria_SC3_B0_B32_clean_20261109':'Maria_SC3_B51_B57_clean_20261109',
    'len(fresh) == 301':'len(fresh) == 310', 'len(set(added)) == 301':'len(set(added)) == 310',
    'len(keys) == 498 and len(missing) == 4631':'len(keys) == 1094 and len(missing) == 4035',
    'previous_exact_bindings_reused=197,new_exact_bindings=301':'previous_exact_bindings_reused=784,new_exact_bindings=310',
    'SC3 census:498 exact reviewed objects,4631 remaining':'SC3 census:1094 exact reviewed objects,4035 remaining',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-exact-clean-source-position-ledger-reconciliation310','exec'),globals())
