"""Inspect original2000 behavior; retain the failed uninitialized-context probe."""
import struct
from collections import deque
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn import UC_HOOK_CODE,UcError
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B122_2000_diagnostic_v3260b')
if __name__=='__main__':
    assert not ROOT.exists();image=NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[122]
    inventory,_,_=scoped_inventory();walk=inventory.__globals__['walk'];structural=walk(arm,block);effects=[b for b in structural['opaque_effect_bridges'] if b['source_offset'] in [58,228]]
    cpu=machine(arm);stream,owner,result,length=0x02660000,0x02662000,0x02664000,0x02664100
    cpu.mem_write(stream-16,b'\xa5'*(len(block)+32));cpu.mem_write(stream,block);cpu.mem_write(owner,struct.pack('<4I',0,stream+58,0,0));cpu.mem_write(result,bytes(24));cpu.mem_write(length,bytes(4));trace=deque(maxlen=60)
    h=cpu.hook_add(UC_HOOK_CODE,lambda u,pc,z,d:trace.append(pc));error=None
    try:call(cpu,0x2A510,(result,owner,length,0),instruction_limit=100000)
    except UcError as e:error=str(e)
    finally:cpu.hook_del(h)
    regs={k:cpu.reg_read(r) for k,r in [('pc',UC_ARM_REG_PC),('r0',UC_ARM_REG_R0),('r1',UC_ARM_REG_R1),('r2',UC_ARM_REG_R2),('r3',UC_ARM_REG_R3)]};md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    disassembly=[]
    for pc in trace:
        if 0x02000000<=pc<0x02000000+len(arm):
            at=pc-0x02000000;ins=list(md.disasm(arm[at:at+4],pc));disassembly.extend(hex(i.address)+' '+i.mnemonic+' '+i.op_str for i in ins)
    ROOT.mkdir(parents=True);save(ROOT/'original2000_structural_bridges_and_context_fault.json',dict(source_block_sha256=sha(block),native_structural_effect_boundaries=effects,isolated_uninitialized_context_fault=error,last_registers=regs,last60_original_instructions=disassembly,no_source_resident_text_extent_proven_only_under_structural_effect_bridges=True,pure_no_effect_decoder_assumption_rejected=True,full_current_context_and_original_side_effect_binding_required=True,failed_producer='scripts/map_lil_B122_B127_source_v3260.py',failed_producer_sha256=sha(Path('scripts/map_lil_B122_B127_source_v3260.py').read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_or_editorial_credit=True,full_goal_complete=False))
    print('BRIDGES',effects);print('FAULT',error,regs);print('\n'.join(disassembly))
