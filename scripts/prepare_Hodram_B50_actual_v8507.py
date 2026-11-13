"""Combine proven whole-command audit with original FE and progressive complete masks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_actual_tools_v8507');assert not root.exists()
    old=Path('scripts/audit_Hodram_B49_actual_v8409.py').read_text(encoding='utf-8')
    tailpath=Path('scripts/audit_Hodram_B49_tail_v8417.py');tail=tailpath.read_text(encoding='utf-8')
    begin="            record=records[at];actor=record['source_selector'];model=native[record['id']];assert len(model['pages'])==1"
    oldstage=old[old.index(begin):old.index('        ids=[r[',old.index(begin))]
    start=tail.index("                record=records[at];actor=record['source_selector'];FE=")
    stage=tail[start:tail.index('            assert normal and not unknown',start)]
    stage='\n'.join(line[4:] if line.startswith('    ') else line for line in stage.split('\n'))
    stage=checked_text('if True:\n'+stage,{'cp=oracle(':'cp=pixels(','choice=choice,':'block=number,'}).split('\n',1)[1]
    proof=derive('scripts/audit_Hodram_B49_actual_v8409.py','scripts/audit_Hodram_B50_actual_v8507.py',{
        'Hodram_B49_actual_v8409':'Hodram_B50_actual_v8507',
        'Hodram_B49_fixtures_v8406':'Hodram_B50_fixtures_v8504',
        'Hodram_B49_models_v8408':'Hodram_B50_models_v8506',
        'Hodram_B49_scene_runs_v8407':'Hodram_B50_scene_runs_v8505',
        'choices=[49]':'choices=[50]',
        '{49:10001}[number]':'{50:10001}[number]',
        'def masks(image):':'def masks(image,width=216):',
        'image.crop((16,296,232,360))':'image.crop((16,296,16+width,360))',
        '(i%216,i//216) for i,v in enumerate(pixels)':'(i%width,i//width) for i,v in enumerate(pixels)',
        'masks=masks(pic)':'masks216=masks(pic,216),masks228=masks(pic,228)',
        oldstage:stage,
        'full_resource_4820_layout2_hide4700_andlater_state_comparison_separate_pending':'full_resource_4800_layout0_hide4700_andlater_state_comparison_separate_pending',
        'native_page_masks_216x64_not_a_full_scene_resource_orfuture_simulation_proof':'progressive216x64_FE228x48_physical64_masks_not_full_scene_orfuture_simulation_proof',
    })
    root.mkdir(parents=True);save(root/'derivations.json',dict(tool=proof,FE_complete_mask_stage_source=str(tailpath),FE_complete_mask_stage_source_sha256=sha(tailpath.read_bytes()),FE_stage=stage,all_native_high_integer_constants_preserved=True,no_runtime_replay_orinput_changes=True,new_credit=0,full_goal_complete=False))
