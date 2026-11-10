"""Source-lock independent original FE paint-register/descriptor/palette/VRAM validation to B49."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_FE_production_tools_v8435');assert not root.exists()
    result=derive('dk4tool/patch/hodram_outcomes_FE_evidence_v2.py','dk4tool/patch/hodram_B49_FE_evidence_v1.py',{
        'Hodram_outcome_FE_geometry_runs_v8336':'Hodram_B49_FE_runs_v8419',
        "data['fixtures']['fixtures']":"data['tail_fixtures']['fixtures']",
        "f['source_block']==48":"f['source_block']==49",
        'DK4_MES_B48_R0006':'DK4_MES_B49_R0081',
        "Path('work/analysis/Hodram_outcome_FE_scene_runs_v8333b')/f'route1_B48_{version}'":"Path('work/analysis/Hodram_B49_tail_runs_v8416')/f'route1_{version}_accept'",
        '4001':'4931',
        "e['start']<=4000":"e['start']<=4930",
        '[3490,3910]':'[4870,4930]',
        '8002':'9862',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_original_FE_PC_R0_R1_completeinput_NUL_typed_descriptors_palette_bankD_VRAM_andRGB_guards_preserved=True,all_native_high_integer_constants_andmultiplicity_preserved=True,no_paint_CPU_index_orlogical_palette_normalization_changed=True,no_emulator_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
