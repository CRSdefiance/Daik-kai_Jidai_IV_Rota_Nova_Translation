"""Original ordinary Cabin helper selects every reviewed private comment."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/personal_chatter_v841')


def main():
    rom=Path('out/all_routes_combined_v838_candidate.nds')
    arm=NdsImage.open(rom).read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert all(arm[a:b]==clean[a:b] for a,b in ((0x12104,0x122A4),(0x1278C,0x12920),(0x82BA8,0x82BD0)))
    assert struct.unpack_from('<I',arm,0x128B0)[0]==struct.unpack_from('<I',arm,0x12918)[0]==1361
    source=Path('E:/Rota Nova translations/Generated/work/emulation_v193/personal_cabin_v840_838_Charles_after/frame_003800_arm9_ram.bin')
    raw=source.read_bytes()
    cases=[]
    for actor in range(25):
        cpu=machine(arm)
        cpu.mem_write(0x02000000,raw)
        def get(at,*args):
            call(cpu,at,args)
            return cpu.reg_read(UC_ARM_REG_R0)
        controller=get(0xCB1A8)+0x2090
        model=get(0x82E04,controller)
        assert get(0x132C0,model,12)==12
        # Declared isolated CPU bank setup. No live emulator/party/health edits.
        for slot in range(31):
            if get(0x82BC4,controller,slot)==actor:
                get(0x82BA8,controller,slot)
        get(0x82BB8,controller,12,actor)
        assert get(0x81F54,controller,actor)==12
        helper=0x128B4 if actor<4 else 0x1278C
        chosen=[]
        def numeric(u,pc,size,unused):
            chosen.append(u.reg_read(UC_ARM_REG_R0))
            u.reg_write(UC_ARM_REG_R0,0x02450000)
            u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
        hook=cpu.hook_add(UC_HOOK_CODE,numeric,begin=0x0205528C,end=0x0205528C)
        try:
            get(helper,actor)
        finally:
            cpu.hook_del(hook)
        assert chosen==[1361+actor]
        cases.append({'actor_ID':actor,'original_role_helper':hex(0x02000000+helper),
            'source_native_role_type':12,'selected_message_ID':chosen[0],
            'complete_original_numeric_helper_and_ABI_pass':True})
    save(ROOT/'ordinary_Cabin_context_verification.json',{
        'candidate_sha256':sha(rom.read_bytes()),'source_capture':str(source),'source_capture_sha256':sha(raw),
        'source_code_spans_and_both1361_bases_equal_clean':True,
        'all25_original_Cabin_role_helper_selections':cases,
        'ordinary12104_state0_path':'For healthy actors with source mood1..3 and context not[0,1],12104 calls128B4 for protagonists0..3 or1278C for actors4..24. Role12/16 selects1361+actor. The real Cabin has source type12.',
        'helper_probe_does_not_replace_health_mood_or_claim25_actual_visits':True,
        'actual_complete12104_and_visible_pixels_bound_separately_in_gameplay_proof':True,
        'no_ROM_live_RAM_save_or_ownership_changes':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('All25 ordinary Cabin role-helper IDs pass;actual whole-selector and display coverage remain explicitly sampled.',flush=True)


if __name__=='__main__':
    main()
