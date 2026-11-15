"""Rebuild all20 draft objects, original typed aliases and four source-relative operands reversibly."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B214_relocation_v6716')
DOC=Path('translations/lil_B214_editorial_manuscript_v1.json')
SOURCE=Path('work/analysis/lil_B214_source_v6697/all17_clean_current_letter_notices_reactions_full1316_inverse.json')
FONT=Path('work/analysis/lil_B214_native_pages_v6706/all17_complete_single_pages136_native_alignments.json')
CONTROL=Path('work/analysis/lil_B214_controls_v6708/four_unforced_predicates_ten_structural_cases50_seeded_ends_four_route_models.json')
VIEW=Path('work/analysis/lil_B214_view_v6711/seventeen_native_pages_eleven_names_nine_source_panels_and_scope_viewed.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,source,font,control,view=map(read,[DOC,SOURCE,FONT,CONTROL,VIEW]);assert font['manuscript_sha256']==sha(DOC.read_bytes()) and not view['visual_review_pending']
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256'];arm=image.read_file('/__arm9__.bin');file=image.read_file('/data/SC2.DK4');bank=IlnkContainer.parse(file).blocks;block=bank[214];spec=source['blocks'][0]
    inventory,walker,inventory_source=scoped_inventory();old_commands,old_speeches=inventory(arm,block)
    assert old_commands==spec['all_current_native_commands'] and len(old_commands)==27 and len(old_speeches)==10 and len(block)==1316 and block[1310:]==bytes(6)
    fonts={r['id']:r for r in font['records']};patches=[];texts=[];styles=[]
    for row in doc['records']:
        if row['kind']!='progressive':continue
        at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex']);assert block[at:at+len(old)+1]==old+b'\0'
        value=bytes.fromhex(fonts[row['id']]['compiled_hex']);pad=len(value)%2!=len(old)%2
        if pad:value+=b' '
        assert value[0]==old[0]==row['source_selector'] and b'\0' not in value and len(value)%2==len(old)%2
        patches.append(dict(start=at,end=at+len(old),old=old,value=value,id=row['id'],kind='speech'))
        texts.append(dict(id=row['id'],old_offset=at,old_length=len(old),new_length=len(value),target_hex=value.hex(),parity_space_added=pad))
    for obj in spec['actor_style_objects']:
        at=obj['command_offset'];old=bytes.fromhex(obj['current_command']['whole_command_hex']);assert block[at:at+len(old)]==old and old[18:20]==b'\0\xd0'
        rows=sorted([r for r in doc['records'] if r['kind']!='progressive' and r['command_offset']==at],key=lambda r:r['current_reference']['offset']);table=[None]*8;chunks=[];cursor=0;alternatives=[];oldtable=list(struct.unpack_from('<8H',old,2))
        for row in rows:
            compiled=bytes.fromhex(fonts[row['id']]['compiled_hex']);assert compiled[0]==208;value=compiled[1:];ref=row['current_reference'];assert block[ref['offset']:ref['offset']+ref['bytes']].hex()==row['current_hex'] and b'\0' not in value
            assert [i for i,v in enumerate(oldtable) if v+20==ref['offset']-at]==row['style_indices']
            for style in row['style_indices']:assert table[style] is None;table[style]=cursor
            chunk=value+b'\0';chunk+=bytes(-len(chunk)%2);chunks.append(chunk)
            alternatives.append(dict(id=row['id'],old_offset=ref['offset'],old_length=ref['bytes'],style_indices=row['style_indices'],new_relative_offset=20+cursor,new_length=len(value),target_hex=value.hex(),virtual_D0_excluded_from_stored_body=True));cursor+=len(chunk)
        assert all(isinstance(v,int) for v in table) and all((oldtable[i]==oldtable[j])==(table[i]==table[j]) for i in range(8) for j in range(8))
        value=old[:2]+struct.pack('<8H',*table)+old[18:20]+b''.join(chunks);assert len(value)%2==0
        patches.append(dict(start=at,end=at+len(old),old=old,value=value,id=f'B214_style_{at}',kind='actor-style'))
        styles.append(dict(old_offset=at,old_length=len(old),new_length=len(value),target_hex=value.hex(),old_style_offsets=oldtable,new_style_offsets=table,source_selector_header_hex=old[18:20].hex(),alternative_records=alternatives))
    patches.sort(key=lambda p:p['start']);assert len(patches)==11 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            if p['start']<offset<p['end']:raise ValueError('Undeclared interior reference into replaced body:'+str(offset))
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-len(p['old'])
        return offset+delta
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:1314]);logical=bytearray(b''.join(pieces));assert len(logical)==mapped(1314)<0x2400;fixups=[]
    for original_edge in read(control['eight_relative_sites80_native_cases'])['operands_requiring_adjustment_when_resizing']:
        edge=dict(offset=original_edge['offset'],word=original_edge['word'],span=original_edge['matched_skip_target']-original_edge['offset']-4,fallthrough=original_edge['unmatched_next_offset'],skip_target=original_edge['matched_skip_target'])
        at=mapped(edge['offset']);target=mapped(edge['skip_target']);span=target-at-4;assert 0<=span<=0xFFFF and span%2==0 and struct.unpack_from('<H',logical,at)[0]==edge['word']
        struct.pack_into('<H',logical,at+2,span);fixups.append(dict(**edge,new_offset=at,new_fallthrough=at+4,new_skip_target=target,new_span=span))
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4);commands,speeches=inventory(arm,target);assert len(commands)==27 and len(speeches)==10;by={c['offset']:c for c in commands};maps=[]
    for old in old_commands:
        new=by[mapped(old['offset'])];assert new['word']==old['word'] and new['ancestor_0100_offsets']==[mapped(a) for a in old['ancestor_0100_offsets']] and mapped(old['offset']+old['native_extent'])==new['offset']+new['native_extent']
        if old['word'] not in [0x100,0x200,0x300,0x400,0x4000,0x4100]:assert old['whole_command_hex']==new['whole_command_hex']
        if old['word']==0x4000:assert block[old['offset']:old['offset']+6]==target[new['offset']:new['offset']+6]
        maps.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],old_extent=old['native_extent'],new_extent=new['native_extent']))
    boundaries=set(by)|{len(logical)};cases=[];cpu=machine(arm);cpu.mem_write(0x02660000-16,b'\xa5'*(len(target)+32));cpu.mem_write(0x02660000,target);before=bytes(cpu.mem_read(0x02000000,0x400000))
    for edge in fixups:
        assert edge['new_fallthrough'] in boundaries and edge['new_skip_target'] in boundaries
        for previous in [0,1,2,3,0xFFFFFFFF]:
            owner,result,length=0x02650000,0x02668000,0x02668100;cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<4I',0,0x02660000+edge['new_offset'],0,0));guard=bytes(cpu.mem_read(owner-16,64));cpu.mem_write(result-16,b'\xa5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xa5'*36);cpu.mem_write(length,bytes(4));call(cpu,0x2A510,(result,owner,length,previous));extent=struct.unpack('<I',cpu.mem_read(length,4))[0]
            take=edge['word']==0x100 or (edge['word']==0x200 and previous==0) or (edge['word']==0x300 and previous==1) or (edge['word']==0x400 and previous==2)
            assert edge['new_offset']+extent==(edge['new_skip_target'] if take else edge['new_fallthrough']) and struct.unpack('<6I',cpu.mem_read(result,24))==(3,0,0,0,0,0)
            assert bytes(cpu.mem_read(0x02000000,0x400000))==before and bytes(cpu.mem_read(0x02660000,len(target)))==target and bytes(cpu.mem_read(owner-16,64))==guard
            for p in [0x02660000-16,0x02660000+len(target),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(p,16))==b'\xa5'*16
            cases.append(dict(new_offset=edge['new_offset'],previous_value=previous,extent=extent,target_is_mapped_original_boundary=True,all_ABI_actor_RNG_4MiB_and_canaries_exact=True))
    for row in texts:
        row.update(new_offset=mapped(row['old_offset']),new_record_index=target[:mapped(row['old_offset'])].count(b'\0'));at=row['new_offset'];assert target[at:at+row['new_length']+1]==bytes.fromhex(row['target_hex'])+b'\0'
    for obj in styles:
        obj['new_offset']=mapped(obj['old_offset']);assert target[obj['new_offset']:obj['new_offset']+obj['new_length']].hex()==obj['target_hex']
        for row in obj['alternative_records']:
            row.update(new_offset=obj['new_offset']+row['new_relative_offset']);row['new_record_index']=target[:row['new_offset']].count(b'\0');assert target[row['new_offset']:row['new_offset']+row['new_length']+1]==bytes.fromhex(row['target_hex'])+b'\0'
    inverse=bytearray(logical);struct.pack_into('<H',inverse,4,1306)
    for edge in fixups:struct.pack_into('<H',inverse,edge['new_offset']+2,edge['span'])
    for p in reversed(patches):at=mapped(p['start']);inverse[at:at+len(p['value'])]=p['old']
    assert bytes(inverse)+block[1314:]==block and target[mapped(1310):mapped(1310)+4]==bytes(4) and mapped(1310)+4==len(logical)
    ROOT.mkdir(parents=True);bp=ROOT/'SC2_block214_RESEARCH_ONLY.bin';bp.write_bytes(target);newbank=list(bank);newbank[214]=target;data=IlnkContainer(newbank).to_bytes();sp=ROOT/'SC2_RESEARCH_ONLY.DK4';sp.write_bytes(data);assert [i for i,(a,b) in enumerate(zip(bank,IlnkContainer.parse(data).blocks,strict=True)) if a!=b]==[214]
    save(ROOT/'all17_object_relocation_RESEARCH_ONLY.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=str(SOURCE),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),target_SC2=str(sp),target_SC2_sha256=sha(data),source_SC2_sha256=sha(file),blocks=[dict(block=214,source_block_sha256=sha(block),research_block_sha256=sha(target),source_bytes=len(block),research_bytes=len(target),source_logical_end=1314,research_logical_end=len(logical),source_tail_bytes=2,research_tail_bytes=len(target)-len(logical),research_block=str(bp),text_records=texts,actor_style_commands=styles,choice_commands=[],relative_skip_fixups=fixups,target_native_skip_cases=cases,command_map=maps,all27_commands10_preambles7_bodies8_slots_and_aliases_preserved=True,inverse_recovers_every_original1316_byte=True,complete_end_map=dict(source_offset=1310,target_offset=mapped(1310),extent=4))],all335_other_blocks_exact=True,source_typed_virtual_prefixes_not_stored=True,external_references_complete=False,not_release_approved_relocation_map=True,final_stored_native_planes_external_entries_loaders_actual_pages_and_atomic_release_pending=True,manuscript_formatting_gates_still_false=True,explicit_unmatched_native_walk=walker,unchanged_inventory_function=inventory_source,new_review_credit=0,new_ROMs=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,SOURCE,FONT,CONTROL,VIEW,Path(__file__)]},full_goal_complete=False))
    print(dict(source=1316,target_stored=len(target),target_logical=len(logical),tail=len(target)-len(logical),commands=len(commands),speech_objects=10,stored_style_bodies=7,relative_cases=len(cases),parity_tail_spaces=sum(r['parity_space_added'] for r in texts),inverse_all1316=True,SC2_sha256=sha(data)))
