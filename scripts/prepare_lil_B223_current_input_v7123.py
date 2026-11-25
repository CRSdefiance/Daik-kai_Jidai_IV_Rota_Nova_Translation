"""Prepare strict current-input binding to the new registered image's own boot."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_current_input_tools_v7123')
if __name__=='__main__':
    assert not ROOT.exists()
    a='scripts/bind_current_V7067_native_v7077.py';b='scripts/bind_current_V7118_native_v7123.py'
    c={'V7067':'V7118','v7077':'v7123','lil_B222_release_v7068':'lil_B223_release_v7119','lil_B222_runs_v7070':'lil_B223_runs_v7121'}
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);row=derive(a,b,c)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_input_binder.json',dict(tool=row,own_registered_NewGame4000_RAM_required=True,strict2b6_COMMON_directory123264_payload_and_actual_captain_guards_unchanged=True,new_credit=0,full_goal_complete=False))
