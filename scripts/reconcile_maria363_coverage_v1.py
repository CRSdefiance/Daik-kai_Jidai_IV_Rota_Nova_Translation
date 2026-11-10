"""Extend the exact source census by363 positions without replaying old inventory."""
from scripts.reconcile_maria321_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(previous, {
    'work/story_source_coverage_20261110_SC3_v13':'work/story_source_coverage_20261110_SC3_v14',
    'work/story_source_coverage_20261110_SC3_v12':'work/story_source_coverage_20261110_SC3_v13',
    'maria321_B196_B215':'maria363_B216_B252',
    "len(prior['missing']) == 1707":"len(prior['missing']) == 1386",
    'Maria_SC3_B196_B215_clean_20261110':'Maria_SC3_B216_B252_clean_20261110',
    "doc['all321_individual_five_gates_pass']":"doc['all363_individual_five_gates_pass']",
    'len(fresh) == 321':'len(fresh) == 363',
    'len(set(added)) == 321':'len(set(added)) == 363',
    'len(keys) == 3743 and len(missing) == 1386':'len(keys) == 4106 and len(missing) == 1023',
    'previous_exact_bindings_reused=3422,new_exact_bindings=321':'previous_exact_bindings_reused=3743,new_exact_bindings=363',
    'SC3 census:3743 exact reviewed objects,1386 remaining':'SC3 census:4106 exact reviewed objects,1023 remaining',
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-incremental-exact-source-position-census','exec'),globals())
