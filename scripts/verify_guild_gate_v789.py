"""Original Guild money/First Mate availability predicate at its real bounds."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC,UC_ARM_REG_LR,UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_item_roles_v789 import set_condition
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import STACK
from scripts.verify_village_wrap_v608 import save


def main():
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/item_roles_v789_live/frame_003200_arm9_ram.bin').read_bytes()
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    rows=[]
    for version in (783,788):
        rom=NdsImage.open(f'out/all_routes_combined_v{version}_candidate.nds')
        arm=rom.read_file('/__arm9__.bin')
        assert arm[0x5B26C:0x5B324]==clean[0x5B26C:0x5B324]
        table=struct.unpack_from('<I',arm,0x5B31C)[0]
        data=arm[table-0x02000000:table-0x02000000+48]
        assert len(data)==48
        for assigned in (False,True):
            fixture=set_condition(arm,raw,{'mode':'item-and-letter-roles'})[0] if assigned else raw
            for funds in (999,1000):
                cpu=machine(arm);cpu.mem_write(0x02000000,fixture)
                call(cpu,0xCB1A8,());controller=cpu.reg_read(UC_ARM_REG_R0)+0x2090
                call(cpu,0x825E4,(controller,1));actor=cpu.reg_read(UC_ARM_REG_R0)
                assert actor==(10 if assigned else 208)
                cpu.mem_write(STACK+0xC,data)
                cpu.reg_write(UC_ARM_REG_SP,STACK)
                observed=[]
                def amount(c,pc,size,unused):
                    observed.append(c.reg_read(UC_ARM_REG_R0))
                    c.reg_write(UC_ARM_REG_R0,funds)
                    c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
                hook=cpu.hook_add(UC_HOOK_CODE,amount,begin=0x0203CCC8,end=0x0203CCC8)
                try: cpu.emu_start(0x0205B2A0,0x0205B2EC,count=100000)
                finally: cpu.hook_del(hook)
                assert len(observed)==1
                fields=struct.unpack('<2I',cpu.mem_read(STACK+0x30,8))
                initial=struct.unpack_from('<2I',data,0x24)
                assert initial==(1,1)
                enabled=assigned and funds>=1000
                assert fields==(initial if enabled else (0,0))
                rows.append({'version':version,'assigned_First_Mate':actor,'declared_cash_getter_result':funds,
                    'original_menu_flags':list(fields),'document_entry_enabled':enabled})
    save('work/analysis/item_transactions_v789/Guild_menu_gate.json',{'all8_original_predicate_cases':rows,
        'source_fragment':[0x0205B2A0,0x0205B2EC],'source_fragment_sha256':sha(clean[0x5B2A0:0x5B2EC]),
        'only_cash_getter_stubbed_to_declared_scalar_boundary_values':True,
        'real_company_and_role_providers_and_source_menu_table_execute_unchanged':True,
        'actual_earned_funds_assignment_and_all_other_document_type_conditions_not_claimed':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight original Guild entry cases prove >=1000 coins plus an assigned First Mate;999 and unassigned controls remain disabled.',flush=True)


if __name__ == '__main__': main()
