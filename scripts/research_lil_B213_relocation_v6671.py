"""Reconstruct all18 speeches and four relative operands with full1028-byte inverse."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.lil_B213_profile_v1 import profile_for
from dk4tool.dialogue.lil_B213_layout_v1 import encode_relocatable_dialogue
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B213_relocation_v6671');DOC=Path('translations/lil_B213_editorial_manuscript_v2.json');BRANCH=Path('work/analysis/lil_B213_branches_v6654/original_relative_skip_operand_proof.json');OWNER,STREAM,RESULT,LENGTH=0x02650000,0x02660000,0x02668000,0x02668100
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);SOURCE=Path(doc['source_context']);packet=read(SOURCE);spec=packet['blocks'][0];rom=Path(doc['current_ROM']);assert sha(rom.read_bytes())==doc['current_ROM_sha256'];image=NdsImage.open(rom);arm=image.read_file('/__arm9__.bin');container=IlnkContainer.parse(image.read_file('/data/SC2.DK4'));source=container.blocks[213];old_end=8+struct.unpack_from('<H',source,4)[0];assert len(source)==1028 and old_end==1026 and source[old_end:]==b'\0\0' and sha(source)==spec['current_block_sha256'];patches=[];texts=[];choices=[]
    for row in doc['records']:
        if row['kind']!='progressive':continue
        at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex']);assert source[at:at+len(old)+1]==old+b'\0';encoded=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,source,row['id']));value=encoded.encoded;pad=len(value)%2!=len(old)%2
        if pad:value+=b' '
        assert b'\0' not in value and value[0]==old[0]==row['source_selector'] and len(value)%2==len(old)%2;patches.append(dict(start=at,end=at+len(old),value=value,old=old,kind='speech',id=row['id']));texts.append(dict(id=row['id'],old_offset=at,old_length=len(old),new_length=len(value),compiled_hex=encoded.encoded.hex(),target_hex=value.hex(),parity_space_added=pad,source_reference=row['source_reference'],current_reference=row['current_reference'],source_preamble_hex=row['source_complete_preamble_hex']))
    patches.sort(key=lambda p:p['start']);assert len(patches)==18 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            if p['start']<offset<p['end']:raise ValueError('Unmapped interior reference into replaced B213 object:'+str(offset))
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-(p['end']-p['start'])
        return offset+delta
    parts=[];last=0
    for p in patches:parts.extend([source[last:p['start']],p['value']]);last=p['end']
    parts.append(source[last:old_end]);logical=bytearray(b''.join(parts));assert len(logical)==mapped(old_end) and len(logical)<0x2400;branch=read(BRANCH);assert branch['source_context_sha256']==sha(SOURCE.read_bytes());fixups=[]
    for edge in branch['operands_requiring_adjustment_when_resizing']:
        assert edge['block']==213;start=mapped(edge['offset']);target=mapped(edge['matched_skip_target']);span=target-start-4;assert 0<=span<=0xFFFF and span%2==0 and struct.unpack_from('<H',logical,start)[0]==edge['word'];old_span=struct.unpack_from('<H',source,edge['span_field_offset'])[0];struct.pack_into('<H',logical,start+2,span);fixups.append({**edge,'new_offset':start,'new_unmatched_next':start+4,'new_matched_skip_target':target,'source_span':old_span,'target_span':span})
    assert len(fixups)==4;struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4);inventory,walker,invsource=scoped_inventory();commands,speeches=inventory(arm,target);assert len(commands)==27 and len(speeches)==18;byoffset={c['offset']:c for c in commands};boundaries=set(byoffset)|{len(logical)};maps=[]
    for old in spec['all_current_native_commands']:
        new=byoffset[mapped(old['offset'])];assert new['word']==old['word'] and new['ancestor_0100_offsets']==[mapped(a) for a in old['ancestor_0100_offsets']]
        if old['word'] not in [0x100,0x200,0x300,0x400,0x4000,0x2100,0x2200]:assert old['whole_command_hex']==new['whole_command_hex']
        maps.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],old_extent=old['native_extent'],new_extent=new['native_extent'],source_0100_ancestors=old['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
    cpu=machine(arm);cpu.mem_write(STREAM-16,b'\xa5'*(len(target)+32));cpu.mem_write(STREAM,target);main_before=bytes(cpu.mem_read(0x02000000,0x400000));cases=[]
    for edge in fixups:
        assert edge['new_unmatched_next'] in boundaries and edge['new_matched_skip_target'] in boundaries
        for previous in [0,1,2,3,0xFFFFFFFF]:
            cpu.mem_write(OWNER-16,b'\xa5'*64);cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+edge['new_offset'],0,0));before=bytes(cpu.mem_read(OWNER-16,64));cpu.mem_write(RESULT-16,b'\xa5'*80);cpu.mem_write(RESULT,bytes(24));cpu.mem_write(LENGTH-16,b'\xa5'*36);cpu.mem_write(LENGTH,bytes(4));call(cpu,0x2A510,(RESULT,OWNER,LENGTH,previous));extent=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0];take=edge['word']==0x100 or (edge['word']==0x200 and previous==0) or (edge['word']==0x300 and previous==1) or (edge['word']==0x400 and previous==2);assert edge['new_offset']+extent==(edge['new_matched_skip_target'] if take else edge['new_unmatched_next']) and struct.unpack('<6I',cpu.mem_read(RESULT,24))==(3,0,0,0,0,0);assert bytes(cpu.mem_read(OWNER-16,64))==before and bytes(cpu.mem_read(STREAM,len(target)))==target and bytes(cpu.mem_read(0x02000000,0x400000))==main_before
            for at in [STREAM-16,STREAM+len(target),RESULT-16,RESULT+24,LENGTH-16,LENGTH+4]:assert bytes(cpu.mem_read(at,16))==b'\xa5'*16
            cases.append(dict(new_offset=edge['new_offset'],last_result=previous,native_extent=extent,all_source_targets_mapped_native_boundaries_and_ABI_memory_canaries_exact=True))
    for r in texts:
        at=mapped(r['old_offset']);r.update(new_offset=at,new_record_index=target[:at].count(b'\0'));assert target[at-5:at+1].hex()==r['source_preamble_hex'] and target[at:at+r['new_length']].hex()==r['target_hex'] and target[at+r['new_length']]==0
    ends=[];effects=[]
    for old in spec['all_current_native_commands']:
        if old['word'] not in [0,0xA000]:continue
        at=mapped(old['offset']);value=bytes.fromhex(old['whole_command_hex']);assert target[at:at+len(value)]==value;item=dict(source_offset=old['offset'],target_offset=at,extent=len(value),source_hex=value.hex());(ends if old['word']==0 else effects).append(item)
    assert [(e['source_offset'],e['source_hex']) for e in ends]==[(1022,'00000000')] and len(effects)==1 and ends[-1]['target_offset']+4==len(logical)
    restored=bytearray(target[:len(logical)]);struct.pack_into('<H',restored,4,old_end-8)
    for edge in fixups:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    assert bytes(restored)+source[old_end:]==source;ROOT.mkdir(parents=True);bp=ROOT/'SC2_block213_RESEARCH_ONLY.bin';bp.write_bytes(target);blocks=list(container.blocks);blocks[213]=target;assert all(a==b for n,(a,b) in enumerate(zip(container.blocks,blocks,strict=True)) if n!=212);archive=IlnkContainer(blocks).to_bytes();ap=ROOT/'SC2_RESEARCH_ONLY.DK4';ap.write_bytes(archive)
    group=dict(block=213,source_block_sha256=sha(source),research_block_sha256=sha(target),source_bytes=1028,source_logical_end=1026,source_tail_bytes=2,research_bytes=len(target),research_logical_end=len(logical),research_tail_bytes=len(target)-len(logical),research_block=str(bp),text_records=texts,choice_commands=choices,actor_style_commands=[],relative_skip_fixups=fixups,target_native_skip_cases=cases,command_map=maps,original_A000_map=effects,complete_end_map=ends,inverse_recovers_every_original1028_byte=True,all27_original_words_ancestors_preambles_predicate_staging_A000_and_normal_end_preserved=True,external_references_complete=False)
    save(ROOT/'all18_objects4_spans_normal_end_full1028_inverse_RESEARCH.json',dict(candidate=str(rom),candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),target_SC2=str(ap),target_SC2_sha256=sha(archive),blocks=[group],all335_other_SC2_blocks_exact=True,source_normal_state0_terminal_four_bytes_preserved=True,all20_relocated_native_skip_cases_pass=True,all18_exact_source_current_compiled_and_research_references_bound=True,source_tail_and_header_full_inverse=True,final_stored_fonts_loaders_external_references_actual_and_release_pending=True,external_references_complete=False,not_release_map_or_candidate=True,no_ROM_registry_ledger_or_completion_change=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,SOURCE,BRANCH,Path('translations/lil_B213_native_contract_v1.json'),Path('dk4tool/dialogue/lil_B213_profile_v1.py'),Path('dk4tool/dialogue/lil_B213_layout_v1.py'),Path(__file__)]},full_goal_complete=False));print(dict(source_stored=1028,target_stored=len(target),target_logical=len(logical),target_tail=len(target)-len(logical),parity_tails=sum(r['parity_space_added'] for r in texts),native_skips=len(cases),ends=ends,credit=0))
