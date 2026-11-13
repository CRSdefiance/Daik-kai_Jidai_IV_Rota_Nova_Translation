"""Prepare own registered B50 coldboot context;reuse old startup only as exact comparison evidence."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_startup_tools_v8545');assert not root.exists();tools=[]
    tools.append(derive('scripts/capture_Hodram_B49_registered_v8477.py','scripts/capture_Hodram_B50_registered_v8545.py',{
        'Hodram_B49_registered_context_runs_v8477':'Hodram_B50_registered_context_runs_v8545',
        'Hodram_B49_release_v8476':'Hodram_B50_release_v8544',
        'all-routes-unified-v8475':'all-routes-unified-v8543',
        'Hodram_B49_registered_route{route}_v8477_V8475':'Hodram_B50_registered_route{route}_v8545_V8543',
        'not B49 activation':'not B50 activation',
        'ordinary_route_selection_not_optional_B47_B48_activation':'ordinary_route_selection_not_optional_B50_activation',
    }))
    tools.append(derive('scripts/Hodram_B49_registered_route_context_v8478.py','scripts/Hodram_B50_registered_route_context_v8546.py',{
        'Hodram_B49_release_v8476':'Hodram_B50_release_v8544',
        'only_SC1_B49_change_324_otherblocks_andall_other_files_components_exact':'only_SC1_B50_change_324_otherblocks_andall_other_files_components_exact',
        'registered V8377':'registered V8543',
    }))
    tools.append(derive('scripts/bind_Hodram_B49_registered_v8478.py','scripts/bind_Hodram_B50_registered_v8546.py',{
        'Hodram_B49_registered_route_context_v8478':'Hodram_B50_registered_route_context_v8546',
        'Hodram_B49_registered_binding_v8478':'Hodram_B50_registered_binding_v8546',
        'Hodram_B49_registered_context_runs_v8477':'Hodram_B50_registered_context_runs_v8545',
        'current_V8475_Hodram_native_v8478':'current_V8543_Hodram_native_v8546',
        'Hodram_B49_release_v8476':'Hodram_B50_release_v8544',
        'all-routes-unified-v8475':'all-routes-unified-v8543','V8475':'V8543',
        'optional_B49_activation':'optional_B50_activation',
    }))
    tools.append(derive('scripts/verify_Hodram_B49_registered_startup_v8479.py','scripts/verify_Hodram_B50_registered_startup_v8547.py',{
        'Hodram_B49_registered_startup_view_v8479':'Hodram_B50_registered_startup_view_v8547',
        'Hodram_B49_registered_binding_v8478':'Hodram_B50_registered_binding_v8546',
        'Hodram_outcomes_registered_binding_v8380':'Hodram_B49_registered_binding_v8478',
        'Hodram_B49_release_v8476':'Hodram_B50_release_v8544','V8475':'V8543',
        'optional_B49_activation':'optional_B50_activation',
    }))
    root.mkdir(parents=True);save(root/'derivations.json',dict(tools=tools,all_original_native_addresses_field_offsets_actor_payload_name_andmultiplicity_guards_preserved=True,own_registered_coldboot_required_before_credit=True,unchanged_old_capture_andnameplanes_reused_only_through_exact_hash_bindings=True,no_new_capture_orcredit_yet=True,new_credit=0,full_goal_complete=False))
