"""Reconcile the complete native Lil source census."""

from scripts.reconcile_lil254_coverage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "Extend the exact SC3 census with the301 newly registered bindings; no native inventory replay.": "Complete the exact Lil SC2 census with the final 261 registered bindings.",
    "work/story_source_coverage_20261110_SC2_v7": "work/story_source_coverage_20261110_SC2_v8",
    "work/story_source_coverage_20261110_SC2_v6/coverage.json": "work/story_source_coverage_20261110_SC2_v7/coverage.json",
    "lil254_B312_B319": "lil261_B323_B335",
    "Lil_SC2_B312_B319": "Lil_SC2_B323_B335",
    "all254_individual": "all261_individual",
    "len(prior['missing']) == 515": "len(prior['missing']) == 261",
    "len(fresh) == 254": "len(fresh) == 261",
    "len(set(added)) == 254": "len(set(added)) == 261",
    "len(keys) == 6459 and len(missing) == 261": "len(keys) == 6720 and not missing",
    "previous_exact_bindings_reused=6205,new_exact_bindings=254": "previous_exact_bindings_reused=6459,new_exact_bindings=261",
    "SC2 census:6459 exact reviewed objects,261 remaining; all 6720 source positions checked,zero duplicate credit.": "SC2 census: 6720 exact reviewed objects, zero remaining and zero duplicate credit.",
    "    print('First remaining exchanges:',[(g['block'],len(g['records'])) for g in groups[:16]])": "    assert not groups",
})

if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
