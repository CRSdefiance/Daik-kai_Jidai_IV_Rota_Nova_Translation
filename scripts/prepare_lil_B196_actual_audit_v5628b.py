"""Include already captured settled highlight frames; preserve the strict first audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B196_actual_tools_v5628b')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/audit_lil_B196_actual_v5628.py','scripts/audit_lil_B196_actual_v5628b.py',{
        "ROOT=Path('work/analysis/lil_B196_actual_v5628')":"ROOT=Path('work/analysis/lil_B196_actual_v5628b')",
        "interval['start']+35<frame":"interval['start']+30<frame",
        "                visible=pic.getpixel((104,268+20*option))==(0,165,172)":
        "                sourcepic=photosets[path,'clean_Japanese'][frame][1]\n                colors=[pic.getpixel((104,268+20*i)) for i in range(2)]\n                assert colors==[sourcepic.getpixel((104,268+20*i)) for i in range(2)]\n                assert all(color in ([(0,165,172),(205,198,180)] if i==option else [(205,198,180)]) for i,color in enumerate(colors))\n                visible=colors[option]==(0,165,172)",
        'complete_Buy_Pass_native_foreground_masks_equal=True,selected_highlight_matches_return_when_visible=visible':
        'complete_Buy_Pass_native_foreground_masks_equal=True,paired_Japanese_background_and_original_blink_phase_equal=True,selected_highlight_matches_return_when_visible=visible'})
    ROOT.mkdir(parents=True);save(ROOT/'settled_capture_window_correction.json',dict(tool=result,
        original_audit='scripts/audit_lil_B196_actual_v5628.py',original_output='work/analysis/lil_B196_actual_v5628/three_paired_paths_native_panels_menus_and_separate_endings.json',
        finding='Seven menus had complete native labels after age35 but original selected highlight blinked off at the sparse later capture;already stored age31-35 frames show settled labels and correct Pass highlight.',
        original_DOWN_frames_after_entry=[30,31,32,33,34],new_hold_window_excludes_entry_through_age30=True,
        complete_native_foreground_and_visible_correct_returned_option_remain_required=True,
        both_option_backgrounds_now_also_match_paired_Japanese_and_source_blink_phase=True,
        no_new_ROM_input_run_capture_retiming_mask_or_gameplay_change=True,full_goal_complete=False))
