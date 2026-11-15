"""Turn the original saved FE descriptor/VRAM proof into a read-only production reader."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B56_FE_production_tools_v8850');assert not root.exists()
    original=Path('scripts/bind_Hodram_B56_FE_v8819b.py').read_text(encoding='utf-8')
    tail=original[original.index('    ROOT.mkdir(parents=True);save('):]
    ending="""    proof=evidence_data['B56_FE']
    require(proof['groups']==groups,'every independently reconstructed FE descriptor/palette/view/vtable/held bitmap/VRAM/RGB field')
    require(proof['actual_frames']==14002 and proof['new_credit']==0 and not proof['full_goal_complete'],'existing paired B56 runs only/no new editorial orframe credit')
    for key in ['whole_scene_tests_not_repeated','same_whole_native_scene_runs_14002_frames','all_actual_FE_typed_descriptors_palette_complete_bitmap_andphysical_RGB_match_independent_model','no_gameplay_state_save_conditions_roles_roster_funds_RNG_results_orcontroller_retiming','read_only_callbacks_host_slots_andcore_restored','not_natural_optional_activation_original_location_customnames_fullroute_hardware_oreveryframe_causality']:
        require(proof[key] is True,'bounded FE evidence scope:'+key)
    for path,digest in proof['evidence'].items():require(sha(Path(path).read_bytes())==digest,'original complete FE evidence file:'+path)
    return dict(original_paint_contexts=2,complete_same_run_FE_holds=6,typed_geometry=[228,48,288,6,12,16],complete_palette_bitmap_VRAM_physical_RGB_andcurrent_source_vtables_bound=True,no_new_emulator_frames_orcredit=True)

def check_FE_live(evidence_data,parent,load,require):
    try:return _check_FE_live(evidence_data,parent,load,require)
    except (KeyError,TypeError,IndexError,AssertionError,StopIteration) as error:
        raise ValueError('Original live FE descriptor/bitmap/VRAM/RGB evidence contradicts source: '+str(error)) from error
"""
    module=derive('scripts/bind_Hodram_B56_FE_v8819b.py','dk4tool/patch/hodram_B54_B60_FE_actual_v1.py',{
        "if __name__=='__main__':":"def _check_FE_live(evidence_data,parent,load,require):",
        "assert not ROOT.exists();models=read(MODELS)":"models=evidence_data['models']",
        "arm=image.read_file('/__arm9__.bin');assert":"arm=image.read_file('/__arm9__.bin');require(arm==parent.read_file('/__arm9__.bin'),'complete unchanged current source runtime');assert",
        tail:ending,
    })
    root.mkdir(parents=True);save(root/'source_locked_FE_live_reader.json',dict(module=module,all_original_native_addresses_sizes_context_bitmap_font_metric_header_palette_vtable_RAM_VRAM_physicalRGB_readonly_callback_andhost_restore_guards_preserved=True,no_new_snapshot_capture_producer_execution_orROM_write=True,new_credit=0,full_goal_complete=False))
