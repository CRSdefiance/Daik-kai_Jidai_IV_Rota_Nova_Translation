"""Trace original53F0C ->54058 -> printf/macro -> speech formatter frame.

Only portrait UI construction is bridged; original prologue, table selection,
COMMON copy, printf and macro code run. Stop before the formatter is executed.
"""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, STOP
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/escape_direct_frame_v1182')


def main():
    assert not ROOT.exists()
    rom=NdsImage.open('out/all_routes_combined_v1166_candidate.nds')
    arm=rom.read_file('/__arm9__.bin')
    path=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_escape_v1179_1166_compassAttack8/frame_006902_arm9_ram.bin')
    raw=path.read_bytes();cpu,get=get_machine(arm,raw)
    actor=get(0xCB184)+4+18*32
    assert get(0x53F4C,actor,0x02117620)==1973
    frames=[]
    def observe(u,pc,size,data):
        if pc==0x0205408C:
            # Jump over UI/portrait object construction only. sl,sb,fp and
            # the original244-byte frame have already been set by native code.
            u.reg_write(UC_ARM_REG_PC,0x02054144)
        else:
            sp=u.reg_read(UC_ARM_REG_SP)
            values=[struct.unpack('<I',u.mem_read(sp+off,4))[0] for off in (0x264,0x270,0x274,0x27C)]
            frames.append({'formatter_entry':pc,'SP':sp,'frame_offsets':dict(zip(map(hex,(0x264,0x270,0x274,0x27C)),values)),
                'R1_text_hex':bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1),128)).split(b'\0')[0].hex()})
            u.emu_stop()
    cpu.hook_add(UC_HOOK_CODE,observe,begin=0x0205408C,end=0x0205408C)
    cpu.hook_add(UC_HOOK_CODE,observe,begin=0x01FFCF3C,end=0x01FFCF3C)
    cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
    cpu.reg_write(UC_ARM_REG_R0,actor);cpu.reg_write(UC_ARM_REG_R1,0x02117620)
    cpu.emu_start(0x02053F0C,STOP,count=3000000)
    assert len(frames)==1 and cpu.reg_read(UC_ARM_REG_PC)==0x01FFCF3C
    assert frames[0]['frame_offsets']['0x264']==0x02053F40
    assert frames[0]['frame_offsets']['0x274']==0x02117620
    ROOT.mkdir(parents=True)
    save(ROOT/'original_direct_frame_contract.json',{'ROM_sha256':sha(Path('out/all_routes_combined_v1166_candidate.nds').read_bytes()),
        'source_snapshot':str(path),'source_snapshot_sha256':sha(raw),'frames':frames,
        'correct_contract':[0x02053F40,0x274,0x0211,[0x7500,0x7620]],
        'V1152_53DB8_27C_membership_is_wrong_for_this_direct_original_consumer':True,
        'original53F0C_prologue_selection_copy_printf_and_macro_execute':True,
        'portrait_UI_construction_only_is_a_CPU_boundary_not_actual_gameplay':True,
        'not_a_ROM_or_completion_credit_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Original direct frame proven:parent02053F40,table at+274,high0211; no queued-parent assumption.')


if __name__=='__main__':main()
