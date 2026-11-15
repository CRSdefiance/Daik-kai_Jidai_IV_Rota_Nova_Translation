"""Prepare current build startup comparison against exact parent-owned NewGame/town captures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B222_startup_tools_v7071')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('scripts/verify_lil_B221_startup_v7015.py','scripts/verify_lil_B222_startup_v7071.py',{'B221':'B222','v7015':'v7071','v7014':'v7070','v7011':'v7067','v6956':'v7029','V6956':'V7029','Current7011':'Current7067',"oldtp=Path('work/analysis/lil_B220_runs_v6959')/(case+'_terminal.json')":"oldtp=(Path('work/analysis/square_shopkeeper_run_v7019/terminal.json') if case=='newgame' else Path('work/analysis/square_shopkeeper_runs_v7032/town_terminal.json'))"}),
        ('scripts/record_lil_B221_startup_view_v7015.py','scripts/record_lil_B222_startup_view_v7071.py',{'B221':'B222','v7015':'v7071','V6956':'V7029'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',dict(tools=rows,newgame_parent_capture7019_bound_by_exact_whole_ROM_V7029_hash=True,town_parent_capture7032_bound_to_registered_V7029=True,no_old_ROM_RAM_overlay_or_native_address_change=True,new_credit=0,full_goal_complete=False))
