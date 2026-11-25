"""Derive strict independent B50 production reconstruction without a nonexistent menu."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_rebuild_tools_v8518');assert not root.exists()
    source=Path('dk4tool/patch/hodram_B49_reconstruction_v2.py').read_text(encoding='utf-8')
    a=source.index("    require(len(group['choice_commands'])");b=source.index("    patches.sort(",a)
    c=source.index("    require(mapped(choice['old_offset'])");d=source.index('    for clean_version in [False,True]:',c)
    result=derive('dk4tool/patch/hodram_B49_reconstruction_v2.py','dk4tool/patch/hodram_B50_reconstruction_v1.py',{
        'Hodram B49 reconstruction:':'Hodram B50 reconstruction:',
        'def reconstruct(old,clean,group,packet,rows,edges,choice_rows,typed):':'def reconstruct(old,clean,group,packet,rows,edges):',
        "    end=8+struct.unpack_from('<H',old,4)[0]":"    require(group['block']==50 and len(rows)==3 and not edges and not group['relative_fixups'],'exact B50 three-record no-relative scope')\n    require(len(packet['all_current_commands'])==12 and all(c['word'] not in [0x100,0x200,0x300,0x400,0x2100,0x8000,0x8100] for c in packet['all_current_commands']),'complete12commands without query or menu')\n    end=8+struct.unpack_from('<H',old,4)[0]",
        source[a:b]:'',source[c:d]:'',
        "        elif word==0x2100:require(a==choice['old_offset'] and z==choice['new_offset'] and target[z:z+new['native_extent']]==typed,'complete original-provider menu')\n":'',
    })
    from dk4tool.patch.hodram_B50_reconstruction_v1 import reconstruct
    mapping=read('work/analysis/Hodram_B50_references_v8503/source_current_final_map.json');packet=read('work/analysis/Hodram_B50_current_v8488/current_effective.json')['groups'][0]
    doc=read('translations/hodram_B50_editorial_manuscript_v5.json');group=mapping['groups'][0]
    target=reconstruct(bytes.fromhex(packet['current_block_hex']),bytes.fromhex(packet['clean_block_hex']),group,packet,doc['records'],[])
    assert target==Path(group['target_block']).read_bytes() and sha(target)==group['target_block_sha256']
    root.mkdir(parents=True);save(root/'independent_reconstruction_positive.json',dict(derivation=result,all_source_current_controls_preambles_zero_relative_query_choice_sites_terminal_tail_andinverse_guards_preserved=True,target_block_sha256=sha(target),entire_research_block_byte_exact=True,source_andcurrent_full_block_inverse_exact=True,no_ROM_mutation_oratomic_commit=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('work/analysis/Hodram_B50_references_v8503/source_current_final_map.json'),Path('work/analysis/Hodram_B50_current_v8488/current_effective.json'),Path('translations/hodram_B50_editorial_manuscript_v5.json')]}))
    print('Independent B50 production reconstruction equals complete tested block;all12commands/3preambles/end/tails andboth full inverses pass.No ROM commit.')
