"""Prepare fresh current cold boots, exact-parent controls and own-image native input."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_startup_tools_v7171')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[
      ('scripts/run_lil_B223_startup_v7121.py','scripts/run_lil_B224_startup_v7171.py',{'B223':'B224','v7121':'v7171','version=7118':'version=7168'}),
      ('scripts/verify_lil_B223_startup_v7122.py','scripts/verify_lil_B224_startup_v7172.py',{'B223':'B224','v7122':'v7172','v7121':'v7171','v7118':'v7168','v7067':'v7118','V7067':'V7118','Current7118':'Current7168',"oldtp=Path('work/analysis/lil_B222_runs_v7070')":"oldtp=Path('work/analysis/lil_B223_runs_v7121')"}),
      ('scripts/record_lil_B223_startup_view_v7122.py','scripts/record_lil_B224_startup_view_v7172.py',{'B223':'B224','v7122':'v7172','V7067':'V7118'}),
      ('scripts/bind_current_V7118_native_v7123.py','scripts/bind_current_V7168_native_v7173.py',{'V7118':'V7168','v7123':'v7173','lil_B223_release_v7119':'lil_B224_release_v7169','lil_B223_runs_v7121':'lil_B224_runs_v7171'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_startup_and_input_tools.json',dict(tools=rows,parent_controls_exact_registered_V7118_runs7121=True,unchanged_native_addresses_inputs_capture_schedule_and_donors=True,fresh_current_NewGame4001_and_inherited_town17401_frames=True,own_registered_NewGame4000_RAM_required=True,strict2b6_COMMON_directory123264_payload_and_actual_captain_guards_unchanged=True,targeted_headless_not_full_route_or_hardware=True,new_credit=0,full_goal_complete=False))
