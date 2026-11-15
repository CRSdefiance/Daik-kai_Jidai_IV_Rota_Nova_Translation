"""Prepare measured B49 comparison without carrying forward B48 outcome assumptions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B49_measurement_tools_v8108')
if __name__=='__main__':
    assert not ROOT.exists()
    common={
        'Rafael_B48_actual_v8053/paired_source_English_observed_path_complete_pages_names_andR347_transition.json':'Rafael_B49_actual_v8107/paired_source_English_observed_path_complete_pages_names_C281_andreturn.json',
        'Rafael_B48_actual_comparison_v8054':'Rafael_B49_actual_comparison_v8108',
        '78_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json':'all_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json',
    }
    a=derive('scripts/measure_Rafael_B48_pairs_v8054.py','scripts/measure_Rafael_B49_pairs_v8108.py',{
        **common,"frames[-1]==40001":"frames[-1]==24001",
        'all78_whole_upper_scene_portrait_andheader_RGB_equal':'all_observed_whole_upper_scene_portrait_andheader_RGB_equal',
        'all78_source_English_upper_scene_portrait_complete_header_pairs_equal':'all_observed_source_English_upper_scene_portrait_complete_header_pairs_equal',
    })
    old="R347_two_page_measurement=next(r for r in rows if r['canonical_source_offset']==next(s['source_reference']['header_offset'] for s in read('translations/rafael_B48_editorial_manuscript_v3.json')['records'] if s['source_record_index']==347))"
    b=derive('scripts/measure_Rafael_B48_waits_v8056.py','scripts/measure_Rafael_B49_waits_v8109.py',{
        **common,'Rafael_B48_waits_v8056':'Rafael_B49_waits_v8109',
        'out/all_routes_combined_v8013_candidate.nds':'out/all_routes_combined_v8066_candidate.nds',
        "next(r for r in rows if r['before_English_phase'] or r['after_English_phase'])":"next((r for r in rows if r['before_English_phase'] or r['after_English_phase']),None)",
        old:"C281_original_command_measurement=next(r for r in rows if r['word']==0xC281)",
        'original_wait_code_measured_R347_page_RNG_phases_andlater_limits.json':'original_wait_code_measured_C281_RNG_phases_andlater_limits.json',
        'original_extra_English_page_wait_observed_with_identical_ordinary_inputs':'original_single_page_waits_andC281_measured_with_identical_ordinary_inputs',
        'actual_later_persistent_objects_actors_andall_sampled_RGB_differ_models_state_tasks_calendar_equal=True':"actual_later_component_equality=pair['five_native_component_equality'],actual_later_whole_actor_equality=pair['whole_actors_equal'],actual_later_RGB_differences=len(pair['later_RGB_differences']),actual_later_RGB_samples=pair['later_sample_count']",
        "'R347_two_page_measurement'":"'C281_original_command_measurement'",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[a,b])
    print('Prepared B49 actual state/RGB/timing/RNG measurements; outcomes will be measured.')
