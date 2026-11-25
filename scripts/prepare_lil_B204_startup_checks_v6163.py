"""Bind current startup comparison to the exact V6110-equivalent source boots."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_startup_tools_v6163')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/verify_lil_B203_startup_v6053.py','scripts/verify_lil_B204_startup_v6163.py',{
        'B203':'B204','startup_v6053':'startup_v6163','runs_v6052':'runs_v6162','combined_v6050':'combined_v6160','combined_v5998':'combined_v6110','V5998':'V6110','Current6050':'Current6160',
        "oldtp=Path('work/analysis/lil_B202_runs_v6000')/(case+'_terminal.json')":"oldtp=Path('work/analysis')/({'newgame':'shachihoko_runs_v6095','town':'shachihoko_runs_v6096'}[case])/(case+'_terminal.json')",
    })]
    tools.append(derive('scripts/record_lil_B203_startup_view_v6053.py','scripts/record_lil_B204_startup_view_v6163.py',{'B203':'B204','startup_v6053':'startup_v6163','V5998':'V6110'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_startup_checks.json',dict(tools=tools,parent_newgame_source='work/analysis/shachihoko_runs_v6095/newgame_terminal.json',parent_town_source='work/analysis/shachihoko_runs_v6096/town_terminal.json',only_identical_registered_V6110_whole_ROM_hash_reuse=True,all31_requested_and_final_RGB_frames_five_actor_controls_and_donor_hashes_required=True,full_goal_complete=False));print('V6160 startup verifier bound to exact V6110 source boots;31 whole RGB frames/five actor controls/donor hashes required.')
