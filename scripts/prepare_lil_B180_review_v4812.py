"""Measure B180's actual per-path differences without importing B179 assertions."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B180_review_tools_v4812')
if __name__=='__main__':
    assert not ROOT.exists()
    original=Path('scripts/review_lil_B179_actual_v4743.py').read_text(encoding='utf-8')
    a=original.index('    timings=');b=original.index('    selections.extend',a)
    block='''    shared=lambda v:{r['original_source_offset']:r for r in v['selected_B22_command_pairs'] if 'original_source_offset' in r}
    before,after_commands=map(shared,actual['versions'])
    timings=[dict(source=before[at],English=after_commands[at]) for at in sorted(before.keys()&after_commands.keys())
        if (before[at]['start'],before[at]['returned'])!=(after_commands[at]['start'],after_commands[at]['returned'])]
    conditional_only=dict(clean=sorted(before.keys()-after_commands.keys()),English=sorted(after_commands.keys()-before.keys()))
    for v in actual['versions']:
        assert len(v['selected_intervals'])==11 and v['single_source_end572_actually_reached']
        assert len(v['source_A000'])==len(v['source_C200'])==1
        assert v['selected_B22_command_pairs'][-1]['result_words']==[0,0]
    holds={r['id']:r['holds'] for r in actual['actual_panels']}
    focus=[holds[key][0]['frame'] for key in ['DK4_MES_B180_R0005','DK4_MES_B180_R0028','DK4_MES_B180_R0038','DK4_MES_B180_R0073']]
    selections=[focus[:2],focus[2:],[after[0]['frame'],9001]]
'''
    tools=[derive('scripts/review_lil_B179_actual_v4743.py','scripts/review_lil_B180_actual_v4812.py',{
        original[a:b]:block,
        'B179':'B180','actual_review_v4743':'actual_review_v4812',
        'actual_v4742/actual_all14_progressive_FE_A000_and_single_end_no_C200':'actual_v4811c/actual_all11_progressive_FE_RNG_effect_C200_and_single_end',
        'display_fixture_v4739':'display_fixture_v4808','display_v4741':'display_v4810',
        "actual['complete_matching_observations']==14":"actual['complete_matching_observations']==11",
        "len(actual['review_sheets'])==3":"len(actual['review_sheets'])==2",
        'all14_complete_held_planes_and_source_paired_regions_match':'all11_complete_held_planes_and_source_paired_regions_match',
        'all14_speeches13_progressive1_impersonal_FE_actually_observed':'all11_speeches10_progressive1_impersonal_FE_actually_observed',
        'source_A0008_single_end508_actually_executed_no_C200=True,actual25_of25_stored_fixture_commands_selected=True':
        'source_selected_effect_C200_single_end572_actually_executed=True,actual_conditional_paths_verified=True,conditional_only_source_offsets=conditional_only,observed_random_path_difference=actual[\'observed_random_path_difference\']',
        'source_event179_natural_eligibility':'source_event180_natural_eligibility',
        "session_id=5678":"session_id=41140","session_id=35045":"session_id=20129",
        'paired_all115_samples25_commands14_planes_and_final_state_analysis':'paired_all115_samples_conditional_commands11_planes_and_final_state_analysis',
        'complete_panels=14':'complete_panels=11'}))]
    ROOT.mkdir(parents=True);save(ROOT/'prepared_review.json',dict(tools=tools,
        cross_path_differences_measured_not_forced_equal=True,full_goal_complete=False))
