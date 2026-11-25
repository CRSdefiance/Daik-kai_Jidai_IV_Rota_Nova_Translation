"""Original six-type menu,real targets and exact Speech/proof boundaries."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_PC,UC_ARM_REG_SP,UC_ARM_REG_LR

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_letter_eligibility_v790 import set_condition
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import STACK,STOP
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/letter_eligibility_v790')
RAM=Path('E:/Rota Nova translations/Generated/work/emulation_v193/letter_eligibility_v790_live/frame_003200_arm9_ram.bin')


def menu(arm,raw,speech=None):
    cpu=machine(arm);cpu.mem_write(0x02000000,raw)
    observed=[]
    def score(c,at,size,data):
        assert c.reg_read(UC_ARM_REG_R1)==7
        observed.append(c.reg_read(UC_ARM_REG_R0))
        c.reg_write(UC_ARM_REG_R0,speech)
        c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
    hook=cpu.hook_add(UC_HOOK_CODE,score,begin=0x0207DCC8,end=0x0207DCC8) if speech is not None else None
    cpu.reg_write(UC_ARM_REG_R0,0);cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
    try:cpu.emu_start(0x0205B324,0x0205B490,count=2000000)
    finally:
        if hook is not None:cpu.hook_del(hook)
    sp=cpu.reg_read(UC_ARM_REG_SP)
    flags=[struct.unpack('<I',cpu.mem_read(sp+0x10+i*16,4))[0] for i in range(6)]
    if speech is not None:assert len(observed)==1
    return flags


def main():
    raw=RAM.read_bytes();rows=[];fixtures=[]
    for version in (783,788):
        arm=NdsImage.open(f'out/all_routes_combined_v{version}_candidate.nds').read_file('/__arm9__.bin')
        qualified,proof=set_condition(arm,raw,{'mode':'Istanbul-letter-eligibility'})
        fixtures.append(proof)
        flags=menu(arm,qualified)
        assert flags==[1]*6
        rows.append({'version':version,'case':'real native Speech215 and all source targets','flags':flags})
        for speech in (79,80,99,100,119,120,199,200):
            flags=menu(arm,qualified,speech)
            assert flags==[1,int(speech>=80),int(speech>=100),int(speech>=120),1,int(speech>=200)]
            rows.append({'version':version,'case':'declared Speech scalar boundary','Speech':speech,'flags':flags})
        cpu=machine(arm);cpu.mem_write(0x02000000,qualified)
        call(cpu,0xCB190,());item=cpu.reg_read(UC_ARM_REG_R0)+4+149*20
        missing=bytearray(qualified);missing[item+17-0x02000000]&=~4
        flags=menu(arm,bytes(missing),200)
        assert flags==[1,1,1,1,1,0]
        rows.append({'version':version,'case':'Speech200 without regional proof acquired flag','flags':flags})
        flags=menu(arm,raw)
        assert flags==[1,0,0,0,0,0]
        rows.append({'version':version,'case':'unmodified no First Mate;outer Guild entry separately disabled','flags':flags})
    assert len(rows)==22
    save(ROOT/'native_eligibility_verification.json',{'all22_original_menu_predicate_cases':rows,
        'all12_real_mode_target_lists':[{'version':v,'lists':p['all_six_original_target_filters']} for v,p in zip((783,788),fixtures)],
        'actual_RAM_source':str(RAM),'actual_RAM_sha256':sha(raw),'fixture_proofs':fixtures,
        'complete_source_constructor_before_SDK_rendering':[0x0205B324,0x0205B490],
        'real_native_positive_cases_have_no_stubs':True,
        'boundary_cases_stub_only_Speech_getter_to_declared_scalar':True,
        'source_role_faction_region_proof_and_candidate_filters_execute_unchanged':True,
        'fixture_producer_sha256':sha(Path('scripts/native_letter_eligibility_v790.py').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('22 original six-type eligibility cases and both complete six-mode target lists pass;no menu flag overrides.',flush=True)


if __name__=='__main__':main()
