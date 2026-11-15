"""Bind the default B52 source/English path without claiming the unvisited alternative."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_default_audit_tools_v8651');assert not root.exists()
    result=derive('scripts/audit_Hodram_B51_actual_v8576.py','scripts/audit_Hodram_B52_actual_v8651.py',{
        'Hodram_B51_actual_v8576':'Hodram_B52_actual_v8651','Hodram_B51_fixtures_v8573':'Hodram_B52_fixtures_v8648','Hodram_B51_models_v8575':'Hodram_B52_models_v8650','Hodram_B51_scene_runs_v8574':'Hodram_B52_scene_runs_v8649',
        'choices=[51]':'choices=[52]','{51:10001}':'{52:10001}',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,whole_resident_source_commands_actual_native_branch_lengths_readonly_callbacks_complete_body_name_masks_andnormal_value_carry_guards_preserved=True,missing_alternative_is_explicit_not_inferred_as_actual=True,actual_menu_glyph_geometry_highlight_controller_andalternate_flagged_end_checks_remain_separate=True,no_capture_replay_orcredit=True,new_credit=0,full_goal_complete=False))
