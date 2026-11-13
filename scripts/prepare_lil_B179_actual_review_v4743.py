"""Prepare fresh measurements and all differing full screens for B179."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_actual_review_tools_v4743')
assert not ROOT.exists()
tool=derive('scripts/review_lil_B178_actual_v4695.py','scripts/review_lil_B179_actual_v4743.py',{
    'B178':'B179','actual_review_v4695':'actual_review_v4743','actual_v4694':'actual_v4742',
    'actual_all13_progressive_FE_A000_C200_and_single_end':'actual_all14_progressive_FE_A000_and_single_end_no_C200',
    'display_fixture_v4691':'display_fixture_v4739','display_v4693':'display_v4741',
    "actual['complete_matching_observations']==13":"actual['complete_matching_observations']==14",
    "len(v['selected_intervals'])==13":"len(v['selected_intervals'])==14",
    'single_source_end490_actually_reached':'single_source_end508_actually_reached',
    "assert v['source_A000'][0]['result_words']==v['source_C200']['result_words']==[3,0]":
        "assert v['source_A000'][0]['result_words']==[3,0] and v['source_C200']==[]",
    "focus=[holds['DK4_MES_B178_R0032'][0]['frame'],holds['DK4_MES_B178_R0051'][0]['frame']]":
        "focus=[holds[key][0]['frame'] for key in ['DK4_MES_B179_R0031','DK4_MES_B179_R0039','DK4_MES_B179_R0050','DK4_MES_B179_R0054']]",
    "selections=[focus,[after[0]['frame'],9001]]":"selections=[focus[:2],focus[2:],[after[0]['frame'],9001]]",
    "if differences:selections.append([r['frame'] for r in differences[:2]])":
        "selections.extend([[r['frame'] for r in differences[start:start+2]] for start in range(0,len(differences),2)])",
    'all13_complete_held_planes':'all14_complete_held_planes',
    'all13_speeches12_progressive1':'all14_speeches13_progressive1',
    'source_A0008_C200488_single_end490_actually_executed':'source_A0008_single_end508_actually_executed_no_C200',
    'source_event178_natural_eligibility':'source_event179_natural_eligibility',
    'session_id=79256':'session_id=5678','session_id=95847':'session_id=35045',
    'paired_all115_samples25_commands13_planes':'paired_all115_samples25_commands14_planes',
    'complete_panels=13':'complete_panels=14',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,all_measured_postscene_RGB_differences_get_complete_paired_screens=True,
    no_inherited_timing_RGB_state_or_PRNG_outcome=True,source_C200_absent=True,full_goal_complete=False))
