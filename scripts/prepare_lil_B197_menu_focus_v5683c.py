"""Capture original selection blink directly;do not retime or replace earlier evidence."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_menu_focus_tools_v5683c')
if __name__=='__main__':
    assert not ROOT.exists()
    actual=read('work/analysis/lil_B197_actual_v5684/three_paths_complete_native_panels_three_options_and_source_comparisons.json')
    assert actual['failures']==[dict(path='no_buy',menu=230,finding='No complete three-label masks with visibly correct returned option.')]
    assert actual['actual_unique_speech_panels']==21 and not actual['paired_nontext_region_differences'] and not actual['command_result_differences']
    tool=derive('scripts/run_lil_B197_English_fixture_v5683b.py','scripts/run_lil_B197_English_fixture_v5683c.py',{
        'English_run_v5683b':'English_run_v5683c','English_v5683b_':'English_v5683c_',
        "'--frames','13001'":"'--frames','4601'",
        "range(2350,13001,60)":"range(4320,4441,5)"})
    ROOT.mkdir(parents=True);save(ROOT/'one_missing_visible_highlight_focus.json',dict(tool=tool,
        reason='Prior full refusal run has correct actual result1 and complete labels at4390,but selection highlight is in its inactive blink phase;4330 is still in Down press transition.',
        original_ROM_inputs_frames_buttons_and_state_unmodified=True,only_capture_schedule_and_total_observation_frames_changed=True,
        original_full_run_result_and_normal_return_evidence_preserved=True,no_original_frames_masked_or_retimed=True,
        supplemental_run_stops_at4601_and_not_claimed_as_complete_scene=True,new_credit=0,full_goal_complete=False))
