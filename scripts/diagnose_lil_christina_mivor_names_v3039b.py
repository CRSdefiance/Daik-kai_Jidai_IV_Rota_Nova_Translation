"""Current registered actor catalog and contextual identity reconciliation."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Christina_Mivor_names_v3039b')
SOURCE=Path('work/analysis/lil_Christina_Mivor_source_v3035/complete145_clean_current_native_context.json')
def names(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(0x02000000,0x400000));root=get(0xCB184);assert get(0x7F244)==2
    results=[];writes=[]
    hook=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,d:writes.append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=address,size=size,value=value)),begin=0x02000000,end=0x023fffff)
    for ident in [6,7,79,162,167]:
        actor=root+4+32*ident;vt=struct.unpack('<I',cpu.mem_read(actor,4))[0];fn=struct.unpack('<I',cpu.mem_read(vt+8,4))[0]
        ptr=get(fn-0x02000000,actor);value=bytes(cpu.mem_read(ptr,80)).split(b'\0')[0].decode('cp932')
        results.append(dict(actor_ID=ident,actor_object=actor,getter=fn,pointer=ptr,current_catalog_name=value))
    cpu.hook_del(hook);after=bytes(cpu.mem_read(0x02000000,0x400000));changes=[dict(address=0x02000000+i,before=a,after=b) for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]
    return dict(rows=results,native_writes=writes,changed_bytes=changes,current_executed_instruction_addresses=len(provider.executed_current))
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_Christina_Mivor_controls_v3037/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context');result=ctx.execute(names);ctx.machines.pop();assert not ctx.machines
    save(ROOT/'current_catalog_getter_write_diagnostic.json',dict(result=result,source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_approval_or_credit=True,full_goal_complete=False))
    print(result)
