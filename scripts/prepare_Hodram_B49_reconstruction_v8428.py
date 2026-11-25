"""Source-lock the independent mixed speech/menu reconstruction helper to B49's exact validated spans."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_rebuild_tools_v8428');assert not root.exists()
    result=derive('dk4tool/patch/rafael_B46_reconstruction_v1.py','dk4tool/patch/hodram_B49_reconstruction_v1.py',{
        'Rafael B46 reconstruction':'Hodram B49 reconstruction',
        '/data/SC0.DK4':'/data/SC1.DK4',
        "at==256 and len(before)==len(ja)==choice['old_length']==36":"at==574 and len(before)==len(ja)==choice['old_length']==26",
        'old[at:at+36]==before and clean[at:at+36]==ja':'old[at:at+26]==before and clean[at:at+26]==ja',
        "len(typed)==choice['new_length']==30":"len(typed)==choice['new_length']==22",
        "row['command_offset']==at":"row['current_choice_command_offset']==at",
        "mapped(choice['old_offset'])==choice['new_offset']==242":"mapped(choice['old_offset'])==choice['new_offset']==518",
    })
    from dk4tool.patch.hodram_B49_reconstruction_v1 import reconstruct
    from dk4tool.dialogue.hodram_B49_choices_v2 import compile_choices
    mapping=read('work/analysis/Hodram_B49_relocation_v8398/reconstruction.json');packet=read('work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json')['groups'][0]
    doc=read('translations/hodram_B49_editorial_manuscript_v4.json');controls=read('work/analysis/Hodram_B49_source_controls_v8384/source_controls.json');group=mapping['groups'][0]
    old=bytes.fromhex(packet['current_block_hex']);clean=bytes.fromhex(packet['clean_block_hex'])
    target=reconstruct(old,clean,group,packet,doc['records'],controls['operands_requiring_adjustment_when_resizing'],doc['typed_choice_records'],compile_choices(doc['typed_choice_records']))
    assert target==Path(group['target_block']).read_bytes() and sha(target)==group['target_block_sha256']
    root.mkdir(parents=True);save(root/'independent_reconstruction_positive.json',dict(derivation=result,full_source_current_block_andall36_commands8_relatives14_preambles_two_choices_terminal_andtails_independently_reconstructed=True,target_block_sha256=sha(target),exact_research_block_equal=True,source_andcurrent_full_inverses_pass=True,no_ROM_mutation_oratomic_commit=True,semantic_mutations_independent_native_actual_atomic_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
