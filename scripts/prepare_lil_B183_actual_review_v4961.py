"""Prepare measured B183 review without assuming equal timing,RNG or final state."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B183_actual_review_tools_v4961')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/review_lil_B181_actual_v4862.py','scripts/review_lil_B183_actual_v4961.py',{
        'B181':'B183','actual_review_v4862':'actual_review_v4961','actual_v4861/actual_all10':'actual_v4960/actual_all25',
        'display_fixture_v4857':'display_fixture_v4957','display_v4860':'display_v4959',
        "actual['complete_matching_observations']==10":"actual['complete_matching_observations']==25",
        "len(actual['review_sheets'])==2":"len(actual['review_sheets'])==5",
        '9001':'11001','len(comparisons)==115':'len(comparisons)==149',
        "len(v['selected_B22_command_pairs'])==22 and len(v['selected_intervals'])==10":"len(v['selected_B22_command_pairs'])==37 and len(v['selected_intervals'])==25",
        'single_source_end392':'single_source_end952',"v['source_C200']['original_source_offset']==390":"v['source_C200']['original_source_offset']==950",
        "['DK4_MES_B181_R0023','DK4_MES_B181_R0027','DK4_MES_B181_R0035','DK4_MES_B181_R0039']":
        "['DK4_MES_B183_R0035','DK4_MES_B183_R0049','DK4_MES_B183_R0053','DK4_MES_B183_R0057','DK4_MES_B183_R0095']",
        'selections=[focus[:2],focus[2:],[after[0][\'frame\'],9001]]':
        "selections=[focus[:2],focus[2:4],[focus[4],after[0]['frame']],[11001]]",
        'all115_sampled':'all149_sampled','all10_complete':'all25_complete','all10_speeches9_progressive1':'all25_speeches23_progressive2',
        'source_A0008_C200390_single_end392':'source_A0008_C200950_single_end952','actual22_of22':'actual37_of37','source_event181':'source_event183',
        "reaped_tool_sessions=[dict(case='clean_Japanese',session_id=37983,exit_code=0),dict(case='reviewed_English',session_id=61146,exit_code=0)]":
        "terminal_reports=[dict(case=f['case'],path='work/analysis/lil_B183_display_run_v4959_'+f['case']+'/terminal.json',receipt=read('work/analysis/lil_B183_display_run_v4959_'+f['case']+'/terminal.json')) for f in fixture['fixtures']]",
        'paired_all115_samples22_commands10_planes':'paired_all149_samples37_commands25_planes','complete_panels=10':'complete_panels=25'
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_review.json',dict(tool=tool,expected_complete_panels=25,source_commands=28,stored_fixture_commands=37,
        frames_per_boot=11001,expected_captured_frame_pairs=149,no_actual_equality_assumed=True,
        focus_includes_corrected_question_service_Slam_return_to_shopkeeper_and_closing_forecast=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared B183 measured149-frame comparison and full-screen views;actual results still pending.')
