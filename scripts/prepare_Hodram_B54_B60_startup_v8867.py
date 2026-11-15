"""Require a new registered ROM's own ordinary startup; preserve the exact unchanged native-name reuse guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_startup_tools_v8867');assert not root.exists()
    capture=derive('scripts/capture_Hodram_B31_B53_registered_v8780.py','scripts/capture_Hodram_B54_B60_registered_v8867.py',{
      'B31_B53':'B54_B60','Hodram_B31_B53_registered_context_runs_v8780':'Hodram_B54_B60_registered_context_runs_v8867',
      'Hodram_B31_B53_release_v8779':'Hodram_B54_B60_release_v8866','all-routes-unified-v8778':'all-routes-unified-v8865',
      'Hodram_B31_B53_registered_route{route}_v8780_V8778':'Hodram_B54_B60_registered_route{route}_v8867_V8865',
    })
    context=derive('scripts/Hodram_B31_B53_registered_route_context_v8781.py','scripts/Hodram_B54_B60_registered_route_context_v8868.py',{
      'V8778':'V8865','Hodram_B31_B53_release_v8779':'Hodram_B54_B60_release_v8866',
      'only_SC1_B31_B53_change_323_otherblocks_andall_other_files_components_exact':'only_SC1_B54_B60_change_318_otherblocks_andall_other_files_components_exact',
    })
    binding=derive('scripts/bind_Hodram_B31_B53_registered_v8781.py','scripts/bind_Hodram_B54_B60_registered_v8868.py',{
      'B31_B53':'B54_B60','V8778':'V8865',
      'Hodram_B31_B53_registered_route_context_v8781':'Hodram_B54_B60_registered_route_context_v8868',
      'Hodram_B31_B53_registered_binding_v8781':'Hodram_B54_B60_registered_binding_v8868',
      'Hodram_B31_B53_registered_context_runs_v8780':'Hodram_B54_B60_registered_context_runs_v8867',
      'current_V8778_Hodram_native_v8781':'current_V8865_Hodram_native_v8868',
      'Hodram_B31_B53_release_v8779':'Hodram_B54_B60_release_v8866','all-routes-unified-v8778':'all-routes-unified-v8865',
    })
    view=derive('scripts/verify_Hodram_B31_B53_registered_startup_v8782.py','scripts/verify_Hodram_B54_B60_registered_startup_v8869.py',{
      'B31_B53':'B54_B60','V8778':'V8865',
      'Hodram_B31_B53_registered_startup_view_v8782':'Hodram_B54_B60_registered_startup_view_v8869',
      'Hodram_B31_B53_registered_binding_v8781':'Hodram_B54_B60_registered_binding_v8868',
      'Hodram_B52_registered_binding_v8707':'Hodram_B31_B53_registered_binding_v8781',
      'Hodram_B31_B53_release_v8779':'Hodram_B54_B60_release_v8866',
    })
    root.mkdir(parents=True);save(root/'source_locked_registered_startup.json',dict(capture=capture,context=context,binding=binding,view=view,all_original_native_high_integer_constants_andmultiplicity_preserved=True,own_registered_ROM_coldboot4001frames_captain1_payload_name12_Blades8_all6RGBpairs_anddirect_view_required=True,unchanged_names_getters_reuse_requires_complete_ARM9_COMMON_font_andwhole_actual_actors_equal=True,no_historical_RAM_overlay_no_optional_event_orfullroute_claim=True,no_capture_orcredit_by_preparer=True,full_goal_complete=False))
