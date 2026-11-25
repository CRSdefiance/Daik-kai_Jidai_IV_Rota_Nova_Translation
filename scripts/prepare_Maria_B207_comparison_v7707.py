"""Bind measured Maria returns andone-route sheet geometry; preserve all late-state differences."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_comparison_tools_v7707')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/measure_papal_trade_scene_pairs_v7651b.py','scripts/measure_Maria_B207_scene_pairs_v7707.py',{
        'papal_trade_actual_comparison_v7651b':'maria_B207_actual_comparison_v7707',
        'papal_trade_actual_v7650/four_complete_scene_captures72_speech_occurrences_exact_body_headers_andnormal_returns':'maria_B207_actual_v7706/Maria_two_complete_scene_captures36_occurrences_exact_body_headers_andnormal_returns',
        '(1536,820)':'(1536,410)','for route in [0,1]':'for route in [3]',
        'frames[0]==8170':'frames[0]==8780',
        'x,y=(i*2+j)*256,route*410':'x,y=(i*2+j)*256,0',
        'two_routes_unmasked_return_midpoint_final_source_English_pairs':'Maria_unmasked_return_midpoint_final_source_English_pairs',
        '36_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGBl_limits':'Maria18_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits',
        'all36_source_English_upper_scene_portrait_complete_header_pairs_equal':'all18_source_English_upper_scene_portrait_complete_header_pairs_equal',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_Maria_measured_comparison.json',dict(derivation=result,measured_first_late_frame8780_bound_to_actual_returns8696_8694=True,no_PRNG_offset_orother_native_high_constant_change=True,new_credit=0,full_goal_complete=False))
