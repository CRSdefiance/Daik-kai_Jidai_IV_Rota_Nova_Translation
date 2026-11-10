"""Extend the exact Maria source census by305 positions without replaying inventory."""
from scripts.reconcile_maria390_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/story_source_coverage_20261110_SC3_v11':'work/story_source_coverage_20261110_SC3_v12',
    'work/story_source_coverage_20261109_SC3_v10':'work/story_source_coverage_20261110_SC3_v11',
    'maria390_B152_B175_integrated_final_review_v1.json':'maria305_B176_B195_integrated_final_review_v1.json',
    'work/maria390_B152_B175_release_v1':'work/maria305_B176_B195_release_v1',
    "len(prior['missing']) == 2402":"len(prior['missing']) == 2012",
    'Maria_SC3_B152_B175_clean_20261109':'Maria_SC3_B176_B195_clean_20261110',
    "doc['all390_individual_five_gates_pass']":"doc['all305_individual_five_gates_pass']",
    'len(fresh) == 390':'len(fresh) == 305','len(set(added)) == 390':'len(set(added)) == 305',
    'len(keys) == 3117 and len(missing) == 2012':'len(keys) == 3422 and len(missing) == 1707',
    'previous_exact_bindings_reused=2727,new_exact_bindings=390':'previous_exact_bindings_reused=3117,new_exact_bindings=305',
    'SC3 census:3117 exact reviewed objects,2012 remaining':'SC3 census:3422 exact reviewed objects,1707 remaining',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-incremental-source-position-census-complete-retained-inventory','exec'),globals())
