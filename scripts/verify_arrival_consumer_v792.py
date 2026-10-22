"""Connect the original modal consumer, native printf and bounded wrapper."""

import struct

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_SP

from dk4tool.patch.arrival_notices_editorial import ROOT,compiled
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save
from scripts.verify_arrival_native_v792 import format_case,prepared


def main():
    arm=(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes()
    raw_path='E:/Rota Nova translations/Generated/work/emulation_v193/letter_delivery_v791_recovered/frame_017200_arm9_ram.bin'
    from pathlib import Path
    raw=Path(raw_path).read_bytes();rows=read('translations/arrival_notices_editorial_manuscript_v2.json')['records'];proof=[]
    for row in rows:
        cpu=machine(arm);cpu.mem_write(BASE,raw)
        s=MainCodeFile(arm,BASE).sections[4];cpu.mem_write(s.ramAddress,bytes(s.data))
        if row['message_id']==348:
            call(cpu,0xABF50,(5,));argument=cpu.reg_read(UC_ARM_REG_R0);value=bytes(cpu.mem_read(argument,32)).split(b'\0')[0]
        else:
            call(cpu,0xCB160,());obj=cpu.reg_read(UC_ARM_REG_R0)+4
            vt=struct.unpack('<I',cpu.mem_read(obj,4))[0];fn=struct.unpack('<I',cpu.mem_read(vt+8,4))[0]
            call(cpu,fn-BASE,(obj,));argument=cpu.reg_read(UC_ARM_REG_R0);value=bytes(cpu.mem_read(argument,128)).split(b'\0')[0]
            assert value==b'Castor Co.'
        seen=[];dest=[]
        def loader(c,pc,size,data):
            assert c.reg_read(UC_ARM_REG_R0)==row['message_id']
            c.mem_write(0x0247A000,compiled(row)+b'\0');c.reg_write(UC_ARM_REG_R0,0x0247A000);c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
        def modal(c,pc,size,data):
            sp=c.reg_read(UC_ARM_REG_SP)
            seen.append([struct.unpack('<I',c.mem_read(sp+0xC4,4))[0],struct.unpack('<I',c.mem_read(sp+0xD0,4))[0]])
            dest.append(c.reg_read(UC_ARM_REG_R0))
        hooks=[cpu.hook_add(UC_HOOK_CODE,fn,begin=BASE+at,end=BASE+at) for fn,at in ((loader,0x5528C),(modal,0x01FFC900-BASE))]
        cpu.reg_write(UC_ARM_REG_R0,row['message_id']);cpu.reg_write(UC_ARM_REG_R1,argument)
        cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
        try:cpu.emu_start(BASE+0x546B8,BASE+0x5479C,count=2000000)
        finally:
            for h in hooks:cpu.hook_del(h)
        assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x5479C
        assert seen==[[0x020546E8,row['message_id']]]
        expected=format_case(prepared(arm),row,value)
        text=bytes(cpu.mem_read(dest[0],256)).split(b'\0')[0]
        assert text.hex()==expected['formatted_hex']
        proof.append({'id':row['message_id'],'original_modal_parent_and_ID':seen[0],'value_hex':value.hex(),
            'formatted_hex':text.hex(),'original_printf_macro_expander_and_wrapper_execute':True,
            'lookup_selection_bridge_only':True,'complete_native_copies_verified_separately':True,
            'stop_before_original_SDK_widget_construction':True})
    save(ROOT/'consumer_proof.json',{'rows':proof,'RAM_source':raw_path,'RAM_sha256':sha(raw),
        'ARM9_sha256':sha(arm),'full_actual_GPU_presentation_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('All three original modal consumers bind real faction/number arguments and exact complete paragraphs.',flush=True)


if __name__=='__main__':main()
