"""Freeze complete source/English pixel,header,control,return andlate-state audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_confrontation_actual_tools_v7811')
ACTUAL='work/analysis/maria_confrontation_actual_v7811/two_scene_captures_actual_pages_headers_branches_returns.json'
if __name__=='__main__':
    assert not ROOT.exists();results=[]
    results.append(derive('scripts/audit_Maria_story_scenes_v7752c.py','scripts/audit_Maria_confrontation_actual_v7811.py',{
        'maria_story_actual_v7752c':'maria_confrontation_actual_v7811',
        'work/analysis/maria_story_scene_fixtures_v7749/six_complete_source_English_original_prelude_fixtures.json':
        'work/analysis/maria_confrontation_scene_fixtures_v7808/two_complete_source_English_original_prelude_fixtures.json',
        'maria_story_scene_runs_v7750':'maria_confrontation_scene_runs_v7809',
        'work/analysis/maria_B35_source_rightcell_v7753/67_source_native_pages8_name_planes_R65_actual_rightcell_bound.json':
        'work/analysis/maria_confrontation_source_name_planes_v7810/16_clean_source_native_pages3_complete_name_planes12_literal_alignments.json',
        'work/analysis/maria_story_stored_v7743/67_final_stored_targets268_alignments33_zero_ink_tails68_pages.json':
        'work/analysis/maria_confrontation_stored_v7803/16_final_stored_targets64_alignments11_zero_ink_tails16_pages.json',
        'work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json':
        'work/analysis/maria_confrontation_current_v7789/all16_complete_source_current_refs_before_new_English_manuscript.json',
        'assert width in [216,228]':'assert width==216',
        "if version=='English' and not (ascii_equal and cp_equal):":"if not (ascii_equal and cp_equal):",
        "gray_required=version=='English'":"gray_required=True",
        'for number in [34,108,35]:':'for number in [36]:',
        'six_scene_captures_actual_pages_headers_branches_returns_andunplayed_conditions.json':'two_scene_captures_actual_pages_headers_branches_returns.json',
        'all_six_jobs_terminal_andreaped':'both_jobs_terminal_andreaped',
        'source_Japanese_black_masks_verified_English_black_andperglyph_ASCII_CP932_gray_required':'source_andEnglish_black_andperglyph_ASCII_CP932_gray_masks_required',
        '[FIXTURES,FONT,STORED,CURRENT,RIGHTCELL,Path(__file__)]':'[FIXTURES,FONT,STORED,CURRENT,Path(__file__)]',
    }))
    results.append(derive('scripts/measure_Maria_story_scene_pairs_v7754.py','scripts/measure_Maria_confrontation_pair_v7812.py',{
        'maria_story_actual_comparison_v7754':'maria_confrontation_actual_comparison_v7812',
        'work/analysis/maria_story_actual_v7752c/six_scene_captures_actual_pages_headers_branches_returns_andunplayed_conditions.json':ACTUAL,
        'for number in [34,108,35]:':'for number in [36]:',
        'three_actual_pairs_measured_portraits_timing_RNG_states_RGB_limits.json':'one_actual_pair_measured_portraits_timing_RNG_states_RGB_limits.json',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivations=results,
        all_original_native_numeric_constants_readonly_trace_branch_extent_return_carry_andheader_guards_preserved=True,
        all_B36_source_andEnglish_planes216px_no_new_source_geometry_exception=True,
        source_andEnglish_complete_black_ASCII_gray_andCP932_gray_required=True,
        unchanged_original_state_actor_calendar_RNG_andlate_RGB_getters_preserved=True,
        no_natural_activation_fullroute_orcausal_equivalence_claim=True,new_credit=0,full_goal_complete=False))
