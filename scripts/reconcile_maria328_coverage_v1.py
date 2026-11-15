"""Extend the exact source census by328 registered objects without replaying native inventory."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/reconcile_maria301_coverage_v1.py').read_text(encoding='utf-8'),{
    'work/story_source_coverage_20261109_SC3_v2':'work/story_source_coverage_20261109_SC3_v7',
    'work/story_source_coverage_20261109_SC3_v1':'work/story_source_coverage_20261109_SC3_v6',
    'maria301_integrated_final_review_v1.json':'maria328_integrated_final_review_v1.json',
    'work/maria301_release_v1':'work/maria328_release_v1',
    "len(prior['missing']) == 4932":"len(prior['missing']) == 3732",
    "doc['all301_individual_five_gates_pass']":"doc['all328_individual_five_gates_pass']",
    'Maria_SC3_B0_B32_clean_20261109':'Maria_SC3_B73_B95_clean_20261109',
    'len(fresh) == 301':'len(fresh) == 328','len(set(added)) == 301':'len(set(added)) == 328',
    'len(keys) == 498 and len(missing) == 4631':'len(keys) == 1725 and len(missing) == 3404',
    'previous_exact_bindings_reused=197,new_exact_bindings=301':'previous_exact_bindings_reused=1397,new_exact_bindings=328',
    'SC3 census:498 exact reviewed objects,4631 remaining':'SC3 census:1725 exact reviewed objects,3404 remaining',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-clean-source-andledger-position-reconciliation328','exec'),globals())
