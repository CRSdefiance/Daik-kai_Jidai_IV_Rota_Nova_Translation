"""Prepare fresh current-image cold boots and exact-parent comparison."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_startup_tools_v7121')
if __name__=='__main__':
    assert not ROOT.exists()
    old="oldtp=(Path('work/analysis/square_shopkeeper_run_v7019/terminal.json') if case=='newgame' else Path('work/analysis/square_shopkeeper_runs_v7032/town_terminal.json'))"
    new="oldtp=Path('work/analysis/lil_B222_runs_v7070')/(case+'_terminal.json')"
    jobs=[('scripts/run_lil_B222_startup_v7070.py','scripts/run_lil_B223_startup_v7121.py',{'B222':'B223','v7070':'v7121','version=7067':'version=7118'}),
      ('scripts/verify_lil_B222_startup_v7071.py','scripts/verify_lil_B223_startup_v7122.py',{'B222':'B223','v7071':'v7122','v7070':'v7121','v7067':'v7118','v7029':'v7067','V7029':'V7067','Current7067':'Current7118',old:new}),
      ('scripts/record_lil_B222_startup_view_v7071.py','scripts/record_lil_B223_startup_view_v7122.py',{'B222':'B223','v7071':'v7122','V7029':'V7067'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_startup_runners.json',dict(tools=rows,parent_controls_exact_registered_V7067_runs7070=True,no_native_address_input_schedule_capture_or_donor_change=True,fresh_current_NewGame4001_and_inherited_town17401_frames=True,targeted_headless_not_full_route_or_hardware=True,new_credit=0,full_goal_complete=False))
