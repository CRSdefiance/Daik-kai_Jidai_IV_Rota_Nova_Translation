"""Relocate complete speech, actor-style and three-option objects with guards."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B165_relocation_v4032')
DOC=Path('translations/lil_B165_editorial_manuscript_v6.json')
VOICE=None
MENU=None
ROM=Path('out/all_routes_combined_v4002_candidate.nds')
OWNER,STREAM,RESULT,LENGTH=0x02650000,0x02660000,0x02668000,0x02668100

if __name__=='__main__':
    assert not ROOT.exists()
    doc,menu=read(DOC),{'records':[]};voice={'records':[]}
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    container=IlnkContainer.parse(image.read_file('/data/SC2.DK4'))
    fontpath=Path(doc['native_font_proof']);font=read(fontpath)
    assert sha(fontpath.read_bytes())==doc['native_font_proof_sha256']
    fonts={r['id']:r for r in font['cases']}
    context=read(doc['source_context']);branches=read(doc['branch_proof'])
    inventory,walker,inventory_source=scoped_inventory()
    cpu=machine(arm);results=[];ROOT.mkdir(parents=True)
    (ROOT/'explicit_unmatched_native_walk.py.txt').write_text(walker,encoding='utf-8')
    for spec in context['blocks']:
        number=spec['block'];source=container.blocks[number];old_end=8+struct.unpack_from('<H',source,4)[0]
        assert sha(source)==spec['current_block_sha256']
        patches=[];texts=[];styles=[];choices=[]
        for row in doc['records']:
            if row['block']!=number:continue
            at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex'])
            assert source[at:at+len(old)]==old
            value=bytes.fromhex(fonts[row['id']]['encoded_hex'])
            pad=len(value)%2!=len(old)%2
            if pad:value+=b' '
            assert b'\0' not in value and value[:1]==old[:1] and len(value)%2==len(old)%2
            patches.append(dict(start=at,end=at+len(old),value=value,old=old,kind='speech',id=row['id']))
            texts.append(dict(id=row['id'],record_index=row['current_record_index'],old_offset=at,
                old_length=len(old),new_length=len(value),parity_space_added=pad,target_hex=value.hex()))
        for command in spec['all_current_native_commands']:
            word,at=command['word'],command['offset']
            if word not in [0x4100,0x2100]:continue
            old=bytes.fromhex(command['whole_command_hex'])
            assert source[at:at+len(old)]==old and len(old)==command['native_extent']
            if word==0x4100:
                rows=sorted([r for r in voice['records'] if r['block']==number and r['command_offset']==at],key=lambda r:r['current_reference']['offset'])
                assert rows and sum(len(r['style_indices']) for r in rows)==8
                assert old[:2]==b'\0\x41' and old[18]==0 and all(r['source_selector']==old[19] for r in rows)
                table=[None]*8;chunks=[];cursor=0;alternatives=[]
                oldtable=list(struct.unpack_from('<8H',old,2))
                for row in rows:
                    value=bytes.fromhex(row['compiled_stored_alternative_hex'])
                    assert fonts[row['id']]['encoded_hex']==format(old[19],'02x')+value.hex() and b'\0' not in value
                    ref=row['current_reference'];relative=ref['offset']-at
                    assert source[ref['offset']:ref['offset']+ref['bytes']].hex()==row['current_hex']
                    assert [i for i,v in enumerate(oldtable) if v+20==relative]==row['style_indices']
                    for index in row['style_indices']:
                        assert table[index] is None
                        table[index]=cursor
                    chunk=value+b'\0';chunk+=b'\0'*(-len(chunk)%2)
                    chunks.append(chunk)
                    alternatives.append(dict(id=row['id'],style_indices=row['style_indices'],old_offset=ref['offset'],
                        old_length=ref['bytes'],new_relative_offset=20+cursor,new_length=len(value),
                        target_hex=value.hex(),actual_virtual_prefix_excluded_from_stored_body=True))
                    cursor+=len(chunk)
                assert all(isinstance(v,int) for v in table)
                assert all((oldtable[i]==oldtable[j])==(table[i]==table[j]) for i in range(8) for j in range(8))
                value=old[:2]+struct.pack('<8H',*table)+old[18:20]+b''.join(chunks)
                assert len(value)%2==0 and value[18:20]==old[18:20]
                styles.append(dict(old_offset=at,old_length=len(old),new_length=len(value),target_hex=value.hex(),
                    old_style_offsets=oldtable,new_style_offsets=table,source_header_selector_hex=old[18:20].hex(),
                    aliases_and_all8_style_indices_preserved=True,alternative_records=alternatives))
                kind='actor-style'
            else:
                rows=sorted([r for r in menu['records'] if r['block']==number and r['command_offset']==at],key=lambda r:r['option_index'])
                assert [r['option_index'] for r in rows]==[0,1]
                value=bytes.fromhex(rows[0]['typed_target_object_hex'])
                assert all(r['typed_target_object_hex']==value.hex() for r in rows) and value[:2]==b'\0\x21'
                labels=[r['english'] for r in rows]
                choices.append(dict(old_offset=at,old_length=len(old),new_length=len(value),labels=labels,
                    target_hex=value.hex(),text_base=6,count=2,record_IDs=[r['id'] for r in rows]))
                kind='choice'
            patches.append(dict(start=at,end=at+len(old),value=value,old=old,kind=kind,id=f'B{number}_{kind}_{at}'))
        patches.sort(key=lambda p:p['start'])
        assert all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
        def mapped(offset):
            delta=0
            for p in patches:
                if offset<p['start']:break
                if p['start']<offset<p['end']:raise ValueError('Interior reference into complete replaced object:'+str(offset))
                if offset==p['start']:return offset+delta
                delta+=len(p['value'])-(p['end']-p['start'])
            return offset+delta
        parts=[];last=0
        for p in patches:parts.extend([source[last:p['start']],p['value']]);last=p['end']
        parts.append(source[last:old_end]);logical=bytearray(b''.join(parts))
        assert len(logical)==mapped(old_end) and len(logical)<0x2400
        fixups=[]
        for edge in branches['operands_requiring_adjustment_when_resizing']:
            if edge['block']!=number:continue
            start=mapped(edge['offset']);target=mapped(edge['matched_skip_target']);span=target-start-4
            assert 0<=span<=0xFFFF and span%2==0 and struct.unpack_from('<H',logical,start)[0]==edge['word']
            old_span=struct.unpack_from('<H',source,edge['span_field_offset'])[0]
            struct.pack_into('<H',logical,start+2,span)
            fixups.append({**edge,'new_offset':start,'new_unmatched_next':start+4,'new_matched_skip_target':target,
                'source_span':old_span,'target_span':span})
        struct.pack_into('<H',logical,4,len(logical)-8)
        target=bytes(logical)+b'\0'*(-len(logical)%4)
        unowned=None
        target_commands,target_speeches=inventory(arm,target)
        assert len(target_commands)==len(spec['all_current_native_commands']) and len(target_speeches)==sum(c['word']==0x4000 for c in spec['all_current_native_commands'])
        boundaries={r['offset'] for r in target_commands}|{len(logical)}
        by_offset={r['offset']:r for r in target_commands};command_map=[]
        for old in spec['all_current_native_commands']:
            new=by_offset[mapped(old['offset'])]
            assert new['word']==old['word']
            assert new['ancestor_0100_offsets']==[mapped(a) for a in old['ancestor_0100_offsets']]
            if old['word'] not in [0x100,0x200,0x300,0x400,0x4000,0x4100,0x2100]:
                assert source[old['offset']:old['offset']+old['native_extent']]==target[new['offset']:new['offset']+new['native_extent']]
            command_map.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],
                old_extent=old['native_extent'],new_extent=new['native_extent']))
        cases=[]
        cpu.mem_write(STREAM-16,b'\xa5'*(len(target)+32));cpu.mem_write(STREAM,target)
        main_before=bytes(cpu.mem_read(0x02000000,0x400000))
        for edge in fixups:
            assert edge['new_unmatched_next'] in boundaries and edge['new_matched_skip_target'] in boundaries
            for choice in [0,1,2,3,0xFFFFFFFF]:
                cpu.mem_write(OWNER-16,b'\xa5'*64);cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+edge['new_offset'],0,0))
                owner_before=bytes(cpu.mem_read(OWNER-16,64))
                cpu.mem_write(RESULT-16,b'\xa5'*64);cpu.mem_write(RESULT,bytes(24))
                cpu.mem_write(LENGTH-16,b'\xa5'*36);cpu.mem_write(LENGTH,bytes(4))
                call(cpu,0x2A510,(RESULT,OWNER,LENGTH,choice))
                extent=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0]
                take=edge['word']==0x100 or (edge['word']==0x200 and choice==0) or (edge['word']==0x300 and choice==1) or (edge['word']==0x400 and choice==2)
                assert edge['new_offset']+extent==(edge['new_matched_skip_target'] if take else edge['new_unmatched_next'])
                assert struct.unpack('<6I',cpu.mem_read(RESULT,24))==(3,0,0,0,0,0)
                assert bytes(cpu.mem_read(OWNER-16,64))==owner_before
                assert bytes(cpu.mem_read(STREAM,len(target)))==target and bytes(cpu.mem_read(0x02000000,0x400000))==main_before
                for p in [STREAM-16,STREAM+len(target),RESULT-16,RESULT+24,LENGTH-16,LENGTH+4]:
                    assert bytes(cpu.mem_read(p,16))==b'\xa5'*16
                cases.append(dict(new_offset=edge['new_offset'],last_result=choice,native_extent=extent,
                    source_target_preserved_at_mapped_native_boundary=True,ABI_all4MiB_owner_stream_result_length_and_guards_exact=True))
        for row in texts:
            row['new_offset']=mapped(row['old_offset']);at=row['new_offset']
            row['new_record_index']=target[:at].count(b'\0')
            assert target[at-5:at]==source[row['old_offset']-5:row['old_offset']]==b'\0\x40\xff\xff\0'
            assert target[at:at+row['new_length']].hex()==row['target_hex'] and target[at+row['new_length']]==0
        for row in styles+choices:
            row['new_offset']=mapped(row['old_offset']);at=row['new_offset'];value=bytes.fromhex(row['target_hex'])
            assert target[at:at+len(value)]==value
            if 'alternative_records' in row:
                for r in row['alternative_records']:
                    r['new_offset']=at+r['new_relative_offset'];r['new_record_index']=target[:r['new_offset']].count(b'\0')
                    assert target[r['new_offset']:r['new_offset']+r['new_length']].hex()==r['target_hex']
                    assert target[r['new_offset']+r['new_length']]==0
            else:
                row['label_references']=[]
                for i,label in enumerate(row['labels']):
                    p=at+6+struct.unpack_from('<H',target,at+2+i*2)[0]
                    assert target[p:target.index(b'\0',p)].decode('ascii')==label
                    row['label_references'].append(dict(id=row['record_IDs'][i],option_index=i,new_offset=p,new_length=len(label),
                        new_record_index=target[:p].count(b'\0')))
        pause_maps=[]
        for oldcmd in spec['all_current_native_commands']:
            if oldcmd['word']!=0x2000:continue
            start=mapped(oldcmd['offset']);resume=mapped(oldcmd['offset']+oldcmd['native_extent'])
            assert oldcmd['whole_command_hex']=='0020' and oldcmd['native_extent']==2
            assert target[start:start+2]==source[oldcmd['offset']:oldcmd['offset']+2]==b'\0\x20'
            assert resume==start+2 and resume in boundaries
            pause_maps.append(dict(old_offset=oldcmd['offset'],new_offset=start,source_resume=oldcmd['offset']+2,target_resume=resume,source_two_byte_pause_and_mapped_resumption_boundary_exact=True))
        end_maps=[]
        for oldcmd in spec['all_current_native_commands']:
            if oldcmd['word']!=0:continue
            at=oldcmd['offset'];new=mapped(at)
            assert oldcmd['native_extent']==4 and source[at:at+4]==target[new:new+4]==bytes(4)
            end_maps.append(dict(source_offset=at,target_offset=new,extent=4,source_four_zero_bytes_exact=True))
        assert len(end_maps)==(2 if number==163 else 1)
        assert end_maps[-1]['source_offset']+4==old_end and end_maps[-1]['target_offset']+4==len(logical)
        if number==163:assert end_maps[0]['target_offset']+4==end_maps[1]['target_offset']
        restored=bytearray(target[:len(logical)]);struct.pack_into('<H',restored,4,old_end-8)
        for edge in fixups:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
        for p in reversed(patches):
            at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
        assert bytes(restored)==source[:old_end]
        file=ROOT/f'SC2_block{number:03d}_RESEARCH_ONLY.bin';file.write_bytes(target)
        results.append(dict(block=number,source_block_sha256=sha(source),research_block_sha256=sha(target),
            source_bytes=len(source),research_bytes=len(target),source_logical_end=old_end,research_logical_end=len(logical),
            unowned_appended_copy=unowned,original2000_pause_and_resume_maps=pause_maps,
            original_declared_end_word_maps=end_maps,
            text_records=texts,actor_style_commands=styles,choice_commands=choices,relative_skip_fixups=fixups,
            target_native_skip_cases=cases,command_map=command_map,
            all_nested_original_command_types_ancestors_and_opaque_bytes_preserved=True,
            inverse_restoration_recovers_every_original_logical_byte=True,research_block=str(file),
            external_entry_and_actual_revised_paths_approval_pending=True))
    assert len(results)==1 and sum(len(r['text_records']) for r in results)==24
    assert sum(len(r['actor_style_commands']) for r in results)==0 and sum(len(c['alternative_records']) for r in results for c in r['actor_style_commands'])==0
    assert sum(len(r['choice_commands']) for r in results)==0 and sum(len(r['relative_skip_fixups']) for r in results)==20
    assert sum(len(r['target_native_skip_cases']) for r in results)==100 and sum(len(r['command_map']) for r in results)==56
    assert sum(len(r['original2000_pause_and_resume_maps']) for r in results)==0
    target_blocks=list(container.blocks)
    for block in results:target_blocks[block['block']]=Path(block['research_block']).read_bytes()
    assert all(old==new for n,(old,new) in enumerate(zip(container.blocks,target_blocks,strict=True)) if n not in [165])
    prospective=IlnkContainer(target_blocks).to_bytes();target_file=ROOT/'SC2_RESEARCH_ONLY.DK4';target_file.write_bytes(prospective)
    save(ROOT/'nested_source_relocation_research.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=None,choices_sha256=None,
        no_original2100_objects=True,source_context=doc['source_context'],source_branch_proof=doc['branch_proof'],
        target_SC2=str(target_file),target_SC2_sha256=sha(prospective),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        blocks=results,all24speech_and20_relative_operands_preserved=True,
        all100_relocated_native_skip_cases_match_original_target_mapping=True,all335_other_SC2_blocks_exact=True,
        explicit_unmatched_native_walk=walker,unchanged_inventory_function=inventory_source,
        predicates_typed_dispatch_final_parity_fonts_external_references_and_sampling_pending=True,
        no_source2000_commands=True,source_FE_system_objects=0,no_source00_or_dynamic_objects=True,
        one_declared_end_word_at_logical_tail_exact=True,
        external_references_complete=False,not_a_release_relocation_map=True,no_ROM_registry_or_completion_change=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print([(r['block'],r['source_bytes'],r['research_bytes'],len(r['relative_skip_fixups'])) for r in results],flush=True)
    print('56commands/24speech/20spans/100targetskipcases,one endword,inversebytes and335otherblocks exact. Researchonly.')
