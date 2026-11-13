"""Extend the exact Maria source census by390 positions without replaying its inventory."""
from scripts.reconcile_maria335_B137_B151_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/story_source_coverage_20261109_SC3_v10':'work/story_source_coverage_20261110_SC3_v11',
    'work/story_source_coverage_20261109_SC3_v9':'work/story_source_coverage_20261109_SC3_v10',
    'maria335_B137_B151_integrated_final_review_v1.json':'maria390_B152_B175_integrated_final_review_v1.json',
    'work/maria335_B137_B151_release_v1':'work/maria390_B152_B175_release_v1',
    "len(prior['missing']) == 2737":"len(prior['missing']) == 2402",
    "doc['all335_individual_five_gates_pass']":"doc['all390_individual_five_gates_pass']",
    'Maria_SC3_B137_B151_clean_20261109':'Maria_SC3_B152_B175_clean_20261109',
    'len(fresh) == 335':'len(fresh) == 390','len(set(added)) == 335':'len(set(added)) == 390',
    'len(keys) == 2727 and len(missing) == 2402':'len(keys) == 3117 and len(missing) == 2012',
    'previous_exact_bindings_reused=2392,new_exact_bindings=335':'previous_exact_bindings_reused=2727,new_exact_bindings=390',
    'SC3 census:2727 exact reviewed objects,2402 remaining':'SC3 census:3117 exact reviewed objects,2012 remaining',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-exact-clean-source-membership-andledger-position-guards','exec'),globals())
