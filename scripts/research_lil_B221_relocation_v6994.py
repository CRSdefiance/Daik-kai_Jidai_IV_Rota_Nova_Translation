"""Relocate fourteen speech strings and one complete menu with an exact1208-byte inverse."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B221_profile_v1 import profile_for
from dk4tool.dialogue.lil_B221_layout_v1 import encode_relocatable_dialogue
from dk4tool.dialogue.lil_B221_choices_v1 import compile_choices
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B221_relocation_v6994')
DOC=Path('translations/lil_B221_editorial_manuscript_v1.json')
MENU=Path('translations/lil_B221_choice_manuscript_v1.json')
BRANCH=Path('work/analysis/lil_B221_branches_v6970/original_relative_skip_operand_proof.json')
POLICY=Path('work/analysis/lil_B221_policy_validation_v6993b/fourteen_paragraphs_one_typed_menu36_distinct_rejections_seven_row_reasons.json')
OWNER,STREAM,RESULT,LENGTH=0x02650000,0x02660000,0x02668000,0x02668100

if __name__=='__main__':
    assert not ROOT.exists()
    doc,menu,branches,policy=map(read,[DOC,MENU,BRANCH,POLICY])
    assert policy['all36_distinct_safety_and_fidelity_rejections_before_ROM_mutation']
    SOURCE=Path(doc['source_context']);packet=read(SOURCE);spec=packet['blocks'][0]
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    container=IlnkContainer.parse(image.read_file('/data/SC2.DK4'));source=container.blocks[221]
    old_end=8+struct.unpack_from('<H',source,4)[0]
    assert len(source)==old_end==1208 and sha(source)==spec['current_block_sha256']
    patches=[];texts=[]
    for row in doc['records']:
        at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex'])
        assert source[at:at+len(old)+1]==old+b'\0'
        encoded=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,source,row['id']))
        value=encoded.encoded;pad=len(value)%2!=len(old)%2
        if pad:value+=b' '
        assert b'\0' not in value and value[0]==old[0]==row['source_selector']
        assert len(value)%2==len(old)%2
        patches.append(dict(start=at,end=at+len(old),value=value,old=old,kind='speech',id=row['id']))
        texts.append(dict(id=row['id'],kind='progressive',record_index=row['current_record_index'],
            source_selector=row['source_selector'],source_voice_class=row['source_voice_class'],
            old_offset=at,old_length=len(old),new_length=len(value),compiled_hex=encoded.encoded.hex(),
            target_hex=value.hex(),parity_space_added=pad,source_reference=row['source_reference'],
            current_reference=row['current_reference'],source_preamble_hex=row['source_complete_preamble_hex']))
    command=next(c for c in spec['all_current_native_commands'] if c['word']==0x2100)
    assert command['offset']==150 and command['native_extent']==28
    old_choice=bytes.fromhex(command['whole_command_hex']);target_choice=compile_choices(menu['records'])
    assert source[150:178]==old_choice and len(target_choice)==14
    patches.append(dict(start=150,end=178,value=target_choice,old=old_choice,kind='choice',id='B221_choice_150'))
    patches.sort(key=lambda p:p['start'])
    assert len(patches)==15 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
    def mapped(at):
        delta=0
        for patch in patches:
            if at<patch['start']:break
            if patch['start']<at<patch['end']:raise ValueError('Interior reference into a complete replaced B221 object:'+str(at))
            if at==patch['start']:return at+delta
            delta+=len(patch['value'])-len(patch['old'])
        return at+delta
    parts=[];last=0
    for patch in patches:
        parts.extend([source[last:patch['start']],patch['value']]);last=patch['end']
    parts.append(source[last:old_end]);logical=bytearray(b''.join(parts))
    assert len(logical)==mapped(old_end)<0x2400
    fixups=[]
    for edge in branches['operands_requiring_adjustment_when_resizing']:
        assert edge['block']==221
        start=mapped(edge['offset']);target=mapped(edge['matched_skip_target']);span=target-start-4
        assert 0<=span<=0xFFFF and span%2==0 and struct.unpack_from('<H',logical,start)[0]==edge['word']
        source_span=struct.unpack_from('<H',source,edge['span_field_offset'])[0]
        struct.pack_into('<H',logical,start+2,span)
        fixups.append(dict(**edge,new_offset=start,new_unmatched_next=start+4,new_matched_skip_target=target,
            source_span=source_span,target_span=span))
    assert len(fixups)==4
    struct.pack_into('<H',logical,4,len(logical)-8)
    target=bytes(logical)+bytes(-len(logical)%4)
    inventory,walker,inventory_source=scoped_inventory()
    commands,speeches=inventory(arm,target)
    assert len(commands)==21 and len(speeches)==14
    byoffset={c['offset']:c for c in commands};boundaries=set(byoffset)|{len(logical)};maps=[]
    for old in spec['all_current_native_commands']:
        new=byoffset[mapped(old['offset'])]
        assert new['word']==old['word']
        assert new['ancestor_0100_offsets']==[mapped(a) for a in old['ancestor_0100_offsets']]
        assert new['native_extent']==mapped(old['offset']+old['native_extent'])-new['offset']
        if old['word']==0x4000:
            assert source[old['offset']:old['offset']+6]==target[new['offset']:new['offset']+6]
        elif old['word']==0x2100:
            assert bytes.fromhex(new['whole_command_hex'])==target_choice
        elif old['word'] not in [0x100,0x200,0x300]:
            assert old['whole_command_hex']==new['whole_command_hex']
        maps.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],
            old_extent=old['native_extent'],new_extent=new['native_extent'],
            source_0100_ancestors=old['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
    cpu=machine(arm);cpu.mem_write(STREAM-16,b'\xa5'*(len(target)+32));cpu.mem_write(STREAM,target)
    main_before=bytes(cpu.mem_read(0x02000000,0x400000));cases=[]
    for edge in fixups:
        assert edge['new_unmatched_next'] in boundaries and edge['new_matched_skip_target'] in boundaries
        for choice in [0,1,2,3,0xFFFFFFFF]:
            cpu.mem_write(OWNER-16,b'\xa5'*64);cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+edge['new_offset'],0,0))
            owner_before=bytes(cpu.mem_read(OWNER-16,64))
            cpu.mem_write(RESULT-16,b'\xa5'*64);cpu.mem_write(RESULT,bytes(24))
            cpu.mem_write(LENGTH-16,b'\xa5'*36);cpu.mem_write(LENGTH,bytes(4))
            call(cpu,0x2A510,(RESULT,OWNER,LENGTH,choice))
            extent=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0]
            taken=edge['word']==0x100 or (edge['word']==0x200 and choice==0) or (edge['word']==0x300 and choice==1)
            assert edge['new_offset']+extent==(edge['new_matched_skip_target'] if taken else edge['new_unmatched_next'])
            assert struct.unpack('<6I',cpu.mem_read(RESULT,24))==(3,0,0,0,0,0)
            assert bytes(cpu.mem_read(OWNER-16,64))==owner_before
            assert bytes(cpu.mem_read(STREAM,len(target)))==target and bytes(cpu.mem_read(0x02000000,0x400000))==main_before
            for at in [STREAM-16,STREAM+len(target),RESULT-16,RESULT+24,LENGTH-16,LENGTH+4]:
                assert bytes(cpu.mem_read(at,16))==b'\xa5'*16
            cases.append(dict(new_offset=edge['new_offset'],last_result=choice,native_extent=extent,
                source_target_preserved_at_mapped_native_boundary=True,
                ABI_all4MiB_owner_stream_result_length_and_guards_exact=True))
    for row in texts:
        at=mapped(row['old_offset']);row.update(new_offset=at,new_record_index=target[:at].count(b'\0'))
        assert target[at-5:at+1].hex()==row['source_preamble_hex']
        assert target[at:at+row['new_length']].hex()==row['target_hex'] and target[at+row['new_length']]==0
    choice_at=mapped(150);choice_refs=[]
    for row in menu['records']:
        index=row['option_index'];at=choice_at+6+struct.unpack_from('<H',target,choice_at+2+index*2)[0]
        value=row['english'].encode('ascii')
        assert target[at:at+len(value)+1]==value+b'\0'
        choice_refs.append(dict(id=row['id'],kind='typed-choice-label',option_index=index,
            old_offset=row['current_reference']['offset'],old_length=row['current_reference']['bytes'],
            new_offset=at,new_length=len(value),new_record_index=target[:at].count(b'\0'),
            target_hex=value.hex(),source_reference=row['source_reference'],current_reference=row['current_reference']))
    choices=[dict(old_offset=150,old_length=28,new_offset=choice_at,new_length=14,
        labels=['Yes','No'],target_hex=target_choice.hex(),text_base=6,count=2,
        record_IDs=[r['id'] for r in menu['records']],label_references=choice_refs)]
    effects=[dict(source_offset=1196,target_offset=mapped(1196),extent=8,source_hex='00a0ffff47000110')]
    ends=[dict(source_offset=1204,target_offset=mapped(1204),extent=4,source_hex='00000000',source_four_zero_bytes_exact=True)]
    assert target[mapped(1196):mapped(1196)+8]==bytes.fromhex(effects[0]['source_hex'])
    assert target[mapped(1204):mapped(1204)+4]==bytes(4) and mapped(1204)+4==len(logical)
    restored=bytearray(target[:len(logical)]);struct.pack_into('<H',restored,4,old_end-8)
    for edge in fixups:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
    for patch in reversed(patches):
        at=mapped(patch['start']);restored[at:at+len(patch['value'])]=patch['old']
    assert bytes(restored)==source
    ROOT.mkdir(parents=True)
    bp=ROOT/'SC2_block221_RESEARCH_ONLY.bin';bp.write_bytes(target)
    (ROOT/'explicit_unmatched_native_walk.py.txt').write_text(walker,encoding='utf-8')
    blocks=list(container.blocks);blocks[221]=target;archive=IlnkContainer(blocks).to_bytes()
    ap=ROOT/'SC2_RESEARCH_ONLY.DK4';ap.write_bytes(archive)
    assert [i for i,(a,b) in enumerate(zip(container.blocks,IlnkContainer.parse(archive).blocks,strict=True)) if a!=b]==[221]
    group=dict(block=221,source_block_sha256=sha(source),research_block_sha256=sha(target),
        source_bytes=1208,source_logical_end=1208,source_tail_bytes=0,
        research_bytes=len(target),research_logical_end=len(logical),research_tail_bytes=len(target)-len(logical),
        research_block=str(bp),text_records=texts,all_object_references=texts+choice_refs,
        choice_commands=choices,actor_style_commands=[],relative_skip_fixups=fixups,target_native_skip_cases=cases,
        command_map=maps,original_A000_map=effects,original_C200_map=[],complete_end_map=ends,
        original_declared_end_word_maps=ends,original2000_pause_and_resume_maps=[],
        inverse_recovers_every_original1208_byte=True,all21_original_commands_and_complete_preambles_preserved=True,
        all_nested_original_command_types_ancestors_and_opaque_bytes_preserved=True,external_references_complete=False)
    save(ROOT/'all16_objects21_commands_four_relatives_full1208_inverse_RESEARCH.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choice_manuscript=str(MENU),choice_manuscript_sha256=sha(MENU.read_bytes()),
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        target_SC2=str(ap),target_SC2_sha256=sha(archive),blocks=[group],all335_other_SC2_blocks_exact=True,
        all16_exact_source_current_compiled_and_research_references_bound=True,
        source_tail_header_all_four_relative_operands_and_entire_menu_full_inverse=True,
        final_stored_fonts_menu_loaders_external_references_actual_and_release_pending=True,
        external_references_complete=False,not_release_map_or_candidate=True,new_emulator_runs=0,new_review_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,MENU,SOURCE,BRANCH,POLICY,
            Path('translations/lil_B221_native_contract_v1.json'),Path('dk4tool/dialogue/lil_B221_profile_v1.py'),
            Path('dk4tool/dialogue/lil_B221_layout_v1.py'),Path('dk4tool/dialogue/lil_B221_choices_v1.py'),Path(__file__)]},full_goal_complete=False))
    print(dict(source=1208,target=len(target),logical=len(logical),tail=len(target)-len(logical),
        parity_tails=sum(r['parity_space_added'] for r in texts),choice_offset=choice_at,
        relative_fixups=[(r['offset'],r['new_offset'],r['target_span']) for r in fixups],
        A000=effects,end=ends,complete_inverse=True,credit=0))
