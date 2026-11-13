"""Extend the exact source census by359 positions; preserve all prior inventory credit."""
from scripts.reconcile_maria363_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/story_source_coverage_20261110_SC3_v14':'work/story_source_coverage_20261110_SC3_v15',
    'work/story_source_coverage_20261110_SC3_v13':'work/story_source_coverage_20261110_SC3_v14',
    'maria363_B216_B252':'maria359_B253_B274',
    "len(prior['missing']) == 1386":"len(prior['missing']) == 1023",
    'Maria_SC3_B216_B252_clean_20261110':'Maria_SC3_B253_B274_clean_20261110',
    "doc['all363_individual_five_gates_pass']":"doc['all359_individual_five_gates_pass']",
    'len(fresh) == 363':'len(fresh) == 359',
    'len(set(added)) == 363':'len(set(added)) == 359',
    'len(keys) == 4106 and len(missing) == 1023':'len(keys) == 4465 and len(missing) == 664',
    'previous_exact_bindings_reused=3743,new_exact_bindings=363':'previous_exact_bindings_reused=4106,new_exact_bindings=359',
    'SC3 census:4106 exact reviewed objects,1023 remaining':'SC3 census:4465 exact reviewed objects,664 remaining',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-incremental-exact-source-position-census','exec'),globals())
