"""Execute the original macro wrapper; account for its original full-name scratch ring."""
import struct
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC
from scripts.native_call_abi_v764 import call

def expand(arm,common,raw,plan,body,prefix):
    cpu,get,provider=machine(arm,common,raw,plan)
    root=get(0xCB184);captain=get(0x7F244);identity=get(0x2434C,prefix)
    assert identity==prefix and captain==2
    actor=root+0x19E4 if identity==captain else root+4+32*identity
    initial=bytes(cpu.mem_read(0x02000000,0x400000));cases=[]
    h=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x020242CC,end=0x020242CC)
    try:
        for phase in range(4):
            inp,out=0x02660000+phase,0x02662000
            cpu.mem_write(inp-16,b'\xA5'*2080);cpu.mem_write(inp,body+b'\0');input_before=bytes(cpu.mem_read(inp-16,2080))
            cpu.mem_write(out-16,b'\xA5'*4128);rings=[];writes=[]
            def ring(u,pc,size,data):
                owner=u.reg_read(UC_ARM_REG_R0);index=struct.unpack('<I',u.mem_read(owner+8,4))[0]
                assert index<32;rings.append(dict(owner=owner,counter_address=owner+8,source_index=index,output_slot=owner+12+index*128))
            rh=cpu.hook_add(UC_HOOK_CODE,ring,begin=0x020AC000,end=0x020AC000)
            wh=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,d:writes.append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=address,size=size,value=value)),begin=0x02000000,end=0x023fffff)
            try:call(cpu,0x242C8,(out,inp,actor),instruction_limit=400000)
            finally:cpu.hook_del(rh);cpu.hook_del(wh)
            value=bytes(cpu.mem_read(out,4096)).split(b'\0')[0];restored=bytearray(cpu.mem_read(0x02000000,0x400000))
            assert len(rings) in [0,1]
            if rings:
                r=rings[0];pointer=r['output_slot'];name=bytes(cpu.mem_read(pointer,128)).split(b'\0')[0]
                assert len(name)<128;counter=r['counter_address'];end=pointer+len(name)+1
                for w in writes:
                    if w['address']==counter:assert w['PC'] in [0x020AC00C,0x020AC020] and w['size']==4
                    else:assert pointer<=w['address'] and w['address']+w['size']<=end and w['size']==1 and w['PC'] in [0x020CED7C,0x020CED90,0x020CEDAC,0x020CEDC0],w
                assert struct.unpack('<I',cpu.mem_read(counter,4))[0]==(r['source_index']+1)%32
                for a,b in [(counter,counter+4),(pointer,end)]:
                    restored[a-0x02000000:b-0x02000000]=initial[a-0x02000000:b-0x02000000]
                    cpu.mem_write(a,initial[a-0x02000000:b-0x02000000])
            else:assert not writes
            assert bytes(restored)==initial and bytes(cpu.mem_read(0x02000000,0x400000))==initial
            assert bytes(cpu.mem_read(inp-16,2080))==input_before
            assert bytes(cpu.mem_read(out-16,16))==b'\xA5'*16 and bytes(cpu.mem_read(out+len(value)+1,4095-len(value)))==b'\xA5'*(4095-len(value))
            cases.append(dict(input_alignment=phase,output_hex=value.hex(),original_scratch_rings=rings,original_getter_writes=writes,
                original_macro_ABI_input_output_canaries_and_all_unowned4MiB_exact=True,
                source_owned_name_ring_restoration_recovers_complete4MiB=True))
    finally:cpu.hook_del(h)
    return dict(original_selector=identity,actor_object=actor,source_prefix=prefix,captain=captain,cases=cases,
        current_executed_instruction_addresses=len(provider.executed_current),original_242CC_UI_boundary_unexecuted=True,
        no_model_event_RNG_or_roster_mutation=True)
