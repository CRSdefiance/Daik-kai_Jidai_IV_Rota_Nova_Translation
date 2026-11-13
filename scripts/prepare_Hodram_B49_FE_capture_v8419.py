"""Capture the exact original FE paint call andheld WRAM;reuse completed tail VRAM exports."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_FE_tools_v8419');assert not root.exists()
    result=derive('scripts/capture_Hodram_outcome_FE_geometry_v8336.py','scripts/capture_Hodram_B49_FE_v8419.py',{
        'Hodram_outcome_FE_geometry_runs_v8336':'Hodram_B49_FE_runs_v8419',
        'work/analysis/Hodram_outcome_actual_models_v8334/six_clean_six_stored_native_bodies_one_Lil_header_distinct_FE.json':'work/analysis/Hodram_B49_models_v8408/native_models.json',
        'work/analysis/Hodram_outcome_fixtures_v8332/four_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json':'work/analysis/Hodram_B49_tail_v8415/bounded_tail_fixtures.json',
        'Hodram_B48_FE_geometry_':'Hodram_B49_FE_geometry_',
        '_v8336':'_v8419',
        "f['source_block']==48":"f['source_block']==49",
        "Path('work/analysis/Hodram_outcome_FE_scene_runs_v8333b')/f'route1_B48_{version}'":"Path('work/analysis/Hodram_B49_tail_runs_v8416')/f'route1_{version}_accept'",
        "e['start']<=4000":"e['start']<=4930",
        '4001':'4931',
        "'3490','3910'":"'4870','4930'",
        'ordinary_optional_activation':'possession_orordinary_optional_activation',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,exact_same_input_prefix_of_completed_accept_tail_runs=True,one_original_source_qualified_FE_paint_CPU_WRAM_DTCM_ITCM_snapshot_perlanguage=True,two_held_WRAM_exports_perlanguage=[4870,4930],completed_tail_native_VRAM_exports_reused_not_replayed=True,concrete_missing_held_WRAM_andoriginal_paint_call_data_resolved_by_focused_capture=True,no_inventory_flags_RNG_result_orinput_retiming=True,new_credit=0,full_goal_complete=False))
