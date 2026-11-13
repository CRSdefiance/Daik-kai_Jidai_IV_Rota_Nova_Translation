"""Bind a narrowly audited existing unlock fixture to own-current Maria New Game."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_context_tools_v7680')
if __name__=='__main__':
    assert not ROOT.exists()
    context=derive('scripts/maria_current_native_context_v7671.py','scripts/maria_unlocked_current_context_v7680.py',{
        'class MariaCurrentContext:':'class MariaUnlockedCurrentContext:',
        'from pathlib import Path':'from pathlib import Path\nfrom scripts.maria_existing_unlock_contract_v7680 import validate_capture',
        "assert not report.get('battery_save_preloaded') and not any(v for k,v in report.items() if k.startswith('synthetic_'))":"validate_capture(report)",
    })
    capture=derive('scripts/capture_Maria_B207_context_v7671.py','scripts/capture_Maria_B207_context_v7680.py',{
        'v7671':'v7680',
        'from pathlib import Path':'from pathlib import Path\nfrom scripts.maria_existing_unlock_contract_v7680 import HISTORICAL,validate_fixture,validate_capture',
        "ROOT.mkdir(parents=True);inputs=ROOT/'ordinary_Maria_NewGame_prefix.json';save(inputs,prefix)":"ROOT.mkdir(parents=True);fixture=read(HISTORICAL);fixture.update(production_ROM=str(rom),production_ROM_sha256=v['candidate_sha256'],current_test_scope='Own-current ordinary Maria NewGame with existing system-only unlock;not earned or optional B207 activation.');fp=ROOT/'existing_system_unlock_manifest.json';save(fp,fixture);validate_fixture(fp);inputs=ROOT/'ordinary_Maria_NewGame_prefix.json';save(inputs,prefix)",
        'no_battery_savestate_ROM_RAM_roles_roster_funds_RNG_event_orresult_fixture=True':'existing_system_unlock_manifest=str(fp),existing_system_unlock_manifest_sha256=sha(fp.read_bytes()),earned_unlock_verified=False,no_savestate_ROM_RAM_roles_roster_funds_RNG_event_orresult_fixture=True',
        "'--inputs-json',str(inputs),":"'--inputs-json',str(inputs),'--battery-save',fixture['fixture_save'],'--allow-gallery-fixtures','--gallery-save-fixture-manifest',str(fp),",
        "assert r['frames']==4001 and r['cold_boot'] and not r['savestate_loaded'] and not r.get('battery_save_preloaded') and not r['callback_errors'] and not any(v for k,v in r.items() if k.startswith('synthetic_'))":"assert r['frames']==4001;validate_capture(r)",
        "actual_captain3_strict_payload_binding_pending=True":"actual_captain3_strict_payload_binding_pending=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False",
    })
    binder=derive('scripts/bind_Maria_B207_context_v7672.py','scripts/bind_Maria_B207_context_v7681.py',{
        'maria_B207_native_v7672':'maria_B207_native_v7681',
        'maria_B207_route_run_v7671':'maria_B207_route_run_v7680',
        'from scripts.maria_current_native_context_v7671 import MariaCurrentContext':'from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext as MariaCurrentContext\nfrom scripts.maria_existing_unlock_contract_v7680 import validate_capture',
        "assert r['frames']==4001 and r['cold_boot'] and not r['savestate_loaded'] and not r.get('battery_save_preloaded') and not r['callback_errors']":"assert r['frames']==4001;validate_capture(r)",
        "Path('scripts/maria_current_native_context_v7671.py')":"Path('scripts/maria_unlocked_current_context_v7680.py'),Path('scripts/maria_existing_unlock_contract_v7680.py')",
        'new_credit=0,evidence=':'new_credit=0,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,evidence=',
    })
    consumers=derive('scripts/prove_Maria_B207_consumers_v7673.py','scripts/prove_Maria_B207_consumers_v7682.py',{
        'maria_B207_consumers_v7673':'maria_B207_consumers_v7682',
        'maria_B207_native_v7672':'maria_B207_native_v7681',
        'from scripts.maria_current_native_context_v7671 import MariaCurrentContext':'from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext as MariaCurrentContext',
        'new_credit=0,evidence=':'new_credit=0,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,evidence=',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_exact_unlock_successors.json',dict(context=context,capture=capture,binder=binder,consumers=consumers,strict_captain3_andallnative_payload_instruction_actor_ownership_guards_unchanged=True,only_exact_existing_system_fixture_permitted=True,all_prior_attempts_preserved=True,new_credit=0,full_goal_complete=False))
