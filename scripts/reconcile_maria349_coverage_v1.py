"""Extend the exact clean-source census by349 positions without replaying old checks."""
from scripts.reconcile_maria359_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/story_source_coverage_20261110_SC3_v15':'work/story_source_coverage_20261110_SC3_v16',
    'work/story_source_coverage_20261110_SC3_v14':'work/story_source_coverage_20261110_SC3_v15',
    'maria359_B253_B274':'maria349_B275_B285',
    "len(prior['missing']) == 1023":"len(prior['missing']) == 664",
    'Maria_SC3_B253_B274_clean_20261110':'Maria_SC3_B275_B285_clean_20261110',
    "doc['all359_individual_five_gates_pass']":"doc['all349_individual_five_gates_pass']",
    'len(fresh) == 359':'len(fresh) == 349',
    'len(set(added)) == 359':'len(set(added)) == 349',
    'len(keys) == 4465 and len(missing) == 664':'len(keys) == 4814 and len(missing) == 315',
    'previous_exact_bindings_reused=4106,new_exact_bindings=359':'previous_exact_bindings_reused=4465,new_exact_bindings=349',
    'SC3 census:4465 exact reviewed objects,664 remaining':'SC3 census:4814 exact reviewed objects,315 remaining',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-incremental-exact-source-position-census','exec'),globals())
