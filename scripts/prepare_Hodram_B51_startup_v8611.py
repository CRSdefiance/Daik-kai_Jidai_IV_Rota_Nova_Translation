"""Prepare own registered B51 coldboot, captain1 context and explicitly scoped startup review."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B51_startup_tools_v8611');assert not root.exists();tools=[]
    tools.append(derive('scripts/capture_Hodram_B50_registered_v8545.py','scripts/capture_Hodram_B51_registered_v8611.py',{
        'Hodram_B50_registered_context_runs_v8545':'Hodram_B51_registered_context_runs_v8611',
        'Hodram_B50_release_v8544':'Hodram_B51_release_v8610',
        'all-routes-unified-v8543':'all-routes-unified-v8609',
        'Hodram_B50_registered_route{route}_v8545_V8543':'Hodram_B51_registered_route{route}_v8611_V8609',
        'not B50 activation':'not B51 activation','ordinary_route_selection_not_optional_B50_activation':'ordinary_route_selection_not_optional_B51_activation'}))
    tools.append(derive('scripts/Hodram_B50_registered_route_context_v8546.py','scripts/Hodram_B51_registered_route_context_v8612.py',{
        'Hodram_B50_release_v8544':'Hodram_B51_release_v8610',
        'only_SC1_B50_change_324_otherblocks_andall_other_files_components_exact':'only_SC1_B51_change_324_otherblocks_andall_other_files_components_exact',
        'registered V8543':'registered V8609'}))
    tools.append(derive('scripts/bind_Hodram_B50_registered_v8546.py','scripts/bind_Hodram_B51_registered_v8612.py',{
        'Hodram_B50_registered_route_context_v8546':'Hodram_B51_registered_route_context_v8612',
        'Hodram_B50_registered_binding_v8546':'Hodram_B51_registered_binding_v8612',
        'Hodram_B50_registered_context_runs_v8545':'Hodram_B51_registered_context_runs_v8611',
        'current_V8543_Hodram_native_v8546':'current_V8609_Hodram_native_v8612',
        'Hodram_B50_release_v8544':'Hodram_B51_release_v8610',
        'all-routes-unified-v8543':'all-routes-unified-v8609','V8543':'V8609',
        'optional_B50_activation':'optional_B51_activation'}))
    tools.append(derive('scripts/verify_Hodram_B50_registered_startup_v8547.py','scripts/verify_Hodram_B51_registered_startup_v8613.py',{
        'Hodram_B50_registered_startup_view_v8547':'Hodram_B51_registered_startup_view_v8613',
        'Hodram_B50_registered_binding_v8546':'Hodram_B51_registered_binding_v8612',
        'Hodram_B49_registered_binding_v8478':'Hodram_B50_registered_binding_v8546',
        'Hodram_B50_release_v8544':'Hodram_B51_release_v8610','V8543':'V8609',
        'optional_B50_activation':'optional_B51_activation'}))
    root.mkdir(parents=True);save(root/'derivations.json',dict(tools=tools,all_original_native_addresses_offsets_actor_payload_name_andmultiplicity_guards_preserved=True,own_registered_coldboot_anddirect_sheet_view_required_before_credit=True,unchanged_old_startup_names_reused_only_through_exact_hash_bindings=True,no_new_capture_orcredit_yet=True,new_credit=0,full_goal_complete=False))
