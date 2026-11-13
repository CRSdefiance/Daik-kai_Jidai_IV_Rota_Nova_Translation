"""Keep terminal failed concurrent captures and use fresh serial output folders."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B197_serial_capture_tools_v5683b')
if __name__=='__main__':
    assert not ROOT.exists()
    buy=read('work/analysis/lil_B197_English_run_v5683_buy_reviewed_English/terminal.json')
    assert buy['terminal'] and buy['observer_host_slots_restored']
    partial=[]
    for path,session,reason in [('no_buy',45482,'MemoryError while saving frame'),('delegate',9879,'IndexError reading observer.pending;cause not established')]:
        run=Path('work/analysis/lil_B197_English_run_v5683_'+path+'_reviewed_English')
        assert not (run/'terminal.json').exists();plan=read(run/'run_plan.json');cap=Path(plan['capture_folder'])
        photos=sorted(cap.glob('frame_*_cold_boot.png'))
        partial.append(dict(path=path,tool_session_id=session,tool_terminal_exit_code=1,reason=reason,
            run_folder=str(run),capture_folder=str(cap),partial_photo_count=len(photos),last_partial_photo=None if not photos else str(photos[-1]),
            absent_success_terminal_or_completed_capture_not_counted_as_pass=True,
            original_run_plan_sha256=sha((run/'run_plan.json').read_bytes()),all_partial_files_preserved=True))
    tool=derive('scripts/run_lil_B197_English_fixture_v5683.py','scripts/run_lil_B197_English_fixture_v5683b.py',{
        'English_run_v5683':'English_run_v5683b','English_v5683_':'English_v5683b_'})
    ROOT.mkdir(parents=True);save(ROOT/'failed_handles_reaped_and_exact_input_serial_successor.json',dict(tool=tool,
        failed_concurrent_runs=partial,completed_buy_tool_session=43857,completed_buy_exit_code=0,
        unchanged_ROM_source_commands_input_frames_buttons_and_unforced_state=True,
        only_new_output_paths_no_gameplay_or_renderer_change=True,remaining_runs_must_be_serial=True,new_credit=0,full_goal_complete=False))
