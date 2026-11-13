"""Map complete clean/current speech and typed choices without editorial credit."""
import struct
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B122_B127_source_v3260')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3259/verified_handoff.json')
HISTORY=Path('work/analysis/lil_after_London_inventory_v1913/all336_states_and_original_London_town_eligibility.json')
BASE=0x02000000

def choice_getters(arm,command):
    value=bytes.fromhex(command['whole_command_hex']);versions=[]
    for phase in [0,2]:
        cpu=machine(arm);stream,owner=0x02660000+phase,0x02662000
        cpu.mem_write(stream-16,b'\xa5'*(len(value)+32));cpu.mem_write(stream,value)
        cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<3I',0,0,stream));owned=bytes(cpu.mem_read(owner-16,64));before=bytes(cpu.mem_read(BASE,0x400000))
        call(cpu,0x2A3B8,(owner,));assert cpu.reg_read(UC_ARM_REG_R0)==2;labels=[]
        for option in [0,1]:
            relative=6+struct.unpack_from('<H',value,2+2*option)[0];assert 6<=relative<len(value)
            call(cpu,0x2A30C,(owner,option));pointer=cpu.reg_read(UC_ARM_REG_R0);assert pointer==stream+relative
            body=value[relative:value.index(b'\0',relative)];assert body
            labels.append(dict(option_index=option,relative_offset=relative,offset=command['offset']+relative,hex=body.hex(),text=body.decode('cp932')))
        assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==owned and bytes(cpu.mem_read(stream,len(value)))==value
        assert bytes(cpu.mem_read(stream-16,16))==bytes(cpu.mem_read(stream+len(value),16))==b'\xa5'*16
        versions.append(dict(input_alignment=phase,count=2,labels=labels,original_count_pointer_ABI_all4MiB_owner_stream_and_boundary_guards_exact=True))
    return versions

def empty2000(arm,command):
    assert command['whole_command_hex']=='0020' and command['native_extent']==2
    cpu=machine(arm);stream,owner,result,length=0x02660000,0x02662000,0x02664000,0x02664100;value=bytes.fromhex(command['whole_command_hex'])
    cpu.mem_write(stream-16,b'\xa5'*34);cpu.mem_write(stream,value);cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream,0,0));owned=bytes(cpu.mem_read(owner-16,64));before=bytes(cpu.mem_read(BASE,0x400000));cases=[]
    for previous in [0,1,2,3,0xFFFFFFFF]:
        cpu.mem_write(result-16,b'\xa5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xa5'*36);cpu.mem_write(length,bytes(4))
        call(cpu,0x2A510,(result,owner,length,previous));extent=struct.unpack('<I',cpu.mem_read(length,4))[0];decoded=struct.unpack('<6I',cpu.mem_read(result,24))
        assert extent==2 and decoded==(3,0,0,0,0,0) and bytes(cpu.mem_read(BASE,0x400000))==before
        assert bytes(cpu.mem_read(owner-16,64))==owned and bytes(cpu.mem_read(stream,2))==value
        for at in [stream-16,stream+2,result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xa5'*16
        cases.append(dict(previous_result=previous,native_extent=extent,native_result=list(decoded),no_source_resident_text_payload=True,ABI_all4MiB_owner_stream_result_length_and_boundary_guards_exact=True))
    return cases

if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    c=ledger['current_integrated_candidate'];current,clean=NdsImage.open(c['path']),NdsImage.open('work/clean.nds');arm,original=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    assert sha(Path(c['path']).read_bytes())==c['sha256'];history=read(HISTORY)
    ev=clean.read_file('/data/EV2.DK4');assert current.read_file('/data/EV2.DK4')==ev
    spans=[(0x2425C,0x242C8),(0x242CC,0x24310),(0x24314,0x24330),(0x24334,0x243A0),(0x2A1D8,0x2A600)]
    assert all(arm[a:b]==original[a:b] for a,b in spans)
    jp,en=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [clean,current]];inventory,walk,invsource=scoped_inventory();packets=[];rows=[];choices=[];getters=[];controls=[]
    for n in range(122,128):
        source,target=jp[n],en[n];old,spoken=inventory(original,source);now,translated=inventory(arm,target)
        shape=lambda rs:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in rs];assert shape(old)==shape(now)
        records=[];menus=[];opaque=[]
        for sequence,(a,b) in enumerate(zip(spoken,translated,strict=True)):
            sa,ca=a['offset']+5,b['offset']+5;raw=source[sa:source.index(b'\0',sa+1)];value=target[ca:target.index(b'\0',ca+1)];prefix=raw[0]
            assert value[0]==prefix and source[sa-5:sa+1]==target[ca-5:ca+1] and source[sa-5:sa]==bytes.fromhex('0040ffff00')
            ident=f'DK4_MES_B{n}_R{source[:sa].count(bytes([0])):04d}'
            r=dict(id=ident,file_path='/data/SC2.DK4',block=n,source_record_index=source[:sa].count(b'\0'),current_record_index=target[:ca].count(b'\0'),source_reference=dict(offset=sa,bytes=len(raw),header_offset=sa-5),current_reference=dict(offset=ca,bytes=len(value),header_offset=ca-5),source_hex=raw.hex(),current_hex=value.hex(),source_Japanese=raw[1:].decode('cp932'),current_English=value[1:].decode('cp932'),source_complete_preamble_hex=source[sa-5:sa+1].hex(),source_presentation_prefix_hex=format(prefix,'02x'),source_selector=prefix,kind='system-FE' if prefix==254 else 'progressive',speaker='Original FE modal presenter; not actor254' if prefix==254 else 'Source selector'+format(prefix,'02X')+'; current identity pending',original_actor_ID=None if prefix==254 else prefix,native_command_extent=a['native_extent'],ancestor_0100_offsets=a['ancestor_0100_offsets'],spoken_sequence_index=sequence,current_macro_dispatch_consumer_and_complete_native_display_pending=True,source_prose_or_completion_credit_added=0)
            records.append(r);rows.append(r)
        for a,b in zip(old,now,strict=True):
            if a['word']==0x2000:
                cases=[]
                for version,code,cmd in [('clean',original,a),('current',arm,b)]:cases.append(dict(version=version,cases=empty2000(code,cmd)))
                obj=dict(block=n,command_offset=a['offset'],source_command=a,current_command=b,versions=cases,no_source_resident_text_payload=True,preserve_two_byte_control_as_unowned_data=True);opaque.append(obj);controls.append(obj)
            if a['word']!=0x2100:continue
            versions=[]
            for version,code,cmd in [('clean',original,a),('current',arm,b)]:versions.append(dict(version=version,command=cmd,alignment_cases=choice_getters(code,cmd)))
            source_labels,current_labels=[v['alignment_cases'][0]['labels'] for v in versions];objrows=[]
            for s,t in zip(source_labels,current_labels,strict=True):
                option=s['option_index'];assert t['option_index']==option
                r=dict(id=f'DK4_CHOICE_B{n}_C{a["offset"]}_O{option}',file_path='/data/SC2.DK4',block=n,command_offset=a['offset'],option_index=option,source_reference=dict(offset=s['offset'],bytes=len(bytes.fromhex(s['hex']))),current_reference=dict(offset=t['offset'],bytes=len(bytes.fromhex(t['hex']))),source_hex=s['hex'],current_hex=t['hex'],source_Japanese=s['text'],current_English=t['text'],kind='typed-choice-label',speaker='Player-selected reply; exchange speaker context pending',source_prose_or_completion_credit_added=0)
                choices.append(r);objrows.append(r)
            menus.append(dict(command_offset=a['offset'],source_command=a,current_command=b,original_count_and_pointer_cases=versions,records=objrows));getters.extend(versions)
        packets.append(dict(block=n,clean_block_sha256=sha(source),current_block_sha256=sha(target),source_bytes=len(source),current_bytes=len(target),all_clean_native_commands=old,all_current_native_commands=now,source_current_native_command_shape_exact=True,records=records,choices=menus,nontext_2000_controls=opaque,original_event_source=history['all336_original_events'][n],historical_completion_or_dependency_state_not_current_eligibility=True))
    assert len(rows)==155 and len(choices)==4 and sum(len(b['all_clean_native_commands']) for b in packets)==312 and len(controls)==2
    known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};assert not known&{historical_key(r) for r in rows+choices}
    ROOT.mkdir(parents=True)
    save(ROOT/'complete159_clean_current_native_context.json',dict(format='dk4-editorial-source-context-packet-v1',source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),original_EV2_sha256=sha(ev),actual_historical_snapshot=history['snapshot'],actual_historical_snapshot_sha256=history['snapshot_sha256'],historical_snapshot_ROM=history['candidate'],historical_snapshot_is_London_not_selected_B122_B127_scenes=True,source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],blocks=packets,records=rows,typed_choice_records=choices,typed_actor_style_records=[],total_editorial_objects=159,speech_objects=155,ordinary_source_speeches=145,system_FE_panels=10,typed_choice_objects=2,typed_choice_labels=4,nontext_2000_commands=controls,original_choice_getter_cases=getters,all16_original_label_getters_clean_current_even_alignments_pass=True,all20_original2000_decoder_cases_have_type3_extent2_without_stored_text=True,all312_physical_commands_and155_speech_preambles_current_clean_shape_exact=True,whole_clean_context_current_identity_entry_macros_oldEnglish_comparison_and_all_native_release_gates_pending=True,older_English_not_used_as_translation_source=True,source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,explicit_unmatched_native_walk=walk,unchanged_inventory_function=invsource,prior_state_inventory=str(HISTORY),prior_state_inventory_sha256=sha(HISTORY.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Next159physical objects mapped:155speech/4labels in2menus;312commands;16source/current label getters/20native2000decoder cases pass. Two2000controls contain no stored text. No editorialcredit.')
