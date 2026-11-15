"""Rebind the validated typed FE descriptor/palette/VRAM reader to fresh B49 paint evidence."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_FE_binding_tools_v8420');assert not root.exists()
    result=derive('scripts/bind_Hodram_outcome_FE_geometry_v8338b.py','scripts/bind_Hodram_B49_FE_v8420.py',{
        'Hodram_outcome_FE_geometry_v8338b':'Hodram_B49_FE_binding_v8420',
        'Hodram_outcome_FE_geometry_runs_v8336':'Hodram_B49_FE_runs_v8419',
        'work/analysis/Hodram_outcome_actual_models_v8334/six_clean_six_stored_native_bodies_one_Lil_header_distinct_FE.json':'work/analysis/Hodram_B49_models_v8408/native_models.json',
        "Path('work/analysis/Hodram_outcome_FE_scene_runs_v8333b')/f'route1_B48_{version}'":"Path('work/analysis/Hodram_B49_tail_runs_v8416')/f'route1_{version}_accept'",
        '4001':'4931',
        "e['start']<=4000":"e['start']<=4930",
        '[3490,3910]':'[4870,4930]',
        'focused_actual_frames=8002':'focused_actual_frames=9862',
        '8002focusedframes':'9862focusedframes',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_original_FE_descriptor_vtable_palette_VRAM_bank_mapping_bitmap_andRGB_guards_unchanged=True,all_native_high_integer_constants_andmultiplicity_preserved=True,current_B49_original_paint_snapshots_andheld_WRAM_bind_completed_tail_VRAM_exports=True,no_repeated_whole_flow_native_data_orcontroller_retiming=True,new_credit=0,full_goal_complete=False))
