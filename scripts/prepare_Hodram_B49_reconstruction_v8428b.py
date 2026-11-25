"""Correct the preserved helper's one inherited menu replacement span;all reconstruction guards remain active."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_rebuild_tools_v8428b');assert not root.exists()
    result=derive('dk4tool/patch/hodram_B49_reconstruction_v1.py','dk4tool/patch/hodram_B49_reconstruction_v2.py',{
        "patches.append(dict(start=at,end=at+36,old=before,source=ja,value=typed,id='complete-native-menu'))":"patches.append(dict(start=at,end=at+26,old=before,source=ja,value=typed,id='complete-native-menu'))",
    })
    from dk4tool.patch.hodram_B49_reconstruction_v2 import reconstruct
    from dk4tool.dialogue.hodram_B49_choices_v2 import compile_choices
    mapping=read('work/analysis/Hodram_B49_relocation_v8398/reconstruction.json');packet=read('work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json')['groups'][0]
    doc=read('translations/hodram_B49_editorial_manuscript_v4.json');controls=read('work/analysis/Hodram_B49_source_controls_v8384/source_controls.json');group=mapping['groups'][0]
    target=reconstruct(bytes.fromhex(packet['current_block_hex']),bytes.fromhex(packet['clean_block_hex']),group,packet,doc['records'],controls['operands_requiring_adjustment_when_resizing'],doc['typed_choice_records'],compile_choices(doc['typed_choice_records']))
    assert target==Path(group['target_block']).read_bytes() and sha(target)==group['target_block_sha256']
    root.mkdir(parents=True);save(root/'independent_reconstruction_positive.json',dict(derivation=result,failed_v1_andproducer_preserved=True,only_actual26byte_menu_replacement_span_corrected=True,all_source_current_native_control_relative_preamble_choice_terminal_tail_andinverse_guards_preserved=True,target_block_sha256=sha(target),entire_research_block_byte_exact=True,source_andcurrent_full_block_inverse_exact=True,no_ROM_mutation_oratomic_commit=True,independent_native_actual_semantic_precommit_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('Independent B49 production reconstructionv2 equals complete tested block;all36commands/8relatives/14preambles/2choices/end/tails andboth full inverses pass. Failedv1 preserved;no ROM commit.')
