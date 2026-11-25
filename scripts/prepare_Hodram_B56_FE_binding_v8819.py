"""Bind B56's actual four complete holds perlanguage to original FE contexts andVRAM."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B56_FE_tools_v8819');assert not root.exists()
    result=derive('scripts/bind_Hodram_B50_FE_v8508.py','scripts/bind_Hodram_B56_FE_v8819.py',{
        'Hodram_B50_FE_binding_v8508':'Hodram_B56_FE_binding_v8819',
        'Hodram_B50_scene_runs_v8505':'Hodram_B54_B60_scene_runs_v8816',
        'Hodram_B50_models_v8506/native_models.json':'Hodram_B54_B60_models_v8817/native_models.json',
        "folder=RUNS/f'route1_B50_{version}'":"folder=RUNS/f'route1_B56_{version}'",
        "terminal['frames']==10001":"terminal['frames']==7001",
        'work/analysis/Hodram_B50_actual_v8507/B50/paired_actual_dialogue_headers_flow_returns.json':'work/analysis/Hodram_B56_actual_v8818/B56/paired_actual_dialogue_headers_flow_returns.json',
        'held=={4330,4390,4450}':'held=={4030,4090,4150,4210}',
        'assert len(holds)==3':'assert len(holds)==4',
        'two_original_FE_paint_snapshots_six_exact_bitmap_palette_RGB_holds.json':'two_original_FE_paint_snapshots_eight_exact_bitmap_palette_RGB_holds.json',
        'actual_frames=20002':'actual_frames=14002',
        'same_whole_native_scene_runs_20002_frames':'same_whole_native_scene_runs_14002_frames',
        'B50 actual FE:two originalpaint snapshots/six same-run held nativebitmaps/palettes/RGB;228x48/288stride/6x12/16pitch andcurrent vtables exact;no repeatedwholeflow tests.':'B56 actual FE:two originalpaint snapshots/eight same-run held nativebitmaps/palettes/RGB;228x48/288stride/6x12/16pitch andcurrent vtables exact;no repeatedwholeflow tests.',
    })
    root.mkdir(parents=True);save(root/'source_locked_FE_binding.json',dict(derivation=result,
        two_existing7001frame_runs_reused_no_recapture=True,actual_FEhold_frames_perlanguage=[4030,4090,4150,4210],
        all_original_typed_context_bitmap_palette_current_vtable_VRAM_RGB_readonly_andwholememory_guards_preserved=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
