"""Add three read-only native-state exports to not-yet-run B48; original controller schedule unchanged."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_FE_scene_tools_v8333b');assert not root.exists()
    result=derive('scripts/run_Hodram_outcomes_v8333.py','scripts/run_Hodram_outcomes_FE_v8333b.py',{
        'choices=[47,48]':'choices=[48]',
        'Hodram_outcome_scene_runs_v8333':'Hodram_outcome_FE_scene_runs_v8333b',
        "_v8333'":"_v8333b'",
        "'--dump-ram']":"'--capture-native-state-at','3490','3910','4510','--dump-ram']",
        'producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False':'producer_sha256=sha(Path(__file__).read_bytes()),read_only_native_state_export_frames=[3490,3910,4510],no_change_to_ordinary_controller_schedule_ororiginal_script=True,full_goal_complete=False',
    })
    root.mkdir(parents=True);save(root/'three_readonly_native_exports_unchanged_controller_schedule.json',dict(derivation=result,new_B48_captures_only_no_completed_run_repeated=True,
        exports_read_CPU_RAM_TCM_andVRAM_not_savestate_load_orstate_mutation=True,all_native_address_constants_andmultiplicity_preserved=True,new_credit=0,full_goal_complete=False))
