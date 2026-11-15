"""Prepare the same-context B200 English fixture and complete paired glyph audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B200_English_capture_tools_v5858')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B199_English_fixture_v5805.py','scripts/research_lil_B200_English_fixture_v5859.py',{
        'B199':'B200','prepare_lil_B199_reference_tools_v5796':'prepare_lil_B200_reference_tools_v5850',
        'English_fixture_v5805':'English_fixture_v5859','English_v5805':'English_v5859',
        'source_fixture_v5780':'source_fixture_v5835','source_fixture_v5781':'source_fixture_v5836',
        'English_fixture_v5806':'English_fixture_v5860','English_run_v5806':'English_run_v5860','English_v5806':'English_v5860',
        'source_run_v5781':'source_run_v5836','source_v5781':'source_v5836',
        'bank[199]':'bank[200]','source_block=199':'source_block=200',
        'assert len(bank[199])==1116 and end==1114 and bank[199][end:]==bytes(2)':'assert len(bank[200])==end==828',
        'len(native)==47 and len(commands)==56 and len(speeches)==31':'len(native)==31 and len(commands)==40 and len(speeches)==19',
        'all56_stored_fixture_commands':'all40_stored_fixture_commands',
        'all47_source_commands_plus9_initializers_retained_without_omission':'all31_source_commands_plus9_initializers_retained_without_omission',
        'not_natural_event199_activation':'not_natural_event200_activation',
        '47 original+9 initializer commands,31 speech objects,no predicates':'31 original+9 initializer commands,19 speech objects,no predicates'})]
    tools.append(derive('scripts/audit_lil_B199_actual_v5807.py','scripts/audit_lil_B200_actual_v5861.py',{
        'B199':'B200','actual_v5807':'actual_v5861','source_fixture_v5780':'source_fixture_v5835',
        'English_fixture_v5805':'English_fixture_v5859','source_run_v5781':'source_run_v5836','English_run_v5806':'English_run_v5860',
        'fonts_v5792/all31_progressive_FE_native_planes_and248_alignment_cases':'fonts_v5848/all19_progressive_FE_native_planes_and152_alignment_cases',
        'all47_source_commands_retained':'all31_source_commands_retained',
        '[5,9,12,16,19,23,27,31,34,37,40,43,47,50,54,58,62,66,70,73,77,81,84,88,91,95,99,103,107,111,115]':
        '[5,9,13,17,21,25,29,33,37,40,44,47,50,54,58,62,65,69,72]',
        "pairs[-1]['source_offset']==1162":"pairs[-1]['source_offset']==926",
        "assert len(actual)==31 and sum(r['prefix']==254 for r in actual)==1":"assert len(actual)==19 and sum(r['prefix']==254 for r in actual)==2",
        'thirty_one_actual_panels_source_matched_controls_and_complete_native_holds':'nineteen_actual_panels_source_matched_controls_and_complete_native_holds',
        'actual_unique_speech_panels=31':'actual_unique_speech_panels=19',
        'all47_source_commands_and9_initializers_stored':'all31_source_commands_and9_initializers_stored',
        'same_observed_source_path_original_results_no_predicates_and_end1162':'same_observed_source_path_original_results_no_predicates_and_end926',
        'no_natural_event199_activation':'no_natural_event200_activation','panels=31':'panels=19',
        "        versions.append(dict(case=case,command_pairs=pairs":"        assert len(pairs)==40\n        versions.append(dict(case=case,command_pairs=pairs"}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_English_fixture_and_actual_audit_tools.json',dict(tools=tools,
        source_boot_reused_not_repeated=True,expected_source_speeches=19,expected_commands=40,source_predicates=0,
        original_inputs_and_source_conditions_roster_funds_RNG_unforced=True,
        all_differences_measured_without_inheriting_B199_timing_or_PRNG_results=True,
        Stranger_label_target_not_applied=True,no_new_ROM_or_run_or_review_credit_yet=True,full_goal_complete=False))
    print('B200 English fixture and19-panel paired actual audit prepared. Japanese boot reused;no forced state.')
