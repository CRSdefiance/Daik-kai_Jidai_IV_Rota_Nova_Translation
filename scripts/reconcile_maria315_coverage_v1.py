"""Complete the exact native SC3 census without replaying previously credited reviews."""
from scripts.reconcile_maria349_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'work/story_source_coverage_20261110_SC3_v16': 'work/story_source_coverage_20261110_SC3_v17',
    'work/story_source_coverage_20261110_SC3_v15': 'work/story_source_coverage_20261110_SC3_v16',
    'maria349_B275_B285': 'maria315_B286_B302',
    "len(prior['missing']) == 664": "len(prior['missing']) == 315",
    'Maria_SC3_B275_B285_clean_20261110': 'Maria_SC3_B286_B302_clean_20261110',
    "doc['all349_individual_five_gates_pass']": "doc['all315_individual_five_gates_pass']",
    'len(fresh) == 349': 'len(fresh) == 315',
    'len(set(added)) == 349': 'len(set(added)) == 315',
    'len(keys) == 4814 and len(missing) == 315': 'len(keys) == 5129 and len(missing) == 0',
    'previous_exact_bindings_reused=4465,new_exact_bindings=349': 'previous_exact_bindings_reused=4814,new_exact_bindings=315',
    'SC3 census:4814 exact reviewed objects,315 remaining': 'SC3 census:5129 exact reviewed objects,0 remaining',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-incremental-exact-source-position-census', 'exec'), globals())
