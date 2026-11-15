"""Extend the exact source census by337 registered objects without replaying inventory."""
from scripts.reconcile_maria330_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/story_source_coverage_20261109_SC3_v8':'work/story_source_coverage_20261109_SC3_v9',
    'work/story_source_coverage_20261109_SC3_v7':'work/story_source_coverage_20261109_SC3_v8',
    'maria330_integrated_final_review_v1.json':'maria337_integrated_final_review_v1.json','work/maria330_release_v1':'work/maria337_release_v1',
    "len(prior['missing']) == 3404":"len(prior['missing']) == 3074","doc['all330_individual_five_gates_pass']":"doc['all337_individual_five_gates_pass']",
    'Maria_SC3_B96_B124_clean_20261109':'Maria_SC3_B125_B136_clean_20261109','len(fresh) == 330':'len(fresh) == 337','len(set(added)) == 330':'len(set(added)) == 337',
    'len(keys) == 2055 and len(missing) == 3074':'len(keys) == 2392 and len(missing) == 2737',
    'previous_exact_bindings_reused=1725,new_exact_bindings=330':'previous_exact_bindings_reused=2055,new_exact_bindings=337',
    'SC3 census:2055 exact reviewed objects,3074 remaining':'SC3 census:2392 exact reviewed objects,2737 remaining',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-clean-source-andledger-position-reconciliation','exec'),globals())
