"""Reconcile330 registered objects with the preserved complete native inventory."""
from scripts.reconcile_maria328_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/story_source_coverage_20261109_SC3_v7':'work/story_source_coverage_20261109_SC3_v8',
    'work/story_source_coverage_20261109_SC3_v6':'work/story_source_coverage_20261109_SC3_v7',
    'maria328_integrated_final_review_v1.json':'maria330_integrated_final_review_v1.json','work/maria328_release_v1':'work/maria330_release_v1',
    "len(prior['missing']) == 3732":"len(prior['missing']) == 3404","doc['all328_individual_five_gates_pass']":"doc['all330_individual_five_gates_pass']",
    'Maria_SC3_B73_B95_clean_20261109':'Maria_SC3_B96_B124_clean_20261109','len(fresh) == 328':'len(fresh) == 330','len(set(added)) == 328':'len(set(added)) == 330',
    'len(keys) == 1725 and len(missing) == 3404':'len(keys) == 2055 and len(missing) == 3074',
    'previous_exact_bindings_reused=1397,new_exact_bindings=328':'previous_exact_bindings_reused=1725,new_exact_bindings=330',
    'SC3 census:1725 exact reviewed objects,3404 remaining':'SC3 census:2055 exact reviewed objects,3074 remaining',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-exact-clean-source-andledger-position-reconciliation','exec'),globals())
