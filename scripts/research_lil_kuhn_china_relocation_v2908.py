"""Research218 speech replacements and160 original relative operands in nine blocks."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_China_relocation_v2908')
ROM=Path('out/all_routes_combined_v2883_candidate.nds')
OWNER,STREAM,RESULT,LENGTH=0x02650000,0x02660000,0x02668000,0x02668100


if __name__=='__main__':
    assert not ROOT.exists()
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin')
    container=IlnkContainer.parse(image.read_file('/data/SC2.DK4'))
    doc=read('translations/lil_kuhn_china_editorial_manuscript_v6.json')
    font=read('work/analysis/lil_Kuhn_China_fonts_v2904/current_macro_QA_and_progressive_font_proof.json')
    assert sha(Path(font['manuscript']).read_bytes())==font['manuscript_sha256']
    fe=read('work/analysis/lil_Kuhn_China_FE_v2901b/current_FE_macro_font_and_typed_paper_proof.json');fonts={r['id']:r for r in font['cases']+fe['cases']}
    context=read('work/analysis/lil_Kuhn_China_connected_source_v2891/complete218_clean_current_native_context.json')
    packet={'blocks':[dict(block=b['block'],all_nested_native_commands=b['all_current_native_commands'],choices=[dict(offset=c['current_command']['offset'],current_hex=c['current_command']['whole_command_hex'],source_hex=c['source_command']['whole_command_hex']) for c in b['choices']]) for b in context['blocks']]}
    branches=read('work/analysis/lil_Kuhn_China_branches_v2892/original_relative_skip_operand_proof.json')
    cpu=machine(arm);results=[]
    ROOT.mkdir(parents=True)
    for spec in packet['blocks']:
        number=spec['block'];source=container.blocks[number];old_end=8+struct.unpack_from('<H',source,4)[0]
        patches=[];texts=[];choices=[]
        for row in doc['records']:
            if row['block']!=number:continue
            at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex'])
            assert source[at:at+len(old)]==old
            value=bytes.fromhex(fonts[row['id']]['encoded_hex']);pad=len(value)%2!=len(old)%2
            if pad:value+=b' '
            assert b'\0' not in value and value[:1]==old[:1] and len(value)%2==len(old)%2
            patches.append({'start':at,'end':at+len(old),'value':value,'old':old,'kind':'speech','id':row['id']})
            texts.append({'id':row['id'],'record_index':row['current_record_index'],'old_offset':at,
                'old_length':len(old),'new_length':len(value),'parity_space_added':pad,'target_hex':value.hex()})
        patches.sort(key=lambda p:p['start']);assert all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
        def mapped(offset):
            delta=0
            for p in patches:
                if offset<p['start']:break
                if p['start']<offset<p['end']:raise ValueError('Unclassified interior reference into replaced text:'+str(offset))
                if offset==p['start']:return offset+delta
                delta+=len(p['value'])-(p['end']-p['start'])
            return offset+delta
        parts=[];last=0
        for p in patches:
            parts.extend((source[last:p['start']],p['value']));last=p['end']
        parts.append(source[last:old_end]);logical=bytearray(b''.join(parts))
        assert len(logical)==mapped(old_end) and len(logical)<0x2400
        fixups=[]
        for edge in branches['operands_requiring_adjustment_when_resizing']:
            if edge['block']!=number:continue
            start=mapped(edge['offset']);target=mapped(edge['matched_skip_target']);span=target-start-4
            assert 0<=span<=0xFFFF and span%2==0
            assert struct.unpack_from('<H',logical,start)[0]==edge['word']
            old_span=struct.unpack_from('<H',source,edge['span_field_offset'])[0]
            struct.pack_into('<H',logical,start+2,span)
            fixups.append({**edge,'new_offset':start,'new_unmatched_next':start+4,
                'new_matched_skip_target':target,'source_span':old_span,'target_span':span})
        struct.pack_into('<H',logical,4,len(logical)-8)
        target=bytes(logical)+b'\0'*(-len(logical)%4)
        target_commands,target_speeches=inventory(arm,target)
        all_boundaries={r['offset'] for r in target_commands}|{len(logical)}
        assert len(target_commands)==len(spec['all_nested_native_commands'])
        by_offset={r['offset']:r for r in target_commands}
        for old in spec['all_nested_native_commands']:
            new=by_offset[mapped(old['offset'])]
            assert new['word']==old['word']
            assert new['ancestor_0100_offsets']==[mapped(a) for a in old['ancestor_0100_offsets']]
            if old['word'] not in (0x100,0x200,0x300,0x2100,0x4000):
                assert source[old['offset']:old['offset']+old['native_extent']]==target[new['offset']:new['offset']+new['native_extent']]
        assert len(target_speeches)==len(texts)
        cases=[]
        cpu.mem_write(STREAM-16,b'\xA5'*(len(target)+32));cpu.mem_write(STREAM,target)
        for edge in fixups:
            assert edge['new_unmatched_next'] in all_boundaries and edge['new_matched_skip_target'] in all_boundaries
            for choice in (0,1,2,3,0xFFFFFFFF):
                cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+edge['new_offset'],0,0))
                cpu.mem_write(RESULT,bytes(24));cpu.mem_write(LENGTH,bytes(4))
                call(cpu,0x2A510,(RESULT,OWNER,LENGTH,choice))
                extent=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0]
                take=edge['word']==0x100 or(edge['word']==0x200 and choice==0)or(edge['word']==0x300 and choice==1)
                assert edge['new_offset']+extent==(edge['new_matched_skip_target'] if take else edge['new_unmatched_next'])
                assert struct.unpack('<6I',cpu.mem_read(RESULT,24))==(3,0,0,0,0,0)
                assert bytes(cpu.mem_read(STREAM,len(target)))==target
                cases.append({'new_offset':edge['new_offset'],'last_result':choice,'native_extent':extent,
                    'source_target_preserved_at_mapped_native_boundary':True})
        for row in texts:
            row['new_offset']=mapped(row['old_offset']);at=row['new_offset']
            assert target[at-5:at]==source[row['old_offset']-5:row['old_offset']]==b'\0\x40\xff\xff\0'
            assert target[at:at+row['new_length']].hex()==row['target_hex']
        for row in choices:
            row['new_offset']=mapped(row['old_offset']);at=row['new_offset'];value=bytes.fromhex(row['target_hex'])
            assert target[at:at+len(value)]==value
            for index,label in enumerate(row['labels']):
                label_at=at+6+struct.unpack_from('<H',target,at+2+index*2)[0]
                assert target[label_at:target.index(b'\0',label_at)].decode('ascii')==label
        # Inverse restore proves every unowned source byte and opaque command survived.
        restored=bytearray(target[:len(logical)]);struct.pack_into('<H',restored,4,old_end-8)
        for edge in fixups:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
        for p in reversed(patches):
            at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
        assert bytes(restored)==source[:old_end]
        file=ROOT/f'SC2_block{number:03d}_RESEARCH_ONLY.bin';file.write_bytes(target)
        results.append({'block':number,'source_block_sha256':sha(source),'research_block_sha256':sha(target),
            'source_bytes':len(source),'research_bytes':len(target),'source_logical_end':old_end,'research_logical_end':len(logical),
            'text_records':texts,'choice_commands':choices,'relative_skip_fixups':fixups,'target_native_skip_cases':cases,
            'all_nested_original_command_types_ancestors_and_opaque_bytes_preserved':True,
            'inverse_restoration_recovers_every_original_logical_byte':True,
            'research_block':str(file),'external_entry_and_actual_revised_paths_approval_pending':True})
    assert len(results)==9 and sum(len(r['text_records']) for r in results)==218 and sum(len(r['relative_skip_fixups']) for r in results)==160 and sum(len(r['target_native_skip_cases']) for r in results)==800
    target_blocks=list(container.blocks)
    for block in results:target_blocks[block['block']]=Path(block['research_block']).read_bytes()
    prospective=IlnkContainer(target_blocks).to_bytes();target_file=ROOT/'SC2_RESEARCH_ONLY.DK4';target_file.write_bytes(prospective)
    assert all(old==new for n,(old,new) in enumerate(zip(container.blocks,target_blocks,strict=True)) if n not in [51,52,53,54,55,56,146,147,148])
    save(ROOT/'nested_source_relocation_research.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'manuscript':'translations/lil_kuhn_china_editorial_manuscript_v6.json','manuscript_sha256':sha(Path('translations/lil_kuhn_china_editorial_manuscript_v6.json').read_bytes()),
        'source_branch_proof':'work/analysis/lil_Kuhn_China_branches_v2892/original_relative_skip_operand_proof.json',
        'target_SC2':str(target_file),'target_SC2_sha256':sha(prospective),'source_SC2_sha256':sha(image.read_file('/data/SC2.DK4')),'blocks':results,'all218_texts_and160_relative_operands_preserved':True,
        'all800_relocated_native_skip_cases_match_original_target_mapping':sum(len(r['target_native_skip_cases']) for r in results)==800,
        'external_references_final_padding_and_representative_approval_pending':True,
        'external_references_complete':False,'not_a_release_relocation_map':True,'no_ROM_registry_or_completion_change':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print([(r['block'],r['source_bytes'],r['research_bytes'],len(r['relative_skip_fixups'])) for r in results],flush=True)
