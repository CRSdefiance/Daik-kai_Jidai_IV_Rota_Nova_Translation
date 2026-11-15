"""Use the verified current directional-selection pointer mode; preserve both prior attempts."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_context_tools_v7677')
if __name__=='__main__':
    assert not ROOT.exists()
    capture=derive('scripts/capture_Maria_B207_context_v7674.py','scripts/capture_Maria_B207_context_v7677.py',{
        'v7674':'v7677',
        ",'--touchscreen'":'',
        'current_verified_Rafael_NewGame_menu_then_three_ordinary_RIGHT_presses=True':'current_verified_Rafael_NewGame_menu_then_three_ordinary_RIGHT_presses=True,default_mouse_pointer_mode_matches_verified_Rafael_Hodram_route_selection=True,preserved_touchscreen_attempt="work/analysis/maria_B207_route_run_v7674/terminal.json"',
    })
    binder=derive('scripts/bind_Maria_B207_context_v7675.py','scripts/bind_Maria_B207_context_v7678.py',{
        'maria_B207_native_v7675':'maria_B207_native_v7678',
        'maria_B207_route_run_v7674':'maria_B207_route_run_v7677',
    })
    consumers=derive('scripts/prove_Maria_B207_consumers_v7676.py','scripts/prove_Maria_B207_consumers_v7679.py',{
        'maria_B207_consumers_v7676':'maria_B207_consumers_v7679',
        'maria_B207_native_v7675':'maria_B207_native_v7678',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_pointer_mode_successors.json',dict(capture=capture,binder=binder,consumers=consumers,strict_captain3_guard_unchanged=True,all_prior_attempts_preserved=True,new_credit=0,full_goal_complete=False))
