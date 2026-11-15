"""Measure only changed scene pairs; unchanged B35 comparisons remain retained."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_final_comparison_tools_v7767');assert not root.exists()
    d=derive('scripts/measure_Maria_story_scene_pairs_v7754.py','scripts/measure_Maria_story_final_pairs_v7767.py',{
        'maria_story_actual_comparison_v7754':'maria_story_final_comparison_v7767',
        'work/analysis/maria_story_actual_v7752c/six_scene_captures_actual_pages_headers_branches_returns_andunplayed_conditions.json':'work/analysis/maria_story_final_actual_binding_v7766/six_final_v3_actual_groups_two_fresh_four_exact_reused.json',
        'for number in [34,108,35]:':'for number in [34,108]:',
        'three_actual_pairs_measured_portraits_timing_RNG_states_RGB_limits.json':'two_final_pairs_measured_portraits_timing_RNG_states_RGB_limits.json',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=d,
        exact_original_native_state_getters_actors_RNG_andRGB_comparison_guards_preserved=True,
        no_repeat_of_exact_unchanged_B35_measurements=True,new_credit=0,full_goal_complete=False))
