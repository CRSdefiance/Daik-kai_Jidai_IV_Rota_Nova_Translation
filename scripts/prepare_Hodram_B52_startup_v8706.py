"""Prepare own registered B52 cold boot and strict captain1 context; preserve native rules."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_startup_tools_v8706');assert not root.exists();tools=[]
    tools.append(derive('scripts/capture_Hodram_B51_registered_v8611.py','scripts/capture_Hodram_B52_registered_v8706.py',{
        'Hodram_B51_registered_context_runs_v8611':'Hodram_B52_registered_context_runs_v8706',
        'Hodram_B51_release_v8610':'Hodram_B52_release_v8705','all-routes-unified-v8609':'all-routes-unified-v8704',
        'Hodram_B51_registered_route{route}_v8611_V8609':'Hodram_B52_registered_route{route}_v8706_V8704',
        'not B51 activation':'not B52 activation','ordinary_route_selection_not_optional_B51_activation':'ordinary_route_selection_not_optional_B52_activation',
    }))
    tools.append(derive('scripts/Hodram_B51_registered_route_context_v8612.py','scripts/Hodram_B52_registered_route_context_v8707.py',{
        'Hodram_B51_release_v8610':'Hodram_B52_release_v8705',
        'only_SC1_B51_change_324_otherblocks_andall_other_files_components_exact':'only_SC1_B52_change_324_otherblocks_andall_other_files_components_exact',
        'registered V8609':'registered V8704',
    }))
    tools.append(derive('scripts/bind_Hodram_B51_registered_v8612.py','scripts/bind_Hodram_B52_registered_v8707.py',{
        'Hodram_B51_registered_route_context_v8612':'Hodram_B52_registered_route_context_v8707',
        'Hodram_B51_registered_binding_v8612':'Hodram_B52_registered_binding_v8707',
        'Hodram_B51_registered_context_runs_v8611':'Hodram_B52_registered_context_runs_v8706',
        'current_V8609_Hodram_native_v8612':'current_V8704_Hodram_native_v8707',
        'Hodram_B51_release_v8610':'Hodram_B52_release_v8705','all-routes-unified-v8609':'all-routes-unified-v8704','V8609':'V8704',
        'optional_B51_activation':'optional_B52_activation',
    }))
    tools.append(derive('scripts/verify_Hodram_B51_registered_startup_v8613.py','scripts/verify_Hodram_B52_registered_startup_v8708.py',{
        'Hodram_B51_registered_startup_view_v8613':'Hodram_B52_registered_startup_view_v8708',
        'Hodram_B51_registered_binding_v8612':'Hodram_B52_registered_binding_v8707',
        'Hodram_B50_registered_binding_v8546':'Hodram_B51_registered_binding_v8612',
        'Hodram_B51_release_v8610':'Hodram_B52_release_v8705','V8609':'V8704',
        'optional_B51_activation':'optional_B52_activation',
    }))
    root.mkdir(parents=True)
    save(root/'derivations.json',dict(tools=tools,
         every_original_native_address_offset_name_actor_payload_andmultiplicity_guard_preserved=True,
         own_registered_coldboot_anddirect_sheet_view_required_before_credit=True,
         no_unchanged_scene_capture_getter_orfont_probe_replay=True,
         new_capture_andstartup_checks_not_yet_executed=True,new_credit=0,full_goal_complete=False))
