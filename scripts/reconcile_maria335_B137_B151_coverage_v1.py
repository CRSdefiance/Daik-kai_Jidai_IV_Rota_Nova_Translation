"""Extend the exact source census by335 registered objects without replaying inventory."""
from scripts.reconcile_maria337_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/story_source_coverage_20261109_SC3_v9':'work/story_source_coverage_20261109_SC3_v10',
    'work/story_source_coverage_20261109_SC3_v8':'work/story_source_coverage_20261109_SC3_v9',
    'maria337_integrated_final_review_v1.json':'maria335_B137_B151_integrated_final_review_v1.json',
    'work/maria337_release_v1':'work/maria335_B137_B151_release_v1',
    "len(prior['missing']) == 3074":"len(prior['missing']) == 2737",
    "doc['all337_individual_five_gates_pass']":"doc['all335_individual_five_gates_pass']",
    'Maria_SC3_B125_B136_clean_20261109':'Maria_SC3_B137_B151_clean_20261109',
    'len(fresh) == 337':'len(fresh) == 335','len(set(added)) == 337':'len(set(added)) == 335',
    'len(keys) == 2392 and len(missing) == 2737':'len(keys) == 2727 and len(missing) == 2402',
    'previous_exact_bindings_reused=2055,new_exact_bindings=337':'previous_exact_bindings_reused=2392,new_exact_bindings=335',
    'SC3 census:2392 exact reviewed objects,2737 remaining':'SC3 census:2727 exact reviewed objects,2402 remaining',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-exact-clean-source-andledger-position-reconciliation','exec'),globals())
