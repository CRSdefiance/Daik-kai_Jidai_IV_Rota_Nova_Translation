"""Source-bound actor/null routing for the original recruiting callers."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_tavern_recruitment_v771 import CURRENT,RAM_REPORT,ROOT as CONTEXT
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/recruitment_release_v773')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open(CURRENT);arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    raw=snapshot(read(RAM_REPORT),3200);u=machine(arm);u.mem_write(BASE,raw)
    # Fixed city metadata and role/culture mapping are immutable ROM constants,
    # not mutable story flags. Verify all114 original town objects,not just90.
    table=struct.unpack_from('<I',arm,0x7F1EC)[0];towns=[]
    for town in read(CONTEXT/'native_context.json')['actual114_native_town_objects']:
        call(u,0xB5690,(town['object'],));info=u.reg_read(UC_ARM_REG_R0)
        assert info==BASE+0x122560+town['index']*0x74
        assert bytes(u.mem_read(info,0x74))==arm[info-BASE:info-BASE+0x74]
        culture=arm[info-BASE+0x15]
        assert culture==clean[info-BASE+0x15]
        slot=table+culture*14+13
        assert bytes(u.mem_read(slot,1))==arm[slot-BASE:slot-BASE+1]==clean[slot-BASE:slot-BASE+1]
        npc_id=arm[slot-BASE];assert npc_id!=208
        call(u,0xB2CD8,(town['object'],13));actor=u.reg_read(UC_ARM_REG_R0);assert actor
        towns.append({'index':town['index'],'metadata':info,'immutable_culture':culture,'immutable_role13_NPC_ID':npc_id,'actor':actor})
    for lo,hi in((0x53CB0,0x53E4C),(0x54058,0x5408C),(0xB2CD8,0xB2D58),(0xB51B4,0xB51CC),(0xB5600,0xB562C),(0xB5690,0xB56A8),(0x7F1D4,0x7F1F4)):
        assert arm[lo:hi]==clean[lo:hi]
    rows=[];selected=[0];seen=[]
    def role(c,pc,size,unused):
        c.reg_write(UC_ARM_REG_R0,selected[0]);c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
    def voice(c,pc,size,unused):
        c.reg_write(UC_ARM_REG_R0,883);c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
    def loader(c,pc,size,unused):
        c.reg_write(UC_ARM_REG_R0,0x02479000);c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
    def portrait(c,pc,size,unused):seen.append(pc);c.emu_stop()
    u.mem_write(0x02479000,b' Admiral, we do not have enough money.\0')
    hooks=[u.hook_add(UC_HOOK_CODE,fn,begin=BASE+at,end=BASE+at) for fn,at in
        ((role,0x82478),(voice,0x53F4C),(loader,0x5528C),(portrait,0x5408C),(portrait,0x54774))]
    try:
        for wrapper,message in((0x53CB0,0x02118380),(0x53D44,0x021183A0),(0x53DCC,904)):
            for index in range(209):
                selected[0]=index;seen.clear()
                u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP)
                for reg,value in((UC_ARM_REG_R0,1),(UC_ARM_REG_R1,message),(UC_ARM_REG_R2,0x02479100)):u.reg_write(reg,value)
                u.emu_start(BASE+wrapper,STOP,count=20000)
                assert seen==[BASE+0x5408C]
                rows.append({'wrapper':BASE+wrapper,'supplied_role_index':index,'actual_core_branch':seen[0]})
    finally:
        for hook in hooks:u.hook_del(hook)
    save(ROOT/'consumer_routing.json',{'all114_immutable_city_cultures_and_role13_mappings':towns,
        'all627_source_wrapper_pointer_construction_cases':rows,
        'role_index_fixture_scope':'Only role-index provider,voice selection and message lookup stubbed to isolate original pointer construction;not627 real officer/voice/gameplay cases',
        'original_four_real_role_bindings_reference':str(CONTEXT/'native_context.json'),
        'original_source_callers_select_nonnull_portrait_core_for_this_family':True,
        'null_system_core_left_unchanged_not_claimed_newly_localized':True,
        'source_ROM_sha256':sha(CURRENT.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('114 immutable town/NPC mappings and627 original wrapper pointer cases select the portrait core;no legitimate new null consumer found.',flush=True)


if __name__=='__main__':main()
