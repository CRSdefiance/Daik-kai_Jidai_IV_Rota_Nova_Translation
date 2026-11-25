"""Extend the exact Maria source census by321 positions without replaying inventory."""
from scripts.reconcile_maria305_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'work/story_source_coverage_20261110_SC3_v12': 'work/story_source_coverage_20261110_SC3_v13',
    'work/story_source_coverage_20261110_SC3_v11': 'work/story_source_coverage_20261110_SC3_v12',
    'maria305_B176_B195_integrated_final_review_v1.json': 'maria321_B196_B215_integrated_final_review_v1.json',
    'work/maria305_B176_B195_release_v1': 'work/maria321_B196_B215_release_v1',
    "len(prior['missing']) == 2012": "len(prior['missing']) == 1707",
    'Maria_SC3_B176_B195_clean_20261110': 'Maria_SC3_B196_B215_clean_20261110',
    "doc['all305_individual_five_gates_pass']": "doc['all321_individual_five_gates_pass']",
    'len(fresh) == 305': 'len(fresh) == 321',
    'len(set(added)) == 305': 'len(set(added)) == 321',
    'len(keys) == 3422 and len(missing) == 1707': 'len(keys) == 3743 and len(missing) == 1386',
    'previous_exact_bindings_reused=3117,new_exact_bindings=305':
        'previous_exact_bindings_reused=3422,new_exact_bindings=321',
    'SC3 census:3422 exact reviewed objects,1707 remaining':
        'SC3 census:3743 exact reviewed objects,1386 remaining',
})

if __name__ == '__main__':
    exec(compile(source,__file__+'::same-incremental-source-position-census-complete-retained-inventory','exec'),globals())
