"""Credit the one original source position for the two-panel paragraph; reuse the clean census."""
from scripts.reconcile_maria270_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    "ROOT = Path('work/story_source_coverage_20261109_SC3_v3')":"ROOT = Path('work/story_source_coverage_20261109_SC3_v4')",
    "PRIOR = Path('work/story_source_coverage_20261109_SC3_v2/coverage.json')":"PRIOR = Path('work/story_source_coverage_20261109_SC3_v3/coverage.json')",
    'maria270_integrated_final_review_v1.json':'maria_B50_integrated_final_review_v1.json',
    'work/maria270_release_v1':'work/maria_B50_release_v1',
    "len(prior['missing']) == 4631":"len(prior['missing']) == 4361",
    'all270_individual_five_gates_pass':'all16_individual_five_gates_pass',
    'Maria_SC3_B37_B49_display_20261109':'Maria_SC3_B50_FE_research_20261109',
    'len(fresh) == 270':'len(fresh) == 16','len(set(added)) == 270':'len(set(added)) == 16',
    'len(keys) == 768 and len(missing) == 4361':'len(keys) == 784 and len(missing) == 4345',
    'previous_exact_bindings_reused=498,new_exact_bindings=270':'previous_exact_bindings_reused=768,new_exact_bindings=16',
    'SC3 census:768 exact reviewed objects,4361 remaining':'SC3 census:784 exact reviewed objects,4345 remaining',
})
exec(compile(source,__file__+'::same-all5129-clean-positions-no-duplicate-pagination-credit','exec'),globals())
