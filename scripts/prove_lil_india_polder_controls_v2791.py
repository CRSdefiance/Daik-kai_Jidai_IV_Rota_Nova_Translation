"""Bind146 ordinary/FE preambles and original Mediterranean/Africa predicates."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_India_Polder_controls_v2791')
PACKET=Path('work/analysis/lil_India_Polder_source_v2789/complete112_clean_current_native_context.json')
BASE=0x02000000

def predicate(arm,common,raw,plan,block,command):
    cpu,get,provider=machine(arm,common,raw,plan)
    stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100
    cpu.mem_write(stream-16,b'\xA5'*(len(block)+32));cpu.mem_write(stream,block)
    cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+command['offset'],0,0));guard=bytes(cpu.mem_read(owner-16,64))
    cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4))
    before=bytes(cpu.mem_read(BASE,0x400000));calls=[]
    def trace(u,pc,size,unused):
        calls.append(dict(address=pc,args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]))
    h=cpu.hook_add(UC_HOOK_CODE,trace,begin=BASE+0x23840,end=BASE+0x23840)
    scratch=0x02279600;writes=[]
    wh=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,access,address,size,value,d:writes.append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=address,size=size,value=value)),begin=scratch,end=scratch+3)
    try:call(cpu,0x2A510,(result,owner,length,0),instruction_limit=500000)
    finally:cpu.hook_del(h);cpu.hook_del(wh)
    values=struct.unpack('<6I',cpu.mem_read(result,24));extent=struct.unpack('<I',cpu.mem_read(length,4))[0]
    assert values[0]==2 and values[1] in [0,1] and extent==command['native_extent']
    after=bytes(cpu.mem_read(BASE,0x400000));operand=stream+command['offset']+4
    expected_write=command['word']==0x8000 and operand%4!=0
    assert struct.unpack_from('<I',arm,0x2A5E8)[0]==scratch and arm[0x2A5D8:0x2A5DC]==bytes.fromhex('000081e5')
    expected=[dict(PC=BASE+0x2A5D8,address=scratch,size=4,value=int.from_bytes(block[command['offset']+4:command['offset']+8],'little'))] if expected_write else []
    assert writes==expected,(command,writes,expected)
    unowned=bytearray(after);unowned[scratch-BASE:scratch-BASE+4]=before[scratch-BASE:scratch-BASE+4];assert unowned==before
    cpu.mem_write(scratch,before[scratch-BASE:scratch-BASE+4])
    assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(stream,len(block)))==block and bytes(cpu.mem_read(owner-16,64))==guard
    for at in [stream-16,stream+len(block),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    return dict(offset=command['offset'],word=command['word'],source_command_hex=command['whole_command_hex'],native_result=list(values),native_extent=extent,
        original_event_completion_calls=calls,original_unaligned_operand_read_scratch_writes=writes,source_owned_scratch_address=scratch,sole_scratch_restore_recovers_all4MiB_exact=True,current_executed_instruction_addresses=len(provider.executed_current),
        all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact=True,no_predicate_or_event_flag_forced=True)

if __name__=='__main__':
    assert not ROOT.exists();packet=read(PACKET);current=NdsImage.open(packet['current_ROM']);old=NdsImage.open(packet['historical_snapshot_ROM']);clean=NdsImage.open('work/clean.nds')
    arm=old.read_file('/__arm9__.bin');now=current.read_file('/__arm9__.bin');original=clean.read_file('/__arm9__.bin')
    raw=Path(packet['actual_historical_snapshot']).read_bytes();assert sha(raw)==packet['actual_historical_snapshot_sha256']
    spans=[(0x2425C,0x242C8),(0x242CC,0x24310),(0x24314,0x24330),(0x24334,0x243A0),(0x54020,0x54060),(0x23840,0x23A28),(0x2A1D8,0x2A530),(0x2A5BC,0x2A600),(0x5473C,0x54798),(0x5479C,0x54804)]
    for a,b in spans:assert now[a:b]==arm[a:b]==original[a:b]==raw[a:b]
    assert arm[0x54798:0x5479C]==now[0x54798:0x5479C]==raw[0x54798:0x5479C] and arm[0x54798:0x5479C]!=original[0x54798:0x5479C]
    selectors={n:n for n in [2,9,16,21,151,171]};cases=[]
    for row in packet['records']:
        prefix=int(row['source_presentation_prefix_hex'],16)
        for version,field in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            cpu,get=get_machine(arm,raw);root=get(0xCB184);assert get(0x7F244)==2 and get(0x2434C,prefix)==(208 if prefix==254 else prefix)
            actor=None if prefix==254 else root+0x19E4 if prefix==2 else root+4+32*prefix
            text=bytes.fromhex(row[field]);assert text[0]==prefix
            at=0x02660000;cpu.mem_write(at-16,b'\xA5'*2080);cpu.mem_write(at,text[1:]+b'\0');guard=bytes(cpu.mem_read(at-16,2080));seen=[]
            def boundary(u,pc,size,unused):
                if pc==BASE+0x940B0:seen.append(dict(boundary=pc,kind='unexecuted-UI-preparation'))
                else:
                    first,second=u.reg_read(UC_ARM_REG_R0),u.reg_read(UC_ARM_REG_R1);obj=first if pc==BASE+0x54020 else None;ptr=second if pc==BASE+0x54020 else first
                    seen.append(dict(boundary=pc,kind='unexecuted-native-progressive-body',actor_object=obj,text_hex=bytes(u.mem_read(ptr,2048)).split(b'\0')[0].hex()))
                u.reg_write(UC_ARM_REG_R0,0);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
            hooks=[cpu.hook_add(UC_HOOK_CODE,boundary,begin=pc,end=pc) for pc in [BASE+0x940B0,BASE+0x54020,BASE+0x5473C,BASE+0x53AC4]]
            try:call(cpu,0x2425C,(prefix,at),instruction_limit=500000)
            finally:
                for hook in hooks:cpu.hook_del(hook)
            assert len(seen)==2 and seen[0]['boundary']==BASE+0x940B0 and seen[1]['boundary']==BASE+(0x5473C if prefix==254 else 0x54020) and seen[1]['actor_object']==actor
            assert seen[1]['text_hex']==next(p['output_hex'] for p in row['original_macro_probes'] if p['version']==version)
            assert bytes(cpu.mem_read(BASE,0x400000))==raw and bytes(cpu.mem_read(at-16,2080))==guard
            cases.append(dict(id=row['id'],version=version,prefix=prefix,original_actor_ID=prefix,complete_preamble_hex=row['source_complete_preamble_hex'],boundaries=seen,
                whole4MiB_input_guards_actor_models_and_saved_register_ABI_exact=True,not_a_current_font_or_actual_scene_activation=True))
    assert len(cases)==224 and not any(c['prefix']==254 for c in cases)
    ROOT.mkdir(parents=True);contextpath=ROOT/'historical_source_context.json';save(contextpath,dict(actual_snapshot=packet['actual_historical_snapshot'],actual_snapshot_sha256=sha(raw)))
    inputpath=ROOT/'current_native_input.json';save(inputpath,dict(current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],current_ARM9_sha256=sha(now),current_COMMON_sha256=sha(current.read_file('/COMMON/MESFILE.DK4')),native_context_proof=str(contextpath)))
    ctx=CurrentContext(inputpath,packet['historical_snapshot_ROM'],ROOT/'current_context');predicates=[]
    blocks=IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks
    for spec in packet['blocks']:
        for command in spec['all_current_native_commands']:
            if command['word'] not in [0x8000,0x8100]:continue
            predicates.append(dict(block=spec['block'],**ctx.execute(predicate,blocks[spec['block']],command)));ctx.machines.pop()
    assert not ctx.machines and len(predicates)==9
    event_queries=[dict(block=p['block'],offset=p['offset'],event=q['args'][1],args=q['args']) for p in predicates for q in p['original_event_completion_calls']]
    assert [(q['block'],q['event']) for q in event_queries]==[(37,129),(38,48),(38,48)]
    save(ROOT/'source_bound112_preambles_and_original_conditional_predicates.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],ARM9_sha256=sha(now),
        source_context=str(PACKET),source_context_sha256=sha(PACKET.read_bytes()),ordinary_native_actor_selectors={str(k):v for k,v in selectors.items()},
        complete_original_preambles=[dict(id=r['id'],preamble_hex=r['source_complete_preamble_hex']) for r in packet['records']],
        all112_complete_preambles_and224_historical_dispatch_contexts_pass=True,dispatch_cases=cases,current_original_predicate_cases=predicates,
        all_predicates_current_instruction_and_unowned4MiB_exact=True,source_owned_unaligned_read_scratch_restored_all4MiB_exact=True,
        no_RAM_roster_event_RNG_or_outcome_mutation=True,no_FE_or_typed_choice_objects_in_selected_source=True,existing_FE54798_wrap_call_owner='dk4tool.patch.regional_assignment_wrap',UI_and_panel_bodies_explicit_unexecuted_boundaries=[BASE+0x940B0,BASE+0x54020,BASE+0x5473C],
        source_exact_spans=[dict(start=a,end=b,sha256=sha(now[a:b])) for a,b in spans],original_event_queries=event_queries,original_predicate_context_plan=str(ctx.proof_path),
        actual_selected_India_Polder_IDs=[],new_individual_nameplate_observations=[],new_emulator_runs=0,
        scope='All112complete sourcepreambles and224historical dispatchcases bind original54020selectors2/9/16/21/151/171. Source171is executableResearchStudentstate,notageneralShiftJISprefix rule;151isgenericRetainerclass,notearnedFirstMate. Cataloggetters donotclaimnewnameplates oruniquereusedNPCidentity. UI940B0andnativepanelbodies remainexplicitunexecutedboundaries. Nineoriginal8000/8100predicates executeunderboundedcurrent-code overlays withactor/event/RNG/unowned4MiB exact;sourceowned02279600alignmentreadscratch is restoredexactly. Nativegetter23840queries event129inB37and48twiceinB38. This bindstheAmsterdamrecollection andfather-relatedalternatives withoutclaimingthat event48is thefulltrue-name reveal orforcingeligibility. Event40requires39;129mustnotfollowcompleted37. No selectedsceneactivation,newemulatorrun,newnameplate,currentfont/GPUapproval orcompletioncredit isclaimed. Fullcurrentfonts/QA,relocation/references,representative andregisteredrelease gates remainrequired.',
        no_ROM_registry_or_editorial_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(f'112complete preambles/224historical dispatch and{len(predicates)}current predicates pass. Nativeeventqueries bind129and48/48;allunownedstate exact. No newsceneactivation.')
