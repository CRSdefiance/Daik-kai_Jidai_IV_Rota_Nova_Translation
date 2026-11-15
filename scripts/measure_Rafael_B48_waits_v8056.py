"""Measure original-command RNG phases andkeep all actual later differences;no complete causal claim."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.measure_Rafael_B46_waits_v7951 import distance,phase
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_waits_v8056')
ACTUAL=Path('work/analysis/Rafael_B48_actual_v8053/paired_source_English_observed_path_complete_pages_names_andR347_transition.json')
COMPARE=Path('work/analysis/Rafael_B48_actual_comparison_v8054/78_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json')
PRIOR=Path('work/analysis/Rafael_B46_waits_v7951/both_choices_original_wait_code_measured_RNG_phases_andlater_limits.json')
if __name__=='__main__':
    assert not ROOT.exists();actual,comparison,prior=map(read,[ACTUAL,COMPARE,PRIOR])
    assert not actual['unresolved'] and len(comparison['groups'])==1
    source,english=[next(g for g in actual['groups'] if g['version']==v) for v in ['clean_Japanese','English']]
    pair=comparison['groups'][0];rows=[]
    image=NdsImage.open(english['fixture']['research_ROM']);arm=image.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    parent=NdsImage.open('out/all_routes_combined_v8013_candidate.nds').read_file('/__arm9__.bin')
    assert arm==parent and sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    spans=[(0xC9D8C,0xC9DB4),(0xD9834,0xD9858)]
    assert all(arm[a:b]==clean[a:b] for a,b in spans)
    assert source['command_pairs'][0]['before_RNG']==english['command_pairs'][0]['before_RNG']==848781860
    for i,(a,b) in enumerate(zip(source['command_pairs'],english['command_pairs'],strict=True)):
        assert a['word']==b['word'] and a['canonical_source_offset']==b['canonical_source_offset'] and a['native_result']==b['native_result']
        rows.append(dict(index=i,word=a['word'],canonical_source_offset=a['canonical_source_offset'],
            source_duration=a['returned']-a['start'],English_duration=b['returned']-b['start'],
            source_RNG_steps=distance(a['before_RNG'],a['after_RNG']),English_RNG_steps=distance(b['before_RNG'],b['after_RNG']),
            before_English_phase=phase(a['before_RNG'],b['before_RNG']),after_English_phase=phase(a['after_RNG'],b['after_RNG'])))
    first=next(r for r in rows if r['before_English_phase'] or r['after_English_phase'])
    group=dict(route=0,same_initial_seed=848781860,all_command_measurements=rows,first_observed_phase_difference=first,
        R347_two_page_measurement=next(r for r in rows if r['canonical_source_offset']==next(s['source_reference']['header_offset'] for s in read('translations/rafael_B48_editorial_manuscript_v3.json')['records'] if s['source_record_index']==347)),
        exit_seeds=[source['command_pairs'][-1]['after_RNG'],english['command_pairs'][-1]['after_RNG']],
        exit_English_phase=rows[-1]['after_English_phase'],final_seeds=pair['final_PRNG_seeds'],
        final_English_phase=phase(*pair['final_PRNG_seeds']),source_English_exits=pair['source_English_exits'],
        command_difference_rows=len(pair['command_comparison_differences']),duration_difference_rows=len(pair['duration_differences']),
        five_component_equality=pair['five_native_component_equality'],whole_actors_equal=pair['whole_actors_equal'],
        raw_calendar_measurements=pair['raw_calendars_no_invented_date_interpretation'],
        later_RGB_differences=len(pair['later_RGB_differences']),later_samples=pair['later_sample_count'])
    assert pair['all_original_initializer_andexchange_results_equal'] and pair['all_UI_request_words_equal']
    ROOT.mkdir(parents=True)
    save(ROOT/'original_wait_code_measured_R347_page_RNG_phases_andlater_limits.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),comparison=str(COMPARE),comparison_sha256=sha(COMPARE.read_bytes()),
        groups=[group],LCG=dict(multiplier=1103515245,increment=12345,modulus=4294967296,bounded_step_search=100000),
        current_clean_equal_code_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        earlier_discarded_wait_contract=str(PRIOR),earlier_discarded_wait_contract_sha256=sha(PRIOR.read_bytes()),
        earlier_contract_reused_only_for_exact_unchanged_code_not_fresh_every_call_causal_trace=True,
        original_extra_English_page_wait_observed_with_identical_ordinary_inputs=True,
        observed_phase_differences_consistent_with_original_wait_timing_not_complete_causal_proof=True,
        actual_selected_command_results_UI_requests_portraits_andheaders_equal=True,
        actual_later_persistent_objects_actors_andall_sampled_RGB_differ_models_state_tasks_calendar_equal=True,
        exact_RNG_state_future_random_outcomes_orfull_simulation_equality_NOT_verified=True,
        no_input_retiming_seed_result_condition_orRAM_forcing_no_new_emulator_runs=True,
        all_raw_measurements_kept_for_later_older_record_technical_reaudit=True,
        incidental_following_prose_captures_have_no_new_editorial_credit=True,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,COMPARE,PRIOR,Path(distance.__code__.co_filename),Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print({k:group[k] for k in ['first_observed_phase_difference','R347_two_page_measurement','exit_English_phase','final_English_phase','later_RGB_differences','later_samples','raw_calendar_measurements']})
