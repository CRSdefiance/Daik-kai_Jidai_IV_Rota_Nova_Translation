"""Current registered actor catalog and contextual identity reconciliation."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Shrines_Temples_voices_v3167')
SOURCE=Path('work/analysis/lil_Shrines_Temples_source_v3163/complete235_clean_current_native_context.json')
def names(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(0x02000000,0x400000));root=get(0xCB184);assert get(0x7F244)==2
    results=[];scratch=[]
    assert arm[0xAC000:0xAC02C]==NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')[0xAC000:0xAC02C]
    for ident in range(207):
        actor=root+0x19E4 if ident==2 else root+4+32*ident;vt=struct.unpack('<I',cpu.mem_read(actor,4))[0];fn=struct.unpack('<I',cpu.mem_read(vt+8,4))[0]
        voice=get(0x7E988,actor);assert 0<=voice<8
        prior=bytes(cpu.mem_read(0x02000000,0x400000));rings=[];writes=[]
        def ring(u,pc,size,unused):
            owner=u.reg_read(UC_ARM_REG_R0);index=struct.unpack('<I',u.mem_read(owner+8,4))[0]
            assert index<32;rings.append(dict(owner=owner,counter_address=owner+8,source_index=index,output_slot=owner+12+index*128))
        h=cpu.hook_add(UC_HOOK_CODE,ring,begin=0x020AC000,end=0x020AC000)
        w=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,d:writes.append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=address,size=size,value=value)),begin=0x02000000,end=0x023fffff)
        try:ptr=get(fn-0x02000000,actor)
        finally:cpu.hook_del(h);cpu.hook_del(w)
        value=bytes(cpu.mem_read(ptr,80)).split(b'\0')[0].decode('cp932')
        restored=bytearray(cpu.mem_read(0x02000000,0x400000))
        if ident<82:
            assert len(rings)==1 and ptr==rings[0]['output_slot']
            r=rings[0];counter=r['counter_address'];end=ptr+len(value.encode('cp932'))+1
            for write in writes:
                if write['address']==counter:
                    assert write['PC'] in [0x020AC00C,0x020AC020] and write['size']==4
                else:assert ptr<=write['address'] and write['address']+write['size']<=end and write['size']==1 and write['PC'] in [0x020CED7C,0x020CED90,0x020CEDAC,0x020CEDC0]
            assert struct.unpack('<I',cpu.mem_read(counter,4))[0]==(r['source_index']+1)%32
            for start,stop in [(counter,counter+4),(ptr,end)]:
                restored[start-0x02000000:stop-0x02000000]=prior[start-0x02000000:stop-0x02000000]
                cpu.mem_write(start,prior[start-0x02000000:stop-0x02000000])
            scratch.append(dict(actor_ID=ident,original_ring=r,source_owned_output_bytes=end-ptr,original_getter_writes=writes))
        else:assert not rings and not writes
        assert bytes(restored)==prior and bytes(cpu.mem_read(0x02000000,0x400000))==prior
        results.append(dict(actor_ID=ident,actor_object=actor,getter=fn,pointer=ptr,current_catalog_name=value,original_voice_class=voice))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(rows=results,source_owned_original_name_ring_scratch=scratch,all_actor_models_and_unowned4MiB_exact=True,original_name_ring_scratch_restored_recovers_all4MiB=True,current_executed_instruction_addresses=len(provider.executed_current))


def dynamic(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan)
    before=bytes(cpu.mem_read(0x02000000,0x400000));root=get(0xCB184);captain=get(0x7F244)
    controller=get(0xCB1A8)+0x2090;rows=[]
    for prefix in [207,208]:
        role=prefix-207;strict=get(0x825E4,controller,role);selected=get(0x82478,controller,role);resolved=get(0x2434C,prefix)
        assert selected==resolved
        actor=None if resolved>=207 else root+0x19E4 if resolved==captain else root+4+32*resolved
        voice=None if actor is None else get(0x7E988,actor)
        rows.append(dict(source_selector=prefix,role_index=role,strict_assignment=strict,original_speech_fallback_actor=selected,resolved_actor_ID=resolved,actor_object=actor,source_voice_class=voice))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    assert rows[0]['resolved_actor_ID']==captain==2
    return dict(rows=rows,all_actor_role_RNG_and_unowned4MiB_exact=True,current_executed_instruction_addresses=len(provider.executed_current),historical_London_context_not_selected_new_scene_participation=True)

if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);ROOT.mkdir(parents=True);image=NdsImage.open(source['current_ROM'])
    contextpath=ROOT/'historical_source_context.json';save(contextpath,dict(actual_snapshot=source['actual_historical_snapshot'],actual_snapshot_sha256=source['actual_historical_snapshot_sha256']))
    inputpath=ROOT/'current_native_input.json';save(inputpath,dict(current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],current_ARM9_sha256=source['current_ARM9_sha256'],current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),native_context_proof=str(contextpath)))
    ctx=CurrentContext(inputpath,source['historical_snapshot_ROM'],ROOT/'current_context')
    result=ctx.execute(names);ctx.machines.pop();roles=ctx.execute(dynamic);ctx.machines.pop();assert not ctx.machines
    assert len(result['rows'])==207 and {r['original_voice_class']for r in result['rows']}==set(range(8))
    byid={r['actor_ID']:r for r in result['rows']}
    static=sorted({r['source_selector'] for r in source['records']if r['source_selector']<207})
    save(ROOT/'current_catalog207_eight_voice_groups_and_dynamic_CF_D0.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),catalog=result,dynamic_selectors=roles,
        eight_voice_groups={str(i):[dict(actor_ID=r['actor_ID'],current_name=r['current_catalog_name'])for r in result['rows']if r['original_voice_class']==i]for i in range(8)},selected_static_source_selectors={str(i):byid[i]for i in static},
        dynamic_CF_is_original_role0_captain_and_D0_role1_with_original_fallback=True,source_4100_style_comes_from_original_actor_record_byte1C=True,
        no_roster_role_event_RNG_or_outcome_fixture=True,original_name_ring_ownership_reused_not_new_runtime_repair=True,current_native_input=str(inputpath),current_native_input_sha256=sha(inputpath.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        no_new_nameplate_observation_or_name_asset_change=True,new_emulator_runs=0,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Current207actor catalog/eightvoices andCF/D0native roles pass;allunownedstate exact;source-ownedname rings restored.')
    print('STATIC',{i:byid[i]['current_catalog_name']for i in static})
    print('DYNAMIC',roles['rows'])
    print('CORE VOICES',{i:byid[i]['original_voice_class']for i in range(2,23)})
