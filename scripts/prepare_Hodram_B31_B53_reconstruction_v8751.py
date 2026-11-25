"""Derive two-block production reconstruction from the unchanged sparse-inverse core."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_reconstruction_tools_v8751');assert not root.exists()
    old="""    require(group['block']==51 and len(rows)==5 and not group['choice_commands'],'exact B51 five-record no-menu scope')
    require(len(packet['all_current_commands'])==20 and sum(c['word'] in [0x8000,0x8100] for c in packet['all_current_commands'])==2 and not any(c['word']==0x2100 for c in packet['all_current_commands']),'complete20commands/twoqueries/no-menu')"""
    scope="""    require(group['block'] in [31,53],'exact two-block scope')
    number=group['block'];count=2 if number==31 else 1
    require(len(rows)==count and not group['choice_commands'],'complete source speech/no-menu scope')
    require(len(packet['all_current_commands'])==9 and len(group['all_target_commands'])==9,'complete9command block')
    require(sum(c['word'] in [0x8000,0x8100] for c in packet['all_current_commands'])==(1 if number==31 else 0) and not any(c['word']==0x2100 for c in packet['all_current_commands']),'complete original query/no-menu scope')
    require([(c['offset'],c['whole_command_hex'],c['native_extent']) for c in packet['all_current_commands'] if c['word']==0]==[(192 if number==31 else 132,'00000000',4)],'complete original normal end')
    require([(c['offset'],c['whole_command_hex'],c['native_extent']) for c in group['all_target_commands'] if c['word']==0]==[(224 if number==31 else 150,'00000000',4)],'complete target normal end')"""
    append="        patches.append(dict(start=at,end=at+len(before),old=before,source=raw,value=value,id=ident))"
    final="""        final=row['final_reference']
        require(final==dict(file_path=group['file_path'],block=group['block'],offset=ref['new_offset'],bytes=len(value),header_offset=ref['new_offset']-5,record_index=ref['new_record_index'],target_block_sha256=group['target_block_sha256']),'complete final source-qualified reference:'+ident)
"""+append
    receipt=derive('dk4tool/patch/hodram_B51_reconstruction_v1.py','dk4tool/patch/hodram_B31_B53_reconstruction_v1.py',{
        'Hodram B51 reconstruction:':'Hodram B31/B53 reconstruction:',old:scope,
        "len(selected)==len(group['relative_fixups'])==8":"len(selected)==len(group['relative_fixups'])==(4 if group['block']==31 else 0)",
        append:final,
        "        require(target[z:z+new['native_extent']].hex()==new['whole_command_hex'],'target full command bytes')":"        require(target[z:z+new['native_extent']].hex()==new['whole_command_hex'],'target full command bytes')\n        require(old[a:a+previous['native_extent']].hex()==previous['whole_command_hex'] and struct.unpack_from('<H',old,a)[0]==struct.unpack_from('<H',target,z)[0]==word,'exact original/target opcode andcomplete source command bytes')",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_native_high_integer_constants_andmultiplicity_preserved=True,
        original_sparse_body_replacement_relative_mapping_separate_tail_cachebounds_andfullclean_current_inverses_preserved=True,
        exact31_two_speeches_onequery_fourrelatives_normalend192to224_and53_one_speech_zeroqueries_zerorelatives_normalend132to150=True,
        stronger_final_row_reference_andliteral_command_opcode_sourcebyte_guards_added=True,
        no_approved_word_compiledbytes_layout_font_QA_orROM_change=True,new_credit=0,full_goal_complete=False))
