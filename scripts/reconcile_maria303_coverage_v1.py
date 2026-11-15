"""Extend the exact SC3 source census with303 registered bindings;reuse native inventory."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(Path('scripts/reconcile_maria301_coverage_v1.py').read_text(encoding='utf-8'), {
    'work/story_source_coverage_20261109_SC3_v2': 'work/story_source_coverage_20261109_SC3_v6',
    'work/story_source_coverage_20261109_SC3_v1': 'work/story_source_coverage_20261109_SC3_v5',
    'maria301_integrated_final_review_v1.json': 'maria303_integrated_final_review_v1.json',
    'work/maria301_release_v1': 'work/maria303_release_v1',
    "len(prior['missing']) == 4932": "len(prior['missing']) == 4035",
    "doc['all301_individual_five_gates_pass']": "doc['all303_individual_five_gates_pass']",
    'Maria_SC3_B0_B32_clean_20261109': 'Maria_SC3_B58_B70_clean_20261109',
    'len(fresh) == 301': 'len(fresh) == 303', 'len(set(added)) == 301': 'len(set(added)) == 303',
    'len(keys) == 498 and len(missing) == 4631': 'len(keys) == 1397 and len(missing) == 3732',
    'previous_exact_bindings_reused=197,new_exact_bindings=301': 'previous_exact_bindings_reused=1094,new_exact_bindings=303',
    'SC3 census:498 exact reviewed objects,4631 remaining': 'SC3 census:1397 exact reviewed objects,3732 remaining',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-clean-source-position-andledger-reconciliation303', 'exec'), globals())
