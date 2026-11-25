"""Observe actual own-current Maria initialization with the exact disclosed system unlock."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_initializer_tools_v7701b')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/capture_papal_trade_initializers_v7646.py','scripts/capture_Maria_B207_initializer_v7701.py',{
        'Observe each actual current opening prelude through ordinary New Game, without fixtures.':'Observe the actual current Maria opening prelude with the exact existing system-only unlock.',
        'from pathlib import Path':'from pathlib import Path\nfrom scripts.maria_existing_unlock_contract_v7680 import validate_fixture,validate_capture',
        'papal_trade_original_initializers_v7646':'maria_B207_original_initializer_v7701',
        'choices=[0,1]':'choices=[3]',
        'papal_trade_original_initializers_route{route}_v7646':'Maria_B207_original_initializer_route{route}_v7701',
        'editorial_handoff_verification_v7637':'editorial_handoff_verification_v7693b',
        'all-routes-unified-v7611':'all-routes-unified-v7660',
        "inp=Path(f'work/analysis/papal_trade_route_runs_v7625/route{route}/ordinary_NewGame_inputs.json')":"inp=Path('work/analysis/maria_B207_route_run_v7680/ordinary_Maria_NewGame_prefix.json');fp=Path('work/analysis/maria_B207_route_run_v7680/existing_system_unlock_manifest.json');fixture=validate_fixture(fp)",
        "{0:'Rafael',1:'Hodram'}[route]":"{3:'Maria'}[route]",
        '4001':'6001',
        'no_save_savestate_ROM_RAM_roster_role_funds_RNG_event_orresult_fixture=True':'existing_system_only_unlock_manifest=str(fp),existing_system_only_unlock_manifest_sha256=sha(fp.read_bytes()),earned_unlock_verified=False,no_savestate_ROM_RAM_roster_role_funds_RNG_event_orresult_fixture=True',
        "'--inputs-json',str(inp),":"'--inputs-json',str(inp),'--battery-save',fixture['fixture_save'],'--allow-gallery-fixtures','--gallery-save-fixture-manifest',str(fp),'--touchscreen',",
        "'--capture-at','4000'":"'--capture-at','4000','5000','6000'",
        "assert r['frames']==4001 and r['cold_boot'] and not r['savestate_loaded'] and not r.get('battery_save_preloaded') and not r['callback_errors']":"assert r['frames']==6001;validate_capture(r)",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_Maria_original_initializer_capture.json',dict(derivation=result,all_original_source_observer_guards_preserved=True,exact_existing_system_unlock_not_earned=True,new_credit=0,full_goal_complete=False))
