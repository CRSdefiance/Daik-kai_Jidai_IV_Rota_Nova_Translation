"""Prepare six-block speech/two-option relocation with both pause resumes."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/research_lil_B111_B119_relocation_v3239b.py');new=Path('scripts/research_lil_B122_B127_relocation_v3288b.py');assert not new.exists()
    text=old.read_text(encoding='utf-8')
    changes={
        'lil_B111_B119_relocation_v3239b':'lil_B122_B127_relocation_v3288b',
        'lil_B111_B119_editorial_manuscript_v5.json':'lil_B122_B127_editorial_manuscript_v5.json',
        "VOICE=Path('translations/lil_B111_B119_actor_style_manuscript_v4.json')":"VOICE=None",
        'MENU=None':"MENU=Path('translations/lil_B122_B127_choice_manuscript_v4.json')",
        'all_routes_combined_v3204_candidate.nds':'all_routes_combined_v3251_candidate.nds',
        "doc,voice=map(read,[DOC,VOICE]);menu={'records':[]}":"doc,menu=map(read,[DOC,MENU]);voice={'records':[]}",
        '0x2200':'0x2100',"[0,1,2]":"[0,1]","value[:2]==b'\\0\\x22'":"value[:2]==b'\\0\\x21'",
        'text_base=8,count=3':'text_base=6,count=2',"p=at+8+struct.unpack_from":"p=at+6+struct.unpack_from",
        'len(results)==9':'len(results)==6',"sum(len(r['text_records']) for r in results)==116":"sum(len(r['text_records']) for r in results)==155",
        "sum(len(r['actor_style_commands']) for r in results)==6":"sum(len(r['actor_style_commands']) for r in results)==0",
        "for c in r['actor_style_commands'])==34":"for c in r['actor_style_commands'])==0",
        "sum(len(r['choice_commands']) for r in results)==0":"sum(len(r['choice_commands']) for r in results)==2",
        "sum(len(r['command_map']) for r in results)==305":"sum(len(r['command_map']) for r in results)==312",
        'range(111,120)':'range(122,128)',
        'actor_styles=str(VOICE),actor_styles_sha256=sha(VOICE.read_bytes())':'choices=str(MENU),choices_sha256=sha(MENU.read_bytes())',
        'no_player_choice_objects=True':'two_original2100_menus_four_labels=True',
        'all116speech_34aliased_alternatives_no_choices_and64_relative_operands_preserved':'all155speech_four_choice_labels_and64_relative_operands_preserved',
        'all327_other_SC2_blocks_exact':'all330_other_SC2_blocks_exact'}
    for a,b in changes.items():assert a in text,a;text=text.replace(a,b)
    start=text.index('        if number==115:');end=text.index('        target_commands,target_speeches',start)
    text=text[:start]+text[end:]
    anchor='        restored=bytearray(target[:len(logical)])';assert text.count(anchor)==1
    text=text.replace(anchor,'''        pause_maps=[]
        for oldcmd in spec['all_current_native_commands']:
            if oldcmd['word']!=0x2000:continue
            start=mapped(oldcmd['offset']);resume=mapped(oldcmd['offset']+oldcmd['native_extent'])
            assert oldcmd['whole_command_hex']=='0020' and oldcmd['native_extent']==2
            assert target[start:start+2]==source[oldcmd['offset']:oldcmd['offset']+2]==b'\\0\\x20'
            assert resume==start+2 and resume in boundaries
            pause_maps.append(dict(old_offset=oldcmd['offset'],new_offset=start,source_resume=oldcmd['offset']+2,target_resume=resume,source_two_byte_pause_and_mapped_resumption_boundary_exact=True))
'''+anchor)
    anchor='            unowned_appended_copy=unowned,';assert anchor in text;text=text.replace(anchor,anchor+'original2000_pause_and_resume_maps=pause_maps,')
    anchor="    target_blocks=list(container.blocks)";assert anchor in text
    text=text.replace(anchor,"    assert sum(len(r['original2000_pause_and_resume_maps']) for r in results)==2\n"+anchor)
    anchor='        external_references_complete=False,';assert anchor in text
    text=text.replace(anchor,"        both_original2000_pause_words_and_mapped_resume_boundaries_exact=True,original2000_wait_proof=doc['original2000_wait_proof'],original2000_wait_proof_sha256=doc['original2000_wait_proof_sha256'],\n"+anchor)
    text=text[:text.rindex('    print(\'')]+"    print('312 physical commands/155 speeches/2 two-option menus/64 span fixups/320 skip cases;both2000 pause/resume boundaries,inverse bytes and330otherblocks exact. Research only.')\n"
    compile(text,str(new),'exec');new.write_text(text,encoding='utf-8')
    root=Path('work/analysis/lil_B122_B127_relocation_tools_v3288');root.mkdir(parents=True)
    save(root/'source_successor_provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),changes='155 direct speeches,two2100 menus/six-byte headers/four labels,64 spans,source2000 pause/resume mapping;six exact source/current blocks. No4100 or unowned copy targets.',no_previous_producer_changed=True,producer_sha256=sha(Path(__file__).read_bytes())))
