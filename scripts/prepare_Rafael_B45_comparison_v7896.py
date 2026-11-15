"""Source-lock the existing full state/RGB comparison to the paired B45 observations."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_comparison_tools_v7896');assert not root.exists()
    result=derive('scripts/measure_papal_trade_scene_pairs_v7651b.py','scripts/measure_Rafael_B45_pairs_v7896.py',{
        'work/analysis/papal_trade_actual_comparison_v7651b':'work/analysis/Rafael_B45_actual_comparison_v7896',
        'work/analysis/papal_trade_actual_v7650/four_complete_scene_captures72_speech_occurrences_exact_body_headers_andnormal_returns.json':
        'work/analysis/Rafael_B45_actual_v7895b/paired12_source_English_actual_body_name_FE_branch_andnormal_return_audit.json',
        "sheet=Image.new('RGB',(1536,820)":"sheet=Image.new('RGB',(1536,410)",
        'for route in [0,1]:':'for route in [0]:',
        'canonical_clean_offset':'canonical_source_offset',
        'frames[0]==8170':'frames[0]==6730',
        'all18_whole_upper_scene_portrait_andheader_RGB_equal':'all12_whole_upper_scene_portrait_andheader_RGB_equal',
        'scene_pairs=18':'scene_pairs=12',
        'two_routes_unmasked_return_midpoint_final_source_English_pairs.png':'Rafael_unmasked_return_midpoint_final_source_English_pairs.png',
        '36_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGBl_limits.json':'12_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json',
        'all36_source_English_upper_scene_portrait_complete_header_pairs_equal':'all12_source_English_upper_scene_portrait_complete_header_pairs_equal',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        original_native_high_constants_complete_snapshot_actor_getter_component_andunmasked_RGB_checks_preserved=True,
        source_English_timing_andRNG_differences_recorded_not_retimed_orhidden=True,
        FE_absent_nameplate_included_in_whole_upper_pane_comparison=True,
        no_new_emulator_runs_orprose_credit=True,new_credit=0,full_goal_complete=False))
