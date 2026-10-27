"""Parse originalEV2 source context and bind the B141 action through current getters."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_entry_v3536')
SOURCE=Path('work/analysis/lil_B141_source_v3532b/all14_clean_current_complete_context.json')
def native_entry(arm,common,raw,plan,ev,rows):
    cpu,get,provider=machine(arm,common,raw,plan);assert get(0x7F244)==2;header=raw.find(ev[:96]);assert header>=0 and raw.find(ev[:96],header+1)<0;owner=0x02000000+header-0x34;out=0x02640000;before=bytes(cpu.mem_read(0x02000000,0x400000));cases=[]
    for row in rows:
        cpu.mem_write(out-16,b'\xA5'*36);get(0x23888,out,owner+4,row['event_ID']);pointer=struct.unpack('<I',cpu.mem_read(out,4))[0];assert pointer==0x02000000+header+96+row['body_offset'];value=bytes(cpu.mem_read(pointer,row['source_record_bytes']));expected=bytes.fromhex(row['source_hex']);assert value[4:]==expected[4:] and (struct.unpack_from('<I',value)[0]^row['source_word0'])&~0xC0008000==0
        complete=get(0x23840,owner+4,row['event_ID']);assert complete in [0,1] and bytes(cpu.mem_read(out-16,16))==bytes(cpu.mem_read(out+4,16))==b'\xA5'*16
        cases.append(dict(event_ID=row['event_ID'],source_event_pointer=pointer,source_word0_state_bits_only_mask=0xC0008000,original_completion_flag_in_historical_opening=complete,not_current_eligibility_or_selected_B141_activation=True))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before;return dict(rows=cases,all4MiB_actor_roster_event_RNG_and_original_ABI_exact=True,current_executed_instruction_addresses=len(provider.executed_current))
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image,clean=NdsImage.open(packet['current_ROM']),NdsImage.open('work/clean.nds');ev=image.read_file('/data/EV2.DK4');assert ev==clean.read_file('/data/EV2.DK4') and sha(ev)==packet['original_EV2_sha256'];body=ev[96:];counts=struct.unpack_from('<9H',ev,10);starts=struct.unpack_from('<9I',ev,40);total=sum(counts);events=[];action_begin,action_end=struct.unpack_from('<2I',ev,0x4C);words=struct.unpack_from(f'<{(action_end-action_begin)//2}H',body,action_begin)
    for category,count in enumerate(counts):
        offset=starts[category]
        for local in range(count):
            word0,word1=struct.unpack_from('<2I',body,offset);length=(word1&255)*4;assert length>=8;record=body[offset:offset+length];assert len(record)==length;must=[];must_not=[];following=8
            if word1&(1<<24):
                packed=struct.unpack_from('<H',record,8)[0];yes,no=packed>>8,packed&255;needed=struct.unpack_from(f'<{yes+no}H',record,10) if yes+no else ();must=list(needed[:yes]);must_not=list(needed[yes:]);following+=((yes+no)*2+5)&~3;assert following<=length and all(v<total or v==65535 for v in [*must,*must_not])
            action=(word0>>16)&0x3FFF;assert action<len(words);native_word=words[action]
            events.append(dict(event_ID=len(events),category=category,category_local_index=local,body_offset=offset,source_record_bytes=length,source_hex=record.hex(),source_word0=word0,source_word1=word1,action_index=action,native_action_word=native_word,script_block=(native_word&4095) if native_word&0xF000==0x2000 else None,must_be_completed=must,must_not_be_completed=must_not,payload_after_dependency_prefix_hex=record[following:].hex(),additional_native_conditions_and_outer_scheduler_unexecuted=True));offset+=length
        assert offset==struct.unpack_from('<I',ev,44+category*4)[0]
    assert len(events)==total;chosen=[r for r in events if r['script_block']==141];assert len(chosen)==1;ids={chosen[0]['event_ID'],*[n for r in chosen for n in r['must_be_completed']+r['must_not_be_completed'] if n!=65535]};selected=[r for r in events if r['event_ID'] in ids]
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B141_voices_v3533/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');result=ctx.execute(native_entry,ev,selected);ctx.machines.pop();assert not ctx.machines
    save(ROOT/'source_EV2_B141_action_dependency_and_native_getter_binding.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),EV2_sha256=sha(ev),all_original_source_events=events,selected_B141_source_event=chosen[0],selected_source_event_and_dependency_native_getters=result,source_owned_getter_adapter=inspect.getsource(native_entry),historical_snapshot_is_Lil_opening_not_current_B141_eligibility=True,original_source_EV2_and_action_table_exact=True,source_controls_branches_and_all_editorial_gates_pending=True,actual_selected_B141_IDs=[],new_emulator_runs=0,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_event=chosen[0]['event_ID'],category=chosen[0]['category'],action=chosen[0]['action_index'],native_action_hex=hex(chosen[0]['native_action_word']),requires=chosen[0]['must_be_completed'],requires_not=chosen[0]['must_not_be_completed'],native_getter_cases=len(result['rows']),selected_gameplay=False))
