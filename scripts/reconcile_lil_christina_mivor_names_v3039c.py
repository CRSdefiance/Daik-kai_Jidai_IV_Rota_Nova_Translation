"""Current registered actor catalog and contextual identity reconciliation."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Christina_Mivor_names_v3039c')
SOURCE=Path('work/analysis/lil_Christina_Mivor_source_v3035/complete145_clean_current_native_context.json')
def names(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(0x02000000,0x400000));root=get(0xCB184);assert get(0x7F244)==2
    results=[];scratch=[]
    assert arm[0xAC000:0xAC02C]==NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')[0xAC000:0xAC02C]
    for ident in [6,7,79,162,167]:
        actor=root+4+32*ident;vt=struct.unpack('<I',cpu.mem_read(actor,4))[0];fn=struct.unpack('<I',cpu.mem_read(vt+8,4))[0]
        prior=bytes(cpu.mem_read(0x02000000,0x400000));rings=[];writes=[]
        def ring(u,pc,size,unused):
            owner=u.reg_read(UC_ARM_REG_R0);index=struct.unpack('<I',u.mem_read(owner+8,4))[0]
            assert index<32;rings.append(dict(owner=owner,counter_address=owner+8,source_index=index,output_slot=owner+12+index*128))
        h=cpu.hook_add(UC_HOOK_CODE,ring,begin=0x020AC000,end=0x020AC000)
        w=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,d:writes.append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=address,size=size,value=value)),begin=0x02000000,end=0x023fffff)
        try:ptr=get(fn-0x02000000,actor)
        finally:cpu.hook_del(h);cpu.hook_del(w)
        value=bytes(cpu.mem_read(ptr,80)).split(b'\0')[0].decode('cp932');expected={6:'Julio Erneco',7:'Cristina Erneco',79:'Mivor Genz',162:'Boy',167:'Lady'}[ident];assert value==expected
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
        results.append(dict(actor_ID=ident,actor_object=actor,getter=fn,pointer=ptr,current_catalog_name=value))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(rows=results,source_owned_original_name_ring_scratch=scratch,all_actor_models_and_unowned4MiB_exact=True,original_name_ring_scratch_restored_recovers_all4MiB=True,current_executed_instruction_addresses=len(provider.executed_current))
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_Christina_Mivor_controls_v3037/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context');result=ctx.execute(names);ctx.machines.pop();assert not ctx.machines
    byid={r['actor_ID']:r for r in result['rows']};assert byid[79]['current_catalog_name']=='Mivor Genz' and byid[162]['current_catalog_name']=='Boy' and byid[167]['current_catalog_name']=='Lady'
    save(ROOT/'current_registered_names_and_source_identity_contract.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),**result,
        Mivor_full_name='Mivor Genz',provisional_source_packet_Gentz_annotation_superseded_not_original_Japanese=True,
        approved_Christina_spelling_retained_legacy_Cristina_catalog_not_edited=True,Julio_biological_grandfather_source_B72_R0176=True,
        Boy_FE_source_visible_label='Boy:',Boy_and_mother_actor162_167_and_nonkinship_familiar_addresses=True,
        failed_producer_preserved='scripts/reconcile_lil_christina_mivor_names_v3039.py',failed_assumption='Original full-name getter is not read-only: it increments its32slot128byte ring and formats the returned name. Exact original instruction-owned counter/output writes are bounded and restored in this successor. No ROM/runtime defect is asserted.',
        diagnostic='work/analysis/lil_Christina_Mivor_names_v3039b/current_catalog_getter_write_diagnostic.json',
        registered_name_config=source['registered_name_catalog_config'],registered_name_config_sha256=source['registered_name_catalog_config_sha256'],
        no_new_nameplate_observation_or_name_asset_change=True,new_emulator_runs=0,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(current_catalog={i:r['current_catalog_name'] for i,r in byid.items()},all_unowned_state_exact=True,no_editorial_credit=True))
