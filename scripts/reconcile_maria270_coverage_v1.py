"""Extend the existing source-position census with only the 270 new registered bindings."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/reconcile_maria301_coverage_v1.py').read_text(encoding='utf-8'),{
    "ROOT = Path('work/story_source_coverage_20261109_SC3_v2')":"ROOT = Path('work/story_source_coverage_20261109_SC3_v3')",
    "PRIOR = Path('work/story_source_coverage_20261109_SC3_v1/coverage.json')":"PRIOR = Path('work/story_source_coverage_20261109_SC3_v2/coverage.json')",
    'maria301_integrated_final_review_v1.json':'maria270_integrated_final_review_v1.json',
    'work/maria301_release_v1':'work/maria270_release_v1',
    "len(prior['missing']) == 4932":"len(prior['missing']) == 4631",
    'all301_individual_five_gates_pass':'all270_individual_five_gates_pass',
    'Maria_SC3_B0_B32_clean_20261109':'Maria_SC3_B37_B49_display_20261109',
    'len(fresh) == 301':'len(fresh) == 270','len(set(added)) == 301':'len(set(added)) == 270',
    'len(keys) == 498 and len(missing) == 4631':'len(keys) == 768 and len(missing) == 4361',
    'previous_exact_bindings_reused=197,new_exact_bindings=301':'previous_exact_bindings_reused=498,new_exact_bindings=270',
    'SC3 census:498 exact reviewed objects,4631 remaining':'SC3 census:768 exact reviewed objects,4361 remaining',
})
exec(compile(source,__file__+'::same-exact-clean-source-position-reconciliation-without-native-replay','exec'),globals())
